from bottle import route, template, request, redirect, hook, abort


# dao
countm_dao = None
summary_dao = None
user_dao = None


'''
    FILTERS
'''

def auth_filter(fn):
    def check_auth(**kwargs):
        print "auth_filter executed: req. sess: ", request.session

        try:
            logged_username = request.session['logged_username']
        except Exception, e:
            logged_username = None

        if  logged_username == None:
            return template('login')

        return fn(**kwargs)
    return check_auth

def perm_filter(fn):
    def perm_filter(**kwargs):
        print "perm_filter executed: req. sess: ", request.session

        try:
            logged_username = request.session['logged_username']
        except Exception, e:
            logged_username = None

        if  logged_username == None or logged_username == "anonymous":
            abort(401, "you have no permissions for this operation")

        return fn(**kwargs)
    return perm_filter

@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']
    print "request.session: ", request.session


'''
    PAGE CONTROLLERS
'''

@route('/countm', method="GET")
@auth_filter
def index():
    # payment_list = countm_dao.find_all()
    return template('index')

@route('/countm/login', method="POST")
def login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    request.session['logged_username'] = user_dao.getUsername(username, password)
    redirect('/countm')

@route('/countm/logout', method="GET")
def logout():
    request.session['logged_username'] = None
    return template('login')


'''
    REST API CONTROLLER
'''

@route('/countm/rest/api/v1.0/payment', method="GET")
@auth_filter
def payment_getAll():
    return { "payments": countm_dao.find_all() }


@route('/countm/rest/api/v1.0/payment', method="POST")
@auth_filter
@perm_filter
def payment_add():
    d = request.json
    countm_dao.insert(d["when"],d["who"],d["whom"],d["what"],d["how_many"])
    return "true"

@route('/countm/rest/api/v1.0/payment', method="PUT")
@auth_filter
@perm_filter
def payment_add():
    d = request.json
    countm_dao.update(d['id'], d["when"],d["who"],d["whom"],d["what"],d["how_many"])
    return "true"

@route('/countm/rest/api/v1.0/payment/<id>', method="DELETE")
@auth_filter
@perm_filter
def payment_delete(id):
    countm_dao.delete(id)
    return "true"

@route('/countm/rest/api/v1.0/payment/summary', method='GET')
@auth_filter
def payment_summary():
    return { "report": summary_dao.payment_summary() }

