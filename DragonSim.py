#!/usr/bin/env python
#
# 3       - Left Motor Servo
# 4       - Right Motor Servo
# 5       - Pan Servo
# 14 (A0) - Analog Sensor
# 15 (A1) - Left Whisker
# 16 (A1) - Right Whisker

SIMULATE = 1

SENSOR_PIN = 14
L_BUMP = 15
R_BUMP = 16 

SENSOR_THRESH = 400

DELAY_VAL = 700 # Delay for turning

if SIMULATE:
    import time
    import sys
    import select
    import termios

    def Delay(msec):
        time.sleep(msec/1000)
    class Servo:
        def _init__(self):
            self._pos = 90
        def angle(self, pos):
            self._pos = pos;
        def getAngle(self):
            return self._pos
    simBumpL = 0
    simBumpR = 0
    simSensor = 0
    motorStr = ''
    prevSimBumpL = 0
    prevSimBumpR = 0
    prevSensor = 0
    prevMotorStr = ''
    throbberStr = " .oO"
    throbberIdx = 0
    def ReadBump(pin):
        global simBumpL
        global simBumpR
        global simSensor
        global motorStr
        global prevSimBumpL
        global prevSimBumpR
        global prevSensor
        global prevMotorStr
        global throbberIdx
        events = epoll.poll(timeout=0)
        for fileno, _ in events:
            if fileno == sys.stdin.fileno():
                data = sys.stdin.read(1)
                ch = data[0]
                if ch == 'l':
                    simBumpL = 1 - simBumpL
                if ch == 'r':
                    simBumpR = 1 - simBumpR
                if ch >= '0' and ch <= '9':
                    simSensor = (ord(ch) - ord('0')) * 100
        #if (prevSimBumpL != simBumpL or
        #    prevSimBumpR != simBumpR or
        #    prevSensor != simSensor or
        #    prevMotorStr != motorStr):
        #    sys.stdout.write('\n')
        #    prevSimBumpL = simBumpL
        #    prevSimBumpR = simBumpR
        #    prevSensor = simSensor
        #    prevMotorStr = motorStr
        panAngle = panServo.getAngle()
        sys.stdout.write("\rMotors: %s Pan: %3d Bump L: %d R: %d Sensor: %3d %c\n" %(motorStr, panAngle, simBumpL, simBumpR, simSensor, throbberStr[throbberIdx]))
        sys.stdout.flush()
        throbberIdx = (throbberIdx + 1) % 4

        if pin == L_BUMP:
            return simBumpL
        else:
            return simBumpR
    def ReadSensor():
        return simSensor
    panServo = Servo()

    stdin_fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(stdin_fd)
    new_settings = termios.tcgetattr(stdin_fd)
    new_settings[3] &= ~(termios.ICANON | termios.ECHO)
    new_settings[6][termios.VTIME] = 0
    new_settings[6][termios.VMIN] = 1
    termios.tcsetattr(stdin_fd, termios.TCSANOW, new_settings)
    epoll = select.epoll()
    epoll.register(sys.stdin.fileno(), select.POLLIN)
else:
    LServo = pyb.Servo()
    LServo.attach(3)

    RServo = pyb.Servo()
    RServo.attach(4);

    panServo = pyb.Servo()
    panServo.attach(5)
    def Delay(msec):
        pyb.delay(msec)
    def ReadBump(pin):
        return pyb.gpio(pin)
    def ReadSensor():
        return pyb.analogRead(SENSOR_PIN)

panServo.angle(90)
Delay(250)      # Give the pan servo time to get to where its going

def BumpTest():
    bump_L = ReadBump(L_BUMP)
    bump_R = ReadBump(R_BUMP)
    while bump_L or bump_R:
        if bump_L:
            MotorsR()
        else:
            MotorsL()
        Delay(100)
        bump_L = ReadBump(L_BUMP)
        bump_R = ReadBump(R_BUMP)

def MotorsFwd():
    global motorStr
    if SIMULATE:
        motorStr = "Forward ";
    else:
        LServo.angle(180)
        RServo.angle(0)

def MotorsBwd():
    global motorStr
    if SIMULATE:
        motorStr = "Backward";
    else:
        LServo.angle(0)
        RServo.angle(180)

def MotorsL():
    global motorStr
    if SIMULATE:
        motorStr = "Left    ";
    else:
        LServo.angle(180)
        RServo.angle(180)

def MotorsR():
    global motorStr
    if SIMULATE:
        motorStr = "Right   ";
    else:
        LServo.angle(0)
        RServo.angle(0)

def StopMotors():
    global motorStr
    if SIMULATE:
        motorStr = "Stop    ";
    else:
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
        Delay(1000)
        if pos == 135:
            pos_incr = -1
        elif pos == 0:
            pos_incr = 1
        pos += pos_incr

Roaming();
