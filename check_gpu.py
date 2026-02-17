import sys

def check_gpu():
    print(f"Python version: {sys.version}")
    
    try:
        from openvino.runtime import Core
        core = Core()
        devices = core.available_devices
        print(f"OpenVINO Available Devices: {devices}")
        
        gpu_found = any("GPU" in d for d in devices)
        if gpu_found:
            print("Success: Intel GPU detected by OpenVINO!")
            for d in devices:
                if "GPU" in d:
                    print(f"Device: {d} - {core.get_property(d, 'FULL_DEVICE_NAME')}")
            return True
        else:
            print("Failure: OpenVINO did NOT detect a GPU.")
            return False
            
    except ImportError:
        print("OpenVINO not found.")
        return False
    except Exception as e:
        print(f"Error checking OpenVINO: {e}")
        return False

if __name__ == "__main__":
    if check_gpu():
        sys.exit(0)
    else:
        sys.exit(1)
