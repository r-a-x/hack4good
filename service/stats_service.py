from flask import g
from util.util_service import UtilService

from collections import defaultdict

class StatsService:

    def __init__(self):
        pass

    @staticmethod
    def getTrendingDisease(pincode):
    #   Find all the users from the database and use it to search the result
        pass


    @staticmethod
    def convertDictionaryToListsList(pinCode):
        results = []
        for key,value in pinCode.iteritems():
            result = []
            result.append( g.pincode[key][0])
            result.append(g.pincode[key][1])
            result.append(value)
            results.append(result)
        return results

    @staticmethod
    def getDisease(disease):
        users = g.mongo.user.find()
        pincodeCount = defaultdict(lambda: 0)
        for user in users:
            user = UtilService.documentToJson(user)
            if "disease" in user and disease in user["disease"].lower():
                pincodeCount[user["pincode"]] = pincodeCount[user["pincode"]] + 1
        return StatsService.convertDictionaryToListsList(pincodeCount)

    @staticmethod
    def getDiseaseCount():
        results = []
        users = g.mongo.user.find()
        countOnPincode = defaultdict(lambda: 0)

        for user in users:
            data = UtilService.documentToJson(user)
            pincode = data["pincode"]
            countOnPincode[pincode] = countOnPincode[pincode] + 1

        for key,value in countOnPincode.iteritems():
            result = []
            lat,long = g.pincode[key][0],g.pincode[key][1]
            result.append( lat )
            result.append( long )
            result.append(value)

        return results

    @staticmethod
    def getPrecaution(disease):
        pass

    @staticmethod
    def getAlerts(pincode):
        pass
