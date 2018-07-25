from flask import g
from util.util_service import UtilService
import random
from collections import defaultdict

class StatsService:

    def __init__(self):
        pass

    @staticmethod
    def getTrendingDisease(pincode=None):
        return ["Your area has higher percentage of the case of Nipah Virus",
                "Please Don't Panic",
                "People in the infected areas must exercise caution and avoid consumption of fruits for a few days until the situation improves",
                "If you feel any type of symptoms. Contact your doctor immediately"]

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

    @staticmethod
    def getNearByLatLong(x,y,delta=10):
        x=float(x)
        y=float(y)
        nearby = []
        for key,value in g.pincode.iteritems():
            x0 = float(value[0])
            y0 = float(value[1])
            if (x-x0)*(x-x0) + (y-y0)*(y-y0) <= delta*delta:
                nearby.append((x0,y0))
        return nearby

    @staticmethod
    def getDiseaseRandom(disease,pincode="124001"):
        results = []
        x,y = g.pincode[pincode]
        nearby = StatsService.getNearByLatLong(x,y)
        for i in range(random.randint(0,1000)):
            result = []
            x,y = UtilService.getRandom(nearby)
            result.append(x)
            result.append(y)
            result.append(random.randint(10,1000))
            results.append(result)
        return results