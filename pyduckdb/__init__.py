"""
Pure Python wrapper around DuckDB's pybind11 generated wrapper.

This API is intended to eventually be a drop-in replacement for SQLite
in most cases.

"""
from pyduckdb.exceptions import *
from pyduckdb.core import *