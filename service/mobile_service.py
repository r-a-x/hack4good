from flask import g
from bson.json_util import dumps

def listHelper(str):
    s = []
    str = str.split(',')
    for e in str:
        s.append(e.replace("[","").replace("]",""))
    return s

def parseList(str):
    if ',' in str:
        return listHelper(str)
    return str

def trimStr(str):
    return str.replace('"','')


def documentToJson(document):
    document = eval(dumps(document))
    mp = {}
    for key, value in document.iteritems():
        if "_id" in key:
            mp["id"] = str(value["$oid"])
        else:
            mp[ trimStr(key) ] = parseList( value )
    return mp

class MobileService:
    def __init__(self):
        pass

    @staticmethod
    def fetchAllUsersInfo():
        userList = g.mongo.user.find({})
        users = []
        for user in userList:
            users.append(documentToJson(user))
        return users

    @staticmethod
    def login(email, password):
        user = g.mongo.user.find({"email":email,"password":password})
        # user["id"]  = user._id.inserted_id
        if user is None:
            return {}
        return user

    @staticmethod
    def registerUser(firstName, lastName, age, sex, pincode, college, email, password):
        user = {"firstName":firstName,"lastName":lastName, "age":age, "sex":sex, "pincode":pincode, "college":college, "email":email, "password":password}
        user_id = g.mongo.user.insert_one(user)
        user["id"] = str(user_id.inserted_id)
        del user["_id"]
        return user

    @staticmethod
    def getQuestions():
        questions = g.mongo.questions.find_one()
        return documentToJson(questions)

    @staticmethod
    def postQuestions(questions):
        inserted_questions = []
        for question in questions:
            question_id = g.mongo.questions.insert_one(question)
            del question["_id"]
            question["id"] = str(question_id.inserted_id)
            inserted_questions.append(question)
        return inserted_questions

    @staticmethod
    def storeDoctorsVerdict(id,firstName, lastName):
        user = g.mongo.user.find({"firstName":firstName, "lastName":lastName})
        #adding additional field in the existing table
        g.mongo.user.update({"firstName":firstName}, {"lastName":lastName},{"$set":{"label":verdict}})
        return 1
