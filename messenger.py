from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# retrieving urls from this week's edition
soup = BeautifulSoup(requests.get("https://www.economist.com/weeklyedition/2021-09-04").text, "html.parser")

matching_elements = soup.find_all(attrs={"class" : ["weekly-edition-wtw__link", "headline-link"]})

urls = list(elem["href"] for elem in matching_elements)

# getting emails to send from and send to
with open('private_details.txt') as f:
    send_to_email = f.readline().rstrip()
    send_from_email = f.readline().rstrip()

# sending articles to kindle
options = Options()
options.headless = True
browser = webdriver.Chrome(options=options)

base_url = "https://pushtokindle.fivefilters.org/send.php?src=safari-app&url="
browser.get(base_url + "https://google.com")
time.sleep(2)
browser.find_element_by_xpath(r'//*[@id="contentIdForA11y3"]/div/div[4]/div/input').send_keys(send_to_email)
time.sleep(2)
browser.find_element_by_xpath(r'//*[@id="contentIdForA11y3"]/div/div[5]/div/input').send_keys(send_from_email)

for url in urls[::-1]:
    browser.get(base_url + "https://economist.com" + url)
    time.sleep(5)
    send_button = browser.find_element_by_xpath(r'//*[@id="app"]/div[1]/div[4]/div[2]/button')
    browser.execute_script("arguments[0].click();", send_button)
    time.sleep(10)
    print(url)

browser.quit()
