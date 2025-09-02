import os

class Account:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            with open(filepath, 'w') as file:
                file.write("0")
        with open(filepath, 'r') as file:
            self.balance = int(file.read())
            
    def withdraw(self, amount):
        self.balance -= amount
    
    def deposit(self, amount):
        self.balance += amount
        
    def commit(self):
        with open(self.filepath, 'w') as file:
            file.write(str(self.balance))

account = Account("./balance.txt")
print("Balance inicial:", account.balance)

account.withdraw(100)
print("Balance después de retirar 100:", account.balance)

account.commit()
