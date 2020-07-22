"""
Created 11/01/2020

@author Jakob McKinney
"""
import struct
import ctypes
import datetime
from GetImage import get_image


# Constant for the action that should be performed by SystemParametersInfoW
SET_DESKTOP_BACKGROUND = 20


def is_64bit_system():
    """
    Returns True if the system running the program
    is a 64-bit system.

    Checks the size of void * (in C) which should be 
    8-bit on 64-bit system.
    """

    return struct.calcsize('P') * 8 == 64


def set_background(img_path):
    """
    Sets the image at the given path as the
    desktop background.
    """
    is_64bit = is_64bit_system()
    if is_64bit:
        ctypes.windll.user32.SystemParametersInfoW(SET_DESKTOP_BACKGROUND, 0, img_path, 3)
    else:
        ctypes.windll.user32.SystemParametersInfoA(SET_DESKTOP_BACKGROUND, 0, img_path, 3)


def main():
    """
    Downloads the image and saves it then
    sets it as the background image using
    the path to that image.
    """
    img_path = get_image(datetime.datetime.today() - datetime.timedelta(1))
    set_background(img_path)  # Needs to be fit


if __name__ == "__main__":
    main()
