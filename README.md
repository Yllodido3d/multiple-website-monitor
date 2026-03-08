# Multi-Site Price Monitor

This project was built based on a fictional client request: monitor product prices across multiple e-commerce websites and send an email alert when a price drop is detected.

## Structure

```
project/
│
├── scrapers/
│   ├── kabum.py           # Scraper for KaBuM
│   └── mercado_livre.py   # Scraper for Mercado Livre
│
├── main.py                # Runs all scrapers and exports raw data to CSV
├── monitor.py             # Runs scrapers, compares prices and sends email alert
├── precos.json            # Auto-generated — stores the last recorded prices
└── config.py              # Email credentials (not included in repo)
```

- Each scraper is an independent module that returns a list of dicts with the extracted data.
- `main.py` exports all scraped data to a CSV file.
- `monitor.py` compares current prices against the last recorded ones and sends an email if any price has dropped.

## Example Output

![image](image.png)

## How to run

1. Install dependencies:
```bash
pip install playwright pandas
playwright install chromium
```

2. Create a `config.py` file with your email credentials:
```python
EMAIL = "your@gmail.com"
SENHA = "your app password"
```
> To generate a Gmail app password: Google Account → Security → 2-Step Verification → App Passwords.

3. Edit the URLs and number of pages in `monitor.py` or `main.py`:
```python
scrape_kabum("https://www.kabum.com.br/hardware/memoria-ram", paginas=3)
scrape_mercado_livre("https://lista.mercadolivre.com.br/mouse-gamer", paginas=2)
```

4. Run the monitor:
```bash
python monitor.py
```

On the first run, `precos.json` is created with the current prices. On subsequent runs, prices are compared and an email is sent if any drop is detected.

To export raw data to CSV instead:
```bash
python main.py
```

## Known Limitations

- Mercado Livre changes the order of results between runs, which can cause false comparisons. Using product URLs as keys instead of names would make matching more reliable — planned as a future improvement.
- Mercado Livre does not work in headless mode and requires a visible browser window.

## Built with

- Python
- Playwright
- smtplib
- csv
