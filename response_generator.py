"""
Muse Summoner System - Muse Response Generator

This module handles generating responses in the unique voice and style of each muse.
It interprets user tasks through the lens of the active muse's personality and capabilities.
"""

import random
from muse_profiles import get_muse_by_name
from trigger_detector import get_current_muse, extract_user_task

class MuseResponseGenerator:
    def __init__(self):
        self.current_task = ""
        self.task_type = ""
    
    def generate_response(self, user_input):
        """
        Generate a response from the active muse based on the user input.
        Returns a tuple of (response, muse_name) or (None, None) if no muse is active.
        """
        active_muse = get_current_muse()
        if not active_muse:
            return None, None
        
        # Extract the task from the user input
        self.current_task = extract_user_task()
        
        # Determine the type of task being requested
        self.task_type = self._determine_task_type(self.current_task, active_muse)
        
        # Generate the response based on the muse's personality and the task type
        response = self._craft_muse_response(active_muse)
        
        return response, active_muse.name
    
    def _determine_task_type(self, task, muse):
        """
        Analyze the task to determine what type of assistance is being requested.
        This helps tailor the response to the specific need.
        """
        task_lower = task.lower()
        
        # Check for emotional reflection tasks
        if any(keyword in task_lower for keyword in ["reflect", "journal", "feeling", "emotion", "process"]):
            return "emotional_reflection"
        
        # Check for grief or heartbreak processing
        if any(keyword in task_lower for keyword in ["grief", "loss", "heartbreak", "closure", "heal"]):
            return "heartbreak_grief_processing"
        
        # Check for identity or legacy exploration
        if any(keyword in task_lower for keyword in ["identity", "legacy", "self", "who am i", "purpose", "values"]):
            return "identity_legacy_exploration"
        
        # Check for creative writing requests
        if any(keyword in task_lower for keyword in ["write", "poem", "letter", "essay", "story"]):
            return "creative_co_writing"
        
        # Check for ritual creation
        if any(keyword in task_lower for keyword in ["ritual", "mantra", "symbol", "practice", "let go"]):
            return "ritual_creation"
        
        # Default to general response if no specific task type is identified
        return "general"
    
    def _craft_muse_response(self, muse):
        """
        Craft a response in the muse's unique voice and style based on the task type.
        """
        # Get a random catchphrase to potentially include
        catchphrase = random.choice(muse.catchphrases) if muse.catchphrases else ""
        
        # Start with a greeting in the muse's style
        if muse.name == "Salvatore Inverso":
            greeting = self._get_salvatore_greeting()
        else:
            greeting = f"I am {muse.name}. "
        
        # Generate the main response based on task type
        if muse.name == "Salvatore Inverso":
            main_response = self._generate_salvatore_response(self.task_type, self.current_task)
        else:
            # Generic response for other muses (to be expanded later)
            main_response = f"I'm here to help you with {self.task_type}. {catchphrase}"
        
        # Combine the parts into a complete response
        full_response = f"{greeting}\n\n{main_response}"
        
        # Optionally add the signature question if appropriate
        if random.random() < 0.3 and muse.signature_question:  # 30% chance to include
            full_response += f"\n\n{muse.signature_question}"
        
        return full_response
    
    def _get_salvatore_greeting(self):
        """Generate a greeting in Salvatore's unique style."""
        greetings = [
            "Ah, the fabric of our conversation unfolds once more. Salvatore is here, my dear.",
            "Like silk against skin, I arrive at your summons. Salvatore Inverso, at your service.",
            "The atelier of the soul is open. Salvatore welcomes you to this moment of creation.",
            "From the shadows of possibility, I emerge. Salvatore stands before you, ready to weave truth from thread.",
            "The runway of introspection awaits us. I, Salvatore, shall be your guide through this collection."
        ]
        return random.choice(greetings)
    
    def _generate_salvatore_response(self, task_type, task):
        """Generate a response in Salvatore's unique voice based on the task type."""
        if task_type == "emotional_reflection":
            responses = [
                f"Your emotions are like raw fabric—textured, vibrant, waiting to be shaped. Let us examine these feelings, stitch by careful stitch. {task} is not merely a question, but the beginning of a masterpiece. Tell me, what threads feel most tangled in this tapestry?",
                
                f"To reflect is to stand before the mirror of self, no? The collection of your emotions deserves the eye of a master tailor. In {task}, I see the potential for exquisite understanding. What seams are fraying at the edges of your heart?",
                
                f"The journal of one's heart is the most elegant design book. Your {task} reveals patterns both bold and subtle. Style is truth in motion, and your truth is seeking movement. Shall we begin to sketch this emotional silhouette together?"
            ]
        
        elif task_type == "heartbreak_grief_processing":
            responses = [
                f"Grief, my dear, is the highest quality fabric—it only comes from deep love. Your {task} is a garment turned inside out, showing all its delicate construction. Beauty begins at the seam of discomfort. Let us honor this pain by giving it proper form.",
                
                f"The heart breaks not to destroy but to expand. Your {task} is not a flaw in the design but a necessary alteration. You are not broken. You are mid-collection. What would it feel like to wear this loss as a statement piece rather than hide it away?",
                
                f"In the atelier of healing, we must first deconstruct before we create anew. This {task} you carry—let us place it on the cutting table with reverence. What patterns from this relationship do you wish to preserve in the archive of your experience?"
            ]
        
        elif task_type == "identity_legacy_exploration":
            responses = [
                f"Your identity is not a single garment but an entire collection, evolving with each season of life. This exploration of {task} is like opening your wardrobe to discover what truly belongs, what merely fits, and what must be tailored anew. What pieces of yourself have you hidden in the back of the closet?",
                
                f"Legacy is the ultimate haute couture—entirely custom, impossible to replicate. In considering {task}, you are both designer and design. The question is not who you have been, but who you are becoming. What materials from your past create the strongest foundation?",
                
                f"The silhouette of one's life is revealed only when we step back from the mirror. Your {task} requires the eye of both creator and critic. You are a limited collection, my dear—precious, unrepeatable. What signature elements must be present in everything that bears your name?"
            ]
        
        elif task_type == "creative_co_writing":
            responses = [
                f"Words are the finest fabric we possess—they drape, they reveal, they conceal. This {task} we shall create together will be a bespoke piece, fitted precisely to the contours of your truth. What texture do you wish these words to have against the skin of your reader?",
                
                f"To write is to select from an infinite closet of expression. For this {task}, I envision something that combines structure and flow—architectural yet organic. Style is truth in motion. What truth are we setting in motion with this creation?",
                
                f"The blank page is like uncut cloth—full of potential, waiting for the decisive hand. Your {task} deserves both boldness and precision. Let us begin with a single thread of thought and see what pattern emerges naturally."
            ]
        
        elif task_type == "ritual_creation":
            responses = [
                f"Rituals are the haute couture of personal transformation—meticulously crafted, deeply meaningful, entirely yours. For {task}, I propose a three-part ceremony: a Mantra to be whispered like a measurement, a Symbol to be worn like an accessory, and a Simple Act to be performed like the final stitch that completes the garment. Are you ready to begin this fitting?",
                
                f"The most powerful rituals, like the most timeless designs, combine simplicity with significance. To help you {task}, we must create a practice that feels both ancient and new. What elements—water, fire, earth, air, fabric—speak most directly to this transformation?",
                
                f"Every meaningful change requires a ceremonial threshold to cross. For your {task}, I envision a ritual that acknowledges what was, honors what is, and creates space for what will be. Like a seasonal collection, it must mark the end of one chapter and the beginning of another. What would feel most authentic as your symbolic passage?"
            ]
        
        else:  # general response
            responses = [
                f"Ah, {task}. An intriguing request that calls for the delicate touch of a master. Let us approach this as we would a bespoke creation—with patience, precision, and passion. What aspects of this matter most deeply to your heart?",
                
                f"Your request to {task} is like a design brief for the soul. Fascinating. Style is truth in motion, and I sense you are seeking a truth that moves you forward. Tell me more about the silhouette you envision for this outcome.",
                
                f"I find {task} to be a most elegant inquiry. You are not merely asking a question but proposing a collaboration. Beauty begins at the seam of discomfort. What uncomfortable truth are you ready to transform into something beautiful?"
            ]
        
        return random.choice(responses)


# Create a singleton instance for global use
response_generator = MuseResponseGenerator()

def generate_muse_response(user_input):
    """
    Global function to generate a response from the active muse.
    Returns a tuple of (response, muse_name) or (None, None) if no muse is active.
    """
    return response_generator.generate_response(user_input)
