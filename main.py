from flask import Flask, g, request
from flask.json import jsonify
from pymongo import MongoClient
from flask_cors import CORS, cross_origin

app = Flask(__name__)

from service.mobile_service import MobileService
from util.util_service import UtilService
from service.stats_service import StatsService
from collections import defaultdict

mongo = MongoClient("localhost", 27017).rabans
PinCodePath = "./resources/IN.txt"
pincode = defaultdict(lambda: 0)


def required_param(key):
    if not g.json_body:
        raise Exception("Missing request body")

    if key not in g.json_body:
        raise Exception("Missing required parameter '" + key + "'")

    return g.json_body[key]


@app.before_request
def unwind_json():
    g.json_body = request.get_json(force=True, silent=True)


@app.before_request
def init_mongo():
    g.mongo = mongo
    g.pincode,g.pincodeAll = initPinCode()


def initPinCode():
    return UtilService.pinCodeParser(PinCodePath)


@app.route('/signup', methods=['POST'])
@cross_origin(origin='*')

def signup():
    return jsonify(
        MobileService.registerUser(required_param("firstName"), required_param("lastName"), required_param("age"),
                                   required_param("sex"), required_param("pincode"), required_param("college"),
                                   required_param("email"), required_param("password")))


@app.route('/login', methods=['POST'])
@cross_origin(origin='*')
def login():
    return jsonify(MobileService.login(required_param("email"), required_param("password")))


@app.route('/mobile/questions', methods=['GET'])
@cross_origin(origin='*')
def getQuestions():
    return jsonify(MobileService.getQuestions())


@app.route('/mobile/answers', methods=['POST'])
@cross_origin(origin='*')
def postAnswers():
    return jsonify(MobileService.addAnswers(g.json_body))


@app.route('/stats/trending/disease/<pincode>')
@cross_origin(origin='*')
def getTrendingDisease():
    return jsonify(StatsService.getTrendingDisease(pincode))


@app.route('/alerts/<pincode>', methods=['GET'])
@cross_origin(origin='*')
def getAlerts(pincode):
    print pincode
    # return jsonify(StatsService.getAlerts(pincode))


@app.route('/')
@cross_origin(origin='*')
def hello():
    return 'Hello, World!'


@app.route('/users', methods=['GET'])
@cross_origin(origin='*')
def fetchfetchAllUsersInfo():
    return jsonify(MobileService.fetchAllUsersInfo())


@app.route('/web/disease', methods=['POST'])
@cross_origin(origin='*')
def postDisease():
    return jsonify(MobileService.storeDoctorsVerdict(required_param("id"), required_param("testResult"),
                                                     required_param("disease")))


@app.route('/users/<id>', methods=['GET'])
@cross_origin(origin='*')
def getUsers(id):
    return jsonify(MobileService.getUsers(id))

@app.route('/heatmap/<disease>', methods=['GET'])
@cross_origin(origin='*')
def getHeatMap(disease):
    return jsonify(StatsService.getDisease(disease.lower()))


@app.route('/heatmap/random/<disease>', methods=['GET'])
@cross_origin(origin='*')
def getHeatMapRandom(disease):
    return jsonify(StatsService.getDiseaseRandom(disease.lower()))


def generateRandomPatientData():
    disease = ["Thalassemia","Sickle cell Anemia","Diarrhea", "Nipah Virus"]




if __name__ == "__main__":
    print "Hello World !!!"
    print "Hello World"
    app.run(debug=True, host='0.0.0.0')
