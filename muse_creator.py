"""
Muse Summoner System - Muse Creation Module

This module enables users to create new muse personas with custom attributes.
It provides functionality to define and add new muses to the system.
"""

from muse_profiles import MuseProfile, add_muse, get_all_muses

class MuseCreator:
    def __init__(self):
        self.creation_steps = [
            "name",
            "trigger_phrase",
            "voice_tone",
            "purpose",
            "tasks_supported",
            "catchphrases",
            "signature_question",
            "sample_tasks",
            "ritual_system"
        ]
        self.current_step = 0
        self.new_muse_data = {}
        self.in_creation_process = False
    
    def start_creation_process(self):
        """Start the muse creation process."""
        self.in_creation_process = True
        self.current_step = 0
        self.new_muse_data = {}
        return self._get_current_prompt()
    
    def process_input(self, user_input):
        """
        Process user input for the current creation step.
        Returns the next prompt or a completion message.
        """
        if not self.in_creation_process:
            return "No muse creation process is currently active."
        
        # Store the user input for the current step
        current_field = self.creation_steps[self.current_step]
        
        # Handle list-type fields
        if current_field in ["tasks_supported", "catchphrases", "sample_tasks"]:
            # Split by newlines or semicolons and clean up
            items = [item.strip() for item in user_input.replace("\n", ";").split(";") if item.strip()]
            self.new_muse_data[current_field] = items
        else:
            self.new_muse_data[current_field] = user_input.strip()
        
        # Move to the next step
        self.current_step += 1
        
        # Check if we've completed all steps
        if self.current_step >= len(self.creation_steps):
            return self._finalize_muse_creation()
        
        # Return the prompt for the next step
        return self._get_current_prompt()
    
    def _get_current_prompt(self):
        """Get the prompt for the current creation step."""
        current_field = self.creation_steps[self.current_step]
        
        prompts = {
            "name": "What name would you like to give your new muse?",
            "trigger_phrase": "What trigger phrase should summon this muse? (e.g., 'Come into fashion' for Salvatore)",
            "voice_tone": "Describe the voice and tone of this muse. How do they speak? What style do they use?",
            "purpose": "What is the primary purpose of this muse? What emotional or creative needs will they address?",
            "tasks_supported": "List the tasks this muse can help with (separate multiple tasks with semicolons or new lines):",
            "catchphrases": "What are some signature catchphrases this muse might use? (separate with semicolons or new lines)",
            "signature_question": "What is a signature question this muse might ask to provoke thought?",
            "sample_tasks": "Provide some example tasks users might ask this muse to help with (include the trigger phrase in examples, separate with semicolons or new lines):",
            "ritual_system": "Does this muse have a ritual system or special approach? (optional, leave blank if none)"
        }
        
        return prompts.get(current_field, "Please provide information for the next step:")
    
    def _finalize_muse_creation(self):
        """Finalize the muse creation process and add the new muse to the database."""
        # Create capabilities dictionary (empty for now, can be expanded later)
        capabilities = {}
        
        # Create the new muse profile
        new_muse = MuseProfile(
            name=self.new_muse_data["name"],
            trigger_phrase=self.new_muse_data["trigger_phrase"],
            voice_tone=self.new_muse_data["voice_tone"],
            purpose=self.new_muse_data["purpose"],
            tasks_supported=self.new_muse_data["tasks_supported"],
            catchphrases=self.new_muse_data["catchphrases"],
            signature_question=self.new_muse_data["signature_question"],
            sample_tasks=self.new_muse_data["sample_tasks"],
            ritual_system=self.new_muse_data.get("ritual_system") if self.new_muse_data.get("ritual_system") else None,
            capabilities=capabilities
        )
        
        # Add the new muse to the database
        muse_id = add_muse(new_muse)
        
        # Reset the creation process
        self.in_creation_process = False
        self.current_step = 0
        self.new_muse_data = {}
        
        # Return a success message
        return f"Muse '{new_muse.name}' has been successfully created! You can now summon them with the trigger phrase: '{new_muse.trigger_phrase}'"
    
    def is_creating_muse(self):
        """Check if a muse creation process is currently active."""
        return self.in_creation_process
    
    def cancel_creation(self):
        """Cancel the current muse creation process."""
        if not self.in_creation_process:
            return "No muse creation process is currently active."
        
        self.in_creation_process = False
        self.current_step = 0
        self.new_muse_data = {}
        
        return "Muse creation process has been cancelled."


# Create a singleton instance for global use
muse_creator = MuseCreator()

def start_muse_creation():
    """Start the process of creating a new muse."""
    return muse_creator.start_creation_process()

def process_creation_input(user_input):
    """Process user input for the current muse creation step."""
    return muse_creator.process_input(user_input)

def is_creating_muse():
    """Check if a muse creation process is currently active."""
    return muse_creator.is_creating_muse()

def cancel_muse_creation():
    """Cancel the current muse creation process."""
    return muse_creator.cancel_creation()

def get_muse_list_formatted():
    """Get a formatted list of all available muses."""
    muses = get_all_muses()
    if not muses:
        return "No muses are currently available."
    
    formatted_list = "Available Muses:\n\n"
    for i, muse in enumerate(muses, 1):
        formatted_list += f"{i}. {muse.name}\n"
        formatted_list += f"   Trigger: \"{muse.trigger_phrase}\"\n"
        formatted_list += f"   Purpose: {muse.purpose}\n\n"
    
    return formatted_list
