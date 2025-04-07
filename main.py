import time
import logging
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

caminho_chromedriver = ChromeDriverManager().install()

service = Service(caminho_chromedriver)
driver = webdriver.Chrome(service=service)

# Configuração do logging
logging.basicConfig(
    filename="log.txt", 
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logging.info("Iniciando o script...")

# Acessar a página
url = "https://vasco.eleventickets.com/#!/home"
driver.get(url)
logging.info(f"Acessando a página: {url}")

def type_keys(text):
    actions = ActionChains(driver)
    actions.send_keys(text)
    actions.perform()

def bot_tab():
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB)
    actions.perform()

def bot_enter():
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()

# Função para enviar e-mail
def enviar_email(assunto, mensagem):
    remetente = "demobruta@gmail.com"
    destinatario = "alexandrermello@hotmail.com"
    senha = "onwxxqvqigzgxjiv"  # Senha de aplicativo gerada no Google #@A1

    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
        logging.info(f"E-mail enviado: {assunto}")
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail: {e}")

time.sleep(10)
# Aceitar cookies
try:
    wait = WebDriverWait(driver, 10)
    botao_aceitar_cookies = wait.until(
        EC.element_to_be_clickable((By.ID, "textBtn"))
    )
    botao_aceitar_cookies.click()
    print("✅ Botão 'ACEITAR TODOS OS COOKIES' clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no botão 'ACEITAR TODOS OS COOKIES': {e}")

time.sleep(3)
try:
    wait = WebDriverWait(driver, 10)
    icone_perfil = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "md-icon[md-svg-src='img/svg/round58.svg']"))
    )
    icone_perfil.click()
    print("✅ Ícone de perfil clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no ícone de perfil: {e}")
try:
    wait = WebDriverWait(driver, 10)
    publico_geral_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[@style='background-color: rgb(0, 0, 0);']//p[text()='Público Geral - Jogos']"
        ))
    )
    publico_geral_btn.click()
    print("✅ Botão 'Público Geral - Jogos' clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no botão 'Público Geral - Jogos': {e}")

# Solicitar e-mail e senha do usuário via input
email_usuario = input("Digite seu e-mail: ")
senha_usuario = input("Digite sua senha: ")

# Digitar o e-mail e a senha
try:
    type_keys(email_usuario)  # Digita o e-mail informado pelo usuário
    bot_tab()  # Passa para o próximo campo
    type_keys(senha_usuario)  # Digita a senha informada pelo usuário
    bot_tab()  # Passa para o próximo campo
    bot_tab()
    bot_enter()
    time.sleep(3)
    print("✅ E-mail e senha inseridos com sucesso!")
except Exception as e:
    print(f"❌ Erro ao inserir o e-mail e senha: {e}")


time.sleep(50000)
driver.quit()
logging.info("Script finalizado, navegador fechado.")
