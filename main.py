from blockchain import Blockchain
from miner import Miner

if __name__ == "__main__":
    # Initialize the blockchain and miner
    blockchain = Blockchain()
    miner = Miner(blockchain)

    # Mine blocks
    miner.mine_block("Block 1 Data")
    miner.mine_block("Block 2 Data")
    miner.mine_block("Block 3 Data")

    # Validate the blockchain
    print("Is the blockchain valid?", blockchain.is_chain_valid())

    # Display blockchain details
    for block in blockchain.chain:
        print(f"Index: {block.index}, Timestamp: {block.timestamp}, Hash: {block.hash}, Previous Hash: {block.previous_hash}, Nonce: {block.nonce}")

    # Display miner's total rewards
    print(f"Miner's total reward: {miner.reward}")
