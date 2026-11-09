"""Core Hierarchical Memory Decay Consolidator implementation."""
import time
import math
from enum import Enum
from typing import Dict, List, Optional, Any


class MemoryTier(str, Enum):
    WORKING = "WORKING"
    EPISODIC = "EPISODIC"
    SEMANTIC = "SEMANTIC"


class MemoryEntry:
    def __init__(self, key: str, content: str, tier: MemoryTier = MemoryTier.WORKING, salience: float = 1.0):
        self.key = key
        self.content = content
        self.tier = tier
        self.salience = salience
        self.access_count = 1
        self.created_at = time.time()
        self.last_accessed = time.time()


class HierarchicalMemory:
    def __init__(self, working_half_life: float = 60.0, episodic_half_life: float = 3600.0):
        self.working_half_life = working_half_life
        self.episodic_half_life = episodic_half_life
        self.entries: Dict[str, MemoryEntry] = {}

    def store(self, key: str, content: str, salience: float = 1.0) -> MemoryEntry:
        entry = MemoryEntry(key, content, MemoryTier.WORKING, salience)
        self.entries[key] = entry
        return entry

    def retrieve(self, key: str) -> Optional[str]:
        if key not in self.entries:
            return None
        entry = self.entries[key]
        entry.access_count += 1
        entry.last_accessed = time.time()
        # Hebbian access boosts salience
        entry.salience = min(2.0, entry.salience + 0.2)

        # Check for promotion to Episodic or Semantic
        if entry.tier == MemoryTier.WORKING and entry.access_count >= 3:
            entry.tier = MemoryTier.EPISODIC
        elif entry.tier == MemoryTier.EPISODIC and entry.access_count >= 6:
            entry.tier = MemoryTier.SEMANTIC

        return entry.content

    def run_decay_cycle(self, elapsed_seconds: float = 60.0):
        keys_to_remove = []
        for key, entry in self.entries.items():
            if entry.tier == MemoryTier.SEMANTIC:
                # Semantic memories are consolidated permanent knowledge
                continue

            half_life = self.working_half_life if entry.tier == MemoryTier.WORKING else self.episodic_half_life
            decay_factor = math.pow(0.5, elapsed_seconds / max(1.0, half_life))
            entry.salience *= decay_factor

            if entry.salience < 0.1:
                keys_to_remove.append(key)

        for k in keys_to_remove:
            del self.entries[k]
