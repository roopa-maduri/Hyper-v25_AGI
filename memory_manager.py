"""
memory_manager.py - AGI Memory System
Stores and retrieves all experiences
"""

import json
import time
import pickle
import hashlib
from collections import defaultdict
from datetime import datetime

class MemoryManager:
    def __init__(self, storage_file="memory_store.json"):
        self.storage_file = storage_file
        self.memory_banks = {
            "short_term": [],
            "long_term": defaultdict(list),
            "procedural": [],  # How-to memories
            "semantic": {},    # Fact memories
            "episodic": []     # Experience memories
        }
        self.access_counter = 0
        
        # Load existing memories
        self._load_memories()
    
    def store(self, memory_type, data, metadata=None):
        """Store a memory"""
        memory_id = self._generate_memory_id(data)
        
        memory_entry = {
            "id": memory_id,
            "type": memory_type,
            "data": data,
            "metadata": metadata or {},
            "timestamp": time.time(),
            "access_count": 0,
            "importance": self._calculate_importance(data)
        }
        
        # Store in appropriate bank
        if memory_type in self.memory_banks:
            if isinstance(self.memory_banks[memory_type], list):
                self.memory_banks[memory_type].append(memory_entry)
            elif isinstance(self.memory_banks[memory_type], dict):
                key = metadata.get("category", "general") if metadata else "general"
                self.memory_banks[memory_type].setdefault(key, []).append(memory_entry)
        
        # Auto-save
        self._save_memories()
        
        return memory_id
    
    def retrieve(self, memory_type=None, query=None, limit=10):
        """Retrieve memories"""
        results = []
        
        if memory_type:
            # Retrieve from specific type
            bank = self.memory_banks.get(memory_type)
            if isinstance(bank, list):
                results = bank[-limit:]
            elif isinstance(bank, dict):
                # Get from all categories
                for category_memories in bank.values():
                    results.extend(category_memories[-5:])  # 5 from each category
                results = results[-limit:]
        else:
            # Retrieve from all banks
            for bank_name, bank in self.memory_banks.items():
                if isinstance(bank, list):
                    results.extend(bank[-3:])  # 3 from each list bank
                elif isinstance(bank, dict):
                    for cat_mem in bank.values():
                        results.extend(cat_mem[-2:])  # 2 from each category
        
        # Filter by query if provided
        if query:
            query_lower = query.lower()
            filtered = []
            for memory in results:
                memory_str = json.dumps(memory).lower()
                if query_lower in memory_str:
                    memory["access_count"] += 1
                    filtered.append(memory)
            results = filtered
        
        self.access_counter += 1
        return results[:limit]
    
    def search(self, query, memory_types=None):
        """Search across memories"""
        results = []
        search_types = memory_types or self.memory_banks.keys()
        
        for mem_type in search_types:
            bank = self.memory_banks.get(mem_type)
            
            if isinstance(bank, list):
                for memory in bank:
                    if self._matches_query(memory, query):
                        memory["access_count"] += 1
                        results.append(memory)
            elif isinstance(bank, dict):
                for category_memories in bank.values():
                    for memory in category_memories:
                        if self._matches_query(memory, query):
                            memory["access_count"] += 1
                            results.append(memory)
        
        # Sort by importance and recency
        results.sort(key=lambda x: (
            x.get("importance", 0),
            x.get("timestamp", 0)
        ), reverse=True)
        
        return results[:20]
    
    def _matches_query(self, memory, query):
        """Check if memory matches query"""
        query_lower = query.lower()
        memory_str = json.dumps(memory).lower()
        return query_lower in memory_str
    
    def _generate_memory_id(self, data):
        """Generate unique memory ID"""
        data_str = json.dumps(data, sort_keys=True)
        return f"mem_{hashlib.md5(data_str.encode()).hexdigest()[:8]}"
    
    def _calculate_importance(self, data):
        """Calculate memory importance (0-1)"""
        # Simple heuristic based on data size and content
        data_str = str(data)
        score = 0
        
        # Size factor
        score += min(len(data_str) / 1000, 0.3)
        
        # Content factors
        important_indicators = ["learn", "important", "critical", "solution", "discovery"]
        for indicator in important_indicators:
            if indicator in data_str.lower():
                score += 0.1
        
        return min(score, 1.0)
    
    def consolidate(self):
        """Consolidate memories (forgetting less important ones)"""
        for bank_name, bank in self.memory_banks.items():
            if isinstance(bank, list):
                # Keep only important/recent memories
                self.memory_banks[bank_name] = sorted(
                    bank,
                    key=lambda x: (x.get("importance", 0), x.get("timestamp", 0)),
                    reverse=True
                )[:1000]  # Keep top 1000
            elif isinstance(bank, dict):
                for category, memories in bank.items():
                    bank[category] = sorted(
                        memories,
                        key=lambda x: (x.get("importance", 0), x.get("timestamp", 0)),
                        reverse=True
                    )[:500]  # Keep top 500 per category
        
        self._save_memories()
        print(f"Memory consolidated: {self.get_stats()['total_memories']} memories remaining")
    
    def _load_memories(self):
        """Load memories from file"""
        try:
            with open(self.storage_file, 'r') as f:
                loaded = json.load(f)
                self.memory_banks.update(loaded)
            print(f"Loaded {self.get_stats()['total_memories']} memories")
        except FileNotFoundError:
            print("No existing memories found, starting fresh")
        except Exception as e:
            print(f"Error loading memories: {e}")
    
    def _save_memories(self):
        """Save memories to file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.memory_banks, f, indent=2)
        except Exception as e:
            print(f"Error saving memories: {e}")
    
    def get_stats(self):
        """Get memory statistics"""
        total_memories = 0
        
        for bank in self.memory_banks.values():
            if isinstance(bank, list):
                total_memories += len(bank)
            elif isinstance(bank, dict):
                for memories in bank.values():
                    total_memories += len(memories)
        
        return {
            "total_memories": total_memories,
            "banks": {k: type(v).__name__ for k, v in self.memory_banks.items()},
            "access_count": self.access_counter,
            "storage_file": self.storage_file
        }

# Quick test
if __name__ == "__main__":
    mm = MemoryManager("test_memory.json")
    
    # Store some memories
    mm.store("short_term", {"task": "Learn AGI", "result": "success"})
    mm.store("semantic", {"fact": "AGI learns from virtual environments"}, {"category": "agi"})
    
    # Retrieve
    memories = mm.retrieve("short_term")
    print(f"Retrieved {len(memories)} memories")
    
    stats = mm.get_stats()
    print(f"Memory stats: {stats}")
