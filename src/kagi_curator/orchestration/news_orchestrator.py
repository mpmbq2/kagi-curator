"""
Abstract base class for orchestrating the complete news curation workflow.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import datetime

from ..curation.news_factory import NewsFactory
from ..formatting.base_formatter import BaseFormatter


class NewsOrchestrator(ABC):
    """
    Abstract base class for orchestrating the complete news curation workflow.
    
    The NewsOrchestrator coordinates multiple NewsFactory objects, aggregates
    their results, and formats the final output using a Formatter instance.
    """
    
    def __init__(self, factories: List[NewsFactory], formatter: BaseFormatter):
        """
        Initialize the NewsOrchestrator.
        
        Args:
            factories: List of NewsFactory objects to execute in sequence
            formatter: Formatter instance to use for final output formatting
        """
        self.factories = factories
        self.formatter = formatter
    
    @abstractmethod
    def _determine_execution_order(self) -> List[NewsFactory]:
        """
        Determine the order in which factories should be executed.
        
        Returns:
            List of NewsFactory objects in execution order
        """
        pass
    
    @abstractmethod
    def _aggregate_results(self, factory_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate results from all factories into a single data structure.
        
        Args:
            factory_results: List of dictionaries from each factory's generate_section() method
            
        Returns:
            Aggregated data structure ready for formatting
        """
        pass
    
    def generate_newsletter(self) -> str:
        """
        Execute the complete news curation workflow.
        
        Returns:
            Formatted string ready for output (email, web display, etc.)
        """
        # Determine execution order
        ordered_factories = self._determine_execution_order()
        
        # Execute each factory
        factory_results = []
        all_errors = []
        
        for factory in ordered_factories:
            try:
                result = factory.generate_section()
                factory_results.append(result)
                # Collect errors from factories
                if "_metadata" in result and "errors" in result["_metadata"]:
                    all_errors.extend(result["_metadata"]["errors"])
            except Exception as e:
                all_errors.append(f"Factory {factory.__class__.__name__} failed: {str(e)}")
        
        # Aggregate results
        aggregated_data = self._aggregate_results(factory_results)
        
        # Add overall metadata
        aggregated_data["_metadata"] = {
            "factory_count": len(ordered_factories),
            "successful_factories": len([r for r in factory_results if "_metadata" in r]),
            "total_errors": len(all_errors),
            "errors": all_errors,
            "generation_timestamp": datetime.datetime.now()
        }
        
        # Format final output
        return self.formatter.format(aggregated_data)