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
    print(f"❌ Erro ao clicar no botão 'Concordo': {e}")

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
    print("✅ Campo de login preenchido com sucesso!")
except Exception as e:
    print(f"❌ Erro ao preencher o campo de login: {e}")

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

# Aguardar até que o botão 'Comprar' esteja presente e clicar
try:
    botao_comprar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-event='18336']"))
    )
    # Clicar no botão
    botao_comprar.click()
    print("✅ Botão 'Comprar' clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no botão 'Comprar': {e}")
try:
    preco_elemento = wait.until(
        EC.element_to_be_clickable((By.ID, "price-7434013"))
    )
    preco_elemento.click()  # Clica no preço
    print("✅ Preço clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no preço: {e}")
time.sleep(5)
try:
    for i in range(3):
        botao_incrementar = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-padrao-ativo.bootstrap-touchspin-up"))
        )
        botao_incrementar.click()  # Clica no botão '+'
        print(f"✅ Clique {i + 1} no botão '+' realizado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no botão '+': {e}")
try:
    botao_final_comprar = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn.fc-btn"))
    )
    botao_final_comprar.click()  # Clica no botão "Comprar"
    print("✅ Botão 'Comprar' final clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no botão 'Comprar' final: {e}")
time.sleep(5)
try:
    # Espera o botão 'OK' dentro da div com o id 'alert-cancel' estar visível e clicável
    botao_ok = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='alert-cancel']"))
    )
    botao_ok.click()  # Clica no botão "OK"
    print("✅ Botão 'OK' clicado com sucesso!")
    
except Exception as e:
    print(f"❌ Erro ao clicar no botão 'OK': {e}")

time.sleep(50000)
driver.quit()
logging.info("Script finalizado, navegador fechado.")
