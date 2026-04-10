"""
Abstract base class for grouping NewsCurator objects into logical sections.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import datetime

from ..models.result import Result
from .news_curator import NewsCurator


class NewsFactory(ABC):
    """
    Abstract base class for grouping NewsCurator objects into logical sections.
    
    A NewsFactory manages multiple NewsCurator objects that together constitute
    a logical news section (e.g., "Vermont" with subsections "Statewide" and "Lamoille County").
    """
    
    def __init__(self, section_name: str, curators: List[NewsCurator]):
        """
        Initialize the NewsFactory.
        
        Args:
            section_name: Name of this news section (e.g., "Vermont", "National")
            curators: List of NewsCurator objects for subsections within this section
        """
        self.section_name = section_name
        self.curators = curators
    
    @abstractmethod
    def _organize_results(self, results: List[Result]) -> Dict[str, Any]:
        """
        Organize the results from subsection curators into a section structure.
        
        Args:
            results: List of Result objects from each subsection curator
            
        Returns:
            Dictionary representing the organized section data
        """
        pass
    
    def generate_section(self) -> Dict[str, Any]:
        """
        Generate the complete section by executing all subsection curators.
        
        Returns:
            Dictionary containing the organized section data
        """
        subsection_results = []
        all_errors = []
        
        # Execute each curator
        for curator in self.curators:
            try:
                result = curator.curate()
                subsection_results.append(result)
                # Collect errors from curators
                all_errors.extend(result.errors)
            except Exception as e:
                all_errors.append(f"Curator {curator.__class__.__name__} failed: {str(e)}")
        
        # Organize results into section structure
        organized_data = self._organize_results(subsection_results)
        
        # Add metadata
        organized_data["_metadata"] = {
            "section_name": self.section_name,
            "subsection_count": len(self.curators),
            "successful_subsections": len([r for r in subsection_results if len(r.articles) > 0]),
            "total_articles": sum(len(r.articles) for r in subsection_results),
            "errors": all_errors,
            "generation_timestamp": datetime.datetime.now()
        }
        
        return organized_data