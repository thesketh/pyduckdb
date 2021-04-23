"""
Type constructors as specified by PEP-249.

"""
import datetime as dt

__all__ = [
    "Date",
    "Time",
    "Timestamp",
    "DateFromTicks",
    "TimeFromTicks",
    "TimestampFromTicks",
    "Binary",
    "STRING",
    "BINARY",
    "NUMBER",
    "DATETIME",
    "ROWID",
]

# Constructor definitions.
Date = dt.date
Time = dt.time
Timestamp = dt.datetime
DateFromTicks = dt.date.fromtimestamp
TimestampFromTicks = dt.datetime.fromtimestamp
TimeFromTicks = lambda timestamp: dt.datetime.fromtimestamp(timestamp).time()
Binary = bytes

# Type definitions.
STRING = str
BINARY = bytes
NUMBER = float
DATETIME = dt.datetime
ROWID = str
