#https://github.com/Archomeda/gw2-yolomouse-cursors/tree/master/originals
from pynput import keyboard
import mss
import pyautogui
from pynput.keyboard import Key, Controller
import cv2
import numpy
import time
import json
import random
import requests
import autotrader
from datetime import datetime, timedelta
import pytz
import os
import subprocess

TAKE_ALL_POSITION = "take_all_pos.txt"
TAKE_ALL_PATH = 'menu_icons/take_all.png'
DELIVERY_BOX_PATH = 'menu_icons/delivery_box.png'
DELIVERY_BOX_HEIGHT_OFFSET = 100
DELIVERY_BOX_WIDTH_OFFSET = 30
TAKE_ALL_HEIGHT_OFFSET = 0
TAKE_ALL_WIDTH_OFFSET = 0
REMAINING_GOLD_NEEDED = 30000
TARGET_PROFIT = 60000
TARGET_DISCOUNT = 10000
 
TOKEN = "03769DA7-CAB5-9C4D-80D8-5C0EEE7C0F2FDF1AE6D4-8FC5-4A13-A64D-886D64C391D7";
BASE_URL = "https://api.guildwars2.com/v2";
ACCOUNT_WALLET_URL = "{}/account/wallet?access_token={}".format(BASE_URL, TOKEN)
ITEM_BOUGHT_URL = "{}/commerce/transactions/history/buys?access_token={}".format(BASE_URL, TOKEN)

dimensions = {
        'left': 0,
        'top': 0,
        'width': 1920,
        'height': 1080
    }
    
def account_wallet_coin():
    try:
        acc_wallet = requests.get(url = ACCOUNT_WALLET_URL).json()

        for wallet in acc_wallet:
            if wallet['id'] == 1:
                return int(wallet['value'])
    except:
        return int(0)
    
def break_money_down(moneyStr):
    bronze = int(moneyStr[-2:])
    silver = int(moneyStr[-4:-2])
    gold = int((int(moneyStr) - silver -  bronze)/10000)
    return (gold, silver, bronze)
    
sct = mss.mss()
keyboard_controller = Controller()

def backspace(times):
    for i in range(times):
        keyboard_controller.press(Key.backspace)
        keyboard_controller.release(Key.backspace)
        delay = random.uniform(0, 2)
        time.sleep(delay)
        
def press_o(times):
    for i in range(times):
        keyboard_controller.press('o')
        keyboard_controller.release('o')
        delay = random.uniform(0, 2)
        time.sleep(delay)
        
def press_f(times):
    for i in range(times):
        keyboard_controller.press('f')
        keyboard_controller.release('f')
        delay = random.uniform(0, 2)
        time.sleep(delay)
        
def press_enter(times):
    for i in range(times):
        keyboard_controller.press(Key.enter)
        keyboard_controller.release(Key.enter)
        
def press_one(times):
    for i in range(times):
        keyboard_controller.press('1')
        keyboard_controller.release('1')
        delay = random.uniform(0, 2)
        time.sleep(delay)
        
def get_delivery_box_location(img, name, method):
    delivery_box_img = cv2.imread(DELIVERY_BOX_PATH)
    
    result = cv2.matchTemplate(img, delivery_box_img, method)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    
    width = max_loc[0] + delivery_box_img.shape[1] + DELIVERY_BOX_WIDTH_OFFSET
    height = max_loc[1] + delivery_box_img.shape[0] + DELIVERY_BOX_HEIGHT_OFFSET
    
    return (max_loc, ((width, height)))
    
def get_take_all_location(img, name, top_left_offset, bottom_right_offset, method):
    take_all_img = cv2.imread(TAKE_ALL_PATH)
    
    result = cv2.matchTemplate(img, take_all_img, method)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    
    take_all_top_left_x = top_left_offset[0]     + max_loc[0]
    take_all_top_left_y = top_left_offset[1]     + max_loc[1]
    take_all_bottom_right_x = top_left_offset[0] + max_loc[0] + take_all_img.shape[1]
    take_all_bottom_right_y = top_left_offset[1] + max_loc[1] + take_all_img.shape[0]
    
    cv2.rectangle(take_all_img, (take_all_top_left_x, take_all_top_left_y), (take_all_bottom_right_x, take_all_bottom_right_y), (255,0,255), 2)

    cv2.imshow('highlights', take_all_img)
    cv2.waitKey()
    cv2.destroyAllWindows() 
    return ((take_all_top_left_x, take_all_top_left_y), (take_all_bottom_right_x, take_all_bottom_right_y))
    
