from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
import requests
import time
import itertools


zillow_url = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.90711440039063%2C%22east%22%3A-121.95954359960938%2C%22south%22%3A37.4265788314989%2C%22north%22%3A38.12236702051197%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLScxSwZpD-sn-lvjZCRYZO09bpHa5ATR5-2NAcu-uedg6-03aQ/viewform?usp=sf_link"

chrome_driver_path = "/Users/Jasper/Developer/ChromeDriver/chromedriver"
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("detach", True)
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)


# SELENIUM ATTEMPT
driver.get(zillow_url)
time.sleep(10)

listing_info_list = []

sublist_a = []
sublist_b = []
sublist_c = []

master_list = []


try:
    list_of_links = driver.find_elements(By.CSS_SELECTOR, "article div div div a")
    list_of_addresses = driver.find_elements(By.CSS_SELECTOR, "div a address")
    print(f"address list test: \n{list_of_addresses}")
    list_of_prices = driver.find_elements(By.CSS_SELECTOR, "span[data-test='property-card-price']")


    time.sleep(1)

    for (link, address, price) in zip(list_of_links, list_of_addresses, list_of_prices):
        # listing_urls.append(listing)
        link_ = link.get_attribute("href")
        print(f"Link: {link_}")
        address_ = address.text.split("| ", 2)[-1]
        print(f"Address: {address_}")
        price_ = price.text.replace('+', '/').split("/", 2)[0]
        print(f"Price: {price_}")
        listing_info_list.append((link_, address_, price_))
        # driver.execute_script("argument[0].scrollIntoView(true);", list_of_links[-1])
        time.sleep(1)

    print(listing_info_list)

except Exception as e:
    print(f"\nException: \n{e}\n\n")


# FOR TESTING
# listing_info_list = [("link test", "address test", "price test"), ("link test 2", "address test 2", "price test 2")]

# Post Info to Google Form

"""driver.get(google_form_url)
time.sleep(3)
entry_fields = driver.find_elements(By.CSS_SELECTOR, "div div div input[class='whsOnd zHQkBf']")"""
# entry_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div')

for link, address, price in listing_info_list:
    driver.get(google_form_url)
    time.sleep(3)
    entry_fields = driver.find_elements(By.CSS_SELECTOR, "div div div input[class='whsOnd zHQkBf']")

    print(f"Link: {link}")
    print(f"Address: {address}")
    print(f"Price: {price}")

    iter_num = 0
    for field in entry_fields:
        if iter_num == 0:
            field.send_keys(address)
            time.sleep(.25)
            field.send_keys(Keys.TAB, price)
            time.sleep(.25)
            field.send_keys(Keys.TAB, Keys.TAB, link)
            time.sleep(.25)
            submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
            submit_button.click()
            time.sleep(.25)
            iter_num += 1
        else:
            pass

    # submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    # submit_button.click()
    # time.sleep(1)

driver.close()
print("\n\nProcess complete!")

"""for a, b, c in entry_fields:
    a.send_keys(link)
    b.send_keys(address)
    c.send_keys(price)"""

