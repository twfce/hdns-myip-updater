#! /usr/bin/python3

import os
import json

from time import sleep
from datetime import datetime
from colored import fg, attr
from hdns import hdns
from myip import myip

def updateDNSRecords(ip):    
    print ("{color}{timestamp} | [*] Requesting all zones{reset}".format(color=fg(3), timestamp=datetime.now(), reset=attr(0)))
    zones = [zone for zone in hdnsAPI.getAllZones() if zone["name"] in CONFIG["zones"]] 

    for zone in zones:
        print ("{color}{timestamp} | [{zone}] Requesting all registered A records for zone{reset}".format(color=fg(3), timestamp=datetime.now(), zone=zone["name"], reset=attr(0)))
        registered_records = hdnsAPI.getAllRecords(zone["id"], record_type="A")        
        print ("{color}{timestamp} | [{zone}] Checking CONFIGured records{reset}".format(color=fg(3), timestamp=datetime.now(), zone=zone["name"], reset=attr(0)))
        for record in CONFIG["zones"][zone["name"]]["records"]:
            registered_record = next((rr for rr in registered_records if rr["name"] == record), None)
            if registered_record:
                print ("{color}{timestamp} | [{record}.{zone}] Already registered. Going to update record{reset}".format(color=fg(3), timestamp=datetime.now(), record=record, zone=zone["name"], reset=attr(0)))
                hdnsAPI.updateRecord(recordId=registered_record["id"], zoneId=zone["id"], name=registered_record["name"], value=ip, ttl=60)
                print ("{color}{timestamp} | [{record}.{zone}] Updated{reset}".format(color=fg(2), timestamp=datetime.now(), record=record, zone=zone["name"], reset=attr(0)))
            else:
                print ("{color}{timestamp} | [{record}.{zone}] Not registered. Going to create new record{reset}".format(color=fg(3), timestamp=datetime.now(), record=record, zone=zone["name"], reset=attr(0)))

                hdnsAPI.createRecord(zoneId=zone["id"], name=record, value=ip, ttl=60)
                print ("{color}{timestamp} | [{record}.{zone}] Created{reset}".format(color=fg(2), timestamp=datetime.now(), record=record, zone=zone["name"], reset=attr(0)))

def checkIpChanged(currentIP):
    if os.path.isfile(".remember"):
        f = open(".remember", "r")
        lastIP = f.read()
        f.close()
        currentIP = report['external_ip']

        if lastIP == currentIP:
            print ("{color}{timestamp} | [*] IP did not change. It's still {IP}{reset}".format(color=fg(3), timestamp=datetime.now(), IP=currentIP, reset=attr(0)))
        else:
            print ("{color}{timestamp} | [*] IP changed! From {lastIP} to {currentIP}{reset}".format(color=fg(214), timestamp=datetime.now(), lastIP=lastIP, currentIP=currentIP, reset=attr(0)))
            f = open(".remember", "w")
            f.write(currentIP)
            f.close()
            print ("{color}{timestamp} | [+] Updated IP cache{reset}".format(color=fg(2), timestamp=datetime.now(), reset=attr(0)))
            updateDNSRecords(currentIP)
    else:
        print ("{color}{timestamp} | [*] This is the first run. IP is {IP}{reset}".format(color=fg(3), timestamp=datetime.now(), IP=currentIP, reset=attr(0)))
        updateDNSRecords(currentIP)
        f = open(".remember", "w")
        f.write(currentIP)
        f.close()

def main():
    while True:        
        checkIpChanged(myipAPI.requestIP())
        sleep(SLEEP_TIMER)

if __name__ == "__main__":
    try:
        HDNS_TOKEN = os.environ["HDNS_TOKEN"]
    except KeyError:
        print ("{color}{timestamp} | [X] You need to specify env variable HDNS_TOKEN!{reset}".format(color=fg(1), timestamp=datetime.now(), reset=attr(0)))
        exit()
    
    SLEEP_TIMER = os.environ["SLEEP_TIMER"]
    CONFIG = json.loads(open("config.json").read())

    hdnsAPI = hdns(HDNS_TOKEN)
    myipAPI = myip()
    main()
