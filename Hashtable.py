class Node:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, key: str, value: str):
        new_node = Node(key, value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def find(self, key: str) -> Node:
        current = self.head
        while current:
            if current.key == key:
                return current
            current = current.next
        return None

    def remove(self, key: str):
        node = self.find(key)
        if node is None:
            return
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next 
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev 

    def print_list(self):
        current = self.head
        while current:
            print(f"[{current.key}: {current.value}]", end=" ")
            current = current.next
        print()

class HashTableError(Exception):
    """Custom exception for HashTable errors."""
    pass

class HashTable:
    def __init__(self, initial_capacity: int = 4):
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = 0.75 
        self.shrink_factor = 0.25
        self.table = [DoublyLinkedList() for _ in range(self.capacity)]

    def hash_function(self, key: str) -> int:
        return hash(key) % self.capacity

    def insert(self, key: str, value: str):
        index = self.hash_function(key)
        node = self.table[index].find(key)
        if node:
            node.value = value 
        else:
            self.table[index].insert(key, value)
            self.size += 1
            
            if self.size / self.capacity > self.load_factor:
                self.resize(self.capacity * 2)

    def get(self, key: str) -> str:
        index = self.hash_function(key)
        node = self.table[index].find(key)
        if node:
            return node.value
        raise HashTableError(f"Key '{key}' not found!")

    def remove(self, key: str):
        index = self.hash_function(key)
        if self.table[index].find(key) is None:
            raise HashTableError(f"Key '{key}' not found!")
        self.table[index].remove(key)
        self.size -= 1
        
        if self.capacity > 4 and self.size / self.capacity < self.shrink_factor:
            self.resize(self.capacity // 2)

    def resize(self, new_capacity: int):
        old_table = self.table
        self.capacity = new_capacity
        self.table = [DoublyLinkedList() for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_table:
            current = bucket.head
            while current:
                self.insert(current.key, current.value)
                current = current.next

    def print_table(self):
        print("Current Hash Table:")
        for i in range(self.capacity):
            print(f"Bucket {i}: ", end="")
            self.table[i].print_list()

def main():
    hash_table = HashTable()
    while True:
        print("\nHash Table Operations:")
        print("1. Insert")
        print("2. Get")
        print("3. Remove")
        print("4. Print Hash Table")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            key = input("Enter key to insert: ")
            value = input("Enter value to insert: ")
            try:
                hash_table.insert(key, value)
                print(f"Inserted ({key}, {value})")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            key = input("Enter key to get value: ")
            try:
                value = hash_table.get(key)
                print(f"Value for key '{key}' is '{value}'")
            except HashTableError as e:
                print(e)
        
        elif choice == '3':
            key = input("Enter key to remove: ")
            try:
                hash_table.remove(key)
                print(f"Removed key '{key}'")
            except HashTableError as e:
                print(e)
        
        elif choice == '4':
            hash_table.print_table()
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
