print("""
╔═══*.·:·.☽✧    ✦    ✧☾.·:·.*═══╗
       S T R A T E G Y  
╚═══*.·:·.☽✧    ✦    ✧☾.·:·.*═══╝
""")

import ccxt
import pandas as pd
import pytz
from pybit.unified_trading import HTTP
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

# ===== Configuration =====
SYMBOLS = ['BTC/USDT:USDT', 'ETH/USDT:USDT', 'XRP/USDT:USDT', 'BCH/USDT:USDT', 'LTC/USDT:USDT', 'ADA/USDT:USDT', 'ETC/USDT:USDT', 'LINK/USDT:USDT', 'TRX/USDT:USDT', 'DOT/USDT:USDT', 'DOGE/USDT:USDT', 'SOL/USDT:USDT', 'BNB/USDT:USDT', 'UNI/USDT:USDT', 'ICP/USDT:USDT', 'AAVE/USDT:USDT', 'FIL/USDT:USDT', 'XLM/USDT:USDT', 'ATOM/USDT:USDT', 'XTZ/USDT:USDT', 'SUSHI/USDT:USDT', 'AXS/USDT:USDT', 'THETA/USDT:USDT', 'AVAX/USDT:USDT', 'SHIB/USDT:USDT', 'MANA/USDT:USDT', 'GALA/USDT:USDT', 'SAND/USDT:USDT', 'DYDX/USDT:USDT', 'CRV/USDT:USDT', 'NEAR/USDT:USDT', 'EGLD/USDT:USDT', 'KSM/USDT:USDT', 'AR/USDT:USDT', 'PEOPLE/USDT:USDT', 'LRC/USDT:USDT', 'NEO/USDT:USDT', 'ALICE/USDT:USDT', 'WAVES/USDT:USDT', 'ALGO/USDT:USDT', 'IOTA/USDT:USDT', 'ENJ/USDT:USDT', 'GMT/USDT:USDT', 'ZIL/USDT:USDT', 'IOST/USDT:USDT', 'APE/USDT:USDT', 'RUNE/USDT:USDT', 'KNC/USDT:USDT', 'APT/USDT:USDT', 'CHZ/USDT:USDT', 'ROSE/USDT:USDT', 'ZRX/USDT:USDT', 'KAVA/USDT:USDT', 'ENS/USDT:USDT', 'MTL/USDT:USDT', 'AUDIO/USDT:USDT', 'SXP/USDT:USDT', 'C98/USDT:USDT', 'OP/USDT:USDT', 'RSR/USDT:USDT', 'SNX/USDT:USDT', 'STORJ/USDT:USDT', '1INCH/USDT:USDT', 'COMP/USDT:USDT', 'IMX/USDT:USDT', 'LUNA/USDT:USDT', 'FLOW/USDT:USDT', 'TRB/USDT:USDT', 'QTUM/USDT:USDT', 'API3/USDT:USDT', 'MASK/USDT:USDT', 'WOO/USDT:USDT', 'GRT/USDT:USDT', 'BAND/USDT:USDT', 'STG/USDT:USDT', 'LUNC/USDT:USDT', 'ONE/USDT:USDT', 'JASMY/USDT:USDT', 'MKR/USDT:USDT', 'BAT/USDT:USDT', 'MAGIC/USDT:USDT', 'ALPHA/USDT:USDT', 'LDO/USDT:USDT', 'CELO/USDT:USDT', 'BLUR/USDT:USDT', 'MINA/USDT:USDT', 'CORE/USDT:USDT', 'CFX/USDT:USDT', 'ASTR/USDT:USDT', 'GMX/USDT:USDT', 'ANKR/USDT:USDT', 'ACH/USDT:USDT', 'FET/USDT:USDT', 'FXS/USDT:USDT', 'HOOK/USDT:USDT', 'SSV/USDT:USDT', 'USDC/USDT:USDT', 'LQTY/USDT:USDT', 'STX/USDT:USDT', 'TRU/USDT:USDT', 'HBAR/USDT:USDT', 'INJ/USDT:USDT', 'BEL/USDT:USDT', 'COTI/USDT:USDT', 'VET/USDT:USDT', 'ARB/USDT:USDT', 'LOOKS/USDT:USDT', 'KAIA/USDT:USDT', 'FLM/USDT:USDT', 'CKB/USDT:USDT', 'ID/USDT:USDT', 'JOE/USDT:USDT', 'TLM/USDT:USDT', 'HOT/USDT:USDT', 'CHR/USDT:USDT', 'RDNT/USDT:USDT', 'ICX/USDT:USDT', 'ONT/USDT:USDT', 'NKN/USDT:USDT', 'ARPA/USDT:USDT', 'SFP/USDT:USDT', 'CTSI/USDT:USDT', 'SKL/USDT:USDT', 'RVN/USDT:USDT', 'CELR/USDT:USDT', 'FLOKI/USDT:USDT', 'SPELL/USDT:USDT', 'SUI/USDT:USDT', 'PEPE/USDT:USDT', 'IOTX/USDT:USDT', 'CTK/USDT:USDT', 'UMA/USDT:USDT', 'TURBO/USDT:USDT', 'BSV/USDT:USDT', 'TON/USDT:USDT', 'GTC/USDT:USDT', 'DENT/USDT:USDT', 'ZEN/USDT:USDT', 'PHB/USDT:USDT', 'ORDI/USDT:USDT', '1000BONK/USDT:USDT', 'LEVER/USDT:USDT', 'USTC/USDT:USDT', 'RAD/USDT:USDT', 'QNT/USDT:USDT', 'MAV/USDT:USDT', 'XVG/USDT:USDT', '1000XEC/USDT:USDT', 'AGLD/USDT:USDT', 'WLD/USDT:USDT', 'PENDLE/USDT:USDT', 'ARKM/USDT:USDT', 'CVX/USDT:USDT', 'YGG/USDT:USDT', 'OGN/USDT:USDT', 'LPT/USDT:USDT', 'BNT/USDT:USDT', 'SEI/USDT:USDT', 'CYBER/USDT:USDT', 'BAKE/USDT:USDT', 'BIGTIME/USDT:USDT', 'WAXP/USDT:USDT', 'POLYX/USDT:USDT', 'TIA/USDT:USDT', 'MEME/USDT:USDT', 'PYTH/USDT:USDT', 'JTO/USDT:USDT', '1000SATS/USDT:USDT', '1000RATS/USDT:USDT', 'ACE/USDT:USDT', 'XAI/USDT:USDT', 'MANTA/USDT:USDT', 'ALT/USDT:USDT', 'JUP/USDT:USDT', 'ZETA/USDT:USDT', 'STRK/USDT:USDT', 'PIXEL/USDT:USDT', 'DYM/USDT:USDT', 'WIF/USDT:USDT', 'AXL/USDT:USDT', 'BEAM/USDT:USDT', 'BOME/USDT:USDT', 'METIS/USDT:USDT', 'NFP/USDT:USDT', 'VANRY/USDT:USDT', 'AEVO/USDT:USDT', 'ETHFI/USDT:USDT', 'OM/USDT:USDT', 'ONDO/USDT:USDT', 'CAKE/USDT:USDT', 'PORTAL/USDT:USDT', 'NTRN/USDT:USDT', 'KAS/USDT:USDT', 'AI/USDT:USDT', 'ENA/USDT:USDT', 'W/USDT:USDT', 'CVC/USDT:USDT', 'TNSR/USDT:USDT', 'SAGA/USDT:USDT', 'TAO/USDT:USDT', 'RAY/USDT:USDT', 'ATA/USDT:USDT', 'SUPER/USDT:USDT', 'ONG/USDT:USDT', 'OMNI1/USDT:USDT', 'LSK/USDT:USDT', 'GLM/USDT:USDT', 'REZ/USDT:USDT', 'XVS/USDT:USDT', 'MOVR/USDT:USDT', 'BB/USDT:USDT', 'NOT/USDT:USDT', 'BICO/USDT:USDT', 'HIFI/USDT:USDT', 'IO/USDT:USDT', 'TAIKO/USDT:USDT', 'BRETT/USDT:USDT', 'ATH/USDT:USDT', 'ZK/USDT:USDT', 'MEW/USDT:USDT', 'LISTA/USDT:USDT', 'ZRO/USDT:USDT', 'BLAST/USDT:USDT', 'DOG/USDT:USDT', 'PAXG/USDT:USDT', 'ZKJ/USDT:USDT', 'BGB/USDT:USDT', 'MOCA/USDT:USDT', 'GAS/USDT:USDT', 'UXLINK/USDT:USDT', 'BANANA/USDT:USDT', 'MYRO/USDT:USDT', 'POPCAT/USDT:USDT', 'PRCL/USDT:USDT', 'CLOUD/USDT:USDT', 'AVAIL/USDT:USDT', 'RENDER/USDT:USDT', 'RARE/USDT:USDT', 'PONKE/USDT:USDT', 'T/USDT:USDT', '1000000MOG/USDT:USDT', 'G/USDT:USDT', 'SYN/USDT:USDT', 'SYS/USDT:USDT', 'VOXEL/USDT:USDT', 'SUN/USDT:USDT', 'DOGS/USDT:USDT', 'ORDER/USDT:USDT', 'SUNDOG/USDT:USDT', 'AKT/USDT:USDT', 'MBOX/USDT:USDT', 'HNT/USDT:USDT', 'CHESS/USDT:USDT', 'FLUX/USDT:USDT', 'POL/USDT:USDT', 'BSW/USDT:USDT', 'NEIROETH/USDT:USDT', 'RPL/USDT:USDT', 'QUICK/USDT:USDT', 'AERGO/USDT:USDT', '1MBABYDOGE/USDT:USDT', '1000CAT/USDT:USDT', 'KDA/USDT:USDT', 'FIDA/USDT:USDT', 'CATI/USDT:USDT', 'FIO/USDT:USDT', 'ARK/USDT:USDT', 'GHST/USDT:USDT', 'LOKA/USDT:USDT', 'VELO/USDT:USDT', 'HMSTR/USDT:USDT', 'AGI/USDT:USDT', 'REI/USDT:USDT', 'COS/USDT:USDT', 'EIGEN/USDT:USDT', 'MOODENG/USDT:USDT', 'DIA/USDT:USDT', 'FTN/USDT:USDT', 'OG/USDT:USDT', 'NEIROCTO/USDT:USDT', 'ETHW/USDT:USDT', 'DegenReborn/USDT:USDT', 'KMNO/USDT:USDT', 'POWR/USDT:USDT', 'PYR/USDT:USDT', 'CARV/USDT:USDT', 'SLERF/USDT:USDT', 'PUFFER/USDT:USDT', '10000WHY/USDT:USDT', 'DEEP/USDT:USDT', 'DBR/USDT:USDT', 'LUMIA/USDT:USDT', 'SCR/USDT:USDT', 'GOAT/USDT:USDT', 'X/USDT:USDT', 'SAFE/USDT:USDT', 'GRASS/USDT:USDT', 'SWEAT/USDT:USDT', 'SANTOS/USDT:USDT', 'SPX/USDT:USDT', 'VIRTUAL/USDT:USDT', 'AERO/USDT:USDT', 'CETUS/USDT:USDT', 'COW/USDT:USDT', 'SWELL/USDT:USDT', 'DRIFT/USDT:USDT', 'PNUT/USDT:USDT', 'ACT/USDT:USDT', 'CRO/USDT:USDT', 'PEAQ/USDT:USDT', 'FWOG/USDT:USDT', 'HIPPO/USDT:USDT', 'SNT/USDT:USDT', 'MERL/USDT:USDT', 'STEEM/USDT:USDT', 'BAN/USDT:USDT', 'OL/USDT:USDT', 'MORPHO/USDT:USDT', 'SCRT/USDT:USDT', 'CHILLGUY/USDT:USDT', '1MCHEEMS/USDT:USDT', 'OXT/USDT:USDT', 'ZRC/USDT:USDT', 'THE/USDT:USDT', 'MAJOR/USDT:USDT', 'CTC/USDT:USDT', 'XDC/USDT:USDT', 'XION/USDT:USDT', 'ORCA/USDT:USDT', 'ACX/USDT:USDT', 'NS/USDT:USDT', 'MOVE/USDT:USDT', 'KOMA/USDT:USDT', 'ME/USDT:USDT', 'VELODROME/USDT:USDT', 'AVA/USDT:USDT', 'VANA/USDT:USDT', 'HYPE/USDT:USDT', 'PENGU/USDT:USDT', 'USUAL/USDT:USDT', 'FUEL/USDT:USDT', 'CGPT/USDT:USDT', 'AIXBT/USDT:USDT', 'FARTCOIN/USDT:USDT', 'HIVE/USDT:USDT', 'DEXE/USDT:USDT', 'GIGA/USDT:USDT', 'PHA/USDT:USDT', 'DF/USDT:USDT', 'AI16Z/USDT:USDT', 'GRIFFAIN/USDT:USDT', 'ZEREBRO/USDT:USDT', 'BIO/USDT:USDT', 'SWARMS/USDT:USDT', 'ALCH/USDT:USDT', 'COOKIE/USDT:USDT', 'SONIC/USDT:USDT', 'AVAAI/USDT:USDT', 'S/USDT:USDT', 'PROM/USDT:USDT', 'DUCK/USDT:USDT', 'BGSC/USDT:USDT', 'SOLV/USDT:USDT', 'ARC/USDT:USDT', 'NC/USDT:USDT', 'PIPPIN/USDT:USDT', 'TRUMP/USDT:USDT', 'MELANIA/USDT:USDT', 'PLUME/USDT:USDT', 'VTHO/USDT:USDT', 'J/USDT:USDT', 'VINE/USDT:USDT', 'ANIME/USDT:USDT', 'XCN/USDT:USDT', 'TOSHI/USDT:USDT', 'VVV/USDT:USDT', 'FORTH/USDT:USDT', 'BERA/USDT:USDT', 'TSTBSC/USDT:USDT', '10000ELON/USDT:USDT', 'LAYER/USDT:USDT', 'B3/USDT:USDT', 'IP/USDT:USDT', 'RON/USDT:USDT', 'HEI/USDT:USDT', 'SHELL/USDT:USDT', 'BROCCOLI/USDT:USDT', 'AUCTION/USDT:USDT', 'GPS/USDT:USDT', 'GNO/USDT:USDT', 'AIOZ/USDT:USDT', 'PI/USDT:USDT', 'AVL/USDT:USDT', 'KAITO/USDT:USDT', 'GODS/USDT:USDT', 'ROAM/USDT:USDT', 'RED/USDT:USDT', 'ELX/USDT:USDT', 'SERAPH/USDT:USDT', 'BMT/USDT:USDT', 'VIC/USDT:USDT', 'EPIC/USDT:USDT', 'OBT/USDT:USDT', 'MUBARAK/USDT:USDT', 'NMR/USDT:USDT', 'TUT/USDT:USDT', 'FORM/USDT:USDT', 'RSS3/USDT:USDT', 'BID/USDT:USDT', 'SIREN/USDT:USDT', 'BROCCOLIF3B/USDT:USDT', 'BANANAS31/USDT:USDT', 'BR/USDT:USDT', 'NIL/USDT:USDT', 'PARTI/USDT:USDT', 'NAVX/USDT:USDT', 'WAL/USDT:USDT', 'KILO/USDT:USDT', 'FUN/USDT:USDT', 'MLN/USDT:USDT', 'GUN/USDT:USDT', 'PUMP/USDT:USDT', 'STO/USDT:USDT', 'XAUT/USDT:USDT', 'AMP/USDT:USDT', 'BABY/USDT:USDT', 'FHE/USDT:USDT', 'PROMPT/USDT:USDT', 'RFC/USDT:USDT', 'KERNEL/USDT:USDT', 'WCT/USDT:USDT', 'PAWS/USDT:USDT', '10000000AIDOGE/USDT:USDT', 'BANK/USDT:USDT', 'EPT/USDT:USDT', 'HYPER/USDT:USDT', 'ZORA/USDT:USDT', 'INIT/USDT:USDT', 'DOLO/USDT:USDT', 'FIS/USDT:USDT', 'DARK/USDT:USDT', 'JST/USDT:USDT', 'TAI/USDT:USDT', 'SIGN/USDT:USDT', 'MILK/USDT:USDT', 'HAEDAL/USDT:USDT', 'PUNDIX/USDT:USDT', 'B2/USDT:USDT', 'AIOT/USDT:USDT', 'GORK/USDT:USDT', 'HOUSE/USDT:USDT', 'ASR/USDT:USDT', 'ALPINE/USDT:USDT', 'MYX/USDT:USDT', 'SYRUP/USDT:USDT', 'OBOL/USDT:USDT', 'SXT/USDT:USDT', 'SHM/USDT:USDT', 'DOOD/USDT:USDT', 'SKYAI/USDT:USDT', 'RDAC/USDT:USDT', 'LAUNCHCOIN/USDT:USDT', 'PRAI/USDT:USDT', 'NXPC/USDT:USDT', 'BADGER/USDT:USDT', 'AGT/USDT:USDT', 'AWE/USDT:USDT', 'TGT/USDT:USDT', 'BLUE/USDT:USDT']
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

