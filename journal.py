from database import get_connection

def journal_entries(portfolio_id):
    """
    Display buy and sell journal entries for a given portfolio ID.
    Output is formatted as a terminal-friendly table.
    """

    print("*" * 18, "JOURNAL ENTRIES", "*" * 18)
    print("_" * 53)

    # Step 1: Connect to database
    conn = get_connection()
    cursor = conn.cursor()

    # Step 2: Fetch BUY entries
    print("-" * 20, "BUY ENTRIES", "-" * 20)
    cursor.execute(
        "SELECT name, quantity, price, total FROM buy WHERE portfolio_id = %s", 
        (portfolio_id,)
    )
    buy_entries = cursor.fetchall()

    print("{:^15}|{:^10}|{:^10}||{:^15}".format("NAME", "QUANT", "PRICE", "TOTAL"))
    for row in buy_entries:
        print("{:^15}|{:^10}|{:^10}||{:^15}".format(str(row[0]), str(row[1]), str(row[2]), str(row[3])))

    print()

    # Step 3: Fetch SELL entries
    print("_" * 53)
    print("-" * 20, "SELL ENTRIES", "-" * 20)
    cursor.execute(
        "SELECT name, quantity, price, total FROM sell WHERE portfolio_id = %s", 
        (portfolio_id,)
    )
    sell_entries = cursor.fetchall()

    print("{:^15}|{:^10}|{:^10}||{:^15}".format("NAME", "QUANT", "PRICE", "TOTAL"))
    for row in sell_entries:
        print("{:^15}|{:^10}|{:^10}||{:^15}".format(str(row[0]), str(row[1]), str(row[2]), str(row[3])))

    # Step 4: Clean up
    cursor.close()
    conn.close()





