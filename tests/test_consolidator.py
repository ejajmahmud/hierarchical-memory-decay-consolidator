"""Unit tests for hierarchical-memory-decay-consolidator."""
import unittest
from hierarchical_memory_decay_consolidator.consolidator import HierarchicalMemory, MemoryTier


class TestHierarchicalMemory(unittest.TestCase):
    def setUp(self):
        self.mem = HierarchicalMemory(working_half_life=2.0)

    def test_promotion_on_repeated_access(self):
        self.mem.store("pref", "val")
        self.assertEqual(self.mem.entries["pref"].tier, MemoryTier.WORKING)

        for _ in range(3):
            self.mem.retrieve("pref")
        self.assertEqual(self.mem.entries["pref"].tier, MemoryTier.EPISODIC)

    def test_decay_eviction(self):
        self.mem.store("fleeting", "temp", salience=0.2)
        self.mem.run_decay_cycle(10.0)
        self.assertNotIn("fleeting", self.mem.entries)
