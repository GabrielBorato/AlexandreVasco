import time
import logging
import requests
import winsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def enviar_telegram(mensagem):
    token = '7935676935:AAEkJJW3gNXrQkbc9z6C9ztcwDMP0-g7XNU'
    chat_ids = [6675236455]  # 6675236455  483107010
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    for chat_id in chat_ids:
        payload = {
            'chat_id': chat_id,
            'text': mensagem
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print("✅ Notificação enviada no Telegram com sucesso.")
            else:
                print(f"❌ Falha ao enviar notificação. Código: {response.status_code}")
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem no Telegram: {e}")

caminho_chromedriver = ChromeDriverManager().install()
service = Service(caminho_chromedriver)
driver = webdriver.Chrome(service=service)

logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logging.info("Iniciando o script...")

url = "https://vasco.eleventickets.com/#!/home"
driver.get(url)
logging.info(f"Acessando a página: {url}")

# Aceitar cookies
try:
    wait = WebDriverWait(driver, 10)
    botao_aceitar_cookies = wait.until(
        EC.presence_of_element_located((By.ID, "textBtn"))
    )
    driver.execute_script("arguments[0].click();", botao_aceitar_cookies)
    print("✅ Botão 'ACEITAR TODOS OS COOKIES' clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no botão 'ACEITAR TODOS OS COOKIES': {e}")

# Acessar o ícone de login
try:
    wait = WebDriverWait(driver, 10)
    icone_perfil = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "md-icon[md-svg-src='img/svg/round58.svg']"))
    )
    icone_perfil.click()
    print("✅ Ícone de perfil clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no ícone de perfil: {e}")
time.sleep(3)

# Selecionar botão Público Geral
try:
    wait = WebDriverWait(driver, 10)
    publico_geral_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//span[.//p[text()='Público Geral - Jogos']]"
        ))
    )
    publico_geral_btn.click()
    print("✅ Botão 'Público Geral - Jogos' clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no botão 'Público Geral - Jogos': {e}")

# Coletar dados do usuário
time.sleep(10)
email_usuario = input("Digite seu e-mail: ")
senha_usuario = input("Digite sua senha: ")

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

# Inserir e-mail e senha
try:
    type_keys(email_usuario)
    bot_tab()
    type_keys(senha_usuario)
    bot_tab()
    bot_tab()
    bot_enter()
    time.sleep(3)
    print("✅ E-mail e senha inseridos com sucesso!")
except Exception as e:
    print(f"❌ Erro ao inserir o e-mail e senha: {e}")

# Clicar em "Comprar / Informações"
try:
    wait = WebDriverWait(driver, 10)
    botao_comprar = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[.//span[text()='Comprar / Informações']]"
        ))
    )
    botao_comprar.click()
    print("✅ Botão 'Comprar / Informações' clicado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao clicar no botão 'Comprar / Informações': {e}")

# Aguarda o usuário selecionar manualmente o jogo
input("👆 Selecione o jogo desejado manualmente e aperte [ENTER] para continuar...")

quantidades = ["4", "3", "2", "1"]
ingressos_disponiveis = False
primeira_tentativa = True

while not ingressos_disponiveis:
    try:
        elementos_blocos = driver.find_elements(By.XPATH, "//*[starts-with(@class, 'bloco')]")

        if elementos_blocos:
            for i, elemento in enumerate(elementos_blocos):
                try:
                    elemento.click()
                    time.sleep(2)
                    logging.info(f"Clicou no bloco {i + 1}")

                    try:
                        div_preco = driver.find_element(By.XPATH, "//div[contains(@class, 'layout-row') and contains(@class, 'flex-order-4')]")
                        span_preco = div_preco.find_element(By.TAG_NAME, "span")
                        preco_texto = span_preco.text.strip()

                        if preco_texto != "R$ 0.00":
                            ingressos_disponiveis = True
                            quantidade_selecionada = False
                            try:
                                wait = WebDriverWait(driver, 10)

                                # Localiza todos os seletores visíveis (vai dar duas opções: Inteira e Meia)
                                seletores = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "md-select-value")))

                                if len(seletores) >= 2:
                                    seletor_meia = seletores[1]  # a segunda roleta (Meia)

                                    # Clica para abrir o dropdown da meia-entrada
                                    driver.execute_script("arguments[0].scrollIntoView(true);", seletor_meia)
                                    seletor_meia.click()
                                    time.sleep(1)

                                    # Aguarda todas as opções
                                    opcoes = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "md-option")))

                                    valores_disponiveis = []
                                    for opcao in opcoes:
                                        texto = opcao.text.strip()
                                        if texto.isdigit():
                                            valores_disponiveis.append((int(texto), opcao))

                                    if valores_disponiveis:
                                        maior_valor, elemento = max(valores_disponiveis, key=lambda x: x[0])
                                        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
                                        elemento.click()
                                        print(f"✅ Selecionado {maior_valor} ingresso(s) meia-entrada.")
                                    else:
                                        print("⚠️ Nenhuma opção de quantidade encontrada para meia-entrada.")
                                else:
                                    print("⚠️ Não foi possível localizar os dois seletores de quantidade.")
                            except Exception as e:
                                print(f"❌ Erro ao selecionar meia-entrada ou adicionar ao carrinho: {e}")
                        time.sleep(1)
                        # Pressiona TAB duas vezes e depois ENTER
                        actions = ActionChains(driver)
                        actions.send_keys(Keys.TAB).pause(0.3)
                        actions.send_keys(Keys.TAB).pause(0.3)
                        actions.send_keys(Keys.ENTER).perform()
                        print("🛒 Ingresso adicionado ao carrinho via teclado.")
                        enviar_telegram(f"✅Ingressos Vasco disponíveis no carrinho")
                        winsound.Beep(2000, 1000)
                        alarme = [(2000, 800), (1500, 800), (2500, 800)]
                        for freq, dur in alarme * 6:
                            winsound.Beep(freq, dur)
                            time.sleep(0.1)
                    except Exception as e:
                        print(f"❌ Erro ao adicionar ingresso via teclado: {e}")
                        logging.info(f"Ingresso encontrado no bloco {i + 1}, parando a busca.")
                        break
                except Exception as e:
                    logging.error(f"Erro ao interagir com o bloco {i + 1}: {e}")
                    if primeira_tentativa:
                        primeira_tentativa = False
                        logging.info("Mensagem de indisponibilidade enviada.")
                    time.sleep(10)
    except Exception as e:
        logging.info("Script finalizado, navegador fechado.")
        driver.quit()
