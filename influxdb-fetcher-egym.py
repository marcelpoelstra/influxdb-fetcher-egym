
import yaml
import egym
import influxdb

class InfluxDbFetcherEgym(object):
    def __init__(self):
        self.config = self.loadConfig()

    def loadConfig(self):
        with open("config.yml", 'r') as stream:
            try:
                y = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return y

    def fetchEgymData(self):
        pass

if __name__ == "__main__":
    f = InfluxDbFetcherEgym()
