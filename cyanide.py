#!/usr/bin/env python

"""
Description:    A simple random comic printer using Cyanide and Happiness's RCG (explosm.net/rcg),
                Raspberry Pi B and a QR701 Mini Thermal Printer
Name:           Seamus de Cleir
Date:           20/10/2018
"""
# RX from Printer to GPIO14 (TX)
# TX from Printer to GPIO15 (RX)

from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, socket, os, requests
from PIL import Image
from Adafruit_Thermal import *
from random import randint

def splitWebNames():
  # Opens cyanide.txt and returns the 3 character codes in a list
  webName = []

  for line in open('cyanide.txt', 'r'):
    webName.append(line.strip().split(','))

  return webName


def ranName(lst):
  # Randomly returns a 3 character code from the list
  num = randint(0, 259)  
  word = lst[0][num]

  return word

def imageMaker(lst):
  # Downloads the png image from explosm.net using the codes
  while True:
    url = 'http://files.explosm.net/rcg/'+ ranName(lst) + ranName(lst) + ranName(lst) + '.png'
    print(url)
    r = requests.get(url, allow_redirects=True)
    open('print.png', 'wb').write(r.content)

    # Check if the image is over 10kb. Not all code combinations are valid
    if os.path.getsize('print.png') > 10000:
      break
  return

# Sets Printer (Baud = 9600)
printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)

listNames = splitWebNames()
imageMaker(listNames)

# Rotates image to landscape for printing
im1 = Image.open('print.png')
im1.rotate(270, expand=True).resize((380, 956), Image.BILINEAR).save('print.png')

# Prints Image
printer.printImage(Image.open('print.png'), True)
printer.feed(20)
time.sleep(15)