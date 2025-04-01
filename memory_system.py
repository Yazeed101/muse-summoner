"""
Muse Summoner System - Memory Module

This module implements persistent memory for muses to remember past conversations.
It stores conversation history and provides context for generating more personalized responses.
"""

import os
import json
import datetime
from collections import deque

class MuseMemory:
    def __init__(self, storage_dir="/tmp/memory_storage"):
        """Initialize the muse memory system with a storage directory."""
        self.storage_dir = storage_dir
        self.memory_cache = {}
        self.max_memory_entries = 50  # Maximum number of conversation entries to keep per muse
        
        # Create the storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def add_memory(self, muse_name, user_input, muse_response):
        """
        Add a new memory entry for a specific muse.
        
        Args:
            muse_name (str): The name of the muse
            user_input (str): The user's input
            muse_response (str): The muse's response
        """
        # Create a memory entry
        timestamp = datetime.datetime.now().isoformat()
        memory_entry = {
            "timestamp": timestamp,
            "user_input": user_input,
            "muse_response": muse_response
        }
        
        # Get the muse's memory file path
        muse_id = muse_name.lower().replace(" ", "_")
        memory_file = os.path.join(self.storage_dir, f"{muse_id}_memory.json")
        
        # Load existing memories or create a new memory list
        memories = self._load_memories(muse_name)
        
        # Add the new memory entry
        memories.append(memory_entry)
        
        # Keep only the most recent entries up to max_memory_entries
        if len(memories) > self.max_memory_entries:
            memories = memories[-self.max_memory_entries:]
        
        # Save the updated memories
        self._save_memories(muse_name, memories)
        
        # Update the memory cache
        self.memory_cache[muse_id] = memories
    
    def get_memories(self, muse_name, count=5):
        """
        Get the most recent memories for a specific muse.
        
        Args:
            muse_name (str): The name of the muse
            count (int): The number of recent memories to retrieve
            
        Returns:
            list: A list of memory entries
        """
        memories = self._load_memories(muse_name)
        
        # Return the most recent memories up to the specified count
        return memories[-count:] if memories else []
    
    def get_memory_summary(self, muse_name):
        """
        Generate a summary of the muse's memories for context.
        
        Args:
            muse_name (str): The name of the muse
            
        Returns:
            str: A summary of the muse's memories
        """
        memories = self.get_memories(muse_name, count=5)
        
        if not memories:
            return "No previous conversations found."
        
        summary = "Recent conversation history:\n\n"
        
        for i, memory in enumerate(memories, 1):
            timestamp = datetime.datetime.fromisoformat(memory["timestamp"])
            formatted_time = timestamp.strftime("%Y-%m-%d %H:%M")
            
            summary += f"Conversation {i} ({formatted_time}):\n"
            summary += f"User: {memory['user_input']}\n"
            summary += f"Muse: {memory['muse_response'][:100]}...\n\n"
        
        return summary
    
    def get_relevant_memories(self, muse_name, current_input, max_results=3):
        """
        Find memories that are relevant to the current user input.
        
        Args:
            muse_name (str): The name of the muse
            current_input (str): The current user input
            max_results (int): Maximum number of relevant memories to return
            
        Returns:
            list: A list of relevant memory entries
        """
        memories = self._load_memories(muse_name)
        
        if not memories:
            return []
        
        # Simple relevance scoring based on word overlap
        current_words = set(current_input.lower().split())
        scored_memories = []
        
        for memory in memories:
            memory_words = set(memory["user_input"].lower().split())
            # Calculate Jaccard similarity (intersection over union)
            intersection = len(current_words.intersection(memory_words))
            union = len(current_words.union(memory_words))
            score = intersection / union if union > 0 else 0
            
            scored_memories.append((score, memory))
        
        # Sort by relevance score in descending order
        scored_memories.sort(reverse=True, key=lambda x: x[0])
        
        # Return the most relevant memories up to max_results
        return [memory for score, memory in scored_memories[:max_results] if score > 0.1]
    
    def clear_memories(self, muse_name):
        """
        Clear all memories for a specific muse.
        
        Args:
            muse_name (str): The name of the muse
        """
        muse_id = muse_name.lower().replace(" ", "_")
        memory_file = os.path.join(self.storage_dir, f"{muse_id}_memory.json")
        
        # Clear the memory file
        self._save_memories(muse_name, [])
        
        # Clear the memory cache
        if muse_id in self.memory_cache:
            del self.memory_cache[muse_id]
    
    def _load_memories(self, muse_name):
        """
        Load memories for a specific muse from the storage file.
        
        Args:
            muse_name (str): The name of the muse
            
        Returns:
            list: A list of memory entries
        """
        muse_id = muse_name.lower().replace(" ", "_")
        
        # Check if memories are already in cache
        if muse_id in self.memory_cache:
            return self.memory_cache[muse_id]
        
        memory_file = os.path.join(self.storage_dir, f"{muse_id}_memory.json")
        
        # If the memory file exists, load it
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r') as f:
                    memories = json.load(f)
                    self.memory_cache[muse_id] = memories
                    return memories
            except (json.JSONDecodeError, IOError):
                # If there's an error loading the file, return an empty list
                return []
        
        # If the file doesn't exist, return an empty list
        return []
    
    def _save_memories(self, muse_name, memories):
        """
        Save memories for a specific muse to the storage file.
        
        Args:
            muse_name (str): The name of the muse
            memories (list): A list of memory entries
        """
        muse_id = muse_name.lower().replace(" ", "_")
        memory_file = os.path.join(self.storage_dir, f"{muse_id}_memory.json")
        
        try:
            with open(memory_file, 'w') as f:
                json.dump(memories, f, indent=2)
        except IOError as e:
            print(f"Error saving memories for {muse_name}: {e}")


# Create a singleton instance for global use
muse_memory = MuseMemory()

def add_conversation_memory(muse_name, user_input, muse_response):
    """
    Global function to add a conversation memory for a muse.
    
    Args:
        muse_name (str): The name of the muse
        user_input (str): The user's input
        muse_response (str): The muse's response
    """
    muse_memory.add_memory(muse_name, user_input, muse_response)

def get_conversation_history(muse_name, count=5):
    """
    Global function to get recent conversation history for a muse.
    
    Args:
        muse_name (str): The name of the muse
        count (int): The number of recent conversations to retrieve
        
    Returns:
        list: A list of conversation entries
    """
    return muse_memory.get_memories(muse_name, count)

def get_memory_context(muse_name, current_input):
    """
    Global function to get memory context for generating a response.
    
    Args:
        muse_name (str): The name of the muse
        current_input (str): The current user input
        
    Returns:
        dict: A dictionary containing memory context
    """
    relevant_memories = muse_memory.get_relevant_memories(muse_name, current_input)
    recent_memories = muse_memory.get_memories(muse_name, count=2)
    
    return {
        "relevant_memories": relevant_memories,
        "recent_memories": recent_memories
    }

def clear_muse_memory(muse_name):
    """
    Global function to clear all memories for a muse.
    
    Args:
        muse_name (str): The name of the muse
    """
    muse_memory.clear_memories(muse_name)
