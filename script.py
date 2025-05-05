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
import logging
from pathlib import Path

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

# ===== Setup Logging =====
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir/'trading.log'),
        logging.StreamHandler()
    ]
)

# ===== Initialize Connections =====
bybit = HTTP(
    api_key="lJu52hbBTbPkg2VXZ2",
    api_secret="e43RV6YDZsn24Q9mucr0i4xbU7YytdL2HtuV",
    demo=True
)

bitget = ccxt.bitget({'enableRateLimit': True})

# ===== Trading Functions =====
def send_email(subject, body):
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
        logging.info("Email notification sent")
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")

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
    try:
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
            TRADE EXECUTED
            =============
            Symbol: {symbol}
            Direction: {signal.upper()}
            Quantity: {quantity}
            Entry Price: {price}
            Stop-Loss: {sl_price} ({STOPLOSS_PERCENT}%)
            Take-Profit: {tp_price} ({TAKEPROFIT_PERCENT}%)
            Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            logging.info(trade_details)
            send_email(f"Trade Executed: {signal.upper()} {symbol}", trade_details)
            return True
        else:
            error_msg = f"Order failed: {order['retMsg']}"
            logging.error(error_msg)
            send_email(f"Trade Failed: {symbol}", error_msg)
            return False
            
    except Exception as e:
        logging.error(f"Error in place_trade_order: {str(e)}", exc_info=True)
        return False

# ===== Signal Detection =====
def check_for_pullback_signal(symbol):
    try:
        lagos_tz = pytz.timezone('Africa/Lagos')
        
        # Fetch data
        ohlcv_15m = bitget.fetch_ohlcv(symbol, TIMEFRAME, limit=500)
        ohlcv_1h = bitget.fetch_ohlcv(symbol, '1h', limit=500)
        
        # Create DataFrames
        df_15m = pd.DataFrame(ohlcv_15m, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df_1h = pd.DataFrame(ohlcv_1h, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Process timestamps
        for df in [df_15m, df_1h]:
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(lagos_tz)
            df.set_index('timestamp', inplace=True)
        
        # Calculate indicators
        df_15m['EMA_Fast'] = df_15m['close'].ewm(span=EMA_FAST, adjust=False).mean()
        df_15m['EMA_Slow'] = df_15m['close'].ewm(span=EMA_SLOW, adjust=False).mean()
        df_15m['EMA_Trend'] = df_15m['close'].ewm(span=EMA_TREND, adjust=False).mean()
        
        df_1h['EMA_Trend'] = df_1h['close'].ewm(span=EMA_TREND, adjust=False).mean()
        df_1h_resampled = df_1h['EMA_Trend'].resample('15min').ffill()
        df_15m['EMA_Trend_1h'] = df_1h_resampled
        
        # Generate signals
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
        
        # Conservative entries
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
        
        # Filter by trend
        df_15m['Entry_Up_Filtered'] = df_15m['Entry_Up'] & (df_15m['close'] > df_15m['EMA_Trend']) & (df_15m['close'] > df_15m['EMA_Trend_1h'])
        df_15m['Entry_Down_Filtered'] = df_15m['Entry_Down'] & (df_15m['close'] < df_15m['EMA_Trend']) & (df_15m['close'] < df_15m['EMA_Trend_1h'])
        
        # Track first entries
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
        
        # Check last closed candle
        last_candle = df_15m.iloc[-117]
        
        if last_candle['First_Up_Arrow']:
            return "buy"
        elif last_candle['First_Down_Arrow']:
            return "sell"
        return None
        
    except Exception as e:
        logging.error(f"Error in check_for_pullback_signal: {str(e)}", exc_info=True)
        return None

# ===== Main Execution =====
if __name__ == "__main__":
    logging.info("Starting trading bot execution")
    logging.info(f"Running strategy on {TIMEFRAME} timeframe")
    logging.info(f"Monitoring symbols: {', '.join(SYMBOLS)}")
    
    try:
        for symbol in SYMBOLS:
            try:
                logging.info(f"Checking {symbol}...")
                signal = check_for_pullback_signal(symbol)
                
                if signal:
                    current_price = get_current_price(symbol)
                    logging.info(f"Signal detected: {signal.upper()} at {current_price}")
                    
                    if place_trade_order(symbol, signal, current_price):
                        logging.info("Trade executed successfully. Exiting.")
                        sys.exit(0)
                    else:
                        logging.warning("Trade execution failed. Continuing...")
                else:
                    logging.info(f"No valid signal for {symbol}")
                    
            except Exception as e:
                logging.error(f"Error processing {symbol}: {str(e)}", exc_info=True)
                continue
                
            time.sleep(1)  # Rate limiting
            
        logging.info("Completed all symbol checks with no signals found")
        sys.exit(0)
        
    except Exception as e:
        logging.critical(f"Fatal error in main execution: {str(e)}", exc_info=True)
        send_email("Trading Bot Crashed", f"Critical error: {str(e)}")
        sys.exit(1)
