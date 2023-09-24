# MBA_UCB

Sure, here's a simple `README.md` for your Python program:

---

# Multi-Armed Bandit with UCB

The Multi-Armed Bandit with Upper Confidence Bound (UCB) is a decision-making algorithm that helps in maximizing the reward when faced with multiple choices with uncertain outcomes. This Python program simulates the multi-armed bandit problem using pairs of frequency and time delay as arms.

## Features

1. Implements the UCB algorithm to decide which arm to choose next.
2. Gathers user input for two metrics: "Comfort" and "Continuity" for each selected arm.
3. Plots 2D graphs for both Comfort and Continuity against arm numbers, showing both raw data points and the average for each arm.
4. Generates a 3D plot showing the relationship between arm number, comfort, and continuity.
5. Saves the data (Comfort and Continuity for each arm over iterations) to a CSV file.

## Prerequisites

- Python 3.x
- NumPy
- Matplotlib

## How to Run

1. Ensure that you have Python installed on your system.
2. Install the required libraries:

```
pip install numpy matplotlib
```

3. Run the program:

```
python <filename>.py
```

4. Follow the on-screen prompts. After each iteration, you'll be asked to input values for "Comfort" and "Continuity" for the selected arm.
5. At the end of all iterations, you'll see the plots, and the data will be saved to a CSV file named using the current timestamp.

## Contributing

Pull requests are welcome. Please open an issue first if you want to propose a change or discuss something.

---

You can save the above content in a file named `README.md` in the same directory as your Python program. Adjust the `<filename>.py` placeholder with your actual Python file name.