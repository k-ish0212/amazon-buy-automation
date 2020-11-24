import os
import time
from os.path import join, dirname
from logger import logger as l
from selenium.common.exceptions import *
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LOGIN_MAIL = os.environ.get('LOGIN_MAIL', None)
LOGIN_PASSWORD = os.environ.get('LOGIN_PASSWORD', None)

ITEM_URL = os.environ.get('ITEM_URL', None)

ACCEPT_SHOP = 'Amazon.com'
#LIMIT_VALUE = 500    # Maximum USD for the purchase
LIMIT_VALUE = os.environ.get('LIMIT_VALUE', None) # Let's add this to the .env file



def login(chromeDriver):
    chromeDriver.find_element_by_id("nav-link-accountList").click()
    chromeDriver.find_element_by_id('ap_email').send_keys(LOGIN_MAIL)
    chromeDriver.find_element_by_id('continue').click()
    chromeDriver.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
    chromeDriver.find_element_by_id('signInSubmit').click()

def purchase_item(chromeDriver):
    chromeDriver.get(ITEM_URL)
    # Checks if out of stock, verify_stock returns False if not in stock
    l.info("Checking stock")
    if in_stock_check(chromeDriver): # removed not, as this was evaluating as true when item was not in stock
        return False
    # Checks price
    l.info("Checking price")
    if not verify_price_within_limit(chromeDriver):
        return False
    # Checks seller
    l.info("Checking seller")
    if not seller_check(chromeDriver):
        return False
    l.info("Clicking buy now")
    chromeDriver.find_element_by_id('buy-now-button').click()  # 1 click buy
    l.info("Placing order")
    chromeDriver.find_element_by_id('submitOrderButtonId-announce').click()
    #chromeDriver.find_element_by_id('placeYourOrder1').click()
    return True


def in_stock_check(chromeDriver):
    inStock = False
    try:
        #shop = chromeDriver.find_element_by_id('tabular-buybox-truncate-1').text  #this is not working for me - i dont see this element
        try:
            chromeDriver.find_element_by_id("outOfStock")
            l.info("Item is outOfStock")
            chromeDriver.refresh()
        except NoSuchElementException as e:
            try:
                chromeDriver.find_element_by_id("tabular-buybox-text")
                l.info("Item is in-stock!")
                inStock = True
            except NoSuchElementException as e:
                time.sleep(1)
                chromeDriver.refresh()
    finally:
        l.info("Item is in-stock!")
        return inStock

def seller_check(chromeDriver):
    element = chromeDriver.find_element_by_id('tabular-buybox-truncate-1').text
    l.info('element is: {}'.format(element))
    shop = element.find(ACCEPT_SHOP)
    l.info('shop is: {}'.format(shop))
    if shop == -1:
        raise Exception("Amazon is not the seller")
        return False
    l.info("Successfully verified Seller")
    return True

def verify_price_within_limit(chromeDriver):
    price = chromeDriver.find_element_by_id('priceblock_ourprice').text
    price = price.replace('$', '')
    price = float(price)
    # price = price.join()
    l.info('price of item is:  {}'.format(price))
    l.info('limit value is: {}'.format(float(LIMIT_VALUE)))
    # int_price = int(price.replace(' ', '').replace(',', '').replace('$', ''))
    # print(int_price)
    if price > float(LIMIT_VALUE):
        l.warn('PRICE IS TOO LARGE.')
        return False
    return True
