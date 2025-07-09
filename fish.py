''' Motor Driver Code for Big Mouth Billy Bass Hardware '''

from gpiozero import Motor
from time import sleep


class Fish:
    head_active = False
    tail_active = False
    mouth_active = False

    def __init__(self):
        ''' Change GPIO Pin values once I connect wires '''
        self.__headf = 17
        self.__headb = 18
        self.__tailf = 4
        self.__tailb = 14
        self.__mouthf = 2
        self.__mouthb = 3
        # Make these accessible for cleanup by removing the double underscore
        self.head_motor = Motor(self.__headf, self.__headb, pwm=False)
        self.tail_motor = Motor(self.__tailf, self.__tailb, pwm=False)
        self.mouth_motor = Motor(self.__mouthf, self.__mouthb, pwm=False)

    def move_head_out(self):
        self.head_active = True
        self.head_motor.forward()
        sleep(0.25)

    def move_head_in(self):
        self.head_active = False
        self.head_motor.backward()
        sleep(0.25)

    def move_tail_out(self):
        self.tail_active = True
        self.tail_motor.forward()
        sleep(0.25)

    def move_tail_in(self):
        self.tail_active = False
        self.tail_motor.backward()
        sleep(0.25)

    def move_mouth_out(self):
        self.mouth_active = True
        self.mouth_motor.forward()
        sleep(0.25)

    def move_mouth_in(self):
        self.mouth_active = False
        self.mouth_motor.backward()
        sleep(0.25)
