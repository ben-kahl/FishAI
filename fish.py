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
        self.__head_motor = Motor(self.__headf, self.__headb)
        self.__tail_motor = Motor(self.__tailf, self.__tailb)
        self.__mouth_motor = Motor(self.__mouthf, self.__mouthb)

    def move_head_out(self):
        self.head_active = True
        self.__head_motor.forward()
        sleep(0.25)
        self.__head_motor.stop()

    def move_head_in(self):
        self.head_active = False
        self.__head_motor.backward()
        sleep(0.25)
        self.__head_motor.stop()

    def move_tail_out(self):
        self.tail_active = True
        self.__tail_motor.forward()
        sleep(0.25)
        self.__tail_motor.stop()

    def move_tail_in(self):
        self.tail_active = False
        self.__tail_motor.backward()
        sleep(0.25)
        self.__tail_motor.stop()

    def move_mouth_out(self):
        self.mouth_active = True
        self.__mouth_motor.forward()
        sleep(0.25)
        self.__mouth_motor.stop()

    def move_mouth_in(self):
        self.mouth_active = False
        self.__mouth_motor.backward()
        sleep(0.25)
        self.__mouth_motor.stop()
