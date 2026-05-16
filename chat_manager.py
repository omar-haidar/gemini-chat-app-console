import google.generativeai as genai
from typing import List, Dict, Optional
from datetime import datetime
import json
import os

class ChatManager:
    def __init__(self, api_key: str, model_name: str = "gemini-3-flash-preview"):
        """Initialize chat manager with Gemini model"""
        genai.configure(api_key=api_key)
        
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config
        )
        
        self.chat = self.model.start_chat(history=[])
        self.conversation_history: List[Dict] = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create conversations directory if it doesn't exist
        self.conversations_dir = "conversations"
        if not os.path.exists(self.conversations_dir):
            os.makedirs(self.conversations_dir)
        
    def send_message(self, message: str) -> str:
        """Send message and get response while maintaining context"""
        try:
            response = self.chat.send_message(message)
            response_text = response.text
            
            self.conversation_history.append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().isoformat()
            })
            
            return response_text
            
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def get_context(self) -> List[Dict]:
        """Get current conversation context"""
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.conversation_history[-10:]
        ]
    
    def clear_context(self):
        """Clear conversation context"""
        self.chat = self.model.start_chat(history=[])
        self.conversation_history = []
    
    def save_conversation(self, filename: Optional[str] = None):
        """Save conversation to JSON file in conversations directory"""
        if filename is None:
            filename = f"conversation_{self.session_id}.json"
        
        # Ensure filename ends with .json
        if not filename.endswith('.json'):
            filename += '.json'
        
        # Full path in conversations directory
        filepath = os.path.join(self.conversations_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "messages": self.conversation_history
            }, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def load_conversation(self, filename: str):
        """Load conversation from JSON file in conversations directory"""
        # If filename doesn't include directory, add conversations dir
        if not filename.startswith(self.conversations_dir):
            filepath = os.path.join(self.conversations_dir, filename)
        else:
            filepath = filename
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.session_id = data["session_id"]
        self.conversation_history = data["messages"]
        
        self.chat = self.model.start_chat(history=[])
        for msg in self.conversation_history:
            if msg["role"] == "user":
                self.chat.send_message(msg["content"])
    
    def list_saved_conversations(self) -> List[str]:
        """List all saved conversations"""
        if not os.path.exists(self.conversations_dir):
            return []
        
        files = [f for f in os.listdir(self.conversations_dir) 
                if f.startswith('conversation_') and f.endswith('.json')]
        return sorted(files, reverse=True)  # Most recent first
    
    def get_stats(self) -> Dict:
        """Get conversation statistics"""
        user_messages = sum(1 for msg in self.conversation_history if msg["role"] == "user")
        ai_messages = sum(1 for msg in self.conversation_history if msg["role"] == "assistant")
        total_chars = sum(len(msg["content"]) for msg in self.conversation_history)
        
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": user_messages,
            "ai_messages": ai_messages,
            "total_characters": total_chars,
            "session_id": self.session_id,
            "saved_conversations": len(self.list_saved_conversations())
        }