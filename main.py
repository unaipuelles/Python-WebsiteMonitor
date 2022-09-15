from configparser import ConfigParser, ExtendedInterpolation
import os
import logging

from controller import Controller
from model import Web as web
from view import ConsoleView as view
from exceptions import config_exceptions


def validate_conf(conf):
    """Validates the config file of the app

    Validates also the paths that are set

    Parameters
    ----------
    conf : ConfigParser
        Configuration file loaded

    Raises
    ------
    DefaultConfigPathError
        If the paths does not exist
    DefaultConfigError
        If the default configuration does not exist
    """
    if 'default' in conf.sections() and 'log' in conf.sections():
        # Validate paths
        if not (os.path.exists(conf['default']['home_dir']) & os.path.exists(conf['log']['log_dir'])):
            raise config_exceptions.DefaultConfigPathError()
    else:
        raise config_exceptions.DefaultConfigError()


def conf_to_dict(conf):
    """Transforms configParser into a dict with all the configurations

    Parameters
    ----------
    conf : ConfigParser

    Returns
    -------
    conf_dict : dict
        Dict with all the configurations
    """
    conf_dict = {}
    for section in conf.sections():  # Iterate all sections
        if section == 'default' or section == 'log':
            # Save normal sections
            conf_dict[section] = dict(conf[section])
        else:
            if not ('webs' in conf_dict):  # Verify if webs key exist
                conf_dict['webs'] = {}  # Init webs kwy
            conf_dict['webs'][section] = dict(conf[section])  # Save web data

    return conf_dict


def log_init(log_config):
    """Init root logger with file and console output

    Parameters
    ----------
    log_config : dict
        Data with the log options

    Returns
    -------
    root_logger : LogRecord
        Root logger
    """
    # Generate formats
    log_file_formatter = logging.Formatter(log_config['log_file_format'])
    log_console_formatter = logging.Formatter(log_config['log_console_format'])

    # Set logging level
    logging.basicConfig(level=int(log_config['logging_level']))

    # Get logger
    root_logger = logging.getLogger("Monitor")
    root_logger.propagate = False

    # Add file handler
    file_handler = logging.FileHandler("{0}/{1}.log".format(log_config['log_dir'], log_config['log_file_name']))
    file_handler.setFormatter(log_file_formatter)
    root_logger.addHandler(file_handler)

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_console_formatter)
    root_logger.addHandler(console_handler)

    return root_logger


if __name__ == '__main__':
    # Load app configuration file
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read("config/app.ini")

    # Validate configuration
    validate_conf(config)

    # Transform into a dict for the controller
    conf_data = conf_to_dict(config)

    # Init logger
    log = log_init(conf_data['log'])

    # Init controller
    c = Controller.Controller(web.Web, view.ConsoleView, conf_data['webs'])

    # Lock the program until user request to finish
    input_str = ""
    while input_str != "exit":
        input_str = input()

    log.info("End of program")
