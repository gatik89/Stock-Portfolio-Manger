from database import get_connection

def profit_loss():
    """
    Displays profit/loss and return percentage for each stock
    that exists in both the 'buy' and 'sell' tables.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Join buy and sell data on stock name
    query = """
        SELECT 
            buy.name, buy.quantity, buy.price, buy.total,
            sell.name, sell.quantity, sell.price, sell.total
        FROM buy
        JOIN sell ON buy.name = sell.name
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Print table headers
    print("{:^15}|{:^10}|{:^10}|{:^12}|{:^15}|{:^10}|{:^10}|{:^12}||{:^10}|{:^10}".format(
        "BUY NAME", "B.QTY", "B.PRICE", "B.TOTAL",
        "SELL NAME", "S.QTY", "S.PRICE", "S.TOTAL",
        "P/L", "RETURN %"
    ))

    # Print a line separator
    print("-" * 122)

    # Iterate through results and calculate profit/loss
    for row in results:
        buy_total = row[3]
        sell_total = row[7]
        gain_loss = sell_total - buy_total

        # Avoid division by zero
        if buy_total == 0:
            return_pct = 0.0
        else:
            return_pct = round(((sell_total - buy_total) / buy_total) * 100, 2)

        print("{:^15}|{:^10}|{:^10}|{:^12}|{:^15}|{:^10}|{:^10}|{:^12}||{:^10}|{:^10}".format(
            row[0], str(row[1]), str(row[2]), str(buy_total),
            row[4], str(row[5]), str(row[6]), str(sell_total),
            str(gain_loss), f"{return_pct}%"
        ))

    # Clean up
    cursor.close()
    conn.close()
