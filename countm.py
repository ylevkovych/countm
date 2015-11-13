import pymongo
import countmDao
import reportDao
from bottle import route, run, template, request, redirect


@route('/countm', method="GET")
def index():
    payment_list = countm_dao.find_all()
    return template('index')

@route('/countm/payment', method="GET")
def payment_getAll():
    print "GET ALL"
    return { "payments": countm_dao.find_all() }


@route('/countm/payment', method="POST")
def payment_add():
    print "ADD PAYMENT: ", request.json
    d = request.json
    countm_dao.insert(d["when"],d["who"],d["whom"],d["what"],d["how_many"])
    return "true"

@route('/countm/payment', method="PUT")
def payment_add():
    print "UPDATE PAYMENT: ", request.json
    d = request.json
    countm_dao.update(d['id'], d["when"],d["who"],d["whom"],d["what"],d["how_many"])
    return "true"

@route('/countm/payment/<id>', method="DELETE")
def payment_delete(id):
    print "DELETE PAYMENT: ", id
    countm_dao.delete(id)
    return "true"

@route('/countm/payment/summary', method='GET')
def payment_summary():
    print "GET SUMMARY"
    return { "report": summary_dao.payment_summary() }

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.countm

countm_dao = countmDao.CountmDao(database)
summary_dao = reportDao.ReportDao(database)

run(host='localhost', port=8082)