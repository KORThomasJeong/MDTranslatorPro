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

### 1. 가상 환경(venv) 구성 (권장)
라이브러리 충돌을 방지하기 위해 가상 환경 사용을 권장합니다.

**Windows:**
```powershell
# 가상 환경 생성
python -m venv venv
# 가상 환경 활성화
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
# 가상 환경 생성
python3 -m venv venv
# 가상 환경 활성화
source venv/bin/activate
```

### 2. 필수 라이브러리 설치
가상 환경이 활성화된 상태에서 아래 명령어를 입력합니다.
```powershell
pip install -r requirements.txt
```

### 3. 프로그램 실행
```powershell
python main.py
```
실행 후 브라우저가 자동으로 열리지 않는다면 `http://127.0.0.1:8000`으로 접속하세요.

## 📦 .exe 실행 파일 만들기

사용자가 파이썬을 설치하지 않아도 실행할 수 있도록 모든 라이브러리를 하나로 묶어 `.exe` 파일로 빌드하는 방법입니다.

### 방법 1: .spec 파일 사용 (권장 ⭐)
이 방법은 Miniconda/Anaconda 환경을 자동으로 감지하여 DLL 문제를 방지합니다.

1. **PyInstaller 설치**:
   ```powershell
   pip install pyinstaller
   ```

2. **빌드 실행**:
   ```powershell
   # .spec 파일을 사용한 빌드
   python -m PyInstaller MD_Translator.spec
   ```

3. **콘솔 창 숨기기 (선택사항)**:
   `MD_Translator.spec` 파일을 열어서 `console=True`를 `console=False`로 변경

### 방법 2: 명령어로 직접 빌드

```powershell
# 일반 파이썬 환경
python -m PyInstaller --onefile --noconfirm --clean --add-data "templates;templates" --add-data "models.txt;." --name "MD_Translator" main.py

# Conda/Miniconda 환경 (DLL 경로 수동 지정)
python -m PyInstaller --onefile --noconfirm --clean --paths "%CONDA_PREFIX%\Library\bin" --add-data "templates;templates" --add-data "models.txt;." --name "MD_Translator" main.py
```

### 주요 옵션 설명
- **--onefile**: 모든 라이브러리와 정적 파일을 하나의 .exe에 통합
- **--add-data**: UI 파일(`templates/`)과 모델 설정(`models.txt`) 포함
- **--paths**: Conda 환경의 DLL 경로 지정 (OpenSSL 등)

### 결과 확인
- `dist` 폴더에 생성된 `MD_Translator.exe` 실행
- 파이썬 미설치 PC에서도 즉시 실행 가능
- 실행 시 CMD 창과 함께 웹 브라우저 자동 실행

### ⚠️ Miniconda/Anaconda 사용자 주의사항
- **에러**: `ImportError: DLL load failed` 또는 `ssl module not available`
- **원인**: Conda 환경의 DLL 파일(libssl, libcrypto 등)을 찾지 못함
- **해결**: 위의 "방법 1 (.spec 파일 사용)"을 사용하면 자동 해결됩니다

## ⚙️ 설정 방법
1. 브라우저 우측 **Settings** 패널에서 OpenAI API Key를 입력합니다.
2. 원하는 모델(GPT-4o 권장)과 출력 토큰 한도를 설정합니다.
3. **Save Settings** 버튼을 눌러 저장합니다.

## 📄 라이선스
이 프로젝트는 자유롭게 수정 및 배포가 가능합니다.
