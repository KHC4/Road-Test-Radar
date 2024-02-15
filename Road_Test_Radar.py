from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import winsound
import datetime

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
# Change chrome driver path accordingly
chrome_driver = "chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

today = str(datetime.date.today())[8:]
next_month = False
if int(today) > 25:
    next_month = True

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
    time.sleep(5)
    driver.find_element(By.XPATH, class_path).click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="headingDiv"]/div[5]/app-progress-button/button/span[1]/span').click()
    time.sleep(5)
    driver.find_element(By.ID, 'openSaturdaysCheckBoxIsSelected').click()


def set_location(selected):
    target_id = []
    for location in selected:
        target_id.append(loc[location])
    return selected


def check_times():
    times = driver.find_elements(By.CSS_SELECTOR, 'app-time-widget')
    if times:
        return [True, [slot.get_attribute('aria-label') for slot in times]]
    return [False, []]


def check(ignored_dates):
    dates = driver.find_elements(By.CSS_SELECTOR,
                                 'button.date-selection-coontainer.custom-date-selection-button.date-available')
    for date in dates:
        date.click()
        driver.find_element(By.XPATH,
                            '//*[@id="main"]/app-select-date/div/div[4]/app-progress-button/button/span[1]/span').click()
        time.sleep(3)
        value = check_times()
        if value[0]:
            if [date.get_attribute('aria-label'), value[1]] in ignored_dates:
                pass
            else:
                return [False, [date.get_attribute('aria-label'), value[1]]]
    return [True, []]


def date_available(ignored):
    with open("data/selected_locations.txt", "r") as file:
        selected = [line.strip() for line in file]
    i = 0
    driver.find_element(By.ID, loc_id[selected[0]]).click()
    driver.find_element(By.XPATH,
                        '//*[@id="main"]/app-drivetest-locations/div/div/div[6]/app-progress-button/button').click()
    time.sleep(3)
    value = check(ignored)
    a = value[0]
    b = value[1]
    while a:
        i = i % len(selected)
        try:
            driver.find_element(By.ID, loc_id[selected[i]]).click()
        except:
            handle_exception()
            return
        time.sleep(5)
        i += 1
        value = check(ignored)
        a = value[0]
        b = value[1]
        if next_month and a:
            driver.find_element(By.XPATH,
                                '//*[@id="main"]/app-select-date/div/app-calendar-selection-container/div[1]/button[2]/span[1]/mat-icon').click()
            time.sleep(3)
            value = check(ignored)
            a = value[0]
            b = value[1]

    play_alarm_sound()
    ignore_date(ignored, b)
    return b


def handle_exception():
    # Handle the exception here
    winsound.PlaySound('assets/shutdown.wav', winsound.SND_FILENAME | winsound.SND_NOWAIT)


def play_alarm_sound():
    # Play the alarm sound
    winsound.PlaySound('assets/alarm.wav', winsound.SND_FILENAME | winsound.SND_NOWAIT)


def ignore_date(ignored, found):
    result = messagebox.askyesno("Ignore Date", "Ignore this date?")
    print(result)
    if result:
        ignored.append(found)
