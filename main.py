# Import the login module for user authentication
from login import user_login, register_user

logged_in_user = None  # Global variable to store logged in user's ID

# User authentication loop
while True:
    print("\n--- Welcome to the Stock Portfolio System ---")
    print("1. Login to an existing account")
    print("2. Create a new account")
    login_input = input("Enter your preference: ").strip()

    if login_input == "1":
        # Allow up to 3 login attempts
        attempts = 3
        while attempts > 0:
            portfolio_id = input("Enter your Portfolio ID: ").strip()
            if not portfolio_id:
                print("Please enter a valid Portfolio ID.")
                continue

            portfolio_password = input("Enter your Portfolio Password: ").strip()
            if not portfolio_password:
                print("Password cannot be empty. Try again.")
                continue

            if user_login(portfolio_id, portfolio_password):
                logged_in_user = portfolio_id
                break
            else:
                attempts -= 1
                print(f"Incorrect credentials. Attempts left: {attempts}")

        if attempts == 0:
            print("Too many failed attempts. Please try again later.")
            continue

    elif login_input == "2":
        register_user()
        continue

    else:
        print("Invalid input. Please choose '1' or '2'.")
        continue

    # Home page loop after successful login
    while True:
        print("\n" + "-" * 5 + " HOME " + "-" * 5)
        print("1. {:^14}".format("BUY"))
        print("2. {:^14}".format("SELL"))
        print("3. {:^14}".format("PROFIT/LOSS"))
        print("4. {:^14}".format("WATCHLIST"))
        print("5. {:^14}".format("STOCK REPORT"))
        print("6. {:^14}".format("UNREALISED P/L"))
        print("7. {:^14}".format("SEARCH STOCK"))

        inp3 = input("Enter the index number from above to perform an activity: ").strip()

        # Buy Entry
        if inp3 == "1":
            from buy_entry import buy_stock
            i=0
            while True:
                print(f"\nEntry {i + 1}")
                name = input("Enter the name of the bought stock: ")
                quantity = int(input(f"Enter the quantity bought of '{name}': "))
                price = float(input(f"Enter the price at which '{quantity}' shares of '{name}' were bought: "))
                buy_stock(name, quantity, price, logged_in_user)
                i += 1
                buy_end = input("Press 'Enter' to buy a new stock, '1' for menu, '2' for exit: ").strip().lower()
                if buy_end == "1":
                    print("Returing to menu...")
                    break
                elif buy_end == "2":
                    print(f"Good bye!")
                    exit()


        # Sell Entry
        elif inp3 == "2":
            from sell_entry import sell_stock
            i = 0
            while True:
                print(f"\nEntry {i + 1}")
                name = input("Enter the name of the sold stock: ")
                quantity = int(input(f"Enter the quantity sold of '{name}': "))
                price = float(input(f"Enter the price at which '{quantity}' shares of '{name}' were sold: "))
                sell_stock(name, quantity, price, logged_in_user)
                i += 1
                sell_end = input("Press 'Enter' to sell a stock, '1' for menu, '2' for exit: ").strip().lower()
                if sell_end == "1":
                    print("Returing to menu...")
                    break
                elif sell_end == "2":
                    print(f"Good bye!")
                    exit()


        # Profit/Loss 
        elif inp3 == "3":
            from profit_loss import profit_loss
            profit_loss()
            p_l_end = input("'1' for menu, '2' for exit: ").strip().lower()
            if p_l_end == "1":
                print("Returing to menu...")
                break
            elif p_l_end == "2":
                print(f"Good bye!")
                exit()

        # Watchlist Section
        elif inp3 == "4":
            while True:
                print("\n" + "-" * 5 + " WATCH LIST " + "-" * 5)
                print("1. {:^14}".format("ADD TO LIST"))
                print("2. {:^14}".format("VIEW LIST"))
                watchlist_input = input("Enter your choice (1 or 2): ").strip()

                if watchlist_input == "1":
                    from watchlist import add_to_list_input, view_list
                    add_to_list_input(logged_in_user)
                    view_list(logged_in_user)

                elif watchlist_input == "2":
                    from watchlist import view_list
                    view_list(logged_in_user)

                # Watchlist options
                while True:
                    inp5 = input("To add, remove, menu, or exit watchlist enter 1, 2, 3, or 4 respectively: ").strip()
                    if inp5 == "1":
                        from watchlist import add_to_list_input
                        add_to_list_input(logged_in_user)
                    elif inp5 == "2":
                        from watchlist import remove_from_list_input
                        remove_from_list_input(logged_in_user)
                    elif inp5 == "3":
                        print("returning to menu...")
                        break
                    elif inp5 == "4":
                        print("Don't have a good day — Have a great day!")
                        exit()
                

        # Stock Journal Entries
        elif inp3 == "5":
            from journal import journal_entries
            journal_entries(logged_in_user)
            journal_end = input("'1' for menu, '2' for exit: ").strip().lower()
            if journal_end == "1":
                print("Returing to menu...")
                break
            elif journal_end == "2":
                print(f"Good bye!")
                exit()

        # Unrealised Profit & Loss
        elif inp3 == "6":
            from holdings import holdings
            holdings(logged_in_user)
            from unrealisedpl import unrealised_pl
            unrealised_pl(logged_in_user)
            unrealised_pL_end = input("'1' for menu, '2' for exit: ").strip().lower()
            if unrealised_pL_end == "1":
                print("Returing to menu...")
                break
            elif unrealised_pL_end == "2":
                print(f"Good bye!")
                exit()

        # Stock Fundamentals Search
        elif inp3 == "7":
            from fundamentals import analyze_stock
            analyze_stock()
            stock_search_end = input("'1' for menu, '2' for exit: ").strip().lower()
            if stock_search_end == "1":
                print("Returing to menu...")
                break
            elif stock_search_end == "2":
                print(f"Good bye!")
                exit()






