import pymongo
import countmDao
import reportDao
import userDao
from bottle import run, app
from beaker.middleware import SessionMiddleware
from bottle import PasteServer
import controller as ctrl



'''
    APP ATTRIBUTES
'''

connection_string = "mongodb://database"
connection = pymongo.MongoClient(connection_string)
database = connection.countm

ctrl.countm_dao = countmDao.CountmDao(database)
ctrl.summary_dao = reportDao.ReportDao(database)
ctrl.user_dao = userDao.UserDao(database)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
_app = SessionMiddleware(app(), session_opts)

run(app=_app, host='127.0.0.1', port=8082, server='gunicorn', workers=3)
