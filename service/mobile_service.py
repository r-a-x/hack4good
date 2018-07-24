from flask import g
from bson.objectid import ObjectId
from util.util_service import UtilService

class MobileService:
    def __init__(self):
        pass


    @staticmethod
    def getUsers(id):
        return UtilService.documentToJson(g.mongo.user.find_one(({"_id":ObjectId(id)})))


    @staticmethod
    def fetchAllUsersInfo():
        userList = g.mongo.user.find({})
        users = []
        for user in userList:
            users.append(UtilService.documentToJson(user))
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
        return UtilService.documentToJson(questions)

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
    def storeDoctorsVerdict(id, testResult,verdict):
        user = g.mongo.user.find_one({"_id":ObjectId(id)})
        g.mongo.user.update({"_id":ObjectId(id)}, {"$set":{"label":verdict, "testResult":testResult}})
        return UtilService.documentToJson(user)