# API Configuration
API_KEY = "4eQbf5STelVE40HOtB"
API_SECRET = "bzo7oS1u8jxHIpkpFzy9mDLMvRrARJcXlKxt"
DEMO_MODE = True

# ===== Initialize Connections =====
bybit = HTTP(
    api_key=API_KEY,
    api_secret=API_SECRET,
    demo=DEMO_MODE
)

bitget = ccxt.bitget({
    'enableRateLimit': True
})

# ===== Helper Functions =====
def convert_symbol_to_bitget(symbol):
    """Convert symbol from Bybit format (BTCUSDT) to Bitget format (BTC/USDT:USDT)"""
    if isinstance(symbol, str):
        if 'USDT' in symbol and '/' not in symbol:
            return f"{symbol.replace('USDT', '')}/USDT:USDT"
    return symbol

def convert_symbol_to_bybit(symbol):
    """Convert symbol from Bitget format (BTC/USDT:USDT) to Bybit format (BTCUSDT)"""
    if isinstance(symbol, str):
        if '/' in symbol:
            return symbol.split('/')[0] + 'USDT'
    return symbol

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
def get_lot_size_info(symbol):
    """Get the lot size rules for the symbol"""
    bybit_symbol = convert_symbol_to_bybit(symbol)
    response = bybit.get_instruments_info(category="linear", symbol=bybit_symbol)
    if response['retCode'] == 0:
        return response['result']['list'][0]['lotSizeFilter']
    raise Exception(f"Failed to get lot size info: {response['retMsg']}")

def adjust_quantity(quantity, lot_size_info):
    """Adjust quantity to comply with exchange rules"""
    qty_step = float(lot_size_info['qtyStep'])
    min_qty = float(lot_size_info['minOrderQty'])
    max_qty = float(lot_size_info['maxOrderQty'])
    return max(min_qty, min(round(quantity / qty_step) * qty_step, max_qty))

def get_current_price(symbol):
    """Get the current market price"""
    bybit_symbol = convert_symbol_to_bybit(symbol)
    ticker = bybit.get_tickers(category="linear", symbol=bybit_symbol)
    if ticker['retCode'] == 0:
        return float(ticker['result']['list'][0]['lastPrice'])
    raise Exception(f"Failed to get price: {ticker['retMsg']}")

