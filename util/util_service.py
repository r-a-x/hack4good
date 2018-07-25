from bson.json_util import dumps
from flask import g
from collections import defaultdict
import random

class UtilService:
    def __init__(self):
        pass

    @staticmethod
    def pinCodeParser(path):
        location = defaultdict(lambda: 0)
        locationAll = defaultdict(lambda: [])
        f = open(path)
        for line in f:
            words = line.split()
            location[words[1]] = (words[-3],words[-2])
            locationAll[words[1]].append((words[-3],words[-2]))
        return location,locationAll

    @staticmethod
    def listHelper(str):
        s = []
        str = str.split(',')
        for e in str:
            s.append(e.replace("[","").replace("]",""))
        return s

    @staticmethod
    def parseList(input):
        if type(input) != type("rahul"):
            return input
        if ',' in input:
            return UtilService.listHelper(input)
        return input

    @staticmethod
    def trimStr(str):
        return str.replace('"','')

    @staticmethod
    def documentToJson(document):
        document = eval(dumps(document))
        mp = {}
        for key, value in document.iteritems():
            if "_id" in key:
                mp["id"] = str(value["$oid"])
            else:
                mp[ UtilService.trimStr(key) ] = UtilService.parseList( value )
        return mp

    @staticmethod
    def convertDocumentsToJson(documents):
        result = []
        for document in documents:
            result.append(UtilService.documentToJson(document))
        return result


    @staticmethod
    def isNumber(string):
        return any(char.isdigit() for char in string)

    @staticmethod
    def generateEmail(firstName,lastName):
        return firstName.lower() + lastName.lower() + "@outlook.com"

    @staticmethod
    def generateLatitudeLongitude():
        return [(213.22, 4322.90)]

    @staticmethod
    def getDisease():
        return ["Thalassemia", "Sickle cell Anemia", "Diarrhea", "Nipah Virus", "Nipah Virus"]

    @staticmethod
    def getRandom(list):
        return list[random.randint(0,len(list)-1)]

    @staticmethod
    def generateUserHelper(firstName, lastName, sex, college, email, disease):
        user = {"firstName": firstName, "lastName": lastName, "age": 23, "sex": sex, "pincode": 124001,
                "college": college, "email": email, "password": firstName.lower(),
                "disease": disease}
        return user


    @staticmethod
    def generateUser(boys,girls,surnames,colleges,diseases):
        firstName,sex=None,None
        gender = random.randint(0,1)
        if gender == 0:
            firstName = UtilService.getRandom(boys)
            sex = "male"
        else:
            firstName = UtilService.getRandom(girls)
            sex = "female"
        lastName = UtilService.getRandom(surnames)
        email = UtilService.generateEmail(firstName, lastName)
        college = UtilService.getRandom(colleges)
        disease = UtilService.getRandom(diseases)
        user = UtilService.generateUserHelper(firstName,lastName,sex,college,email,disease)
        return user




    @staticmethod
    # def generateData(count,latitudeLongitude,diseases,colleges,boys,girls,surnames):
    def generateData(path,count):
        diseases = ["Thalassemia", "Sickle cell Anemia", "Diarrhea", "Nipah Virus", "Nipah Virus"]
        colleges = ["NIT-Allahabad","NIT-Bhopal","Bits Pilani","Vaish College","IP University","Lovely Professional"]
        boys, girls = UtilService.parseNames(path + "names.txt")
        surnames = UtilService.parseSurNames(path + "surnames.txt")

        users = []
        for i in range(count):
            users.append(UtilService.generateUser(boys, girls, surnames, colleges, diseases))
        g.mongo.user.insert(users)
        return users


    @staticmethod
    def parseSurNames(path):
        surnames = []
        f = open(path)
        for surname in f:
            surnames.append(surname.strip())
        return surnames

    @staticmethod
    def parseNames(path):
        boys = []
        girls = []
        f = open(path)
        for line in f:
            if not UtilService.isNumber(line):
                if len(boys) < len(girls):
                    boys.append(line.strip())
                else:
                    girls.append(line.strip())
        return boys,girls

    @staticmethod
    def populateDatabase(path):
        return UtilService.generateData(path,100)

# if __name__ == "__main__":
#     # print UtilService.parseNames("../resources/names.txt")
#     # print UtilService.parseSurNames("../resources/surnames.txt")
#     users = UtilService.generateData(12)
#     for user in users:
#         print user
