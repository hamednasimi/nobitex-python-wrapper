# An unofficial wrapper for the Nobitex crypto exchange API

Currently supports the public API nodes including:

- The orderbook
- Market depth
- Trades
- Nobitex market stats
- OHLCV data
- Global market stats
- Get user profile data

## Get started

```python

import asyncio
from src.client import *

async def main():
    """
    Schedule tasks and get the results ASAP.
    """

    # Create the client
    client = Client()
    
    # If you need account-bound operations, use your token here.
    # client = Client('yourapitokenhere00000000000000000000')

    # Make a try/except block to catch exceptions
    try:
        # Schedule tasks
        tasks = [
            client.get_order_book(symbol=Symbol.BTCUSDT), 
            client.get_market_depth(symbol=Symbol.BTCUSDT), 
            client.get_trades(symbol=Symbol.BTCUSDT), 
            client.get_market_stats(Currency.btc, Currency.ada, destination_currency=Currency.usdt), 
            client.get_global_market_stats(),
            client.get_user_profile(), 
            client.generate_wallet_address(Currency.btc), 
            # client.add_card("bankCARDnumber", "bankNAME"), 
            # client.add_account("bankCARDnumber", "IR0000000000000000000000", "bankNAME"), 
            client.get_user_limitations(), 
            client.get_wallet_list(), 
            client.get_wallets(Currency.usdt, type=TradeType.MARGIN)
            ]

        # Run all of them and catch each result as soon as it's complete
        for future in asyncio.as_completed(tasks):
            result = await future

            # Print the server response in JSON/dictionary format
            print(result)

    except Exception as e:
        print(e)

    finally:
        # You need to close the client connection at the end of the program
        # Avoid creating unique clients for each request
        await client.close()
    
if __name__ == "__main__":
    asyncio.run(main())
```

The code seems to work reliably if you preserve the pattern above but it is not tested.
Use at your own risk.