def place_trade_order(symbol, signal, price):
    """Place the trade order with stop-loss and take-profit"""
    bybit_symbol = convert_symbol_to_bybit(symbol)
    lot_size_info = get_lot_size_info(symbol)
    quantity = adjust_quantity(TRADE_AMOUNT_USDT / price, lot_size_info)

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
        trade_details = f"""Symbol: {symbol}
Direction: {signal.upper()}
Quantity: {quantity}
Entry Price: {price}
Stop-Loss: {sl_price} ({STOPLOSS_PERCENT}%)
Take-Profit: {tp_price} ({TAKEPROFIT_PERCENT}%)
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        print(f"\nOrder executed successfully for {symbol}:")
        print(trade_details)
        send_email_notification(f"Trade Executed: {signal.upper()} {symbol}", trade_details)
    else:
        error_msg = f"Order failed for {symbol}: {order['retMsg']}"
        print(error_msg)
        send_email_notification(f"Trade Failed: {symbol}", error_msg)

# ===== Market Data Functions =====
def fetch_market_data(symbol, timeframe, limit=500):
    """Fetch OHLCV data with proper timezone handling"""
    try:
        ccxt_symbol = convert_symbol_to_bitget(symbol)
        ohlcv = bitget.fetch_ohlcv(ccxt_symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(pytz.timezone('Africa/Lagos'))
        df.set_index('timestamp', inplace=True)
        df['EMA'] = df['close'].ewm(span=EMA_TREND, adjust=False).mean()
        return df
    except Exception as e:
        print(f"Error fetching market data for {symbol}: {e}")
        return None

def detect_trend(df, candle_index):
    """Determine trend for a specific candle"""
    if candle_index < 1 or candle_index >= len(df):
        return "Sideways"

    ema_current = df['EMA'].iloc[candle_index]
    ema_prev = df['EMA'].iloc[candle_index-1]
    price = df['close'].iloc[candle_index]

    if ema_current > ema_prev and price > ema_current:
        return "Uptrend"
    elif ema_current < ema_prev and price < ema_current:
        return "Downtrend"
    return "Sideways"

# ===== Trade Analysis Functions =====
def get_last_closed_trade():
    """Get details of the most recent closed trade"""
    try:
        trades = bybit.get_executions(category="linear", limit=50)
        if trades["retCode"] != 0:
            print(f"Error fetching trades: {trades['retMsg']}")
            return None

        trades = trades["result"]["list"]
        if not trades:
            return None

        for trade in sorted(trades, key=lambda x: int(x["execTime"]), reverse=True):
            symbol = trade["symbol"]
            positions = bybit.get_positions(category="linear", symbol=symbol)
            if positions["retCode"] != 0:
                continue

            if not any(float(p["size"]) > 0 for p in positions["result"]["list"]) and trade["closedSize"]:
                return {
                    "symbol": symbol,
                    "symbol_display": convert_symbol_to_bitget(symbol),
                    "close_time": datetime.fromtimestamp(int(trade["execTime"])/1000, pytz.UTC).astimezone(pytz.timezone('Africa/Lagos')),
                    "close_price": float(trade["execPrice"]),
                    "side": "LONG" if trade["side"] == "Sell" else "SHORT"
                }
        return None
    except Exception as e:
        print(f"Error fetching trade history: {e}")
        return None

def has_open_positions():
    """Check if there are any open positions"""
    try:
        positions = bybit.get_positions(category="linear", settleCoin="USDT")
        return positions['retCode'] == 0 and any(float(p['size']) > 0 for p in positions['result']['list'])
    except Exception as e:
        print(f"Error checking open positions: {e}")
        return True

def has_pending_orders():
    """Check if there are any pending orders"""
    try:
        active_orders = bybit.get_open_orders(category="linear", settleCoin="USDT")
        if active_orders['retCode'] == 0 and active_orders['result']['list']:
            return True

        conditional_orders = bybit.get_open_orders(
            category="linear",
            orderFilter='StopOrder',
            settleCoin="USDT"
        )
        return conditional_orders['retCode'] == 0 and conditional_orders['result']['list']
    except Exception as e:
        print(f"Error checking pending orders: {e}")
        return True

def get_first_trend_flip_details(symbol, close_time, trade_side):
    """Get detailed information about the first trend flip after trade close"""
    try:
        df = fetch_market_data(symbol, '15m', 500)
        if df is None or len(df) < 2:
            return None

        close_candle_idx = df.index.get_indexer([close_time], method='nearest')[0]
        if close_candle_idx < 1:
            close_candle_idx = 1

        for i in range(close_candle_idx + 1, len(df)):
            current_trend = detect_trend(df, i)

            if (trade_side == "LONG" and current_trend == "Downtrend") or \
               (trade_side == "SHORT" and current_trend == "Uptrend"):
                return {
                    'time': df.index[i],
                    'new_trend': current_trend,
                    'price': df['close'].iloc[i],
                    'ema_value': df['EMA'].iloc[i],
                    'formatted_time': df.index[i].strftime('%Y-%m-%d %H:%M:%S')
                }
        return None
    except Exception as e:
        print(f"Error checking trend flip: {e}")
        return None

def should_block_signals():
    """Determine if we should block signal checking"""
    if has_open_positions():
        print("Blocking signals: Open positions exist")
        return True

    if has_pending_orders():
        print("Blocking signals: Pending orders exist")
        return True

    last_trade = get_last_closed_trade()
    if not last_trade:
        return False

    print(f"\nLast trade was {last_trade['side']} on {last_trade['symbol_display']}")
    print(f"Closed at: {last_trade['close_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Close Price: {last_trade['close_price']}")

    # Check for counter-trend closing
    df = fetch_market_data(last_trade['symbol'], '15m', 500)
    if df is not None and len(df) > 1:
        close_candle_idx = df.index.get_indexer([last_trade['close_time']], method='nearest')[0]
        trend_at_close = detect_trend(df, close_candle_idx)

        is_counter_trend = (
            (last_trade['side'] == "LONG" and trend_at_close == "Downtrend") or
            (last_trade['side'] == "SHORT" and trend_at_close == "Uptrend")
        )

        if is_counter_trend:
            print("\n⚠️ Last trade was counter-trend closing")
            print("Allowing signal checking without trend flip requirement")
            return False

    # For normal closings, require trend flip
    flip_details = get_first_trend_flip_details(
        last_trade['symbol'],
        last_trade['close_time'],
        last_trade['side']
    )

    if flip_details:
        print(f"\n✅ Trend flip detected after normal closing:")
        print(f"Flip Time: {flip_details['formatted_time']}")
        print(f"New Trend: {flip_details['new_trend']}")
        print(f"Price at Flip: {flip_details['price']}")
        return False
    else:
        print("\nBlocking signals: No trend flip detected after normal closing")
        return True

# ===== Strategy Functions =====
def check_for_pullback_signal(symbol):
    """Check for first pullback signal on last closed candle"""
    try:
        ohlcv_15m = bitget.fetch_ohlcv(convert_symbol_to_bitget(symbol), TIMEFRAME, limit=500)
        ohlcv_1h = bitget.fetch_ohlcv(convert_symbol_to_bitget(symbol), '1h', limit=500)

        df_15m = pd.DataFrame(ohlcv_15m, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df_1h = pd.DataFrame(ohlcv_1h, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        for df in [df_15m, df_1h]:
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(pytz.timezone('Africa/Lagos'))
            df.set_index('timestamp', inplace=True)

        # Calculate EMAs
        df_15m['EMA_Fast'] = df_15m['close'].ewm(span=EMA_FAST, adjust=False).mean()
        df_15m['EMA_Slow'] = df_15m['close'].ewm(span=EMA_SLOW, adjust=False).mean()
        df_15m['EMA_Trend'] = df_15m['close'].ewm(span=EMA_TREND, adjust=False).mean()
        df_1h['EMA_Trend'] = df_1h['close'].ewm(span=EMA_TREND, adjust=False).mean()

        # Resample 1h EMA to 15m
        df_15m['EMA_Trend_1h'] = df_1h['EMA_Trend'].resample('15min').ffill()

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

        # Conservative pullback entries
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

        # Track first conservative entry after each signal
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

    except Exception as e:
        print(f"Error checking pullback signal for {symbol}: {e}")
        return None

# ===== Main Execution =====
if __name__ == "__main__":
    print(f"Running multi-symbol strategy on {TIMEFRAME} timeframe")
    print(f"Trade amount: {TRADE_AMOUNT_USDT} USDT per symbol")
    print(f"Stop-loss: {STOPLOSS_PERCENT}%, Take-profit: {TAKEPROFIT_PERCENT}%")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

    try:
        if should_block_signals():
            print("\nSignal checking blocked due to one or more conditions")
            print("1. Open positions exist OR")
            print("2. Pending orders exist OR")
            print("3. No trend flip after normal closing")
            sys.exit(0)

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

            time.sleep(1)

    except Exception as e:
        error_msg = f"Fatal error in main execution: {str(e)}"
        print(error_msg)
        send_email_notification("Trading Bot Crashed", error_msg)





print("""
  ⚙️▬▬ι═══════ﺤ -═══════ι▬▬⚙️
     C R O S S U N D E R  
  ⚙️▬▬ι═══════ﺤ -═══════ι▬▬⚙️
