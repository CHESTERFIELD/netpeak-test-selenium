from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from faker import Faker
import time
import logging
import random

# opts = Options()
# opts.headless = True # без графического интерфейса.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()

def to_fill_input_by_xpath(driver, xpath, obj):
    ''' The input element that to find by xpath to fill obj.value. '''
    input = driver.find_element_by_xpath(xpath)
    if obj == "0123456789":
        input.send_keys(Keys.ARROW_LEFT)
    input.send_keys(obj)
    time.sleep(1)

def to_fill_select_by_name(driver, name, min, max):
    ''' The select element that to find by name to select random choice by index.'''
    select = Select(driver.find_element_by_name(name))
    select.select_by_index(random.randint(min, max))
    time.sleep(1)

def func():
    try:
        logging.info('Application - Start')
        host = "https://netpeak.ua/"
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        driver.implicitly_wait(20)
        # driver = webdriver.Chrome(options=opts)

        driver.get(host)
        assert "Netpeak" in driver.title

        # xpath to element "a" with attr href 'https://career.netpeak.ua/'
        career_element_button = driver.find_element_by_xpath(
                            "//a[@href='https://career.netpeak.ua/']"
                            )

        career_element_button.click()

        # copy xpath in browsers
        work_in_netpeak_button = driver.find_element_by_xpath(
                            "/html/body/div[5]/div/div/div[5]/div/a"
                            )
        work_in_netpeak_button.click()

        input_field = driver.find_element_by_xpath("/html/body/form/div[1]/div/div[1]/div[8]/div[1]/input")

        driver.execute_script("arguments[0].type = 'file';", input_field)

        input_field.send_keys("/home/chesterfield/Desktop/MishchenkoNikita.jpg")

        # driver.find_element_by_xpath("//*[@id='upload']").click()

        # upload_error_element = WebDriverWait(driver, 10).until(
        #                 EC.text_to_be_present_in_element((By.XPATH, "/html/body/form/div[1]/div/div[1]/div[8]/div[2]/label"),
        #                 "Ошибка: неверный формат файла (разрешённые форматы: doc, docx, pdf, txt, odt, rtf)." ))

        # if (upload_error_element.text == "Ошибка: неверный формат файла (разрешённые форматы: doc, docx, pdf, txt, odt, rtf)."):
        #     print("Error upload cv. The file`s format incorrect. ")

        time.sleep(1)

        # to fill first_name
        to_fill_input_by_xpath(driver, '//*[@id="inputName"]', fake.first_name())
        # to fill last_name
        to_fill_input_by_xpath(driver, '//*[@id="inputLastname"]', fake.last_name())
        # to fill email
        to_fill_input_by_xpath(driver, '//*[@id="inputEmail"]', fake.email())
        # to fill phone_number
        to_fill_input_by_xpath(driver, '//*[@id="inputPhone"]', "0123456789")

        # to choice birthday
        to_fill_select_by_name(driver, "bd", 1, 31)
        to_fill_select_by_name(driver, "bm", 1, 12)
        to_fill_select_by_name(driver, "by", 1, 59)

        # click submit button "SEND FORM"
        driver.find_element_by_xpath("//*[@id='submit']").click()

        time.sleep(1)

        element_p = driver.find_element_by_xpath("/html/body/div[2]/div/p")
        color = element_p.get_attribute('color')

        print(color)

        if color == 'red':
            print("Element 'Все поля являются обязательными для заполнения' is red.")


        driver.find_element_by_xpath("//img[@alt='Netpeak']").click()

        if WebDriverWait(driver, 10).until(EC.url_to_be(host)):
            print("You on landing page.")
    except AssertionError:
        print("'Netpeak' not find in driver title")
    except TimeoutException:
        print("Element 'Ошибка: неверный формат файла (разрешённые форматы: doc, docx, pdf, txt, odt, rtf).' not found.")
    finally:
        driver.close()
        driver.quit()
        logging.info('Application - End')


func()
