"""Lightweight utility for constructing context windows."""
from __future__ import annotations

from typing import Iterable, List


class ContextWindow:
    """Generate overlapping text windows for model friendly chunking."""

    def __init__(self, window_size: int, overlap: int = 0) -> None:
        if window_size <= 0:
            msg = "window_size must be greater than zero"
            raise ValueError(msg)
        if overlap < 0:
            msg = "overlap must be zero or positive"
            raise ValueError(msg)
        if overlap >= window_size:
            msg = "overlap must be smaller than window_size"
            raise ValueError(msg)
        self.window_size = window_size
        self.overlap = overlap

    def _sliding_slices(self, tokens: List[str]) -> Iterable[List[str]]:
        start = 0
        step = self.window_size - self.overlap
        while start < len(tokens):
            yield tokens[start : start + self.window_size]
            if step <= 0:
                break
            start += step

    def generate(self, text: str) -> List[str]:
        """Return windows that preserve whitespace separation."""

        tokens = text.split()
        if not tokens:
            return []
        return [" ".join(chunk) for chunk in self._sliding_slices(tokens)]

    def __call__(self, text: str) -> List[str]:
        return self.generate(text)
