import pickle
import matplotlib.pyplot as plt
import sys
import os


def load_data(filename):
    filepath = os.path.join('Results', filename)
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data


def plot_data(data):
    for trial in data:
        trial_number = trial["trial_number"]
        cursor_positions = trial["cursor_positions"]

        x_positions = [pos[0] for pos in cursor_positions]
        y_positions = [pos[1] for pos in cursor_positions]

        plt.figure()
        plt.plot(x_positions, y_positions, label=f'Trial {trial_number}')
        plt.scatter(x_positions[0], y_positions[0], color='green', label='Start')
        plt.scatter(x_positions[-1], y_positions[-1], color='red', label='End')
        plt.title(f'Trial {trial_number}')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.legend()
        plt.gca().invert_yaxis()  # Invert y-axis to match screen coordinates
        plt.show()


def main(filename=None):
    if filename is None:
        filename = 'Results/data_01_20240711_003011.pkl'
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return

    print(f'{filename=}')

    data = load_data(filename)
    plot_data(data)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python read_participant_data.py <pkl_file>")
        # print("Calling with default values!")
        filename = None
        # filename = 'data_01_20240711_003011.pkl'
        # filename = 'data_12_20240711_004126.pkl'
        # filename = 'data_24_20240712_115133.pkl'
        filename = 'Results/data_25_20240712_115805.pkl'

        main(filename=filename)
    else:
        filename = sys.argv[1]
        main(filename)
