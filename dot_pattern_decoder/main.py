from pathlib import Path

from dot_pattern_decoder import DotPatternDecoder, Direction
import math
import constants
import cv2

display = print
from printer import Printer


decoder = DotPatternDecoder(Path.cwd().joinpath('../2020-04-08_22-00-09.jpg'))

decoder.get_position_codes(decoder.preprocess_image())

decoder.correction_position_2(decoder.x_codes, decoder.y_codes)
decoder.correction_position_2(decoder.x_codes, decoder.x_codes)


# lines_after_correction = correction_virtual_lines(average_x.copy(), classes_x, difference_x)
# print(lines_after_correction)


# direction_x = np.array([
#     [0, 0, -1, -1, 0, 0, 0, -1],
#     [1, -1, 0, 0, 0, 0, 0, 1],
#     [0, 1, 0, 0, 0, 0, 0, 0],
#     [-1, 1, 0, 0, 0, 1, 1, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 1, 0, -1, 0, 0],
#     [1, 1, -1, 0, 0, -1, 0, -1],
#     [0, 1, 0, 1, 1, 0, 0, 0],
# ])
#
# direction_y = np.array([
#     [1, 1, 0, 0, -1, -1, -1, 0],
#     [0, 0, 1, 1, 1, 1, 1, 0],
#     [-1, 0, 1, 1, -1, 1, -1, 1],
#     [0, 0, -1, -1, 1, 0, 0, 0],
#     [0, -1, -1, 1, -1, 1, 1, -1],
#     [-1, 1, 0, 0, 1, 0, -1, -1],
#     [0, 0, 0, 1, 1, 0, 1, 0],
#     [-1, 0, 1, 0, 0, -1, 1, 1],
# ])

#
# direction_x = np.array([
#     [-1, 0, -1, -1, -2, 0, -2, -2],
#     [1, -1, 0, 0, -2, 0, -2, 2],
#     [0, 1, -1, 0, -2, 0, -2, -2],
#     [-1, 1, 0, 0, -2, 1, 2, 2],
#     [1, 0, 0, 0, -2, 0, -2, -2],
#     [0, 0, 1, 1, -2, -1, -2, 2],
#     [1, 1, -1, 0, -2, -1, -2, -2],
#     [0, 1, 0, 1, 2, 0, -2, -2],
# ])
#
# direction_y = np.array([
#     [1, 1, 0, 0, -1, -1, -1, 0],
#     [-2, -2, 2, 2, 2, 2, 2, -2],
#     [-1, 0, 1, 1, -1, 1, -1, 1],
#     [0, 0, -1, -1, 1, 0, 0, 0],
#     [0, -1, -1, 1, -1, 1, 1, -1],
#     [-1, 1, 0, 0, 1, 0, -1, -1],
#     [-2, -2, -2, 2, 2, -2, 2, 2],
#     [-1, 0, 1, 0, 0, -1, 1, 1],
# ])
#
# direction_x, direction_y = correction_position_2(direction_x.copy(), direction_y.copy())
# direction_y, direction_x = correction_position_2(direction_y.transpose(), direction_x.transpose())
# direction_x, direction_y = direction_x.transpose(), direction_y.transpose()
#
# print(direction_x)
# print(direction_y)

# direction_x, direction_y = DotPatternDecoder.directions2positions(direction_x, direction_y)
# direction_x = direction_x.transpose()

# print(DotPatternDecoder.decode_first_column(direction_x), DotPatternDecoder.decode_first_column(direction_y))
