print("Dragon.py")

#
# 3       - Left Motor Servo
# 4       - Right Motor Servo
# 5       - Pan Servo
# 14 (A0) - Analog Sensor
# 15 (A1) - Left Whisker
# 16 (A1) - Right Whisker

SENSOR_PIN = 14
L_BUMP = 15
R_BUMP = 16 

SENSOR_THRESH = 400

DELAY_VAL = 700 # Delay for turning

LServo = pyb.Servo()
LServo.min_usecs(1000);
LServo.max_usecs(2000);
LServo.attach(3)

RServo = pyb.Servo()
RServo.min_usecs(1000);
RServo.max_usecs(2000);
RServo.attach(4);

panServo = pyb.Servo()
panServo.min_usecs(1000);
panServo.max_usecs(2000);
panServo.attach(5)

def Delay(msec):
    pyb.delay(msec)

def ReadBump(pin):
    return pyb.gpio(pin) == 0

def ReadSensor():
    return pyb.analogRead(SENSOR_PIN)

panServo.angle(90)
Delay(250)      # Give the pan servo time to get to where its going

def BumpTest():
    bump_L = ReadBump(L_BUMP)
    bump_R = ReadBump(R_BUMP)
    while bump_L or bump_R:
        if bump_L:
            MotorsL()
        else:
            MotorsR()
        Delay(100)
        bump_L = ReadBump(L_BUMP)
        bump_R = ReadBump(R_BUMP)

def MotorsFwd():
    LServo.angle(180)   # fwd
    RServo.angle(0)     # fwd

def MotorsBwd():
    LServo.angle(0)     # bwd
    RServo.angle(180)   # bwd

def MotorsL():
    LServo.angle(180)   # fwd
    RServo.angle(180)   # bwd

def MotorsR():
    LServo.angle(0)     # bwd
    RServo.angle(0)     # fwd

def StopMotors():
    LServo.angle(90)
    RServo.angle(90)

def Roaming():
    pos = 90
    pos_incr = 1

    while True:
        panServo.angle(pos)
        BumpTest()
        MotorsFwd()

        sensor_val = ReadSensor()
        if sensor_val > SENSOR_THRESH:
            if pos > 90:
                MotorsL()
            else:
                MotorsR()
            Delay(DELAY_VAL)
        Delay(10)   # This delay help overcome current spikes from the servos
        if pos == 180:
            pos_incr = -1
        elif pos == 0:
            pos_incr = 1
        pos += pos_incr

Roaming();
