import pickle

from crypto_bot.database import db
from crypto_bot.utils.func import named_timer, ticker_to_path
from crypto_bot.puller.queries import Queries
from crypto_bot.data_preparator.sequencer import Sequencer
from crypto_bot.data_preparator.trade_filter import TradeFilter


class Preparator:
    @named_timer('data set preparation')
    def prepare(self, ticker):
        with db.get_db() as _db:
            queries = Queries(_db)
            prices = TradeFilter().filter(queries.select_all_by_ticker(ticker))
            self._ticker = ticker
            self._data_set = Sequencer().generate(prices).normalize().to_dict()
        return self

    def save(self):
        with open(ticker_to_path(self._ticker), 'wb') as pickle_file:
            pickle.dump(self._data_set, pickle_file)

    def load(self, ticker):
        with open(ticker_to_path(ticker), 'rb') as pickle_file:
            data_set = pickle.load(pickle_file)
            print(data_set)
