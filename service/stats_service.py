from flask import g
class StatsService:

    def __init__(self):
        pass

    @staticmethod
    def getTrendingDisease(pincode):
    #   Find all the users from the database and use it to search the result
        pass

    @staticmethod
    def getDiseaseCount():
        results = []
        users = g.mongo.user.find()
        for user in users:
            results.append(d)
        return results
    @staticmethod
    def getPrecaution(disease):
        pass

    @staticmethod
    def getAlerts(pincode):
        pass
