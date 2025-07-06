from nsepython import nse_eq

def current_prices(name):
    """
    Fetches the current market price of the given NSE stock.

    Args:
        name (str): The stock symbol (e.g., 'TCS', 'RELIANCE').

    Returns:
        float or str: Rounded last traded price if successful, otherwise "N/A".
    """
    try:
        # Fetch real-time stock data using NSE API
        data = nse_eq(name.upper())
        
        # Extract and return the last traded price, rounded to 2 decimals
        return round(float(data['priceInfo']['lastPrice']), 2)
    
    except Exception as e:
        # Handle errors gracefully and log issue
        print(f"⚠️ Error fetching price for '{name}': {e}")
        return "N/A"
