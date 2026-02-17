from huggingface_hub import HfApi
api = HfApi()
models = api.list_models(author="OpenVINO", search="whisper", limit=20)
for model in models:
    print(model.id)
