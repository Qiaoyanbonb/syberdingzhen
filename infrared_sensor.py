import RPi.GPIO as GPIO
import time

class InfraredSensor:
    def __init__(self, pin):
        self.ObstaclePin = pin
        self.last_state = 0  # 初始状态为无障碍
        GPIO.setup(self.ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_status(self):
        current_state = GPIO.input(self.ObstaclePin)

        if current_state == 0 and self.last_state == 1:
            self.last_state = 0
            return 1  # 检测到一次从无障碍到有障碍
        elif current_state == 1:
            self.last_state = 1  # 更新状态为无障碍
        return 0  # 没有检测到变化

    def destroy(self):
        GPIO.cleanup()

# 单独测试函数
def test_infrared_sensor(pin):
    GPIO.setmode(GPIO.BCM)  # 设置BCM编号模式
    infrared = InfraredSensor(pin=pin)  # 使用具体的引脚号

    try:
        while True:
            status = infrared.get_status()
            if status == 1:
                print("Detected an obstacle!")
            time.sleep(0.1)  # 延时避免频繁检测
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        infrared.destroy()

if __name__ == "__main__":
    test_infrared_sensor(pin=24)  # 使用引脚号进行测试
