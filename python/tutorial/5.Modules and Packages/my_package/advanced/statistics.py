# statistics.py - Statistical analysis module

"""
Statistical analysis utilities for the advanced subpackage.
"""

import math
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter

class StatisticalAnalyzer:
    """Advanced statistical analysis class."""
    
    def __init__(self, data: List[float] = None):
        self.data = data or []
        self.cache = {}
    
    def load_data(self, data: List[float]):
        """Load new data and clear cache."""
        self.data = data
        self.cache = {}
    
    def add_data_point(self, value: float):
        """Add a single data point."""
        self.data.append(value)
        self.cache = {}  # Clear cache when data changes
    
    def _calculate_if_needed(self, key: str, calculation_func):
        """Cache calculation results."""
        if key not in self.cache:
            self.cache[key] = calculation_func()
        return self.cache[key]
    
    def mean(self) -> float:
        """Calculate mean."""
        return self._calculate_if_needed('mean', lambda: sum(self.data) / len(self.data))
    
    def variance(self, population: bool = False) -> float:
        """Calculate variance."""
        def calc_variance():
            mean_val = self.mean()
            squared_diffs = [(x - mean_val) ** 2 for x in self.data]
            divisor = len(self.data) if population else len(self.data) - 1
            return sum(squared_diffs) / divisor
        
        key = 'population_variance' if population else 'sample_variance'
        return self._calculate_if_needed(key, calc_variance)
    
    def standard_deviation(self, population: bool = False) -> float:
        """Calculate standard deviation."""
        return math.sqrt(self.variance(population))
    
    def z_scores(self) -> List[float]:
        """Calculate z-scores for all data points."""
        def calc_z_scores():
            mean_val = self.mean()
            std_dev = self.standard_deviation()
            return [(x - mean_val) / std_dev for x in self.data]
        
        return self._calculate_if_needed('z_scores', calc_z_scores)
    
    def percentile(self, p: float) -> float:
        """Calculate the p-th percentile."""
        if not 0 <= p <= 100:
            raise ValueError("Percentile must be between 0 and 100")
        
        sorted_data = sorted(self.data)
        index = (p / 100) * (len(sorted_data) - 1)
        
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower_index = int(index)
            upper_index = lower_index + 1
            weight = index - lower_index
            return sorted_data[lower_index] * (1 - weight) + sorted_data[upper_index] * weight
    
    def quartiles(self) -> Tuple[float, float, float]:
        """Calculate Q1, Q2 (median), Q3."""
        return self.percentile(25), self.percentile(50), self.percentile(75)
    
    def iqr(self) -> float:
        """Calculate Interquartile Range."""
        q1, _, q3 = self.quartiles()
        return q3 - q1
    
    def outliers(self, method: str = 'iqr') -> List[float]:
        """Detect outliers using IQR or z-score method."""
        if method == 'iqr':
            q1, _, q3 = self.quartiles()
            iqr_val = self.iqr()
            lower_bound = q1 - 1.5 * iqr_val
            upper_bound = q3 + 1.5 * iqr_val
            return [x for x in self.data if x < lower_bound or x > upper_bound]
        
        elif method == 'zscore':
            z_scores = self.z_scores()
            return [self.data[i] for i, z in enumerate(z_scores) if abs(z) > 2]
        
        else:
            raise ValueError("Method must be 'iqr' or 'zscore'")
    
    def correlation(self, other_data: List[float]) -> float:
        """Calculate Pearson correlation coefficient with another dataset."""
        if len(self.data) != len(other_data):
            raise ValueError("Datasets must have the same length")
        
        n = len(self.data)
        sum_x = sum(self.data)
        sum_y = sum(other_data)
        sum_xy = sum(x * y for x, y in zip(self.data, other_data))
        sum_x2 = sum(x ** 2 for x in self.data)
        sum_y2 = sum(y ** 2 for y in other_data)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))
        
        return numerator / denominator if denominator != 0 else 0
    
    def linear_regression(self, y_data: List[float]) -> Tuple[float, float]:
        """Calculate linear regression coefficients (slope, intercept)."""
        if len(self.data) != len(y_data):
            raise ValueError("Datasets must have the same length")
        
        n = len(self.data)
        sum_x = sum(self.data)
        sum_y = sum(y_data)
        sum_xy = sum(x * y for x, y in zip(self.data, y_data))
        sum_x2 = sum(x ** 2 for x in self.data)
        
        # Calculate slope (m) and intercept (b) for y = mx + b
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        return slope, intercept
    
    def summary_statistics(self) -> Dict[str, Any]:
        """Get comprehensive summary statistics."""
        if not self.data:
            return {"error": "No data available"}
        
        q1, median, q3 = self.quartiles()
        
        return {
            "count": len(self.data),
            "mean": self.mean(),
            "median": median,
            "mode": self._calculate_mode(),
            "std_dev": self.standard_deviation(),
            "variance": self.variance(),
            "min": min(self.data),
            "max": max(self.data),
            "range": max(self.data) - min(self.data),
            "q1": q1,
            "q3": q3,
            "iqr": self.iqr(),
            "outliers_count": len(self.outliers()),
            "skewness": self._calculate_skewness(),
            "kurtosis": self._calculate_kurtosis()
        }
    
    def _calculate_mode(self) -> Any:
        """Calculate mode of the data."""
        counter = Counter(self.data)
        max_count = max(counter.values())
        modes = [k for k, v in counter.items() if v == max_count]
        return modes[0] if len(modes) == 1 else modes
    
    def _calculate_skewness(self) -> float:
        """Calculate skewness (measure of asymmetry)."""
        mean_val = self.mean()
        std_dev = self.standard_deviation()
        n = len(self.data)
        
        skew = sum(((x - mean_val) / std_dev) ** 3 for x in self.data) / n
        return skew
    
    def _calculate_kurtosis(self) -> float:
        """Calculate kurtosis (measure of tail heaviness)."""
        mean_val = self.mean()
        std_dev = self.standard_deviation()
        n = len(self.data)
        
        kurt = sum(((x - mean_val) / std_dev) ** 4 for x in self.data) / n
        return kurt - 3  # Subtract 3 for excess kurtosis