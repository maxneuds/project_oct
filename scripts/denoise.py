#! python

import numpy as np
import cv2
import copy
from matplotlib import pyplot as plt
import argparse
import sys
import os
from datetime import datetime as dt
from os.path import isfile, join
from os import path
from os import listdir
from shutil import copyfile
import json
import random


####################
#
# args
#
####################


parser = argparse.ArgumentParser(
    description=f"turn via polygons to rects",
    epilog='e.g.: python rectify.py /home/user/data/train')
parser.add_argument(
    "path", type=str, help="path to image folder")
args = parser.parse_args()


####################
#
# set paths
#
####################


file_script = os.path.abspath(__file__)
dir_input = os.path.abspath(args.path)
dir_output = dir_input + '_denoise'


####################
#
# functions
#
####################


def clean_im(im):
  grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
  denoise = cv2.fastNlMeansDenoising(grey, None, 11, 5, 19)
  ret, thresh = cv2.threshold(denoise, 25, 255, cv2.THRESH_TOZERO)
  clean = copy.copy(thresh)
  clean_counter = 0
  for i, row in enumerate(clean):
    l = len(row)
    unique, counts = np.unique(row, return_counts=True)
    d = dict(zip(unique, counts))
    if 0 in d.keys():
      n_zeros = d[0]
      if n_zeros > 50:
        clean[i, :] = 0
        clean_counter += 1
  if clean_counter > clean.shape[0]/100*85:
    clean = thresh
  return(clean)


def process_ims(ims):
  for f in ims:
    f_out = os.path.join(dir_output, f)
    f_in = os.path.join(dir_input, f)
    im = cv2.imread(f_in)
    clean = clean_im(im)
    cv2.imwrite(f_out, clean)


####################
#
# main
#
####################


def main():
  if not os.path.exists(dir_output):
    os.mkdir(dir_output)
  files = [f for f in os.listdir(dir_input) if f.endswith('.png') or f.endswith('.jpg')]
  process_ims(files)


if __name__ == '__main__':
  main()
