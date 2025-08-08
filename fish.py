''' Motor Driver Code for Big Mouth Billy Bass Hardware '''

from gpiozero import Motor, Button
from time import sleep
import time


class Fish:
    head_motor = None
    tail_motor = None
    mouth_motor = None
    button = None

    def __init__(self):
        # Using software pwm. Not super precise but that's okay for this application
        try:
            self.head_motor = Motor(forward=17, backward=27, pwm=True)
            self.tail_motor = Motor(forward=14, backward=4, pwm=True)
            self.mouth_motor = Motor(forward=2, backward=3, pwm=True)
            # self.button = Button(32)
            print('Motors and buttons initialized')
            self.head_motor.forward(speed=0.5)
            sleep(0.5)
            self.head_motor.stop()
        except Exception as e:
            print(f'Error configuring motors: {e}')

    def cleanup_fish(self):
        # This function will be called when the application exits
        print("Cleaning up GPIO pins...")
        self.head_motor.close()
        self.tail_motor.close()
        self.mouth_motor.close()
        print("GPIO pins released.")

    def listen(self, duration):
        print("listening")
        self.head_motor.forward(speed=0.40)
        sleep(duration*.75)
        self.head_motor.backward(speed=0.25)
        sleep(duration*.25)
        self.head_motor.stop()

    def talk(self, timestamps):
        start_time = time.time()
        end_time = timestamps[-1] + 0.5 if timestamps else 0
        timestamp_iter = iter(timestamps)
        next_character_time = next(timestamp_iter, None)

        talk_threshhold = 0.4
        last_animation_time = -1
        while time.time() - start_time < end_time:
            curr_time = time.time() - start_time
            if next_character_time is not None and curr_time >= next_character_time:
                if curr_time - last_animation_time > talk_threshhold:
                    self.mouth_motor.forward(speed=1)
                    sleep(.3)
                    self.mouth_motor.backward(speed=1)
                    sleep(.1)
                    self.mouth_motor.stop()
                    last_animation_time = curr_time
                next_word_time = next(timestamp_iter, None)
            else:
                self.head_motor.forward(speed=0.2)
                sleep(0.1)
                self.head_motor.stop()

    def move_head_out(self):
        self.head_motor.forward()
        sleep(0.25)
        self.head_motor.stop()

    def move_head_in(self):
        self.head_motor.backward()
        sleep(0.25)
        self.head_motor.stop()

    def move_tail_out(self):
        self.tail_motor.forward()
        sleep(0.25)
        self.tail_motor.stop()

    def move_tail_in(self):
        self.tail_motor.backward()
        sleep(0.25)
        self.tail_motor.stop()

    def move_mouth_out(self):
        self.mouth_motor.forward()
        sleep(0.25)
        self.mouth_motor.stop()

    def move_mouth_in(self):
        self.mouth_motor.backward()
        sleep(0.25)
        self.mouth_motor.stop()


if __name__ == '__main__':
    fish = Fish()
    while True:
        user_in = input(
            'Input a fish command (1 for mouth, 2 for head, 3 for tail, 4 for talk, 5 for listen, 6 to exit)'
        )
        match int(user_in.strip()):
            case 1:
                fish.move_mouth_out()
            case 2:
                fish.move_head_out()
            case 3:
                fish.move_tail_out()
            case 4:
                fish.talk()
            case 5:
                fish.listen(3)
            case 6:
                fish.cleanup_fish()
                break
            case _:
                print('invalid input')
