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

#
# first version with fixed folder structure
#
# parser = argparse.ArgumentParser(
#     description=f"fetch via annoteded images from folder",
#     epilog='e.g.: python get_data.py via_export_json.json kaggle/DRUSEN')
# parser.add_argument(
#     "labelfile", type=str, help="via label json export file path")
# parser.add_argument(
#     "data", type=str, help="data folder with the images from the annotation export")
# args = parser.parse_args()


####################
#
# set paths
#
####################


file_script = os.path.abspath(__file__)
dir_base = os.path.abspath(os.getcwd())
dir_labels = os.path.abspath(os.path.join(dir_base, 'labels'))
if not os.path.exists(dir_labels):
  print(f'Directory: {dir_labels} -> Not found!')
  sys.exit()
dir_oct = os.path.abspath(os.path.join(dir_base, '../Bilder/OCT'))
if not os.path.exists(dir_oct):
  print(f'Directory: {dir_oct} -> Not found!')
  sys.exit()
now = dt.now()
dir_output = os.path.abspath(os.path.join(dir_base, f'data_{now.strftime("%y%m%d_%H%M")}'))
if os.path.exists(dir_output):
  print(f'Directory: {dir_output} -> Already exists!')
  sys.exit()
dir_output_train = os.path.join(dir_output, 'train')
dir_output_val = os.path.join(dir_output, 'val')


####################
#
# functions
#
####################


def get_label_files(dir):
  content = os.listdir(dir)
  # grab all json files
  files = [f for f in content if os.path.isfile(os.path.join(dir, f)) and f.endswith('.json')]
  # map the absolute path on all files
  files = [os.path.join(dir, f) for f in files]
  return files


def get_im_path(im_name):
  # extra files directly in OCT folder
  if im_name.startswith('x_'):
    dir_oct_scan = dir_oct
  else:
    foldername = '_'.join(im_name.split('_')[:3])
    dir_oct_scan = os.path.join(dir_oct, foldername)
  file_im = os.path.join(dir_oct_scan, im_name)
  file_im = os.path.abspath(file_im)
  return(file_im)


def gen_clean_dict(json_file):
  dict_labels = {}
  dict_files = {}
  # open json label file
  with open(json_file) as f:
    # load json into dict
    dict_file = json.load(f)
    for key in dict_file:
      dict_im = dict_file[key]
      # check for empty or bad data
      try:
        if len(dict_im['regions']) > 0:
          filename = dict_im['filename']
          file_im = get_im_path(filename)
          # maybe for a filefix one day
          # size_im = os.path.getsize(file_im)
          #
          # add dict to output dict
          if os.path.exists(file_im):
            dict_labels[key] = dict_im
            dict_files[key] = file_im
          else:
            print(f'{file_im} -> Not found -> dropping!')
      except KeyError as e:
        pass
  return dict_labels, dict_files


def train_test_split(labels, files):
  # settings
  n_val = 10
  #

  labels_train = {}
  labels_val = {}
  files_train = {}
  files_val = {}

  # pick random images for val
  count_im = len(labels)
  print(labels)
  print(n_val)
  keys_val = random.sample(list(labels.keys()), n_val)
  for key in labels:
    if key in keys_val:
      labels_val[key] = labels[key]
      files_val[key] = files[key]
    else:
      labels_train[key] = labels[key]
      files_train[key] = files[key]
  return labels_train, labels_val, files_train, files_val


def copy_images(files, split):
  if split == 'val':
    dir_dst = dir_output_val
  else:
    dir_dst = dir_output_train
  for f in files:
    if 'png' in f:
      filename = f.split('.png')[0] + '.png'
    elif 'jpg' in f:
      filename = f.split('.jpg')[0] + '.jpg'
    elif 'jpeg' in f:
      filename = f.split('.jpeg')[0] + '.jpeg'
    src = files[f]
    dst = os.path.join(dir_dst, filename)
    if not os.path.exists(dir_output):
      os.mkdir(dir_output)
    if not os.path.exists(dir_output_train):
      os.mkdir(dir_output_train)
    if not os.path.exists(dir_output_val):
      os.mkdir(dir_output_val)
    print(f'Copy: {src} -> {dst}')
    copyfile(src, dst)


def gen_labelfile(dict_l, split):
  # remove null values... wherever these come from
  dict_labels = {k: v for k, v in dict_l.items() if k is not None and v is not None}
  if split == 'val':
    dir_dst = dir_output_val
  else:
    dir_dst = dir_output_train
  dst = os.path.join(dir_dst, 'via_labels.json')
  with open(dst, 'w') as f:
    json.dump(dict_labels, f, sort_keys=True, indent=2)
  print(f'Save labels to: {dst}')


####################
#
# main
#
####################


def main():
  # get via export (hopefully) json label files
  files_labels = get_label_files(dir_labels)

  labels = {}
  files = {}
  for f in files_labels:
    labels_new, files_new = gen_clean_dict(f)
    labels.update(labels_new)
    files.update(files_new)
  labels_train, labels_val, files_train, files_val = train_test_split(labels, files)
  copy_images(files_train, 'train')
  copy_images(files_val, 'val')
  gen_labelfile(labels_train, 'train')
  gen_labelfile(labels_val, 'val')


if __name__ == '__main__':
  main()