""")



import ccxt
import pandas as pd
import numpy as np
from pybit.unified_trading import HTTP
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import pytz

# Initialize exchanges and trading session
exchange = ccxt.bitget()
session = HTTP(
    api_key="4eQbf5STelVE40HOtB",
    api_secret="bzo7oS1u8jxHIpkpFzy9mDLMvRrARJcXlKxt",
    demo=True
)

# Timezone setup
LAGOS_TZ = pytz.timezone('Africa/Lagos')
UTC_TZ = pytz.UTC

# Settings
timeframe = '15m'
limit = 500
h = 8.0
mult = 3.0
repaint = True
len_ema = 200
STOP_LOSS_PERCENT = 2.0  # 2% stop loss
TAKE_PROFIT_PERCENT = 10.0  # 10% take profit

# Email settings
SENDER_EMAIL = "dahmadu071@gmail.com"
RECIPIENT_EMAILS = ["teejeedeeone@gmail.com"]
EMAIL_PASSWORD = "oase wivf hvqn lyhr"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def format_pnl(pnl):
    """Format PnL with proper sign and profit/loss indication"""
    if pnl > 0:
        return f"+{pnl:.2f}% (Profit)"
    elif pnl < 0:
        return f"{pnl:.2f}% (Loss)"
    return f"{pnl:.2f}% (Break-even)"

def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAILS
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email notification sent")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_pybit_symbol(ccxt_symbol):
    """Convert CCXT symbol to Bybit symbol format"""
    return ccxt_symbol.split('/')[0] + ccxt_symbol.split('/')[1].split(':')[0]

def gauss(x, h):
    """Gaussian window function"""
    return np.exp(-(x ** 2) / (h ** 2 * 2))

def calculate_nwe(src, h, mult, repaint):
    """Calculate Nadaraya-Watson Envelope"""
    n = len(src)
    out = np.zeros(n)
    mae = np.zeros(n)
    upper = np.zeros(n)
    lower = np.zeros(n)
    
    if not repaint:
        coefs = np.array([gauss(i, h) for i in range(n)])
        den = np.sum(coefs)
        
        for i in range(n):
            out[i] = np.sum(src * coefs) / den
        
        mae = pd.Series(np.abs(src - out)).rolling(499).mean().values * mult
        upper = out + mae
        lower = out - mae
    else:
        nwe = []
        sae = 0.0
        
        for i in range(n):
            sum_val = 0.0
            sumw = 0.0
            for j in range(n):
                w = gauss(i - j, h)
                sum_val += src[j] * w
                sumw += w
            y2 = sum_val / sumw
            nwe.append(y2)
            sae += np.abs(src[i] - y2)
        
        sae = (sae / n) * mult
        
        for i in range(n):
            upper[i] = nwe[i] + sae
            lower[i] = nwe[i] - sae
            out[i] = nwe[i]
    
    return out, upper, lower

def detect_crossunder(close, lower):
    """Detect crossunder condition"""
    return (close.shift(1) > lower.shift(1)) & (close < lower)

def fetch_market_data(symbol, timeframe, limit=500):
    """Fetch OHLCV data with proper timezone handling"""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(LAGOS_TZ)
        df.set_index('timestamp', inplace=True)
        df['EMA'] = df['close'].ewm(span=len_ema, adjust=False).mean()
        return df
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None

def detect_trend(df, candle_index):
    """Determine trend for a specific candle"""
    if candle_index < 1 or candle_index >= len(df):
        return "Sideways"
    
    ema_current = df['EMA'].iloc[candle_index]
    ema_prev = df['EMA'].iloc[candle_index-1]
    price = df['close'].iloc[candle_index]
    
    if ema_current > ema_prev and price > ema_current:
        return "Uptrend"
    elif ema_current < ema_prev and price < ema_current:
        return "Downtrend"
    return "Sideways"

def get_most_recent_open_trade_symbol():
    """Get symbol of most recent open trade"""
    try:
        executions = session.get_executions(
            category="linear",
            limit=50,
            settleCoin="USDT"
        )
        
        if executions["retCode"] != 0:
            print(f"Error fetching executions: {executions['retMsg']}")
            return None
            
        if not executions["result"]["list"]:
            return None
            
        for trade in sorted(executions["result"]["list"], 
                          key=lambda x: int(x["execTime"]), 
                          reverse=True):
            if trade["execType"] == "Trade" and float(trade["execQty"]) > 0:
                positions = session.get_positions(
                    category="linear",
                    symbol=trade["symbol"]
                )
                
                if positions["retCode"] == 0 and positions["result"]["list"]:
                    for position in positions["result"]["list"]:
                        if position["symbol"] == trade["symbol"] and float(position["size"]) > 0:
                            return f"{trade['symbol'].replace('USDT', '')}/USDT:USDT"
        
        return None
    except Exception as e:
        print(f"Error checking trades: {e}")
        return None

def get_open_trade(symbol):
    """Get details of open trade for specified symbol"""
    try:
        pybit_symbol = get_pybit_symbol(symbol)
        positions = session.get_positions(
            category="linear",
            symbol=pybit_symbol
        )
        if positions["retCode"] == 0 and positions["result"]["list"]:
            for position in positions["result"]["list"]:
                if position["symbol"] == pybit_symbol and float(position["size"]) > 0:
                    unrealized_pnl = float(position['unrealisedPnl'])
                    return {
                        'side': position['side'],
                        'size': float(position['size']),
                        'entry_price': float(position['avgPrice']),
                        'unrealized_pnl': unrealized_pnl,
                        'pnl_status': format_pnl(unrealized_pnl),
                        'created_time': datetime.fromtimestamp(int(position['createdTime'])/1000, UTC_TZ).astimezone(LAGOS_TZ)
                    }
        return None
    except Exception as e:
        print(f"Error checking open positions: {e}")
        return None

def get_last_closed_trade():
    """Get details of last closed trade"""
    try:
        trades = session.get_executions(
            category="linear",
            limit=50,
            settleCoin="USDT"
        )
        
        if trades["retCode"] != 0:
            print(f"Error fetching trades: {trades['retMsg']}")
            return None
            
        trades = trades["result"]["list"]
        if not trades:
            return None

        for trade in sorted(trades, key=lambda x: int(x["execTime"]), reverse=True):
            symbol = trade["symbol"]
            positions = session.get_positions(
                category="linear",
                symbol=symbol
            )
            
            if positions["retCode"] != 0:
                continue
                
            position_open = any(float(p["size"]) > 0 for p in positions["result"]["list"])
            
            if not position_open and trade["closedSize"]:
                utc_time = datetime.fromtimestamp(int(trade["execTime"])/1000, UTC_TZ)
                lagos_time = utc_time.astimezone(LAGOS_TZ)
                
                if trade['side'] == 'Sell':  # Closing long
                    trade_type = 'Long Close'
                    actual_side = 'Buy'
                    entry_price = float(trade["avgEntryPrice"]) if "avgEntryPrice" in trade else float(trade["execPrice"])
                    exit_price = float(trade["execPrice"])
                    pnl_percent = ((exit_price - entry_price) / entry_price) * 100
                else:  # Closing short
                    trade_type = 'Short Close'
                    actual_side = 'Sell'
                    entry_price = float(trade["avgEntryPrice"]) if "avgEntryPrice" in trade else float(trade["execPrice"])
                    exit_price = float(trade["execPrice"])
                    pnl_percent = ((entry_price - exit_price) / entry_price) * 100
                
                return {
                    'symbol': f"{symbol.replace('USDT', '')}/USDT:USDT",
                    'type': trade_type,
                    'side': actual_side,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'pnl': pnl_percent,
                    'pnl_status': format_pnl(pnl_percent),
                    'closed_time': lagos_time,
                    'utc_close_time': utc_time
                }
        return None
    except Exception as e:
        print(f"Error fetching trade history: {e}")
        return None

def analyze_trend_since_close(symbol, since_timestamp):
    """Analyze trend changes since trade close (matches your reference script)"""
    try:
        df = fetch_market_data(symbol, timeframe, limit)
        if df is None or len(df) < 2:
            return None, "Error: Not enough market data"
        
        # Find the candle where trade was closed
        close_candle_idx = df.index.get_indexer([since_timestamp], method='nearest')[0]
        if close_candle_idx < 1:
            close_candle_idx = 1
        
        # Get trend at close time
        trend_at_close = detect_trend(df, close_candle_idx)
        
        # Check for counter-trend closing
        last_trade = get_last_closed_trade()
        if last_trade:
            if (last_trade['side'] == "Sell" and trend_at_close == "Uptrend") or \
               (last_trade['side'] == "Buy" and trend_at_close == "Downtrend"):
                return None, "⚠️ COUNTER-TREND CLOSING DETECTED"
        
        # Analyze trend changes
        current_trend = trend_at_close
        first_flip = None
        
        for i in range(close_candle_idx + 1, len(df)):
            new_trend = detect_trend(df, i)
            
            if new_trend != current_trend and new_trend in ["Uptrend", "Downtrend"]:
                first_flip = {
                    'time': df.index[i],
                    'new_trend': new_trend,
                    'price': df['close'].iloc[i],
                    'candle_time': df.index[i].strftime('%Y-%m-%d %H:%M:%S')
                }
                break
        
        if first_flip:
            duration = first_flip['time'] - since_timestamp
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            return first_flip, f"FIRST TREND FLIP: {first_flip['new_trend']} at {first_flip['candle_time']} ({hours}h {minutes}m after close)"
        
        return None, "✅ No trend flips detected since closing"
    
    except Exception as e:
        print(f"Error analyzing trend: {e}")
        return None, f"Error analyzing trend: {e}"

def check_crossunder(symbol):
    """Check for crossunder condition on specified symbol"""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        src = df['close'].values
        out, upper, lower = calculate_nwe(src, h, mult, repaint)
        
        close_series = pd.Series(src)
        lower_series = pd.Series(lower)
        crossunder = detect_crossunder(close_series, lower_series)
        
        return crossunder.iloc[-246]
    except Exception as e:
        print(f"Error checking crossunder: {e}")
        return False

def cancel_all_pending_orders(symbol):
    """Cancel all pending orders for specified symbol"""
    try:
        pybit_symbol = get_pybit_symbol(symbol)
        response = session.cancel_all_orders(
            category="linear",
            symbol=pybit_symbol
        )
        if response["retCode"] == 0:
            print("All pending orders canceled")
            return True
        else:
            print(f"Failed to cancel orders: {response['retMsg']}")
            return False
    except Exception as e:
        print(f"Error canceling orders: {e}")
        return False

def place_long_market_order(symbol, usdt_amount=50):
    """Place long market order for specified symbol"""
    try:
        pybit_symbol = get_pybit_symbol(symbol)
        
        ticker = session.get_tickers(category="linear", symbol=pybit_symbol)
        market_price = float(ticker["result"]["list"][0]["lastPrice"])
        
        instrument_info = session.get_instruments_info(category="linear", symbol=pybit_symbol)
        lot_size = instrument_info["result"]["list"][0]["lotSizeFilter"]
        qty_step = float(lot_size["qtyStep"])
        
        quantity = round((usdt_amount / market_price) / qty_step) * qty_step
        
        # Calculate stop loss and take profit prices
        stop_loss_price = market_price * (1 - STOP_LOSS_PERCENT/100)
        take_profit_price = market_price * (1 + TAKE_PROFIT_PERCENT/100)
        
        response = session.place_order(
            category="linear",
            symbol=pybit_symbol,
            side="Buy",
            orderType="Market",
            qty=str(quantity),
            stopLoss=str(stop_loss_price),
            takeProfit=str(take_profit_price)
        )
        
        if response["retCode"] == 0:
            msg = f"""Long market order placed for {quantity} {symbol.split('/')[0]} at {market_price}
