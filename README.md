# Whisper Transcription Server

A FastAPI-based server for transcribing audio using OpenAI's Whisper model (`turbo`).

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [ffmpeg](https://ffmpeg.org/download.html) (Ensure it's in your PATH)

## Setup

1.  Create a virtual environment:
    ```bash
    python -m venv .venv
    ```

2.  Activate the virtual environment:
    - Windows: `.\.venv\Scripts\activate`
    - Linux/Mac: `source .venv/bin/activate`

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the server**:
    ```bash
    uvicorn main:app --reload
    ```
    The server will start at `http://127.0.0.1:8001` (or the port specified in `.env` via `PORT`).

2.  **API Documentation**:
    Interactive OpenAPI documentation is available at `http://127.0.0.1:8001/docs`.

3.  **Transcribe an audio file**:
    Send a `POST` request to `/api/transcribe` with the audio file. The response includes the transcription and the autodetected language.

    **Example using `curl`**:
    ```bash
    curl -X POST -F "file=@path/to/audio.wav" http://127.0.0.1:8001/api/transcribe
    ```

    Example using Python:
    ```python
    import requests
    response = requests.post(
        "http://127.0.0.1:8001/api/transcribe",
        files={"file": open("audio.mp3", "rb")}
    )
    print(response.json())
    ```

    **Example response**:
    ```json
    {
      "status": "success",
      "output": {
        "lang": "en",
        "text": "Hello world"
      }
    }
    ```

## Testing

The test scripts automatically launch the server if it is not already running.

1.  **Run a single transcription test**:
    ```bash
    python tests/test_api.py tests/silent.wav
    ```

2.  **Run the full test battery**:
    ```bash
    python tests/test_battery.py
    ```
