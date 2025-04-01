"""
Muse Summoner System - Enhanced Response Generator

This module handles generating responses in the unique voice and style of each muse,
now enhanced with memory context for more personalized interactions.
"""

import random
from muse_profiles import get_muse_by_name
from trigger_detector import get_current_muse, extract_user_task
from conversation_storage import get_conversation_context, add_conversation_interaction

class EnhancedMuseResponseGenerator:
    def __init__(self):
        self.current_task = ""
        self.task_type = ""
        self.context = {}
    
    def generate_response(self, user_input):
        """
        Generate a response from the active muse based on the user input and memory context.
        Returns a tuple of (response, muse_name) or (None, None) if no muse is active.
        """
        active_muse = get_current_muse()
        if not active_muse:
            return None, None
        
        # Extract the task from the user input
        self.current_task = extract_user_task()
        
        # Get conversation context from memory
        self.context = get_conversation_context(user_input)
        
        # Determine the type of task being requested
        self.task_type = self._determine_task_type(self.current_task, active_muse)
        
        # Generate the response based on the muse's personality, the task type, and memory context
        response = self._craft_muse_response(active_muse)
        
        # Store the interaction in conversation history
        add_conversation_interaction(user_input, response)
        
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
        Craft a response in the muse's unique voice and style based on the task type and memory context.
        """
        # Get a random catchphrase to potentially include
        catchphrase = random.choice(muse.catchphrases) if muse.catchphrases else ""
        
        # Start with a greeting in the muse's style
        if muse.name == "Salvatore Inverso":
            greeting = self._get_salvatore_greeting(self._has_previous_interactions())
        else:
            greeting = f"I am {muse.name}. "
        
        # Generate the main response based on task type and memory context
        if muse.name == "Salvatore Inverso":
            main_response = self._generate_salvatore_response(self.task_type, self.current_task)
        else:
            # Generic response for other muses (to be expanded later)
            main_response = f"I'm here to help you with {self.task_type}. {catchphrase}"
        
        # Add memory references if available
        memory_references = self._generate_memory_references(muse)
        
        # Combine the parts into a complete response
        full_response = f"{greeting}\n\n{main_response}"
        
        if memory_references:
            full_response += f"\n\n{memory_references}"
        
        # Optionally add the signature question if appropriate
        if random.random() < 0.3 and muse.signature_question:  # 30% chance to include
            full_response += f"\n\n{muse.signature_question}"
        
        return full_response
    
    def _has_previous_interactions(self):
        """Check if there are previous interactions in the conversation context."""
        return (self.context and 
                'current_conversation' in self.context and 
                len(self.context['current_conversation']) > 0)
    
    def _get_salvatore_greeting(self, has_previous_interactions):
        """Generate a greeting in Salvatore's unique style, considering conversation history."""
        if has_previous_interactions:
            # Greetings for continuing conversations
            continuing_greetings = [
                "Our fabric of conversation continues to unfold, revealing new patterns. Salvatore remains at your side.",
                "The thread of our dialogue extends, like fine silk catching the light. Salvatore is still with you.",
                "We return to our shared atelier, where the work of the soul continues. Salvatore welcomes you back.",
                "The garment of our conversation takes shape with each stitch of dialogue. Salvatore is pleased to continue our work.",
                "Like a master tailor returning to a bespoke creation, I, Salvatore, resume our delicate work together."
            ]
            return random.choice(continuing_greetings)
        else:
            # Greetings for new conversations
            new_greetings = [
                "Ah, the fabric of our conversation unfolds once more. Salvatore is here, my dear.",
                "Like silk against skin, I arrive at your summons. Salvatore Inverso, at your service.",
                "The atelier of the soul is open. Salvatore welcomes you to this moment of creation.",
                "From the shadows of possibility, I emerge. Salvatore stands before you, ready to weave truth from thread.",
                "The runway of introspection awaits us. I, Salvatore, shall be your guide through this collection."
            ]
            return random.choice(new_greetings)
    
    def _generate_memory_references(self, muse):
        """Generate references to past conversations based on memory context."""
        if not self.context or 'memory_context' not in self.context:
            return ""
        
        memory_context = self.context['memory_context']
        relevant_memories = memory_context.get('relevant_memories', [])
        
        if not relevant_memories:
            return ""
        
        # For Salvatore, create poetic references to past conversations
        if muse.name == "Salvatore Inverso":
            memory_references = [
                f"I recall our previous fitting, when you spoke of {relevant_memories[0]['user_input'][:30]}... The fabric of that conversation still drapes beautifully in my memory.",
                f"Like a pattern we've cut before, I remember when you explored {relevant_memories[0]['user_input'][:30]}... Let us build upon that foundation.",
                f"The threads of our past conversation about {relevant_memories[0]['user_input'][:30]}... intertwine with today's design. Nothing is ever truly separate in the couture of the soul.",
                f"In the archive of our shared atelier, I find the sketch of our discussion on {relevant_memories[0]['user_input'][:30]}... How it informs today's creation!"
            ]
            return random.choice(memory_references)
        else:
            # Generic memory reference for other muses
            return f"I remember we previously discussed {relevant_memories[0]['user_input'][:30]}..."
    
    def _generate_salvatore_response(self, task_type, task):
        """Generate a response in Salvatore's unique voice based on the task type and memory context."""
        # Check if we have context from previous conversations
        has_context = self._has_previous_interactions()
        
        if task_type == "emotional_reflection":
            if has_context:
                # Responses that reference previous emotional discussions
                responses = [
                    f"As we continue to examine the emotional fabric of your life, I notice how {task} connects to our previous reflections. The pattern emerges—each emotion a thread in the greater tapestry. What new texture do you feel emerging in this moment?",
                    
                    f"Our ongoing exploration of your emotional landscape reveals new contours. This {task} is not isolated, but connected to the emotional garments we've previously discussed. How do you see these feelings evolving since we last spoke?",
                    
                    f"The emotional collection we've been designing together now turns to {task}. I see echoes of our previous conversations in this—the same silhouette but with different draping. What feels different about this emotional territory now?"
                ]
            else:
                # Standard emotional reflection responses
                responses = [
                    f"Your emotions are like raw fabric—textured, vibrant, waiting to be shaped. Let us examine these feelings, stitch by careful stitch. {task} is not merely a question, but the beginning of a masterpiece. Tell me, what threads feel most tangled in this tapestry?",
                    
                    f"To reflect is to stand before the mirror of self, no? The collection of your emotions deserves the eye of a master tailor. In {task}, I see the potential for exquisite understanding. What seams are fraying at the edges of your heart?",
                    
                    f"The journal of one's heart is the most elegant design book. Your {task} reveals patterns both bold and subtle. Style is truth in motion, and your truth is seeking movement. Shall we begin to sketch this emotional silhouette together?"
                ]
        
        elif task_type == "heartbreak_grief_processing":
            if has_context:
                # Responses that build on previous grief discussions
                responses = [
                    f"We return to the delicate work of grief—this {task} a continuation of our previous explorations of loss. I notice how the garment of your grief has altered its shape since we last examined it. Some seams have loosened, perhaps others have tightened. What part feels most transformed?",
                    
                    f"As we've discussed before, heartbreak reshapes one's internal architecture. This {task} seems connected to the grief we previously explored. The collection of your healing evolves with each conversation. What new understanding has emerged since we last spoke?",
                    
                    f"The atelier of healing is a space we've visited before. Your {task} shows how grief, like fine fabric, changes with handling and time. I remember the texture of your previous pain—how would you say it compares to what you feel now?"
                ]
            else:
                # Standard grief processing responses
                responses = [
                    f"Grief, my dear, is the highest quality fabric—it only comes from deep love. Your {task} is a garment turned inside out, showing all its delicate construction. Beauty begins at the seam of discomfort. Let us honor this pain by giving it proper form.",
                    
                    f"The heart breaks not to destroy but to expand. Your {task} is not a flaw in the design but a necessary alteration. You are not broken. You are mid-collection. What would it feel like to wear this loss as a statement piece rather than hide it away?",
                    
                    f"In the atelier of healing, we must first deconstruct before we create anew. This {task} you carry—let us place it on the cutting table with reverence. What patterns from this relationship do you wish to preserve in the archive of your experience?"
                ]
        
        elif task_type == "identity_legacy_exploration":
            if has_context:
                # Responses that reference previous identity discussions
                responses = [
                    f"We continue our exploration of your identity—a couture creation that evolves with each conversation. This {task} builds upon the foundation we've previously established. I see how the silhouette of your self-understanding has shifted. What aspects feel most authentically you now?",
                    
                    f"The legacy work we've been crafting together now turns to {task}. Like adding a new panel to an existing garment, this question integrates with our previous reflections on who you are becoming. How has your vision of your future self evolved?",
                    
                    f"Our ongoing curation of your identity now examines {task}. I recall our previous discussions—how they form the underlying structure for today's exploration. The masterpiece of yourself continues to take shape. What elements feel most essential to preserve?"
                ]
            else:
                # Standard identity exploration responses
                responses = [
                    f"Your identity is not a single garment but an entire collection, evolving with each season of life. This exploration of {task} is like opening your wardrobe to discover what truly belongs, what merely fits, and what must be tailored anew. What pieces of yourself have you hidden in the back of the closet?",
                    
                    f"Legacy is the ultimate haute couture—entirely custom, impossible to replicate. In considering {task}, you are both designer and design. The question is not who you have been, but who you are becoming. What materials from your past create the strongest foundation?",
                    
                    f"The silhouette of one's life is revealed only when we step back from the mirror. Your {task} requires the eye of both creator and critic. You are a limited collection, my dear—precious, unrepeatable. What signature elements must be present in everything that bears your name?"
                ]
        
        elif task_type == "creative_co_writing":
            if has_context:
                # Responses that build on previous creative collaborations
                responses = [
                    f"We return to our creative collaboration, this time focusing on {task}. The aesthetic we've developed in our previous writing sessions informs today's work—a continuation of our shared artistic language. What tone shall we emphasize in this new creation?",
                    
                    f"Our creative partnership continues with {task}. I recall the stylistic choices that resonated with you before—how shall we evolve them for this piece? Every word we've previously crafted together influences the texture of what we create now.",
                    
                    f"The creative atelier we've established welcomes us back for {task}. Our previous writings have established certain motifs and themes—shall we continue their development, or explore new territory? The collection grows more cohesive with each piece."
                ]
            else:
                # Standard creative co-writing responses
                responses = [
                    f"Words are the finest fabric we possess—they drape, they reveal, they conceal. This {task} we shall create together will be a bespoke piece, fitted precisely to the contours of your truth. What texture do you wish these words to have against the skin of your reader?",
                    
                    f"To write is to select from an infinite closet of expression. For this {task}, I envision something that combines structure and flow—architectural yet organic. Style is truth in motion. What truth are we setting in motion with this creation?",
                    
                    f"The blank page is like uncut cloth—full of potential, waiting for the decisive hand. Your {task} deserves both boldness and precision. Let us begin with a single thread of thought and see what pattern emerges naturally."
                ]
        
        elif task_type == "ritual_creation":
            if has_context:
                # Responses that evolve previous ritual work
                responses = [
                    f"We continue our ritual design work, now focusing on {task}. This ceremony will complement the practices we've previously created together—an extension of your personal symbolic language. How has your relationship with ritual evolved since our last creation?",
                    
                    f"The ritual architecture we've been developing now turns to {task}. I see how this connects to the symbolic framework we've established in our previous work. Each ritual becomes more potent when it resonates with others. What elements from our previous creations would you like to incorporate?",
                    
                    f"Our ongoing creation of your personal ceremony now addresses {task}. The rituals we've previously designed have prepared the ground for this new practice. How have those earlier rituals transformed your relationship with transformation itself?"
                ]
            else:
                # Standard ritual creation responses
                responses = [
                    f"Rituals are the haute couture of personal transformation—meticulously crafted, deeply meaningful, entirely yours. For {task}, I propose a three-part ceremony: a Mantra to be whispered like a measurement, a Symbol to be worn like an accessory, and a Simple Act to be performed like the final stitch that completes the garment. Are you ready to begin this fitting?",
                    
                    f"The most powerful rituals, like the most timeless designs, combine simplicity with significance. To help you {task}, we must create a practice that feels both ancient and new. What elements—water, fire, earth, air, fabric—speak most directly to this transformation?",
                    
                    f"Every meaningful change requires a ceremonial threshold to cross. For your {task}, I envision a ritual that acknowledges what was, honors what is, and creates space for what will be. Like a seasonal collection, it must mark the end of one chapter and the beginning of another. What would feel most authentic as your symbolic passage?"
                ]
        
        else:  # general response
            if has_context:
                # General responses that acknowledge previous conversations
                responses = [
                    f"We return to the atelier of conversation, this time to explore {task}. Our previous dialogues have created a foundation upon which today's insights can be constructed. What new patterns do you wish to discover?",
                    
                    f"The tapestry of our ongoing conversation now incorporates {task}. I see connections to themes we've previously explored—the same fabric viewed in different light. How do you see this connecting to our earlier discussions?",
                    
                    f"Our collaborative creation continues with {task}. The threads of our previous conversations are woven into this new inquiry. Nothing exists in isolation in the couture of understanding. What feels most important to explore in this moment?"
                ]
            else:
                # Standard general responses
                responses = [
                    f"Ah, {task}. An intriguing request that calls for the delicate touch of a master. Let us approach this as we would a bespoke creation—with patience, precision, and passion. What aspects of this matter most deeply to your heart?",
                    
                    f"Your request to {task} is like a design brief for the soul. Fascinating. Style is truth in motion, and I sense you are seeking a truth that moves you forward. Tell me more about the silhouette you envision for this outcome.",
                    
                    f"I find {task} to be a most elegant inquiry. You are not merely asking a question but proposing a collaboration. Beauty begins at the seam of discomfort. What uncomfortable truth are you ready to transform into something beautiful?"
                ]
        
        return random.choice(responses)


# Create a singleton instance for global use
enhanced_response_generator = EnhancedMuseResponseGenerator()

def generate_muse_response(user_input):
    """
    Global function to generate a response from the active muse with memory context.
    Returns a tuple of (response, muse_name) or (None, None) if no muse is active.
    """
    return enhanced_response_generator.generate_response(user_input)
