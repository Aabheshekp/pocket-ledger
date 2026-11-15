# Pocket Ledger

A Python desktop expense tracker built with Tkinter and SQLite. Add, list, and delete expenses; see the current month's total; and export all rows to CSV. Records are stored locally in `pocket-ledger.sqlite3`.

## Requirements

Python 3.10+ with Tk support (usually included in the standard Windows Python installer).

## Run

```sh
python app.py
```

Amounts use the user's chosen currency; the app does not perform currency conversion. Back up the database file to preserve records.

### Category

App development | Python, Tkinter, SQLite
