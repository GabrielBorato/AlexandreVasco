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

# Configuração do logging
logging.basicConfig(
    filename="log.txt", 
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logging.info("Iniciando o script...")

# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Acessar a página
url = "https://vasco.eleventickets.com/#!/home"
driver.get(url)
logging.info(f"Acessando a página: {url}")

# Função para enviar e-mail
def enviar_email(assunto, mensagem):
    remetente = "demobruta@gmail.com"
    destinatario = "alexandrermello@hotmail.com"
    senha = "onwxxqvqigzgxjiv"  # Senha de aplicativo gerada no Google

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

# Aguarde a página carregar
time.sleep(10)
# Aceitar cookies
try:
    wait = WebDriverWait(driver, 10)
    botao_aceitar_cookies = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button-accept-cookie')]"))
    )
    botao_aceitar_cookies.click()
    logging.info("Botão 'ACEITAR TODOS OS COOKIES' clicado com sucesso!")
except Exception as e:
    logging.error(f"Erro ao clicar no botão 'ACEITAR TODOS OS COOKIES': {e}")
    print("Cookies aceito com sucesso")
time.sleep(5)

# Clicar no botão LOGIN
try:
    botao_login = driver.find_element(By.XPATH, "//a[@ng-click='login(true,null)']")
    botao_login.click()
    logging.info("Botão LOGIN clicado com sucesso!")
except Exception as e:
    logging.error(f"Erro ao clicar no botão LOGIN: {e}")
    print("Botão login clicado com sucesso")
time.sleep(2)
try:
    # Aguardar a imagem estar visível e interagível
    imagem_socio_torcedor = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[contains(@src, '64x64loginvasco.png')]"))
    )

    # Rolando até a imagem para garantir visibilidade
    driver.execute_script("arguments[0].scrollIntoView();", imagem_socio_torcedor)

    # Clicando na imagem
    imagem_socio_torcedor.click()

    logging.info("Imagem do Sócio Torcedor clicada com sucesso!")
    print("deuboa")
except Exception as e:
    logging.error(f"Erro ao clicar na imagem do Sócio Torcedor: {e}")
    print("nãodeuboa")

try:
    # Aguardar o botão LOGIN estar visível e clicável
    botao_login = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'LOGIN')]"))
    )

    # Rolando até o botão para garantir visibilidade
    driver.execute_script("arguments[0].scrollIntoView();", botao_login)

    # Clicando no botão LOGIN
    botao_login.click()

    logging.info("Botão LOGIN clicado com sucesso!")
    print("deuboa: Botão LOGIN")
except Exception as e:
    logging.error(f"Erro ao clicar no botão LOGIN: {e}")
    print("nãodeuboa: Botão LOGIN")

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

# Solicitar e-mail e senha do usuário via input
email_usuario = input("Digite seu e-mail: ")
senha_usuario = input("Digite sua senha: ")

try:
    time.sleep(3)
    type_keys(email_usuario)  # Digita o e-mail informado pelo usuário
    bot_tab()  # Passa para o próximo campo
    type_keys(senha_usuario)  # Digita a senha informada pelo usuário
    bot_tab()  # Passa para o próximo campo
    bot_enter()
    time.sleep(3)

    print("deuboa: E-mail e senha inseridos com sucesso!")
except Exception as e:
    print(f"nãodeuboa: Erro ao inserir os dados de login - {e}")

try:
    elemento_jogo = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@routerlink='/ingressos']//span[contains(text(), '8')]"))
    )
    elemento_jogo.click()
    logging.info("Clicou na data '8 abr.' com sucesso.")
except Exception as e:
    logging.error(f"Erro ao clicar na data: {e}")
time.sleep(50000)
driver.quit()
logging.info("Script finalizado, navegador fechado.")
