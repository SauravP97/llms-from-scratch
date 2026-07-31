import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import torch

MAX_COL_LENGTH_FOR_2D_VISUALIZATION = 16
MAX_ROW_LENGTH_FOR_2D_VISUALIZATION = 16

MAX_COL_LENGTH_FOR_3D_VISUALIZATION = 4
MAX_ROW_LENGTH_FOR_3D_VISUALIZATION = 4

MAX_THIRD_DIMENSION_LENGTH_FOR_VISUALIZATION = 3


def visualize_3d_matrix(
    matrix: torch.Tensor, x_label="", y_label="", z_label="", width=6
):
    if len(matrix.shape) != 3:
        raise ValueError("Input matrix must be 3 dimensional for visualization")

    third_dimension_size = matrix.shape[0]
    fig, ax = plt.subplots(
        1,
        min(third_dimension_size, MAX_THIRD_DIMENSION_LENGTH_FOR_VISUALIZATION),
        figsize=(width, 6),
    )

    for i in range(third_dimension_size):
        if i >= 3:
            print(
                f"Capping the 3rd dimension size at {MAX_THIRD_DIMENSION_LENGTH_FOR_VISUALIZATION}, provided: {third_dimension_size}"
            )
            break

        ax[i] = _visualize_matrix(
            matrix[i].detach().numpy(),
            ax[i],
            MAX_COL_LENGTH_FOR_3D_VISUALIZATION,
            MAX_ROW_LENGTH_FOR_3D_VISUALIZATION,
            x_label,
            y_label,
        )
    plt.show()


def visualize_2d_matrix(matrix: torch.Tensor, x_label="", y_label="", width=6):
    matrix = matrix.detach().numpy()
    fig, ax = plt.subplots(figsize=(width, 6))

    ax: Axes = _visualize_matrix(
        matrix,
        ax,
        MAX_COL_LENGTH_FOR_2D_VISUALIZATION,
        MAX_ROW_LENGTH_FOR_2D_VISUALIZATION,
        x_label,
        y_label,
    )
    plt.show()


def _visualize_matrix(
    matrix: torch.Tensor,
    ax: Axes,
    max_col_len: int,
    max_row_len: int,
    x_label="",
    y_label="",
) -> Axes:
    # Set limits and invert the y-axis to match standard matrix row order
    rows, cols = matrix.shape
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(rows - 0.5, -0.5)

    if cols <= max_col_len and rows <= max_row_len:
        # Loop through the grid and print each number as text
        for i in range(rows):
            for j in range(cols):
                if isinstance(
                    matrix[i, j],
                    (int, float, complex, np.float64, np.int32, np.float32),
                ):
                    formatted_num = f"{matrix[i, j]:.2f}"
                    ax.text(
                        j, i, str(formatted_num), va="center", ha="center", fontsize=14
                    )
                else:
                    ax.text(
                        j, i, str(matrix[i, j]), va="center", ha="center", fontsize=14
                    )
    else:
        # Loop through the grid and print each number as text
        column_capped = False
        rows_capped = False

        if rows > max_row_len:
            print(f"Max Row limit exceeded, Allowed: {max_row_len}, Received: {rows}")
            print(f"Capping rows at: {max_row_len}")
            rows = max_row_len
            rows_capped = True

        if cols > max_col_len:
            print(
                f"Max Column limit exceeded, Allowed: {max_col_len}, Received: {cols}"
            )
            print(f"Capping columns at: {max_col_len}")
            column_capped = True
            cols = max_col_len

        ax.set_xlim(-0.5, cols + 1 - 0.5)
        ax.set_ylim(rows + 1 - 0.5, -0.5)

        for i in range(rows):
            for j in range(cols):
                if isinstance(
                    matrix[i, j],
                    (int, float, complex, np.float64, np.int32, np.float32),
                ):
                    formatted_num = f"{matrix[i, j]:.2f}"
                    ax.text(
                        j, i, str(formatted_num), va="center", ha="center", fontsize=14
                    )
                else:
                    ax.text(
                        j, i, str(matrix[i, j]), va="center", ha="center", fontsize=14
                    )
            if column_capped:
                ax.text(cols, i, "...", va="center", ha="center", fontsize=14)

        if rows_capped:
            for j in range(cols + 1):
                ax.text(j, rows, "...", va="center", ha="center", fontsize=14)

    # Strip away all visual chart elements
    ax.set_xlabel(x_label, fontsize=12, labelpad=10)
    ax.set_ylabel(y_label, fontsize=12, labelpad=10)
    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))

    return ax
