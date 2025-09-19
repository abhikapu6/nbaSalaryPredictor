from io import StringIO
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class wait_for_text_changed:
    def __init__(self, locator, current_text):
        self.locator = locator
        self.current_text = current_text

    def __call__(self, driver):
        return driver.find_element(*self.locator).text != self.current_text
def click_element(element):
    driver.execute_script("arguments[0].click();", element)

driver = webdriver.Chrome()

driver.get('https://www.hoopshype.com/salaries/players/?season=2014')
time.sleep(5)
html = driver.page_source
initial_pages = pd.read_html(StringIO(html), displayed_only=False)
table = initial_pages[0]


i = 0
while True:
    if i > 26:
        break
    button = driver.find_element(By.CSS_SELECTOR,"button.hd3Vfp__hd3Vfp._3JhbLM__3JhbLM")    
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    time.sleep(5) 
    click_element(button)
    time.sleep(10)
    html = driver.page_source
    next_pages = pd.read_html(StringIO(html), displayed_only=False)
    page_df = next_pages[0]
    table =  pd.concat([table, page_df], axis=0, ignore_index=True)
    i += 1


driver.quit()

table = table.drop(columns=['Unnamed: 0'])

# print(table)
# print(table.shape)
# print(table.columns)
table.to_csv('/Users/abhik/Desktop/contracts2015.csv', index=False)
print("I made the contracts file")
