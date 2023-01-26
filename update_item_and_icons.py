#https://pyautogui.readthedocs.io/en/latest/

import requests

minProfit = 50000;
minCost = 10000;
maxCost = 100000;
marketMaxSell = 500000;

typeFilters = ["Armor"]
rarityFilterList = ["Exotic"]

ALL_ITEMS_FILE = "all_listed_items.txt"
TOKEN = "<TOKEN>";
BASE_URL = "https://api.guildwars2.com/v2";
MARKET_LISTING_URL = "{}/commerce/listings?access_token={}".format(BASE_URL, TOKEN)
ITEM_LISTING_URL = "{}/items?access_token={}".format(BASE_URL, TOKEN);
COMMERCE_ITEM_LISTING_URL = "{}/commerce/listings?".format(BASE_URL);
TRANSACTION_CURRENT_BUY_URL = "{}/commerce/transactions/current/buys?access_token={}".format(BASE_URL, TOKEN);
IMAGE_LOCATION = "icon/"

def download_all_listing_item_ids():
    market_listing = requests.get(url = MARKET_LISTING_URL).json()

    output_file = open(ALL_ITEMS_FILE, "w")
    
    # to remove duplicated items
    itemDict = {}
    cnt = 0
    finalCnt = 0
    ids = ""
    for itemId in market_listing:
        
        if cnt == 100:
            req_url = "{}&ids={}".format(ITEM_LISTING_URL, ids)
            commerce_listing = requests.get(url = req_url).json()
            #print(commerce_listing)
            
            for item in commerce_listing:   
                if item['name'] in itemDict:        
                    itemDict[item['name']]['hasDuplicate'] = True
                else:
                    itemDict[item['name']] = {
                        'output_line' : str(item['id']) + ',' + item['name'] + ',' + item['rarity'] + ',' + item['type'] + "\n",
                        'hasDuplicate' : False
                    }
            
            print(finalCnt)
            ids = ""
            cnt = 0
            
        ids = ids + str(itemId) + ",";
        cnt = cnt + 1
        finalCnt = finalCnt + 1
  
    req_url = "{}&ids={}".format(ITEM_LISTING_URL, ids)
    commerce_listing = requests.get(url = req_url).json()

    for item in commerce_listing:
        if item['name'] in itemDict:        
            itemDict[item['name']]['hasDuplicate'] = True
        else:
            itemDict[item['name']] = {
                'output_line' : str(item['id']) + ',' + item['name'] + ',' + item['rarity'] + ',' + item['type'] + "\n",
                'hasDuplicate' : False
            }
            
    for key in itemDict:
        if itemDict[key]['hasDuplicate'] == False:
            output_file.write(itemDict[key]['output_line'])
    
    output_file.close()


download_all_listing_item_ids()
