from flask import Flask, render_template, request
import yfinance as yf
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    stock_data = {}
    if request.method == "POST":
        symbol = request.form.get("symbol").upper().strip()
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            name = info.get("longName")
            price = info.get("currentPrice")
            previous = info.get("previousClose")

            if name and price and previous:
                change = price - previous
                percent = (change / previous) * 100
                tz = pytz.timezone("America/Los_Angeles")
                current_time = datetime.now(tz).strftime('%a %b %d %H:%M:%S %Z %Y')
                stock_data = {
                    "time": current_time,
                    "symbol": symbol,
                    "name": name,
                    "price": f"{price:.2f}",
                    "change": f"{change:+.2f}",
                    "percent": f"{percent:+.2f}%"
                }
            else:
                stock_data["error"] = "Incomplete data received."
        except Exception as e:
            stock_data["error"] = f"Error: {str(e)}"

    return render_template("index.html", stock=stock_data)

if __name__ == "__main__":
    app.run(debug=True)
