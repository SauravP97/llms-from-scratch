import numpy as np
import matplotlib.pyplot as plt


def visualize_matrix(matrix, x_label='', y_label='', width=6):
    # Create the plot
    matrix = matrix.detach().numpy()
    
    fig, ax = plt.subplots(figsize=(width, 6))

    # Set limits and invert the y-axis to match standard matrix row order
    rows, cols = matrix.shape
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(rows - 0.5, -0.5)

    # print(type(matrix[0,0]))
    # Loop through the grid and print each number as text
    for i in range(rows):
        for j in range(cols):
            if isinstance(matrix[i,j], (int, float, complex, np.float64, np.int32, np.float32)):
                formatted_num = f"{matrix[i, j]:.2f}"
                ax.text(j, i, str(formatted_num), va='center', ha='center', fontsize=14)
            else:
                ax.text(j, i, str(matrix[i,j]), va='center', ha='center', fontsize=14)

    # Strip away all visual chart elements
    ax.set_xlabel(x_label, fontsize=12, labelpad=10)
    ax.set_ylabel(y_label, fontsize=12, labelpad=10)
    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))

    plt.show()