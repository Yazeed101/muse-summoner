"""
Muse Summoner System - Configuration Module

This module provides configuration options for the Muse Summoner system.
It allows for easy customization of system behavior and features.
"""

import os
import json

# Default configuration
DEFAULT_CONFIG = {
    # General settings
    "system_name": "Muse Summoner",
    "debug_mode": False,
    
    # Memory settings
    "memory_enabled": True,
    "max_memory_entries": 50,
    "memory_relevance_threshold": 0.1,
    
    # Web application settings
    "web_host": "0.0.0.0",
    "web_port": 5000,
    "session_timeout": 3600,  # 1 hour
    
    # Muse settings
    "default_muse": "salvatore_inverso",
    "muse_profiles_dir": "muse_profiles",
    "memory_storage_dir": "memory",
    
    # Customization settings
    "allow_muse_creation": True,
    "allow_memory_clearing": True,
    "allow_system_commands": True,
    
    # Advanced settings
    "response_generation": {
        "include_memory_references": True,
        "signature_question_probability": 0.3,
        "max_response_length": 2000
    }
}

class Config:
    def __init__(self, config_file="config.json"):
        """Initialize the configuration with default values or from a config file."""
        self.config_file = config_file
        self.config = DEFAULT_CONFIG.copy()
        
        # Load configuration from file if it exists
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self._update_config(loaded_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading configuration: {e}")
    
    def _update_config(self, new_config):
        """Update configuration with new values, preserving nested structure."""
        for key, value in new_config.items():
            if key in self.config and isinstance(value, dict) and isinstance(self.config[key], dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def get(self, key, default=None):
        """Get a configuration value by key."""
        # Support nested keys with dot notation (e.g., "response_generation.max_response_length")
        if '.' in key:
            parts = key.split('.')
            value = self.config
            for part in parts:
                if part not in value:
                    return default
                value = value[part]
            return value
        
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value."""
        # Support nested keys with dot notation
        if '.' in key:
            parts = key.split('.')
            config = self.config
            for part in parts[:-1]:
                if part not in config:
                    config[part] = {}
                config = config[part]
            config[parts[-1]] = value
        else:
            self.config[key] = value
    
    def save(self):
        """Save the current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self.config = DEFAULT_CONFIG.copy()
        return self.save()
    
    def get_all(self):
        """Get the entire configuration dictionary."""
        return self.config.copy()


# Create a singleton instance for global use
config = Config()

def get_config(key=None, default=None):
    """
    Global function to get configuration values.
    If key is None, returns the entire configuration.
    """
    if key is None:
        return config.get_all()
    return config.get(key, default)

def set_config(key, value):
    """Global function to set a configuration value."""
    return config.set(key, value)

def save_config():
    """Global function to save the current configuration."""
    return config.save()

def reset_config():
    """Global function to reset configuration to defaults."""
    return config.reset_to_defaults()
