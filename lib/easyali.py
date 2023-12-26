import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class AliException(Exception):
    
    pass


class EasyAli():
    
    '''
    Used to retrieve the price of a product from an AliExpress link.
    '''
    
    def __init__(self, **kwargs):

        if kwargs.get("docker_is_used", False):

            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-ssl-errors=yes')
            options.add_argument('--ignore-certificate-errors')
            
            self.driver = webdriver.Remote(
                command_executor='http://172.20.0.1:4444/wd/hub',
                options=options
            )

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
            price = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[9]/div/div[4]/div/div[1]/div[1]/div/div[2]/div[2]")
            f_price = price.text.replace(" ", "").replace("₽", "")
            return f_price
        except Exception as e:
            raise AliException(f"Can't get price from page: {link}. Exception info: {e.__str__()}")

    def calculate_from_json(self, json_data_str: str) -> float:

        data = json.loads(json_data_str)

        total_price = 0

        for el in data["elements"]:

            price = self.get_price_from_page(el["link"]) * el["count"]
            total_price += price

        return total_price