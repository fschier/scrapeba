"""
scrapeba - Scrape and consolidate data on the German labour market

This package scrapes and consolidates freely available data from the 
Bundesagentur für Arbeit on the German labour market.
"""

__version__ = "0.1.0"
__author__ = "Felix Schier"

from .get_district import get_district
from .get_data import get_data

__all__ = ["get_district", "get_data"]
