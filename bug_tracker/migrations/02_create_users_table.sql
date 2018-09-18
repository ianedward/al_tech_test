CREATE TABLE users(
  id INTEGER PRIMARY KEY,
  name VARCHAR(255),
  password TEXT,
  datetime_joined CHAR(26) DEFAULT (datetime('now', 'localtime'))
)
