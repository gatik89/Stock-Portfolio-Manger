from database import get_connection

def buy_stock(name, quantity, price, portfolio_id):
    """
    Inserts or updates a stock purchase entry in the portfolio database.

    Args:
        name (str): Name of the stock.
        quantity (int): Quantity of shares bought.
        price (float): Price per share.
        portfolio_id (str): Identifier for the user portfolio.
    """

    total = price * quantity  # Total cost for current purchase

    # Get database connection
    conn = get_connection()
    cursor = conn.cursor()

    # Check if stock already exists in the portfolio
    cursor.execute(
        "SELECT quantity, price FROM buy WHERE name=%s AND portfolio_id=%s",
        (name, portfolio_id)
    )
    result = cursor.fetchone()

    if result:
        # Existing stock entry found – update the quantity and average price
        existing_quantity, existing_price = result

        new_quantity = existing_quantity + quantity

        # Weighted average price calculation
        total_existing_cost = existing_quantity * existing_price
        total_new_cost = quantity * price
        new_price = (total_existing_cost + total_new_cost) / new_quantity

        new_total = new_quantity * new_price

        update_query = """
            UPDATE buy
            SET quantity=%s, price=%s, total=%s
            WHERE name=%s AND portfolio_id=%s
        """
        cursor.execute(
            update_query,
            (new_quantity, round(new_price, 2), round(new_total, 2), name, portfolio_id)
        )
        conn.commit()

        print(f"✅ '{name}' updated in your portfolio.")
        print(f"Quantity Added: {quantity} | Purchase Price: ₹{price} | Total Value: ₹{round(total_new_cost, 2)}")

    else:
        # No existing entry – insert new stock
        insert_query = """
            INSERT INTO buy (name, quantity, price, total, portfolio_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query,
            (name, quantity, price, total, portfolio_id)
        )
        conn.commit()

        print(f"✅ You have purchased ₹{round(total, 2)} worth of '{name}'.")
        print(f"Buy entry recorded successfully!")
        print(f"Quantity: {quantity} | Price: ₹{price} | Total: ₹{round(total, 2)}")

    # Close DB connection
    cursor.close()
    conn.close()





