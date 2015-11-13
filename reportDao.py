

class ReportDao(object):

    def __init__(self, database):
        self.db = database
        self.countm = database.countm

    def payment_summary(self):
        data = {}
        result = self.countm.aggregate([ {'$group': {'_id': {'who': "$who", 'what': "$what"}, 'how_many': {'$sum': "$how_many"} } } ])
        for r in result['result']:
            who = r['_id']['who']
            what = r['_id']['what']
            how_many = r['how_many']

            try:
                data[who]
            except Exception, e:
                data[who] = []
                
            data[who] = data[who] + [(str(how_many) + ' ' + what)]

        print data
        return data
