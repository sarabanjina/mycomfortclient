# myComfortClient
Windhager myComfort Python client for Home Assistant

# Usage
This module is intended to use inside HA to interact as a client of RC7030 gateway (myComfort).

Here is the manual usage of the module : 
    
    python3 -m mycomfortclient --help
    usage: mycomfortclient [-h] --hostname HOSTNAME [--port PORT] --username
                       USERNAME --password PASSWORD [--cache CACHE] [--debug]

    optional arguments:
      -h, --help           show this help message and exit
      --hostname HOSTNAME
      --port PORT
      --username USERNAME
      --password PASSWORD
      --cache CACHE
      --debug

# Example
Here is what you should get in a real world : 

    Boiler serial_no : 0700183ec901
    Boiler actual temperature : 35.77
    Boiler setpoint temperature : 0.0
    Boiler exhaust temperature : 31.4
    Boiler operating hours : 991
    Boiler current output : 0
    Boiler current mode : Stand-by
    Boiler cleaning stage 1 : 516
    Boiler cleaning stage 2 : 1566
    Boiler full service : 3666
    Boiler burner starts : 939
    Boiler pellet consumption since bulk fill : 1.78
    Boiler pellet consumption total : 1.78
    Module serial_no : 07024a742a01
    Outside temperature : 11.8
    Actual flow temperature : 16.9
    Setpoint flow temperature : 0.0
    Actual DHW temperature : 14.4
    Setpoint DHW temperature : 10.0
    Active program : Stand-by
    Operation mode : Stand-by
    Burner active : False
    Room temperature setpoint : 5.0
    Module serial_no : 07024a749b01
    Outside temperature : 11.8
    Actual flow temperature : 17.1
    Setpoint flow temperature : 0.0
    Active program : Heating program 1
    Operation mode : Stand-by heating limit
    Burner active : False
    Room temperature setpoint : 13.0    

# Limitations
It doesn't handle thermostat for now (I don't have anyone to test). It it only tested on a Windhager Biowin II heater (for now).
