import logging


class Error(Exception):
    """Base class for exceptions in this module.

    Parameters
    ----------
    message : str
        Message that will output the exception
    """
    def __init__(self, message):
        self.message = message
        self.print_message()

    def print_message(self):
        logging.getLogger("Monitor").error(self.message)
