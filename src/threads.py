from threading import Lock

class SharedData:
    """Class to hold shared data with thread-safe modifications."""
    def __init__(self):
        self.data = []  # Shared list
        self.lock = Lock()  # Lock for thread safety

    def update(self, new_data):
        """Thread-safe method to add data to the list."""
        with self.lock:
            self.data = new_data.copy()
    def get_data(self):
        """Thread-safe method to return a copy of the current list."""
        with self.lock:
            return self.data.copy()