Stop Loss: {stop_loss_price:.4f} ({STOP_LOSS_PERCENT}%)
Take Profit: {take_profit_price:.4f} ({TAKE_PROFIT_PERCENT}%)"""
            print(msg)
            send_email("Long Position Opened", msg)
            return True
        else:
            print(f"Failed to place order: {response['retMsg']}")
            return False
    except Exception as e:
        print(f"Error placing long order: {e}")
        return False

def close_short_position(symbol):
    """Close short position for specified symbol"""
    try:
        pybit_symbol = get_pybit_symbol(symbol)
        position = get_open_trade(symbol)
        
        if position and position['side'] == 'Sell':
            ticker = session.get_tickers(category="linear", symbol=pybit_symbol)
            market_price = float(ticker["result"]["list"][0]["lastPrice"])
            
            response = session.place_order(
                category="linear",
                symbol=pybit_symbol,
                side="Buy",
                orderType="Market",
                qty=str(position['size'])
            )
            
            if response["retCode"] == 0:
                msg = f"Short position closed at {market_price}. PnL: {position['pnl_status']}"
                print(msg)
                send_email("Short Position Closed", msg)
                return True
            else:
                print(f"Failed to close short position: {response['retMsg']}")
                return False
        return False
    except Exception as e:
        print(f"Error closing short position: {e}")
        return False

def main():
    print(f"\n🚀 Starting Crossunder Strategy at {datetime.now(LAGOS_TZ).strftime('%Y-%m-%d %H:%M:%S')} Lagos Time\n")
    
    # 1. Check for any open trades
    open_symbol = get_most_recent_open_trade_symbol()
    if open_symbol:
        print(f"🔍 Open Trade Detected:")
        open_trade = get_open_trade(open_symbol)
        
        if open_trade:
            print(f"Symbol: {open_symbol}")
            print(f"Direction: {'SHORT' if open_trade['side'] == 'Sell' else 'LONG'}")
            print(f"Entry Price: {open_trade['entry_price']}")
            print(f"Size: {open_trade['size']}")
            print(f"Unrealized PnL: {open_trade['pnl_status']}")
            print(f"Created Time: {open_trade['created_time'].strftime('%Y-%m-%d %H:%M:%S')} Lagos Time")
            print("\nOpen LONG trade - doing nothing as per strategy")
            
            # Handle open SHORT trade
            if open_trade['side'] == 'Sell':
                if check_crossunder(open_symbol):
                    print("\n⚠️ CROSSUNDER DETECTED - Closing SHORT Position")
                    if close_short_position(open_symbol):
                        print("✅ SHORT Position Closed Successfully")
                    else:
                        print("❌ Failed to Close SHORT Position")
                else:
                    print("\n✅ No Crossunder - Keeping SHORT Position Open")
            
            #print("\n🛑 Strategy Blocked: Existing Open Position Detected")
            return
        
        else:
            print("\nℹ️ No Valid Open Positions Found")
    
    # 2. Check last closed trade
    last_trade = get_last_closed_trade()
    if not last_trade:
        print("\nℹ️ No Previous Trades Found - Standing By")
        return
    
    print(f"\n🔍 Last Closed Trade:")
    print(f"Symbol: {last_trade['symbol']}")
    print(f"Type: {last_trade['type']}")
    print(f"Direction: {'LONG' if last_trade['side'] == 'Buy' else 'SHORT'}")
    print(f"Entry Price: {last_trade['entry_price']}")
    print(f"Exit Price: {last_trade['exit_price']}")
    print(f"Closed Time: {last_trade['closed_time'].strftime('%Y-%m-%d %H:%M:%S')} Lagos Time")
    print(f"PnL: {last_trade['pnl_status']}")
    
    # Only act if last closed was LONG
    if last_trade['side'] == 'Buy':
        # Analyze trend since close
        flip_info, trend_message = analyze_trend_since_close(last_trade['symbol'], last_trade['closed_time'])
        print(f"\n📈 Trend Analysis:")
        print(trend_message)
        
        if "COUNTER-TREND" in trend_message:
            print("🛑 Not Entering New Trade Due to Counter-Trend Close")
        elif "FLIP" in trend_message:
            print("🛑 Not Entering New Trade Due to Trend Flip")
        else:
            # Check current market data
            df = fetch_market_data(last_trade['symbol'], timeframe, limit)
            if df is not None:
                current_trend = detect_trend(df, len(df)-1)
                print(f"\n📊 Current Market Trend: {current_trend}")
                
                if check_crossunder(last_trade['symbol']):
                    print("\n⚠️ CROSSUNDER DETECTED - Preparing to Enter LONG")
                    if current_trend in ("Uptrend", "Sideways"):
                        if cancel_all_pending_orders(last_trade['symbol']):
                            print("✅ Orders Canceled - Entering LONG")
                            place_long_market_order(last_trade['symbol'])
                        else:
                            print("❌ Failed to Cancel Pending Orders")
                    else:
                        print("🛑 Crossunder Ignored - Market in Downtrend")
                else:
                    print("\n✅ No Crossunder Detected - Standing By")
    
    print("\n✅ Strategy Execution Completed")

if __name__ == "__main__":
    main()













print("""
  _________________________________
 /                                 \\
