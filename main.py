import os
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile
import traceback
from pathlib import Path
from huggingface_hub import snapshot_download
import numpy as np
import scipy.io.wavfile

import json
# OpenVINO GenAI
import openvino_genai as ov_genai
from langdetect import detect
from pydantic import BaseModel, Field

class TranscriptionOutput(BaseModel):
    lang: str = Field(..., description="The autodetected language code (e.g., 'en', 'es')")
    text: str = Field(..., description="The transcribed text from the audio file")

class TranscriptionResponse(BaseModel):
    status: str = Field(..., description="The status of the request (e.g., 'success', 'error')")
    output: TranscriptionOutput = Field(..., description="The transcription result object")

app = FastAPI(
    title="Whisper Transcription Server",
    description="A lightweight API for audio transcription using OpenVINO GenAI and OpenAI's Whisper model.",
    version="1.0.0"
)

# Global variables
pipe = None
# Use pre-exported OpenVINO model
MODEL_ID = "OpenVINO/whisper-large-v3-int8-ov"
MODEL_DIR = "model_ov"

@app.on_event("startup")
async def load_model():
    global pipe
    print(f"Loading Whisper model '{MODEL_ID}' with OpenVINO GenAI...")
    try:
        # Download model
        print("Ensuring model is downloaded...")
        model_path = snapshot_download(repo_id=MODEL_ID, local_dir=MODEL_DIR)
        print(f"Model available at {model_path}")

        # Initialize pipeline
        # device="GPU" for Intel Arc
        device = "GPU"
        try:
            print(f"Initializing WhisperPipeline on {device}...")
            pipe = ov_genai.WhisperPipeline(model_path, device=device)
            print("Pipeline created successfully on GPU.")
        except Exception as e:
            print(f"Failed to initialize on GPU: {e}. Falling back to CPU.")
            pipe = ov_genai.WhisperPipeline(model_path, device="CPU")
            print("Pipeline created successfully on CPU.")

    except Exception as e:
        print(f"Error loading model: {e}")
        traceback.print_exc()
        raise e

@app.post("/api/transcribe", response_model=TranscriptionResponse, tags=["Transcription"])
async def transcribe_audio(file: UploadFile = File(...)):
    if not pipe:
        return JSONResponse(status_code=500, content={"status": "error", "output": "Model not loaded"})

    temp_audio_path = None
    try:
        suffix = f".{file.filename.split('.')[-1]}" if '.' in file.filename else ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name
            
        print(f"Transcribing {temp_audio_path}...")
        
        # Try processing audio data
        try:
            # Convert audio to 16kHz WAV using ffmpeg
            # ffmpeg -i input -ar 16000 -ac 1 -c:a pcm_s16le output.wav
            wav_path = temp_audio_path + ".converted.wav"
            try:
                import subprocess
                subprocess.run([
                    "ffmpeg", "-y", "-i", temp_audio_path,
                    "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
                    wav_path
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Read the converted file
                samplerate, data = scipy.io.wavfile.read(wav_path)
            except subprocess.CalledProcessError:
                print("FFmpeg failed to convert audio. Falling back to original file.")
                samplerate, data = scipy.io.wavfile.read(temp_audio_path)
                wav_path = None # Don't delete if we failed to create it? Or create check.
            except Exception as e:
                # If reading fails, re-raise to be caught by outer try? 
                # Or just let it fail to outer except
                raise e
                
            # OpenVINO GenAI generate
            MODEL_SAMPLE_RATE = 16000
            if samplerate != MODEL_SAMPLE_RATE:
                # Should have been fixed by ffmpeg, but double check
                print(f"Warning: Sample rate is {samplerate}, expected {MODEL_SAMPLE_RATE}.")

            
            # Whisper expects 16kHz float32
            # If samplerate != 16000, we might need resampling.
            # But let's assume input matches for now or library handles it?
            # Actually, standard Whisper requires 16k.
            # If we don't resample, result is bad.
            # For simplicity, let's try passing the file path AGAIN but maybe casting to str explicitly?
            # Or pass `input_ids`? No.
            # Let's try to pass raw samples.
            
            if data.dtype != np.float32:
                # Normalize to float32 -1.0 to 1.0
                if data.dtype == np.int16:
                    data = data.astype(np.float32) / 32768.0
                elif data.dtype == np.int32:
                    data = data.astype(np.float32) / 2147483648.0
                elif data.dtype == np.uint8:
                        data = (data.astype(np.float32) - 128.0) / 128.0
            
            # Pipeline.generate() expects list of floats? Or numpy array?
            # C++ API expects std::vector<float>.
            # Python binding usually accepts list or numpy array.
            
            result = pipe.generate(data.tolist()) # strict list?
            # Or data (numpy)
            # Let's try data.tolist() to be safe.
            
        except Exception as e:
             print(f"Failed to process audio data: {e}")
             # Retrying with path just in case
             result = pipe.generate(str(temp_audio_path))

        transcription = str(result)
        if hasattr(result, 'texts'):
             transcription = result.texts[0]
        elif isinstance(result, list):
             transcription = result[0]
             
        # Add language detection
        detected_lang = "unknown"
        if transcription.strip():
            try:
                detected_lang = detect(transcription.strip())
            except Exception:
                pass

        print(f"Transcription: {transcription.strip()}")
        print(f"Detected Language: {detected_lang}")

        return {
            "status": "success",
            "output": {
                "lang": detected_lang,
                "text": transcription.strip()
            }
        }

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": "error", "output": str(e)})
    finally:
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
            except:
                pass
        # Clean up converted file
        if 'wav_path' in locals() and wav_path and os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except:
                pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
