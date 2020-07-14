#! python

import time
import argparse
import sys
import os
from os.path import isfile, join
from os import path
from os import listdir
from PIL import Image
import cv2
import matplotlib.pyplot as plt


####################
#
# args
#
####################


parser = argparse.ArgumentParser(
    description=f"cut avi files from oct into images",
    epilog='e.g.: python octextract.py data')
parser.add_argument(
    "target", type=str, help="target. Either a file to extract or a folder with files.")
args = parser.parse_args()
args_target = args.target


####################
#
# set paths
#
####################


file_script = os.path.abspath(__file__)
path_target = os.path.abspath(args_target)
path_base = os.path.abspath(os.path.join(path_target, '..'))
path_data = os.path.join(path_base, 'data')
path_org = os.path.join(path_data, 'org')
path_oct = os.path.join(path_data, 'oct')
path_fund = os.path.join(path_data, 'fund')


####################
#
# functions
#
####################


def get_files(path):
  files = []
  # if folder then get all avi from folder, else just use the file
  if os.path.isdir(path):
    files = [f for f in listdir(path) if isfile(join(path, f)) and str(f).endswith('.avi')]
  else:
    files.append(path)
  # exit if list is empty
  if not files:
    print('No files found to extract.')
    sys.exit(0)
  print('Found files:')
  for f in files:
    print(f' -> {f}')
  return(files)


def avi_extract(file_avi):
  count = 0
  success = 1

  # define object capute
  file_avi = os.path.join(path_target, file_avi)
  cv2_vid = cv2.VideoCapture(file_avi)

  # loop through frames
  while success:
    count += 1
    success, cv2_im = cv2_vid.read()

    if success:
      cv2_im = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
      pil_im = Image.fromarray(cv2_im)
      name = f"{str(os.path.basename(file_avi)).split('.')[0]}_{count}"
      img_cutter(pil_im, name)


def img_cutter(im_org, name):
  width, _ = im_org.size

  print(f'Cutting: {name}')

  # anchor points manually extracted using gimp
  top = 18
  bottom = 496
  left_oct = 498
  left_fund = 6
  right_oct = width
  right_fund = 491
  im_oct = im_org.crop((left_oct, top, right_oct, bottom))
  im_fund = im_org.crop((left_fund, top, right_fund, bottom))

  # create folder if not exist
  if not os.path.exists(path_data):
    os.mkdir(path_data)
  if not os.path.exists(path_oct):
    os.mkdir(path_oct)
  if not os.path.exists(path_fund):
    os.mkdir(path_fund)
  if not os.path.exists(path_org):
    os.mkdir(path_org)

  # save images
  file_org = join(path_org, f'{name}.png')
  print(f' -> Saving: {file_org}')
  im_org.save(file_org, 'png')
  file_oct = join(path_oct, f'{name}_oct.png')
  print(f' -> Saving: {file_oct}')
  im_oct.save(file_oct, 'png')
  file_fund = join(path_fund, f'{name}_fund.png')
  print(f' -> Saving: {file_fund}')
  im_fund.save(file_fund, 'png')


####################
#
# main
#
####################


def main():
  # empty line for aestethics
  print('')
  # get a list of files
  files = get_files(path_target)
  try:
    for f in files:
      avi_extract(f)
  except KeyboardInterrupt:
    print('Interrupted by user.')


if __name__ == '__main__':
  main()
