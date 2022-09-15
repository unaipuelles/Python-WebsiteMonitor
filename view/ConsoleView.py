import logging


class ConsoleView(object):
    """
            A class that prints the data to console prompt

            Attributes
            ----------
            out : LogRecord
                Console output

            Methods
            -------
        """

    def __init__(self):
        # Init new log with console output only
        log = logging.getLogger("View")
        log.setLevel(logging.INFO)
        log.addHandler(logging.StreamHandler())
        log.propagate = False
        self.out = log

    @staticmethod
    def __format_datetime(time):
        """Convert datetime to desired format

        Parameters
        ----------
        time: datetime.datetime
            Datetime to format

        Returns
        -------
        time : str
            Str with date format. Example 16/08/2021 09:52:12
        """
        return time.strftime('%d/%m/%Y %H:%M:%S')

    def show_response(self, web_stats, time_from):
        """Print all webs stats

        Parameters
        ----------
        web_stats : dict
            Stats of all the webs
        time_from : datetime.datetime
            Time from the stats are calculated
        """
        self.out.info("########################")
        self.out.info("#   Web Monitor Stats  #")
        self.out.info("########################")
        self.out.info("Average calculated from {}".format(self.__format_datetime(time_from)))
        for web in web_stats:
            self.out.info("Web: {}".format(web['name']))
            self.out.info("Response time AVG: {}".format(web['stats']['response_avg']))
            self.out.info("Response codes: {}".format(web['stats']['response_codes']))
            self.out.info("Availability: {}%".format(web['stats']['availability']))
            self.out.info("------------------------")

    def web_available(self, web_name, actual_time):
        """Print website available

        Parameters
        ----------
        web_name : str
            Name of the web
        actual_time : datetime.datetime
            Date when the status changed
        """
        self.out.info("[ALERT] Website {} is UP again. Time={}".format(web_name, self.__format_datetime(actual_time)))

    def web_not_available(self, web_name, availability, actual_time):
        """Print website not available

        Parameters
        ----------
        web_name : str
            Name of the web
        availability : float
            Availability of the web
        actual_time : datetime.datetime
            Date when the status changed
        """
        formatted_time = actual_time.strftime('%d/%m/%Y %H:%M:%S')
        message = "[ALERT] Website {} is DOWN. Availability={}, Time={}"
        self.out.info(message.format(web_name, availability, self.__format_datetime(actual_time)))
