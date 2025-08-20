# Different types of methods in Python classes

class BankAccount:
    # Class attribute
    bank_name = "Python Bank"
    interest_rate = 0.05
    
    def __init__(self, account_holder, balance=0):
        """Constructor method"""
        self.account_holder = account_holder
        self.balance = balance
        self.transactions = []
    
    # Instance method
    def deposit(self, amount):
        """Instance method to deposit money"""
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited: ${amount}")
            return f"Deposited ${amount}. New balance: ${self.balance}"
        return "Invalid amount"
    
    def withdraw(self, amount):
        """Instance method to withdraw money"""
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrew: ${amount}")
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        return "Invalid amount or insufficient funds"
    
    def get_balance(self):
        """Instance method to get current balance"""
        return self.balance
    
    def calculate_interest(self):
        """Instance method using class attribute"""
        interest = self.balance * self.interest_rate
        return f"Interest on ${self.balance} at {self.interest_rate*100}%: ${interest:.2f}"
    
    # Class method
    @classmethod
    def create_savings_account(cls, account_holder, initial_deposit):
        """Class method - alternative constructor"""
        account = cls(account_holder, initial_deposit)
        account.account_type = "Savings"
        return account
    
    @classmethod
    def get_bank_info(cls):
        """Class method to get bank information"""
        return f"Bank: {cls.bank_name}, Interest Rate: {cls.interest_rate*100}%"
    
    @classmethod
    def update_interest_rate(cls, new_rate):
        """Class method to update interest rate"""
        cls.interest_rate = new_rate
        return f"Interest rate updated to {new_rate*100}%"
    
    # Static method
    @staticmethod
    def validate_account_number(account_number):
        """Static method - utility function"""
        return len(str(account_number)) == 10 and str(account_number).isdigit()
    
    @staticmethod
    def calculate_compound_interest(principal, rate, time, frequency=1):
        """Static method for financial calculations"""
        amount = principal * (1 + rate/frequency) ** (frequency * time)
        return round(amount - principal, 2)
    
    @staticmethod
    def format_currency(amount):
        """Static method for formatting"""
        return f"${amount:,.2f}"
    
    # Property methods (getters and setters)
    @property
    def account_info(self):
        """Property method - getter"""
        return f"Account Holder: {self.account_holder}, Balance: {self.format_currency(self.balance)}"
    
    def get_transaction_history(self):
        """Instance method to get transaction history"""
        if self.transactions:
            return "\n".join(self.transactions)
        return "No transactions yet"

# Examples of using different method types

# Using instance methods
account1 = BankAccount("Alice", 1000)
print(account1.deposit(500))
print(account1.withdraw(200))
print(account1.calculate_interest())

# Using class methods
print(BankAccount.get_bank_info())
savings_account = BankAccount.create_savings_account("Bob", 2000)
print(f"Savings account created: {savings_account.account_info}")

# Using static methods
print(f"Valid account number: {BankAccount.validate_account_number(1234567890)}")
print(f"Invalid account number: {BankAccount.validate_account_number(123)}")

compound_interest = BankAccount.calculate_compound_interest(1000, 0.05, 2)
print(f"Compound interest: ${compound_interest}")

# Using property
print(account1.account_info)

# Method chaining example
class FluentCalculator:
    def __init__(self, value=0):
        self.value = value
    
    def add(self, number):
        """Instance method that returns self for chaining"""
        self.value += number
        return self
    
    def multiply(self, number):
        """Instance method that returns self for chaining"""
        self.value *= number
        return self
    
    def subtract(self, number):
        """Instance method that returns self for chaining"""
        self.value -= number
        return self
    
    def get_result(self):
        """Instance method to get final result"""
        return self.value

# Method chaining example
calc = FluentCalculator(10)
result = calc.add(5).multiply(2).subtract(3).get_result()
print(f"Chained calculation result: {result}")

# Private methods (convention)
class SecureAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self._balance = balance  # Protected attribute
    
    def _validate_transaction(self, amount):
        """Private method (by convention)"""
        return amount > 0 and amount <= self._balance
    
    def __encrypt_data(self, data):
        """Private method with name mangling"""
        return f"encrypted_{data}"
    
    def transfer_money(self, amount, recipient):
        """Public method using private method"""
        if self._validate_transaction(amount):
            self._balance -= amount
            encrypted_info = self.__encrypt_data(f"Transfer to {recipient}")
            return f"Transferred ${amount} to {recipient}. {encrypted_info}"
        return "Transaction failed"

secure_account = SecureAccount("John", 1000)
print(secure_account.transfer_money(500, "Jane"))