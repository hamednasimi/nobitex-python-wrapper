# Originally published by Hamed Nasimi at 

import asyncio
import aiohttp
import time
from .utils import *

# TODO Make the exception class
# TODO Make the methods argument lists fool-proof (conditions and assertions)
# TODO Make importing the client also import the `utils` classes

class Client:
    """
    The class for handling the setup and configuration of the client object.
    """
    
    # Constants
    
    REST_API_BASE_URL = 'https://api.nobitex.ir'
    
    # Dunder methods

    def __init__(
        self, 
        api_token: str = None, 
        bot_mode: bool = True, 
        bot_name: str = 'WrapperBot', 
        rate_limiter: bool = True
        ) -> None:
        """
        Initializes the client with the given API token and sets up the necessary resources.
        
        Args:
            api_token: The API token to use for authentication.
            bot_mode: Whether to run in bot mode or not. Defaults to True.
            bot_name: The name of the bot. Defaults to 'WrapperBot'.
            rate_limiter: Whether to use the built-in rate limiter. Defaults to True.
            
        Returns:
            None
            
        Raises:
            None
        """
        
        self.__session = aiohttp.ClientSession(base_url=Client.REST_API_BASE_URL)
        
    # Methods
    
    async def close(self) -> None:
        """
        The function to run when closing the aiohttp session.
        """
        await self.__session.close()
        
    async def __get(
        self, 
        url: str, 
        params: dict = None
        ) -> dict:
        """
        The main coroutine for handling GET requests.
        
        Args:
            url: The URL of the API endpoint to call.
            params: The dictionary that will get converted to query string.
            
        Returns:
            A dictionary containing the response.
        """
        
        # print(params) # DEBUG
        if url and not params:
            response = await self.__session.get(f"{url}")
        elif url and params:
            response = await self.__session.get(f"{url}", params=params)
        # print(response.url)
        return await response.json()
    
    async def __post(
        self, 
        url: str, 
        params: dict = None
        ) -> dict:
        """
        The main coroutine for handling POST requests.
        
        Args:
            url: The URL of the API endpoint to call.
            params: The dictionary that will get converted to query string.
            
        Returns:
            A dictionary containing the response.
        """
        # print(url) # DEBUG
        if url and not params:
            response = await self.__session.post(f"{url}")
        elif url and params:
            response = await self.__session.post(f"{url}", params=params)
        # print(response.url)
        return await response.json()
    
    async def get_order_book(
        self, 
        symbol: Symbol
        ) -> dict:
        """
        Get the order book for a given symbol or all the available symbols.
        
        Rate limit: 60/min
        Token: Not required

        Args:
            Symbol (symbol): The symbol to get the order book for.
            To get the result for all symbols use `Symbol.ALL`.

        Returns:
            The order book data as a dictionary.
            
        Raises:
            None
        """
        
        return await self.__get(f"{Path.GET_ORDER_BOOK.value}{symbol.value}")

    async def get_market_depth(
        self, 
        symbol: Symbol
        ) -> dict:
        """
        Get the market depth for a given symbol.
        
        Rate limit: 60/min
        Token: Not required

        Args:
            Symbol (symbol): The symbol to get the market depth for.
            Can't pass `Symbol.ALL` as the argument.

        Returns:
            The market depth data as a dictionary.
            
        Raises:
            None
        """
        if symbol == Symbol.ALL:
            raise ValueError("Can't get the market depth for all symbols at once.\
Consider fetching them by calling this method for each individual symbol.")
        return await self.__get(f"{Path.GET_MARKET_DEPTH.value}{symbol.value}")
    
    async def get_trades(
        self, 
        symbol: Symbol
        ) -> dict:
        """
        Get the list of trades for a given symbol.
        
        Rate limit: 15/min
        Token: Not required

        Args:
            Symbol (symbol): The symbol to get the list of trades for.
            Can't pass `Symbol.ALL` as the argument.

        Returns:
            The list of trades as a dictionary.
            
        Raises:
            None
        """
        
        if symbol == Symbol.ALL:
            raise ValueError("Can't get the trades data for all symbols at once.\
Consider fetching them by calling this method for each individual symbol.")
        return await self.__get(f"{Path.GET_TRADES.value}{symbol.value}")
    
    async def get_market_stats(
        self, 
        *source_currency: tuple[Currency, ...], 
        destination_currency: Currency
        ) -> dict:
        """
        Get the latest market stats for one/multiple source(s) and one destination currency.
        
        Rate limit: 100/min
        Token: Not required

        Args:
            source_currency (srcCurrency): The source currency/currencies.
            destination_currency (dstCurrency): The destination currency.

        Returns:
            The market stats as a dictionary.
            
        Raises:
            None
        """
        
        sources = ",".join(i.value for i in source_currency)
        return await self.__get(
            f"{Path.GET_MARKET_STATS.value}", 
            params={"srcCurrency": sources, "dstCurrency": destination_currency.value})
        
    async def ohlcv(
        self, 
        symbol: Symbol, 
        resolution: Resolution,
        from_: int,
        to_: int,
        countback: int,
        page: int = 1
        ) -> dict:
        
        """
        Get the OHLCV data for the given timeframe.
        
        Rate limit: N/A
        Token: Not required

        Args:
            symbol: The symbol for which to get the OHLCV data.
            resolution: The candle timeframe.
            from_: Beginning time (in unix time)
            to_: End time (in unix time)
            countback: The number of candles before `to_` to fetch.
            (higher precedence than `from_`)
            page: The number of pages to split the returning results into.

        Returns:
            OHLCV data as a dictionary.
            
        Raises:
            None
        """
        
        return await self.__get(
            f"{Path.OHLCV.value}", 
            params={"symbol": symbol.value, 
                    "resolution": resolution.value, 
                    "from": from_, 
                    "to": to_, 
                    "countback": countback, 
                    "page": page})
        
    async def get_global_market_stats(self) -> dict:
        """
        Get the latest global market stats from Binance and Kraken.
        
        Rate limit: 100/10min
        Token: Not required

        Args:
            None

        Returns:
            The global market stats as a dictionary.
            
        Raises:
            None
        """
        
        return await self.__post(
            f"{Path.GET_GLOBAL_MARKET_STATS.value}")