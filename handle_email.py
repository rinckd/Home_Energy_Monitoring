# -*- coding: utf-8 -*-
import logging
import exceptions
import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp import mail_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import taskqueue

from google.appengine.ext import db
from google.appengine.api.datastore import Key

from datetime import datetime, date, timedelta

def parse_header(header):
    sensor_key = [] # list of sensors in order that they appear in .csv attachment
    logging.info(header)
    header = header.split('","')
    for element in header:
        if (element[0] == 'D') or (element[0] == '#') or (element[0] =='"'):
            continue 
        elif element[0] == 'T':
            pass
        else:
            sensor_key.append('skip')
            continue

        logging.info(element)
        location = re.compile(r"\(LBL: ([^']*)\)").search(element).group(1)
        sensor_key.append(location)
    return sensor_key
    
class MyMailHandler(mail_handlers.InboundMailHandler):
    def receive(self, message):
        (encoding, payload) = list(message.bodies(content_type='text/plain'))[0]
        body_text = payload.decode()
        logging.info('Received email message from %s: %s' % (message.sender,
                                                             body_text))
        attachments = []
        try:
            if message.attachments:
                if isinstance(message.attachments[0], basestring):
                    attachments = [message.attachments]
                else:
                    attachments = message.attachments
        except exceptions.AttributeError:
            logging.info('This email has no attachments')
        for filename, content in attachments:
            logging.info("filename: " + filename)
            data = content.decode()
            data = data.split('\n')
            counter = 0
            for element in data:
                # delete the top title row
                if counter == 0:
                    counter += 1
                    continue
                if counter == 1:
                    sensor_key = parse_header(element)
                    logging.info(sensor_key)
                    nodes = len(sensor_key)     # note: dew points and relative humidity are not saved
                                                # these are located at the end of the file
                                                # if this location changes with hobonode updates
                                                # this will cause a problem
                    counter += 1
                    continue
                element = element.split(',')
                del element[0]
                try:
                    sampleTime = element[0]
                except IndexError:
                    continue
                logging.info(sampleTime)
                del element[0]
                sensor_number = 0
                for column in element:
                    if sensor_number+1 > nodes:
                        continue
                    if sensor_key[sensor_number] == 'skip':
                        sensor_number += 1
                        continue
                    if not column:
                        logReading = 0.0
                    else:
                        logReading = float(column)
                    taskqueue.add(url='/log_data',
                                  params={'sensor': sensor_key[sensor_number],
                                          'sampleTime': sampleTime,
                                          'logReading': logReading})
                    sensor_number += 1
#                logging.info(element)

        
        
application = webapp.WSGIApplication([MyMailHandler.mapping()],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
