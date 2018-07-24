from flask import Flask, g, request
from flask.json import jsonify
from pymongo import MongoClient

app = Flask(__name__)

from service.mobile_service import MobileService
from util.util_service import UtilService
from service.stats_service import StatsService

mongo = MongoClient("localhost", 27017).rabans
PinCodePath = "./resources/IN.txt"
pincode = {}


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


def initPinCode():
    pincode = UtilService.pinCodeParser(PinCodePath)


@app.route('/signup', methods=['POST'])
def signup():
    return jsonify(
        MobileService.registerUser(required_param("firstName"), required_param("lastName"), required_param("age"),
                                   required_param("sex"), required_param("pincode"), required_param("college"),
                                   required_param("email"), required_param("password")))


@app.route('/login', methods=['POST'])
def login():
    return jsonify(MobileService.login(required_param("email"), required_param("password")))


@app.route('/mobile/questions', methods=['GET'])
def getQuestions():
    return jsonify(MobileService.getQuestions())


@app.route('/mobile/answers', methods=['POST'])
def postAnswers():
    return jsonify(MobileService.addAnswers(g.json_body))


@app.route('/stats/trending/disease/<pincode>')
def getTrendingDisease():
    return jsonify(StatsService.getTrendingDisease(pincode))


@app.route('/alerts/<pincode>', methods=['GET'])
def getAlerts(pincode):
    print pincode
    # return jsonify(StatsService.getAlerts(pincode))


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/users', methods=['GET'])
def fetchfetchAllUsersInfo():
    return jsonify(MobileService.fetchAllUsersInfo())


@app.route('/web/disease', methods=['POST'])
def postDisease():
    return jsonify(MobileService.storeDoctorsVerdict(required_param("id"), required_param("testResult"),
                                                     required_param("verdict")))

@app.route('/users/<id>', methods=['GET'])
def getUsers(id):
    return jsonify(MobileService.getUsers(id))

if __name__ == "__main__":
    initPinCode()
    app.run(debug=True, host='0.0.0.0')
