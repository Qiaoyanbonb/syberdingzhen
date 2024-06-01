import os
import subprocess
import time

AUDIO_FILES = {
    "welcome": "welcome.wav",
    "dzy": "dzy.wav",
    "igs": "igs.mp3",
    "light": "light.wav",
    "xbbz": "xbbz.wav",
    "away": "away.wav",
    "cnm": "cnm.wav",
    "final": "final.wav"
}

# 全局变量用于存储当前的音频播放进程
audio_process = None

def play_audio(file):
    global audio_process
    stop_audio()  # 在播放新的音频之前先停止当前的音频

    file_extension = os.path.splitext(file)[1].lower()

    try:
        if file_extension == '.mp3':
            audio_process = subprocess.Popen(["mpg123", "-q", file])
        elif file_extension == '.wav':
            audio_process = subprocess.Popen(["aplay", file])
        else:
            print(f"Unsupported file format: {file_extension}")
    except Exception as e:
        print(f"Error occurred: {e}")

def stop_audio():
    global audio_process
    if audio_process is not None:
        audio_process.terminate()  # 终止音频播放进程
        audio_process = None

if __name__ == "__main__":
    # 测试播放和停止功能
    play_audio(AUDIO_FILES["welcome"])
    time.sleep(5)
    stop_audio()