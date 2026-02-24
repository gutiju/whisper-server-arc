import requests
import sys
import os
from utils import ensure_server_running

def run_tests():
    url = "http://127.0.0.1:8000/api/transcribe"
    server_process, started_by_us = ensure_server_running()

    tests = [
        {
            "filename": "silent.wav",
            "expected_status": 200,
            "expected_output_contains": "NorthstarIT.co.uk" # Hallucination check
        },
        {
            "filename": "test.m4a",
            "expected_status": 200,
            "expected_output": "What are the meetings that I have in my calendars for today?"
        }
    ]

    print(f"Running {len(tests)} tests against {url}...\n")
    
    passed_count = 0
    
    try:
        for test in tests:
            # Resolve file path relative to this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, test["filename"])
            
            if not os.path.exists(file_path):
                print(f"⚠️ Skipping {file_path}: File not found.")
                continue
                
            print(f"Testing {test['filename']}...")
            try:
                with open(file_path, "rb") as f:
                    response = requests.post(url, files={"file": f})
                    
                if response.status_code != test["expected_status"]:
                    print(f"❌ FAILED: Status code {response.status_code}, expected {test['expected_status']}")
                    print(f"   Response: {response.text}")
                    continue
                    
                data = response.json()
                output_data = data.get("output", {})
                if isinstance(output_data, dict):
                    output = output_data.get("text", "").strip()
                else:
                    output = str(output_data).strip()
                
                # Check assertion
                if "expected_output" in test:
                    if output == test["expected_output"]:
                        print(f"✅ PASSED: Output matches expected.")
                        passed_count += 1
                    else:
                        print(f"❌ FAILED: Output mismatch.")
                        print(f"   Expected: '{test['expected_output']}'")
                        print(f"   Actual:   '{output}'")
                elif "expected_output_contains" in test:
                    if test["expected_output_contains"] in output:
                        print(f"✅ PASSED: Output contains expected substring.")
                        passed_count += 1
                    else:
                        print(f"❌ FAILED: Output does not contain expected substring.")
                        print(f"   Expected substring: '{test['expected_output_contains']}'")
                        print(f"   Actual:             '{output}'")
                else:
                    print(f"✅ PASSED: Status code check only.")
                    passed_count += 1
                    
            except Exception as e:
                print(f"❌ ERROR: {e}")
    finally:
        if started_by_us and server_process:
            print("\nShutting down server...")
            server_process.terminate()
            server_process.wait()

    print(f"\nSummary: {passed_count}/{len(tests)} tests passed.")

if __name__ == "__main__":
    run_tests()
