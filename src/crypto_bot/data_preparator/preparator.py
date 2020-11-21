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
            data_set = Sequencer().generate(prices).normalize().to_dict()
            self.__save(data_set, ticker)

    def __save(self, model_data, ticker):
        with open(ticker_to_path(ticker), 'wb') as pickle_file:
            pickle.dump(model_data, pickle_file)

    def __load(self, ticker):
        with open(ticker_to_path(ticker), 'rb') as pickle_file:
            model_data = pickle.load(pickle_file)
            print(model_data)