def buy_item_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = 340
    y_offset = -625
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset+90, take_all_bottom_right_y+y_offset+65))
    
def sell_item_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = 510
    y_offset = -625
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset+90, take_all_bottom_right_y+y_offset+65))
    
def my_transaction_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = 675
    y_offset = -625
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset+90, take_all_bottom_right_y+y_offset+65))
    
def search_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = -75
    y_offset = -518
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset+120, take_all_bottom_right_y+y_offset+0))
    
def gizmo_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = 130
    y_offset = -518
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset-50, take_all_bottom_right_y+y_offset+0))
    
def gizmo_drop_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = -40
    y_offset = -480
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset+70, take_all_bottom_right_y+y_offset+0))
    
def gizmo_exotic_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = -40
    y_offset = -330
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset+70, take_all_bottom_right_y+y_offset+0))
    
def current_transaction_buying_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = -75
    y_offset = -443
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset+120, take_all_bottom_right_y+y_offset+0))
    
def current_transaction_selling_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = -75
    y_offset = -410
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset+120, take_all_bottom_right_y+y_offset+0))
    
def transaction_cancels_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):

    locations = []
    
    first_x_offset = 742
    first_y_offset = -443
    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset, take_all_bottom_right_y+first_y_offset)))

#    first_x_offset = 742
#    first_y_offset = -385
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset, take_all_bottom_right_y+first_y_offset)))
#
#    first_x_offset = 742
#    first_y_offset = -323
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset, take_all_bottom_right_y+first_y_offset)))
#
#    first_x_offset = 742
#    first_y_offset = -262
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset, take_all_bottom_right_y+first_y_offset)))
#
#    first_x_offset = 742
#    first_y_offset = -200
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset, take_all_bottom_right_y+first_y_offset)))
#
#    first_x_offset = 742
#    first_y_offset = -140
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset, take_all_bottom_right_y+first_y_offset)))
#
#    first_x_offset = 742
#    first_y_offset = -80
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset, take_all_bottom_right_y+first_y_offset)))
#
#    first_x_offset = 742
#    first_y_offset = -20
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset, take_all_bottom_right_y+first_y_offset)))

    return locations
  
def buy_individual_item_locations(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):

    locations = []
    
    first_x_offset = 177
    first_y_offset = -460
    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset-13, take_all_bottom_right_y+first_y_offset+31)))

#    first_x_offset = 177
#    first_y_offset = -400
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset-13, take_all_bottom_right_y+first_y_offset+31)))
#    
#    first_x_offset = 177
#    first_y_offset = -338
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset-13, take_all_bottom_right_y+first_y_offset+31)))
#
#    first_x_offset = 177
#    first_y_offset = -277
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset-13, take_all_bottom_right_y+first_y_offset+31)))
#
#    first_x_offset = 177
#    first_y_offset = -215
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset-13, take_all_bottom_right_y+first_y_offset+31)))
#
#    first_x_offset = 177
#    first_y_offset = -155
#    locations.append(((take_all_top_left_x+first_x_offset, take_all_top_left_y+first_y_offset), (take_all_bottom_right_x+first_x_offset-13, take_all_bottom_right_y+first_y_offset+31)))

    return locations
      
def instantly_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = 230
    y_offset = -310
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset+60, take_all_bottom_right_y+y_offset+0))

def instantly_gold_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = 250
    y_offset = -410
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset, take_all_bottom_right_y+y_offset+10))

def instantly_silver_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = 340
    y_offset = -410
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset-25, take_all_bottom_right_y+y_offset+10))

def instantly_bronze_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = 415
    y_offset = -410
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset-25, take_all_bottom_right_y+y_offset+10))

def trading_icon_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y):
    x_offset = -142
    y_offset = -518
    return ((take_all_top_left_x+x_offset, take_all_top_left_y+y_offset), (take_all_bottom_right_x+x_offset-28, take_all_bottom_right_y+y_offset+20))

