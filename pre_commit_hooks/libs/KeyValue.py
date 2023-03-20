class KeyValue:
    """ Key-Value structure for error details, etc. """
    key: str
    message: str

    def __init__(self, key: str, message: str):
        self.key = key
        self.message = message
