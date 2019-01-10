"""
This module demonstrates lets you practice implementing classes and the
wait-until-event pattern, in the context of robot motion that uses sensors.

Authors: David Mutchler, Vibha Alangar, Matt Boutell, Dave Fisher,
         Mark Hays, Amanda Stouder, Aaron Wilkin, their colleagues,
         and Ethan Mahn.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

import ev3dev.ev3 as ev3
import time
import math


def main():
    """ Calls the other functions to test/demo them. """
    # run_test_wait_for_seconds()
    # run_test_init()
    # run_test_go_and_stop()
    # run_test_go_straight_for_seconds()
    # run_test_go_straight_for_inches()
    run_test_go_straight_until_black()


def run_test_wait_for_seconds():
    """ Tests the   wait_for_seconds   function by calling it. """
    print()
    print('--------------------------------------------------')
    print('Testing the   wait_for_seconds   function:')
    print('--------------------------------------------------')

    wait_for_seconds()

    print('Here is a second test:')
    wait_for_seconds()


def wait_for_seconds():
    """ Prints Hello, waits for 3 seconds, then prints Goodbye. """
    # -------------------------------------------------------------------------
    # DONE: 2. With your instructor, implement and test this function.
    #   IMPORTANT:  Do NOT use the    time.sleep   function
    #               anywhere in this project.
    #               (Exception: Use it in test-functions to separate tests.)
    #
    #               Instead, use the   time.time   function
    #               that returns the number of seconds since "the Epoch"
    #               (January 1, 1970, 00:00:00 (UTC) on some platforms).
    #
    #   The testing code is already written for you (above, in main).
    #   NOTE: this function has nothing to do with robots,
    #   but its concepts will be useful in the forthcoming robot exercises.
    # -------------------------------------------------------------------------
    print('Hello')
    t0=time.time()
    while True:
        if time.time()-t0 >=3:
            break
    print('Goodbye')


def run_test_init():
    """ Tests the   __init__   method of the SimpleRoseBot class. """
    print()
    print('--------------------------------------------------')
    print('Testing the   __init__   method of the SimpleRoseBot class:')
    print('--------------------------------------------------')
    # -------------------------------------------------------------------------
    # DONE: 3. Implement this function, then implement the   __init__   method
    #   of the SimpleRoseBot class, then use this function to test __init__.
    # -------------------------------------------------------------------------
    SimpleRoseBot()

def run_test_go_and_stop():
    """ Tests the   go   and   stop   methods of the SimpleRoseBot class. """
    print()
    print('--------------------------------------------------')
    print('Testing the  go  and  stop  methods of the SimpleRoseBot class:')
    print('--------------------------------------------------')
    # -------------------------------------------------------------------------
    # DONE: 4. Implement this function, then implement the   go  and   stop
    #   methods of the SimpleRoseBot class, then use this function
    #   to test both   go   and   stop   at the same time.
    # -------------------------------------------------------------------------
    robot=SimpleRoseBot()
    robot.go(100,65)
    wait_for_seconds()
    robot.stop()

def run_test_go_straight_for_seconds():
    """ Tests the   go_straight_for_seconds   method of SimpleRoseBot. """
    print()
    print('--------------------------------------------------')
    print('Testing the   go_straight_for_seconds   method of SimpleRoseBot:')
    print('--------------------------------------------------')
    # -------------------------------------------------------------------------
    # DONE: 5. Implement this function, then implement the
    #   go_straight_for_seconds   method of the SimpleRoseBot class,
    #   then use this function to test that method.
    # -------------------------------------------------------------------------
    robot = SimpleRoseBot()
    robot.go_straight_for_seconds(7, 42)

def run_test_go_straight_for_inches():
    """ Tests the   go_straight_for_inches   method of SimpleRoseBot. """
    print()
    print('--------------------------------------------------')
    print('Testing the   go_straight_for_inches   method of SimpleRoseBot:')
    print('--------------------------------------------------')
    # -------------------------------------------------------------------------
    # DONE: 6. Implement this function, then implement the
    #   go_straight_for_inches   method of the SimpleRoseBot class,
    #   then use this function to test that method.
    # -------------------------------------------------------------------------
    robot = SimpleRoseBot()
    robot.go_straight_for_inches(8,83)

def run_test_go_straight_until_black():
    """ Tests the   go_straight_until_black   method of SimpleRoseBot. """
    print()
    print('--------------------------------------------------')
    print('Testing the   go_straight_until_black   method of SimpleRoseBot:')
    print('--------------------------------------------------')
    # -------------------------------------------------------------------------
    # TODO: 7. Implement this function, then implement the
    #   go_straight_until_black   method of the SimpleRoseBot class,
    #   then use this function to test that method.
    # -------------------------------------------------------------------------
    robot = SimpleRoseBot()
    run_test_go_straight_until_black(53)

###############################################################################
# Put your   SimpleRoseBot    class here (below this comment).
# Your instructor may help you get started.
###############################################################################

class SimpleRoseBot(object):

    def __init__(self):
        self.left_motor = Motor('B')
        self.right_motor = Motor('C')
        self.color_sensor = ColorSensor(3)

    def go(self,lw_speed,rw_speed):
        self.left_motor.turn_on(lw_speed)
        self.right_motor.turn_on(rw_speed)

    def stop(self):
        self.left_motor.turn_off()
        self.right_motor.turn_off()

    def go_straight_for_seconds(self,seconds,speed):
        self.go(speed,speed)
        t0=time.time()
        while True:
            if time.time()-t0 >= seconds:
                break
        self.stop()

    def go_straight_for_inches(self,inches,speed):
        self.go(speed,speed)
        x0=self.left_motor.get_position()
        while True:
            if (self.left_motor.get_position()-x0)*(3.14/360)*1.3 >= inches:
                break
        self.stop()

    def go_straight_until_black(self, speed):
        self.go(speed,speed)
        while True:
            if self.color_sensor.get_reflected_light_intensity() <20:
                break
        self.stop

###############################################################################
# The  Motor   and   ColorSensor classes.  USE them, but do NOT modify them.
###############################################################################
class Motor(object):
    WheelCircumference = 1.3 * math.pi

    def __init__(self, port):  # port must be 'B' or 'C' for left/right wheels
        self._motor = ev3.LargeMotor('out' + port)

    def turn_on(self, speed):  # speed must be -100 to 100
        self._motor.run_direct(duty_cycle_sp=speed)

    def turn_off(self):
        self._motor.stop(stop_action="brake")

    def get_position(self):  # Units are degrees (that the motor has rotated).
        return self._motor.position

    def reset_position(self):
        self._motor.position = 0


class ColorSensor(object):
    def __init__(self, port):  # port must be 3
        self._color_sensor = ev3.ColorSensor('in' + str(port))

    def get_reflected_light_intensity(self):
        # Returned value is from 0 to 100,
        # but in practice more like 3 to 90+ in our classroom lighting.
        return self._color_sensor.reflected_light_intensity


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
