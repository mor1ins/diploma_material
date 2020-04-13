import math
import os

import cv2
import numpy as np
from constants import Constants
from skimage.measure import label, regionprops
from helpers import sequence_p, transpose, find
from PIL import Image, ImageFilter, ImageDraw
from pathlib import Path


class Direction:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.average = coordinates.mean(axis=1)
        self.max = coordinates.max(axis=1)
        self.min = coordinates.min(axis=1)
        self.difference = self.max - self.min
        self.threshold_for_class = 2 / 3 * self.difference.max()
        self.classes = [
            'A' if diff > self.threshold_for_class else 'B'
            for diff in self.difference]

    def zip_all(self):
        return zip(self.average, self.max, self.min, self.difference, self.classes)


class DotPatternDecoder:
    MNS = Constants.MNS
    A_1 = Constants.A_1
    A_2 = Constants.A_2
    A_3 = Constants.A_3
    A_4 = Constants.A_4

    def __init__(self, path_to_image=None):
        if path_to_image is None or not (os.path.exists(path_to_image) and os.path.isfile(path_to_image)):
            self.raw_image = None
        else:
            self.raw_image = Image.open(path_to_image)
        self.image_grayscale = None
        self.deleted_noise_image = None
        self.deleted_noise_image_with_centroids = None
        self.black_white_image = None
        self.centroids_image = None
        self.direction_x = None
        self.direction_y = None
        self.x_codes = None
        self.y_codes = None

    def convert_to_grayscale(self):
        return self.raw_image.convert(mode='LA')

    @staticmethod
    def split_into_three_intervals(minimum, maximum):
        diff = maximum - minimum
        border_1 = minimum + 1 / 3 * diff
        border_2 = border_1 + 1 / 3 * diff
        return (minimum, border_1), (border_1, border_2), (border_2, maximum)

    @staticmethod
    def split_into_two_intervals(minimum, maximum):
        diff = maximum - minimum
        border_1 = minimum + 1 / 2 * diff
        return (minimum, border_1), (border_1, maximum)

    @staticmethod
    def value_belongs_to_interval(value, interval):
        return interval[0] <= value <= interval[1]

    def get_position_code(self, value, intervals, codes):
        for i in range(len(intervals)):
            if self.value_belongs_to_interval(value, intervals[i]):
                return codes[i]

    def split_into_intervals(self, minimum, maximum, klass):
        if klass == 'A':
            return self.split_into_three_intervals(minimum, maximum)
        else:
            return self.split_into_two_intervals(minimum, maximum)

    def get_position_codes_by_direction(self, direction: Direction):
        intervals = [
            self.split_into_intervals(minimum, maximum, klass)
            for coordinate, maximum, minimum, diff, klass in direction.zip_all()
        ]

        codes = np.zeros_like(direction.coordinates)
        for i in range(len(codes)):
            for j in range(len(codes[i])):
                value = direction.coordinates[i, j]
                interval = intervals[i]
                possible_codes = [-1, 0, 1] if direction.classes[i] == 'A' else [-2, 2]
                codes[i, j] = self.get_position_code(value, interval, possible_codes)

        return codes

    @staticmethod
    def reverse_sign(array):
        new_array = array.copy()
        for i in range(len(new_array)):
            for j in range(len(new_array)):
                if new_array[i, j] != 0:
                    new_array[i, j] *= -1
        return new_array

    def get_position_codes(self, centroids):
        self.direction_x = Direction(centroids[:, :, 0])
        self.direction_y = Direction(centroids[:, :, 1].transpose())

        self.x_codes = self.get_position_codes_by_direction(self.direction_x)
        y_codes = self.get_position_codes_by_direction(self.direction_y).transpose()
        self.y_codes = self.reverse_sign(y_codes)

        self.direction_y.coordinates = self.direction_y.coordinates.transpose()
        return self.x_codes, self.y_codes

    @staticmethod
    def get_centroids(image):
        image = np.array(image.convert(mode='1'))
        label_img = label(image)
        regions = regionprops(label_img)
        return np.array([region.centroid for region in regions])

    @staticmethod
    def make_dots_thick(points):
        thick_centroids = []
        for p in points:
            x, y = p
            possible_offsets = [-1, 0, 1]
            for offset_x in possible_offsets:
                for offset_y in possible_offsets:
                    thick_centroids.append((x + offset_x, y + offset_y))

        return thick_centroids

    @staticmethod
    def get_white_image_like(image):
        white_image = np.zeros_like(image)
        for y in range(image.height):
            for x in range(image.width):
                white_image[y, x] = [255, 255]
        return white_image

    @staticmethod
    def binarize_image(image, threshold=110):
        image = image.convert('LA')
        image = np.array(image)
        for raw in image:
            for column in raw:
                column[0] = 0 if column[0] < threshold else 255
        return Image.fromarray(image)

    @staticmethod
    def points_to_image(image, points):
        array = np.array(image)
        for y, x in points:
            array[int(y), int(x)] = [0, 255]
        image = Image.fromarray(array)
        return image

    def preprocess_image(self):
        self.image_grayscale = self.convert_to_grayscale()
        self.black_white_image = self.binarize_image(self.image_grayscale)
        self.deleted_noise_image = self.black_white_image.filter(ImageFilter.MedianFilter(3))
        centroids = self.get_centroids(self.deleted_noise_image)
        centroids_with_neighbours = self.make_dots_thick(centroids)
        centroids_zero_array = self.get_white_image_like(self.deleted_noise_image)
        self.deleted_noise_image_with_centroids = self.points_to_image(self.deleted_noise_image, centroids_with_neighbours)
        self.centroids_image = self.points_to_image(centroids_zero_array, centroids_with_neighbours)

        # image_fft, fft_points = fft(raw_image.convert(mode='RGB'), 0.06)
        # ret, image_fft = cv2.threshold(image_fft, 1, 255, cv2.THRESH_BINARY)

        N = int(math.sqrt(len(centroids)))
        centroids_in_grid = centroids[np.argsort(centroids[:, 0])].reshape(N, N, 2)

        for i in range(N):
            centroids_in_grid[i] = centroids_in_grid[i][np.argsort(centroids_in_grid[i][:, 1])]

        return centroids_in_grid

    @staticmethod
    def dir2pos(x, y):
        translations = Constants.DIRECTIONS_TO_BITS_TRANSLATIONS
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

    @staticmethod
    def replace_code_in_line(line, code, to):
        DotPatternDecoder.replace(line, [(code, to), (-1 * code, np.sign(-1 * code) * to)])

    @staticmethod
    def get_replacements(what, to, other):
        return [(what, to), (-1 * what, other)]

    def correction_position_2(self, first, second):
        indexes = range(len(first))
        for j in indexes:
            for i in indexes:
                x_code, y_code = first[i, j], second[i, j]
                if abs(y_code) == 2:
                    if abs(x_code) == 1:
                        new_line = self.replace(
                            second[i], self.get_replacements(what=y_code, to=0, other=-1 * np.sign(y_code))
                        )
                        second[i] = new_line
                    elif abs(x_code) == 0:
                        new_line = self.replace(
                            second[i], self.get_replacements(what=y_code, to=np.sign(y_code), other=0)
                        )
                        second[i] = new_line

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

    def code_correction(self):
        self.correction_position_2(self.x_codes, self.y_codes)
        self.correction_position_2(self.x_codes, self.x_codes)

    def decode(self):
        self.get_position_codes(self.preprocess_image())
        self.code_correction()

    @staticmethod
    def filter_with_threshold(matrix, threshold):
        filtered = np.zeros_like(matrix)
        points = []
        for y in range(len(filtered)):
            raw = []
            need_append = False
            for x in range(len(filtered[y])):
                if matrix[y, x] > threshold:
                    filtered[y, x] = matrix[y, x]
                    raw.append((x, y))
                    need_append = True

            if need_append:
                points.append(raw)

        return np.log(1 + np.abs(filtered)), points

    def fft(self, image_for_fft, threshold):
        image_for_cv = cv2.cvtColor(np.array(image_for_fft), cv2.COLOR_RGB2GRAY)

        img_c2 = np.fft.fft2(image_for_cv)
        img_c3 = np.fft.ifftshift(img_c2)
        img_c5, points = self.filter_with_threshold(img_c3, img_c3.max() * threshold)
        #   img_c5, points = img_c3, points
        return img_c5, points

    @staticmethod
    def add_virtual_lines(image, values_x, values_y):
        virtual_lines = image.convert(mode='RGB')
        drawer = ImageDraw.Draw(virtual_lines)
        color = (0, 255, 255)
        for x in values_x:
            drawer.line([(x, 0), (x, virtual_lines.height)], fill=color, width=1)

        for y in values_y:
            drawer.line([(0, y), (virtual_lines.width, y)], fill=color, width=1)

        return virtual_lines

    @staticmethod
    def filter_by_class(classes, widths, target_class):
        return list(map(
            lambda v: v[1],
            filter(lambda c: c[0] == target_class, zip(classes, widths))
        ))

    def get_avg_by_class(self, classes, target_class, widths):
        return np.array(list(self.filter_by_class(classes, widths, target_class))).mean()

    @staticmethod
    def get_new_position(coordinate, width, avg_width):
        return coordinate - width / 2

    @staticmethod
    def correction_virtual_lines(self, lines_coordinate, classes, widths):
        avg_for_class_a = self.get_avg_by_class(classes, 'A', widths)
        new_coordinates = [
            self.get_new_position(coordinate, width, avg_for_class_a)
            for coordinate, width
            in zip(
                self.filter_by_class(classes, lines_coordinate, 'B'),
                self.filter_by_class(classes, widths, 'B')
            )
        ]
        j = 0
        for i in range(len(lines_coordinate)):
            if classes[i] == 'B':
                lines_coordinate[i] = new_coordinates[j]
                j += 1

        return lines_coordinate

