from playwright.sync_api import sync_playwright

def scrape_kabum():
    dados = []
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        url = f"https://www.kabum.com.br/hardware/memoria-ram"
        page.goto(url)
        page.wait_for_selector(".productCard")

        produtos = page.locator(".productCard")

        for i in range(produtos.count()):
            produto = produtos.nth(i)
            nome = produto.locator(".nameCard").inner_text()
            preco = produto.locator(".priceCard").inner_text()

            dados.append({
                "site": "kabum",
                "name": nome,
                "price": preco
            })
        browser.close()
    return dados

