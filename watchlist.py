from database import get_connection
from current_prices import current_prices

# Add a stock to the watchlist

def add_to_list(name, trigger_price, portfolio_id):
    """
    Adds or updates a stock in the user's watchlist.
    Updates trigger price if stock already exists.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Check if stock already exists
    cursor.execute(
        "SELECT * FROM watchlist WHERE name = %s AND portfolio_id = %s", 
        (name, portfolio_id)
    )
    result = cursor.fetchone()

    if result:
        # Update trigger price and timestamp
        cursor.execute(
            "UPDATE watchlist SET trigger_price = %s, date = NOW() WHERE name = %s AND portfolio_id = %s",
            (trigger_price, name, portfolio_id)
        )
    else:
        # Insert new entry
        cursor.execute(
            "INSERT INTO watchlist (name, trigger_price, portfolio_id) VALUES (%s, %s, %s)",
            (name, trigger_price, portfolio_id)
        )
        print(f"'{name}' added to your watchlist at a trigger price of ₹{trigger_price}")

    conn.commit()
    cursor.close()
    conn.close()

def add_to_list_input(portfolio_id):
    """
    Prompts user to add multiple stocks to their watchlist via input.
    """
    try:
        num_of_stocks = int(input("Enter the number of stocks to add to your watchlist: "))
        for i in range(num_of_stocks):
            print(f"{i+1} of {num_of_stocks}")
            name = input("Enter the stock ticker: ").strip().upper()
            trigger_price_input = float(input(f"Enter the trigger price level of '{name}': "))
            add_to_list(name, trigger_price_input, portfolio_id)
    except ValueError:
        print("Invalid input. Please enter valid numbers.")

# View the current watchlist

def view_list(portfolio_id):
    """
    Displays the user's watchlist along with current prices and % difference.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, date, trigger_price FROM watchlist WHERE portfolio_id = %s", 
        (portfolio_id,)
    )
    result = cursor.fetchall()

    print("{:^13}|{:^20}|{:^15}|{:^15}|{:^15}".format(
        "NAME", "DATE", "TRIGGER PRICE", "CURRENT PRICE", "% DIFFERENCE"
    ))
    print("-" * 85)

    for name, date, trigger_price in result:
        current_price = current_prices(name)
        try:
            difference = round(((trigger_price - current_price) / trigger_price) * 100, 1)
        except ZeroDivisionError:
            difference = 0.0

        print("{:^13}|{:^20}|{:^15}|{:^15}|{:^15}".format(
            name, str(date), str(trigger_price), str(current_price), f"{difference}%"
        ))

    cursor.close()
    conn.close()

# Remove a stock from the watchlist

def remove_from_list(name, portfolio_id):
    """
    Removes a specific stock from the watchlist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM watchlist WHERE name = %s AND portfolio_id = %s", 
        (name, portfolio_id)
    )
    conn.commit()

    print(f"'{name}' has been removed from your watchlist.")

    cursor.close()
    conn.close()

def remove_from_list_input(portfolio_id):
    """
    Prompts user to remove multiple stocks from their watchlist via input.
    """
    try:
        num_of_stocks = int(input("Enter the number of stocks to remove from your watchlist: "))
        for i in range(num_of_stocks):
            print(f"{i+1} of {num_of_stocks}")
            name = input("Enter the name of the stock: ").strip().upper()
            remove_from_list(name, portfolio_id)
    except ValueError:
        print("Invalid input. Please enter valid numbers.")









