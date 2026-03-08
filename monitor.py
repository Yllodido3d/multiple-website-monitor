from email.mime.text import MIMEText
import smtplib
import json
import os
from scrapers.kabum import scrape_kabum
from scrapers.mercado_livre import scrape_mercado_livre
import config


def carregar_precos_anteriores():
    if os.path.exists("precos.json"):
        with open("precos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def salvar_precos(precos):
    with open("precos.json", "w", encoding="utf-8") as f:
        json.dump(precos, f, ensure_ascii=False, indent=2)


def checar_alertas(atuais, anteriores):
    alertas = []
    for nome, preco in atuais.items():
        if nome in anteriores and preco < anteriores[nome]:
            alertas.append((nome, anteriores[nome], preco))
    return alertas


# ------------------------------------------------------------------------
# 1- rodar os scrapers
dados = scrape_kabum("https://www.kabum.com.br/hardware/memoria-ram") + \
    scrape_mercado_livre("https://lista.mercadolivre.com.br/mouse-gamer")

# 2- trasnformar essa lista em um dict de produtos simples, com nome e preco
precos_atuais = {}
for produto in dados:
    precos_atuais[produto["name"]] = produto["price"]

# 3- carregar o json anterior (preços anteriores)
precos_anteriores = carregar_precos_anteriores()

# 4- compara
alertas = checar_alertas(precos_atuais, precos_anteriores)

# 5- salva os atuais (e substitui os anteriores)
salvar_precos(precos_atuais)

# 6- enviar email de alerta


def enviar_email(alertas, remetente, senha, destinatario):
    if not alertas:
        print("No price drops detected")
        return

    corpo = "Price drops detected:\n\n"
    for nome, preco_antes, preco_depois in alertas:
        corpo += f"{nome}\nBefore: {preco_antes} → Now: {preco_depois}\n\n"

    msg = MIMEText(corpo)
    msg["Subject"] = "🔔 Price drop alert"
    msg["From"] = remetente
    msg["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remetente, senha)
        smtp.sendmail(remetente, destinatario, msg.as_string())

    print("Email sent!")


enviar_email(
    alertas,
    remetente=config.EMAIL,
    senha=config.SENHA,
    destinatario=config.EMAIL
)
