from playwright.sync_api import sync_playwright


def scrape_kabum(url, pages=1):
    dados = []
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(url)

        for _ in range(pages):
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
            if _ < pages - 1:
                page.get_by_role("button", name="Next page").click()

        browser.close()
    return dados
