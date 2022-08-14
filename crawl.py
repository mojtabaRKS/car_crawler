from pyexpat import model
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pymysql.cursors


url = 'http://bama.ir/sell/car'

driver = webdriver.Chrome(
    "/home/mojtaba/Projects/bama_crawler/chromedriver_linux64/chromedriver")

driver.get(url)
options = driver.find_element(
    By.ID, "CarBrandID").find_elements(By.TAG_NAME, 'option')

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='',
                             cursorclass=pymysql.cursors.DictCursor)


with connection:
    with connection.cursor() as cursor:
        for option in options:
            value = option.get_attribute('value')
            text = option.get_attribute('innerText')
            if value != 250 or value != 0:
                sql = "INSERT INTO `car_brands` (`name`, `slug`, `status`) VALUES (%s, %s)"
                cursor.execute(sql, (text, text.replace(' ', '-'), 'active'))
                model_id = cursor.lastrowid
                option.click()
                sleep(5)

                models_options = driver.find_element(
                    By.ID, 'CarModelId').find_elements(By.TAG_NAME, 'option')
                if (len(models_options) == 2):
                    continue
                else:
                    i = 0
                    year_from = 0
                    year_to = 0
                    for model_o in models_options:
                        model_value = option.get_attribute('value')
                        model_text = option.get_attribute('innerText')

                        if model_value != 0 or model_value != 50 or model_value != 250:
                            model_o.click()
                            sleep(5)
                            sql = "INSERT INTO `car_models` (`car_brand_id`, `name`, `slug`, `year_from`, `year_to`, `is_jalali`, `status`) VALUES (%s, %s,  %s,  %s, %s, %s, %s)"
                            cursor.execute(
                                sql, (model_id, text, text.replace(' ', '-'), ,'active'))

                        i += 1

            sleep(2)


driver.close
