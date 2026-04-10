"""
Abstract base class for formatting news data into various output formats.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseFormatter(ABC):
    """
    Abstract base class for formatting news data into various output formats.
    
    This interface allows the NewsOrchestrator to remain agnostic about the 
    final output format, enabling easy extension to support web, plain text,
    JSON, or other formats without changing core logic.
    """
    
    @abstractmethod
    def format(self, data: Dict[str, Any]) -> str:
        """
        Format the structured news data into a string representation.
        
        Args:
            data: Structured news data containing sections, subsections, and articles
            
        Returns:
            Formatted string ready for output (HTML, plain text, etc.)
        """
        pass
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'format') and 
                callable(subclass.format))