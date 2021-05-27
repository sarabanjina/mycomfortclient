'''
Main for mycomfortclient
'''
import argparse
from mycomfortclient.myComfortObject import myComfortObject
from mycomfortclient.myComfortGateway import Gateway
import logging

logger = logging.getLogger("mycomfortclient")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def main():
    '''
    Main method
    '''
    parser = argparse.ArgumentParser("mycomfortclient")
    parser.add_argument("--hostname", action="store", required=True)
    parser.add_argument("--port", action="store", default="80", required=False)
    parser.add_argument("--username", action="store", required=True)
    parser.add_argument("--password", action="store", required=True)
    parser.add_argument("--cache", action="store", default="60", required=False)
    parser.add_argument("--debug", action="store_true", required=False)

    args = parser.parse_args()

    if args.debug:
        gateway = Gateway(args.hostname, args.port, args.username, args.password, args.cache, logging.DEBUG)
    else:
        gateway = Gateway(args.hostname, args.port, args.username, args.password, args.cache)

    for boiler in gateway.boilers():
        print("Boiler serial_no : %s" % boiler.serial_no)
        print("Boiler actual temperature : " + boiler.getBoilerTemperature())
        print("Boiler setpoint temperature : " + boiler.getBoilerSetpointTemperature())
        print("Boiler exhaust temperature : " + boiler.getExhaustTemperature())
        print("Boiler operating hours : %s" % (boiler.getBurnerHours()))
        print("Boiler current output : %s" % (boiler.getBurnerModulation()))
        print("Boiler current mode : %s" % (boiler.getOperatingMode()))
        print("Boiler cleaning stage 1 : %s" % (boiler.getOperatingTimeCleaning()))
        print("Boiler cleaning stage 2 : %s" % (boiler.getOperatingTimeMainCleaning()))
        print("Boiler full service : %s" % (boiler.getOperatingTimeMaintenance()))
        print("Boiler burner starts : %s" % (boiler.getBurnerStarts()))
        print("Boiler pellet consumption since bulk fill : %s" % (boiler.getBoilerConsumptionBulkfill()))
        print("Boiler pellet consumption total : %s" % (boiler.getBoilerConsumptionTotal()))

    for module in gateway.modules():
        print("Module serial_no : %s" % module.serial_no)
        print("Outside temperature : " + module.getOutsideTemperature())
        print("Actual flow temperature : " + module.getFlowTemperature())
        print("Setpoint flow temperature : " + module.getFlowSetpointTemperature())
        if module.isDHWCircuit():
            print("Actual DHW temperature : " + module.getDHWTemperature())
            print("Setpoint DHW temperature : " + module.getDHWSetpointTemperature())

        print("Active program : " + module.getActiveProgram())
        print("Operation mode : " + module.getOperationMode())
        print("Burner active : " + str(module.getBurnerActive()))
        print("Room temperature setpoint : " + module.getCurrentDesiredTemperature())

if __name__ == "__main__":
    main()