def refresh_take_all_location():
    scr = numpy.array(sct.grab(dimensions))
    scr_remove = scr[:,:,:3]
    delivery_box_loc = get_delivery_box_location(scr_remove, 'cv2.TM_CCOEFF_NORMED', cv2.TM_CCOEFF_NORMED)
    
    delivery_box_top_left_x = delivery_box_loc[0][0]
    delivery_box_bottom_right_x = delivery_box_loc[1][0]
    delivery_box_top_left_y = delivery_box_loc[0][1]
    delivery_box_bottom_right_y = delivery_box_loc[1][1]
    
    delivery_box_cropped_img = scr_remove[delivery_box_top_left_y:delivery_box_bottom_right_y, delivery_box_top_left_x:delivery_box_bottom_right_x]
    delivery_box_loc = get_take_all_location(delivery_box_cropped_img, 'delivery_box_cropped_img', (delivery_box_top_left_x, delivery_box_top_left_y), (delivery_box_bottom_right_x, delivery_box_bottom_right_y), cv2.TM_CCOEFF_NORMED)
    
    
    take_all_top_left_x = delivery_box_loc[0][0]
    take_all_top_left_y = delivery_box_loc[0][1]
    take_all_bottom_right_x = delivery_box_loc[1][0]
    take_all_bottom_right_y = delivery_box_loc[1][1]
    
    if (os.path.exists(TAKE_ALL_POSITION)):
        os.remove(TAKE_ALL_POSITION)
    with open(TAKE_ALL_POSITION, "w") as file:
        locStr = str(take_all_top_left_x) + ',' + str(take_all_top_left_y) + ',' + str(take_all_bottom_right_x) + ',' + str(take_all_bottom_right_y)
        print(locStr)
        file.write(locStr)
        file.close()

def build_all_locations():
#    img = numpy.array(sct.grab(dimensions))
#    scr_remove = img[:,:,:3]
    
    all_locations = {}
