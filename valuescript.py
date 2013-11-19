import csv, codecs, cStringIO
import json
import urllib2

group_id = 207305762667302
limit = 500
access_token = ''

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

with open('valuedata.csv', 'wb') as outfile:
    json_data = urllib2.urlopen('https://graph.facebook.com/' + str(group_id) +'/feed?limit=' + str(limit) + '&access_token=' + access_token)
    data = json.load(json_data)
    json_data.close()

    messages = []
    
    for post in data['data']:
        if 'message' in post:
            messages.append([post['from']['name'], post['message']])
        if 'comments' in post:
            for comment in post['comments']['data']:
                if 'message' in comment:
                    messages.append([comment['from']['name'], comment['message']])

    writer = UnicodeWriter(outfile, delimiter='\t')
    for message in messages:
        writer.writerow(message)