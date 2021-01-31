from src.database.db import get_db
from src.database.queries import Queries as PgQueries
from src.puller.queries import Queries as SqliteQueries
from src.utils.func import named_timer


class Migration:
    def sqlite_to_postgres(self):
        with get_db() as conn:
            sqlite_queries = SqliteQueries(conn)
            pg_queries = PgQueries()
            all_tickers = sqlite_queries.select_all_from_tickers()
            pg_queries.insert_tickers(all_tickers)
            for id, ticker in all_tickers:
                print(id, ticker)
                ticker_trades = sqlite_queries.select_all_by_ticker(ticker)
                trades_without_ids = [trade[1:] for trade in ticker_trades]
                print(trades_without_ids[0])
                named_timer(log_name=f'insert_trades for {ticker}')(pg_queries.insert_trades(trades_without_ids))
