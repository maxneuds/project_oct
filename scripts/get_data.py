#! python

import time
import argparse
import sys
import os
from os.path import isfile, join
from os import path
from os import listdir
from shutil import copyfile
import json


####################
#
# args
#
####################


parser = argparse.ArgumentParser(
    description=f"fetch via annoteded images from folder",
    epilog='e.g.: python get_data.py via_export_json.json kaggle/DRUSEN')
parser.add_argument(
    "labelfile", type=str, help="via label json export file path")
parser.add_argument(
    "data", type=str, help="data folder with the images from the annotation export")
args = parser.parse_args()


####################
#
# set paths
#
####################


file_script = os.path.abspath(__file__)
path_base = os.path.abspath(os.getcwd())
path_output = os.path.abspath(os.path.join(path_base, 'data_selection'))
# path_data = os.path.join(path_base, 'data')
# path_org = os.path.join(path_data, 'org')
# path_oct = os.path.join(path_data, 'oct')
# path_fund = os.path.join(path_data, 'fund')


####################
#
# functions
#
####################


def proc_labels(labelfile):
  # load json label file
  json_file = os.path.join(labelfile)
  with open(json_file) as f:
    imgs_anns = json.load(f)
  for idx, v in enumerate(imgs_anns.values()):
    # print(v)
    filename = v["filename"]
    src = os.path.join(args.data, filename)
    dst = os.path.join(path_output, filename)
    print(f'Found: {filename}!')
    print(f'Copy: {src} -> {dst}')
    copyfile(src, dst)

####################
#
# main
#
####################


def main():
  if not os.path.exists(path_output):
    os.mkdir(path_output)
  proc_labels(args.labelfile)


if __name__ == '__main__':
  main()
