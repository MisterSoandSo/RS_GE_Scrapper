#!/usr/bin/env python

import urllib.request, urllib.error
import json
import config
import pyrebase


RUNESCAPE_GE_URL = "http://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item="
ExchangeID = []
firebase = pyrebase.initialize_app(config.config)
db = firebase.database()

def doNothing():
    pass

#Extract information from json
def extractItemtodayTrend(item_dict):
    item_price_str = item_dict["item"]["today"]["price"]
    return item_price_str
    
def extractItemCurrentPrice(item_dict):
    item_price_str = item_dict["item"]["current"]["price"]
    return item_price_str
    
def extractItemID(item_dict):
    item_id = item_dict["item"]["id"]
    return item_id

def extractItemName(item_dict):
    item_name = item_dict["item"]["name"]
    return item_name

#Save Item to dictionary
def saveItem(item_info_dictionary, update):   
    item = {}
    item["name"] = extractItemName(item_info_dictionary)
    key  = extractItemID(item_info_dictionary)
    item["id"] = key
    item["currentPrice"] = extractItemCurrentPrice(item_info_dictionary)
    item["todayTrend"] = extractItemtodayTrend(item_info_dictionary)
    if update:
        db.child("exchangeID").child(key).update(item)
    else:
        db.child("exchangeID").child(key).set(item)

#Get information from Online
def getItemInfo(key,update):
    url = RUNESCAPE_GE_URL + str(key)
    try:
        conn = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        pass
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        pass
    else:
        # 200
        item_info_dictionary = json.loads(conn.read().decode())
        if item_info_dictionary is not None:
            saveItem(item_info_dictionary,update)

#Extract existing keys from firebase 
def extractKeys():
    inventory = db.child("exchangeID").get()
    for eID in inventory.each():
        t_key = int(eID.key())
        if not t_key in ExchangeID: 
            ExchangeID.append(t_key)

#main function call                                      
def main_ge():
    print("Scraping the Grand Exchange. Please wait as this may take time ...")
    extractKeys()
    for k in range(10):
        print("Updating known Exchange ID items ...")
        i = 0
        for i in ExchangeID:
            #getItemInfo(i,1)
            doNothing()
        print("Looking for Exchange ID items ...")
        for (j) in range(50):
            key = i+j+1
            getItemInfo(key, 0)
        print("Total number of Valid ID's found: ", str(len(ExchangeID))) 
    print("Done.")
    
if __name__ == "__main__":
    main_ge()
