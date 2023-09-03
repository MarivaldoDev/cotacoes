from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PySimpleGUI import PySimpleGUI as sg


def buscar_cotacao(cotacao):
    servico = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    navegador = webdriver.Chrome(options=chrome_options, service=servico)
    navegador.get(f'https://www.google.com/search?q=cotação+{cotacao}')
    try:
        valor = navegador.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
    except:
        return 0
    else:
        return float(valor)

sg.theme("Reddit")
# Layout
layout = [
    [sg.Text("Cotação"), sg.Input(key="cotação", size=(20, 1))],
    [sg.Button("Buscar")],
    [sg.Text(" ", key="mensagem")],
]

# janela
janela = sg.Window("Pegador de cotações", layout)

# ler os eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    elif eventos == "Buscar":
        cotacao = valores["cotação"]
        resultado = buscar_cotacao(cotacao)
        if resultado == 0:
            janela["mensagem"].update("Apenas aceitamos cotações!")
        else:
            janela["mensagem"].update(f"A cotação do {cotacao} está R$ {resultado:.2f}")

janela.close()