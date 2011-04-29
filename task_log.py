import logging
import models
import datetime

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

fmt = '%m/%d/%y %I:%M:%S %p' # datetime format Hobo keeps time in


class MailWorker(webapp.RequestHandler):
    def post(self):
        data_point = float(self.request.get('logReading'))
        new_log = models.Log(sensor = self.request.get('sensor'),
                             dateTime =  datetime.datetime.strptime(self.request.get('sampleTime'), fmt),
                             reading = data_point)
        new_log.put()                     
        logging.info('Logged a sensor reading')
        logging.info(self.request.get('sampleTime'))
        

application = webapp.WSGIApplication([('/.*', MailWorker)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
