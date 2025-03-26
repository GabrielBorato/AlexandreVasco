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

caminho_chromedriver = r"C:\Users\gabriel.borato\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

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
url = "https://ingressos.flamengo.com.br/"
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

def limpar_campo_email():
    # Clicar no campo de e-mail
    campo_login.click()
    # Selecionar tudo (Ctrl + A)
    actions = ActionChains(driver)
    actions.send_keys(Keys.CONTROL + "a")  # Ctrl + A para selecionar tudo
    actions.perform()
    # Apagar tudo (Backspace)
    actions.send_keys(Keys.BACKSPACE)
    actions.perform()
    logging.info("Campo de e-mail limpo com sucesso!")


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
    botao_concordo = wait.until(
        EC.element_to_be_clickable((By.ID, "setCookies"))
    )
    botao_concordo.click()
    print("✅ Botão 'Concordo' clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no botão: {e}")

time.sleep(5)
try:
    login_element = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//small[text()='Login']"))
    )
    login_element.click()
    print("✅ Elemento 'Login' clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no elemento 'Login': {e}")

try:
    campo_login = wait.until(
        EC.visibility_of_element_located((By.ID, "login"))
    )
    campo_login.send_keys("seu_email_ou_usuario_aqui")  # Substitua por um valor válido
    print("✅ Campo de login preenchido com sucesso!")
except Exception as e:
    print(f"❌ Erro ao preencher o campo de login: {e}")


# Solicitar e-mail e senha do usuário via input
email_usuario = input("Digite seu e-mail: ")
senha_usuario = input("Digite sua senha: ")

try:
    time.sleep(3)
    limpar_campo_email()  # Limpa o campo de e-mail
    type_keys(email_usuario)  # Digita o e-mail informado pelo usuário
    bot_tab()  # Passa para o próximo campo
    type_keys(senha_usuario)  # Digita a senha informada pelo usuário
    bot_tab()  # Passa para o próximo campo
    bot_tab()
    bot_enter()
    time.sleep(3)

    print("deuboa: E-mail e senha inseridos com sucesso!")
except Exception as e:
    print(f"nãodeuboa: Erro ao inserir os dados de login - {e}")

time.sleep(50000)
driver.quit()
logging.info("Script finalizado, navegador fechado.")

