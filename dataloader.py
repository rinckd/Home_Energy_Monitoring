import datetime
import os
import csv
import logging

import re

from google.appengine.ext import db
from google.appengine.api.datastore import Key
from google.appengine.api import taskqueue
from energy import models

import sys

print 'Content-Type: text/html'
print ''
print(sys.version)
sensors = models.Sensor.all()
conversion = []
sensor_key = []
header_info = ["#","Date Time, GMT-04:00","Temp, °F (LBL: 2nd Floor Hallway)","RH, % (LBL: 2nd Floor Hallway)","Temp, °F (LBL: 1st Floor Hutch)","RH, % (LBL: 1st Floor Hutch)","Temp, °F (LBL: Outside)","RH, % (LBL: Outside)","Temp, °F (LBL: Boiler Room)","RH, % (LBL: Boiler Room)","Temp, °F (LBL: Boiler Return)","Temp, °F (LBL: Boiler Send)","Temp, °F (LBL: Apartment Hallway)","RH, % (LBL: Apartment Hallway)","DewPt, °F","DewPt, °F","DewPt, °F","DewPt, °F","DewPt, °F"]
'''
rows =[ '1,03/24/11 02:01:00 AM,62.319,35.072,141.022,193.336,56.858,44.621,34.403,35.558',
         '2,03/24/11 02:02:00 AM,62.276,35.135,140.475,170.582,56.858,44.621,34.410,35.558',
         '3,03/24/11 02:03:00 AM,62.319,35.072,146.140,157.329,56.815,44.618,34.403,35.517',
         '4,03/24/11 02:04:00 AM,62.362,35.009,150.476,174.160,56.858,44.684,34.395,35.593',
         '5,03/24/11 02:05:00 AM,62.406,35.077,148.883,199.033,56.858,44.715,34.483,35.611',
         '6,03/24/11 02:06:00 AM,62.447,34.981,143.172,201.306,56.815,44.681,34.450,35.552',
         '7,03/24/11 02:05:00 PM,,,999.999,999.999,99.999,99.999,99.999,99.999']
'''

data = []
for row in csv.reader(open('Home_Setup_All_Data.csv'), delimiter=','):
    data.append(row)

for element in header_info:
    if (element[0] == 'D') or (element[0] == '#'):
        continue 
    elif element[0] == 'T':
        units = 'Temp'
        if element[8] == 'F':
            conversion.append('False')
        else:
            conversion.append('True')
    else:
        units = 'RH'
        conversion.append('False')
    location = re.compile(r"\(LBL: ([^']*)\)").search(element).group(1)
    sensor_key.append(units + location)
    if any((item.name == location and item.units == units) for item in sensors) :
        pass # sensor already exists in database
    else:
        # add new sensor to database
        new_sensor = models.Sensor(key_name = units + location, name = location, units = units)
        new_sensor.put()
        print 'made new sensor', new_sensor
        print ('<br>')
        
nodes = len(sensor_key) # note: dew points are not saved
                        # these are located at the end of the file
                        # if this location changes with hobonode updates
                        # this will cause a problem
for row in data:
    try:
        del row[0] # first column is just the sequential sample number
    except IndexError:
        continue
    sampleTime = row[0]
    del row[0]
    sensor_number = 0
    

    for column in row:
        if sensor_number+1 > nodes:
            continue
        if not column:
            logReading = 0.0
        else:
            logReading = float(column)
        taskqueue.add(url='/log_data',
                      params={'key_identifier': sensor_key[sensor_number],
                              'sampleTime': sampleTime,
                              'logReading': logReading})
        sensor_number += 1

# find out what hour it is from last samples
# if >1 then print new days graphic
# blobstore for storing images ? 
# Serving Dynamic Images with Google App Engine (python) Austin Chau
# if not... text blub for storing google chart link maker

print 'go away now'

print ('<br>')
print ''

if os.environ['SERVER_SOFTWARE'].startswith('Development'):
    print ('<p>You are running on the development server.   You can use '
           '<a href="/_ah/admin/inboundmail">the development server console</a> '
           'to send email to this application.</p>')
else:
    app_email_address = 'support@' + os.environ['APPLICATION_ID'] + '.appspotmail.com'
    print ('<p>You are running on App Engine.  You can '
           '<a href="mailto:%s">send email to %s</a> to send a message '
           'to the application.</p>' % (app_email_address, app_email_address))

print '<p>This app will write to the log when it receives email messages.</p>'

print '<p>The time is: %s</p>' % str(datetime.datetime.now())
