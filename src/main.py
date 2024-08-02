import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.selenium_operations import login, delete_all_leave_requests, set_new_leave_request
from src.excel_parser import get_non_working_periods_dict
from src.config import jira_url, jira_login, jira_password


opts = Options()
# opts.add_argument('headless')
# opts.add_argument('--disable-gpu')
# opts.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=opts)


def check_page_status(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f'Page status: {e}')


def main():
    if check_page_status(jira_url):
        try:
            input('press ENTER to start')
            non_working_periods_dict = get_non_working_periods_dict()
            if 'Invalid data' in non_working_periods_dict:
                input(f'{non_working_periods_dict}\nPress Enter to exit')
                return non_working_periods_dict
            driver.set_window_size(1920, 1080)
            driver.get(jira_url)
            if login(driver, jira_login, jira_password):
                try:
                    set_new_leave_request(driver, non_working_periods_dict)
                except Exception as e:
                    print(f'Error: {e}')
        finally:
            time.sleep(2)
            driver.quit()
            input('Press Enter to exit')
    else:
        print(f'page {jira_url} is not accessible')


if __name__ == '__main__':
    main()