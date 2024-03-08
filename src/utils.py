from enum import Enum
from typing import Literal


class Symbol(Enum):

    ALL = "all"
    BTCIRT = 'BTCIRT'
    ETHIRT = 'ETHIRT'
    LTCIRT = 'LTCIRT'
    USDTIRT = 'USDTIRT'
    XRPIRT = 'XRPIRT'
    BCHIRT = 'BCHIRT'
    BNBIRT = 'BNBIRT'
    EOSIRT = 'EOSIRT'
    XLMIRT = 'XLMIRT'
    ETCIRT = 'ETCIRT'
    TRXIRT = 'TRXIRT'
    DOGEIRT = 'DOGEIRT'
    UNIIRT = 'UNIIRT'
    DAIIRT = 'DAIIRT'
    LINKIRT = 'LINKIRT'
    DOTIRT = 'DOTIRT'
    AAVEIRT = 'AAVEIRT'
    ADAIRT = 'ADAIRT'
    SHIBIRT = 'SHIBIRT'
    FTMIRT = 'FTMIRT'
    MATICIRT = 'MATICIRT'
    AXSIRT = 'AXSIRT'
    MANAIRT = 'MANAIRT'
    SANDIRT = 'SANDIRT'
    AVAXIRT = 'AVAXIRT'
    MKRIRT = 'MKRIRT'
    GMTIRT = 'GMTIRT'
    USDCIRT = 'USDCIRT'
    BTCUSDT = 'BTCUSDT'
    ETHUSDT = 'ETHUSDT'
    LTCUSDT = 'LTCUSDT'
    XRPUSDT = 'XRPUSDT'
    BCHUSDT = 'BCHUSDT'
    BNBUSDT = 'BNBUSDT'
    EOSUSDT = 'EOSUSDT'
    XLMUSDT = 'XLMUSDT'
    ETCUSDT = 'ETCUSDT'
    TRXUSDT = 'TRXUSDT'
    PMNUSDT = 'PMNUSDT'
    DOGEUSDT = 'DOGEUSDT'
    UNIUSDT = 'UNIUSDT'
    DAIUSDT = 'DAIUSDT'
    LINKUSDT = 'LINKUSDT'
    DOTUSDT = 'DOTUSDT'
    AAVEUSDT = 'AAVEUSDT'
    ADAUSDT = 'ADAUSDT'
    SHIBUSDT = 'SHIBUSDT'
    FTMUSDT = 'FTMUSDT'
    MATICUSDT = 'MATICUSDT'
    AXSUSDT = 'AXSUSDT'
    MANAUSDT = 'MANAUSDT'
    SANDUSDT = 'SANDUSDT'
    AVAXUSDT = 'AVAXUSDT'
    MKRUSDT = 'MKRUSDT'
    GMTUSDT = 'GMTUSDT'
    USDCUSDT = 'USDCUSDT'
    
class Currency(Enum):

    rls = 'rls'
    btc = 'btc'
    eth = 'eth'
    ltc = 'ltc'
    usdt = 'usdt'
    xrp = 'xrp'
    bch = 'bch'
    bnb = 'bnb'
    eos = 'eos'
    xlm = 'xlm'
    etc = 'etc'
    trx = 'trx'
    pmn = 'pmn'
    doge = 'doge'
    uni = 'uni'
    dai = 'dai'
    link = 'link'
    dot = 'dot'
    aave = 'aave'
    ada = 'ada'
    shib = 'shib'
    ftm = 'ftm'
    matic = 'matic'
    axs = 'axs'
    mana = 'mana'
    sand = 'sand'
    avax = 'avax'
    mkr = 'mkr'
    gmt = 'gmt'
    usdc = 'usdc'
    
class Path(Enum):

    # Public market data
    GET_ORDER_BOOK = "/v2/orderbook/"
    GET_MARKET_DEPTH = "/v2/depth/"
    GET_TRADES = "/v2/trades/"
    GET_MARKET_STATS = "/market/stats"
    OHLCV = "/market/udf/history"
    GET_GLOBAL_MARKET_STATS = "/market/global-stats"
    
    # User info
    GET_USER_PROFILE = "/users/profile"
    GENERATE_WALLET_ADDRESS = "/users/wallets/generate-address"
    ADD_CARD = "/users/cards-add"
    ADD_ACCOUNT = "/users/accounts-add"
    GET_USER_LIMITATIONS = "/users/limitations"
    GET_WALLET_LIST = "/users/wallets/list"
    GET_WALLETS = "/v2/wallets"
    
class Resolution(Enum):

    _1MIN = '1'
    _5MIN = '5'
    _15MIN = '15'
    _30MIN = '30'
    _1HOUR = '60'
    _3HOUR = '180'
    _4HOUR = '240'
    _6HOUR = '360'
    _12HOUR = '720'
    _1DAY = 'D'
    _2DAY = '2D'
    _3DAY = '3D'
    
class TradeType(Enum):

    SPOT = "spot"
    MARGIN = "margin"


RESTAPIRequestType = Literal["GET", "POST", "PUT", "DELETE"]

