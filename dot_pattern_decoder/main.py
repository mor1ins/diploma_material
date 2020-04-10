import numpy as np
from dot_pattern_decoder import DotPatternDecoder

direction_x = np.array([
    [0, 0, -1, -1, 0, 0, 0, -1],
    [1, -1, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [-1, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, -1, 0, 0],
    [1, 1, -1, 0, 0, -1, 0, -1],
    [0, 1, 0, 1, 1, 0, 0, 0],
])

direction_y = np.array([
    [1, 1, 0, 0, -1, -1, -1, 0],
    [0, 0, 1, 1, 1, 1, 1, 0],
    [-1, 0, 1, 1, -1, 1, -1, 1],
    [0, 0, -1, -1, 1, 0, 0, 0],
    [0, -1, -1, 1, -1, 1, 1, -1],
    [-1, 1, 0, 0, 1, 0, -1, -1],
    [0, 0, 0, 1, 1, 0, 1, 0],
    [-1, 0, 1, 0, 0, -1, 1, 1],
])

direction_x, direction_y = DotPatternDecoder.directions2positions(direction_x, direction_y)
direction_x = direction_x.transpose()

print(DotPatternDecoder.decode_first_column(direction_x), DotPatternDecoder.decode_first_column(direction_y))
