import time
from selenium import webdriver

PAGE_URL = "http://orteil.dashnet.org/experiments/cookie/"
TIMEOUT = 300
CHECK_INTERVAL = 5

driver = webdriver.Chrome()
driver.get(PAGE_URL)
cookie = driver.find_element_by_id("cookie")
item_list = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in item_list]

def buy_upgrade():
    cookies = int(driver.find_element_by_id("money").text.replace(",", ""))
    raw_prices = driver.find_elements_by_css_selector("#store b")
    prices = [int(price.text.split("-")[1].strip().replace(",", "")) for price in raw_prices if price.text != ""]

    upgrades = {prices[n]: item_ids[n] for n in range(len(prices))}
    purchasable_upgrades = {cost: id for cost, id in upgrades.items() if cookies > cost}

    if purchasable_upgrades:
        driver.find_element_by_id(purchasable_upgrades[max(purchasable_upgrades)]).click()

start_time = time.time()
end_time = start_time + TIMEOUT
check_time = start_time + CHECK_INTERVAL

while time.time() < end_time:
    cookie.click()
    if time.time() > check_time:
        buy_upgrade()
        check_time += CHECK_INTERVAL

cps = driver.find_element_by_id("cps").text
print(f"Exited after {TIMEOUT} seconds with a score of {cps.split(' : ')[1]} cookies per second.")
driver.close()
