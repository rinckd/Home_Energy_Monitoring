'''
Sensor Configuration File

Changing this list of sensors changes what sensor will be available to view from the website
It WILL NOT change what data is logged to the sensor.

All data logged from sensor comes from HOBO software. If those sensors are labeled names
different from the names seen below, you will not see any information from these
sensors on the website, but that data is being stored in Google App Engine's database
'''
class Sensors:
    ##############################################################################
    #
    #
    # Make sure all sensors are set to transmit Fahrenheit!!!
    #
    #
    ##############################################################################
    #
    # list:
    #    - type the names of each of the sensors EXACTLY as it is displayed
    #      in Hobo software in the field below
    #    
    list = ['2nd Floor Hallway', '1st Floor Hutch', 'Outside', 'Boiler Room', 
            'Boiler Send', 'Boiler Return','Apartment Hallway']
    #
    ##############################################################################
    #
    # anchor:
    #    - give each sensor in the list a unique one-word identifier
    #      this is just for URL identifiers... so that links are /boilerRoom and 
    #      not /boiler%20Room
    #
    anchor = ['2ndflr_hallway', '1stflr_hutch', 'outside', 'boilerRoom', 'boilerSend', 
              'boilerReturn', 'apt_hallway']
    #
    ##############################################################################
    #
    # name: 
    #    - What we call it on the website user interface
    #    - I added this so that additional information could be used in Hobo software
    #    - that wouldn't be exposed to end users.
    #    - For Example: We hid a sensor in the hutch on the first floor
    #    -              To remember where it is, the list calls it '1st Floor Hutch'
    #    -              On the website this is just called '1st Floor'
    #
    name = ['2nd Floor Hallway', '1st Floor', 'Outside', 'Boiler Room', 'Boiler Send', 
            'Boiler Return', 'Apartment Hallway']
    #
    ##############################################################################
    