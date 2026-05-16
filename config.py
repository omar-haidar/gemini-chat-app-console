import os

class Config:
    # API Key will be loaded from settings.txt
    GOOGLE_API_KEY = None
    
    # Model settings
    MODEL_NAME = "gemini-3-flash-preview"
    
    # Chat settings
    MAX_HISTORY = 50
    TEMPERATURE = 0.7
    TOP_P = 0.95
    TOP_K = 40
    
    # Terminal colors
    COLORS = {
        'user': '\033[92m',
        'ai': '\033[94m',
        'system': '\033[93m',
        'error': '\033[91m',
        'reset': '\033[0m'
    }
    
    @classmethod
    def load_api_key(cls):
        """Load API key from settings.txt file"""
        try:
            with open('settings.txt', 'r') as f:
                for line in f:
                    if line.startswith('API_KEY='):
                        cls.GOOGLE_API_KEY = line.split('=', 1)[1].strip()
                        return True
        except FileNotFoundError:
            pass
        return False