import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from locatorsLogin import LocatorsLogin

# Carrega as variáveis de ambiente
load_dotenv()
Orange = os.getenv('Orange')


class TestLogin:
    def setup_method(self):
        '''Configuração do driver antes de cada teste'''
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Modo sem interface gráfi
        self.driver = webdriver.Chrome(options=chrome_options)

    def teardown_method(self):
        '''Finaliza o driver após cada teste'''
        self.driver.quit()

    def test_positiveLogin(self):
        '''Verifica se é possível fazer um login com sucesso'''
        self.driver.get(f"{Orange}/web/index.php/auth/login")
        time.sleep(3)
        self.driver.find_element(By.XPATH, LocatorsLogin.username).send_keys('Admin')
        self.driver.find_element(By.NAME, LocatorsLogin.password).send_keys("admin123")
        self.driver.find_element(By.TAG_NAME, LocatorsLogin.submit).click()
        time.sleep(2)
        assert self.driver.find_element(By.XPATH, LocatorsLogin.dashboard).is_displayed()

    def test_loginInvalidRegistration(self):
        '''Verifica se é possível fazer um login com matrícula inválida'''
        self.driver.get(f"{Orange}/web/index.php/auth/login")
        time.sleep(3)
        self.driver.find_element(By.XPATH, LocatorsLogin.username).send_keys('Admi')
        self.driver.find_element(By.NAME, LocatorsLogin.password).send_keys("admin124")
        self.driver.find_element(By.TAG_NAME, LocatorsLogin.submit).click()
        time.sleep(4)
        assert self.driver.find_element(By.XPATH, LocatorsLogin.userNotfound).is_displayed()

    def test_loginSpecialCharacters(self):
        '''Verifica se é possível fazer um login com caracteres especiais'''
        self.driver.get(f"{Orange}/web/index.php/auth/login")
        time.sleep(3)
        self.driver.find_element(By.XPATH, LocatorsLogin.username).send_keys('@@@@')
        self.driver.find_element(By.NAME, LocatorsLogin.password).send_keys("admin124")
        self.driver.find_element(By.TAG_NAME, LocatorsLogin.submit).click()
        time.sleep(4)
        assert self.driver.find_element(By.XPATH, LocatorsLogin.userNotfound).is_displayed()

    def test_LogOut(self):
        '''Verifica se é possível fazer logout com sucesso'''
        self.driver.get(f"{Orange}/web/index.php/auth/login")
        time.sleep(4)
        self.driver.find_element(By.XPATH, LocatorsLogin.username).send_keys('Admin')
        self.driver.find_element(By.NAME, LocatorsLogin.password).send_keys("admin123")
        self.driver.find_element(By.TAG_NAME, LocatorsLogin.submit).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, LocatorsLogin.dashboard).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, LocatorsLogin.icon).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, LocatorsLogin.logout).click()
        time.sleep(4)
        assert self.driver.find_element(By.XPATH, LocatorsLogin.layout).is_displayed()
