from selenium import webdriver
import time


def gatherdetails(max_price, max_kilo):
    global timesRun
    firstsave = True if timesRun == 1 else False
    # scroll to the first post
    firstad = browser.find_element_by_xpath('//div[@class="feeditem table"]')
    browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'})", firstad)
    ## sleeping few seconds to load the page
    time.sleep(2)
    post = 1
    for feed in browser.find_elements_by_xpath('//div[@class="feeditem table"]'):
        if post <= 20:
            time.sleep(1)
            feed.click()
            post += 1
            time.sleep(1.5)
            try:
                car_kilo = int(feed.find_element_by_xpath('.//dd[@id="more_details_kilometers"]/span').text)
                car_price = feed.find_element_by_xpath('.//div[@data-test-id="item_price"]').text
            except Exception:
                print('Loading was too long, could not retrieve the data from post, moving to next')
                feed.find_element_by_xpath('*//div/div').click()
                browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'})", feed)
                continue
            ## price recived '27,800 ₪', so seperating the number from the symbol..
            car_price = car_price.split()
            car_price = int(car_price[0].replace(',', ''))
            ## if its worthy, return True, then add to whishlist
            if calculator(max_price, max_kilo, car_price, car_kilo):
                addwhishlist(feed)
                if firstsave:
                    time.sleep(2)
                    understand = browser.find_element_by_xpath(
                        '*//button[@class="y2-button y2-raised y2-primary left_button"]')
                    browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'})", understand)
                    print(understand.text)
                    understand.click()
                    time.sleep(0.5)
                    browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'})", feed)
                    firstsave = False
                time.sleep(0.3)
            timesRun += 1
            ##close post##
            feed.find_element_by_xpath('*//div/div').click()
            # scrolling to the next#
            browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'})", feed)


def calculator(m_price, m_kilo, price, kilo):
    # first if is to avoid fake posts
    if price > 1_000 and kilo > 1_000:
        if price / m_price <= 0.85 and kilo / m_kilo <= 0.9:
            return True
        elif price / m_price <= 0.75:
            return True
        elif kilo / m_kilo <= 0.65:
            return True
    else:
        return False
    return False


def addwhishlist(feed):
    feed.find_element_by_xpath('.//button[@class="like_icon"]').click()


###### there is many sleeping functions because the site and posts must load so the code won't break ######
print("""
Please enter 'https://www.yad2.co.il/vehicles/private-cars', filter out your results as you wish.
*Note please mark image & price only and paste the URL\n
""")
url = str(input("You may enter '0' for default link in order to use test link: ") or '0')
if '0' == url:
    url = 'https://www.yad2.co.il/vehicles/private-cars?year=2010--1&price=-1-28000&km=10000-100000&ownerID=1&gearBox=1&imgOnly=1&priceOnly=1'
if 'yad2' not in url:
    print('invalid URL.. exiting..')
    exit()
print(f"Link chosen: {url}")
pages = int(input("How many pages to search? \n *less than 0 will automatically choose 1: ") or 1)
if pages < 1:
    pages = 1
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
browser = webdriver.Chrome('./chromedriver', options=chrome_options)
max_price = 28000
max_kilo = 100_000
## reset page in case page is already given ##
if 'page=' in url:
    print("Reseting page.. starting from page 1...")
    url = url.split('&')
    del url[-1]
    url = '&'.join(url)
url = url + '&page=0'
timesRun = 1
for page in range(1, pages + 1):
    url = url.replace('&page={}'.format(page - 1), '&page={}'.format(page))
    browser.get(url=url)
    time.sleep(3)
    if browser.current_url != url:
        print("Please go to yad2.co.il and solve the captcha")
        browser.quit()
        exit()
    print(f"going over page {page}")
    gatherdetails(int(max_price), int(max_kilo))
time.sleep(2)
print("finished.. heading to wishlist page.. best of luck!")
browser.find_element_by_xpath('*//li[@class="header_favorite"]/a').click()
