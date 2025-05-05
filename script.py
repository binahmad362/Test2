import os
import sys
import ccxt
import pandas as pd
import pytz
from pybit.unified_trading import HTTP
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===== Configuration =====
SYMBOLS = [
    'XRP/USDT:USDT',
    'BTC/USDT:USDT',
    'ETH/USDT:USDT',
    'SOL/USDT:USDT',
    'ADA/USDT:USDT'
]
TRADE_AMOUNT_USDT = 50
STOPLOSS_PERCENT = 2
TAKEPROFIT_PERCENT = 7.5

# Email Configuration
SENDER_EMAIL = "dahmadu071@gmail.com"
RECIPIENT_EMAILS = ["teejeedeeone@gmail.com"]
EMAIL_PASSWORD = "oase wivf hvqn lyhr"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Strategy Parameters
EMA_FAST = 38
EMA_SLOW = 62
EMA_TREND = 200
TIMEFRAME = '15m'

# GitHub Actions State File
STATE_FILE = "trade_state.txt"

# ===== State Management =====
def check_trade_state():
    """Check if we've already made a trade in this run"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return f.read().strip() == "TRADED"
    return False

def set_trade_state():
    """Mark that we've made a trade"""
    with open(STATE_FILE, 'w') as f:
        f.write("TRADED")

# ===== Initialize Connections =====
bybit = HTTP(
    api_key=os.getenv("BYBIT_API_KEY", "lJu52hbBTbPkg2VXZ2"),
    api_secret=os.getenv("BYBIT_API_SECRET", "e43RV6YDZsn24Q9mucr0i4xbU7YytdL2HtuV"),
    demo=True  # Use demo=True for testing, False for live
)

bitget = ccxt.bitget({
    'enableRateLimit': True
})

# ===== Email Functions =====
def send_email_notification(subject, body):
    """Send email notification about trade execution"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(RECIPIENT_EMAILS)
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAILS, msg.as_string())
        
        print("Email notification sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# ===== Trading Functions =====
def place_trade_order(symbol, signal, price):
    """Place the trade order with stop-loss and take-profit"""
    if check_trade_state():
        print("Already executed a trade in this run. Exiting.")
        sys.exit(0)
    
    bybit_symbol = symbol.replace('/USDT:USDT', 'USDT')
    lot_size_info = get_lot_size_info(symbol)
    
    # Calculate position size
    raw_qty = TRADE_AMOUNT_USDT / price
    quantity = adjust_quantity(raw_qty, lot_size_info)
    
    # Calculate SL and TP prices
    if signal == "buy":
        sl_price = round(price * (1 - STOPLOSS_PERCENT/100), 4)
        tp_price = round(price * (1 + TAKEPROFIT_PERCENT/100), 4)
        side = "Buy"
    else:  # sell/short
        sl_price = round(price * (1 + STOPLOSS_PERCENT/100), 4)
        tp_price = round(price * (1 - TAKEPROFIT_PERCENT/100), 4)
        side = "Sell"
    
    # Place the order
    order = bybit.place_order(
        category="linear",
        symbol=bybit_symbol,
        side=side,
        orderType="Market",
        qty=str(quantity),
        takeProfit=str(tp_price),
        stopLoss=str(sl_price),
        timeInForce="GTC"
    )
    
    if order['retCode'] == 0:
        set_trade_state()  # Mark that we've made a trade
        trade_details = (
            f"Symbol: {symbol}\n"
            f"Direction: {signal.upper()}\n"
            f"Quantity: {quantity} {bybit_symbol.replace('USDT', '')}\n"
            f"Entry Price: {price}\n"
            f"Stop-Loss: {sl_price} ({STOPLOSS_PERCENT}%)\n"
            f"Take-Profit: {tp_price} ({TAKEPROFIT_PERCENT}%)\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        print(f"\nOrder executed successfully for {symbol}:")
        print(trade_details)
        
        # Send email notification
        email_subject = f"Trade Executed: {signal.upper()} {symbol}"
        send_email_notification(email_subject, trade_details)
        
        # Exit after first successful trade
        sys.exit(0)
    else:
        error_msg = f"Order failed for {symbol}: {order['retMsg']}"
        print(error_msg)
        send_email_notification(f"Trade Failed: {symbol}", error_msg)

# ===== Main Execution =====
if __name__ == "__main__":
    # Check if we've already traded in this run
    if check_trade_state():
        print("Already executed a trade in this workflow run. Exiting.")
        sys.exit(0)
    
    print(f"Running multi-symbol strategy on {TIMEFRAME} timeframe")
    print(f"Trade amount: {TRADE_AMOUNT_USDT} USDT per symbol")
    print(f"Stop-loss: {STOPLOSS_PERCENT}%, Take-profit: {TAKEPROFIT_PERCENT}%")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    try:
        for symbol in SYMBOLS:
            try:
                print(f"\nChecking {symbol}...")
                signal = check_for_pullback_signal(symbol)
                if signal:
                    current_price = get_current_price(symbol)
                    print(f"Signal detected on last closed candle: {signal.upper()}")
                    place_trade_order(symbol, signal, current_price)
                else:
                    print(f"No valid pullback signal for {symbol}")
            except Exception as e:
                print(f"Error processing {symbol}: {str(e)}")
                send_email_notification(
                    f"Error processing {symbol}",
                    f"Error occurred while processing {symbol}:\n{str(e)}"
                )
                continue
            
            time.sleep(1)  # Rate limiting
            
    except Exception as e:
        error_msg = f"Fatal error in main execution: {str(e)}"
        print(error_msg)
        send_email_notification("Trading Bot Crashed", error_msg)
        sys.exit(1)
