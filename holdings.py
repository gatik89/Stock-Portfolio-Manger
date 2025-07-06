from database import get_connection

def holdings(portfolio_id):
    """
    Update the 'holdings' table based on buy and sell transactions
    for a given portfolio_id.
    """
    # Step 1: Connect to the database
    conn = get_connection()
    cursor = conn.cursor()

    # Step 2: Fetch buy data: { name: {quantity, price} }
    cursor.execute(
        "SELECT name, quantity, price FROM buy WHERE portfolio_id = %s", 
        (portfolio_id,)
    )
    buy_data = {
        row[0]: {"quantity": row[1], "price": row[2]} 
        for row in cursor.fetchall()
    }

    # Step 3: Fetch sell data: { name: quantity }
    cursor.execute(
        "SELECT name, quantity FROM sell WHERE portfolio_id = %s", 
        (portfolio_id,)
    )
    sell_data = {
        row[0]: row[1] 
        for row in cursor.fetchall()
    }

    # Step 4: Compute net holdings
    filtered = []
    for name, b_data in buy_data.items():
        total_buy_quantity = b_data["quantity"]
        avg_price = b_data["price"]
        sell_quantity = sell_data.get(name, 0)
        net_quantity = total_buy_quantity - sell_quantity

        if net_quantity > 0:
            total_value = avg_price * net_quantity
            filtered.append((name, net_quantity, avg_price, total_value, portfolio_id))

    # Step 5: Update holdings table
    cursor.execute(
        "DELETE FROM holdings WHERE portfolio_id = %s", 
        (portfolio_id,)
    )
    cursor.executemany(
        """
        INSERT INTO holdings 
        (name, net_quantity, avg_price, total, portfolio_id) 
        VALUES (%s, %s, %s, %s, %s)
        """,
        filtered
    )

    # Step 6: Finalize
    conn.commit()
    print(f"Updated {len(filtered)} holdings.")

    # Step 7: Clean up
    cursor.close()
    conn.close()

        
        

