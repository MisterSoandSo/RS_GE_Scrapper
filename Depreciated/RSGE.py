'''
Author: Andrew So (MisterSoandSo)
Writen in python 3.7 for a CS class. 
'''

import urllib.request
import datetime
import os
import json
import sys

RUNESCAPE_GE_URL = "http://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item="
SAVE_DIRECTORY = sys.path[0] + "/ge-logs/"
ITEM_DICTIONARY = {}
ITEM_SHOPPING_LIST = {}
TODAY = None
USER_ITEMS_FILENAME = "items.json"


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

#Returns String from memory list
def rettodayTrend(item):
    rid = "item" + str(item +1)
    item_price_str = ITEM_DICTIONARY[rid]["todayTrend"]
    return item_price_str
    
def retCurrentPrice(item):
    rid = "item"  + str(item +1)
    item_price_str = ITEM_DICTIONARY[rid]["currentPrice"]
    return item_price_str
    
def retItemID(item):
    rid = "item" + str(item +1)
    item_id = ITEM_DICTIONARY[rid]["id"]
    return item_id

def retItemName(item):
    rid = "item" + str(item +1)
    item_name = ITEM_DICTIONARY[rid]["name"]
    return item_name

#Get information from Online
def getItemInfo(item_id,item_key_from_user):
    global ITEM_INFO
    request_string = RUNESCAPE_GE_URL + str(item_id)
    with urllib.request.urlopen(request_string) as url:
        item_info_dictionary = json.loads(url.read().decode())

    if item_key_from_user is not None:
        item = {}
        item["name"] = extractItemName(item_info_dictionary)
        item["id"] = extractItemID(item_info_dictionary)
        item["currentPrice"] = extractItemCurrentPrice(item_info_dictionary)
        item["todayTrend"] = extractItemtodayTrend(item_info_dictionary)
        ITEM_DICTIONARY[item_key_from_user] = item
        
def parseJson(path_to_user_item_list):
    global ITEM_SHOPPING_LIST
    user_items_json_file = open(path_to_user_item_list, 'r')
    user_items_list_json_text = user_items_json_file.read()
    user_items_dictionary = json.loads(user_items_list_json_text)  
    ITEM_SHOPPING_LIST = user_items_dictionary

#Format for writing to text file
def niceFormatItemPrice(items_list):
    str_format = ""

    if len(items_list) <= 0:
        return "none"

    for item in range(len(items_list)):
        str1 = str(retItemID(item))
        str2 = str(retItemName(item))
        str3 = str(retCurrentPrice(item))
        str4 = str(rettodayTrend(item))
        str_format = str_format + str1.ljust(6) + str2.ljust(25) + "| " + str3.ljust(8) + " | " + str4 + "\n"
    return str_format

def OutputLogs(items_list):
    global TODAY
    today = datetime.date.today()
    TODAY = today.isoformat()
    filename = today.isoformat() + "-ge-log.txt"

    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)

    log_file = open(SAVE_DIRECTORY + filename, "w")
    log_file.write("---- Please note prices are subject to change on the actual market ----\n")
    log_file.write("Id: ".ljust(31)  + "| Price: ".ljust(11) + "| Today's trends: " +"\n")
    log_file.write(niceFormatItemPrice(items_list))
    log_file.write("\n---- I'm not responsible for your lost of gold from bad transactions ----\n")

#main function call                                      
def main_ge():
    print("Scraping the Grand Exchange. Please wait as this may take time ...")
    parseJson(os.path.join(sys.path[0], USER_ITEMS_FILENAME))
    for key, item_info in sorted(ITEM_SHOPPING_LIST.items()):
        getItemInfo(item_info["id"], key)
    OutputLogs(ITEM_DICTIONARY)
    print("Done.")

if __name__ == "__main__":
    main_ge()


