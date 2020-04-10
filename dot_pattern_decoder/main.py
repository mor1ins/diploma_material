import time

import numpy as np


def sequence_p(start, step):
    while True:
        yield start
        start += step


def transpose(matrix):
    return [list(matrix[:, row]) for row in range(len(matrix))]


def find(sequence, subsequence):
    # print(subsequence)
    sequence_copy = sequence.copy()
    sequence_str = ''.join(map(lambda el: str(el), sequence_copy))
    # print(sequence_str)
    subsequence_str = ''.join(map(lambda el: str(el), subsequence))
    result = sequence_str.find(subsequence_str)
    if result == -1:
        middle = int(len(sequence_str) / 2)
        sequence_copy[:middle], sequence_copy[middle + 1:] = sequence_copy[middle:], sequence_copy[:middle]
        sequence_str = ''.join(map(lambda el: str(el), sequence_copy))
        result = sequence_str.find(subsequence_str)
        # print(sequence_str)

    return result


class DotPatternDecoder:
    MNS = [
        0, 0, 0, 0, 0, 0, 1, 0, 0, 1,
        1, 1, 1, 1, 0, 1, 0, 0, 1, 0,
        0, 0, 0, 1, 1, 1, 0, 1, 1, 1,
        0, 0, 1, 0, 1, 0, 1, 0, 0, 0,
        1, 0, 1, 1, 0, 1, 1, 0, 0, 1,
        1, 0, 1, 0, 1, 1, 1, 1, 0, 0,
        0, 1, 1
    ]

    A_1 = [
        0, 0, 0, 0, 0, 1, 0, 0, 0, 0,   2, 0, 1, 0, 0, 1, 0, 1, 0, 0,
        2, 0, 0, 0, 1, 1, 0, 0, 0, 1,   2, 0, 0, 1, 0, 2, 0, 0, 2, 0,
        2, 0, 1, 1, 0, 1, 0, 1, 1, 0,   2, 0, 1, 2, 0, 1, 0, 1, 2, 0,
        2, 1, 0, 0, 1, 1, 1, 0, 1, 1,   1, 1, 0, 2, 1, 0, 1, 0, 2, 1,
        1, 0, 0, 1, 2, 1, 0, 1, 1, 2,   0, 0, 0, 2, 1, 0, 2, 0, 2, 1,
        1, 1, 0, 0, 2, 1, 2, 0, 1, 1,   1, 2, 0, 2, 0, 0, 1, 1, 2, 1,
        0, 0, 0, 2, 2, 0, 1, 0, 2, 2,   0, 0, 1, 2, 2, 0, 2, 0, 2, 2,
        1, 0, 1, 2, 1, 2, 1, 0, 2, 1,   2, 1, 1, 0, 2, 2, 1, 2, 1, 2,
        0, 2, 2, 0, 2, 2, 2, 0, 1, 1,   2, 2, 1, 1, 0, 1, 2, 2, 2, 2,
        1, 2, 0, 0, 2, 2, 1, 1, 2, 1,   2, 2, 1, 0, 2, 2, 2, 2, 2, 0,
        2, 1, 2, 2, 2, 1, 1, 1, 2, 1,   1, 2, 0, 1, 2, 2, 1, 2, 2, 0,
        1, 2, 1, 1, 1, 1, 2, 2, 2, 0,   0, 2, 1, 1, 2, 2
    ]

    A_2 = [
        0, 0, 0, 0, 0, 1, 0, 0, 0, 0,   2, 0, 1, 0, 0, 1, 0, 1, 0, 1,
        1, 0, 0, 0, 1, 1, 1, 1, 0, 0,   1, 1, 0, 1, 0, 0, 2, 0, 0, 0,
        1, 2, 0, 1, 0, 1, 2, 1, 0, 0,   0, 2, 1, 1, 1, 0, 1, 1, 1, 0,
        2, 1, 0, 0, 1, 2, 1, 2, 1, 0,   1, 0, 2, 0, 1, 1, 0, 2, 0, 0,
        1, 0, 2, 1, 2, 0, 0, 0, 2, 2,   0, 0, 1, 1, 2, 0, 2, 0, 0, 2,
        0, 2, 0, 1, 2, 0, 0, 2, 2, 1,   1, 0, 0, 2, 1, 0, 1, 1, 2, 1,
        0, 2, 0, 2, 2, 1, 0, 0, 2, 2,   2, 1, 0, 1, 2, 2, 0, 0, 2, 1,
        2, 2, 1, 1, 1, 1, 1, 2, 0, 0,   1, 2, 2, 1, 2, 0, 1, 1, 1, 2,
        1, 1, 2, 0, 1, 2, 1, 1, 1, 2,   2, 0, 2, 2, 0, 1, 1, 2, 2, 2,
        2, 1, 2, 1, 2, 2, 0, 1, 2, 2,   2, 0, 2, 0, 2, 1, 1, 2, 2, 1,
        0, 2, 2, 0, 2, 1, 0, 2, 1, 1,   0, 2, 2, 2, 2, 0, 1, 0, 2, 2,
        1, 2, 2, 2, 1, 1, 2, 1, 2, 0,   2, 2, 2,
    ]

    A_3 = [
        0, 0, 0, 0, 0, 1, 0, 0, 1, 1,   0, 0, 0, 1, 1, 1, 1, 0, 0, 1,
        0, 1, 0, 1, 1, 0, 1, 1, 1, 0,   1
    ]

    A_4 = [
        0, 0, 0, 0, 0, 1, 0, 2, 0, 0,   0, 0, 2, 0, 0, 2, 0, 1, 0, 0,
        0, 1, 1, 2, 0, 0, 0, 1, 2, 0,   0, 2, 1, 0, 0, 0, 2, 1, 1, 2,
        0, 1, 0, 1, 0, 0, 1, 2, 1, 0,   0, 1, 0, 0, 2, 2, 0, 0, 0, 2,
        2, 1, 0, 2, 0, 1, 1, 0, 0, 1,   1, 1, 0, 1, 0, 1, 1, 0, 1, 2,
        0, 1, 1, 1, 1, 0, 0, 2, 0, 2,   0, 1, 2, 0, 2, 2, 0, 1, 0, 2,
        1, 0, 1, 2, 1, 1, 0, 1, 1, 1,   2, 2, 0, 0, 1, 0, 1, 2, 2, 2,
        0, 0, 2, 2, 2, 0, 1, 2, 1, 2,   0, 2, 0, 0, 1, 2, 2, 0, 1, 1,
        2, 1, 0, 2, 1, 1, 0, 2, 0, 2,   1, 2, 0, 0, 1, 1, 0, 2, 1, 2,
        1, 0, 1, 0, 2, 2, 0, 2, 1, 0,   2, 2, 1, 1, 1, 2, 0, 2, 1, 1,
        1, 0, 2, 2, 2, 2, 0, 2, 0, 2,   2, 1, 2, 1, 1, 1, 1, 2, 1, 2,
        1, 2, 2, 2, 1, 0, 0, 2, 1, 2,   2, 1, 0, 1, 1, 2, 2, 1, 1, 2,
        1, 2, 2, 2, 2, 1, 2, 0, 1, 2,   2, 1, 2, 2, 0, 2, 2, 2, 1, 1
    ]

    def __init__(self):
        pass

    def decode_image(self, image):
        pass

    @staticmethod
    def dir2pos(x, y):
        translations = [
            ((-1, 0), (1, 0)),
            ((1, 0), (0, 1)),
            ((0, 1), (0, 0)),
            ((0, -1), (1, 1)),
        ]
        for dir, pos in translations:
            if dir[0] == x and dir[1] == y:
                return pos

    @staticmethod
    def directions2positions(x_direction, y_direction):
        x_position = np.zeros_like(x_direction)
        y_position = np.zeros_like(y_direction)
        for i in range(len(x_direction)):
            for j in range(len(x_direction[i])):
                x_position[i, j], y_position[i, j] = DotPatternDecoder.dir2pos(x_direction[i, j], y_direction[i, j])
                # print(f'({x_direction[i, j]}, {y_direction[i, j]}) -> ({x_position[i, j]}, {y_position[i, j]})')

        return x_position, y_position

    @staticmethod
    def find_position_in_mns(sequence):
        subsequence_length = 6
        return find(DotPatternDecoder.MNS, sequence[:subsequence_length])

    @staticmethod
    def find_all_positions_in_mns(sequences):
        return [DotPatternDecoder.find_position_in_mns(sequence) for sequence in sequences]

    @staticmethod
    def calculate_pds(col1, col2):
        # why???
        return (col2 - col1) % len(DotPatternDecoder.MNS)

    @staticmethod
    def calculate_pds_sequence(sequence):
        return [DotPatternDecoder.calculate_pds(c1, c2) for c1, c2 in zip(sequence[:-1], sequence[1:])]

    @staticmethod
    def take_n(sequences, n):
        return [''.join([str(el) for el in row[:n]]) for row in sequences]

    @staticmethod
    def calculate_sds_sequence(sequence):
        return [DotPatternDecoder.calculate_sds(pds) for pds in sequence]

    @staticmethod
    def calculate_sds(pds):
        pds -= 5
        pds, a1 = divmod(pds, 3)
        pds, a2 = divmod(pds, 3)
        pds, a3 = divmod(pds, 2)
        a4 = pds
        return a1, a2, a3, a4

    @staticmethod
    def find_positions_in_sds(sds):
        return (
            find(DotPatternDecoder.A_1, sds[0]),
            find(DotPatternDecoder.A_2, sds[1]),
            find(DotPatternDecoder.A_3, sds[2]),
            find(DotPatternDecoder.A_4, sds[3]),
        )

    @staticmethod
    def find_coordinate_by_sds_seq(sds):
        a1, a2, a3, a4 = sds

        sequence_a1 = sequence_p(a1, len(DotPatternDecoder.A_1))
        sequence_a2 = sequence_p(a2, len(DotPatternDecoder.A_2))
        sequence_a3 = sequence_p(a3, len(DotPatternDecoder.A_3))
        sequence_a4 = sequence_p(a4, 241)

        a1 = [next(sequence_a1), sequence_a1]
        a2 = [next(sequence_a2), sequence_a2]
        a3 = [next(sequence_a3), sequence_a3]
        a4 = [next(sequence_a4), sequence_a4]

        while True:
            if a1[0] == a2[0] == a3[0] == a4[0]:
                break

            minimum = min(a1, a2, a3, a4, key=lambda x: x[0])
            minimum[0] = next(minimum[1])

        return a1[0]

    @staticmethod
    def decode_first_column(direction):
        positions_in_mns = DotPatternDecoder.find_all_positions_in_mns(direction)
        pds_in_direction = DotPatternDecoder.calculate_pds_sequence(positions_in_mns)
        sds_in_direction = np.array(DotPatternDecoder.calculate_sds_sequence(pds_in_direction))
        sds_in_direction = sds_in_direction.transpose()

        sds_seq_length = 5
        sds_in_direction = DotPatternDecoder.take_n(sds_in_direction, sds_seq_length)

        sds_positions = DotPatternDecoder.find_positions_in_sds(sds_in_direction)

        coordinate_position = DotPatternDecoder.find_coordinate_by_sds_seq(sds_positions)
        return coordinate_position


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
# print(len(DotPatternDecoder.A_1), len(DotPatternDecoder.A_2), len(DotPatternDecoder.A_3), len(DotPatternDecoder.A_4))