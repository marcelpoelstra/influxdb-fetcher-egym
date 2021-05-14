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
        for Session in sessions:
            data = api.GetSessionData(Session)
            points = data.getPoints()
            sessiondate = data.getSessionDate()
            exercisedata = data.getExercises()
            for Exercise in exercisedata:
                created = (Exercise.getCreated() * 1000000 )
                exerciseid = Exercise.getExerciseId()
                generalexerciseid = Exercise.getGeneralExerciseId()
                uniqueexerciseclientid = Exercise.getUniqueExerciseClientId()
                exercisetype = Exercise.getExerciseType()
                datasource = Exercise.getDataSource()
                done = Exercise.getDone()
                expoints = Exercise.getExPoints()
                duration = Exercise.getDuration()
                targetspeed = Exercise.getTargetSpeed()
                distance = Exercise.getDistance()
                setsdata = Exercise.getSets()
                if not setsdata:
                    settype = "N/A"
                    numofreps = 0
                    weight = 0.0
                    self.addToInfluxDb(created, generalexerciseid, exercisetype, exerciseid, datasource, done, expoints, uniqueexerciseclientid, duration, targetspeed, distance, settype, numofreps, weight)

                else:
                    for Set in setsdata:
                        settype = Set.getSetType()
                        numofreps = Set.getReps()
                        weight = Set.getWeight()
                        self.addToInfluxDb(created, generalexerciseid, exercisetype, exerciseid, datasource, done, expoints, uniqueexerciseclientid, duration, targetspeed, distance, settype, numofreps, weight)

    def addToInfluxDb(self, created, generalexerciseid, exercisetype, exerciseid, datasource, done, expoints, uniqueexerciseclientid, duration, targetspeed, distance, settype, numofreps, weight):
        json_body = [{
                        "measurement": "egymdata",
                        "time": created,
                        "tags": {
                            "GeneralExerciseID": generalexerciseid,
                            "ExerciseType": exercisetype,
                            "Datasource" : datasource,
                            "Done": done,
                            "SetType": settype,
                            },
                        "fields": {
                            "ExerciseID": exerciseid,
                            "UniqueExerciseClientId": uniqueexerciseclientid,
                            "Exercise Points" : expoints,
                            "Duration" : duration,
                            "Targetspeed" : targetspeed,
                            "Distance" : distance,
                            "NumberOfReps": numofreps,
                            "Weight": weight,
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
