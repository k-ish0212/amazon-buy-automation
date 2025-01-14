# coding: utf-8

from logger import logger
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import chromedriver_binary

import amazonBot
import sys
import pdb

def launch():
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}

    opt = webdriver.ChromeOptions()
    # opt.add_argument('--disable-xss-auditor')
    # opt.add_argument('--disable-web-security')
    # opt.add_argument('--disable-dev-shm-usage')
    # opt.add_argument('--allow-running-insecure-content')
    # opt.add_argument('--remote-debugging-port=921')
    # opt.add_argument('--disable-webgl')
    # opt.add_argument('--disable-popup-blocking')

    # opt.add_argument('--no-sandbox')
    # opt.add_argument('--disable-gpu')
    # opt.add_argument('--window-size=1920,1080')

    # opt.add_argument('--headless')

    browser = webdriver.Chrome('chromedriver', options=opt, desired_capabilities=d)
    # opt.add_argument("--user-data-dir=selenium") # added this option to use cookies, you may need to perform initial login within Selenium
    browser.implicitly_wait(10)
    browser.set_page_load_timeout(5)
    logger.info('Started Chrome')

    return browser

if __name__ == '__main__':
    logger.info('Starting App')

    # Launch selenium
    try:
        b = launch()
        b.get(amazonBot.ITEM_URL)
    except Exception as inst:
        logger.error('Failed to open browser: {}'.format(format(inst)))
        logger.error('!!! Exiting App !!!')
        sys.exit(100)

    # Item purchasing logic
    try:
        done = False
        while(not done):
            try:
                # Navigate to the item and buy if checks pass
                if amazonBot.purchase_item(b):
                    done = True
                    logger.info("Successfully purchased item!!!!")
                    pdb.set_trace()
            except Exception as e:
                logger.error('{}'.format(e))
                logger.error('!!! Exiting App !!!')
                sys.exit(101)
    finally:
        logger.info('Closing Chromium')
        try:
            b.close()
        except BaseException:
            pass
        logger.info('Closed Chromium')

    logger.info('End of app')
