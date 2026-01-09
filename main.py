import os
import sys
import json
import asyncio
import webbrowser
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from openai import AsyncOpenAI
from langchain_text_splitters import MarkdownTextSplitter
import aiofiles

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Helper for PyInstaller paths
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Configuration storage
CONFIG_FILE = "config.json"
MODELS_FILE = get_resource_path("models.txt")
TRANSLATIONS_DIR = "translations"
os.makedirs(TRANSLATIONS_DIR, exist_ok=True)

class TranslationStatus:
    def __init__(self):
        self.progress = 0
        self.current_step = ""
        self.is_running = False
        self.should_stop = False
        self.result_file = ""
        self.preview = ""

status = TranslationStatus()

def load_config():
    # Priority: 1. config.json, 2. .env, 3. Defaults
    config = {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
        "max_tokens": int(os.getenv("MAX_TOKENS", 2048))
    }
    
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            saved_config = json.load(f)
            config.update(saved_config)
    return config

def get_available_models():
    default_models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
    if os.path.exists(MODELS_FILE):
        with open(MODELS_FILE, "r", encoding="utf-8") as f:
            models = [line.strip() for line in f if line.strip()]
            return models if models else default_models
    return default_models

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

@app.get("/", response_class=HTMLResponse)
async def index():
    template_path = get_resource_path("templates/index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/config")
async def get_config():
    return {
        "config": load_config(),
        "available_models": get_available_models()
    }

@app.post("/config")
async def update_config(api_key: str = Form(...), model: str = Form(...), max_tokens: int = Form(...)):
    config = {"api_key": api_key, "model": model, "max_tokens": max_tokens}
    save_config(config)
    return {"status": "success"}

@app.get("/status")
async def get_status():
    return {
        "progress": status.progress,
        "current_step": status.current_step,
        "is_running": status.is_running,
        "result_file": status.result_file,
        "preview": status.preview
    }

async def translate_chunk(client, chunk, config):
    prompt = f"""You are a professional translator specializing in Markdown documents. 
Translate the following English Markdown content into Korean.
Maintain all Markdown formatting (headers, lists, bold, italics, etc.).
DO NOT translate code blocks (content between ```) or inline code (content between `), but translate comments if any.
Ensure the tone is natural and professional.

Content to translate:
{chunk}
"""
    model_name = config["model"]
    
    # Prepare API parameters
    params = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}]
    }

    # Handle parameter differences for newer models (o1, o3, gpt-5 etc.)
    is_reasoning_model = any(m in model_name for m in ["o1", "o3", "gpt-5"])
    
    if is_reasoning_model:
        params["max_completion_tokens"] = config["max_tokens"]
        # Standard reasoning models MUST use temperature=1 as per OpenAI API rules.
        # They handle accuracy through internal reasoning tokens, not temperature.
        params["temperature"] = 1
    else:
        params["max_tokens"] = config["max_tokens"]
        # For standard models (gpt-4o, etc.), use 0 for maximum translation accuracy.
        params["temperature"] = 0

    try:
        response = await client.chat.completions.create(**params)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during translation: {e}")
        return f"\n[Translation Error: {str(e)}]\n"

@app.post("/translate")
async def start_translation(file: UploadFile = File(...)):
    config = load_config()
    if not config["api_key"]:
        raise HTTPException(status_code=400, detail="API Key is missing. Please set it in settings.")

    content = await file.read()
    text = content.decode("utf-8")
    
    # Intelligent Chunking
    splitter = MarkdownTextSplitter(chunk_size=2000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    
    status.should_stop = False
    asyncio.create_task(run_translation_task(chunks, file.filename, config))
    return {"status": "started"}

@app.post("/stop")
async def stop_translation():
    status.should_stop = True
    status.current_step = "Stopping translation..."
    return {"status": "stopping"}

async def run_translation_task(chunks, filename, config):
    global status
    status.is_running = True
    status.progress = 0
    status.current_step = "Starting translation..."
    status.preview = ""
    
    client = AsyncOpenAI(api_key=config["api_key"])
    translated_chunks = []
    
    total = len(chunks)
    for i, chunk in enumerate(chunks):
        if status.should_stop:
            status.current_step = "Translation stopped by user."
            status.is_running = False
            return

        status.current_step = f"Translating chunk {i+1} of {total}..."
        status.progress = int(((i) / total) * 100)
        
        translated = await translate_chunk(client, chunk, config)
        translated_chunks.append(translated)
        
        # Update preview (first few chunks)
        if i < 3:
            status.preview += translated + "\n\n"
            
    status.progress = 100
    status.current_step = "Finalizing..."
    
    final_text = "\n\n".join(translated_chunks)
    output_filename = f"ko_{filename}"
    output_path = os.path.join(TRANSLATIONS_DIR, output_filename)
    
    async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
        await f.write(final_text)
    
    status.result_file = output_filename
    status.is_running = False
    status.current_step = "Translation complete!"

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(TRANSLATIONS_DIR, filename)
    if os.path.exists(file_path):
        from fastapi.responses import FileResponse
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    # Open browser automatically
    webbrowser.open("http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
