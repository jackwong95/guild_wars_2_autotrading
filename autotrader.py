import requests
import json

minProfit = 50000;
minCost = 10000;
maxCost = 100000;
marketMaxSell = 500000;
MAX_CHAR_COUNT = 30

typeFilters = ["Armor", "UpgradeComponent", "Weapon", "MiniPet", "Consumable", "CraftingMaterial", "Gizmo"]
rarityFilterList = ["Exotic"]

ALL_ITEMS_FILE = "all_listed_items.txt"
TOKEN = "<TOKEN>";
BASE_URL = "https://api.guildwars2.com/v2";
MARKET_LISTING_URL = "{}/commerce/listings?access_token={}".format(BASE_URL, TOKEN)
ITEM_LISTING_URL = "{}/items?access_token={}".format(BASE_URL, TOKEN);
COMMERCE_ITEM_LISTING_URL = "{}/commerce/listings?".format(BASE_URL);
TRANSACTION_CURRENT_BUY_URL = "{}/commerce/transactions/current/buys?access_token={}".format(BASE_URL, TOKEN);
TRANSACTION_CURRENT_SELL_URL = "{}/commerce/transactions/current/sells?access_token={}".format(BASE_URL, TOKEN);


def download_all_listing_item_ids():
    market_listing = requests.get(url = MARKET_LISTING_URL).json()

    output_file = open(ALL_ITEMS_FILE, "w")

    cnt = 0
    finalCnt = 0
    ids = ""
    for itemId in market_listing:
        
        if cnt == 100:
            req_url = "{}&ids={}".format(ITEM_LISTING_URL, ids)
            commerce_listing = requests.get(url = req_url).json()
            #print(commerce_listing)
            
            for item in commerce_listing:
                output_file.write(str(item['id']) + ',' + item['name'] + ',' + item['rarity'] + ',' + item['type'] + "\n")
            
            print(finalCnt)
            ids = ""
            cnt = 0
            
        ids = ids + str(itemId) + ",";
        cnt = cnt + 1
        finalCnt = finalCnt + 1
  
    req_url = "{}&ids={}".format(ITEM_LISTING_URL, ids)
    commerce_listing = requests.get(url = req_url).json()
    for item in commerce_listing:
        output_file.write(str(item['id']) + ',' + item['name'] + ',' + item['rarity'] + ',' + item['type'] + "\n")

    output_file.close()
    
def read_from_items_file():
    file = open(ALL_ITEMS_FILE, 'r')
    lines = file.readlines()
    dicts = {}
    
    for line in lines:
        l = line.strip().split(",")
        currDict = {'name':l[1], 'rarity':l[2], 'type':l[3]}
        
        if currDict['rarity'] not in rarityFilterList:
            continue
            
        if currDict['type'] not in typeFilters:
            continue
            
        dicts[l[0]] = currDict
        
    return dicts

def get_market_listing(item_ids):
    market_listing = []
    cnt = 0
    finalCnt = 0
    ids = ""
    
    for item_id in item_ids:
        
        if cnt == 150:
            try:
            
                req_url = "{}&ids={}".format(COMMERCE_ITEM_LISTING_URL, ids)
                commerce = requests.get(url = req_url).json()
                market_listing.extend(commerce)
                
                print(finalCnt)
                
                ids = ""
                cnt = 0

            except:
                continue
            
        ids = ids + str(item_id) + ",";
        cnt = cnt + 1
        finalCnt = finalCnt + 1
        
    req_url = "{}&ids={}".format(COMMERCE_ITEM_LISTING_URL, ids)
    commerce = requests.get(url = req_url).json()
    market_listing.extend(commerce)
    
    
    return market_listing
    
def filter_based_on_market_listing(item_lookup, listing):
    newDict = {}
    
    for item in listing:
        if 'buys' not in item or 'sells' not in item or len(item['buys']) == 0 or len(item['sells']) == 0:
            continue
            
        maxBuy = max([elem['unit_price'] for elem in item['buys']])
        minSell = min([elem['unit_price'] for elem in item['sells']])
        profit = minSell - maxBuy
        
        itemId = str(item['id'])
        item_lookup[itemId]['maxBuy'] = maxBuy
        item_lookup[itemId]['minSell'] = minSell
        item_lookup[itemId]['profit'] = profit
        
        newDict[itemId] = item_lookup[itemId]
    
    return newDict
        #print(itemId + ", " + item_lookup[itemId]['name'] + ", " + str(maxBuy) + ", " + str(minSell) + ", " + str(profit))
        #print(listing[] + " " + itemIdToNameMap.get(commerceListing.id+"") + " " + maxBuy + " " + minSell + " " + profit)

def print_item(key, item_lookup):
    print('id: {}, name: {}, market_max_buy: {}, market_min_sell:{}, profit:{}'.format(
        key,
        item_lookup[key]['name'],
        str(item_lookup[key]['maxBuy']),
        str(item_lookup[key]['minSell']),
        str(item_lookup[key]['profit'])
        ))

