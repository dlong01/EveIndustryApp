class Formatter:
    def __init__(self):
        self.level = 0

    def __enter__(self):
        # Code to execute when entering the context
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Code to execute when exiting the context
        pass

    def increase_indent(self):
        self.level += 1
    
    def decrease_indent(self):
        if self.level > 0:
            self.level -= 1

    def print(self, text):
        print('\t' * self.level + text)
