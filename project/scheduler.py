import schedule


from fetch_weather import FetchWeather


class ScriptRunner:

    @staticmethod
    def start():
        FetchWeather().start()


a = ScriptRunner
schedule.every().minute.do(a.start)
while True:
    schedule.run_pending()


