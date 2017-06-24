#!/usr/bin/env python

import yaml
import egym
from influxdb import InfluxDBClient
from datetime import date
from datetime import timedelta

class InfluxDbFetcherEgym(object):
    def __init__(self):
        self.config = self.loadConfig()
        self.fetchEgymData()

    def loadConfig(self):
        with open("config.yml", 'r') as stream:
            try:
                y = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return y

    def fetchEgymData(self):
        api = egym.Api(email=self.config['egym_email'],
                      password=self.config['egym_password'])
        sessions = api.GetUserSessions(date.today() - timedelta(days=7), date.today())
        for session in sessions:
            data = api.GetSessionData(session)
            points = data.getPoints()
            isodate = data.getIsoDate()
            self.addToInfluxDb(isodate, points)

    def addToInfluxDb(self, isodate, points):
        json_body = [{
                        "measurement": "egym",
                        "time": isodate,
                        "fields": {
                            "value": points
                            }
                    }]
        client = InfluxDBClient(self.config['influx_host'], 
                                self.config['influx_port'], 
                                self.config['influx_user'],
                                self.config['influx_password'],
                                self.config['influx_db'],
                                )
        client.write_points(json_body)

if __name__ == "__main__":
    f = InfluxDbFetcherEgym()
