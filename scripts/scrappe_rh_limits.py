# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 17:25:44 2021

@author: tlcal
"""
import time
from datetime import datetime
#import numpy as np
#import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import mysql.connector
from mysql.connector import Error

### variables 
DRIVER_PATH = 'C:\\Users/tlcal/Documents/Robinhood-stocks/other/chromedriver.exe'
rh_stock_limit_website = 'https://robinhood.com/us/en/support/articles/changes-due-to-recent-market-volatility/'



options = Options()
options.add_argument("--start-maximized")
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
driver.get(rh_stock_limit_website)
time.sleep(2)

val = [] #will contain all the rows to be inserted in database

### new version timestamp will be used through MySQL
#now = datetime.now()
#time_updated = now.strftime("%d-%m-%Y %H:%M:%S")

for table in driver.find_elements_by_xpath('//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[3]/div[3]/div[2]/span/table/tbody'):
    #rows = table.find_elements_by_xpath('//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[3]/div[3]/div[2]/span/table/tbody/tr[1]')
    rows = [item for item in table.find_elements_by_xpath(".//*[self::tr or self::tr]")]
    for row in rows:
        column = [col for col in row.find_elements_by_xpath(".//*[self::td or self::td]")]
        #for col in column:
            #print(col.text)
        #val_aux = (column[0].text, column[1].text, column[2].text, time_updated)
        val_aux = (column[0].text.replace(",", "."), column[1].text.replace(",", "."), column[2].text.replace(",", "."))
        
        #print(val_aux)
        val.append(val_aux)
    #print(rows)

#print(val)

#get element with longest height on page (this has to be done manually)
ele=driver.find_element("xpath", '//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[3]')

total_height = ele.size["height"]
driver.set_window_size(1920, total_height)      #the trick

time.sleep(1)

timestr = time.strftime("%Y%m%d-%H%M%S")

#save full page screenshot
driver.save_screenshot('../screenshots/screenshot_{0}.png'.format(timestr))

driver.quit() #close chrome

time.sleep(1)

#print(val)
print("Executed at: {}".format(timestr))

### insert data in database ###

try:
    ### MySQL variables 
    connection = mysql.connector.connect(host='localhost',
                                         database='robinhood_stocks',
                                         user='root',
                                         password='1234')

    sql_query = "INSERT INTO robinhood_stocks.stock_limits (company_code, shares_limit, contract_options, datetime_update) VALUES (%s, %s, %s, now())"

    cursor = connection.cursor()
    result = cursor.executemany(sql_query, val)
    connection.commit()
    print("Records inserted successfully ")
    print(cursor.rowcount, "records were inserted.")
    
except mysql.connector.Error as error:
    print("Failed to insert records in MySQL: {}".format(error))
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("Success: MySQL connection is closed")    
        
