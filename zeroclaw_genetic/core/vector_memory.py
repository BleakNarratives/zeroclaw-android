"""
VectorMemory: Lightweight semantic memory for agents using FAISS
Stores successful code mutations and agent decisions for cross-session retrieval
"""
import json
import os
from typing import List, Dict
from datetime import datetime
try:
    import faiss
    import numpy as np
except ImportError:
    faiss = None
    np = None

class VectorMemory:
    """Lightweight vector memory using FAISS for semantic retrieval"""
    
    def __init__(self, dimension: int = 384, db_path: str = "zeroclaw_memory.faiss"):
        self.dimension = dimension
        self.db_path = db_path
        self.metadata_path = db_path.replace('.faiss', '_metadata.json')
        self.index = None
        self.metadata = []
        self.load_or_create()
    
    def load_or_create(self):
        """Load existing FAISS index or create new one"""
        if faiss is None:
            self.index = []
            self.metadata = []
            return
        
        if os.path.exists(self.db_path) and os.path.exists(self.metadata_path):
            try:
                self.index = faiss.read_index(self.db_path)
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
            except Exception as e:
                print(f"Failed to load index: {e}. Creating new one.")
                self.index = faiss.IndexFlatL2(self.dimension)
                self.metadata = []
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
    
    def store_memory(self, embedding: List[float], agent_id: str, 
                     memory_type: str, content: Dict, success_score: float):
        """Store a memory with embedding, metadata, and success score"""
        if faiss is None:
            self.index.append({
                'embedding': embedding,
                'agent_id': agent_id,
                'memory_type': memory_type,
                'content': content,
                'success_score': success_score,
                'timestamp': datetime.now().isoformat()
            })
        else:
            vector = np.array([embedding], dtype=np.float32)
            self.index.add(vector)
            metadata_entry = {
                'agent_id': agent_id,
                'memory_type': memory_type,
                'content': content,
                'success_score': success_score,
                'timestamp': datetime.now().isoformat(),
                'embedding': embedding
            }
            self.metadata.append(metadata_entry)
        self.save()
    
    def retrieve_memories(self, query_embedding: List[float], agent_id: str = None, 
                         k: int = 5, min_score: float = 0.5) -> List[Dict]:
        """Retrieve top-k similar memories for an agent"""
        if faiss is None:
            results = []
            for i, mem in enumerate(self.index):
                if agent_id and mem['agent_id'] != agent_id:
                    continue
                if mem['success_score'] >= min_score:
                    results.append(mem)
            return results[:k]
        
        query_vector = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(query_vector, min(k * 3, len(self.metadata)))
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                meta = self.metadata[int(idx)]
                if agent_id and meta['agent_id'] != agent_id:
                    continue
                if meta['success_score'] >= min_score:
                    results.append(meta)
                if len(results) >= k:
                    break
        return results
    
    def retrieve_by_type(self, memory_type: str, agent_id: str = None, 
                        k: int = 10) -> List[Dict]:
        """Retrieve all memories of a specific type"""
        if faiss is None:
            results = [m for m in self.index 
                      if m['memory_type'] == memory_type 
                      and (not agent_id or m['agent_id'] == agent_id)]
            return results[:k]
        
        results = [m for m in self.metadata 
                  if m['memory_type'] == memory_type 
                  and (not agent_id or m['agent_id'] == agent_id)]
        return results[:k]
    
    def absorb_memory(self, source_agent_id: str, target_agent_id: str, 
                     memory_type: str = 'mutation') -> Dict:
        """Twoie Logic: Target agent absorbs memories from source agent"""
        source_memories = self.retrieve_by_type(memory_type, agent_id=source_agent_id, k=5)
        absorbed_count = 0
        total_score_increase = 0.0
        
        for mem in source_memories:
            self.store_memory(
                embedding=mem.get('embedding', [0.0] * self.dimension),
                agent_id=target_agent_id,
                memory_type=f"{memory_type}_absorbed",
                content=mem['content'],
                success_score=mem['success_score'] * 0.9
            )
            absorbed_count += 1
            total_score_increase += mem['success_score'] * 0.1
        
        return {
            'source_agent': source_agent_id,
            'target_agent': target_agent_id,
            'memories_absorbed': absorbed_count,
            'fitness_boost': min(total_score_increase, 0.5)
        }
    
    def save(self):
        """Persist index and metadata to disk"""
        if faiss is not None and self.index is not None:
            try:
                faiss.write_index(self.index, self.db_path)
                with open(self.metadata_path, 'w') as f:
                    json.dump(self.metadata, f, indent=2)
            except Exception as e:
                print(f"Failed to save memory: {e}")
    
    def clear(self):
        """Clear all memories"""
        if faiss is not None:
            self.index = faiss.IndexFlatL2(self.dimension)
        else:
            self.index = []
        self.metadata = []
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.metadata_path):
            os.remove(self.metadata_path)
    
    def get_agent_lineage(self, agent_id: str) -> Dict:
        """Get full memory lineage for an agent"""
        agent_memories = [m for m in self.metadata if m['agent_id'] == agent_id]
        return {
            'agent_id': agent_id,
            'total_memories': len(agent_memories),
            'memory_types': list(set(m['memory_type'] for m in agent_memories)),
            'avg_success_score': sum(m['success_score'] for m in agent_memories) / len(agent_memories) if agent_memories else 0.0,
            'memories': agent_memories
        }