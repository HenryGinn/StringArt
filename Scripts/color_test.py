import numpy as np
from PIL import Image


color_1 = np.array([100, 0, 0])
color_2 = np.array([0, 0, 0])

array = np.ones((2, 2, 3))*255
array[:, 0, :] = color_1
array[0, 1, :] = color_1
array[0, 0, :] = array[0, 0, :] - 255 + np.max(array[0, 0, :])/255 * color_1
array[1, 1, :] = array[0, 0, :]
array[1, 1, :] = array[1, 1, :] - 255 + np.max(array[1, 1, :])/255 * color_1
#array[0, 0, :] = array[0, 0, :] + (255 - max(array[0, 0, :]))/255 * color_1

# current + (max - current) / max * color_1
# current + (max - max_of_current) / max * color_1

image = Image.fromarray(np.uint8(array))
image = image.resize((500, 500), resample=Image.BOX)
path = "/home/henry/Documents/Python/StringArt/Data/Test.png"
image.save(path)

