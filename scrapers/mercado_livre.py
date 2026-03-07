from playwright.sync_api import sync_playwright
import re


def scrape_mercado_livre(url,pages=1):
    dados = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)

        for _ in range(pages):
            page.wait_for_selector(".ui-search-layout__item")

            try:
                # tirar o popup, se tiver
                botão = page.get_by_role("button", name="Mais tarde")
                if botão.is_visible():
                    botão.click()
            except:
                pass

            produtos = page.locator("li.ui-search-layout__item")

            total = produtos.count()

            for i in range(total):
                produto = produtos.nth(i)

                nome = produto.locator("h3").inner_text()

                fracao = produto.locator(
                    ".poly-price__current .andes-money-amount__fraction").first.inner_text()
                centavos = produto.locator(
                    ".poly-price__current .andes-money-amount__cents").first

                # centavos nem sempre existe
                if centavos.count() > 0:
                    preco = f"R${fracao},{centavos.inner_text()}"
                else:
                    preco = f"R${fracao},00"

                dados.append({
                    "site": "Mercado Livre",
                    "name": nome,
                    "price": preco
                })
            
            #clica em proxmi depois de raspar
            if _ < pages - 1:
                page.get_by_role("link", name="Seguinte").click()

        browser.close()
        return dados

