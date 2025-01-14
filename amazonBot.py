from http.client import PAYMENT_REQUIRED
import os
import sys
import time
from random import randint
import re

from dotenv import load_dotenv
from logger import logger as l
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from amazoncaptcha import AmazonCaptcha
import pdb

load_dotenv(verbose=True)
dotenv_path = '.env'
load_dotenv(dotenv_path)

LOGIN_MAIL = os.environ.get('LOGIN_MAIL', "")
LOGIN_PASSWORD = os.environ.get('LOGIN_PASSWORD', "")

ITEM_URL = os.environ.get('ITEM_URL', "")

CHECKOUT_URL = "https://www.amazon.co.jp/gp/cart/view.html?ref_=nav_cart"
PAYMENT_URL = "https://www.amazon.co.jp/gp/buy/payselect/handlers/display.html?_from=cheetah"
SUBMIT_URL = "https://www.amazon.co.jp/gp/buy/spc/handlers/display.html?hasWorkingJavascript=1"

ACCEPT_SHOP = "amazon"
LIMIT_VALUE = int(os.environ.get('LIMIT_VALUE', "")) # Maximum Yen for the purchase

# class GracefulKiller:
#   kill_now = False
#   def __init__(self):
#     signal.signal(signal.SIGINT, self.exit_gracefully)
#     signal.signal(signal.SIGTERM, self.exit_gracefully)

#   def exit_gracefully(self, *args):
#     self.kill_now = True

def login(chromeDriver):
    chromeDriver.find_element_by_id("nav-link-accountList").click()
    chromeDriver.find_element_by_id('ap_email').send_keys(LOGIN_MAIL)
    chromeDriver.find_element_by_id('continue').click()
    chromeDriver.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
    chromeDriver.find_element_by_id('signInSubmit').click()
    l.info("Successfully logged in")


def validate_captcha(chromeDriver):
    time.sleep(1)
    l.info("Solving CAPTCHA")
    chromeDriver.get('https://www.amazon.com/errors/validateCaptcha')
    captcha = AmazonCaptcha.fromdriver(chromeDriver)
    solution = captcha.solve()
    chromeDriver.find_element_by_id('captchacharacters').send_keys(solution)
    chromeDriver.find_element_by_class_name('a-button-text').click()
    time.sleep(1)


def purchase_item(chromeDriver):
    # Logs in and purchases the item
    login(chromeDriver)
    
    l.info("Starting purchase process...")
    # Checks if out of stock, price is right, and shipper is amazon keeps waiting if not in stock (for a random amount of time as to not get banned)
    while not in_stock_check(chromeDriver) or not verify_price_within_limit(chromeDriver): # or not seller_check(chromeDriver):
        l.info("Could not purchase desired item...waiting for stock/pricing/seller")
        sleep = randint(15, 90)
        l.info(f"Sleeping for {sleep} seconds...")
        time.sleep(sleep)
        chromeDriver.refresh()

    # # Logs in and purchases the item
    # login(chromeDriver)

    # Solve Captcha
    # validate_captcha(chromeDriver)

    if not checkout(chromeDriver):
        return False
    time.sleep(1)
    if not go_to_order(chromeDriver):
        return False
    time.sleep(1)
    if not submit_order(chromeDriver):
        return False
    return True


def in_stock_check(chromeDriver):
    l.info("Checking stock...")
    inStock = False

    try:
        if chromeDriver.find_element_by_id("corePriceDisplay_desktop_feature_div").text: #("sns-base-price").text:
            l.info("Item is in-stock!")
            inStock = True
        else:
            try:
                chromeDriver.find_element_by_id("outOfStock")
                l.info("Item is outOfStock")
                chromeDriver.refresh()
                inStock = False
            except:
                l.warn("Item is out of stock!")
    except Exception as e:
        l.error('Error checking stock: {}'.format(e))

    finally:
        return inStock


def seller_check(chromeDriver):
    l.info("Checking shipper...")
    element = chromeDriver.find_element_by_id("tabular-buybox-truncate-0").text
    shop = element.lower().find(ACCEPT_SHOP)
    if shop == -1:
        l.warn("Amazon is not the seller/shipper")
        return False
    else:
        l.info(f"Successfully verified shipper as: {element}")
        return True


def verify_price_within_limit(chromeDriver):
    try:
        price = re.sub(r"\D", "", chromeDriver.find_element("xpath", '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]/span[2]').text)
    except Exception as e:
        l.error('Error verifying price: {}'.format(e))
        return False

    l.info(f'price of item is: {price}')
    l.info('limit value is: {}'.format(float(LIMIT_VALUE)))

    if float(price.replace('$', '')) > LIMIT_VALUE:
        l.warn('PRICE IS TOO LARGE.')
        return False

    return True


def checkout(chromeDriver):
    l.info("Checking out...")
    chromeDriver.get(ITEM_URL)

    try:
        WebDriverWait(chromeDriver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='buy-now-button']"))).click() # "//input[@name='proceedToRetailCheckout']"))).click()
        return True

        
        
    except Exception as e:
        l.warn(f"Could not add order: {e}")
    return False

def go_to_order(chromeDriver):
    l.info("proceed to order...")
    chromeDriver.get(PAYMENT_URL)
    try:
        WebDriverWait(chromeDriver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='orderSummaryPrimaryActionBtn']/span/input"))).click()
        time.sleep(1)
        return True

    except Exception as e:
        l.warn(f"Could not place card select on order: {e}") 

    return False

def submit_order(chromeDriver):
    chromeDriver.get(SUBMIT_URL)
    try:
        WebDriverWait(chromeDriver, 3).until(
            
            EC.element_to_be_clickable((By.XPATH, "//input[@name='placeYourOrder1']"))).click()
    except Exception as e:
        l.warn(f"Try: , Could not place order: {e}")
        

def checkout_1click(chromeDriver):
    l.info("Buy now with 1-click")
    chromeDriver.find_element_by_id('buy-now-button').click()
    l.info("Confirming order")
    chromeDriver.find_element_by_name('placeYourOrder1').click()
