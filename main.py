import hashlib
import json
import time

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [vars(txn) for txn in self.transactions],
            "nonce": self.nonce
        }
        data_json = json.dumps(data, sort_keys=True).encode('utf-8')
        return hashlib.sha256(data_json).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", [], 1632535482.903651)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_last_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        
    def validate_block(self, block):
        if block.previous_hash != self.get_last_block().hash:  # Check if the block has a valid hash
            return False

        if block.hash != block.calculate_hash():  # Check if the block has a valid hash
            return False

        for transaction in block.transactions:
            if not self.validate_transaction(transaction):  # Check if all transactions in the block are valid
                return False

        if block.timestamp < self.get_last_block().timestamp:  # Check if the block has a valid timestamp
            return False

        return True  # If all checks pass, the block is valid
    
    def handle_transaction(self, transaction):
        if not self.validate_transaction(transaction):  # Check if the transaction is valid
            return False

        next_block = Block(len(self.chain), self.get_last_block().hash, [transaction])  # If the transaction is valid, add it to the next block
        self.add_block(next_block)
        return True

    def validate_transaction(self, transaction):
        if transaction.sender not in self.get_all_addresses():  # Check if the transaction has a valid sender
            return False

        if transaction.recipient not in self.get_all_addresses():  # Check if the transaction has a valid recipient
            return False

        if transaction.amount < 0:  # Check if the transaction has a valid amount
            return False

        return True   # If all checks pass, the transaction is valid

    def get_all_addresses(self):
        addresses = set()
        for block in self.chain:
            for transaction in block.transactions:
                addresses.add(transaction.sender)
                addresses.add(transaction.recipient)

        return addresses
    
# This function is used to validate a block before it is added to the blockchain
def validate_new_block(block, Blockchain):
    if block.previous_hash != Blockchain.get_last_block().hash:  # Check if the block has a valid previous hash
        return False

    if block.hash != block.calculate_hash():  # Check if the block has a valid hash
        return False

    for transaction in block.transactions:
        if not Blockchain.validate_transaction(transaction):  # Check if all transactions in the block are valid
            return False

    if block.timestamp < Blockchain.get_last_block().timestamp:  # Check if the block has a valid timestamp
        return False

    return True # If all checks pass, the block is valid

# This function can be used to handle a new transaction
def handle_new_transaction(transaction, Blockchain):
    return Blockchain.handle_transaction(transaction)
    
my_blockchain = Blockchain()  # Initialize the blockchain

# Console User Interface
while True:
    print("\nBlockchain Menu:")
    print("1. Add Transaction")
    print("2. View Blockchain")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        sender = input("Enter sender: ")
        recipient = input("Enter recipient: ")
        amount = float(input("Enter amount: "))
        transaction = Transaction(sender, recipient, amount)
        transaction_pool = [transaction]
        new_block = Block(len(my_blockchain.chain), my_blockchain.get_last_block().hash, transaction_pool)
        my_blockchain.add_block(new_block)
        print(f"Transaction added to the blockchain.")

    elif choice == "2":
        for block in my_blockchain.chain:
            print()
            print(f"Block {block.index}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Timestamp: {block.timestamp}")
            print("Transactions:")
            for txn in block.transactions:
                print(f"  Sender: {txn.sender}, Recipient: {txn.recipient}, Amount: {txn.amount}")
            print()

    elif choice == "3":
        print("Exiting the Blockchain program.")
        break

    else:
        print("Invalid choice. Please enter a valid option.")