"""
LINKED LISTS IN DATA STRUCTURES - COMPLETE GUIDE
=================================================
"""

# ============================================
# 1. NODE CLASS DEFINITION
# ============================================


class Node:
    """Single node in a linked list"""

    def __init__(self, data):
        self.data = data  # Store data
        self.next = None  # Reference to next node

    def __repr__(self):
        return f"Node({self.data})"


# ============================================
# 2. SINGLY LINKED LIST CLASS
# ============================================


class SinglyLinkedList:
    """Implementation of Singly Linked List"""

    def __init__(self):
        self.head = None  # First node
        self.size = 0  # Track size

    def is_empty(self):
        """Check if list is empty - O(1)"""
        return self.head is None

    def get_size(self):
        """Get size of list - O(1)"""
        return self.size

    # ============================================
    # INSERTION OPERATIONS
    # ============================================

    def insert_at_beginning(self, data):
        """Insert at beginning - O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        print(f"Inserted {data} at beginning")

    def insert_at_end(self, data):
        """Insert at end - O(n)"""
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:  # Traverse to last node
                current = current.next
            current.next = new_node

        self.size += 1
        print(f"Inserted {data} at end")

    def insert_at_position(self, data, position):
        """Insert at specific position - O(n)"""
        if position < 0 or position > self.size:
            print(f"Invalid position {position}")
            return

        if position == 0:
            self.insert_at_beginning(data)
            return

        new_node = Node(data)
        current = self.head

        # Traverse to position-1
        for i in range(position - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.size += 1
        print(f"Inserted {data} at position {position}")

    def insert_after_value(self, data, after_value):
        """Insert after a specific value - O(n)"""
        current = self.head

        while current:
            if current.data == after_value:
                new_node = Node(data)
                new_node.next = current.next
                current.next = new_node
                self.size += 1
                print(f"Inserted {data} after {after_value}")
                return
            current = current.next

        print(f"Value {after_value} not found")

    # ============================================
    # DELETION OPERATIONS
    # ============================================

    def delete_at_beginning(self):
        """Delete first node - O(1)"""
        if self.is_empty():
            print("List is empty")
            return None

        deleted_data = self.head.data
        self.head = self.head.next
        self.size -= 1
        print(f"Deleted {deleted_data} from beginning")
        return deleted_data

    def delete_at_end(self):
        """Delete last node - O(n)"""
        if self.is_empty():
            print("List is empty")
            return None

        if self.head.next is None:  # Only one node
            deleted_data = self.head.data
            self.head = None
            self.size -= 1
            print(f"Deleted {deleted_data} from end")
            return deleted_data

        current = self.head
        while current.next.next:  # Go to second-last node
            current = current.next

        deleted_data = current.next.data
        current.next = None
        self.size -= 1
        print(f"Deleted {deleted_data} from end")
        return deleted_data

    def delete_at_position(self, position):
        """Delete at specific position - O(n)"""
        if position < 0 or position >= self.size:
            print(f"Invalid position {position}")
            return None

        if position == 0:
            return self.delete_at_beginning()

        current = self.head
        for i in range(position - 1):
            current = current.next

        deleted_data = current.next.data
        current.next = current.next.next
        self.size -= 1
        print(f"Deleted {deleted_data} from position {position}")
        return deleted_data

    def delete_by_value(self, value):
        """Delete first occurrence of value - O(n)"""
        if self.is_empty():
            print("List is empty")
            return False

        # If head node contains the value
        if self.head.data == value:
            self.head = self.head.next
            self.size -= 1
            print(f"Deleted {value}")
            return True

        current = self.head
        while current.next:
            if current.next.data == value:
                current.next = current.next.next
                self.size -= 1
                print(f"Deleted {value}")
                return True
            current = current.next

        print(f"Value {value} not found")
        return False

    # ============================================
    # SEARCH OPERATIONS
    # ============================================

    def search(self, value):
        """Search for a value - O(n)"""
        current = self.head
        position = 0

        while current:
            if current.data == value:
                print(f"Found {value} at position {position}")
                return position
            current = current.next
            position += 1

        print(f"Value {value} not found")
        return -1

    def contains(self, value):
        """Check if value exists - O(n)"""
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False

    # ============================================
    # ACCESS OPERATIONS
    # ============================================

    def get_at_position(self, position):
        """Get value at position - O(n)"""
        if position < 0 or position >= self.size:
            print(f"Invalid position {position}")
            return None

        current = self.head
        for i in range(position):
            current = current.next

        return current.data

    def get_first(self):
        """Get first element - O(1)"""
        return self.head.data if self.head else None

    def get_last(self):
        """Get last element - O(n)"""
        if self.is_empty():
            return None

        current = self.head
        while current.next:
            current = current.next
        return current.data

    # ============================================
    # TRAVERSAL OPERATIONS
    # ============================================

    def display(self):
        """Display entire list - O(n)"""
        if self.is_empty():
            print("List is empty")
            return

        current = self.head
        elements = []

        while current:
            elements.append(str(current.data))
            current = current.next

        print(" -> ".join(elements) + " -> NULL")

    def display_detailed(self):
        """Display with positions - O(n)"""
        if self.is_empty():
            print("List is empty")
            return

        current = self.head
        position = 0

        print("Position | Data | Next")
        print("---------|------|-----")

        while current:
            next_data = current.next.data if current.next else "NULL"
            print(f"   {position:2d}    | {current.data:4d} | {next_data}")
            current = current.next
            position += 1

    def to_list(self):
        """Convert to Python list - O(n)"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    # ============================================
    # UTILITY OPERATIONS
    # ============================================

    def reverse(self):
        """Reverse the linked list - O(n)"""
        prev = None
        current = self.head

        while current:
            next_node = current.next  # Store next
            current.next = prev  # Reverse link
            prev = current  # Move prev forward
            current = next_node  # Move current forward

        self.head = prev
        print("List reversed")

    def find_middle(self):
        """Find middle element using slow-fast pointer - O(n)"""
        if self.is_empty():
            return None

        slow = fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow.data

    def detect_loop(self):
        """Detect if list has a loop - O(n)"""
        slow = fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False

    def remove_duplicates(self):
        """Remove duplicates from sorted list - O(n)"""
        if self.is_empty():
            return

        current = self.head

        while current and current.next:
            if current.data == current.next.data:
                current.next = current.next.next
                self.size -= 1
            else:
                current = current.next

        print("Duplicates removed")

    def clear(self):
        """Clear entire list - O(1)"""
        self.head = None
        self.size = 0
        print("List cleared")


