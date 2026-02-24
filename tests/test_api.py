import requests
import sys
import os
from utils import ensure_server_running

def test_transcribe(audio_file_path):
    url = "http://127.0.0.1:8000/api/transcribe"
    server_process, started_by_us = ensure_server_running()
    
    try:
        with open(audio_file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        json_data = response.json()
        print(json_data)
        
        if response.status_code == 200:
            if json_data.get("status") == "success":
                print("\n✅ Verification SUCCESS")
            else:
                print("\n❌ Verification FAILED: Status is not success")
        else:
             print("\n❌ Verification FAILED: Server returned error")

    except Exception as e:
        print(f"\n❌ Verification ERROR: {e}")
    finally:
        if started_by_us and server_process:
            print("\nShutting down server...")
            server_process.terminate()
            server_process.wait()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_api.py <path_to_audio_file>")
    else:
        test_transcribe(sys.argv[1])
