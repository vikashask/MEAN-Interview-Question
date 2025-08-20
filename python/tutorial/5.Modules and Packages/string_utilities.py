# string_utilities.py - Another module example

"""
String utility functions module.
Demonstrates various string operations and utilities.
"""

import re
from typing import List, Optional

# Module constants
DEFAULT_SEPARATOR = ", "
WORD_PATTERN = r'\b\w+\b'

def capitalize_words(text: str) -> str:
    """Capitalize the first letter of each word."""
    return ' '.join(word.capitalize() for word in text.split())

def reverse_string(text: str) -> str:
    """Reverse a string."""
    return text[::-1]

def count_words(text: str) -> int:
    """Count the number of words in a string."""
    words = re.findall(WORD_PATTERN, text)
    return len(words)

def count_characters(text: str, include_spaces: bool = True) -> int:
    """Count characters in a string."""
    if include_spaces:
        return len(text)
    return len(text.replace(' ', ''))

def remove_duplicates(text: str) -> str:
    """Remove duplicate characters while preserving order."""
    seen = set()
    result = []
    for char in text:
        if char not in seen:
            seen.add(char)
            result.append(char)
    return ''.join(result)

def find_longest_word(text: str) -> Optional[str]:
    """Find the longest word in a string."""
    words = re.findall(WORD_PATTERN, text)
    if not words:
        return None
    return max(words, key=len)

def is_palindrome(text: str) -> bool:
    """Check if a string is a palindrome (ignoring spaces and case)."""
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text.lower())
    return cleaned == cleaned[::-1]

def create_acronym(text: str) -> str:
    """Create an acronym from a string."""
    words = text.split()
    return ''.join(word[0].upper() for word in words if word)

def word_frequency(text: str) -> dict:
    """Return a dictionary of word frequencies."""
    words = re.findall(WORD_PATTERN, text.lower())
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

class TextAnalyzer:
    """A class for analyzing text."""
    
    def __init__(self, text: str):
        self.text = text
        self._words = None
        self._sentences = None
    
    @property
    def words(self) -> List[str]:
        """Get list of words (cached)."""
        if self._words is None:
            self._words = re.findall(WORD_PATTERN, self.text.lower())
        return self._words
    
    @property
    def sentences(self) -> List[str]:
        """Get list of sentences (cached)."""
        if self._sentences is None:
            self._sentences = [s.strip() for s in re.split(r'[.!?]+', self.text) if s.strip()]
        return self._sentences
    
    def summary(self) -> dict:
        """Get a summary of text statistics."""
        return {
            'character_count': len(self.text),
            'character_count_no_spaces': count_characters(self.text, False),
            'word_count': len(self.words),
            'sentence_count': len(self.sentences),
            'longest_word': find_longest_word(self.text),
            'is_palindrome': is_palindrome(self.text),
            'word_frequency': word_frequency(self.text)
        }

def main():
    """Test the string utilities module."""
    test_text = "Hello World! This is a test string. A test string for testing."
    
    print("String Utilities Test:")
    print(f"Original: {test_text}")
    print(f"Capitalized: {capitalize_words(test_text.lower())}")
    print(f"Reversed: {reverse_string(test_text)}")
    print(f"Word count: {count_words(test_text)}")
    print(f"Character count: {count_characters(test_text)}")
    print(f"Longest word: {find_longest_word(test_text)}")
    print(f"Is palindrome: {is_palindrome('A man a plan a canal Panama')}")
    print(f"Acronym: {create_acronym('Python Is Amazing Language')}")
    
    # Test TextAnalyzer
    analyzer = TextAnalyzer(test_text)
    print(f"\nText Analysis Summary:")
    for key, value in analyzer.summary().items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()