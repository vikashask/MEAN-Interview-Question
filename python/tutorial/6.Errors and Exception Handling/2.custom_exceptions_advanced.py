# Custom Exceptions and Real-World Applications

"""
STEP 7: Creating Custom Exceptions
=================================
Custom exceptions help make your code more readable and maintainable
by providing specific error types for your application domain.
"""

print("=" * 60)
print("STEP 7: CUSTOM EXCEPTIONS")
print("=" * 60)

# Basic custom exception
class CustomError(Exception):
    """Base custom exception class"""
    pass

class ValidationError(CustomError):
    """Raised when data validation fails"""
    def __init__(self, message, field_name=None):
        self.field_name = field_name
        super().__init__(message)

class AuthenticationError(CustomError):
    """Raised when authentication fails"""
    def __init__(self, message, user_id=None):
        self.user_id = user_id
        super().__init__(message)

# Example usage of custom exceptions
def validate_email(email):
    """Validate email format"""
    if not isinstance(email, str):
        raise ValidationError("Email must be a string", "email")
    
    if "@" not in email:
        raise ValidationError("Email must contain @ symbol", "email")
    
    if "." not in email.split("@")[1]:
        raise ValidationError("Email must have valid domain", "email")
    
    return True

def authenticate_user(username, password):
    """Simple authentication example"""
    valid_users = {"admin": "secret123", "user": "password"}
    
    if username not in valid_users:
        raise AuthenticationError(f"User '{username}' not found", username)
    
    if valid_users[username] != password:
        raise AuthenticationError("Invalid password", username)
    
    return f"User '{username}' authenticated successfully"

# Testing custom exceptions
test_emails = ["valid@example.com", "invalid-email", 123, "no-domain@com"]

for email in test_emails:
    try:
        validate_email(email)
        print(f"✓ Valid email: {email}")
    except ValidationError as e:
        print(f"✗ Invalid email '{email}': {e} (field: {e.field_name})")

# Testing authentication
auth_tests = [("admin", "secret123"), ("admin", "wrong"), ("unknown", "any")]

for username, password in auth_tests:
    try:
        result = authenticate_user(username, password)
        print(f"✓ {result}")
    except AuthenticationError as e:
        print(f"✗ Auth failed: {e} (user_id: {e.user_id})")

"""
STEP 8: Exception Context Managers
=================================
"""

print("\n" + "=" * 60)
print("STEP 8: EXCEPTION CONTEXT MANAGERS")
print("=" * 60)

