import time
from block import Block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.mining_time_target = 10  # Target block generation time in seconds
        self.mining_times = []

    def create_genesis_block(self):
        """
        Create the first block in the chain.
        """
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        """
        Retrieve the last block in the chain.
        """
        return self.chain[-1]

    def add_block(self, new_block):
        """
        Add a new block to the blockchain after mining.
        """
        new_block.previous_hash = self.get_latest_block().hash
        start_time = time.time()
        new_block.mine_block(self.difficulty)
        end_time = time.time()
        self.chain.append(new_block)
        self.adjust_difficulty(end_time - start_time)

    def adjust_difficulty(self, mining_time):
        """
        Dynamically adjust the difficulty to maintain the target block generation time.
        """
        self.mining_times.append(mining_time)
        if len(self.mining_times) > 5:  # Keep a sliding window of 5 blocks
            self.mining_times.pop(0)
        avg_time = sum(self.mining_times) / len(self.mining_times)
        if avg_time < self.mining_time_target:
            self.difficulty += 1
        elif avg_time > self.mining_time_target and self.difficulty > 1:
            self.difficulty -= 1
        print(f"Adjusted difficulty: {self.difficulty}")

    def is_chain_valid(self):
        """
        Validate the blockchain's integrity.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check the hash of the current block
      
