import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from locatorsLogin import LocatorsLogin

# Carrega as variáveis de ambiente
load_dotenv()
Orange = os.getenv('Orange')

class LoginPage:
    """
    Classe que representa a página de login do sistema OrangeHRM.
    Encapsula todas as ações possíveis na página de login e logout.
    """

    def __init__(self, driver):
        """Inicializa a página de login com o driver do navegador."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.url = f"{Orange}/web/index.php/auth/login"

    def open(self):
        """Abre a página de login."""
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.XPATH, LocatorsLogin.username)))

    def login(self, username, password):
        """Realiza o login com as credenciais fornecidas."""
        self.driver.find_element(By.XPATH, LocatorsLogin.username).send_keys(username)
        self.driver.find_element(By.NAME, LocatorsLogin.password).send_keys(password)
        self.driver.find_element(By.TAG_NAME, LocatorsLogin.submit).click()
        self.wait.until(lambda d: d.find_element(By.TAG_NAME, "body"))

    def is_dashboard_displayed(self):
        """Verifica se o dashboard foi exibido após login com sucesso."""
        return self.wait.until(EC.presence_of_element_located((By.XPATH, LocatorsLogin.dashboard))).is_displayed()

    def is_user_not_found_displayed(self):
        """Verifica se a mensagem de erro de login é exibida."""
        return self.wait.until(EC.presence_of_element_located((By.XPATH, LocatorsLogin.userNotfound))).is_displayed()

    def is_required_displayed(self):
        """Verifica se a mensagem de senha obrigatória é exibida."""
        return self.wait.until(EC.presence_of_element_located((By.XPATH, LocatorsLogin.required))).is_displayed()

    def logout(self):
        """Executa as ações para realizar o logout do sistema."""
        self.wait.until(EC.element_to_be_clickable((By.XPATH, LocatorsLogin.icon))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, LocatorsLogin.logout))).click()

    def is_logged_out(self):
        """Verifica se o usuário foi redirecionado para a tela de login após o logout."""
        return self.wait.until(EC.presence_of_element_located((By.XPATH, LocatorsLogin.layout))).is_displayed()


class TestLogin:

    def setup_method(self):
        """Configura o WebDriver antes de cada teste."""
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Descomente se quiser rodar sem abrir o navegador
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.login_page = LoginPage(self.driver)

    def teardown_method(self):
        """Encerra o WebDriver após cada teste."""
        self.driver.quit()

    def test_positive_login(self):
        """Verifica se o login com credenciais válidas é realizado com sucesso."""
        self.login_page.open()
        self.login_page.login("Admin", "admin123")
        assert self.login_page.is_dashboard_displayed()

    def test_login_invalid_registration(self):
        """Verifica se o sistema exibe mensagem de erro para login com usuário inválido."""
        self.login_page.open()
        self.login_page.login("Admi", "admin124")
        assert self.login_page.is_user_not_found_displayed()

    def test_login_special_characters(self):
        """Verifica se o sistema exibe erro ao tentar login com caracteres especiais."""
        self.login_page.open()
        self.login_page.login("@@@@", "admin124")
        assert self.login_page.is_user_not_found_displayed()

    def test_no_Password(self):
        """Verifica se é possível fazer um login sem inserir senha"""
        self.login_page.open()
        self.login_page.login("Admin", "")
        assert self.login_page.is_required_displayed()

    def test_logout(self):
        """Verifica se o logout é realizado com sucesso"""
        self.login_page.open()
        self.login_page.login("Admin", "admin123")
        self.login_page.logout()
        assert self.login_page.is_logged_out()
