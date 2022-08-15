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
        drop_sql = 'TRUNCATE TABLE car_brands'
        drop_sql2 = 'TRUNCATE TABLE car_models'
        cursor.execute(drop_sql)
        cursor.execute(drop_sql2)
        connection.commit()


        i = 1
        for option in options:
            value = option.get_attribute('value')
            text = option.get_attribute('innerText')
            if value != '250' and value != '0' and value != '50':
                slug = text.replace(' ', '-')
                sql = "INSERT INTO `car_brands` (`name`, `slug`, `status`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (text,slug , 'active'))
                model_id = cursor.lastrowid
                option.click()

                sleep(5)

                models_options = driver.find_element(
                    By.ID, 'CarModelId').find_elements(By.TAG_NAME, 'option')
                if (len(models_options) == 2):
                    continue
                else:
                    years = []

                    for model_o in models_options:
                        model_value = model_o.get_attribute('value')
                        model_text = model_o.get_attribute('innerText')

                        if model_value != '0' and model_value != '50' and model_value != '250':
                            model_o.click()
                            sleep(5)
                            model_years = driver.find_element(By.ID, 'ModelYear').find_elements(By.TAG_NAME, 'option')
                            if len(model_years) != 2:
                                for my in model_years:
                                    year_value = my.get_attribute('value')
                                    if year_value != '0' and year_value != '50' and year_value != '250' :
                                        years.append(int(year_value))

                            years.sort()

                            model_sql = "INSERT INTO `car_models` (`car_brand_id`, `name`, `slug`, `year_from`, `year_to`, `is_jalali`, `status`) VALUES (%s, %s,  %s,  %s, %s, %s, %s)"
                            year_from = years[0]
                            year_to = years[len(years) -1 ]
                            is_jalali = '1' if year_from < 1700 else '0'
                            model_slug = model_text.replace(' ', '-')

                            cursor.execute(model_sql, (
                                model_id,
                                model_text,
                                model_slug,
                                year_from,
                                year_to,
                                is_jalali,
                                'active'
                                )
                            )

            print('imported number ' + str(i) + ' of : ' + str(len(options)))
            connection.commit()
            sleep(1)
            i += 1

driver.close
