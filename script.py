import ccxt
import pandas as pd
import pytz
from pybit.unified_trading import HTTP
import time
from datetime import datetime
import os
import sys
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
TRADE_AMOUNT_USDT = 50          # Position size in USDT
STOPLOSS_PERCENT = 2            # 2% stop-loss
TAKEPROFIT_PERCENT = 7.5        # 7.5% take-profit

# Email Configuration
SENDER_EMAIL = "dahmadu071@gmail.com"
RECIPIENT_EMAILS = ["teejeedeeone@gmail.com"]
EMAIL_PASSWORD = "oase wivf hvqn lyhr"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Strategy Parameters (EXACTLY AS IN YOUR ORIGINAL)
EMA_FAST = 38
EMA_SLOW = 62
EMA_TREND = 200
TIMEFRAME = '15m'

# GitHub Actions State File
STATE_FILE = "trade_state.txt"

# ===== Initialize Connections =====
bybit = HTTP(
    api_key="lJu52hbBTbPkg2VXZ2",
    api_secret="e43RV6YDZsn24Q9mucr0i4xbU7YytdL2HtuV",
    demo=True  # Set to False for live trading
)

bitget = ccxt.bitget({
    'enableRateLimit': True
})

# ===== Email Function (NEW) =====
def send_email(subject, body):
    """Send email notification"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(RECIPIENT_EMAILS)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# ===== Trading Functions (EXACTLY AS IN YOUR ORIGINAL) =====
def get_lot_size_info(symbol):
    bybit_symbol = symbol.replace('/USDT:USDT', 'USDT')
    response = bybit.get_instruments_info(category="linear", symbol=bybit_symbol)
    if response['retCode'] == 0:
        return response['result']['list'][0]['lotSizeFilter']
    raise Exception(f"Failed to get lot size info: {response['retMsg']}")

def adjust_quantity(quantity, lot_size_info):
    qty_step = float(lot_size_info['qtyStep'])
    min_qty = float(lot_size_info['minOrderQty'])
    max_qty = float(lot_size_info['maxOrderQty'])
    adjusted_qty = round(quantity / qty_step) * qty_step
    return max(min_qty, min(adjusted_qty, max_qty))

def get_current_price(symbol):
    bybit_symbol = symbol.replace('/USDT:USDT', 'USDT')
    ticker = bybit.get_tickers(category="linear", symbol=bybit_symbol)
    if ticker['retCode'] == 0:
        return float(ticker['result']['list'][0]['lastPrice'])
    raise Exception(f"Failed to get price: {ticker['retMsg']}")

def place_trade_order(symbol, signal, price):
    """EXACTLY YOUR ORIGINAL TRADE EXECUTION LOGIC"""
    bybit_symbol = symbol.replace('/USDT:USDT', 'USDT')
    lot_size_info = get_lot_size_info(symbol)
    
    raw_qty = TRADE_AMOUNT_USDT / price
    quantity = adjust_quantity(raw_qty, lot_size_info)
    
    if signal == "buy":
        sl_price = round(price * (1 - STOPLOSS_PERCENT/100), 4)
        tp_price = round(price * (1 + TAKEPROFIT_PERCENT/100), 4)
        side = "Buy"
    else:
        sl_price = round(price * (1 + STOPLOSS_PERCENT/100), 4)
        tp_price = round(price * (1 - TAKEPROFIT_PERCENT/100), 4)
        side = "Sell"
    
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
        trade_details = f"""
        Symbol: {symbol}
        Direction: {signal.upper()}
        Quantity: {quantity} {bybit_symbol.replace('USDT', '')}
        Entry Price: {price}
        Stop-Loss: {sl_price} ({STOPLOSS_PERCENT}%)
        Take-Profit: {tp_price} ({TAKEPROFIT_PERCENT}%)
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        print(f"Order executed:\n{trade_details}")
        send_email(f"Trade Executed: {signal.upper()} {symbol}", trade_details)
        return True
    else:
        error_msg = f"Order failed for {symbol}: {order['retMsg']}"
        print(error_msg)
        send_email(f"Trade Failed: {symbol}", error_msg)
        return False

