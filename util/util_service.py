from bson.json_util import dumps
from collections import defaultdict
class UtilService:
    def __init__(self):
        pass

    @staticmethod
    def pinCodeParser(path):
        location = defaultdict(lambda :0)
        f = open(path)
        for line in f:
            words = line.split()
            location[words[1]] = (words[-3],words[-2])
        return location

    @staticmethod
    def listHelper(str):
        s = []
        str = str.split(',')
        for e in str:
            s.append(e.replace("[","").replace("]",""))
        return s

    @staticmethod
    def parseList(str):
        if ',' in str:
            return UtilService.listHelper(str)
        return str

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