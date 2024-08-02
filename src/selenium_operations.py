import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.excel_parser import date_in

# from config import url_parts

locators = {
    'username_field': (By.NAME, 'os_username'),
    'password_field': (By.NAME, 'os_password'),
    'leave_button': (By.ID, 'Leave'),
    'search_date_field': (By.ID, 'search-date'),
    'delete_buttons': (By.XPATH, '//*[@id="delete-button"]'),
    'new_leave_request_button': (By.ID, 'new-absence-button'),
    'leave_period_field': (By.CLASS_NAME, 'el-input__inner'),
    'ok_button': (By.CLASS_NAME, 'el-input__icon.el-icon-time'),
    'user_field': (By.CLASS_NAME, 'select2-container.aui-select2-container'),
    'select_search': (By.CLASS_NAME, 'select2-input.select2-focused'),
    'select2_drop': (By.XPATH, '//*[@id="select2-drop"]/ul'),
    'first_result': (
        By.CSS_SELECTOR,
        'li.select2-results-dept-1.select2-result.select2-result-selectable.select2-highlighted'),
    'submit_request_button': (By.ID, 'submit-absence-request')
}

url_parts = {
    'login_url': 'login',
    'roster_url': 'secure/RosterIndexAction',
    'absence_url': 'absence/',
    'absence_new_url': 'absence/new'
}


def current_url_check(driver, c_url: str) -> bool:
    return c_url in driver.current_url


def login(driver, jira_login, jira_password) -> bool:
    """
    Jira login
    """
    try:
        username_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(locators['username_field'])
        )
        username_field.clear()
        username_field.send_keys(jira_login)

        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(locators['password_field'])
        )
        password_field.clear()
        password_field.send_keys(jira_password)
        password_field.send_keys(Keys.ENTER)
        return True
    except Exception as e:
        print(f'login error {e}')
        return False


def delete_all_leave_requests(driver) -> str:
    """
    delete all Leave Requests
    start: excel_parsing.date_in
    end: end
    """
    if current_url_check(driver, url_parts['roster_url']):
        leave_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(locators['leave_button'])
        )
        leave_button.click()
    if current_url_check(driver, url_parts['absence_url']):
        search_date_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(locators['search_date_field'])
        )
        search_date_field.clear()
        search_date_field.send_keys(date_in.str_date)
        search_date_field.send_keys(Keys.TAB)
        deleted_count = 1
        while True:
            if current_url_check(driver, url_parts['absence_url']):
                try:
                    delete_buttons = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(locators['delete_buttons'])
                    )
                except:
                    print('delete_button не найдена. Обновление страницы...')
                    delete_buttons = []
                if not delete_buttons:
                    try:
                        driver.refresh()
                        print('Страница обновлена')
                        search_date_field = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located(locators['search_date_field'])
                        )
                        search_date_field.clear()
                        search_date_field.send_keys(date_in.str_date)
                        search_date_field.send_keys(Keys.TAB)
                        print(f'Дата {date_in.str_date} установлена')
                        time.sleep(5)
                        delete_buttons = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located(locators['delete_buttons'])
                        )
                    except:
                        print('delete_buttons не найдены')
                if delete_buttons:
                    delete_buttons[0].click()
                    print(f'Исключение:{deleted_count} удалено')
                    deleted_count += 1
                    time.sleep(2)
                else:
                    return 'Удаление выполнено.'


def set_new_leave_request(driver, non_working_periods_dict: dict) -> None:
    """
    Create new Leave Requests
    start: date_in
    end: new_month
    """
    if current_url_check(driver, url_parts['roster_url']):
        leave_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(locators['leave_button'])
        )
        leave_button.click()
    # test_count
    count = 0
    for user in non_working_periods_dict:
        for day in non_working_periods_dict[user]:
            if current_url_check(driver, url_parts['absence_url']):
                WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, 'aui-message-success'))
                )
                # xpath // *[ @ id = "aui-flag-container"] / div / div
                new_leave_request_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, 'new-absence-button'))
                )
                new_leave_request_button.click()

                if current_url_check(driver, url_parts['absence_new_url']):
                    leave_period_field = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(locators['leave_period_field'])
                    )
                    leave_period_field.clear()
                    leave_period_field.send_keys(day)
                    leave_period_field.click()

                    ok_button = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(locators['ok_button'])
                    )
                    ok_button.click()

                    user_field = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(locators['user_field'])
                    )
                    user_field.click()

                    select_search = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(locators['select_search'])
                    )

                    select_search.clear()
                    select_search.send_keys(user)

                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located(locators['select2_drop'])
                    )

                    first_result = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(locators['first_result'])
                    )
                    first_result.click()

                    submit_request_button = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(locators['submit_request_button'])
                    )
                    submit_request_button.click()
                    print(f'{user}: {day} ADDED')
                    count += 1
                    time.sleep(5)
