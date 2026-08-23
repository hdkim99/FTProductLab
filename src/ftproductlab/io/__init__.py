"""Documented file input and result export."""

from .csv import read_product_csv
from .export import result_to_dict, write_analysis_bundle

__all__ = ["read_product_csv", "result_to_dict", "write_analysis_bundle"]
