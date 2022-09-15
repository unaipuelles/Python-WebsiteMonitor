from exceptions import generic_exception as ge


class DefaultConfigError(ge.Error):
    """Exception raised for errors in config file: Default section does not exist
    """
    def __init__(self):
        super().__init__('Default configuration does not exist. This configuration is required.')


class DefaultConfigPathError(ge.Error):
    """Exception raised for errors in config file: Paths are incorrect
    """
    def __init__(self):
        super().__init__('Error with default config paths')