# ===== Signal Detection (EXACTLY AS IN YOUR ORIGINAL) =====
def check_for_pullback_signal(symbol):
    lagos_tz = pytz.timezone('Africa/Lagos')
    
    ohlcv_15m = bitget.fetch_ohlcv(symbol, TIMEFRAME, limit=500)
    ohlcv_1h = bitget.fetch_ohlcv(symbol, '1h', limit=500)
    
    df_15m = pd.DataFrame(ohlcv_15m, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_1h = pd.DataFrame(ohlcv_1h, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    for df in [df_15m, df_1h]:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(lagos_tz)
        df.set_index('timestamp', inplace=True)
    
    df_15m['EMA_Fast'] = df_15m['close'].ewm(span=EMA_FAST, adjust=False).mean()
    df_15m['EMA_Slow'] = df_15m['close'].ewm(span=EMA_SLOW, adjust=False).mean()
    df_15m['EMA_Trend'] = df_15m['close'].ewm(span=EMA_TREND, adjust=False).mean()
    
    df_1h['EMA_Trend'] = df_1h['close'].ewm(span=EMA_TREND, adjust=False).mean()
    df_1h_resampled = df_1h['EMA_Trend'].resample('15min').ffill()
    df_15m['EMA_Trend_1h'] = df_1h_resampled
    
    df_15m['Signal'] = 0
    df_15m.loc[
        (df_15m['EMA_Fast'] > df_15m['EMA_Slow']) & 
        (df_15m['EMA_Fast'].shift(1) <= df_15m['EMA_Slow'].shift(1)) & 
        (df_15m['close'] > df_15m['EMA_Trend']) & 
        (df_15m['close'] > df_15m['EMA_Trend_1h']), 
        'Signal'] = 1
    
    df_15m.loc[
        (df_15m['EMA_Fast'] < df_15m['EMA_Slow']) & 
        (df_15m['EMA_Fast'].shift(1) >= df_15m['EMA_Slow'].shift(1)) & 
        (df_15m['close'] < df_15m['EMA_Trend']) & 
        (df_15m['close'] < df_15m['EMA_Trend_1h']), 
        'Signal'] = -1
    
    df_15m['Entry_Up'] = (
        (df_15m['EMA_Fast'] > df_15m['EMA_Slow']) & 
        (df_15m['close'].shift(1) < df_15m['EMA_Fast'].shift(1)) & 
        (df_15m['close'] > df_15m['EMA_Fast'])
    )
    
    df_15m['Entry_Down'] = (
        (df_15m['EMA_Fast'] < df_15m['EMA_Slow']) & 
        (df_15m['close'].shift(1) > df_15m['EMA_Fast'].shift(1)) & 
        (df_15m['close'] < df_15m['EMA_Fast'])
    )
    
    df_15m['Entry_Up_Filtered'] = df_15m['Entry_Up'] & (df_15m['close'] > df_15m['EMA_Trend']) & (df_15m['close'] > df_15m['EMA_Trend_1h'])
    df_15m['Entry_Down_Filtered'] = df_15m['Entry_Down'] & (df_15m['close'] < df_15m['EMA_Trend']) & (df_15m['close'] < df_15m['EMA_Trend_1h'])
    
    df_15m['First_Up_Arrow'] = False
    df_15m['First_Down_Arrow'] = False
    
    last_signal = 0
    for i in range(1, len(df_15m)):
        if df_15m['Signal'].iloc[i] == 1:
            last_signal = 1
        elif df_15m['Signal'].iloc[i] == -1:
            last_signal = -1

        if last_signal == 1 and df_15m['Entry_Up_Filtered'].iloc[i]:
            df_15m.at[df_15m.index[i], 'First_Up_Arrow'] = True
            last_signal = 0
        elif last_signal == -1 and df_15m['Entry_Down_Filtered'].iloc[i]:
            df_15m.at[df_15m.index[i], 'First_Down_Arrow'] = True
            last_signal = 0
    
    last_candle = df_15m.iloc[-2]
    
    if last_candle['First_Up_Arrow']:
        return "buy"
    elif last_candle['First_Down_Arrow']:
        return "sell"
    return None

# ===== Main Execution =====
if __name__ == "__main__":
    print(f"Running strategy on {TIMEFRAME} timeframe")
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
                    print(f"Signal detected: {signal.upper()}")
                    if place_trade_order(symbol, signal, current_price):
                        # Exit after first successful trade
                        print("Trade executed. Exiting script.")
                        sys.exit(0)
                else:
                    print(f"No signal for {symbol}")
            except Exception as e:
                print(f"Error processing {symbol}: {str(e)}")
                continue
            
            time.sleep(1)
            
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        send_email("Trading Bot Crashed", f"Error: {str(e)}")
        sys.exit(1)
