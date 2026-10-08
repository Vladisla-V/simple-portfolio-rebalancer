def run_buy_only_rebalancer():
    print("=" * 50)
    print("      BUY-ONLY PORTFOLIO REBALANCER (NO SELLING)      ")
    print("=" * 50)

    # 1. Get available cash
    while True:
        try:
            available_cash = float(input("Enter available funds to invest (e.g., 10000): "))
            if available_cash < 0:
                print("Available funds cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    positions = []
    total_weight = 0.0
    total_current_value = 0.0

    print("\n--- Enter your positions ---")
    
    # 2. Gather positions
    while total_weight < 100.0:
        remaining_weight = 100.0 - total_weight
        print(f"\nCurrent total weight allocated: {total_weight:.2f}% ({remaining_weight:.2f}% remaining)")
        
        name = input("Position Name (e.g., S&P500/SPY): ").strip()
        if not name:
            print("Name cannot be empty.")
            continue

        while True:
            try:
                curr_val = float(input(f"Current market value of {name} (0 if you don't own it yet): "))
                if curr_val < 0:
                    print("Value cannot be negative.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        while True:
            try:
                weight = float(input(f"Desired weight for {name} in % (Max allowed: {remaining_weight:.2f}%): "))
                if weight <= 0:
                    print("Weight must be greater than 0%.")
                    continue
                if weight > remaining_weight + 0.01:
                    print(f"Error: Exceeds 100%. You only have {remaining_weight:.2f}% left.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        positions.append({
            'name': name,
            'current_value': curr_val,
            'target_weight': weight,
            'buy_amount': 0.0
        })
        
        total_weight += weight
        total_current_value += curr_val

        if abs(total_weight - 100.0) < 0.01:
            break

    # 3. Buy-Only Algorithm (Iterative Cash-Flow Rebalancing)
    # We simulate investing the cash penny-by-penny (or chunk-by-chunk) 
    # to the assets that are furthest behind their target weights.
    remaining_cash = available_cash
    chunks = 10000
    cash_chunk = remaining_cash / chunks

    for _ in range(chunks):
        temp_total_value = total_current_value + (available_cash - remaining_cash)
        
        most_underfunded_idx = -1
        worst_deficit = -999999.0
        
        for i, pos in enumerate(positions):
            current_actual_val = pos['current_value'] + pos['buy_amount']
            current_share = (current_actual_val / temp_total_value) * 100 if temp_total_value > 0 else 0
            
            deficit = pos['target_weight'] - current_share
            
            if deficit > worst_deficit:
                worst_deficit = deficit
                most_underfunded_idx = i
        
        positions[most_underfunded_idx]['buy_amount'] += cash_chunk
        remaining_cash -= cash_chunk

    # 4. Print Results
    print("\n" + "=" * 65)
    print("                      BUY-ONLY INVESTMENT PLAN                      ")
    print("=" * 65)
    print(f"Total Portfolio Value Before:  {total_current_value:,.2f}")
    print(f"New Cash Distributed:          {available_cash:,.2f}")
    print(f"Total Portfolio Value After:   {total_current_value + available_cash:,.2f}")
    print("-" * 65)
    print(f"{'Asset':<12} | {'Current Val':<12} | {'Target %':<8} | {'Amount to BUY':<15} | {'New %':<10}")
    print("-" * 65)

    for pos in positions:
        new_val = pos['current_value'] + pos['buy_amount']
        new_pct = (new_val / (total_current_value + available_cash)) * 100
        
        final_buy = pos['buy_amount'] if pos['buy_amount'] > 0.01 else 0.0
        
        print(f"{pos['name']:<12} | {pos['current_value']:<12,.2f} | {pos['target_weight']:<7.2f}% | {final_buy:<15,.2f} | {new_pct:<10.2f}%")
        
    print("=" * 65)
    print("Note: If 'Amount to BUY' is 0.00, it means that specific asset is already")
    print("over-allocated. The script ignored it and gave your cash to the other assets.")

def run_sell_only_rebalancer():
    print("=" * 50)
    print("      SELL-ONLY PORTFOLIO REBALANCER (NO BUYING)      ")
    print("=" * 50)

    # 1. Get the amount to raise
    while True:
        try:
            amount_to_raise = float(input("Enter amount to raise by selling (e.g., 10000): "))
            if amount_to_raise < 0:
                print("Amount to raise cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    positions = []
    total_weight = 0.0
    total_current_value = 0.0

    print("\n--- Enter your positions ---")

    # 2. Gather positions
    while total_weight < 100.0:
        remaining_weight = 100.0 - total_weight
        print(f"\nCurrent total weight allocated: {total_weight:.2f}% ({remaining_weight:.2f}% remaining)")

        name = input("Position Name (e.g., S&P500/SPY): ").strip()
        if not name:
            print("Name cannot be empty.")
            continue

        while True:
            try:
                curr_val = float(input(f"Current market value of {name} (0 if you don't own it yet): "))
                if curr_val < 0:
                    print("Value cannot be negative.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        while True:
            try:
                weight = float(input(f"Desired weight for {name} in % (Max allowed: {remaining_weight:.2f}%): "))
                if weight <= 0:
                    print("Weight must be greater than 0%.")
                    continue
                if weight > remaining_weight + 0.01:
                    print(f"Error: Exceeds 100%. You only have {remaining_weight:.2f}% left.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        positions.append({
            'name': name,
            'current_value': curr_val,
            'target_weight': weight,
            'sell_amount': 0.0
        })

        total_weight += weight
        total_current_value += curr_val

        if abs(total_weight - 100.0) < 0.01:
            break

    while amount_to_raise > total_current_value:
        print(f"Amount to raise ({amount_to_raise:,.2f}) exceeds total portfolio value ({total_current_value:,.2f}).")
        while True:
            try:
                amount_to_raise = float(input("Enter amount to raise by selling (e.g., 10000): "))
                if amount_to_raise < 0:
                    print("Amount to raise cannot be negative.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

    # 3. Sell-Only Algorithm (Iterative Cash-Flow Rebalancing)
    # We simulate raising the cash chunk-by-chunk
    # from the assets that are furthest above their target weights.
    remaining_to_sell = amount_to_raise
    chunks = 10000
    sell_chunk = remaining_to_sell / chunks

    for _ in range(chunks):
        left_in_chunk = sell_chunk

        while left_in_chunk > 1e-12:
            temp_total_value = total_current_value - (amount_to_raise - remaining_to_sell)

            most_overweight_idx = -1
            worst_surplus = -999999.0

            for i, pos in enumerate(positions):
                current_actual_val = pos['current_value'] - pos['sell_amount']
                if current_actual_val <= 0:
                    continue

                current_share = (current_actual_val / temp_total_value) * 100 if temp_total_value > 0 else 0
                surplus = current_share - pos['target_weight']

                if surplus > worst_surplus:
                    worst_surplus = surplus
                    most_overweight_idx = i

            if most_overweight_idx == -1:
                left_in_chunk = 0.0
                break

            room = positions[most_overweight_idx]['current_value'] - positions[most_overweight_idx]['sell_amount']
            step = left_in_chunk if left_in_chunk < room else room
            if step <= 0:
                left_in_chunk = 0.0
                break

            positions[most_overweight_idx]['sell_amount'] += step
            left_in_chunk -= step
            remaining_to_sell -= step

    # 4. Print Results
    portfolio_after = total_current_value - amount_to_raise

    print("\n" + "=" * 65)
    print("                    SELL-ONLY WITHDRAWAL PLAN                    ")
    print("=" * 65)
    print(f"Total Portfolio Value Before:  {total_current_value:,.2f}")
    print(f"Cash Raised:                   {amount_to_raise:,.2f}")
    print(f"Total Portfolio Value After:   {portfolio_after:,.2f}")
    print("-" * 65)
    print(f"{'Asset':<12} | {'Current Val':<12} | {'Target %':<8} | {'Amount to SELL':<15} | {'New %':<10}")
    print("-" * 65)

    for pos in positions:
        new_val = pos['current_value'] - pos['sell_amount']
        new_pct = (new_val / portfolio_after) * 100 if portfolio_after > 0 else 0.0

        final_sell = pos['sell_amount'] if pos['sell_amount'] > 0.01 else 0.0

        print(f"{pos['name']:<12} | {pos['current_value']:<12,.2f} | {pos['target_weight']:<7.2f}% | {final_sell:<15,.2f} | {new_pct:<10.2f}%")

    print("=" * 65)
    print("Note: If 'Amount to SELL' is 0.00, it means that specific asset is already")
    print("under-allocated. The script ignored it and raised the cash from the other assets.")

if __name__ == "__main__":
    while True:
        choice = input("Rebalance by buying or selling? (buy/sell): ").strip().lower()
        if choice == "buy":
            run_buy_only_rebalancer()
            break
        if choice == "sell":
            run_sell_only_rebalancer()
            break
        print("Please enter buy or sell.")
