from exceptions import generic_exception as ge


class WebObjectCreateException(ge.Error):
    """Exception raised with a dict without the necessary parameters for the Web Class
    """
    def __init__(self):
        super().__init__('Could not create web object. Dictionary must have name, interval and url')
