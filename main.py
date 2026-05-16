#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from chat_manager import ChatManager
from config import Config

class SimpleChatApp:
    def __init__(self):
        """Initialize chat application"""
        self.manager = None
        
    def print_separator(self, char="=", length=50):
        """Print separator line"""
        print(char * length)
    
    def show_help(self):
        """Display available commands"""
        help_text = """
Available Commands:
  /help     - Show this help menu
  /clear    - Clear conversation context
  /save     - Save current conversation
  /load     - Load previous conversation
  /list     - List all saved conversations
  /stats    - Show conversation statistics
  /context  - Show current conversation context
  /exit     - Exit application
        """
        print(help_text)
    
    def clear_chat(self):
        """Clear conversation"""
        self.manager.clear_context()
        print("✅ Conversation context cleared")
    
    def save_chat(self):
        """Save conversation to file"""
        try:
            filepath = self.manager.save_conversation()
            print(f"💾 Conversation saved to: {filepath}")
        except Exception as e:
            print(f"❌ Save error: {e}")
    
    def list_conversations(self):
        """List all saved conversations"""
        files = self.manager.list_saved_conversations()
        
        if not files:
            print("📁 No saved conversations found in 'conversations' folder")
            return
        
        print(f"\n📁 Saved Conversations ({len(files)} files):")
        print("-" * 50)
        for i, file in enumerate(files, 1):
            filepath = os.path.join("conversations", file)
            size = os.path.getsize(filepath)
            print(f"  {i}. {file} ({size:,} bytes)")
        print()
    
    def load_chat(self):
        """Load conversation from file"""
        try:
            files = self.manager.list_saved_conversations()
            
            if not files:
                print("❌ No saved conversations found in 'conversations' folder")
                return
            
            print("\n📁 Available conversations:")
            for i, file in enumerate(files, 1):
                print(f"  {i}. {file}")
            
            choice = input("\n🔢 Select file number (or 0 to cancel): ").strip()
            
            if choice == '0' or not choice:
                return
            
            file_index = int(choice) - 1
            if 0 <= file_index < len(files):
                self.manager.load_conversation(files[file_index])
                print(f"✅ Loaded conversation: {files[file_index]}")
                print("📝 Last 5 messages:")
                for msg in self.manager.conversation_history[-5:]:
                    role = '👤' if msg['role'] == 'user' else '🤖'
                    print(f"  {role}: {msg['content'][:100]}...")
            else:
                print("❌ Invalid selection")
                
        except Exception as e:
            print(f"❌ Load error: {e}")
    
    def show_stats(self):
        """Display conversation statistics"""
        stats = self.manager.get_stats()
        print(f"""
📊 Conversation Statistics:
  • Session ID: {stats['session_id']}
  • Total Messages: {stats['total_messages']}
  • Your Messages: {stats['user_messages']}
  • Assistant Replies: {stats['ai_messages']}
  • Total Characters: {stats['total_characters']:,}
  • Saved Conversations: {stats['saved_conversations']}
        """)
    
    def show_context(self):
        """Display current conversation context"""
        context = self.manager.get_context()
        if not context:
            print("📝 No context available")
            return
        
        print("\n📝 Current Conversation Context:")
        for i, msg in enumerate(context, 1):
            role = '👤 You' if msg['role'] == 'user' else '🤖 Assistant'
            print(f"  {i}. {role}: {msg['content'][:100]}...")
        print()
    
    def exit_app(self):
        """Exit application"""
        print("\n👋 Goodbye!")
        choice = input("Save conversation before exit? (y/n): ").lower()
        if choice == 'y':
            self.save_chat()
        sys.exit(0)
    
    def setup_api_key(self):
        """Setup API key"""
        # Try to load from settings file
        if Config.load_api_key() and Config.GOOGLE_API_KEY:
            return Config.GOOGLE_API_KEY
        
        # If no settings file, ask user for key
        print("=" * 50)
        print("🔑 No API Key Found")
        print("Please enter your Google AI Studio API key")
        print("=" * 50)
        
        api_key = input("API Key: ").strip()
        
        if not api_key:
            print("❌ A valid API key is required")
            sys.exit(1)
        
        # Save key for future use
        save_choice = input("💾 Save API key for future use? (y/n): ").lower()
        if save_choice == 'y':
            with open('settings.txt', 'w') as f:
                f.write(f'API_KEY={api_key}')
            print("✅ API key saved to settings.txt")
            print("⚠️ Note: This file contains your secret key, do not share it!")
        
        return api_key
    
    def initialize(self):
        """Initialize application"""
        api_key = self.setup_api_key()
        
        try:
            print("⏳ Connecting to Gemini...")
            self.manager = ChatManager(api_key, Config.MODEL_NAME)
            print("✅ Connected successfully!")
            print(f"📁 Conversations will be saved to: 'conversations/' folder")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def run(self):
        """Run chat application"""
        print("=" * 50)
        print("🤖 Gemini Chat Application")
        print("   Intelligent Chat with Context Support")
        print("=" * 50)
        
        if not self.initialize():
            return
        
        self.show_help()
        print("\n💡 Type /help to see available commands\n")
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                if user_input.startswith('/'):
                    command = user_input.split()[0].lower()
                    
                    if command == '/help':
                        self.show_help()
                    elif command == '/clear':
                        self.clear_chat()
                    elif command == '/save':
                        self.save_chat()
                    elif command == '/load':
                        self.load_chat()
                    elif command == '/list':
                        self.list_conversations()
                    elif command == '/stats':
                        self.show_stats()
                    elif command == '/context':
                        self.show_context()
                    elif command in ['/exit', '/quit']:
                        self.exit_app()
                    else:
                        print(f"❌ Unknown command: {command}")
                        print("Type /help to see available commands")
                    continue
                
                # Send message and get response
                print("⏳ Thinking...", end='\r')
                
                try:
                    response = self.manager.send_message(user_input)
                    print(" " * 20, end='\r')  # Clear thinking indicator
                    print(f"🤖 Assistant:\n{response}\n")
                    
                except Exception as e:
                    print(f"\n❌ Error: {e}")
            
            except KeyboardInterrupt:
                print("\n\n⚠️ Ctrl+C detected")
                self.exit_app()
            
            except EOFError:
                self.exit_app()

def main():
    """Main entry point"""
    app = SimpleChatApp()
    app.run()

if __name__ == "__main__":
    main()