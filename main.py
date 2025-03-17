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
url = "https://www.mengo.com.br/ingressos"
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
time.sleep(5)

# Clicar no botão LOGIN
try:
    botao_login = driver.find_element(By.XPATH, "//button[contains(., 'LOGIN')]")
    botao_login.click()
    logging.info("Botão LOGIN clicado com sucesso!")
except Exception as e:
    logging.error(f"Erro ao clicar no botão LOGIN: {e}")

time.sleep(2)

# Funções para envio de teclas
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

# Preenchendo o formulário de login
try:
    time.sleep(3)
    type_keys("alexandrermello@hotmail.com")
    bot_tab()
    type_keys("Leleca10@.!")
    bot_tab()
    time.sleep(3)
    bot_enter()
    logging.info("Credenciais inseridas com sucesso.")
except Exception as e:
    logging.error(f"Erro ao preencher os campos de login: {e}")

time.sleep(5)

# Verificação de login bem-sucedido
if "ingressos" in driver.current_url:
    logging.info("Login realizado com sucesso!")
else:
    logging.warning("Falha no login!")

time.sleep(10)

# Clicar no botão "Maracanã"
try:
    estadio_button = driver.find_element(By.XPATH, "//p[text()='Maracanã']")
    estadio_button.click()
    logging.info("Botão 'Maracanã' clicado com sucesso!")
except Exception as e:
    logging.error(f"Erro ao clicar no botão 'Maracanã': {e}")

time.sleep(10)

# Clicar no botão "COMPRAR INGRESSO"
try:
    comprar_ingresso_button = driver.find_element(By.XPATH, "//button[contains(., 'COMPRAR INGRESSO')]")
    comprar_ingresso_button.click()
    logging.info("Botão 'COMPRAR INGRESSO' clicado com sucesso!")
except Exception as e:
    logging.error(f"Erro ao clicar no botão 'COMPRAR INGRESSO': {e}")

time.sleep(15)

# Mudar para nova aba
abas = driver.window_handles
driver.switch_to.window(abas[-1])
logging.info("Mudou para a nova aba com sucesso!")

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

# Clicar no elemento ripple
try:
    wait = WebDriverWait(driver, 10)
    elemento_ripple = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='mdl-button__ripple-container']"))
    )
    elemento_ripple.click()
    logging.info("Elemento clicado com sucesso!")
except Exception as e:
    logging.error(f"Erro ao clicar no elemento: {e}")

ingressos_disponiveis = False
primeira_tentativa = True

while not ingressos_disponiveis:
    try:
        elementos_blocos = driver.find_elements(By.XPATH, "//*[starts-with(@class, 'bloco')]")
        
        if elementos_blocos:
            for i in range(len(elementos_blocos)):
                try:
                    elementos_blocos = driver.find_elements(By.XPATH, "//*[starts-with(@class, 'bloco')]")
                    elemento = elementos_blocos[i]
                    elemento.click()
                    time.sleep(2)
                    logging.info(f"Clicou no bloco {i + 1}")

                    try:
                        div_preco = driver.find_element(By.XPATH, "//div[contains(@class, 'layout-row') and contains(@class, 'flex-order-4')]")
                        span_preco = div_preco.find_element(By.TAG_NAME, "span")
                        preco_texto = span_preco.text.strip()

                        if preco_texto != "R$ 0.00":
                            ingressos_disponiveis = True
                            enviar_email("Ingressos Disponíveis!", f"Ingressos disponíveis no bloco {i + 1}! Preço: {preco_texto}")
                            logging.info(f"Ingresso encontrado no bloco {i + 1}, parando a busca.")
                            break
                    except Exception as e:
                        logging.error(f"Erro ao verificar preço: {e}")

                    botoes_fechar = driver.find_elements(By.XPATH, "//md-icon[@md-svg-src='img/svg/clear5.svg']")
                    if len(botoes_fechar) > 1:
                        driver.execute_script("arguments[0].click();", botoes_fechar[1])
                    time.sleep(3)
                except Exception as e:
                    logging.error(f"Erro ao interagir com o bloco {i + 1}: {e}")
        
        if primeira_tentativa:
            primeira_tentativa = False
            enviar_email("Ingressos Indisponíveis", "Ingressos indisponíveis na primeira tentativa, a busca continuará até encontrarmos disponibilidade.")
            logging.info("E-mail de indisponibilidade enviado.")

        time.sleep(10)
    except Exception as e:
        logging.error(f"Erro durante a busca: {e}")

driver.quit()
logging.info("Script finalizado, navegador fechado.")
