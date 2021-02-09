CREATE TABLE IF NOT EXISTS tickers (
  id SERIAL PRIMARY KEY,
  ticker VARCHAR(6) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS trades (
  id SERIAL PRIMARY KEY,
  ticker_id INTEGER NOT NULL,
  tid INTEGER NOT NULL,
  created_at BIGINT NOT NULL,
  price DECIMAL NOT NULL,
  amount DECIMAL NOT NULL,
  CONSTRAINT fk_ticker
    FOREIGN KEY(ticker_id)
    REFERENCES tickers(id)
    ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS trade_index ON trades
(
    ticker_id ASC,
	tid ASC
);
