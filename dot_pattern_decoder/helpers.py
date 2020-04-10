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
