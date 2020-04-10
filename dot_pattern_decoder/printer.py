import matplotlib.pyplot as plt
import tabulate


class Printer:
    def __init__(self):
        pass

    @staticmethod
    def plot_images(images_with_names):
        plt.figure(figsize=(10 * 5, 4.8 * 5), constrained_layout=False)

        for counter, (image, name) in enumerate(images_with_names, 151):
            plt.subplot(counter)
            plt.imshow(image, "gray")
            plt.title(name)

        plt.show()

    @staticmethod
    def print_table(it, do_transpose=True):
        #     table = [[f'Row {i}'] + list(row) for i, row in zip(range(1, N + 1), )]
        #     table = [[''] + [f'Col {i}' for i in range(1, N + 1)]] + table
        display(tabulate.tabulate(it.transpose() if do_transpose else it, tablefmt='html', floatfmt=".2f"))

    @staticmethod
    def print_directions(x_direction, y_direction):
        table = []
        for i in range(len(x_direction)):
            table.append([])
            for x, y in zip(x_direction[i], y_direction[i]):
                table[i].append(f'({int(x)} ; {int(y)})')
        Printer.print_table(table, False)

    @staticmethod
    def print_x_params(min_x, max_x, difference_x, average_x):
        display(tabulate.tabulate(
            [['min'] + list(min_x), ['max'] + list(max_x),
             ['diff'] + list(difference_x), ['avg'] + list(average_x)
             ], [f'x_{i}' for i in range(len(min_x))], tablefmt="html"
        ))

    @staticmethod
    def print_y_params(min_y, max_y, difference_y, average_y):
        display(tabulate.tabulate(
            zip([f'y_{i}' for i in range(len(min_y))], min_y, max_y, difference_y, average_y),
            ['min', 'max', 'diff', 'avg'], tablefmt="html")
        )

    @staticmethod
    def print_vertical_table(table, headers):
        display(tabulate.tabulate(table, headers, tablefmt="html"))

    @staticmethod
    def print_named_rows(bits: dict, headers: list):
        table = bits.keys()
        table = [[key, *bits[key]] for key in table]
        display(tabulate.tabulate(table, headers, tablefmt="html"))




