from __future__ import annotations

from abc import ABC, abstractmethod


class BaseDeliverer(ABC):
    """Abstract base for newsletter delivery mechanisms."""

    @abstractmethod
    def deliver(self, subject: str, html_content: str, plain_content: str = "") -> None:
        """Deliver the newsletter. Raises on failure."""
