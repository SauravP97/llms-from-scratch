import numpy as np
import matplotlib.pyplot as plt
import torch

MAX_COL_LENGTH_FOR_VISUALIZATION = 16
MAX_ROW_LENGTH_FOR_VISUALIZATION = 16


def visualize_3d_matrix(
    matrix: torch.Tensor, x_label="", y_label="", z_label="", width=6
):
    pass


def visualize_matrix(matrix: torch.Tensor, x_label="", y_label="", width=6):
    # Create the plot
    matrix = matrix.detach().numpy()

    fig, ax = plt.subplots(figsize=(width, 6))

    # Set limits and invert the y-axis to match standard matrix row order
    rows, cols = matrix.shape
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(rows - 0.5, -0.5)

    # print(type(matrix[0,0]))
    if (
        cols <= MAX_COL_LENGTH_FOR_VISUALIZATION
        and rows <= MAX_ROW_LENGTH_FOR_VISUALIZATION
    ):
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

        if rows > MAX_ROW_LENGTH_FOR_VISUALIZATION:
            print(
                f"Max Row limit exceeded, Allowed: {MAX_ROW_LENGTH_FOR_VISUALIZATION}, Received: {rows}"
            )
            print(f"Capping rows at: {MAX_ROW_LENGTH_FOR_VISUALIZATION}")
            rows = MAX_ROW_LENGTH_FOR_VISUALIZATION
            rows_capped = True

        if cols > MAX_COL_LENGTH_FOR_VISUALIZATION:
            print(
                f"Max Column limit exceeded, Allowed: {MAX_COL_LENGTH_FOR_VISUALIZATION}, Received: {cols}"
            )
            print(f"Capping columns at: {MAX_COL_LENGTH_FOR_VISUALIZATION}")
            column_capped = True
            cols = MAX_COL_LENGTH_FOR_VISUALIZATION

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

    plt.show()
