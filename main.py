import csv

from sqlalchemy import all_
from scrapers.kabum import scrape_kabum
from scrapers.mercado_livre import scrape_mercado_livre


def main():

    all_data = []

    # rodar os scrapers fodas
    data_kabum = scrape_kabum("https://www.kabum.com.br/hardware/memoria-ram")
    data_mercado_livre = scrape_mercado_livre(
        "https://lista.mercadolivre.com.br/mouse-gamer")

    all_data.extend(data_kabum)
    all_data.extend(data_mercado_livre)

    # salva csv
    with open("products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["site", "name", "price"])
        writer.writeheader()
        writer.writerows(all_data)


if __name__ == "__main__":
    main()
