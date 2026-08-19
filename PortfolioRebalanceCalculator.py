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
    print(f"{'Asset':<12} | {'Current Val':<12} | {'Target %':<8} | {'Amount to BUY':<15} | {'New Est. %':<10}")
    print("-" * 65)

    for pos in positions:
        new_val = pos['current_value'] + pos['buy_amount']
        new_pct = (new_val / (total_current_value + available_cash)) * 100
        
        final_buy = pos['buy_amount'] if pos['buy_amount'] > 0.01 else 0.0
        
        print(f"{pos['name']:<12} | {pos['current_value']:<12,.2f} | {pos['target_weight']:<7.2f}% | {final_buy:<15,.2f} | {new_pct:<10.2f}%")
        
    print("=" * 65)
    print("Note: If 'Amount to BUY' is 0.00, it means that specific asset is already")
    print("over-allocated. The script ignored it and gave your cash to the other assets.")

if __name__ == "__main__":
    run_buy_only_rebalancer()
