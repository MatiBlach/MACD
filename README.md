# MACD Strategy for Stock Trading

This project implements the **MACD (Moving Average Convergence Divergence)** strategy to analyze stock price movements and generate buy and sell signals based on the MACD indicator. The analysis also compares the results of the MACD strategy to a simple "Buy and Forget" strategy. 
## Features

- Calculate **MACD** and **Signal** lines from historical stock data.
- Generate **buy** and **sell** signals based on MACD crossing the Signal line.
- Compare the performance of the **MACD strategy** to a **Buy and Forget** strategy (where you buy stock and hold it without any further actions).
- Visualize the stock price, MACD, Signal line, and buy/sell signals on a plot.
- Display portfolio values over time for both strategies.

## Requirements

The following Python libraries are required:

- `pandas`
- `matplotlib`
- `numpy`
- `datetime`

You can install the necessary libraries using `pip`:

```bash
pip install pandas matplotlib numpy
