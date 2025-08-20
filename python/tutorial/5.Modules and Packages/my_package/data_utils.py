# data_utils.py - Data processing utilities submodule

"""
Data processing utility functions for the my_package package.
"""

import statistics
from typing import List, Dict, Any, Union, Optional
from collections import Counter

def calculate_mean(numbers: List[Union[int, float]]) -> float:
    """Calculate the arithmetic mean of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(numbers) / len(numbers)

def calculate_median(numbers: List[Union[int, float]]) -> float:
    """Calculate the median of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate median of empty list")
    return statistics.median(numbers)

def calculate_mode(numbers: List[Union[int, float]]) -> Union[int, float]:
    """Calculate the mode of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate mode of empty list")
    return statistics.mode(numbers)

def calculate_standard_deviation(numbers: List[Union[int, float]]) -> float:
    """Calculate the standard deviation of a list of numbers."""
    if len(numbers) < 2:
        raise ValueError("Need at least 2 numbers for standard deviation")
    return statistics.stdev(numbers)

def remove_duplicates(data: List[Any]) -> List[Any]:
    """Remove duplicates while preserving order."""
    seen = set()
    result = []
    for item in data:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def filter_by_criteria(data: List[Dict[str, Any]], field: str, value: Any) -> List[Dict[str, Any]]:
    """Filter list of dictionaries by field value."""
    return [item for item in data if item.get(field) == value]

def sort_by_field(data: List[Dict[str, Any]], field: str, reverse: bool = False) -> List[Dict[str, Any]]:
    """Sort list of dictionaries by a specific field."""
    return sorted(data, key=lambda x: x.get(field, 0), reverse=reverse)

def group_by_field(data: List[Dict[str, Any]], field: str) -> Dict[Any, List[Dict[str, Any]]]:
    """Group list of dictionaries by a specific field."""
    groups = {}
    for item in data:
        key = item.get(field)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups

def count_occurrences(data: List[Any]) -> Dict[Any, int]:
    """Count occurrences of each item in a list."""
    return dict(Counter(data))

def find_outliers(numbers: List[Union[int, float]], threshold: float = 2.0) -> List[Union[int, float]]:
    """Find outliers using standard deviation method."""
    if len(numbers) < 3:
        return []
    
    mean = calculate_mean(numbers)
    std_dev = calculate_standard_deviation(numbers)
    
    outliers = []
    for num in numbers:
        if abs(num - mean) > threshold * std_dev:
            outliers.append(num)
    
    return outliers

class DataProcessor:
    """A comprehensive data processing class."""
    
    def __init__(self, data: List[Any] = None):
        self.data = data or []
        self.processed_data = None
        self.metadata = {}
    
    def load_data(self, data: List[Any]):
        """Load new data into the processor."""
        self.data = data
        self.processed_data = None
        self.metadata = {}
    
    def add_data(self, items: Union[Any, List[Any]]):
        """Add new items to existing data."""
        if isinstance(items, list):
            self.data.extend(items)
        else:
            self.data.append(items)
    
    def clean_data(self, remove_duplicates: bool = True, remove_none: bool = True) -> List[Any]:
        """Clean the data by removing duplicates and/or None values."""
        cleaned = self.data.copy()
        
        if remove_none:
            cleaned = [item for item in cleaned if item is not None]
        
        if remove_duplicates:
            cleaned = remove_duplicates(cleaned)
        
        self.processed_data = cleaned
        return cleaned
    
    def get_numeric_data(self) -> List[Union[int, float]]:
        """Extract only numeric data."""
        return [item for item in self.data if isinstance(item, (int, float))]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics for numeric data."""
        numeric_data = self.get_numeric_data()
        
        if not numeric_data:
            return {"error": "No numeric data found"}
        
        try:
            stats = {
                "count": len(numeric_data),
                "mean": calculate_mean(numeric_data),
                "median": calculate_median(numeric_data),
                "min": min(numeric_data),
                "max": max(numeric_data),
                "range": max(numeric_data) - min(numeric_data)
            }
            
            if len(numeric_data) >= 2:
                stats["std_dev"] = calculate_standard_deviation(numeric_data)
                stats["outliers"] = find_outliers(numeric_data)
            
            try:
                stats["mode"] = calculate_mode(numeric_data)
            except statistics.StatisticsError:
                stats["mode"] = "No unique mode"
            
            return stats
        except Exception as e:
            return {"error": f"Error calculating statistics: {e}"}
    
    def transform_data(self, transformer_func) -> List[Any]:
        """Apply a transformation function to all data items."""
        try:
            transformed = [transformer_func(item) for item in self.data]
            self.processed_data = transformed
            return transformed
        except Exception as e:
            raise ValueError(f"Error transforming data: {e}")
    
    def filter_data(self, filter_func) -> List[Any]:
        """Filter data using a custom function."""
        try:
            filtered = [item for item in self.data if filter_func(item)]
            self.processed_data = filtered
            return filtered
        except Exception as e:
            raise ValueError(f"Error filtering data: {e}")
    
    def export_summary(self) -> Dict[str, Any]:
        """Export a comprehensive summary of the data."""
        summary = {
            "total_items": len(self.data),
            "data_types": {},
            "statistics": self.get_statistics(),
            "sample_data": self.data[:5] if self.data else []
        }
        
        # Count data types
        for item in self.data:
            data_type = type(item).__name__
            summary["data_types"][data_type] = summary["data_types"].get(data_type, 0) + 1
        
        return summary

def merge_datasets(*datasets: List[Any]) -> List[Any]:
    """Merge multiple datasets into one."""
    merged = []
    for dataset in datasets:
        merged.extend(dataset)
    return merged

def split_dataset(data: List[Any], train_ratio: float = 0.8) -> tuple:
    """Split dataset into training and testing sets."""
    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1")
    
    split_index = int(len(data) * train_ratio)
    return data[:split_index], data[split_index:]