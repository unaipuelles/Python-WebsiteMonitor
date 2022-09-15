from threading import Thread
import logging
import time
import datetime

from classes import WebChecker as wc


class Controller(object):
    """
    A class that controls the model and the view

    Also has all the logic of the web monitor running

    Attributes
    ----------
    model : Object
        object of the model that we will use
    view : str
        object of the view that we will use
    webs : list
        a list of all the Web objects that we will use to monitor
    log : LogRecord
        log object
    start_time : Time
        variable that we will use to know the start time to show the stats in the output

    """

    def __init__(self, model, view, webs_data):
        """
        Parameters
        ----------
        model : Object
            Model that we will use
        view : Object
            object of the view that we will use
        webs_data : dict
            All the data of the webs
        """
        self.model = model
        self.view = view()
        self.__init_web_objects(webs_data)  # Set all the parameters to the object
        self.log = logging.getLogger("Monitor")
        self.start_time = time.time()
        self.__start_web_monitoring()
        self.__start_stats_monitor()
        self.__start_downtime_check()

    def __init_web_objects(self, webs_data):
        """Creates model objects and saves them in the list of webs

        Parameters
        ----------
        webs_data : dict
            All the data of the webs
        """
        self.webs = []
        for web_name in webs_data.keys():
            self.webs.append(self.model(**webs_data[web_name]))

    def __show_stats(self, start_time):
        """Infinite loop to show stats of the webs

        Shows 9 times 10 minutes stats and the 10th time the las 60 minutes

        Parameters
        ----------
        start_time : float
            Used to know the start time
        """
        count = 1
        while True:  # Infinite loop
            time.sleep(10.0 - ((time.time() - start_time) % 10.0))  # Wait 10 seconds

            if count == 10:  # See if it's the 10th time we execute
                # Set 60 minutes history
                count = 1
                interval_minutes = 60
            else:
                # Set 10 minutes history
                interval_minutes = 10

            # Calculate the time from we need to get the responses
            time_from = datetime.datetime.now() - datetime.timedelta(minutes=interval_minutes)
            # Show stats for each web
            self.__show_web_stats(time_from)

            count += 1

    def __check_downtimes(self):
        """Infinite loop that check the availability of the webs and shows alerts
        """
        while True:
            time.sleep(1)  # Run each second
            for web in self.webs:  # Loop all the webs
                if web.availability != 0.0:  # Avoid calculating for the webs that the availability is 0
                    if web.availability > 80 and not web.status:
                        # Web was down and now is available again
                        self.view.web_available(web.name, datetime.datetime.now())
                        web.set_up()
                    elif web.availability < 80 and web.status:
                        # Web was up and now is down
                        self.view.web_not_available(web.name, web.availability, datetime.datetime.now())
                        web.set_down()

    def __monitor_web(self, web):
        """Inifnite loop thath checks the response of the web in the interval set and saves it

        Parameters
        ----------
        web : Object
            Web object that will be monitored
        """
        while True:
            time.sleep(web.interval)  # Do the requests with the interval set for the Web
            response_data = wc.WebChecker().site_status(web.url)  # Do the request
            web.add_response(response_data)  # Add response data
            self.log.debug("Added response data for {}".format(web.name))

    def __start_web_monitoring(self):
        """Starts threads to monitor each web
        """
        for web in self.webs:  # Loop all the webs
            # Create and start the thread
            web_monitor_thread = Thread(target=self.__monitor_web, args=(web,), daemon=True)
            web_monitor_thread.start()
            self.log.info("Started monitoring for {}".format(web.name))

    def __start_downtime_check(self):
        """Starts web downtime check thread
        """
        downtime_thread = Thread(target=self.__check_downtimes, daemon=True)
        downtime_thread.start()

    def __start_stats_monitor(self):
        """Starts the thread for showing the stats
        """
        stats_thread = Thread(target=self.__show_stats, args=(time.time(),), daemon=True)
        stats_thread.start()

    def __show_web_stats(self, time_from):
        """Calculates the stats of each website and calls to the view to print them

        Parameters
        ----------
        time_from : datetime.datetime
        """
        all_stats = []
        for web in self.webs:  # Loop all the webs
            self.log.debug("Calculating stats for {}".format(web.name))
            web_stats = web.calculate_stats(time_from)  # Calculate stats
            # Append stats to the list for the view
            all_stats.append({
                'name': web.name,
                'stats': web_stats,
                'status': web.status
            })

        # Call the view
        self.view.show_response(all_stats, time_from)
