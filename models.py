'''
Sensor Model Class
I kept this really simple
Google App Engine currently gets incredibly finicky with queries
to keep CPU useage low

Since this ends up being a ton of data, I felt a simple DB was better
than something that requires more overhead

I wouldn't have done it this way in MySQL
'''

from google.appengine.ext import db

class Log(db.Model):
    sensor = db.StringProperty(required=True)
    dateTime = db.DateTimeProperty(required=True)
    reading = db.FloatProperty(required=True)
