from bson import ObjectId

class CountmDao(object):

    def __init__(self, database):
        self.db = database
        self.countm = database.countm

    def find_all(self):
        data = []
        for row in self.countm.find():
            data.append({'id': str(row['_id']), 'when': row['when'], 'who': row['who'], 'whom': row['whom'], 'what': row['what'], 'how_many': row['how_many']})
        return data

    def insert(self, when, who, whom, what, how_many):
        data = { 'when':when, 'who':who, 'whom':whom, 'what':what.upper(), 'how_many':how_many }
        self.countm.insert(self.format_data(data))

    def update(self, id, when, who, whom, what, how_many):
        data = { '_id': ObjectId(id), 'when':when, 'who':who, 'whom':whom, 'what':what.upper(), 'how_many':how_many }        
        self.countm.save(self.format_data(data))

    def delete(self, id):
        data = { '_id': ObjectId(id)}
        try:
            self.countm.remove(data)
        except Exception, e:
            print e

    def format_data(self, data):
        if data == None:
            return

        data['when'] = data['when'] if data['when'] else '01/01/1970'
        data['who'] = str(data['who']).lower().strip() if data['who'] else 'undefined'
        data['whom'] = str(data['whom']).lower().strip() if data['whom'] else 'undefined'
        data['what'] = str(data['what']).upper().strip() if data['what'] else 'USD'

        how_many = data['how_many']
        data['how_many'] = int(how_many) if str(how_many).isdigit() else 0 if how_many else 0

        return data