# ============================================
# 3. DOUBLY LINKED LIST
# ============================================


class DoublyNode:
    """Node for doubly linked list"""

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """Implementation of Doubly Linked List"""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def insert_at_beginning(self, data):
        """Insert at beginning - O(1)"""
        new_node = DoublyNode(data)

        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1
        print(f"Inserted {data} at beginning")

    def insert_at_end(self, data):
        """Insert at end - O(1) with tail pointer"""
        new_node = DoublyNode(data)

        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1
        print(f"Inserted {data} at end")

    def delete_at_beginning(self):
        """Delete at beginning - O(1)"""
        if self.is_empty():
            print("List is empty")
            return None

        deleted_data = self.head.data

        if self.head == self.tail:  # Only one node
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

        self.size -= 1
        print(f"Deleted {deleted_data} from beginning")
        return deleted_data

    def delete_at_end(self):
        """Delete at end - O(1) with tail pointer"""
        if self.is_empty():
            print("List is empty")
            return None

        deleted_data = self.tail.data

        if self.head == self.tail:  # Only one node
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

        self.size -= 1
        print(f"Deleted {deleted_data} from end")
        return deleted_data

    def display_forward(self):
        """Display list forward - O(n)"""
        if self.is_empty():
            print("List is empty")
            return

        current = self.head
        elements = []

        while current:
            elements.append(str(current.data))
            current = current.next

        print("Forward: NULL <- " + " <-> ".join(elements) + " -> NULL")

    def display_backward(self):
        """Display list backward - O(n)"""
        if self.is_empty():
            print("List is empty")
            return

        current = self.tail
        elements = []

        while current:
            elements.append(str(current.data))
            current = current.prev

        print("Backward: NULL <- " + " <-> ".join(elements) + " -> NULL")


# ============================================
# 4. CIRCULAR LINKED LIST
# ============================================


class CircularLinkedList:
    """Implementation of Circular Linked List"""

    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def insert_at_beginning(self, data):
        """Insert at beginning - O(n) to find last node"""
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
            new_node.next = new_node  # Point to itself
        else:
            # Find last node
            current = self.head
            while current.next != self.head:
                current = current.next

            new_node.next = self.head
            current.next = new_node
            self.head = new_node

        self.size += 1
        print(f"Inserted {data} at beginning")

    def display(self):
        """Display circular list - O(n)"""
        if self.is_empty():
            print("List is empty")
            return

        current = self.head
        elements = []

        while True:
            elements.append(str(current.data))
            current = current.next
            if current == self.head:
                break

        print(" -> ".join(elements) + f" -> {self.head.data} (circular)")


