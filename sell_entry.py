from database import get_connection

def sell_stock(name, quantity, price, portfolio_id):
    """
    Records or updates a stock sell transaction in the 'sell' table.

    If the stock already exists for the given portfolio, updates its average price and total.
    Otherwise, inserts a new record.
    """
    total = price * quantity

    conn = get_connection()
    cursor = conn.cursor()

    # Check if stock already exists in 'sell' table for this portfolio
    cursor.execute(
        "SELECT quantity, price FROM sell WHERE name = %s AND portfolio_id = %s",
        (name, portfolio_id)
    )
    result = cursor.fetchone()

    if result:
        # Existing record — update it
        existing_quantity, existing_price = result

        new_quantity = existing_quantity + quantity
        total_existing_cost = existing_quantity * existing_price
        total_new_cost = quantity * price

        # Calculate new average price
        new_price = (total_existing_cost + total_new_cost) / new_quantity
        new_total = new_quantity * new_price

        update_query = """
            UPDATE sell 
            SET quantity = %s, price = %s, total = %s 
            WHERE name = %s AND portfolio_id = %s
        """
        cursor.execute(
            update_query, 
            (new_quantity, round(new_price, 2), round(new_total, 2), name, portfolio_id)
        )
        conn.commit()

        print(f"'{name}' updated in the portfolio.")
        print(f"Quantity: {quantity} | Price: {price} | Total: ₹{round(total_new_cost, 2)}")

    else:
        # No previous record — insert new
        insert_query = """
            INSERT INTO sell (name, quantity, price, total, portfolio_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query, 
            (name, quantity, price, total, portfolio_id)
        )
        conn.commit()

        print(f"You have sold ₹{total} worth of '{name}'.")
        print(f"Sell entry of '{name}' has been successfully recorded!")
        print(f"Quantity: {quantity} | Price: {price} | Total: ₹{total}")

    # Clean up
    cursor.close()
    conn.close()