#    scr = scr_remove.copy()
#    delivery_box_loc = get_delivery_box_location(scr_remove, 'cv2.TM_CCOEFF_NORMED', cv2.TM_CCOEFF_NORMED)
#    print(delivery_box_loc)
#    
#    delivery_box_top_left_x = delivery_box_loc[0][0]
#    delivery_box_bottom_right_x = delivery_box_loc[1][0]
#    delivery_box_top_left_y = delivery_box_loc[0][1]
#    delivery_box_bottom_right_y = delivery_box_loc[1][1]
#    all_locations['delivery_box'] = (delivery_box_top_left_x, delivery_box_top_left_y, delivery_box_bottom_right_x, delivery_box_bottom_right_y)
#    
#    delivery_box_cropped_img = scr_remove[delivery_box_top_left_y:delivery_box_bottom_right_y, delivery_box_top_left_x:delivery_box_bottom_right_x]
#    delivery_box_loc = get_take_all_location(delivery_box_cropped_img, 'delivery_box_cropped_img', (delivery_box_top_left_x, delivery_box_top_left_y), (delivery_box_bottom_right_x, delivery_box_bottom_right_y), cv2.TM_CCOEFF_NORMED)
#    
#    take_all_top_left_x = delivery_box_loc[0][0]
#    take_all_top_left_y = delivery_box_loc[0][1]
#    take_all_bottom_right_x = delivery_box_loc[1][0]
#    take_all_bottom_right_y = delivery_box_loc[1][1]
    take_all_top_left_x = 0
    take_all_top_left_y = 0
    take_all_bottom_right_x = 0
    take_all_bottom_right_y = 0
    with open(TAKE_ALL_POSITION) as f:
        positions = f.readline().rstrip().split(",")
        print(positions)
        take_all_top_left_x = int(positions[0])
        take_all_top_left_y = int(positions[1])
        take_all_bottom_right_x = int(positions[2])
        take_all_bottom_right_y = int(positions[3])

    all_locations['take_all'] = (take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)

    buy_loc = buy_item_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    buy_loc_left_x = buy_loc[0][0]
    buy_loc_left_y = buy_loc[0][1]
    buy_loc_right_x = buy_loc[1][0]
    buy_loc_right_y = buy_loc[1][1]
    all_locations['buy_loc'] = (buy_loc_left_x, buy_loc_left_y, buy_loc_right_x, buy_loc_right_y)
    
    sell_loc = sell_item_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    sell_loc_left_x =  sell_loc[0][0]
    sell_loc_left_y =  sell_loc[0][1]
    sell_loc_right_x = sell_loc[1][0]
    sell_loc_right_y = sell_loc[1][1]
    all_locations['sell_loc'] = (sell_loc_left_x, sell_loc_left_y, sell_loc_right_x, sell_loc_right_y)
    
    my_transaction_loc = my_transaction_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    my_transaction_loc_left_x =  my_transaction_loc[0][0]
    my_transaction_loc_left_y =  my_transaction_loc[0][1]
    my_transaction_loc_right_x = my_transaction_loc[1][0]
    my_transaction_loc_right_y = my_transaction_loc[1][1]
    all_locations['my_transaction'] = (my_transaction_loc_left_x, my_transaction_loc_left_y, my_transaction_loc_right_x, my_transaction_loc_right_y)
    
    search_loc = search_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    search_loc_left_x =  search_loc[0][0]
    search_loc_left_y =  search_loc[0][1]
    search_loc_right_x = search_loc[1][0]
    search_loc_right_y = search_loc[1][1]
    all_locations['search_loc'] = (search_loc_left_x, search_loc_left_y, search_loc_right_x, search_loc_right_y)
    
    gizmo_loc = gizmo_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    gizmo_loc_left_x =  gizmo_loc[0][0]
    gizmo_loc_left_y =  gizmo_loc[0][1]
    gizmo_loc_right_x = gizmo_loc[1][0]
    gizmo_loc_right_y = gizmo_loc[1][1]
    all_locations['gizmo_loc'] = (gizmo_loc_left_x, gizmo_loc_left_y, gizmo_loc_right_x, gizmo_loc_right_y)
    
    gizmo_drop_loc = gizmo_drop_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    gizmo_drop_loc_left_x =  gizmo_drop_loc[0][0]
    gizmo_drop_loc_left_y =  gizmo_drop_loc[0][1]
    gizmo_drop_loc_right_x = gizmo_drop_loc[1][0]
    gizmo_drop_loc_right_y = gizmo_drop_loc[1][1]
    all_locations['gizmo_drop_loc'] = (gizmo_drop_loc_left_x, gizmo_drop_loc_left_y, gizmo_drop_loc_right_x, gizmo_drop_loc_right_y)

    gizmo_exotic_loc = gizmo_exotic_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    gizmo_exotic_loc_left_x =  gizmo_exotic_loc[0][0]
    gizmo_exotic_loc_left_y =  gizmo_exotic_loc[0][1]
    gizmo_exotic_loc_right_x = gizmo_exotic_loc[1][0]
    gizmo_exotic_loc_right_y = gizmo_exotic_loc[1][1]
    all_locations['gizmo_exotic_loc'] = (gizmo_exotic_loc_left_x, gizmo_exotic_loc_left_y, gizmo_exotic_loc_right_x, gizmo_exotic_loc_right_y)

    current_transaction_buy_loc = current_transaction_buying_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    current_transaction_buy_loc_left_x =  current_transaction_buy_loc[0][0]
    current_transaction_buy_loc_left_y =  current_transaction_buy_loc[0][1]
    current_transaction_buy_loc_right_x = current_transaction_buy_loc[1][0]
    current_transaction_buy_loc_right_y = current_transaction_buy_loc[1][1]
    all_locations['current_transaction_buy'] = (current_transaction_buy_loc_left_x, current_transaction_buy_loc_left_y, current_transaction_buy_loc_right_x, current_transaction_buy_loc_right_y)

    current_transaction_sell_loc = current_transaction_selling_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    current_transaction_sell_loc_left_x =  current_transaction_sell_loc[0][0]
    current_transaction_sell_loc_left_y =  current_transaction_sell_loc[0][1]
    current_transaction_sell_loc_right_x = current_transaction_sell_loc[1][0]
    current_transaction_sell_loc_right_y = current_transaction_sell_loc[1][1]
    all_locations['current_transaction_sell'] = (current_transaction_sell_loc_left_x, current_transaction_sell_loc_left_y, current_transaction_sell_loc_right_x, current_transaction_sell_loc_right_y)

    transaction_cancel_locations = []
    transaction_cancels_locs = transaction_cancels_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    for elem in transaction_cancels_locs:
        transaction_cancels_loc_left_x =  elem[0][0]
        transaction_cancels_loc_left_y =  elem[0][1]
        transaction_cancels_loc_right_x = elem[1][0]
        transaction_cancels_loc_right_y = elem[1][1]
        #cv2.rectangle(scr, (transaction_cancels_loc_left_x, transaction_cancels_loc_left_y), (transaction_cancels_loc_right_x, transaction_cancels_loc_right_y), (0,255,255), 2)
        transaction_cancel_locations.append((transaction_cancels_loc_left_x, transaction_cancels_loc_left_y, transaction_cancels_loc_right_x, transaction_cancels_loc_right_y))
    all_locations['transaction_cancel_locations'] = transaction_cancel_locations
    
    buy_individual_item_locations_list = []
    buy_individual_item_locs = buy_individual_item_locations(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    for elem in buy_individual_item_locs:
        buy_individual_item_loc_left_x =  elem[0][0]
        buy_individual_item_loc_left_y =  elem[0][1]
        buy_individual_item_loc_right_x = elem[1][0]
        buy_individual_item_loc_right_y = elem[1][1]
        #cv2.rectangle(scr, (buy_individual_item_loc_left_x, buy_individual_item_loc_left_y), (buy_individual_item_loc_right_x, buy_individual_item_loc_right_y), (255,0,255), 2)
        buy_individual_item_locations_list.append((buy_individual_item_loc_left_x, buy_individual_item_loc_left_y, buy_individual_item_loc_right_x, buy_individual_item_loc_right_y))
    all_locations['buy_individual_item_locations'] = buy_individual_item_locations_list
    
    instantly_loc = instantly_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    instantly_loc_left_x =  instantly_loc[0][0]
    instantly_loc_left_y =  instantly_loc[0][1]
    instantly_loc_right_x = instantly_loc[1][0]
    instantly_loc_right_y = instantly_loc[1][1]
    all_locations['instantly_loc'] = (instantly_loc_left_x, instantly_loc_left_y, instantly_loc_right_x, instantly_loc_right_y)

    instantly_gold_loc = instantly_gold_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    instantly_gold_loc_left_x =  instantly_gold_loc[0][0]
    instantly_gold_loc_left_y =  instantly_gold_loc[0][1]
    instantly_gold_loc_right_x = instantly_gold_loc[1][0]
    instantly_gold_loc_right_y = instantly_gold_loc[1][1]
    all_locations['instantly_gold_loc'] = (instantly_gold_loc_left_x, instantly_gold_loc_left_y, instantly_gold_loc_right_x, instantly_gold_loc_right_y)
    
    instantly_silver_loc = instantly_silver_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    instantly_silver_loc_left_x =  instantly_silver_loc[0][0]
    instantly_silver_loc_left_y =  instantly_silver_loc[0][1]
    instantly_silver_loc_right_x = instantly_silver_loc[1][0]
    instantly_silver_loc_right_y = instantly_silver_loc[1][1]
    all_locations['instantly_silver_loc'] = (instantly_silver_loc_left_x, instantly_silver_loc_left_y, instantly_silver_loc_right_x, instantly_silver_loc_right_y)
    
    instantly_bronze_loc = instantly_bronze_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    instantly_bronze_loc_left_x =  instantly_bronze_loc[0][0]
    instantly_bronze_loc_left_y =  instantly_bronze_loc[0][1]
    instantly_bronze_loc_right_x = instantly_bronze_loc[1][0]
    instantly_bronze_loc_right_y = instantly_bronze_loc[1][1]
    all_locations['instantly_bronze_loc'] = (instantly_bronze_loc_left_x, instantly_bronze_loc_left_y, instantly_bronze_loc_right_x, instantly_bronze_loc_right_y)
    
    trading_icon_loc = trading_icon_location(take_all_top_left_x, take_all_top_left_y, take_all_bottom_right_x, take_all_bottom_right_y)
    trading_icon_left_x =  trading_icon_loc[0][0]
    trading_icon_left_y =  trading_icon_loc[0][1]
    trading_icon_right_x = trading_icon_loc[1][0]
    trading_icon_right_y = trading_icon_loc[1][1]
    all_locations['trading_icon_loc'] = (trading_icon_left_x, trading_icon_left_y, trading_icon_right_x, trading_icon_right_y)

    #cv2.rectangle(scr, (delivery_box_top_left_x, delivery_box_top_left_y), (delivery_box_bottom_right_x, delivery_box_bottom_right_y), (255,255,0), 2)
#    cv2.rectangle(scr, (gizmo_loc_left_x, gizmo_loc_left_y), (gizmo_loc_right_x, gizmo_loc_right_y), (0,255,255), 2)
#    cv2.rectangle(scr, (gizmo_exotic_loc_left_x, gizmo_exotic_loc_left_y), (gizmo_exotic_loc_right_x, gizmo_exotic_loc_right_y), (0,255,255), 2)
#    cv2.rectangle(scr, (gizmo_drop_loc_left_x, gizmo_drop_loc_left_y), (gizmo_drop_loc_right_x, gizmo_drop_loc_right_y), (0,255,255), 2)
#    cv2.rectangle(scr, (take_all_top_left_x, take_all_top_left_y), (take_all_bottom_right_x, take_all_bottom_right_y), (0,255,255), 2)
#    cv2.rectangle(scr, (buy_loc_left_x, buy_loc_left_y), (buy_loc_right_x, buy_loc_right_y), (255,0,255), 2)
#    cv2.rectangle(scr, (sell_loc_left_x, sell_loc_left_y), (sell_loc_right_x, sell_loc_right_y), (255,255,0), 2)
#    cv2.rectangle(scr, (my_transaction_loc_left_x, my_transaction_loc_left_y), (my_transaction_loc_right_x, my_transaction_loc_right_y), (255,255,255), 2)
#    cv2.rectangle(scr, (search_loc_left_x, search_loc_left_y), (search_loc_right_x, search_loc_right_y), (255,255,0), 2)
#    cv2.rectangle(scr, (current_transaction_buy_loc_left_x, current_transaction_buy_loc_left_y), (current_transaction_buy_loc_right_x, current_transaction_buy_loc_right_y), (255,0,255), 2)
#    cv2.rectangle(scr, (current_transaction_sell_loc_left_x, current_transaction_sell_loc_left_y), (current_transaction_sell_loc_right_x, current_transaction_sell_loc_right_y), (0,0,255), 2)
#    cv2.rectangle(scr, (instantly_loc_left_x, instantly_loc_left_y), (instantly_loc_right_x, instantly_loc_right_y), (255,0,255), 2)
#    cv2.rectangle(scr, (instantly_gold_loc_left_x, instantly_gold_loc_left_y), (instantly_gold_loc_right_x, instantly_gold_loc_right_y), (255,0,255), 2)
#    cv2.rectangle(scr, (instantly_silver_loc_left_x, instantly_silver_loc_left_y), (instantly_silver_loc_right_x, instantly_silver_loc_right_y), (255,0,255), 2)
#    cv2.rectangle(scr, (instantly_bronze_loc_left_x, instantly_bronze_loc_left_y), (instantly_bronze_loc_right_x, instantly_bronze_loc_right_y), (255,0,255), 2)
#    cv2.rectangle(scr, (trading_icon_left_x, trading_icon_left_y), (trading_icon_right_x, trading_icon_right_y), (255,0,255), 2)
#
#    cv2.imshow('highlights', scr)
#    cv2.waitKey()
#    cv2.destroyAllWindows() 
    
    return all_locations

def load_data():
    current_buy_items = {}
    with open("current_buy_items_serialize.json", "r") as outfile:
        current_buy_items = json.load(outfile)

    remove_items = {}
    with open("remove_items_serialize.json", "r") as outfile:
        remove_items = json.load(outfile)

    what_to_buy_items = {}
    with open("what_to_buy_items_serialize.json", "r") as outfile:
        what_to_buy_items = json.load(outfile)

    item_lookups = {}
    with open("item_lookup_serialize.json", "r") as outfile:
        item_lookups = json.load(outfile)
        
    return (current_buy_items, remove_items, what_to_buy_items, item_lookups)
    
def middle_location(loc):
    top_left_x, top_left_y, bottom_left_x, bottom_left_y = loc
    middle_offset_x = (bottom_left_x - top_left_x) / 2
    middle_offset_y = (bottom_left_y - top_left_y) / 2
    return (top_left_x + middle_offset_x, top_left_y + middle_offset_y)
    
    
def click_take_all(all_locations):
    top_loc, left_loc = middle_location(all_locations['take_all'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def click_my_transactions(all_locations):
    top_loc, left_loc = middle_location(all_locations['my_transaction'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def click_search(all_locations):
    top_loc, left_loc = middle_location(all_locations['search_loc'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def click_buy_items(all_locations):
    top_loc, left_loc = middle_location(all_locations['buy_loc'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def click_gizmo(all_locations):
    top_loc, left_loc = middle_location(all_locations['gizmo_loc'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def click_gizmo_drop(all_locations):
    top_loc, left_loc = middle_location(all_locations['gizmo_drop_loc'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def click_gizmo_exotic(all_locations):
    top_loc, left_loc = middle_location(all_locations['gizmo_exotic_loc'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def click_sell_items(all_locations):
    top_loc, left_loc = middle_location(all_locations['sell_loc'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def click_buy_individual_item_locations(all_locations, idx):
    top_loc, left_loc = middle_location(all_locations['buy_individual_item_locations'][idx])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def move_instantly_gold(all_locations):
    top_loc, left_loc = middle_location(all_locations['instantly_gold_loc'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    
def move_instantly_silver(all_locations):
    top_loc, left_loc = middle_location(all_locations['instantly_silver_loc'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    
def move_instantly_bronze(all_locations):
    top_loc, left_loc = middle_location(all_locations['instantly_bronze_loc'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    
def click_instantly_transact(all_locations):
    top_loc, left_loc = middle_location(all_locations['instantly_loc'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def click_trading_post(all_locations):
    top_loc, left_loc = middle_location(all_locations['trading_icon_loc'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def click_current_transaction_buy(all_locations):
    top_loc, left_loc = middle_location(all_locations['current_transaction_buy'])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    
def click_transaction_cancel_locations(all_locations, idx):
    top_loc, left_loc = middle_location(all_locations['transaction_cancel_locations'][idx])
    pyautogui.moveTo(top_loc, left_loc, 2, pyautogui.easeInOutQuad)
    pyautogui.click()

def click_login_gw2():
    pyautogui.moveTo(492, 719, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    pyautogui.click()
    pyautogui.click()

def click_character_gw2():
    pyautogui.moveTo(746, 985, 2, pyautogui.easeInOutQuad)
    pyautogui.click()
    pyautogui.click()
    pyautogui.click()
    
def start_gw2():
    subprocess.Popen(["D:\ProgramFiles\Guild Wars 2\Gw2-64.exe"])

def kill_gw2():
    os.system("taskkill /f /im  Gw2-64.exe")

def buy_item_flow(all_locations, what_to_buy_items, item_lookups):
    
    press_o(1)
    time.sleep(1)
    press_o(1)

    account_money = account_wallet_coin()

    click_trading_post(all_locations)
    time.sleep(2)
    click_take_all(all_locations)
    time.sleep(2)
    click_buy_items(all_locations)
    time.sleep(10)
    click_gizmo(all_locations)
    time.sleep(2)
    click_gizmo_drop(all_locations)
    time.sleep(2)
    click_gizmo_exotic(all_locations)
    time.sleep(2)
    click_gizmo(all_locations)
    time.sleep(10)

    for itemID in what_to_buy_items:
        
        if item_lookups[itemID]['maxBuy'] > account_money - REMAINING_GOLD_NEEDED:
            print("account_money: " + str(account_money) + " buying: " + str(item_lookups[itemID]['name']) + " current buying price: " + str(item_lookups[itemID]['maxBuy']))
            continue
        
        click_search(all_locations)
        
        pyautogui.click()
        pyautogui.click()
        pyautogui.click()
        backspace(1)
        
        newItemBuyPrice = item_lookups[itemID]['maxBuy'] + 1000
        
        gold, silver, bronze = break_money_down(str(newItemBuyPrice))
        account_money = account_money - (item_lookups[itemID]['maxBuy'] + 1)
        
        itemID = str(itemID)
        print("buying: " + item_lookups[itemID]['name'] + " current buying price: " + str(item_lookups[itemID]['maxBuy']))
        pyautogui.write(item_lookups[itemID]['name'], interval=0)
        press_enter(1)

        time.sleep(4)

        click_buy_individual_item_locations(all_locations, 0)
        
        time.sleep(2)
        
        move_instantly_gold(all_locations)
        pyautogui.click()
        pyautogui.click()
        backspace(1)
        pyautogui.write(str(gold), interval=0)

        move_instantly_silver(all_locations)
        pyautogui.click()
        pyautogui.click()
        backspace(1)
        pyautogui.write(str(silver), interval=0)
        
#        move_instantly_bronze(all_locations)
#        pyautogui.click()
#        pyautogui.click()
#        backspace(1)
#        pyautogui.write(str(bronze), interval=0)
        
        click_instantly_transact(all_locations)
        click_my_transactions(all_locations)
        press_one(1)

def remove_item_flow(all_locations, remove_items, item_lookups):
    
    press_o(1)
    time.sleep(1)
    press_o(1)

    click_trading_post(all_locations)
    click_my_transactions(all_locations)
    click_current_transaction_buy(all_locations)
    
    for items in remove_items:
        
        click_search(all_locations)
        
        pyautogui.click()
        pyautogui.click()
        pyautogui.click()
        backspace(1)
        
        print("removing: " + items['name'])
        
        pyautogui.write(items['name'], interval=0)
        press_enter(1)
        
        click_transaction_cancel_locations(all_locations, 0)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        
        click_my_transactions(all_locations)
        press_one(1)


    click_take_all(all_locations)
    time.sleep(2)

def sell_item_flow(all_locations, item_lookups):
    
    press_o(1)
    time.sleep(1)
    press_o(1)

    items_bought = requests.get(url = ITEM_BOUGHT_URL).json()

    click_trading_post(all_locations)
    time.sleep(2)
    click_take_all(all_locations)
    time.sleep(2)
    click_sell_items(all_locations)
    time.sleep(10)
    
    for item in items_bought:
        item_id = str(item['item_id'])
        
        if item_id in item_lookups:
            purchased_date = datetime.strptime(item['purchased'], '%Y-%m-%dT%H:%M:%S%z')
            one_day_from_now = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=2)
            
            if purchased_date > one_day_from_now:

                click_search(all_locations)
                
                pyautogui.click()
                pyautogui.click()
                pyautogui.click()
                backspace(1)

                pyautogui.write(item_lookups[item_id]['name'], interval=0)
                press_enter(1)
                
                sell_item_price = min((item_lookups[item_id]['minSell']-TARGET_DISCOUNT), item['price']+TARGET_PROFIT)
                print(str(item_lookups[item_id]) + " " + str(sell_item_price))
                
                click_buy_individual_item_locations(all_locations, 0)
                
                
                gold, silver, bronze = break_money_down(str(sell_item_price))
                
                move_instantly_gold(all_locations)
                pyautogui.click()
                pyautogui.click()
                backspace(1)
                pyautogui.write(str(gold), interval=0)

                move_instantly_silver(all_locations)
                pyautogui.click()
                pyautogui.click()
                backspace(1)
                pyautogui.write(str(silver), interval=0)
                
                move_instantly_bronze(all_locations)
                pyautogui.click()
                pyautogui.click()
                backspace(1)
                pyautogui.write(str(bronze), interval=0)
                
                click_instantly_transact(all_locations)
                click_sell_items(all_locations)
                press_one(1)

def start_guild_wars2_program():
    start_gw2()
    time.sleep(30)
    start_gw2()
    time.sleep(30)
    click_login_gw2()
    time.sleep(60)
    click_character_gw2()
    time.sleep(180)
    press_f(1)
    time.sleep(30)
    press_one(1)
    time.sleep(30)
    
def start_gw_trade():
    all_locations = build_all_locations()
    remove_items, what_to_buy_items, item_lookups = autotrader.refresh_all_items()
#    remove_items, what_to_buy_items, item_lookups = load_data()
    try:
        buy_item_flow(all_locations, what_to_buy_items, item_lookups)
        remove_item_flow(all_locations, remove_items, item_lookups)
#        sell_item_flow(all_locations, item_lookups)
    except:
        print('something went wrong!')

def run_trade_forever():
    while True:
        start_gw_trade()

def start():

    start_gw_trade()
    kill_gw2()
    
    while True:
        start_guild_wars2_program()
        
        for i in range(5):
            try:
                start_gw_trade()
            except:
                continue
     
        kill_gw2()

def on_press(key):
    if key == keyboard.Key.f1:
        try:
            start()
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
    if key == keyboard.Key.f2:
        try:
            run_trade_forever()
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
    if key == keyboard.Key.f3:
        try:
            print (pyautogui.position())
            print('stop {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
    if key == keyboard.Key.f4:
        try:
            refresh_take_all_location()
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

def on_release(key):
    if key == keyboard.Key.esc:
        quit()
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()