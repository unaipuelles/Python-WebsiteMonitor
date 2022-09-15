import requests
import datetime


class WebChecker(object):
    """
    A class that get the response from the url.

    Methods
    -------
    """

    @staticmethod
    def site_status(url):
        """Retrieve web response

        Parameters
        ----------
        url : str
            Url for doing the request

        Returns
        -------
        extracted_data : dict
            Availability, status code, response time and actual time
        """
        try:
            web_response = requests.get(url, timeout=1)
            extracted_data = WebChecker.__transform_response(web_response)
        except (requests.ConnectionError, requests.Timeout):
            extracted_data = WebChecker.__site_down_response()

        return extracted_data

    @staticmethod
    def __transform_response(response):
        """Transform url response data

        Parameters
        ----------
        response : request
            Url request result

        Returns
        -------
        extracted_data : dict
            Availability, status code, response time and actual time
        """
        available = True
        if response.status_code != 200:  # Available is set to false if the response code is not 200
            available = False

        return {
            'available': available,
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds(),
            'timestamp': datetime.datetime.now().timestamp()
        }

    @staticmethod
    def __site_down_response():
        """Url without response data

        Returns
        -------
        extracted_data : dict
            Availability = False and actual time
        """
        return {
            'available': False,
            'timestamp': datetime.datetime.now().timestamp()
        }