def current_buy_items():

    curr_buy_items = []
    page = 0
    
    while True:
        try:
            url = "{}&page={}".format(TRANSACTION_CURRENT_BUY_URL, page)
            buy_resp = requests.get(url = url).json()
            for resp in buy_resp:
                resp['item_id'] = str(resp['item_id'])
                curr_buy_items.append(resp)
            page = page + 1
        except:
            break
        
    return curr_buy_items

def current_sell_items():

    curr_sells_items = []
    page = 0
    
    while True:
        try:
            url = "{}&page={}".format(TRANSACTION_CURRENT_SELL_URL, page)
            buy_resp = requests.get(url = url).json()
            for resp in buy_resp:
                resp['item_id'] = str(resp['item_id'])
                curr_sells_items.append(resp)
            page = page + 1
        except:
            break
        
    return curr_sells_items

def what_to_remove(item_lookup):

    items_to_remove = []    
    
    # catch duplicated items
    buy_transaction_duplicate_cnt = {}
    my_buy_transaction = {}
    for resp in current_buy_items():
        key = str(resp['item_id'])
        my_buy_transaction[key] = resp['price']
        
        if key not in buy_transaction_duplicate_cnt:
            buy_transaction_duplicate_cnt[key] = 1
        else:
            
            try:
                item = item_lookup[key]
                
                if buy_transaction_duplicate_cnt[key] == 1:
                    # want to remove completely, add in the first existing entry 
                    items_to_remove.append(item)
                buy_transaction_duplicate_cnt[key] = buy_transaction_duplicate_cnt[key] + 1
                
                item['item_id'] = key
                items_to_remove.append(item)
                #print(key + " " + str(my_buy_transaction[key]) + " " + str(item_lookup[key]['name']))
            except:
                continue

        #if key in item_lookup and my_buy_transaction[key] != item_lookup[key]['maxBuy']:
        #    print_item(key, item_lookup)
        
    my_sell_transaction = {}
    for resp in current_sell_items():
        key = resp['item_id']
        my_sell_transaction[key] = resp['price']

    itemIdsPassingFilter = {}
    for idx in item_lookup:
        item = item_lookup[idx]
        if item['profit'] >= minProfit and item['maxBuy'] <= maxCost and item['maxBuy'] >= minCost:
            itemIdsPassingFilter[str(idx)] = item

    print("what to remove")
    for idx in my_buy_transaction.keys():
        itemId = str(idx)
        if itemId in item_lookup and (itemId not in itemIdsPassingFilter or my_buy_transaction[itemId] != item_lookup[itemId]['maxBuy'] or itemId in my_sell_transaction):
            #print(str(itemId not in itemIdsPassingFilter) + " " + str(my_buy_transaction[itemId]) + " " + str(my_buy_transaction[key] != item_lookup[itemId]['maxBuy']))
            item = item_lookup[itemId]
            item['item_id'] = itemId
            items_to_remove.append(item)
            
    return items_to_remove

def what_to_buy(item_lookup):

    items_to_buy = []
    my_buy_transaction = {}
    for resp in current_buy_items():
        key = resp['item_id']
        my_buy_transaction[key] = resp['price']

    # don't buy anymore if there are already 2 item in inventory
    my_sell_transaction = {}
    for resp in current_sell_items():
        if resp['quantity'] >= 2:
            key = resp['item_id']
            my_sell_transaction[key] = resp['price']

    itemSortedByProfit = []
        
    itemIdsPassingFilter = {}
    for idx in item_lookup:
        item_id = str(idx)
        
        item = item_lookup[item_id]
        itemSortedByProfit.append((item_id, item['maxBuy']))
        if item_id not in my_buy_transaction and item_id not in my_sell_transaction and item['profit'] >= minProfit and item['maxBuy'] <= maxCost and item['maxBuy'] >= minCost and item['minSell'] <= marketMaxSell and len(item['name']) <= MAX_CHAR_COUNT:
            itemIdsPassingFilter[item_id] = item
            #print(item_lookup[item_id]['name'])
    
    itemSortedByProfit.sort(key=lambda tup: tup[1]) #, reverse=True
    
    
    print("what to buy")
    for idx in itemSortedByProfit:
        itemId = str(idx[0])
        if itemId in my_buy_transaction:
            continue

        if itemId in itemIdsPassingFilter:
            print_item(itemId, item_lookup)
            items_to_buy.append(itemId)
    return items_to_buy

def refresh_all_items():
    #download_all_listing_item_ids()
    at_item_lookup = read_from_items_file()
    market_listing = get_market_listing(at_item_lookup)
    at_item_lookup = filter_based_on_market_listing(at_item_lookup, market_listing)

    at_rmv_item = what_to_remove(at_item_lookup)
    at_buy_item = what_to_buy(at_item_lookup)
    return at_rmv_item, at_buy_item, at_item_lookup
    

#refresh_all_items()
