# Simple Portfolio Rebalancer

A buy-only portfolio rebalancer. It takes cash you want to invest and allocates it to the holdings that are furthest below their target weights. It never sells.

## How to run

1. Install Jupyter: `pip install -r requirements.txt`
2. Open `PortfolioRebalanceCalculator.ipynb` in Jupyter, VS Code, or Cursor.
3. Run the cell.

You will be asked for:

- Available cash to invest
- Each position’s name, current market value (use `0` if you do not own it yet), and target weight in percent

Keep adding positions until the target weights sum to 100%. The notebook then prints how much to buy of each asset.

## License

MIT
