# Whisper Transcription Server

A FastAPI-based server for transcribing audio using OpenAI's Whisper model (`turbo`).

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [ffmpeg](https://ffmpeg.org/download.html) (Ensure it's in your PATH)

## Setup

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```

2.  Activate the virtual environment:
    - Windows: `.\venv\Scripts\activate`
    - Linux/Mac: `source venv/bin/activate`

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Start the server:
    ```bash
    uvicorn main:app --reload
    ```
    The server will start at `http://127.0.0.1:8000`.

2.  Transcribe an audio file:
    Send a `POST` request to `/api/transcribe` with the audio file.

    Example using `curl`:
    ```bash
    curl -X POST -F "file=@path/to/audio.mp3" http://127.0.0.1:8000/api/transcribe
    ```

    Example using Python:
    ```python
    import requests
    response = requests.post(
        "http://127.0.0.1:8000/api/transcribe",
        files={"file": open("audio.mp3", "rb")}
    )
    print(response.json())
    ```

## Testing

Run the included test script (requires generated or existing `silent.wav`):
```bash
python tests/generate_dummy_audio.py
python tests/test_api.py tests/silent.wav
```

You can also run the full test battery:
```bash
python tests/test_battery.py
```
