import sounddevice as sd
import numpy as np
import time

class AudioMeter:
    def __init__(self, samplerate=44100, channels=1, blocksize=1024, device=None):
        self.samplerate = samplerate
        self.channels = channels
        self.blocksize = blocksize
        self.device = device
        self.stream = None
        self.rms_values = []

    def start_stream(self):
        try:
            self.stream = sd.InputStream(
                samplerate=self.samplerate,
                channels=self.channels,
                blocksize=self.blocksize,
                device=self.device,
                callback=self.audio_callback
            )
            self.stream.start()
            print("流启动成功。")
        except Exception as e:
            print(f"启动流时出错: {e}")

    def stop_stream(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            print("流已停止。")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"状态错误: {status}")
        rms = self.calculate_rms(indata)
        self.rms_values.append(rms)

    def calculate_rms(self, data):
        audio_data = np.sqrt(np.mean(data**2))
        return 20 * np.log10(audio_data)

    def get_avg_rms(self):
        if not self.rms_values:
            return 0
        avg_rms = np.mean(self.rms_values)
        self.rms_values = []  # 清空列表以便下一次计算
        return avg_rms*(-1)

if __name__ == "__main__":
    try:
        # 确保设备索引和通道数正确
        audio_meter = AudioMeter(device=2, channels=1)  # 尝试将 channels 设置为 1 或 2
        audio_meter.start_stream()

        # 每秒显示一次分贝值
        for _ in range(50):  # 运行10秒进行测试
            time.sleep(1)
            avg_rms = audio_meter.get_avg_rms()
            print(f"当前平均分贝值: {avg_rms:.2f} dB")

    except Exception as e:
        print(f"错误: {e}")
    finally:
        audio_meter.stop_stream()
