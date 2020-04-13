import numpy as np
from dot_pattern_decoder import DotPatternDecoder


def display(text):
    print(text)


from printer import Printer


def replace(source, replacements):
    destination = np.zeros_like(source)
    for i in range(len(destination)):
        for what, to in replacements:
            if source[i] == what:
                destination[i] = to
                break
            else:
                destination[i] = source[i]

    return destination


def replace_code_in_line(line, code, to):
    replace(line, [(code, to), (-1 * code, np.sign(-1 * code) * to)])


def get_replacements(what, to, other):
    return [(what, to), (-1 * what, other)]


def correction_position_2(x_lines, y_lines):
    indexes = range(len(x_lines))
    for j in indexes:
        for i in indexes:
            x_code, y_code = x_lines[i, j], y_lines[i, j]
            if abs(y_code) == 2:
                if abs(x_code) == 1:
                    new_line = replace(
                        y_lines[i], get_replacements(what=y_code, to=0, other=-1 * np.sign(y_code))
                    )
                    y_lines[i] = new_line
                elif abs(x_code) == 0:
                    new_line = replace(
                        y_lines[i], get_replacements(what=y_code, to=np.sign(y_code), other=0)
                    )
                    y_lines[i] = new_line

    return x_lines, y_lines
    # for j in range(len(x_lines)):
    #     x_line, y_line = x_lines[j], y_lines[j]
    #     for i, (x_code, y_code) in enumerate(zip(x_line, y_line)):
    #         if abs(y_code) == 2:
    #             if abs(x_code) == 1:
    #                 y_lines[:, i] = replace(
    #                     y_lines[:, i], [(y_code, 0), (-1 * y_code, -1 * np.sign(y_code))]
    #                 )
    #             elif abs(x_code) == 0:
    #                 y_lines[:, i] = replace(
    #                     y_lines[:, i], [(y_code, np.sign(y_code)), (-1 * y_code, 0)]
    #                 )


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

direction_x = np.array([
    [-1, 0, -1, -1, -2, 0, -2, -2],
    [1, -1, 0, 0, -2, 0, -2, 2],
    [0, 1, -1, 0, -2, 0, -2, -2],
    [-1, 1, 0, 0, -2, 1, 2, 2],
    [1, 0, 0, 0, -2, 0, -2, -2],
    [0, 0, 1, 1, -2, -1, -2, 2],
    [1, 1, -1, 0, -2, -1, -2, -2],
    [0, 1, 0, 1, 2, 0, -2, -2],
])

direction_y = np.array([
    [1, 1, 0, 0, -1, -1, -1, 0],
    [-2, -2, 2, 2, 2, 2, 2, -2],
    [-1, 0, 1, 1, -1, 1, -1, 1],
    [0, 0, -1, -1, 1, 0, 0, 0],
    [0, -1, -1, 1, -1, 1, 1, -1],
    [-1, 1, 0, 0, 1, 0, -1, -1],
    [-2, -2, -2, 2, 2, -2, 2, 2],
    [-1, 0, 1, 0, 0, -1, 1, 1],
])

direction_x, direction_y = correction_position_2(direction_x.copy(), direction_y.copy())
direction_y, direction_x = correction_position_2(direction_y.transpose(), direction_x.transpose())
direction_x, direction_y = direction_x.transpose(), direction_y.transpose()

print(direction_x)
print(direction_y)

# direction_x, direction_y = DotPatternDecoder.directions2positions(direction_x, direction_y)
# direction_x = direction_x.transpose()

# print(DotPatternDecoder.decode_first_column(direction_x), DotPatternDecoder.decode_first_column(direction_y))
