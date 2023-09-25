import tkinter as tk
from tkinter import ttk
import numpy as np
from MAB_UCB import MultiArmedBanditUCB, plot_data, plot_3d_data, save_to_csv

# All previous code remains unchanged...

class GUI:
    def __init__(self, bandit, iterations, c):
        self.root = tk.Tk()
        self.root.title("MultiArmedBandit GUI")
        
        self.bandit = bandit
        self.iterations = iterations
        self.c = c
        self.current_iteration = 0
        
        self.comfort_scale = ttk.Scale(self.root, from_=0, to=10, orient=tk.HORIZONTAL, length=300)
        self.comfort_scale.set(5)
        self.comfort_scale.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W)
        
        self.continuity_scale = ttk.Scale(self.root, from_=0, to=10, orient=tk.HORIZONTAL, length=300)
        self.continuity_scale.set(5)
        self.continuity_scale.grid(row=1, column=0, padx=20, pady=20, sticky=tk.W)
        
        self.play_signal_btn = ttk.Button(self.root, text="Play Signal", command=self.play_signal)
        self.play_signal_btn.grid(row=2, column=0, padx=20, pady=20, sticky=tk.W)
        
        self.submit_btn = ttk.Button(self.root, text="Submit Feedback", command=self.submit_feedback)
        self.submit_btn.grid(row=2, column=0, padx=20, pady=20, sticky=tk.E)
        
        self.output_text = ttk.Label(self.root, text="", wraplength=280)
        self.output_text.grid(row=3, column=0, padx=20, pady=20)
        
        # Add the plot data button, initially disabled
        self.plot_data_btn = ttk.Button(self.root, text="Plot Data", command=self.plot_data, state=tk.DISABLED)
        self.plot_data_btn.grid(row=4, column=0, padx=20, pady=20)

        self.save_data_btn = ttk.Button(self.root, text="Save Data to CSV", command=self.save_data, state=tk.DISABLED)
        self.save_data_btn.grid(row=4, column=1, padx=20, pady=20)  # You may want to adjust grid coordinates as needed

        
    def play_signal(self):
        # Placeholder for now
        print("Playing Signal...")
        
    def submit_feedback(self):
        if self.current_iteration < self.iterations:
            comfort = self.comfort_scale.get()
            continuity = self.continuity_scale.get()
            reward = comfort + continuity

            chosen_arm = self.bandit.choose_arm(self.current_iteration, self.c)
            self.bandit.update(chosen_arm, reward, comfort, continuity)
            
            self.output_text['text'] = (f"Iteration {self.current_iteration+1}\n"
                                        f"Chosen Arm: {chosen_arm+1}\n"
                                        f"Comfort: {comfort}\n"
                                        f"Continuity: {continuity}")
            
            self.current_iteration += 1
        else:
            self.output_text['text'] = "All iterations completed!"
            self.plot_data_btn.config(state=tk.NORMAL)
            self.save_data_btn.config(state=tk.NORMAL)

    def run(self):
        self.root.mainloop()
        
    def plot_data(self):
        plot_data(self.bandit.arm_comfort_data, 'Comfort')
        plot_data(self.bandit.arm_continuity_data, 'Continuity')
        plot_3d_data(self.bandit.arm_comfort_data, self.bandit.arm_continuity_data)
        save_to_csv(self.bandit.arm_comfort_data, self.bandit.arm_continuity_data)
        
    def save_data(self):
        save_to_csv(self.bandit.arm_comfort_data, self.bandit.arm_continuity_data)

def main():
    # Initial parameters
    pair_freq_timeDelay = np.array([[10,0.5], [10,1], [40,0.5], [40, 1], [100, 0.5], [100,1], 
                                   [150,0.2], [150,0.5] , [200,0.2], [200,0.5]])
    n_arms = len(pair_freq_timeDelay)
    c = 4 
    iterations = 20
    bandit = MultiArmedBanditUCB(n_arms)

    # Start the GUI
    app = GUI(bandit, iterations, c)
    app.run()

# Plots and saving data can be added as buttons on the GUI or run after closing the GUI
if __name__ == "__main__":
    main()