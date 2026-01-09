# MD Translator Pro 🚀

영문 Markdown(.md) 파일을 OpenAI API를 사용하여 한국어로 자동 번역해주는 지능형 번역 도구입니다.

## ✨ 주요 기능

- **지능형 문맥 청킹**: Markdown의 구조(헤더, 단락 등)를 분석하여 문맥이 끊기지 않게 적절한 크기로 자릅니다.
- **코드 블록 보호**: Markdown 내의 코드 블록(```)이나 인라인 코드(`)는 번역하지 않고 그대로 유지합니다.
- **모던 웹 GUI**: 드래그 앤 드롭을 지원하는 프리미엄 다크 모드 UI를 제공합니다.
- **실시간 상태 추적**: 번역 진행률(%), 현재 단계, 그리고 번역된 결과물의 미리보기를 실시간으로 확인할 수 있습니다.
- **설정 자동 저장**: API 키, 모델 선택(GPT-4o 등), 최대 토큰 설정을 `config.json`에 저장하여 재사용합니다.
- **자동 브라우저 실행**: 프로그램을 실행하면 기본 웹 브라우저가 자동으로 열립니다.

## 🛠 설치 및 실행 방법

### 1. 필수 라이브러리 설치
```powershell
pip install fastapi uvicorn openai langchain-text-splitters python-dotenv aiofiles jinja2 python-multipart
```

### 2. 프로그램 실행
```powershell
python main.py
```
실행 후 브라우저가 자동으로 열리지 않는다면 `http://127.0.0.1:8000`으로 접속하세요.

## 📦 .exe 실행 파일 만들기

사용자가 파이썬을 설치하지 않아도 실행할 수 있도록 모든 라이브러리를 하나로 묶어 `.exe` 파일로 빌드하는 방법입니다. 

1. **PyInstaller 설치**:
   ```powershell
   pip install pyinstaller
   ```

2. **빌드 실행 (추천 명령어)**:
   ```powershell
   pyinstaller --onefile --noconfirm --clean --add-data "templates;templates" --name "MD_Translator" main.py
   ```
   - **--onefile**: 모든 라이브러리와 정적 파일을 하나의 .exe에 통합합니다.
   - **--add-data**: UI 파일(`templates/`)을 실행 파일 안에 포함시킵니다.
   - **--clean**: 이전 빌드 캐시를 지우고 깨끗하게 빌드합니다.

3. **결과 확인**:
   - `dist` 폴더 안에 생성된 `MD_Translator.exe`를 실행하십시오.
   - 이 파일 하나만 있으면 파이썬이 설치되지 않은 다른 윈도우 PC에서도 즉시 실행 가능합니다.
   - 실행 시 CMD(콘솔) 창이 함께 뜨며, 웹 브라우저가 자동으로 열립니다.

## ⚙️ 설정 방법
1. 브라우저 우측 **Settings** 패널에서 OpenAI API Key를 입력합니다.
2. 원하는 모델(GPT-4o 권장)과 출력 토큰 한도를 설정합니다.
3. **Save Settings** 버튼을 눌러 저장합니다.

## 📄 라이선스
이 프로젝트는 자유롭게 수정 및 배포가 가능합니다.
