import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import datetime

class MultiArmedBanditUCB:
    def __init__(self, n_arms):
        self.n = n_arms
        # Initialize arm related data structures
        self.arm_counts = [0] * n_arms
        self.arm_values = [0.] * n_arms
        self.arm_comfort_data = {arm: [] for arm in range(n_arms)}
        self.arm_continuity_data = {arm: [] for arm in range(n_arms)}
        
    def choose_arm(self, t, c):
        # UCB formula for choosing arms
        for i in range(self.n):
            if self.arm_counts[i] == 0:
                return i
        
        ucb_values = [self.arm_values[i] + c * math.sqrt(math.log(t+1) / self.arm_counts[i]) for i in range(self.n)]
        return ucb_values.index(max(ucb_values))
    
    def update(self, chosen_arm, reward, comfort, continuity):
        # Update chosen arm data
        self.arm_counts[chosen_arm] += 1
        self.arm_comfort_data[chosen_arm].append(comfort)
        self.arm_continuity_data[chosen_arm].append(continuity)
        
        n = self.arm_counts[chosen_arm]
        value = self.arm_values[chosen_arm]
        
        # Use a running average to update the value of the chosen arm
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.arm_values[chosen_arm] = new_value

def plot_data(arm_data, title):
    # 2D Plot: raw data points and average
    arms = list(arm_data.keys())
    avg_values = [np.mean(arm_data[arm]) for arm in arms]
    
    for arm, values in arm_data.items():
        plt.scatter([arm] * len(values), values, color='blue', marker='o', s=10)
    plt.scatter(arms, avg_values, color='red', marker='o', s=40, label='Average')

    plt.ylabel(title)
    plt.xlabel('Arm')
    plt.title(title + ' for Each Arm')
    plt.xticks(arms)
    plt.legend(loc='upper left')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

def plot_3d_data(arm_comfort_data, arm_continuity_data):
    # 3D Plot: arm number vs. comfort vs. continuity
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for arm, comfort_values in arm_comfort_data.items():
        continuity_values = arm_continuity_data[arm]
        ax.scatter([arm] * len(comfort_values), comfort_values, continuity_values, c='blue', marker='o')

    ax.set_xlabel('Arm Number')
    ax.set_ylabel('Comfort')
    ax.set_zlabel('Continuity')
    ax.set_title('3D View of Arm Number vs Comfort vs Continuity')
    plt.show()

def save_to_csv(arm_comfort_data, arm_continuity_data):
    # Save comfort and continuity data to a CSV file
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_{current_time}.csv"

    max_length = max([len(values) for values in arm_comfort_data.values()])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Create the header for the CSV file
        writer.writerow(["Iteration"] + [f"Arm_{arm}_Comfort" for arm in arm_comfort_data.keys()] + 
                        [f"Arm_{arm}_Continuity" for arm in arm_continuity_data.keys()])

        for i in range(max_length):
            row = [i+1]
            for data in [arm_comfort_data, arm_continuity_data]:
                for arm, values in data.items():
                    if i < len(values):
                        row.append(values[i])
                    else:
                        row.append('')
            writer.writerow(row)

    print(f"Data saved to {filename}")

def main():
    # Initial parameters
    pair_freq_timeDelay = np.array([[10,0.5], [10,1], [40,0.5], [40, 1], [100, 0.5], [100,1], 
                                   [150,0.2], [150,0.5] , [200,0.2], [200,0.5]])
    n_arms = len(pair_freq_timeDelay)
    c = 4 
    iterations = 30
    bandit = MultiArmedBanditUCB(n_arms)
    cumulative_reward = 0
    
    # Main loop to get user inputs and update the bandit
    for i in range(iterations):
        chosen_arm = bandit.choose_arm(i, c)

        while True:
            comfort_input = input(f"Enter comfort for arm {chosen_arm+1} (0-10): ")
            continuity_input = input(f"Enter continuity for arm {chosen_arm+1} (0-10): ")

            if comfort_input.isnumeric() and 0 <= float(comfort_input) <= 10 and \
               continuity_input.isnumeric() and 0 <= float(continuity_input) <= 10:
                comfort = float(comfort_input)
                continuity = float(continuity_input)
                break
            else:
                print("Invalid inputs. Enter values in the range (0-10).")

        reward = comfort + continuity
        bandit.update(chosen_arm, reward, comfort, continuity)
        cumulative_reward += reward

        print(f"Iteration {i+1}")
        print(f"Current best arm: {bandit.arm_values.index(max(bandit.arm_values))+1}")
        print(f"Cumulative reward: {cumulative_reward}\n")

    print(f"The best arm at the end of 30 iterations is: Arm {bandit.arm_values.index(max(bandit.arm_values))+1}")

    # Plotting and saving data
    plot_data(bandit.arm_comfort_data, 'Comfort')
    plot_data(bandit.arm_continuity_data, 'Continuity')
    plot_3d_data(bandit.arm_comfort_data, bandit.arm_continuity_data)
    save_to_csv(bandit.arm_comfort_data, bandit.arm_continuity_data)

