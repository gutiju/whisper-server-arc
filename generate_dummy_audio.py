import wave
import struct

def create_silent_wav(filename="silent.wav", duration=1.0, framerate=44100):
    n_frames = int(duration * framerate)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(framerate)
        
        # Write silence (zeros)
        for _ in range(n_frames):
            wav_file.writeframes(struct.pack('h', 0))

if __name__ == "__main__":
    create_silent_wav()
    print("Created silent.wav")
