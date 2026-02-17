# Agent Instructions: Whisper Transcription Server

## Project Overview
This project builds a lightweight Python server that provides an API for audio transcription using OpenAI's Whisper model (local execution).

## Core Requirements
- **Language**: Python
- **Goal**: Create a server exposing a single endpoint.
- **Endpoint**: `POST /api/transcribe`
- **Input**: Audio file (`multipart/form-data`)
- **Output**: JSON response `{"status": "success/error", "output": "transcription text"}`

## Technical Stack
- **Web Framework**: **FastAPI** (with `python-multipart` for uploads).
- **Whisper Engine**: Local `openai-whisper` library.
- **Model**: `turbo`.
- **Dependency Management**: `pip` with `requirements.txt`.

## Environment
- **OS**: Windows
- **Hardware**: Local Execution.
