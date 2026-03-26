import yfinance as yf
import matplotlib.pyplot as plt

def generate_graph(stock):
    data = yf.download(stock, period="7d")

    # ❌ handle empty data
    if data.empty:
        return None

    plt.figure()
    plt.plot(data['Close'])
    plt.title(f"{stock} Price Trend (Last 7 Days)")
    plt.xlabel("Date")
    plt.ylabel("Price")

    file_path = "static/graph.png"
    plt.savefig(file_path)
    plt.close()

    return file_path