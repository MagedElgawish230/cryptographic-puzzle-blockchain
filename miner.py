import time
from block import Block

class Miner:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.reward = 0  # Initialize miner reward

    def mine_block(self, data):
        """
        Mine a new block with the given data and add it to the blockchain.
        """
        new_block = Block(
            index=len(self.blockchain.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=self.blockchain.get_latest_block().hash
        )

        # Start mining
        print(f"Mining block {new_block.index}...")
        start_time = time.time()
        new_block.mine_block(self.blockchain.difficulty)
        end_time = time.time()

        # Add the block to the blockchain and update rewards
        self.blockchain.add_block(new_block)
        mining_time = end_time - start_time
        self.reward += self.calculate_reward(mining_time)
        print(f"Block {new_block.index} mined in {mining_time:.2f} seconds. Reward: {self.reward}")

    def calculate_reward(self, mining_time):
        """
        Calculate the miner's reward based on the mining time.
        """
        base_reward = 50  # Base reward in tokens
        # Adjust reward slightly based on mining time
        return max(base_reward - (mining_time * 2), 10)  # Minimum reward of 10
