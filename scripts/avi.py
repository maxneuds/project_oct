import cv2
print(cv2.__version__)
vidcap = cv2.VideoCapture('C:/Users/Artur/PycharmProjects/avitopng/drop.avi')
success,image = vidcap.read()
count = 0
success = True
while success:
  cv2.imwrite("C:/Users/Artur/PycharmProjects/avitopng/Frame/frame%d.png" % count, image)     # save frame as JPEG file
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1