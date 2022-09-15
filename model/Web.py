from datetime import datetime, timedelta
from exceptions import web_exception as we


class Web(object):
    """
        A class with the Web data and the statistics calculation.

        Attributes
        ----------
        _name : str
            Name of the web page
        _interval : int
            Interval for web page monitoring
        _url : str
            Url of the web page
        _status : bool
            Status of the web page. True=Up, False=Down
        _availability : float
            Calculated availability for the last 2 minutes
        _responses : list
            List of responses of the request made

        Methods
        -------
        """

    def __init__(self, **kwargs):
        """Init class

        Parameters
        ----------
        kwargs : dict
            name, interval and url dictionary
        """
        required_keys = {'name', 'interval', 'url'}
        if len(kwargs) == 3 and set(kwargs.keys()) == required_keys:
            self._name = kwargs['name']
            self._interval = int(kwargs['interval'])
            self._url = kwargs['url']
            self._status = False
            self._availability = 0.0
            self._responses = []
        else:
            raise we.WebObjectCreateException()

    @property
    def name(self):
        return self._name

    @property
    def interval(self):
        return self._interval

    @property
    def url(self):
        return self._url

    @property
    def status(self):
        return self._status

    @property
    def availability(self):
        return self._availability

    @property
    def responses(self):
        return self._responses

    def __calculate_availability(self):
        """Calculate percentage of availability for the last 2 minutes
        """
        responses = self.responses_from_time(datetime.now() - timedelta(minutes=2))  # Get responses for last 2 minutes
        not_available = 0
        for response in responses:  # Count not available requests
            if not response['available']:
                not_available += 1

        # Calculate percentage
        self._availability = round((((len(responses) - not_available) / len(responses)) * 100), 2)

    def add_response(self, response):
        """Add response data to the object

        Also calculates availability for the last 2 minutes

        Parameters
        ----------
        response : dict
            Web data response
        """
        self._responses.insert(0, response)
        self.__calculate_availability()

    def set_down(self):
        """Set web as down
        """
        self._status = False

    def set_up(self):
        """Set web as up
        """
        self._status = True

    def responses_from_time(self, from_time):
        """Get newer responses than the time passed

        Parameters
        ----------
        from_time : datetime.datetime
            Responses older time

        Returns
        -------
        responses : list
            Responses list
        """
        responses = []
        for response in self._responses:
            if response['timestamp'] > from_time.timestamp():  # Insert only responses newer than the time
                responses.append(response)
            else:
                # As responses is ordered by newer response, when we arrive to a older response than time we finished
                break

        return responses

    def calculate_stats(self, from_time):
        """Calculate response avg, response codes count and availability from the time passed

        Parameters
        ----------
        from_time : datetime.datetime
            Responses older time

        Returns
        -------
        responses : list
            Responses list
        """

        # Init dictionary where all the data is going to save
        stats = {
            'response_avg': -1,
            'response_codes': {},
            'availability': 0.0
        }

        responses_delimited = self.responses_from_time(from_time)  # Get responses from time
        total_seconds = 0.0
        num_responses = len(responses_delimited)
        not_available = 0
        for response in responses_delimited:  # Iterate all responses
            if response['available']:  # If it's available
                total_seconds += response['response_time']  # Sum all the responses seconds
                status_code = response['status_code']
                if status_code in stats['response_codes']:  # If the status code exist add, if not create
                    stats['response_codes'][status_code] += 1
                else:
                    stats['response_codes'][status_code] = 1
            else:
                not_available += 1  # Variable to know if we can calculate stats

        if (num_responses - not_available) > 0:  # If not_available is greater than num_responses don't calculate stats
            stats['response_avg'] = round(total_seconds / (num_responses - not_available), 4)  # Response average
            stats['availability'] = round(((num_responses - not_available) / num_responses)*100, 2)  # Availability

        return stats