# Context manager for database-like operations
class DatabaseConnection:
    """Simulated database connection with exception handling"""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False
    
    def __enter__(self):
        """Enter the context - establish connection"""
        print(f"Connecting to database: {self.db_name}")
        self.connected = True
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context - cleanup even if exception occurred"""
        print(f"Closing connection to database: {self.db_name}")
        self.connected = False
        
        if exc_type:
            print(f"Exception occurred: {exc_type.__name__}: {exc_value}")
            # Return False to propagate the exception
            return False
        
        print("Database operation completed successfully")
        return True
    
    def execute_query(self, query):
        """Simulate query execution"""
        if not self.connected:
            raise RuntimeError("Database not connected")
        
        if "DROP" in query.upper():
            raise ValueError("DROP operations not allowed")
        
        return f"Query executed: {query}"

# Using the context manager
queries = ["SELECT * FROM users", "DROP TABLE users", "INSERT INTO users VALUES (1, 'John')"]

for query in queries:
    try:
        with DatabaseConnection("TestDB") as db:
            result = db.execute_query(query)
            print(f"Success: {result}")
    except Exception as e:
        print(f"Database operation failed: {e}")
    print("-" * 40)

"""
STEP 9: Exception Chaining and Context
=====================================
"""

print("\n" + "=" * 60)
print("STEP 9: EXCEPTION CHAINING")
print("=" * 60)

class DataProcessingError(Exception):
    """Custom exception for data processing errors"""
    pass

def process_data_file(filename):
    """Process data file with exception chaining"""
    try:
        # Simulate file processing
        with open(filename, 'r') as f:
            data = f.read()
            
        # Simulate data parsing
        if not data.strip():
            raise ValueError("File is empty")
        
        # Simulate data validation
        lines = data.split('\n')
        if len(lines) < 2:
            raise ValueError("Insufficient data rows")
        
        return f"Processed {len(lines)} lines"
        
    except FileNotFoundError as e:
        # Chain the exception - preserve original error context
        raise DataProcessingError(f"Could not process data file '{filename}'") from e
    except ValueError as e:
        # Chain the exception with additional context
        raise DataProcessingError(f"Data validation failed for '{filename}'") from e

# Test exception chaining
test_files = ["existing.txt", "nonexistent.txt"]

for filename in test_files:
    try:
        result = process_data_file(filename)
        print(f"Success: {result}")
    except DataProcessingError as e:
        print(f"Processing Error: {e}")
        print(f"Caused by: {e.__cause__}")

"""
STEP 10: Practical Exception Handling Patterns
==============================================
"""

print("\n" + "=" * 60)
print("STEP 10: PRACTICAL PATTERNS")
print("=" * 60)

# Pattern 1: Retry with exponential backoff
import time
import random

class NetworkError(Exception):
    """Simulate network-related errors"""
    pass

def unreliable_network_call():
    """Simulate an unreliable network operation"""
    if random.random() < 0.7:  # 70% chance of failure
        raise NetworkError("Network timeout")
    return "Network call successful"

def retry_with_backoff(func, max_retries=3, base_delay=1):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except NetworkError as e:
            if attempt == max_retries - 1:  # Last attempt
                raise
            
            delay = base_delay * (2 ** attempt)  # Exponential backoff
            print(f"Attempt {attempt + 1} failed: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

# Test retry pattern
try:
    result = retry_with_backoff(unreliable_network_call, max_retries=3)
    print(f"Success: {result}")
except NetworkError as e:
    print(f"All retry attempts failed: {e}")

# Pattern 2: Exception logging and monitoring
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def monitored_operation(operation_name, data):
    """Operation with comprehensive exception monitoring"""
    try:
        logger.info(f"Starting operation: {operation_name}")
        
        # Simulate different types of operations
        if operation_name == "divide":
            result = data['a'] / data['b']
        elif operation_name == "access_list":
            result = data['list'][data['index']]
        elif operation_name == "convert":
            result = int(data['value'])
        else:
            raise ValueError(f"Unknown operation: {operation_name}")
        
        logger.info(f"Operation {operation_name} completed successfully")
        return result
        
    except (ZeroDivisionError, IndexError, ValueError, KeyError) as e:
        logger.error(f"Operation {operation_name} failed: {type(e).__name__}: {e}")
        logger.error(f"Input data: {data}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error in {operation_name}: {type(e).__name__}: {e}")
        raise

# Test monitored operations
test_operations = [
    ("divide", {"a": 10, "b": 2}),
    ("divide", {"a": 10, "b": 0}),
    ("access_list", {"list": [1, 2, 3], "index": 1}),
    ("access_list", {"list": [1, 2, 3], "index": 5}),
    ("convert", {"value": "123"}),
    ("convert", {"value": "abc"}),
]

for op_name, op_data in test_operations:
    try:
        result = monitored_operation(op_name, op_data)
        print(f"✓ {op_name}: {result}")
    except Exception:
        print(f"✗ {op_name}: Operation failed (check logs)")

print("\n" + "=" * 60)
print("ADVANCED TUTORIAL COMPLETED!")
print("=" * 60)
print("Advanced Concepts Covered:")
print("1. Custom exception classes with additional attributes")
print("2. Exception context managers (__enter__ and __exit__)")
print("3. Exception chaining with 'raise ... from ...'")
print("4. Retry patterns with exponential backoff")
print("5. Exception logging and monitoring")
print("6. Real-world exception handling patterns")