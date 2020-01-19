from selenium import webdriver
import time


def gatherdetails(max_price, max_kilo):
    ## sleeping few seconds to load the page
    time.sleep(4)
    global timesRun
    firstime = True if timesRun == 1 else False
    # gather detailes from the post
    height = '9900'
    browser.execute_script("window.scrollTo(0,{})".format(height))
    ##sleeping to load the first post
    time.sleep(3)
    post = 0
    for feed in browser.find_elements_by_xpath('//div[@class="feeditem table"]'):
        if post <= 20:
            feed.click()
            post += 1
            time.sleep(3)
            # car_year = feed.find_element_by_xpath('.//div[@class="data"]/span').text
            car_name = feed.find_element_by_xpath('.//div[@class="rows"]/span[@class="title"]').text
            car_kilo = int(feed.find_element_by_xpath('.//dd[@id="more_details_kilometers"]/span').text)
            car_price = feed.find_element_by_xpath('.//div[@data-test-id="item_price"]').text
            ## price recived '27,800 ₪', so seperating the number from the symbol..
            car_price = car_price.split()
            car_price = int(car_price[0].replace(',', ''))
            ## if its worthy, return True, then add to whishlist
            if calculator(max_price, max_kilo, car_price, car_kilo):
                addwhishlist(feed)
                time.sleep(2)
                if firstime:
                    browser.find_element_by_xpath(
                        '*//button[@class="y2-button y2-raised y2-primary left_button"]').click()
                    timesRun += 1
                    firstime = False
            # closing post and moving to the next
            feed.find_element_by_xpath('*//div/div').click()
            height = str(int(height) - 100)
            browser.execute_script("window.scrollTo(0,{})".format(height))
            time.sleep(1)


def calculator(max_price, max_kilo, price, kilo):
    # max_price, max_kilo, price, kilo, year = [int(i) for i in input().split()]
    if price / max_price <= 0.85 and kilo / max_kilo <= 0.9:
        return True
    elif price / max_price <= 0.75:
        return True
    elif kilo / max_kilo <= 0.65:
        return True
    else:
        return False


def addwhishlist(feed):
    feed.find_element_by_xpath('.//button[@class="like_icon"]').click()

###### there is many sleeping functions because the site and posts must load so the code won't break ######
print("""
Please enter 'https://www.yad2.co.il/vehicles/private-cars', filter out your results as you wish.
Mark Image&Price only and paste the URL :      
""")
url = str(input("You may enter '0' for default link in order to use test link: "))
if '0' == url:
    url = 'https://www.yad2.co.il/vehicles/private-cars?year=2010--1&price=-1-28000&km=10000-100000&ownerID=1&gearBox=1&imgOnly=1&priceOnly=1'
pages = int(input("How many pages to search?: "))
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
browser = webdriver.Chrome('./chromedriver', options=chrome_options)
max_price = 28000
max_kilo = 100_000
url = url + '&page=0'
timesRun = 1
for page in range(1, pages + 1):
    url = url.replace('&page={}'.format(page - 1), '&page={}'.format(page))
    browser.get(url=url)
    time.sleep(3)
    print(f"going over page {page}")
    gatherdetails(int(max_price), int(max_kilo))
time.sleep(2)
print("finished.. heading to wishlist page.. best of luck!")
browser.find_element_by_xpath('*//li[@class="header_favorite"]/a').click()
