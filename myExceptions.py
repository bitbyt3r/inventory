class DuplicateException(Exception): 
    """Exception for duplicate entries""" 
    def __init__(self): 
        pass

class InvalidIDException(Exception): 
    """Exception for invalid ID tags"""
    def __init__(self):
        pass

class CancelledException(Exception): 
    """Exception for when the user cancels an operation""" 
    def __init__(self): 
        pass
