import csv
from scrapers.kabum import scrape_kabum
from scrapers.mercado_livre import scrape_mercado_livre


def main():

    todos_dados = []

    # rodar os scrapers fodas
    dados_kabum = scrape_kabum()
    dados_mercado_livre = scrape_mercado_livre()

    todos_dados.extend(dados_kabum)
    todos_dados.extend(dados_mercado_livre)

    # salva csv
    with open("products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["site", "name", "price"])
        writer.writeheader()
        writer.writerows(todos_dados)


if __name__ == "__main__":
    main()