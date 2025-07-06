from database import get_connection
from current_prices import current_prices

def unrealised_pl(portfolio_id):
    """
    Displays the unrealized profit/loss and return percentage
    for each stock in the user's holdings, based on current market prices.
    """
    print("*" * 20, "UNREALISED P&L", "*" * 20)

    conn = get_connection()
    cursor = conn.cursor()

    # Fetch holdings data for the given portfolio
    cursor.execute(
        "SELECT name, net_quantity, avg_price, total FROM holdings WHERE portfolio_id = %s", 
        (portfolio_id,)
    )
    results = cursor.fetchall()

    # Print table header
    print("{:^15}|{:^10}|{:^10}|{:^15}|{:^10}|{:^15}||{:^15}|{:^10}".format(
        "NAME", "QUANT", "PRICE", "BUY TOTAL",
        "CUR.PRICE", "CUR.TOTAL", "UNREALIZED P/L", "RETURN %"
    ))
    print("-" * 120)

    # Loop through each holding to calculate unrealized P/L
    for name, quantity, avg_price, buy_total in results:
        quantity = float(quantity)
        avg_price = float(avg_price)
        buy_total = float(buy_total)

        # Get current market price
        current_price = current_prices(name)

        # Calculate current value and P/L
        current_total = current_price * quantity
        unrealised_gain = current_total - buy_total

        # Avoid division by zero
        if avg_price == 0:
            return_pct = 0.0
        else:
            return_pct = round(((current_price - avg_price) / avg_price) * 100, 2)

        # Print formatted output
        print("{:^15}|{:^10}|{:^10}|{:^15}|{:^10}|{:^15}||{:^15}|{:^10}".format(
            name, 
            str(quantity), 
            str(avg_price), 
            str(round(buy_total, 2)),
            str(round(current_price, 2)), 
            str(round(current_total, 2)), 
            str(round(unrealised_gain, 2)), 
            f"{return_pct}%"
        ))

    # Close connection
    cursor.close()
    conn.close()
