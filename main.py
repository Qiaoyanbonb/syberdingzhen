import RPi.GPIO as GPIO
import time
from audio_meter import AudioMeter
from light_sensor import LightSensor
from rgb_led import setup as rgb_setup, set_color, destroy as rgb_destroy, colors
from audio_player import play_audio, stop_audio, AUDIO_FILES
from face_detection import detect_faces
from infrared_sensor import InfraredSensor  # 导入InfraredSensor类

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    rgb_setup()

def destroy():
    rgb_destroy()
    GPIO.cleanup()

def learning_mode(sensor, audio_meter, infrared_sensor):
    last_face_detected_time = time.time()
    start_time = time.time()
    audio_meter.start_stream()

    try:
        while True:
            # 检测挥手以退出学习模式
            if infrared_sensor.get_status() == 1:
                return "rest"  # 切换到休息模式

            face_detected = detect_faces()
            if face_detected == 1:
                print("Face detected")
                set_color(colors["green"])
                last_face_detected_time = time.time()
            elif face_detected == 0:
                print("No face detected")
                elapsed_time = time.time() - last_face_detected_time
                if elapsed_time > 20:
                    play_audio(AUDIO_FILES["cnm"])
                    time.sleep(6)
                    set_color(colors["red"])
                elif elapsed_time > 8:
                    play_audio(AUDIO_FILES["away"])
                    set_color(colors["blue"])
                    time.sleep(6)
            else:
                print("Error in face detection")

            light_status = sensor.read_photoresistor()
            print(f"Light status: {light_status}")
            if light_status == 0:
                play_audio(AUDIO_FILES["light"])
                set_color(colors["blue"])

            try:
                avg_rms = audio_meter.get_avg_rms()
                print(f"当前平均分贝值: {avg_rms:.2f} dB")
                if avg_rms < 53: # 测试结果，麦克风输入有问题，声音越大数值越小
                    play_audio(AUDIO_FILES["xbbz"])
                    set_color(colors["blue"])
                    time.sleep(3)
            except Exception as e:
                print(f"Audio stream error: {e}")

            if time.time() - start_time > 1200:  # 20分钟
                play_audio(AUDIO_FILES["final"])
                set_color(colors["off"])
                return "rest"  # 切换到休息模式

            time.sleep(0.5)  # 每秒检测一次
    finally:
        audio_meter.stop_stream()

def resting_mode(infrared_sensor):
    set_color(colors["off"])
    print("进入休息模式")
    play_audio(AUDIO_FILES["dzy"])
    time.sleep(6)
    play_audio(AUDIO_FILES["igs"])

    start_time = time.time()

    while True:
        # 检测挥手以退出休息模式
        if infrared_sensor.get_status() == 1:
            stop_audio()
            return "learn"  # 切换到学习模式

        if time.time() - start_time > 220:  # 220秒后播放完毕
            stop_audio()
            audio_meter = AudioMeter(device=2, channels=1)
            return "learn"  # 自动切换到学习模式

        time.sleep(1)

def main():
    GPIO.setmode(GPIO.BCM)  # 确保引脚编号模式只设置一次
    GPIO.setwarnings(False)
    sensor = LightSensor()
    infrared_sensor = InfraredSensor(pin=24)  # 初始化红外传感器
    audio_meter = AudioMeter(device=2, channels=1)

    setup()
    play_audio(AUDIO_FILES["welcome"])
    time.sleep(8)
    system_state = "learn"

    try:
        while True:
            if system_state == "learn":
                system_state = learning_mode(sensor, audio_meter, infrared_sensor)
            elif system_state == "rest":
                system_state = resting_mode(infrared_sensor)
    except KeyboardInterrupt:
        destroy()
    finally:
        destroy()

if __name__ == '__main__':
    main()