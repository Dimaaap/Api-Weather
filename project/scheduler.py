import schedule

from fetch_weather import FetchWeather


class Scheduler(FetchWeather):

    def scheduler_doing(self):
        schedule.every().minute.do(self.fetch_weather_to_cities)


a = Scheduler()
a.scheduler_doing()
