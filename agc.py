# -*- coding: utf-8 -*-
"""AGC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19MMkFc3x24Qoy9vouZMtext8eMduJ_ZW
"""

cpu_info = !lscpu
for inf_item in cpu_info.get_list():
  print(inf_item)

# Commented out IPython magic to ensure Python compatibility.
!pip install ipython-autotime
# %load_ext autotime

import time

def segmentation(image, state, max_iter, rank):
    image = img_as_float(image)
    height, width = image.shape[:2]
    changes = 1
    n = 0
    state_next = state.copy()

    while changes > 0 and n < max_iter:
        changes = 0
        n += 1
        for j in range(width):
            for i in range(height):
                C_p = image[i, j]
                S_p = state[i, j]
                for jj in range(max(0, j - rank),
                                min(j + rank + 1, width)):
                  for ii in range(max(0, i - rank),
                                  min(i + rank + 1, height)):
                        C_q = image[ii, jj]
                        S_q = state[ii, jj]
                        gc = 1 - np.sqrt(np.sum((C_q - C_p) ** 2)) / sqrt(3)
                        if gc * S_q[1] > S_p[1]:
                            state_next[i, j, 0] = S_q[0]
                            state_next[i, j, 1] = gc * S_q[1]
                            changes += 1
                            break
        state = state_next

    return n, state[:, :, 0]

t0 = time.perf_counter()
from skimage import img_as_float
from math import sqrt
import numpy as np
from matplotlib import pyplot as plt
from skimage import io
t1 = time.perf_counter()

t2 = time.perf_counter()
img = io.imread('AVTO1.gif')
t3 = time.perf_counter()
labels = np.zeros(img.shape[0:2], dtype=np.int)

reg = 1
reg_target = 2
height, width = img.shape[:2]

grass = 1
target = -1

labels[0:reg, :] = grass
labels[height-reg:, :] = grass
labels[reg:, 0:reg] = grass
labels[reg:, width-reg:] = grass

labels[int(height/2 - reg_target):int(height/2 + reg_target),
       int(width/2 - reg_target):int(width/2 + reg_target)] = target

strength = np.zeros_like(labels, dtype=np.float64)

strength[np.nonzero(labels)] = 1.0
t4 = time.perf_counter()
n, growcut_labels = segmentation(img, np.dstack((labels, strength)), rank=2, max_iter=150)
t5 = time.perf_counter()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
ax1.imshow(img, cmap='gray')
ax1.contour(labels, colors='r')
ax1.set_title('Исходное изображение')
ax2.set_title('Наложение полученного результата на изображение');
ax2.imshow(growcut_labels, cmap='gray')
t6 = time.perf_counter()

fig, ax1 = plt.subplots(figsize=(14, 7))
ax1.imshow(growcut_labels, cmap='gray')
ax1.axis('off')

number_of_black_pix = np.sum(growcut_labels == -1)
print('Number of black pixels:', number_of_black_pix)

from PIL import Image
import cv2 as cv
image_path = '/content/mask.gif'

img = Image.open(image_path)
n#ew_image = img.resize((40, 40))
img.show()

import cv2
image = cv2.imread("agc_mask.png", 0)
count = cv2.countNonZero(image)
print(count)
number_of_black_pix = np.sum(image == 255)
print('Number of black pixels:', number_of_black_pix)

img_1 = io.imread('mask.gif')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
ax1.imshow(img_1, cmap='gray')
ax1.set_title('Золотой стандарт')
ax2.set_title('AGC');
ax2.imshow(img)
t6 = time.perf_counter()

number_of_black_pix = np.sum(img == 254)
print('Number of black pixels:', number_of_black_pix)

print('Подключение библиотек:',t1-t0)
print('Функция сегментации:',t2-t1)
print('Чтение изображения:',t3-t2)
print('Автоматическая разметка:',t4-t3)
print('Сегментация %s сек. (%s итераций)'% (t5-t4, n))
print('Вывод результата:',t6-t5)
print('Общее время:',t6-t0)

"""Тест на использование памяти"""

# Commented out IPython magic to ensure Python compatibility.
!pip install line_profiler
# %load_ext line_profiler

!pip install pympler
from pympler import summary, muppy

# Commented out IPython magic to ensure Python compatibility.
!pip install line_profiler
#Load the module
# %load_ext line_profiler

# Commented out IPython magic to ensure Python compatibility.
import cProfile

!pip install line_profiler
# %load_ext line_profiler

sum1 = muppy.get_objects()
list1=[]
from skimage import img_as_float
from math import sqrt
import numpy as np
from matplotlib import pyplot as plt
from skimage import io
def growcut(image, state, max_iter, rank):

    image = img_as_float(image)
    height, width = image.shape[:2]

    changes = 1
    n = 0
    state_next = state.copy()

    while changes > 0 and n < max_iter:
        changes = 0
        n += 1

        for j in range(width):
            for i in range(height):
                C_p = image[i, j]
                S_p = state[i, j]
                for jj in range(max(0, j - rank), min(j + rank + 1, width)):
                  for ii in range(max(0, i - rank), min(i + rank + 1, height)):
                        C_q = image[ii, jj]
                        S_q = state[ii, jj]
                        gc = 1 - np.sqrt(np.sum((C_q - C_p) ** 2)) / sqrt(3)
                        if gc * S_q[1] > S_p[1]:
                            state_next[i, j, 0] = S_q[0]
                            state_next[i, j, 1] = gc * S_q[1]
                            changes += 1
                            break

        state = state_next

    return n, state[:, :, 0]

img = io.imread('AVTO1.gif')

labels = np.zeros(img.shape[0:2], dtype=np.int)

reg = 1
reg_target = 3
height, width = img.shape[:2]

grass = -1
target = 1

labels[0:reg, :] = grass
labels[height-reg:, :] = grass
labels[reg:, 0:reg] = grass
labels[reg:, width-reg:] = grass

labels[int(height/2 - reg_target):int(height/2 + reg_target),
       int(width/2 - reg_target):int(width/2 + reg_target)] = target

strength = np.zeros_like(labels, dtype=np.float64)

strength[np.nonzero(labels)] = 1.0

n, growcut_labels = growcut(img, np.dstack((labels, strength)), rank=2, max_iter=150)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
ax1.imshow(img, cmap='gray')
ax1.contour(labels, colors='r')
ax1.set_title('Исходное изображение')
ax2.set_title('Наложение полученного результата на изображение');
ax2.imshow(img, cmap='gray')
ax2.contour(growcut_labels, colors='r')
sum2 = muppy.get_objects()

summary.print_(summary.get_diff(summary.summarize(sum1), summary.summarize(sum2)))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
ax1.imshow(img, cmap='gray')
ax1.contour(labels, colors='r')
ax1.set_title('Исходное изображение')
ax2.set_title('Наложение полученного результата на изображение');
ax2.imshow(img, cmap='gray')
ax2.contour(growcut_labels, colors='r')