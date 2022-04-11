"""Calculates the optimal size of a cell inside a grid"""

SIZE = "size"
MARGIN = "margin"
PADDING = "padding"
OFFSET = "offset"
BOUNDS = "bounds"


def get_window_optimal_size(index: int, **kwargs):
    """
    Calculates the optimal size of a window for a given index inside a grid
    :param index: The Window's index inside the grid
    :param kwargs: size, bounds, margin, padding, offset
    :return: a tuple containing (x_position, y_position, width, height)
    """
    columns, rows = kwargs[SIZE]
    screen_width, screen_height = kwargs[BOUNDS]
    margin_x, margin_y = kwargs[MARGIN]
    base_padding_x, base_padding_y = kwargs[PADDING]
    base_offset_x, base_offset_y = kwargs[OFFSET]

    padding_x = base_padding_x + margin_x
    padding_y = base_padding_y + margin_y
    offset_x = base_offset_x + margin_x
    offset_y = base_offset_y + margin_y

    width = int(screen_width / columns) - padding_x
    height = int(screen_height / rows) - padding_y

    x_index = int(index % columns)
    y_index = int(index / columns)

    effective_padding_x = x_index * -padding_x
    effective_padding_y = y_index * -padding_y

    x_position = x_index * width - effective_padding_x + offset_x
    y_position = y_index * height - effective_padding_y + offset_y

    return x_position, y_position, width, height
