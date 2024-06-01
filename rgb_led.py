import RPi.GPIO as GPIO
import time

colors = {
    "red": 0xFF0000,
    "green": 0x00FF00,
    "blue": 0x0000FF,
    "yellow": 0xFFFF00,
    "cyan": 0x00FFFF,
    "magenta": 0xFF00FF,
    "white": 0xFFFFFF,
    "off": 0x000000
}

R_PIN = 17
G_PIN = 18
B_PIN = 27

p_R = None
p_G = None
p_B = None

def setup():
    global p_R, p_G, p_B
    GPIO.setup(R_PIN, GPIO.OUT)
    GPIO.setup(G_PIN, GPIO.OUT)
    GPIO.setup(B_PIN, GPIO.OUT)
    p_R = GPIO.PWM(R_PIN, 2000)
    p_G = GPIO.PWM(G_PIN, 2000)
    p_B = GPIO.PWM(B_PIN, 2000)
    p_R.start(0)
    p_G.start(0)
    p_B.start(0)

def pwm_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def led_off():
    GPIO.output(R_PIN, GPIO.LOW)
    GPIO.output(G_PIN, GPIO.LOW)
    GPIO.output(B_PIN, GPIO.LOW)

def set_color(col):
    R_val = (col & 0xff0000) >> 16
    G_val = (col & 0x00ff00) >> 8
    B_val = (col & 0x0000ff) >> 0
    R_val = pwm_map(R_val, 0, 255, 0, 100)
    G_val = pwm_map(G_val, 0, 255, 0, 100)
    B_val = pwm_map(B_val, 0, 255, 0, 100)
    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)
    p_B.ChangeDutyCycle(B_val)

def destroy():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    led_off()
    GPIO.cleanup()
