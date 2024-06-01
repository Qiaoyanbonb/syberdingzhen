import PCF8591 as ADC
import RPi.GPIO as GPIO
import time

class LightSensor:
    def __init__(self, adc_address=0x48, gpio_pin=17):
        self.adc_address = adc_address
        self.gpio_pin = gpio_pin
        GPIO.setmode(GPIO.BCM)
        self.setup()

    def setup(self):
        ADC.setup(self.adc_address)
        GPIO.setup(self.gpio_pin, GPIO.IN)

    def read_photoresistor(self):
        value = ADC.read(0)
        print('Photoresistor Value:', value)
        if value > 225:
            return 0
        else:
            return 1

    def cleanup(self):
        GPIO.cleanup()

# 示例主文件调用
if __name__ == '__main__':
    sensor = LightSensor()
    try:
        while True:
            result = sensor.read_photoresistor()
            print('Return Value:', result)
            time.sleep(0.2)
    except KeyboardInterrupt:
        sensor.cleanup()
