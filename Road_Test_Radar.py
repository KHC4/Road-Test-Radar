import time
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import calendar
from selenium.webdriver.chrome.options import Options
import winsound
import datetime

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
# Change chrome driver path accordingly
chrome_driver = "chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

today = str(datetime.date.today())[8:]
second_month_check = False
if int(today) > 25:
    second_month_check = True

loc = ["Brampton", "Guelph", "Mississauga", "Orangeville", "Hamilton", "Brantford", "Kitchener"]
loc_id = {'Brampton': 'targetLoc2', 'Guelph': 'targetLoc7', 'Mississauga': 'targetLoc12', 'Orangeville': 'targetLoc15',
          'Hamilton': 'targetLoc8', 'Brantford': 'targetLoc3', 'Kitchener': 'targetLoc9'}


def login():
    f_email = open('data/email.txt', 'r')
    email = f_email.readline().strip()
    f = open('data/Current Student.txt', 'r')
    line = f.readline()
    data = line.split(', ')
    name = data[0]
    number = data[1]
    expiry = data[2]
    g = data[3] == 'G'
    if g:
        class_path = '//*[@id="headingDiv"]/div[3]/div[2]/label'
    else:
        class_path = '//*[@id="headingDiv"]/div[3]/div[1]/label'
    driver.find_element(By.ID, 'emailAddress').send_keys(email)
    driver.find_element(By.ID, 'confirmEmailAddress').send_keys(email)
    driver.find_element(By.ID, 'driverLicenceNumber').send_keys(number)
    driver.find_element(By.ID, 'driverLicenceExpiry').send_keys(expiry)
    driver.find_element(By.XPATH,
                        '//*[@id="booking-container"]/div/div[2]/form/div[5]/app-progress-button/button').click()
    licence_class = WebDriverWait(driver, 15).until(ec.presence_of_element_located((By.XPATH, class_path)))
    licence_class.click()
    continue_button = WebDriverWait(driver, 15).until(ec.presence_of_element_located(
        (By.XPATH, '//*[@id="headingDiv"]/div[5]/app-progress-button/button/span[1]/span')))
    continue_button.click()
    open_saturday = WebDriverWait(driver, 15).until(
        ec.presence_of_element_located((By.ID, 'openSaturdaysCheckBoxIsSelected')))
    open_saturday.click()


def set_location(selected):
    target_id = []
    for location in selected:
        target_id.append(loc[location])
    return selected


def check(selected_dates_month1, selected_dates_month2, location, month):
    try:
        WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.CSS_SELECTOR,
                                                                       'button.date-selection-coontainer.custom-date-selection-button.date-available')))
    except TimeoutException:
        return [True, []]

    dates = driver.find_elements(By.CSS_SELECTOR,
                                 'button.date-selection-coontainer.custom-date-selection-button.date-available')
    for date in dates:
        date.click()
        date_string = (date.get_attribute('aria-label').split())[2]
        date_int = int(date_string[:len(date_string) - 1])
        driver.find_element(By.XPATH,
                            '//*[@id="main"]/app-select-date/div/div[4]/app-progress-button/button/span[1]/span').click()
        try:
            times_available = WebDriverWait(driver, 3).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'app-time-widget')))
        except TimeoutException:
            pass

        times = driver.find_elements(By.CSS_SELECTOR, 'app-time-widget')
        if len(times) > 0:
            time_slots = [(slot.find_element(By.CSS_SELECTOR, 'button')).get_attribute('aria-label') for slot in times]
            if month == 1 and selected_dates_month1[date_int][0]:
                for time_slot in time_slots:
                    if location in selected_dates_month1[date_int][1].keys() and time_slot in \
                            selected_dates_month1[date_int][1][location]:
                        pass
                    else:
                        return [False, [location, time_slots, month, date_int]]
            elif month == 2 and selected_dates_month2[date_int][0]:
                for time_slot in time_slots:
                    if location in selected_dates_month2[date_int][1].keys() and time_slot in \
                            selected_dates_month2[date_int][1][location]:
                        pass
                    else:
                        return [False, [location, time_slots, month, date_int]]
    return [True, []]


def date_available(selected_dates_month1, selected_dates_month2):
    with open("data/selected_locations.txt", "r") as file:
        selected = [line.strip() for line in file]
    i = 0
    driver.find_element(By.ID, loc_id[selected[0]]).click()
    try:
        driver.find_element(By.XPATH,
                            '//*[@id="main"]/app-drivetest-locations/div/div/div[6]/app-progress-button/button').click()
    except Exception:
        driver.find_element(By.XPATH,
                            '//*[@id="main"]/app-drivetest-locations/div/div/div[5]/app-progress-button/button').click()
    a, b = check(selected_dates_month1, selected_dates_month2, selected[i], 1)
    while a:
        time.sleep(10)
        i = i % len(selected)
        try:
            js_code = "window.scrollTo(0, 0);"
            driver.execute_script(js_code)
            location = driver.find_element(By.ID, loc_id[selected[i]])
            location.click()
        except:
            handle_exception()
            return
        a, b = check(selected_dates_month1, selected_dates_month2, selected[i], 1)
        if second_month_check and a:
            driver.find_element(By.XPATH,
                                '//*[@id="main"]/app-select-date/div/app-calendar-selection-container/div[1]/button[2]/span[1]/mat-icon').click()
            a, b = check(selected_dates_month1, selected_dates_month2, selected[i], 2)
        i += 1

    play_alarm_sound()
    ignore_date(selected_dates_month1, selected_dates_month2, b)
    return b


def handle_exception():
    # Handle the exception here
    winsound.PlaySound('assets/shutdown.wav', winsound.SND_FILENAME | winsound.SND_NOWAIT)


def play_alarm_sound():
    # Play the alarm sound
    winsound.PlaySound('assets/alarm.wav', winsound.SND_FILENAME | winsound.SND_NOWAIT)


def ignore_date(selected_dates_month1, selected_dates_month2, found):
    result = messagebox.askyesno("Ignore Date", "Ignore this date?")
    print(found)
    if result:
        location = found[0]
        time_slots = found[1]
        month = found[2]
        date = found[3]
        if month == 1:
            if location in selected_dates_month1[date][1].keys():
                for time_slot in time_slots:
                    selected_dates_month1[date][1][location].add(time_slot)
            else:
                selected_dates_month1[date][1][location] = set(time_slots)
        else:
            if location in selected_dates_month2[date][1].keys():
                for time_slot in time_slots:
                    selected_dates_month2[date][1][location].add(time_slot)
            else:
                selected_dates_month2[date][1][location] = set(time_slots)
        pass


def restart():
    driver.get('https://drivetest.ca')
    book_button = WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="home-overview"]/div/div/div/div[10]/div/div/div/div[1]/a')))
    book_button.click()
    login()
