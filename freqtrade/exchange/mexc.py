import logging
from datetime import datetime, timedelta
from typing import Optional

from freqtrade.exchange import Exchange
from freqtrade.util.datetime_helpers import dt_now


logger = logging.getLogger(__name__)


class Mexc(Exchange):
    """
    Mexc exchange class. Contains adjustments needed for Freqtrade to work
    with this exchange.

    Please note that this exchange is not included in the list of exchanges
    officially supported by the Freqtrade development team. So some features
    may still not work as expected.
    """

    def fetch_orders(self, pair: str, since: datetime, params: Optional[dict] = None) -> list[dict]:
        """
        Fetch all orders for a pair "since"
        :param pair: Pair for the query
        :param since: Starting time for the query
        """

        # On mexc, since cannot be more than 7 days.
        # we therefore can only get orders which are within 7 days.
        orders = []

        seven_days_exchange_limit = dt_now() - timedelta(days=7, minutes=-30)

        if since < seven_days_exchange_limit:
            since = seven_days_exchange_limit

        orders = super().fetch_orders(pair, since, params=params)

        return orders
