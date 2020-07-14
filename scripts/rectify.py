#! python

import inspect
import time
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
    epilog='e.g.: python rectify.py labels.json')
parser.add_argument(
    "labelfile", type=str, help="via label json export file path")
args = parser.parse_args()


####################
#
# set paths
#
####################


file_script = os.path.abspath(__file__)
file_input = args.labelfile
file_output = file_input.split('.json')[0] + '_rect.json'


####################
#
# functions
#
####################


def get_dict(json_file):
  # open json label file
  with open(json_file) as f:
    # load json into dict
    dict_file = json.load(f)
  return dict_file


def rectify(d):
  d_new = {}
  for key in d:
    regions = d[key]['regions']
    regions_new = []
    for d_label in regions:
      satt = d_label['shape_attributes']
      ratt = d_label['region_attributes']
      name = satt['name']
      shape_key = list(ratt.keys())[0]
      shape = ratt[shape_key]
      if name == 'rect':
        # already rect -> rect add
        regions_new.append(d_label)
      elif name == 'polygon':
        # polygon -> rectify
        all_x = satt['all_points_x']
        all_y = satt['all_points_y']
        x_min = min(all_x)
        x_max = max(all_x)
        y_min = min(all_y)
        y_max = max(all_y)

        satt_new = {}
        satt_new['x'] = x_min
        satt_new['y'] = y_min
        satt_new['height'] = y_max - y_min
        satt_new['width'] = x_max - x_min
        satt_new['name'] = 'rect'

        ratt_new = {}
        ratt_new[shape_key] = shape

        label_new = {}
        label_new['shape_attributes'] = satt_new
        label_new['region_attributes'] = ratt_new
        regions_new.append(label_new)
      else:
        # drop
        pass
      d[key]['regions'] = regions_new
      d_new[key] = d[key]
  return(d_new)


def gen_labelfile(d):
  with open(file_output, 'w') as f:
    json.dump(d, f, sort_keys=True, indent=2)
  print(f'Save labels to: {file_output}')


####################
#
# main
#
####################


def main():
  d = get_dict(file_input)
  d_new = rectify(d)
  gen_labelfile(d_new)


if __name__ == '__main__':
  main()
