import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import logging
logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(filename='/logs/easyali.log', filemode='w+')

class AliException(Exception):
    
    pass


class EasyAli():
    
    '''
    Used to retrieve the price of a product from an AliExpress link.
    '''
    
    def __init__(self, **kwargs):

        if kwargs.get("docker_is_used", False):

            options = webdriver.ChromeOptions()
            #options.add_argument("--headless=true")
            #options.add_argument("--disable-gpu")
            # options.add_argument("--dns-prefetch-disabled")
            #options.add_argument("--blink-settings=imagesEnabled=false")
            options.add_argument('--ignore-ssl-errors=yes')
            options.add_argument('--ignore-certificate-errors')

            selenium_host = "selenium"
            selenium_port = 4444

            url = f"http://{selenium_host}:{selenium_port}/wd/hub"
            
            max_attempts = 10
            for attempt in range(max_attempts):
                try:
                    self.driver = webdriver.Remote(command_executor=url, options=options)
                    logging.debug("Соединение с Selenium успешно установлено")
                    break
                except Exception as e:
                    logging.debug(f"Ошибка при попытке подключения к Selenium (попытка {attempt + 1}/{max_attempts}): {e}")
                    time.sleep(5)  # Подождем 5 секунд перед следующей попыткой
            else:
                raise RuntimeError("Не удалось подключиться к Selenium после нескольких попыток")


        else:
            
            self.driver = webdriver.Chrome()

    def __del__(self):

        if hasattr(self, 'driver'):
            
            self.driver.quit()
            #self.driver.close()

    def navigate(self, link):

        self.driver.get(link)
    
    def get_price_from_page(self, link) -> float:
        
        '''
        Return's price by aliexpress link.
        Arguments:
            link: str - link to product
        Return:
            float - price
        Raises:
            AliException
        '''
        
        try:
            self.navigate(link)
            try:
                price = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[9]/div/div[4]/div/div[1]/div[1]/div/div[2]/div[2]")
            except:
                price = self.driver.find_element(By.XPATH, "//*[@id=\"__aer_root__\"]/div/div[9]/div/div[4]/div/div[1]/div[1]/div/div/div[2]")
            f_price = price.text.replace(" ", "").replace("₽", "")
            return f_price
        except Exception as e:
            raise AliException(f"Can't get price from page: {link}. Exception info: {e.__str__()}")

    def calculate_from_json(self, json_data_str: str):

        logging.debug(f"Json input: {json_data_str}")

        data = json.loads(json_data_str)

        total_price = 0
        errors = ""

        for el in data["elements"]:

            try:
                price = int(self.get_price_from_page(el["link"])) * el["count"]
                total_price += price
            except AliException as e:
                errors += e.__str__()

        return total_price, errors