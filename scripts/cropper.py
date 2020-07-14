from PIL import Image
import os
from os import listdir
from os import path
from os.path import isfile, join

dir_out = 'out'
dir_res = 'res'

# create output folder if not exist
if not path.exists('out'):
  os.mkdir(dir_out)

# input folder: res
im_res = [f for f in listdir(dir_res) if isfile(join(dir_res, f)) and str(f).endswith('.jpg')]

try:
  for im in im_res:
    # Create an Image object from an Image
    original = Image.open(join(dir_res, im))

    width, height = original.size
    if width > 1200:
      width = int(width * 0.8278)
      original = original.resize((width, 596), Image.LANCZOS)
    left = 0.5*width
    top = 0
    right = left + 500
    bottom = top + 500
    cropped = original.crop((left, top, right, bottom))
    # cropped.show()
    cropped.save(join(dir_out, im), 'jpeg')
except KeyboardInterrupt:
  print('Interrupted by user.')
