from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from scrape import go_scrape
import time
import os


def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def scan_carplate_data(carplate: str,
                       chrome_options: Options,
                       url: str) -> str:
    """Main function of the scraper.
    Takes the death numbers from the given webpage for
    official statistics.
    The web site might change in time. Hence,
    the operations applied in sequence:
    1. Find the element by ID in the given webpage with 'tarih'.
    2. Click on the search button
    3. Extract the data from the redirected URL
    """
    try:
        localdriver = bool(os.environ.get("LOCAL_DRIVER", False))
        driver = webdriver.Chrome(options=chrome_options)
        if localdriver:
            driver = webdriver.Chrome(
                '/home/vjaguilera/Documents/personal/tech/chilean-carplate-scrap-api/chromedriver',
                options=chrome_options)
        print("WEB DRIVER", driver)
        driver.set_window_size(800, 600)
        print("WEB DRIVER WINDOW", driver)
        driver.get(url)
        print("WEB DRIVER NEW URL", driver)
        time.sleep(2)

        ss = bool(os.environ.get("SCREENSHOT", False))
        if ss:
            driver.get_screenshot_as_file("screenshot.png")
        date_element = driver.find_element(By.ID, "txtTerm")
        print("WEB DRIVER ELEMENT", date_element)
        date_element.send_keys(carplate)
        date_element.send_keys(Keys.ENTER)
        time.sleep(2)
        # Scrpa the data
        page_source = driver.page_source
        data = go_scrape(page_source)
        print("DATA", data)
        return data
    except Exception as shit:
        print(f"{shit} happened.")
        return None
    finally:
        driver.quit()


def take_death_number(date_str: str,
                      chrome_options: Options,
                      url: str) -> str:
    """Main function of the scraper.
    Takes the data from the carplate website and scrape it.
    The web site might change in time. Hence, the operations applied in sequence:
    1. Find the search element by ID
    2. Enter the date as text in the given element ID.
    3. Gets the text from the class element 'tablePagination'"""
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(800, 600)
        driver.get(url)
        time.sleep(5)
        date_element = driver.find_element_by_id("tarih")
        date_element.send_keys(date_str)
        date_element.send_keys(Keys.ENTER)
        time.sleep(5)
        pagination = driver.find_element_by_class_name("tablePagination")
        return pagination.text
    except Exception as shit:
        print(f"{shit} happened.")
        return None
    finally:
        driver.quit()
