import gc
import board
import time
import math
import busio
import adafruit_bno055
import adafruit_bmp3xx
import pwmio
import displayio
import digitalio
from adafruit_motor import servo




phase = 0 #variable is changed when phase changes
max_alt = 0 #initialize max altitude as 0 first


#initialize all sensors and motors
i2c = busio.I2C(board.SCL, board.SDA, frequency=200000)  # uses board.SCL and board.SDA
bno = adafruit_bno055.BNO055_I2C(i2c)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
pwm = pwmio.PWMOut(board.D12, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=750, max_pulse=2450)
ascend_led = digitalio.DigitalInOut(board.D13)
ascend_led.direction = digitalio.Direction.OUTPUT
descend_led = digitalio.DigitalInOut(board.D10)
descend_led.direction = digitalio.Direction.OUTPUT

ascend_led.value



#phase 0 - initialize and counts down to the ready phase
def phase_initizalize():
    for countdown in range(10):
        print(10 - countdown)
        time.sleep(0.1)
    my_servo.angle = 75
    print("Roekt Ready.")
    return 1


#phase 1 - ready and check to make sure failsafes are ready in case of unexpected events
def phase_ready(ground, initial_pitch, initial_yaw):
    #TURN ON GREEN FOR READY
    ascend_led.value = True
    yaw_angle = math.atan2(bno.gravity[1], bno.gravity[0]) * (180/math.pi) #math to figure out yaw angle
    pitch_angle = (math.atan2(-bno.gravity[0],math.sqrt((bno.gravity[1] ** 2) + (bno.gravity[2] **2) ))) * (180/math.pi) #math to figure out pitch angle
    altitude = bmp.altitude #take current altitude of the rocket
    if (altitude - ground > 2): #compares current altitude of rocket to ground height to figure out when to change phase
        print("Switching to ascending phase.")
        return 2 #change to ascend phase
    #need pitch_angle and yaw_angle calculations
    elif (abs(abs(pitch_angle) - abs(initial_pitch)) > 30 or abs(abs(yaw_angle) - abs(initial_yaw)) > 30): #if either yaw angle or pitch angle deviates 30° from initial angles then activate failsafe and change to descend phase
        print("Switching to descend")
        return 3 #change to descend phase
    return 1


#phase 2 - during rocket's ascent
def phase_ascend(initial_pitch, initial_yaw, max_alt):
    yaw_angle = math.atan2(bno.gravity[1], bno.gravity[0]) * (180/math.pi) #math to figure out yaw angle
    pitch_angle = (math.atan2(-bno.gravity[0],math.sqrt((bno.gravity[1] ** 2) + (bno.gravity[2] **2) ))) * (180/math.pi) #math to figure out pitch angle
    current_alt = bmp.altitude #take current altitude of rocket
    if(current_alt > max_alt): #update max altitude if current altitude is above it
        max_alt = current_alt
    print("Max Alt: " + str(max_alt))
    print("Current Alt: " + str(current_alt))
    print("Difference: " + str(max_alt-current_alt))
    if(max_alt - current_alt > 2 or (abs(abs(pitch_angle) - abs(initial_pitch)) > 30 or abs(abs(yaw_angle) - abs(initial_yaw)) > 30)): #if either yaw angle or pitch angle deviates 30° from initial angles then activate failsafe and change to descend phase or if the current altitude of the rocket is 2 meters below the max altitude
        return 3, max_alt #change to descend phase
    print("Ascending")
    return 2, max_alt


#phase 3 - during the rocket's descent
def phase_descend():
    #TURN ON RED FOR DESCENT
    if (ascend_led.value):
        ascend_led.value = False
    descend_led.value = True
    print("Parachute Deployed.")
    for angle in range(75, 150, 9):  #0 - 150 degrees, 9 degrees at a time.
        my_servo.angle = angle #deploy the parachute by turning the servo
        time.sleep(0.01)
    time.sleep(2)
    for angle in range(150, 75, -9):  #0 - 150 degrees, 9 degrees at a time.
        my_servo.angle = angle #deploy the parachute by turning the servo
        time.sleep(0.01)


while True:
    if (phase == 0):
        phase = phase_initizalize()
        ground_height = bmp.altitude #takes the ground height of the rocket
        initial_yaw_angle = math.atan2(bno.gravity[1], bno.gravity[0]) * (180/math.pi) #sets initial yaw angle
        initial_pitch_angle = (math.atan2(-bno.gravity[0],math.sqrt((bno.gravity[1] ** 2) + (bno.gravity[2] **2) ))) * (180/math.pi) #sets initial pitch angle
    elif (phase == 1):
        phase = phase_ready(ground_height, initial_pitch_angle, initial_yaw_angle)
    elif (phase == 2):
        time.sleep(0.05)
        phase, max_alt = phase_ascend(initial_pitch_angle, initial_yaw_angle, max_alt)
    elif (phase == 3):
        phase_descend()
        print("servo reset")
        break
    time.sleep(0.01)