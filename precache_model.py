from huggingface_hub import snapshot_download

MODEL_ID = "OpenVINO/whisper-large-v3-int8-ov"
MODEL_DIR = "model_ov"

if __name__ == "__main__":
    print(f"Downloading {MODEL_ID}...")
    try:
        path = snapshot_download(repo_id=MODEL_ID, local_dir=MODEL_DIR)
        print(f"Successfully downloaded to {path}")
    except Exception as e:
        print(f"Failed to download: {e}")
        exit(1)
