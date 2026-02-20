import requests
import sys

def test_transcribe(audio_file_path):
    url = "http://127.0.0.1:8000/api/transcribe"
    try:
        with open(audio_file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(response.json())
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print("\n✅ Verification SUCCESS")
            else:
                print("\n❌ Verification FAILED: Status is not success")
        else:
             print("\n❌ Verification FAILED: Server returned error")

    except Exception as e:
        print(f"\n❌ Verification ERROR: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_api.py <path_to_audio_file>")
    else:
        test_transcribe(sys.argv[1])
