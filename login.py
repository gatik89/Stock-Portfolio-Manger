from database import get_connection
from mysql.connector import IntegrityError

def register_user():
    """
    Registers a new user by collecting their name, a 6-digit portfolio ID,
    and a 4-digit PIN. Handles duplicate ID errors gracefully.
    """
    conn = get_connection()
    cursor = conn.cursor()

    new_name = input("Enter your name: ")

    # Get and validate 6-digit portfolio ID
    while True:
        new_portfolio_id = input("Create your 6-digit portfolio ID: ")
        if len(new_portfolio_id) == 6 and new_portfolio_id.isdigit():
            break
        print("Portfolio ID must be exactly 6 digits.")

    # Get and validate 4-digit password
    while True:
        new_portfolio_pass = input("Enter your 4-digit PIN: ")
        if len(new_portfolio_pass) == 4 and new_portfolio_pass.isdigit():
            break
        print("PIN must be exactly 4 digits.")

    try:
        cursor.execute(
            "INSERT INTO login (name, portfolio_id, portfolio_pass) VALUES (%s, %s, %s)",
            (new_name, new_portfolio_id, new_portfolio_pass)
        )
        conn.commit()
        print(f"Hey {new_name}, your account is created successfully!")

    except IntegrityError:
        print("User already exists. Please try again with a different Portfolio ID.")

    finally:
        cursor.close()
        conn.close()

def user_login(portfolio_id, portfolio_pass):
    """
    Authenticates a user using their portfolio ID and PIN.
    Returns True if valid, else False.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM login WHERE portfolio_id = %s AND portfolio_pass = %s",
        (portfolio_id, portfolio_pass)
    )
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        name = result[1]
        print(f"Welcome {name}! How are you doing today?")
        return True
    else:
        print("Invalid Portfolio ID or PIN.")
        return False