|   C R O S S O V E R  SECRETS   |
 \\_________________________________/
        \\                   /
         \\                 /
          `\\_____________/'
""")



import ccxt
import pandas as pd
import numpy as np
from pybit.unified_trading import HTTP
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import pytz

# Initialize exchanges and trading session
exchange = ccxt.bybit()
session = HTTP(
    api_key="4eQbf5STelVE40HOtB",
    api_secret="bzo7oS1u8jxHIpkpFzy9mDLMvRrARJcXlKxt",
    demo=True
)

# Timezone setup
LAGOS_TZ = pytz.timezone('Africa/Lagos')
UTC_TZ = pytz.UTC

# Settings
timeframe = '15m'
limit = 500
h = 8.0
mult = 3.0
repaint = True
len_ema = 200
STOP_LOSS_PERCENT = 2.0  # 2% stop loss
TAKE_PROFIT_PERCENT = 10.0  # 10% take profit

# Email settings
SENDER_EMAIL = "dahmadu071@gmail.com"
RECIPIENT_EMAILS = ["teejeedeeone@gmail.com"]
EMAIL_PASSWORD = "oase wivf hvqn lyhr"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def format_pnl(pnl):
    """Format PnL with proper sign and profit/loss indication"""
    if pnl > 0:
        return f"+{pnl:.2f}% (Profit)"
    elif pnl < 0:
        return f"{pnl:.2f}% (Loss)"
    return f"{pnl:.2f}% (Break-even)"

def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAILS
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email notification sent")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_pybit_symbol(ccxt_symbol):
    """Convert CCXT symbol to Bybit symbol format"""
    return ccxt_symbol.split('/')[0] + ccxt_symbol.split('/')[1].split(':')[0]

def gauss(x, h):
    """Gaussian window function"""
    return np.exp(-(x ** 2) / (h ** 2 * 2))

def calculate_nwe(src, h, mult, repaint):
    """Calculate Nadaraya-Watson Envelope"""
    n = len(src)
    out = np.zeros(n)
    mae = np.zeros(n)
    upper = np.zeros(n)
    lower = np.zeros(n)
    
    if not repaint:
        coefs = np.array([gauss(i, h) for i in range(n)])
        den = np.sum(coefs)
        
        for i in range(n):
            out[i] = np.sum(src * coefs) / den
        
        mae = pd.Series(np.abs(src - out)).rolling(499).mean().values * mult
        upper = out + mae
        lower = out - mae
    else:
        nwe = []
        sae = 0.0
        
        for i in range(n):
            sum_val = 0.0
            sumw = 0.0
            for j in range(n):
                w = gauss(i - j, h)
                sum_val += src[j] * w
                sumw += w
            y2 = sum_val / sumw
            nwe.append(y2)
            sae += np.abs(src[i] - y2)
        
        sae = (sae / n) * mult
        
        for i in range(n):
            upper[i] = nwe[i] + sae
            lower[i] = nwe[i] - sae
            out[i] = nwe[i]
    
    return out, upper, lower

def detect_crossover(close, upper):
    """Detect if price has crossed above the upper envelope"""
    return (close.shift(1) < upper.shift(1)) & (close > upper)

def fetch_market_data(symbol, timeframe, limit=500):
    """Fetch OHLCV data with proper timezone handling"""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(LAGOS_TZ)
        df.set_index('timestamp', inplace=True)
        df['EMA'] = df['close'].ewm(span=len_ema, adjust=False).mean()
        return df
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None

def detect_trend(df, candle_index):
    """Determine trend for a specific candle"""
    if candle_index < 1 or candle_index >= len(df):
        return "Sideways"
    
    ema_current = df['EMA'].iloc[candle_index]
    ema_prev = df['EMA'].iloc[candle_index-1]
    price = df['close'].iloc[candle_index]
    
    if ema_current > ema_prev and price > ema_current:
        return "Uptrend"
    elif ema_current < ema_prev and price < ema_current:
        return "Downtrend"
    return "Sideways"

def get_most_recent_open_trade_symbol():
    """Get symbol of most recent open trade"""
    try:
        executions = session.get_executions(
            category="linear",
            limit=50,
            settleCoin="USDT"
        )
        
        if executions["retCode"] != 0:
            print(f"Error fetching executions: {executions['retMsg']}")
            return None
            
        if not executions["result"]["list"]:
            return None
            
        for trade in sorted(executions["result"]["list"], 
                          key=lambda x: int(x["execTime"]), 
                          reverse=True):
            if trade["execType"] == "Trade" and float(trade["execQty"]) > 0:
                positions = session.get_positions(
                    category="linear",
                    symbol=trade["symbol"]
                )
                
                if positions["retCode"] == 0 and positions["result"]["list"]:
                    for position in positions["result"]["list"]:
                        if position["symbol"] == trade["symbol"] and float(position["size"]) > 0:
                            return f"{trade['symbol'].replace('USDT', '')}/USDT:USDT"
        
        return None
    except Exception as e:
        print(f"Error checking trades: {e}")
        return None

def get_open_trade(symbol):
    """Get details of open trade for specified symbol"""
    try:
        pybit_symbol = get_pybit_symbol(symbol)
        positions = session.get_positions(
            category="linear",
            symbol=pybit_symbol
        )
        if positions["retCode"] == 0 and positions["result"]["list"]:
            for position in positions["result"]["list"]:
                if position["symbol"] == pybit_symbol and float(position["size"]) > 0:
                    unrealized_pnl = float(position['unrealisedPnl'])
                    return {
                        'side': position['side'],
                        'size': float(position['size']),
                        'entry_price': float(position['avgPrice']),
                        'unrealized_pnl': unrealized_pnl,
                        'pnl_status': format_pnl(unrealized_pnl),
                        'created_time': datetime.fromtimestamp(int(position['createdTime'])/1000, UTC_TZ).astimezone(LAGOS_TZ)
                    }
        return None
    except Exception as e:
        print(f"Error checking open positions: {e}")
        return None

def get_last_closed_trade():
    """Get details of last closed trade"""
    try:
        trades = session.get_executions(
            category="linear",
            limit=50,
            settleCoin="USDT"
        )
        
        if trades["retCode"] != 0:
            print(f"Error fetching trades: {trades['retMsg']}")
            return None
            
        trades = trades["result"]["list"]
        if not trades:
            return None

        for trade in sorted(trades, key=lambda x: int(x["execTime"]), reverse=True):
            symbol = trade["symbol"]
            positions = session.get_positions(
                category="linear",
                symbol=symbol
            )
            
            if positions["retCode"] != 0:
                continue
                
            position_open = any(float(p["size"]) > 0 for p in positions["result"]["list"])
            
            if not position_open and trade["closedSize"]:
                utc_time = datetime.fromtimestamp(int(trade["execTime"])/1000, UTC_TZ)
                lagos_time = utc_time.astimezone(LAGOS_TZ)
                
                if trade['side'] == 'Sell':  # Closing long
                    trade_type = 'Long Close'
                    actual_side = 'Buy'
                    entry_price = float(trade["avgEntryPrice"]) if "avgEntryPrice" in trade else float(trade["execPrice"])
                    exit_price = float(trade["execPrice"])
                    pnl_percent = ((exit_price - entry_price) / entry_price) * 100
                else:  # Closing short
                    trade_type = 'Short Close'
                    actual_side = 'Sell'
                    entry_price = float(trade["avgEntryPrice"]) if "avgEntryPrice" in trade else float(trade["execPrice"])
                    exit_price = float(trade["execPrice"])
                    pnl_percent = ((entry_price - exit_price) / entry_price) * 100
                
                return {
                    'symbol': f"{symbol.replace('USDT', '')}/USDT:USDT",
                    'type': trade_type,
                    'side': actual_side,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'pnl': pnl_percent,
                    'pnl_status': format_pnl(pnl_percent),
                    'closed_time': lagos_time,
                    'utc_close_time': utc_time
                }
        return None
    except Exception as e:
        print(f"Error fetching trade history: {e}")
        return None

def analyze_trend_since_close(symbol, since_timestamp):
    """Analyze trend changes since trade close"""
    try:
        df = fetch_market_data(symbol, timeframe, limit)
        if df is None or len(df) < 2:
            return None, "Error: Not enough market data"
        
        close_candle_idx = df.index.get_indexer([since_timestamp], method='nearest')[0]
        if close_candle_idx < 1:
            close_candle_idx = 1
        
        trend_at_close = detect_trend(df, close_candle_idx)
        
        last_trade = get_last_closed_trade()
        if last_trade:
            if (last_trade['side'] == "Sell" and trend_at_close == "Uptrend") or \
               (last_trade['side'] == "Buy" and trend_at_close == "Downtrend"):
                return None, "⚠️ COUNTER-TREND CLOSING DETECTED"
        
        current_trend = trend_at_close
        first_flip = None
        
        for i in range(close_candle_idx + 1, len(df)):
            new_trend = detect_trend(df, i)
            
            if new_trend != current_trend and new_trend in ["Uptrend", "Downtrend"]:
                first_flip = {
                    'time': df.index[i],
                    'new_trend': new_trend,
                    'price': df['close'].iloc[i],
                    'candle_time': df.index[i].strftime('%Y-%m-%d %H:%M:%S')
                }
                break
        
        if first_flip:
            duration = first_flip['time'] - since_timestamp
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            return first_flip, f"FIRST TREND FLIP: {first_flip['new_trend']} at {first_flip['candle_time']} ({hours}h {minutes}m after close)"
        
        return None, "✅ No trend flips detected since closing"
    
    except Exception as e:
        print(f"Error analyzing trend: {e}")
        return None, f"Error analyzing trend: {e}"

def check_crossover(symbol):
    """Check for crossover condition on specified symbol"""
    try:
        df = fetch_market_data(symbol, timeframe, limit)
        if df is None:
            return False
            
        src = df['close'].values
        out, upper, lower = calculate_nwe(src, h, mult, repaint)
        
        close_series = pd.Series(src)
        upper_series = pd.Series(upper)
        crossover = detect_crossover(close_series, upper_series)
        
        return crossover.iloc[-1]  # Check most recent candle
    except Exception as e:
        print(f"Error checking crossover: {e}")
        return False

def cancel_all_pending_orders(symbol):
    """Cancel all pending orders for specified symbol"""
    try:
        pybit_symbol = get_pybit_symbol(symbol)
        response = session.cancel_all_orders(
            category="linear",
            symbol=pybit_symbol
        )
        if response["retCode"] == 0:
            print("All pending orders canceled")
            return True
        else:
            print(f"Failed to cancel orders: {response['retMsg']}")
            return False
    except Exception as e:
        print(f"Error canceling orders: {e}")
        return False

def close_long_position(symbol):
    """Close long position for specified symbol"""
    try:
        pybit_symbol = get_pybit_symbol(symbol)
        position = get_open_trade(symbol)
        
        if position and position['side'] == 'Buy':
            ticker = session.get_tickers(category="linear", symbol=pybit_symbol)
            market_price = float(ticker["result"]["list"][0]["lastPrice"])
            
            response = session.place_order(
                category="linear",
                symbol=pybit_symbol,
                side="Sell",
                orderType="Market",
                qty=str(position['size'])
            )
            
            if response["retCode"] == 0:
                msg = f"Long position closed at {market_price}. PnL: {position['pnl_status']}"
                print(msg)
                send_email("Long Position Closed", msg)
                return True
            else:
                print(f"Failed to close long position: {response['retMsg']}")
                return False
        return False
    except Exception as e:
        print(f"Error closing long position: {e}")
        return False

def place_short_market_order(symbol, usdt_amount=50):
    """Place short market order for specified symbol"""
    try:
        pybit_symbol = get_pybit_symbol(symbol)
        
        ticker = session.get_tickers(category="linear", symbol=pybit_symbol)
        market_price = float(ticker["result"]["list"][0]["lastPrice"])
        
        instrument_info = session.get_instruments_info(category="linear", symbol=pybit_symbol)
        lot_size = instrument_info["result"]["list"][0]["lotSizeFilter"]
        qty_step = float(lot_size["qtyStep"])
        
        quantity = round((usdt_amount / market_price) / qty_step) * qty_step
        
        # Calculate stop loss and take profit prices
        stop_loss_price = market_price * (1 + STOP_LOSS_PERCENT/100)
        take_profit_price = market_price * (1 - TAKE_PROFIT_PERCENT/100)
        
        response = session.place_order(
            category="linear",
            symbol=pybit_symbol,
            side="Sell",
            orderType="Market",
            qty=str(quantity),
            stopLoss=str(stop_loss_price),
            takeProfit=str(take_profit_price)
        )
        
        if response["retCode"] == 0:
            msg = f"""Short market order placed for {quantity} {symbol.split('/')[0]} at {market_price}
Stop Loss: {stop_loss_price:.4f} ({STOP_LOSS_PERCENT}%)
Take Profit: {take_profit_price:.4f} ({TAKE_PROFIT_PERCENT}%)"""
            print(msg)
            send_email("Short Position Opened", msg)
            return True
        else:
            print(f"Failed to place order: {response['retMsg']}")
            return False
    except Exception as e:
        print(f"Error placing short order: {e}")
        return False

def main():
    print(f"\n🚀 Starting Crossover Strategy at {datetime.now(LAGOS_TZ).strftime('%Y-%m-%d %H:%M:%S')} Lagos Time\n")
    
    # 1. Check for any open trades
    open_symbol = get_most_recent_open_trade_symbol()
    if open_symbol:
        print(f"🔍 Open Trade Detected on {open_symbol}:")
        open_trade = get_open_trade(open_symbol)
        
        if open_trade:
            print(f"Direction: {'SHORT' if open_trade['side'] == 'Sell' else 'LONG'}")
            print(f"Entry Price: {open_trade['entry_price']}")
            print(f"Size: {open_trade['size']}")
            print(f"Unrealized PnL: {open_trade['pnl_status']}")
            print(f"Created Time: {open_trade['created_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Handle open LONG trade (close on crossover)
            if open_trade['side'] == 'Buy':
                if check_crossover(open_symbol):
                    print("\n⚠️ CROSSOVER DETECTED - Closing LONG Position")
                    if close_long_position(open_symbol):
                        print("✅ LONG Position Closed Successfully")
                    else:
                        print("❌ Failed to Close LONG Position")
                else:
                    print("\n✅ No Crossover - Keeping LONG Position Open")
            
            return
        
    # 2. Check last closed trade
    last_trade = get_last_closed_trade()
    if not last_trade:
        print("\nℹ️ No Previous Trades Found - Standing By")
        return
    
    print(f"\n🔍 Last Closed Trade:")
    print(f"Symbol: {last_trade['symbol']}")
    print(f"Type: {last_trade['type']}")
    print(f"Direction: {'LONG' if last_trade['side'] == 'Buy' else 'SHORT'}")
    print(f"Entry Price: {last_trade['entry_price']}")
    print(f"Exit Price: {last_trade['exit_price']}")
    print(f"Closed Time: {last_trade['closed_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"PnL: {last_trade['pnl_status']}")
    
    # Only act if last closed was SHORT trade
    if last_trade['side'] == 'Sell':
        # Analyze trend since close
        flip_info, trend_message = analyze_trend_since_close(last_trade['symbol'], last_trade['closed_time'])
        print(f"\n📈 Trend Analysis:")
        print(trend_message)
        
        if "COUNTER-TREND" in trend_message:
            print("🛑 Not Entering New Trade Due to Counter-Trend Close")
        elif "FLIP" in trend_message:
            print("🛑 Not Entering New Trade Due to Trend Flip")
        else:
            # Check current market data
            df = fetch_market_data(last_trade['symbol'], timeframe, limit)
            if df is not None:
                current_trend = detect_trend(df, len(df)-1)
                print(f"\n📊 Current Market Trend: {current_trend}")
                
                if check_crossover(last_trade['symbol']):
                    print("\n⚠️ CROSSOVER DETECTED - Preparing to Enter SHORT")
                    if current_trend in ("Downtrend", "Sideways"):
                        if cancel_all_pending_orders(last_trade['symbol']):
                            print("✅ Orders Canceled - Entering SHORT")
                            place_short_market_order(last_trade['symbol'])
                        else:
                            print("❌ Failed to Cancel Pending Orders")
                    else:
                        print("🛑 Crossover Ignored - Market in Uptrend")
                else:
                    print("\n✅ No Crossover Detected - Standing By")
    
    print("\n✅ Strategy Execution Completed")

if __name__ == "__main__":
    main()







print("""  
  \033[95m✧⋄⋄✧⋄⋄✧⋄⋄✧⋄⋄✧⋄⋄✧⋄⋄✧⋄⋄✧  
     𝔹𝔸ℕ𝔻 𝕋𝕆𝕌ℂℍ 𝕊𝔼ℚ𝕌𝔼ℕℂ𝔼  
  ✧⋄⋄✧⋄⋄✧⋄⋄✧⋄⋄✧⋄⋄✧⋄⋄✧⋄⋄✧\033[0m  
""")  


import ccxt
import pandas as pd
import numpy as np
from pybit.unified_trading import HTTP
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import pytz

# ======== SETTINGS ========
timeframe = '15m'
limit = 500
h = 8.0          # Bandwidth for Nadaraya-Watson
mult = 3.0       # Multiplier for envelope width
repaint = True   # Repainting mode

# Profit thresholds
TAKE_PROFIT_PCT = 5.0    # Your original TP (unchanged)
PROFIT_LOCK_PCT = 0.1    # Lock 0.1% profit in SL
MIN_PROFIT_PCT = 0.1     # Minimum profit threshold

# Email settings
SENDER_EMAIL = "dahmadu071@gmail.com"
RECIPIENT_EMAILS = ["teejeedeeone@gmail.com"]
EMAIL_PASSWORD = "oase wivf hvqn lyhr"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Timezone settings
LAGOS_TZ = pytz.timezone('Africa/Lagos')
UTC_TZ = pytz.UTC
# ==========================

# Initialize exchanges and session
exchange = ccxt.bybit()
session = HTTP(
    api_key="4eQbf5STelVE40HOtB",
    api_secret="bzo7oS1u8jxHIpkpFzy9mDLMvRrARJcXlKxt",
    demo=True
)

def send_email(subject, body):
    """Send email alerts"""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAILS
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent")
    except Exception as e:
        print(f"Email failed: {e}")

def format_pnl(pnl):
    """Format PnL with proper sign"""
    if pnl > 0:
        return f"+{pnl:.2f}% (Profit)"
    elif pnl < 0:
        return f"{pnl:.2f}% (Loss)"
    return f"{pnl:.2f}% (Break-even)"

def get_most_recent_trade():
    """Get the most recently opened trade"""
    try:
        executions = session.get_executions(
            category="linear",
            limit=50,
            settleCoin="USDT"
        )
        
        if executions["retCode"] != 0:
            print(f"Error fetching executions: {executions['retMsg']}")
            return None
            
        if not executions["result"]["list"]:
            print("No trade history found")
            return None
            
        for trade in sorted(executions["result"]["list"], 
                          key=lambda x: int(x["execTime"]), 
                          reverse=True):
            if trade["execType"] == "Trade" and float(trade["execQty"]) > 0:
                positions = session.get_positions(
                    category="linear",
                    symbol=trade["symbol"]
                )
                
                if positions["retCode"] == 0 and positions["result"]["list"]:
                    for position in positions["result"]["list"]:
                        if position["symbol"] == trade["symbol"] and float(position["size"]) > 0:
                            entry_price = float(position['avgPrice'])
                            mark_price = float(position['markPrice'])
                            pnl_percent = ((mark_price - entry_price) / entry_price) * 100
                            
                            return {
                                'symbol': trade["symbol"],
                                'ccxt_symbol': trade["symbol"].replace("USDT", "") + "/USDT:USDT",
                                'side': trade["side"],
                                'size': float(trade["execQty"]),
                                'entry_price': entry_price,
                                'mark_price': mark_price,
                                'pnl': pnl_percent,
                                'pnl_status': format_pnl(pnl_percent),
                                'executed_time': datetime.fromtimestamp(int(trade["execTime"])/1000, UTC_TZ).astimezone(LAGOS_TZ)
                            }
        
        print("No currently open trades found")
        return None
        
    except Exception as e:
        print(f"Error checking trades: {e}")
        return None

def calculate_nwe(src, h, mult, repaint):
    """Calculate Nadaraya-Watson Envelope"""
    n = len(src)
    if repaint:
        i = np.arange(n)
        j = np.arange(n).reshape(-1, 1)
        weights = np.exp(-((i-j)**2)/(2*h**2))
        sumw = np.sum(weights, axis=1)
        nwe = np.sum(src * weights, axis=1) / sumw
        sae = np.mean(np.abs(src - nwe)) * mult
        upper = nwe + sae
        lower = nwe - sae
    else:
        weights = np.exp(-(np.arange(n)**2)/(2*h**2))
        sumw = np.sum(weights)
        nwe = np.sum(src * weights) / sumw
        mae = pd.Series(np.abs(src - nwe)).rolling(499).mean().values * mult
        upper = nwe + mae
        lower = nwe - mae
    
    return upper, lower

def check_band_touch(symbol):
    """Detect if price touched bands"""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        src = df['close'].values
        upper, lower = calculate_nwe(src, h, mult, repaint)
        
        last_candle = df.iloc[-2]  # Last closed candle
        last_upper = upper[-2]
        last_lower = lower[-2]
        
        touched_upper = (last_candle['high'] >= last_upper) or (last_candle['close'] >= last_upper)
        touched_lower = (last_candle['low'] <= last_lower) or (last_candle['close'] <= last_lower)
        
        return touched_upper, touched_lower, last_upper, last_lower
        
    except Exception as e:
        print(f"Band check error for {symbol}: {e}")
        return False, False, None, None

def close_trade(trade_info):
    """Close position with market order"""
    try:
        resp = session.place_order(
            category="linear",
            symbol=trade_info['symbol'],
            side="Buy" if trade_info['side'] == 'Sell' else "Sell",
            orderType="Market",
            qty=str(trade_info['size'])
        )
        
        if resp["retCode"] == 0:
            msg = (f"Closed {trade_info['side']} position on {trade_info['symbol']}\n"
                  f"Entry: {trade_info['entry_price']:.6f} | Exit: {trade_info['mark_price']:.6f}\n"
                  f"PnL: {trade_info['pnl_status']}")
            print(msg)
            send_email(f"{trade_info['side']} Position Closed", msg)
            return True
        else:
            print(f"Close failed: {resp['retMsg']}")
            return False
    except Exception as e:
        print(f"Close error: {e}")
        return False

def trail_stop(trade_info):
    """Move SL to lock 0.1% profit (without changing TP)"""
    try:
        if trade_info['side'] == 'Buy':
            # For LONG: SL = entry + 0.1% (lock profit)
            new_sl = trade_info['entry_price'] * 1.001
        else:
            # For SHORT: SL = entry - 0.1% (lock profit)
            new_sl = trade_info['entry_price'] * 0.999
        
        resp = session.set_trading_stop(
            category="linear",
            symbol=trade_info['symbol'],
            stopLoss=str(new_sl)  # Only modify SL
        )
        
        if resp["retCode"] == 0:
            print(f"SL moved to {new_sl:.6f} (locking 0.1% profit)")
            return True
        else:
            print(f"SL trail failed: {resp['retMsg']}")
            return False
    except Exception as e:
        print(f"Trail error: {e}")
        return False

def main():
    print(f"\nChecking for trades at {datetime.now(LAGOS_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Get the most recent trade
    trade = get_most_recent_trade()
    if not trade:
        print("No open trades found")
        return
    
    print(f"\nActive Trade:")
    print(f"Symbol: {trade['symbol']}")
    print(f"Direction: {trade['side']}")
    print(f"Size: {trade['size']}")
    print(f"Entry Price: {trade['entry_price']:.6f}")
    print(f"Current Mark Price: {trade['mark_price']:.6f}")
    print(f"Unrealized PnL: {trade['pnl_status']}")
    print(f"Executed Time: {trade['executed_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 2. Check band touches
    touched_upper, touched_lower, last_upper, last_lower = check_band_touch(trade['ccxt_symbol'])
    print(f"\nBand Analysis:")
    print(f"Upper band: {last_upper:.6f} | Lower band: {last_lower:.6f}")
    print(f"Touched upper: {touched_upper} | Touched lower: {touched_lower}")
    
    # 3. Apply trading rules
    if trade['side'] == 'Buy' and touched_upper:
        if trade['pnl'] > TAKE_PROFIT_PCT:
            print(f"\nProfit >{TAKE_PROFIT_PCT}% + Upper touch → Closing")
            close_trade(trade)
        elif trade['pnl'] > MIN_PROFIT_PCT:
            print(f"\nProfit {MIN_PROFIT_PCT}-{TAKE_PROFIT_PCT}% + Upper touch → Locking 0.1% profit")
            trail_stop(trade)
        else:
            print(f"\nProfit ≤{MIN_PROFIT_PCT}% + Upper touch → Closing")
            close_trade(trade)
    
    elif trade['side'] == 'Sell' and touched_lower:
        if trade['pnl'] > TAKE_PROFIT_PCT:
            print(f"\nProfit >{TAKE_PROFIT_PCT}% + Lower touch → Closing")
            close_trade(trade)
        elif trade['pnl'] > MIN_PROFIT_PCT:
            print(f"\nProfit {MIN_PROFIT_PCT}-{TAKE_PROFIT_PCT}% + Lower touch → Locking 0.1% profit")
            trail_stop(trade)
        else:
            print(f"\nProfit ≤{MIN_PROFIT_PCT}% + Lower touch → Closing")
            close_trade(trade)
    
    else:
        print("\nNo band touch → Holding position")

if __name__ == "__main__":
    main()
















print("""  
  \033[90m▁▂▃▄▅▆▇▓▒░ 2xATR ░▒▓▇▆▅▄▃▂▁\033[0m  
""")  

import ccxt
import pandas as pd
import numpy as np
from pybit.unified_trading import HTTP
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import pytz

# ======== SETTINGS ========
timeframe = '15m'
limit = 500
atr_period = 14
atr_multiplier = 2.0
len_ema = 200
order_amount_usdt = 50
stop_loss_percent = 2  # 2% stop loss
take_profit_percent = 10  # 10% take profit

# Email settings
SENDER_EMAIL = "dahmadu071@gmail.com"
RECIPIENT_EMAILS = ["teejeedeeone@gmail.com"]
EMAIL_PASSWORD = "oase wivf hvqn lyhr"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Timezone settings
LAGOS_TZ = pytz.timezone('Africa/Lagos')
UTC_TZ = pytz.UTC
# ==========================

# Initialize exchanges
exchange = ccxt.bybit()
session = HTTP(
    api_key="4eQbf5STelVE40HOtB",
    api_secret="bzo7oS1u8jxHIpkpFzy9mDLMvRrARJcXlKxt",
    demo=True
)

def send_email(subject, body):
    """Send email alerts"""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAILS
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def calculate_atr(df, period=14):
    """Calculate ATR"""
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def fetch_market_data(symbol, timeframe, limit=500):
    """Fetch OHLCV data with proper timezone handling"""
    try:
        ccxt_symbol = f"{symbol.replace('USDT', '')}/USDT:USDT" if 'USDT' in symbol else f"{symbol}/USDT:USDT"
        ohlcv = exchange.fetch_ohlcv(ccxt_symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(LAGOS_TZ)
        df.set_index('timestamp', inplace=True)
        df['EMA'] = df['close'].ewm(span=len_ema, adjust=False).mean()
        return df
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None

def detect_trend(df, candle_index):
    """Determine trend for a specific candle"""
    if candle_index < 1 or candle_index >= len(df):
        return "sideways"
    
    ema_current = df['EMA'].iloc[candle_index]
    ema_prev = df['EMA'].iloc[candle_index-1]
    price = df['close'].iloc[candle_index]
    
    if ema_current > ema_prev and price > ema_current:
        return "uptrend"
    elif ema_current < ema_prev and price < ema_current:
        return "downtrend"
    return "sideways"

def get_last_closed_trade():
    """Get details of the most recent closed trade"""
    try:
        trades = session.get_executions(category="linear", limit=50)
        if trades["retCode"] != 0:
            print(f"Error fetching trades: {trades['retMsg']}")
            return None
            
        trades = trades["result"]["list"]
        if not trades:
            return None

        for trade in sorted(trades, key=lambda x: int(x["execTime"]), reverse=True):
            symbol = trade["symbol"]
            
            positions = session.get_positions(category="linear", symbol=symbol)
            if positions["retCode"] != 0:
                continue
                
            position_open = any(float(p["size"]) > 0 for p in positions["result"]["list"])
            
            if not position_open and trade["closedSize"]:
                utc_time = datetime.fromtimestamp(int(trade["execTime"])/1000, UTC_TZ)
                lagos_time = utc_time.astimezone(LAGOS_TZ)
                
                return {
                    "symbol": symbol,
                    "close_time": lagos_time,
                    "close_price": float(trade["execPrice"]),
                    "side": "Buy" if trade["side"] == "Sell" else "Sell",
                    "utc_close_time": utc_time,
                    "ccxt_symbol": f"{symbol.replace('USDT', '')}/USDT:USDT",
                    "direction": "LONG" if trade["side"] == "Sell" else "SHORT"
                }
        return None
    except Exception as e:
        print(f"Error fetching trade history: {e}")
        return None

def get_trend_flip_since_last_trade(trade_info):
    """Check if trend flipped since last trade"""
    if not trade_info:
        return True
    
    df = fetch_market_data(trade_info["symbol"], timeframe, 500)
    if df is None or len(df) < 2:
        print("Error: Not enough market data for trend analysis")
        return True
    
    close_candle_idx = df.index.get_indexer([trade_info['close_time']], method='nearest')[0]
    if close_candle_idx < 1:
        close_candle_idx = 1
    
    trend_at_close = detect_trend(df, close_candle_idx)
    
    first_flip = None
    for i in range(close_candle_idx + 1, len(df)):
        new_trend = detect_trend(df, i)
        
        if new_trend != trend_at_close and new_trend in ["uptrend", "downtrend"]:
            first_flip = {
                'time': df.index[i],
                'new_trend': new_trend,
                'price': df['close'].iloc[i],
                'candle_time': df.index[i].strftime('%Y-%m-%d %H:%M:%S')
            }
            break
    
    return first_flip

def has_open_orders(symbol):
    """Check for existing conditional orders"""
    try:
        orders = session.get_open_orders(
            category="linear", 
            symbol=symbol,
            orderFilter="StopOrder"
        )
        return orders["retCode"] == 0 and len(orders["result"]["list"]) > 0
    except Exception as e:
        print(f"Order check error: {e}")
        return True

def has_open_position(symbol):
    """Check for open positions"""
    try:
        positions = session.get_positions(category="linear", symbol=symbol)
        if positions["retCode"] == 0:
            for pos in positions["result"]["list"]:
                if float(pos["size"]) > 0:
                    return True
        return False
    except Exception as e:
        print(f"Position check error: {e}")
        return True

def place_conditional_order(symbol, side, trigger_price, last_trade_price):
    """Place conditional stop order with SL/TP"""
    try:
        # Calculate SL and TP prices
        if side == "Buy":
            sl_price = round(trigger_price * (1 - stop_loss_percent/100), 8)
            tp_price = round(trigger_price * (1 + take_profit_percent/100), 8)
        else:
            sl_price = round(trigger_price * (1 + stop_loss_percent/100), 8)
            tp_price = round(trigger_price * (1 - take_profit_percent/100), 8)
        
        # Get quantity
        instrument = session.get_instruments_info(category="linear", symbol=symbol)
        qty_step = float(instrument["result"]["list"][0]["lotSizeFilter"]["qtyStep"])
        quantity = round((order_amount_usdt / trigger_price) / qty_step) * qty_step
        
        # Place order
        response = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(quantity),
            triggerDirection=1 if side == "Buy" else 2,
            triggerPrice=str(trigger_price),
            triggerBy="MarkPrice",
            orderFilter="StopOrder",
            timeInForce="GTC",
            stopLoss=str(sl_price),
            takeProfit=str(tp_price)
        )
        
        if response["retCode"] == 0:
            order_info = {
                "symbol": symbol,
                "side": side,
                "direction": "LONG" if side == "Buy" else "SHORT",
                "trigger_price": trigger_price,
                "quantity": quantity,
                "stop_loss": sl_price,
                "take_profit": tp_price,
                "risk_reward": take_profit_percent / stop_loss_percent,
                "order_time": datetime.now(LAGOS_TZ)
            }
            
            msg = (f"Placed {side} conditional order at {trigger_price:.8f}\n"
                  f"Quantity: {quantity:.6f} {symbol.replace('USDT', '')}\n"
                  f"Stop Loss: {sl_price:.8f} ({stop_loss_percent}%)\n"
                  f"Take Profit: {tp_price:.8f} ({take_profit_percent}%)\n"
                  f"Risk/Reward: 1:{take_profit_percent/stop_loss_percent:.1f}")
            
            print(msg)
            send_email(f"{side} Conditional Order Placed", msg)
            return order_info
        else:
            print(f"Order failed: {response['retMsg']}")
            return None
    except Exception as e:
        print(f"Order placement error: {e}")
        return None

def main():
    print(f"\n🚀 Starting Trading Bot at {datetime.now(LAGOS_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
    
    last_trade = get_last_closed_trade()
    if not last_trade:
        print("No recent trade history - doing nothing")
        return
    
    symbol = last_trade["symbol"]
    print(f"\n🔍 Last Closed Trade:")
    print(f"Symbol: {symbol}")
    print(f"Direction: {last_trade['direction']}")
    print(f"Closed at: {last_trade['close_time'].strftime('%Y-%m-%d %H:%M:%S')} Lagos Time")
    print(f"Close Price: {last_trade['close_price']:.8f}")
    
    if has_open_position(symbol) or has_open_orders(symbol):
        print("\n⚠️ Open position/order exists - doing nothing")
        return
    
    df = fetch_market_data(symbol, timeframe)
    if df is None:
        print("Failed to fetch market data")
        return
    
    current_trend = detect_trend(df, len(df)-1)
    trend_flip_info = get_trend_flip_since_last_trade(last_trade)
    
    print(f"\n📈 Market Trend at Close: {current_trend}")
    if trend_flip_info:
        duration = trend_flip_info['time'] - last_trade['close_time']
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        print(f"\n⚠️ FIRST TREND FLIP DETECTED:")
        print(f"Time: {trend_flip_info['candle_time']} Lagos Time")
        print(f"New Trend: {trend_flip_info['new_trend']}")
        print(f"Price: {trend_flip_info['price']:.8f}")
        print(f"Time Since Close: {hours}h {minutes}m")
    else:
        print("\n✅ No trend flips detected since closing")
    
    print(f"\nCurrent Market Trend: {current_trend}")
    
    if not current_trend or trend_flip_info:
        reject_reasons = []
        if not current_trend: reject_reasons.append("failed to check trend")
        if trend_flip_info: reject_reasons.append("trend flipped since last trade")
        print(f"\n❌ Rejected: {', '.join(reject_reasons)}")
        return
    
    try:
        atr = calculate_atr(df, atr_period).iloc[-1]
        current_price = float(session.get_tickers(category="linear", symbol=symbol)["result"]["list"][0]["lastPrice"])
        
        if last_trade['side'] == 'Buy':
            trigger_price = last_trade['close_price'] + (atr * atr_multiplier)
            order_side = "Buy"
        else:
            trigger_price = last_trade['close_price'] - (atr * atr_multiplier)
            order_side = "Sell"
        
        trigger_price = round(trigger_price, 8)
        
        print(f"\n📊 ATR Analysis:")
        print(f"ATR Value: {atr:.8f}")
        print(f"Projection Price: {trigger_price:.8f}")
        print(f"Current Price: {current_price:.8f}")
        
        if (last_trade['side'] == 'Buy' and current_trend == "uptrend") or \
           (last_trade['side'] == 'Sell' and current_trend == "downtrend"):
            print(f"\n✅ Conditions met - placing {order_side} conditional order")
            order_info = place_conditional_order(symbol, order_side, trigger_price, last_trade['close_price'])
            
            if order_info:
                print(f"\n📝 Order Details:")
                print(f"Direction: {order_info['direction']}")
                print(f"Trigger Price: {order_info['trigger_price']:.8f}")
                print(f"Quantity: {order_info['quantity']:.8f}")
                print(f"Stop Loss: {order_info['stop_loss']:.8f} ({stop_loss_percent}%)")
                print(f"Take Profit: {order_info['take_profit']:.8f} ({take_profit_percent}%)")
                print(f"Risk/Reward: 1:{order_info['risk_reward']:.1f}")
                print(f"Order Time: {order_info['order_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"\n❌ Rejected: Trend condition not met (Current trend: {current_trend})")
                
    except Exception as e:
        print(f"\nATR calculation error: {e}")

if __name__ == "__main__":
    main()
    print("\n✅ Trading bot execution complete!")