# ============================================
# DEMONSTRATION AND EXAMPLES
# ============================================


def demonstrate_singly_linked_list():
    print("\n" + "=" * 60)
    print("SINGLY LINKED LIST DEMONSTRATION")
    print("=" * 60)

    ll = SinglyLinkedList()

    print("\n--- Insertion Operations ---")
    ll.insert_at_end(10)
    ll.insert_at_end(20)
    ll.insert_at_end(30)
    ll.display()

    ll.insert_at_beginning(5)
    ll.display()

    ll.insert_at_position(15, 2)
    ll.display()

    ll.insert_after_value(25, 20)
    ll.display()

    print("\n--- Detailed View ---")
    ll.display_detailed()

    print(f"\nSize: {ll.get_size()}")
    print(f"First element: {ll.get_first()}")
    print(f"Last element: {ll.get_last()}")
    print(f"Element at position 3: {ll.get_at_position(3)}")

    print("\n--- Search Operations ---")
    ll.search(20)
    ll.search(100)
    print(f"Contains 15: {ll.contains(15)}")
    print(f"Contains 99: {ll.contains(99)}")

    print("\n--- Middle Element ---")
    print(f"Middle element: {ll.find_middle()}")

    print("\n--- Deletion Operations ---")
    ll.delete_at_beginning()
    ll.display()

    ll.delete_at_end()
    ll.display()

    ll.delete_at_position(1)
    ll.display()

    ll.delete_by_value(20)
    ll.display()

    print("\n--- Reverse Operation ---")
    ll.reverse()
    ll.display()


def demonstrate_doubly_linked_list():
    print("\n" + "=" * 60)
    print("DOUBLY LINKED LIST DEMONSTRATION")
    print("=" * 60)

    dll = DoublyLinkedList()

    print("\n--- Insertion Operations ---")
    dll.insert_at_end(10)
    dll.insert_at_end(20)
    dll.insert_at_end(30)
    dll.insert_at_beginning(5)

    dll.display_forward()
    dll.display_backward()

    print("\n--- Deletion Operations ---")
    dll.delete_at_beginning()
    dll.display_forward()

    dll.delete_at_end()
    dll.display_forward()


def demonstrate_circular_linked_list():
    print("\n" + "=" * 60)
    print("CIRCULAR LINKED LIST DEMONSTRATION")
    print("=" * 60)

    cll = CircularLinkedList()

    cll.insert_at_beginning(30)
    cll.insert_at_beginning(20)
    cll.insert_at_beginning(10)

    cll.display()


def practical_examples():
    print("\n" + "=" * 60)
    print("PRACTICAL EXAMPLES")
    print("=" * 60)

    # Example 1: Remove duplicates from sorted list
    print("\n--- Remove Duplicates ---")
    ll = SinglyLinkedList()
    for val in [10, 10, 20, 20, 20, 30, 40, 40]:
        ll.insert_at_end(val)

    print("Before:")
    ll.display()

    ll.remove_duplicates()
    print("After:")
    ll.display()

    # Example 2: Detect loop
    print("\n--- Loop Detection ---")
    ll2 = SinglyLinkedList()
    for val in [1, 2, 3, 4, 5]:
        ll2.insert_at_end(val)

    print(f"Has loop: {ll2.detect_loop()}")


def print_complexity_table():
    print("\n" + "=" * 60)
    print("TIME COMPLEXITY COMPARISON")
    print("=" * 60)

    print(
        """
Operation              | Array  | Singly LL | Doubly LL
-----------------------|--------|-----------|----------
Access by index        | O(1)   | O(n)      | O(n)
Search                 | O(n)   | O(n)      | O(n)
Insert at beginning    | O(n)   | O(1)      | O(1)
Insert at end          | O(1)*  | O(n)      | O(1)**
Insert at middle       | O(n)   | O(n)      | O(n)
Delete at beginning    | O(n)   | O(1)      | O(1)
Delete at end          | O(1)   | O(n)      | O(1)**
Delete at middle       | O(n)   | O(n)      | O(n)

*  Amortized (dynamic array)
** With tail pointer
    """
    )


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("LINKED LISTS - COMPLETE TUTORIAL")
    print("=" * 60)

    demonstrate_singly_linked_list()
    demonstrate_doubly_linked_list()
    demonstrate_circular_linked_list()
    practical_examples()
    print_complexity_table()

    print("\n" + "=" * 60)
    print("TUTORIAL COMPLETE!")
    print("=" * 60)
