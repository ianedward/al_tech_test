CREATE TABLE issues(
  id INTEGER PRIMARY KEY,
  title VARCHAR(255),
  description TEXT,
  opened_datetime CHAR(26) DEFAULT (datetime('now', 'localtime')),
  closed_datetime CHAR(26)
)
