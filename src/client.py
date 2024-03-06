# Originally published by Hamed Nasimi at https://github.com/hamednasimi/nobitex-python-wrapper

import asyncio
import aiohttp
import time
from .utils import *

# TODO Make the exception class
# TODO Create the rate limiter
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
       Initializ es the client with the given API token and sets up the necessary resources.
        
        Args:
            api_token: The API token to use for authentication.
            bot_mode: Whether to run in bot mode or not. Defaults to `True`.
            bot_name: The name of the bot. Defaults to `'WrapperBot'`.
            rate_limiter: Whether to use the built-in rate limiter. Defaults to `True`.
            
        Returns:
            None
            
        Raises:
            None
        """
        
        if api_token:
            self.has_token = True
            self.__session = aiohttp.ClientSession(
                base_url=Client.REST_API_BASE_URL, 
                headers={"Authorization": f"Token {api_token}"})
        else:
            self.has_token = False
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
        params: dict = None, 
        headers: dict = None, 
        data: dict = None
        ) -> dict:
        """
        The main coroutine for handling GET requests.
        
        Args:
            url: The URL of the API endpoint to call.
            params: The `dict` that will get converted to query string.
            
        Returns:
            A `dict` containing the response.
        """
        
        # print(str(data)) # DEBUG
        response = await self.__session.get(
            f"{url}", 
            params=params, 
            headers=headers, 
            data=str(data))
        print(response.url)
        return await response.json()
    
    async def __post(
        self, 
        url: str, 
        params: dict = None, 
        headers: dict = None,
        data: dict = None
        ) -> dict:
        """
        The main coroutine for handling POST requests.
        
        Args:
            url: The URL of the API endpoint to call.
            params: The `dict` that will get converted to query string.
            
        Returns:
            A `dict` containing the response.
        """
        
        print(data) # DEBUG
        print(type(data)) # DEBUG
        response = await self.__session.post(
            f"{url}", 
            params=params, 
            headers=headers, 
            data=str(data))
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
            The order book data as a `dict`.
            
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
            The market depth data as a `dict`.
            
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
            The list of trades as a `dict`.
            
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
            The market stats as a `dict`.
            
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
            OHLCV data as a `dict`.
            
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
            The global market stats as a `dict`.
            
        Raises:
            None
        """
        
        return await self.__post(
            f"{Path.GET_GLOBAL_MARKET_STATS.value}")
        
    async def get_user_profile(self) -> dict:
        """
        Get the user info including card info, bank account info etc.
        
        Rate limit: N/A
        Token: Required

        Args:
            None

        Returns:
            Dictionary containing user info.
                        
        Raises:
            None
        """
        
        if self.has_token:
            return await self.__get(Path.GET_USER_PROFILE.value)
        else:
            raise Exception("The client does not have a token! \
Initialize the client using your API token as such: \
`client = Client('apitoken0000000000000')`")
        
    async def generate_wallet_address(
        self, 
        currency: Currency = None, 
        wallet: str = None
        ) -> dict:
        """
        Generate a wallet address for the user.
        
        Rate limit: 30/h
        Token: Required
        
        Args:
            currency: Which currency to create the address for.
            `currency` is required if `wallet` is not passed to the method.
            wallet: The wallet ID. Required if `currency` is not passed.
            If both `currency` and `wallet` are passed, `currency` has precedence.

        Returns:
            `dict` containing the generated address.
        
        Raises:
            None
        """
        
        if currency and not wallet:
            data = {"currency": currency.value}
        elif wallet and not currency:
            data = {"wallet": str(wallet)}
        elif wallet and currency:
            data = {"currency": currency.value, "wallet": str(wallet)}
        elif not currency and not wallet:
            raise Exception("At least one of the argument is needed.")
        if self.has_token:
            return await self.__post(
                Path.GENERATE_WALLET_ADDRESS.value, 
                headers={"content-type": "application/json"},
                data=data)
        else:
            raise Exception("The client does not have a token! \
Initialize the client using your API token as such: \
`client = Client('yourTOKENhereHEX0000000000')`")

    async def add_card(
        self, 
        number: int, 
        bank: str
        ) -> dict:
        """
        Add an iranian bank card to the Nobitex account.
        
        Rate limit: 30/30min
        Token: Required
        
        Args:
            number: The card number to add to the Nobitex account.
            bank: The name of the bank in Persian.

        Returns:
            `dict` containing the status of the request.
        
        Raises:
            None
        """
        
        if number and bank:
            data = {"number": str(number), "bank": str(bank)}
        else:
            raise Exception("Both `number` and `bank` arguments are required.")
        if self.has_token:
            return await self.__post(
                Path.ADD_CARD.value, 
                headers={"content-type": "application/json"},
                data=data)
        else:
            raise Exception("The client does not have a token! \
Initialize the client using your API token as such: \
`client = Client('yourTOKENhereHEX0000000000')`")

    async def add_account(
        self, 
        number: int, 
        shaba: str, 
        bank: str
        ) -> dict:
        """
        Add an iranian bank account to the Nobitex account.
        
        Rate limit: 30/30min
        Token: Required
        
        Args:
            number: The card number to add to the Nobitex account.
            shaba: The bank account's shaba number.
            bank: The name of the bank in Persian.

        Returns:
            `dict` containing the status of the request.
        
        Raises:
            None
        """
        
        data = {}
        if number and shaba and bank:
            data = {"number": str(number), "shaba": str(shaba), "bank": str(bank)}
        else:
            raise Exception("All of the `number`, `shaba` and `bank` arguments are required.")
        if self.has_token:
            return await self.__post(
                Path.ADD_ACCOUNT.value, 
                headers={"content-type": "application/json"},
                data=data)
        else:
            raise Exception("The client does not have a token! \
Initialize the client using your API token as such: \
`client = Client('yourTOKENhereHEX0000000000')`")

    async def get_user_limitations(
        self, 
        ) -> dict:
        """
        Get the limitations on the actions the user can take and the amount of \
allowed withdrawals from the website.
        
        Rate limit: N/A
        Token: Required
        
        Args:
            None

        Returns:
            `dict` containing the user limits.
        
        Raises:
            None
        """
        
        if self.has_token:
            return await self.__post(
                Path.GET_USER_LIMITATIONS.value, 
                headers={"content-type": "application/json"},)
        else:
            raise Exception("The client does not have a token! \
Initialize the client using your API token as such: \
`client = Client('yourTOKENhereHEX0000000000')`")
        
    async def get_wallet_list(
        self
        ) -> dict:
        """
        Get the list of wallets in the user account.
        
        Rate limit: 20/2min
        Token: Required
        
        Args:
            None

        Returns:
            `dict` containing the user wallets.
        
        Raises:
            None
        """
        
        if self.has_token:
            return await self.__get(
                Path.GET_WALLET_LIST.value)
        else:
            raise Exception("The client does not have a token! \
Initialize the client using your API token as such: \
`client = Client('yourTOKENhereHEX0000000000')`")
        
    async def get_wallets(
        self, 
        *currencies: tuple[Currency, ...], 
        type: TradeType = TradeType.SPOT
        ) -> dict:
        """
        Get the list of wallets in the user account.
        By default returns spot wallets.
        
        Rate limit: 12/min
        Token: Required
        
        Args:
            currencies: The source currency/currencies.
            type: The type of wallet you need the address for (spot or margin).

        Returns:
            `dict` containing the user wallets.
        
        Raises:
            None
        """
        
        if type not in [TradeType.SPOT, TradeType.MARGIN]:
            raise Exception("The type needs to be either `TradeType.SPOT` or `TradeType.MARGIN`")
        params = {"type": type.value}
        if currencies:
            params.update({"currencies": ",".join(i.value for i in currencies)})
        if self.has_token:
            return await self.__get(
                Path.GET_WALLETS.value, 
                params=params)
        else:
            raise Exception("The client does not have a token! \
Initialize the client using your API token as such: \
`client = Client('yourTOKENhereHEX0000000000')`")
