# Amazon Purchase Script 

**Use at your own risk. Read thoroughly**

Example: script to buy a PS5 on Amazon (Please do not use this script for scalping, this is simply a free open source solution for those that want a console but are unable to get one due to market competitiveness)

forked from yosh1/amazon-automation

Development: 
--- 
## TODO: 
Detect when Amazon sends to captcha by detecting for text on the captcha page. After detecting, call the `validate_captcha` function. 

Requirements: 
--- 
* Python 3 
* Python modules in `requirements.txt` 
* [WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads) in same directory 

Recommended to be run on Linux or Max. Would be a good script to run on a raspberry pi or server

Notes of caution: 
--- 

Things to check for on Amazon/potential edge cases: 

 * Amazon 2FA (an option is to disable but this will **expose your account to security problems**)
 * ~~Currently uses 1 click buy. Confirm your default address + payments is correct before running this script~~
 * 1 Click buy sometimes did not work for me, so I used the "Add to cart method". I left the 1-click-buy-method in if you want to use that instead.
 * Captchas for hitting Amazon's server a lot

--- 

## Logic/Behavior: 
 
 1. Starts Selenium 
 2. Loops the following until all attributes of the item are correct: 
    1. Verifies item is in stock 
    2. Verifies the price is less than the set maximum
    3. Checks to make sure the shipper is from Amazon.com 
        
        *NOTE: I used shipper instead of seller because quite a few items are not actually sold by Amazon.* **Change this on a case by case basis**
4. Logs in 
5. Adds to cart 
6. Checks out  
 

Sample Log: 

    [26/Nov/2020 19:37:36] INFO - Started Chrome
    [26/Nov/2020 19:37:39] INFO - Starting purchase process...
    [26/Nov/2020 19:37:39] INFO - Checking stock...
    [26/Nov/2020 19:37:39] INFO - Item is in-stock!
    [26/Nov/2020 19:37:39] INFO - price of item is:  $39.99
    [26/Nov/2020 19:37:39] INFO - Checking shipper...
    [26/Nov/2020 19:37:39] INFO - Successfully verified shipper as: Amazon
    [26/Nov/2020 19:37:39] INFO - Logging in as ayang25@gmail.com
    [26/Nov/2020 19:37:41] INFO - Checking out...
    [26/Nov/2020 19:37:57] INFO - Placed order!
    [26/Nov/2020 19:37:57] INFO - Successfully purchased item

Testing notes: 
 * Confirmed loops when item is not in stock 
 * Does not buy when shipper/price are incorrect! 
 * Buys when instock and seller/price are correct 

---

## Copy `.env`

```
$ cp .env.sample .env
```


## Run

```
$ pip install -r requirements.txt 
$ python3 main.py
```

Alternatively use Docker: 

```
$ docker-compose build
$ docker-compose up -d
```

