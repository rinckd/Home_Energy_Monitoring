# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from google.appengine.api import taskqueue
from google.appengine.ext import db
from google.appengine.api.datastore import Key

from dateutil.parser import parse
from datetime import datetime, date, timedelta
import re

import models
import config

def root_view(request):
    loc = datetime.today()
    loc_day = loc.day
    loc_month = loc.month
    loc_year = loc.year
    location = '/data/%d/%d/%d/outside' % (loc_month, loc_day, loc_year)
    return HTTPFound(location = location)

def dateview(request):

    requestday = int(request.matchdict['day'])
    requestmonth = int(request.matchdict['month'])
    requestyear = int(request.matchdict['year'])   
    requestlocation = str(request.matchdict['location']) 
    if 'form.submitted' in request.params:
        result = parse(request.params['date'])
        requestday = result.day
        requestmonth = result.month
        requestyear = result.year
    sensors = config.Sensors.name
    sensor_links = config.Sensors.anchor
    sensor_tabs = str(88/len(sensors))+'%' # this adjusts size of sensor tab 
                                           # links in mako template 
        
    changelocation_url = '%s/data/%02d/%02d/%04d/' % (request.application_url, requestmonth, requestday, requestyear)
    date = '%02d/%02d/%04d' % (requestmonth, requestday, requestyear)    

    try:
        sensor_id = config.Sensors.anchor.index(requestlocation) # index finds location of sensor within list
    except ValueError:
        sensor_id = -1
    if sensor_id >= 0:
        query_location = config.Sensors.list[sensor_id]
    else:
        query_location = 'not found'
    
    day_start = datetime(requestyear, requestmonth, requestday, 0, 0, 0)
    day_end = day_start + timedelta(days=1)
    q = models.Log.all()
    q = db.Query(models.Log)
    q.filter('sensor ==', config.Sensors.list[sensor_id])
    q.filter('dateTime >=', day_start)
    q.filter('dateTime <', day_end)
    logging = ''
    
    if not q:
        logging += 'No readings found'
    for i, item in enumerate(q):
        if i > 0:
            logging += ','
        logging += '[new Date('
        logging += str(item.dateTime.year) + ',' + str(item.dateTime.month-1) + ',' + str(item.dateTime.day) + ','
        logging += str(item.dateTime.hour) + ',' + str(item.dateTime.minute) + ',0),'
        logging += str(item.reading)+']'

    return dict (date = date, requestlocation = requestlocation, 
                 changelocation_url = changelocation_url, sensors = sensors,
                 sensor_links = sensor_links, sensor_tabs = sensor_tabs, logging = logging)


def test(request):
    '''
    my simple debug view for google app engine
    if you want to debug simply add values to logging variable
    then go to url /test to see results
    '''
    
    logging = ''

#    loc = datetime.today()
#    loc_day = loc.day
#    loc_month = loc.month
#    loc_year = loc.year
#    logging += '/data/%d/%d/%d/outside' % (loc_month, loc_day, loc_year)
    
    return dict(logging = logging)



def form2(request):
     return {'project':'energy'}
