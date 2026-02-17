import requests
import sys
import os

def run_tests():
    url = "http://127.0.0.1:8000/api/transcribe"
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
    
    for test in tests:
        file_path = test["filename"]
        if not os.path.exists(file_path):
            print(f"⚠️ Skipping {file_path}: File not found.")
            continue
            
        print(f"Testing {file_path}...")
        try:
            with open(file_path, "rb") as f:
                mod_time = os.path.getmtime(file_path)
                # Ensure we upload cleanly
                if file_path.endswith('.m4a'):
                     print("  (Type: m4a/audio/mp4)")
                
                response = requests.post(url, files={"file": f})
                
            if response.status_code != test["expected_status"]:
                print(f"❌ FAILED: Status code {response.status_code}, expected {test['expected_status']}")
                print(f"   Response: {response.text}")
                continue
                
            data = response.json()
            output = data.get("output", "").strip()
            
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

    print(f"\nSummary: {passed_count}/{len(tests)} tests passed.")

if __name__ == "__main__":
    run_tests()
