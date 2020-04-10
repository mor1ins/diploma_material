import numpy as np
import constants
from helpers import sequence_p, transpose, find


class DotPatternDecoder:
    MNS = constants.MNS
    A_1 = constants.A_1
    A_2 = constants.A_2
    A_3 = constants.A_3
    A_4 = constants.A_4

    def __init__(self):
        pass

    def decode_image(self, image):
        pass

    @staticmethod
    def dir2pos(x, y):
        translations = constants.DIRECTIONS_TO_BITS_TRANSLATIONS
        for direction, pos in translations.values():
            if direction == (x, y):
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
            find(DotPatternDecoder.A_1, sds[0]), find(DotPatternDecoder.A_2, sds[1]),
            find(DotPatternDecoder.A_3, sds[2]), find(DotPatternDecoder.A_4, sds[3]),
        )

    @staticmethod
    def find_coordinate_by_sds_seq(sds):
        a1, a2, a3, a4 = sds

        sequence_a1 = sequence_p(a1, len(DotPatternDecoder.A_1))
        sequence_a2 = sequence_p(a2, len(DotPatternDecoder.A_2))
        sequence_a3 = sequence_p(a3, len(DotPatternDecoder.A_3))

        # + 1, ибо иначе не работает, а последовательности в 240 символов
        sequence_a4 = sequence_p(a4, len(DotPatternDecoder.A_4) + 1)

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
