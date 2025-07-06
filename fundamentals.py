import requests
from bs4 import BeautifulSoup
import yfinance as yf
from nsepython import nse_eq, nse_get_index_list
from math import sqrt
from colorama import Fore, Style, init

init(autoreset=True)

def analyze_stock():
    """
    Main function to analyze a stock using data from Yahoo Finance, NSE, and Screener.in
    """

    # Utility to apply colors based on upward/downward trends
    def color_by_trend(values):
        result = []
        prev = None
        for val in values:
            try:
                clean_val = val.replace(',', '').replace('%', '')
                num = float(clean_val)
                formatted_val = f"{val:^13}"
                if prev is None:
                    result.append(formatted_val)
                else:
                    if num > prev:
                        result.append(Fore.GREEN + formatted_val + Style.RESET_ALL)
                    elif num < prev:
                        result.append(Fore.RED + formatted_val + Style.RESET_ALL)
                    else:
                        result.append(formatted_val)
                prev = num
            except:
                result.append(f"{val:^13}")
                prev = None
        return result

    # Fetch stock fundamentals from Yahoo Finance and NSE
    def company_info(symbol_ns, index_name="NIFTY 50"):
        ticker = yf.Ticker(symbol_ns)
        info = ticker.info
        balancesheet = ticker.balance_sheet
        financial_statements = ticker.financials
        hist = ticker.history(period="10y")
        eq_data = nse_eq(symbol_ns.replace(",NS", ""))
        index_data = nse_get_index_list()

        data = {}
        data["Company Name"] = info.get("longName")
        data["Sector"] = info.get("sector")
        data["Industry"] = info.get("industry")
        data["Website"] = info.get("website")
        data["Current Price"] = info.get("currentPrice")
        data["Market Cap"] = info.get("marketCap")
        data["52 Week High"] = info.get("fiftyTwoWeekHigh")
        data["52 Week Low"] = info.get("fiftyTwoWeekLow")
        data["Book Value"] = info.get("bookValue")
        data["EPS"] = info.get("epsTrailingTwelveMonths")

        # Asset and liability calculations
        try:
            total_assets = float(balancesheet.loc["Total Assets"][0])
        except:
            total_assets = 0

        total_debt = 0
        try:
            long_term_debt = float(balancesheet.loc.get("Long Term Debt", [0])[0])
            short_term_debt = float(balancesheet.loc.get("Short Term Debt", [0])[0])
            total_debt = long_term_debt + short_term_debt
        except:
            pass

        data["Total Assets"] = total_assets
        data["Total Liability"] = total_debt

        try:
            annual_sales = float(financial_statements.loc["Total Revenue"][0])
        except:
            annual_sales = None

        try:
            net_profit = float(financial_statements.loc["Net Income"][0])
        except:
            net_profit = None

        data["Annual Sales"] = annual_sales
        data["Annual Net Profit"] = net_profit

        try:
            if data["EPS"] and data["Book Value"]:
                data["Graham Number"] = sqrt(22.5 * data["EPS"] * data["Book Value"])
        except:
            data["Graham Number"] = None

        data["Stock P/E"] = info.get("trailingPE")
        data["Stock P/B"] = info.get("priceToBook")
        data["Dividend Yield"] = info.get("dividendYield")

        try:
            equity = float(balancesheet.loc["Total Stockholder Equity"][0])
            data["Debt To Equity"] = round((total_debt / equity) * 100, 2)
        except:
            data["Debt To Equity"] = None

        try:
            data["Industry PE"] = eq_data["metadata"]["pdsectorPe"]
        except:
            data["Industry PE"] = None

        data["Analyst Recommendation Score"] = info.get("recommendationMean")
        data["Sentiment"] = info.get("recommendationKey")

        # CAGR Calculations
        if len(hist) >= 250:
            try:
                price = list(hist["Close"])
                today_price = price[-1]

                def cagr(start_price, years):
                    return round(((today_price / start_price) ** (1 / years) - 1) * 100, 2)

                if len(price) >= 250:
                    data["1Y CAGR"] = cagr(price[-250], 1)
                if len(price) >= 750:
                    data["3Y CAGR"] = cagr(price[-750], 3)
                if len(price) >= 1250:
                    data["5Y CAGR"] = cagr(price[-1250], 5)
                if len(price) >= 2000:
                    data["10Y CAGR"] = cagr(price[0], 10)
            except Exception as e:
                data["CAGR error"] = str(e)
        else:
            data["CAGR Data"] = "Not enough history"

        try:
            equity = float(balancesheet.loc["Total Shareholder Fund"][0])
            if net_profit and equity != 0:
                data["ROE"] = round((net_profit / equity) * 100, 2)
        except:
            data["ROE"] = None

        try:
            ebit = float(financial_statements.loc["Ebit"][0])
            cash = float(balancesheet.loc.get("Cash And Cash Equivalents", [0])[0])
            capital_emp = total_assets - short_term_debt - cash
            if ebit and capital_emp:
                data["ROCE"] = round((ebit / capital_emp) * 100, 2)
        except:
            data["ROCE"] = None

        return data

    # Web scraping Screener.in for ratios and tables
    def screener(stock):
        url = f"https://www.screener.in/company/{stock.upper()}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {}, {}

        soup = BeautifulSoup(response.text, "html.parser")
        screener_data = {}

        # Extract company description
        about_company = soup.find("div", class_="company-profile")
        if about_company:
            first_para = about_company.find("p")
            if first_para:
                about_text = first_para.get_text(separator="").strip().split("Read more")[0]
            else:
                about_text = "Not available"
        else:
            about_text = "Not available"
        screener_data["About Company"] = about_text

        # Extract key ratios
        ratio_section = soup.find("ul", id="top-ratios")
        if ratio_section:
            for li in ratio_section.find_all("li"):
                name = li.find("span", class_="name").text.strip()
                value = li.find("span", class_="number") or li.find("span", class_="value")
                screener_data[name] = value.text.strip()

        # Extract financial tables
        financial_tables = {}
        sections = soup.find_all("section", class_="card card-large")
        for section in sections:
            heading = section.find("h2")
            table = section.find("table")
            if heading and table:
                title = heading.text.strip()
                headers = [th.text.strip() for th in table.find_all("th")]
                rows = []
                for row in table.find_all("tr")[1:]:
                    cells = [td.text.strip() for td in row.find_all("td")]
                    if cells:
                        rows.append(cells)
                financial_tables[title] = {"headers": headers, "rows": rows}

        return screener_data, financial_tables

    # Print all structured output
    def print_clean(data, screener, screener_tables):
        def safe_print(label, key, width=30):
            value = data.get(key)
            print(f"{label:<{width}}: {value}")

        print("=" * 40)
        print(f"FUNDAMENTALS - {data.get('Company Name', 'N/A')}")
        print("=" * 40)

        print("Company Info")
        print("-" * 40)
        for i in ["Company Name", "Sector", "Industry", "Website"]:
            safe_print(i, i)

        print("\nStock Details")
        print("-" * 40)
        for i in ["Current Price", "Market Cap", "52 Week High", "52 Week Low", "Book Value", "EPS", "Graham Number"]:
            safe_print(i, i)

        print("\nKey Ratios")
        print("-" * 40)
        for i in ["Stock P/E", "Stock P/B", "Dividend Yield", "Industry PE", "ROE", "ROCE"]:
            safe_print(i, i)

        print("\nCAGR Returns")
        print("-" * 40)
        for i in ["1Y CAGR", "3Y CAGR", "5Y CAGR", "10Y CAGR"]:
            safe_print(i, i)

        print("\nSentiment & Analyst Rating")
        print("-" * 40)
        for i in ["Sentiment", "Analyst Recommendation Score"]:
            safe_print(i, i)

        print("\nScreener Ratios")
        print("=" * 40)
        for k, v in screener.items():
            print(f"{k:<35}: {v}")

        print("=" * 40)
        print("{:^40}".format("Financial Tables"))
        print("=" * 40)
        for title, table in screener_tables.items():
            print(f"\n{title}")
            print("-" * (len(title) + 5))
            header = table["headers"][-9:]
            print(f"{'':^25}" + "|".join(f"{h:^13}" for h in header))
            for row in table["rows"]:
                category = row[0]
                trimmed = row[-9:]
                colored = color_by_trend(trimmed)
                print(f"{category:^23}||" + "|".join(f"{cell:^13}" for cell in colored))

    # Ask user for symbol and run the full analysis
    symbol = input("Enter NSE symbol (e.g., TCS): ").strip().upper()
    if not symbol.endswith(".NS"):
        symbol += ".NS"

    print(f"\nFetching data for {symbol}...\n")
    core_data = company_info(symbol)
    screener_data, screener_tables = screener(symbol.replace(".NS", ""))
    print_clean(core_data, screener_data, screener_tables)




     









    
    


   

