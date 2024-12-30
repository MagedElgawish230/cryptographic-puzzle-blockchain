import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import time
from block import Block
from blockchain import Blockchain
from miner import Miner
import os

class MinerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Cryptographic Puzzle Miner")
        self.master.geometry("600x400")
        self.master.config(bg="#F0F0F0")

        # Initialize blockchain and miner
        self.blockchain = Blockchain()
        self.miner = Miner(self.blockchain)

        # Load difficulty from file if it exists
        self.load_difficulty()

        # Timer variables
        self.start_time = None
        self.current_time = 0
        self.is_mining = False  # Flag to track mining status
        self.stop_event = threading.Event()  # Event to signal thread stop

        # Create UI Frames
        self.info_frame = tk.Frame(self.master, bg="#F0F0F0")
        self.info_frame.pack(pady=20)

        self.mining_frame = tk.Frame(self.master, bg="#F0F0F0")
        self.mining_frame.pack(pady=20)

        self.buttons_frame = tk.Frame(self.master, bg="#F0F0F0")
        self.buttons_frame.pack(pady=20)

        # UI Elements for Info Frame
        self.reward_label = tk.Label(self.info_frame, text="Miner's Total Reward: 0", font=("Arial", 12), bg="#F0F0F0")
        self.reward_label.pack()

        self.last_block_reward_label = tk.Label(self.info_frame, text="Last Block Reward: 0", font=("Arial", 12), bg="#F0F0F0")
        self.last_block_reward_label.pack()

        self.block_info_label = tk.Label(self.info_frame, text="Mining Block...", font=("Arial", 10), bg="#F0F0F0")
        self.block_info_label.pack()

        self.timer_label = tk.Label(self.info_frame, text="Timer: 0s", font=("Arial", 12), bg="#F0F0F0")
        self.timer_label.pack()

        self.mining_speed_label = tk.Label(self.info_frame, text="Mining Speed: 0 hashes/h", font=("Arial", 12), bg="#F0F0F0")
        self.mining_speed_label.pack()

        # UI Elements for Mining Frame (Progress bar, etc.)
        self.progress_bar_label = tk.Label(self.mining_frame, text="Mining Progress:", font=("Arial", 12), bg="#F0F0F0")
        self.progress_bar_label.pack(pady=10)

        self.progress = ttk.Progressbar(self.mining_frame, length=300, mode='indeterminate')
        self.progress.pack()

        # UI Elements for Buttons Frame
        self.start_button = tk.Button(self.buttons_frame, text="Start Mining", command=self.start_mining, font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised", width=15)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.buttons_frame, text="Stop Mining", command=self.stop_mining, font=("Arial", 12), bg="#F44336", fg="white", relief="raised", width=15)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        self.stop_button.config(state=tk.DISABLED)  # Initially disabled

        self.quit_button = tk.Button(self.buttons_frame, text="Quit", command=self.quit_app, font=("Arial", 12), bg="#9E9E9E", fg="white", relief="raised", width=15)
        self.quit_button.pack(side=tk.LEFT, padx=10)

        # Bind the window close event to handle cleanup
        self.master.protocol("WM_DELETE_WINDOW", self.quit_app)

    def start_mining(self):
        """ Start mining in a separate thread to avoid freezing the GUI. """
        if not self.is_mining:
            self.is_mining = True
            self.start_button.config(state=tk.DISABLED)  # Disable the start button
            self.stop_button.config(state=tk.NORMAL)  # Enable the stop button
            self.block_info_label.config(text="Mining Block 1...")  # Update status label
            self.start_time = time.time()  # Record the start time for the timer

            # Start the progress bar animation
            self.progress.start()

            # Create a new thread for mining
            self.stop_event.clear()  # Clear any previous stop signal
            mining_thread = threading.Thread(target=self.mine_blocks)
            mining_thread.daemon = True  # Ensure the thread will exit when the program ends
            mining_thread.start()

    def mine_blocks(self):
        """ Simulate mining multiple blocks in the background. """
        try:
            total_time = 0
            for i in range(3):  # Mine 3 blocks for example
                if self.stop_event.is_set():
                    print("Mining stopped.")
                    break  # Stop mining if the user presses the stop button or closes the window

                block_data = f"Block {i + 1} Data"
                self.miner.mine_block(block_data)

                # Update GUI with the new reward and block info
                self.update_gui_after_mining(i + 1)
                total_time += self.miner.block_mining_time  # Track the total mining time
                time.sleep(2)  # Simulate mining time (you can adjust the sleep time as needed)

                # Update mining speed and timer
                self.update_timer()
                self.update_mining_speed(total_time)

            # After mining is done
            self.progress.stop()  # Stop the progress bar animation
            self.block_info_label.config(text="Mining Completed")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during mining: {e}")
        finally:
            self.start_button.config(state=tk.NORMAL)  # Re-enable the start button
            self.stop_button.config(state=tk.DISABLED)  # Disable the stop button

    def stop_mining(self):
        """ Stop the mining process and save the adjusted difficulty. """
        self.is_mining = False
        self.stop_event.set()  # Signal the mining thread to stop
        self.save_difficulty()  # Save the current difficulty before stopping
        self.block_info_label.config(text="Mining Stopped")
        self.start_button.config(state=tk.NORMAL)  # Re-enable the start button
        self.stop_button.config(state=tk.DISABLED)  # Disable the stop button
        self.progress.stop()  # Stop the progress bar animation

    def update_gui_after_mining(self, block_index):
        """ Update the GUI after mining a block. """
        self.reward_label.config(text=f"Miner's Total Reward: {self.miner.reward}")
        self.last_block_reward_label.config(text=f"Last Block Reward: {self.miner.block_reward}")
        self.block_info_label.config(text=f"Mining Block {block_index + 1}...")

    def update_timer(self):
        """ Update the timer display in the GUI. """
        if self.start_time:
            self.current_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Timer: {self.current_time}s")
        self.master.after(1000, self.update_timer)  # Update every 1 second

    def update_mining_speed(self, total_time):
        """ Calculate and update the mining speed (hashes per hour). """
        if total_time > 0:
            total_hashes = self.miner.blockchain.chain[-1].nonce  # Approximate number of hashes as nonce value
            hashes_per_hour = (total_hashes / total_time) * 3600  # Convert to hashes per hour
            self.mining_speed_label.config(text=f"Mining Speed: {hashes_per_hour:.2f} hashes/h")

    def save_difficulty(self):
        """ Save the current difficulty to a file. """
        with open("difficulty.txt", "w") as file:
            file.write(str(self.blockchain.difficulty))
            print(f"Saved difficulty: {self.blockchain.difficulty}")

    def load_difficulty(self):
        """ Load the difficulty from a file if it exists. """
        if os.path.exists("difficulty.txt"):
            with open("difficulty.txt", "r") as file:
                saved_difficulty = file.read()
                self.blockchain.difficulty = int(saved_difficulty)
                print(f"Loaded difficulty: {self.blockchain.difficulty}")
        else:
            print("No saved difficulty, using default.")
    
    def quit_app(self):
        """ Handle cleanup when the user quits the application. """
        self.stop_mining()  # Stop mining if it's active
        self.master.quit()  # Close the window


# Create the GUI window and run the application
if __name__ == "__main__":
    root = tk.Tk()
    miner_gui = MinerGUI(root)
    root.mainloop()
