from typing import Dict
from src.services.storage_service import StorageService

class UserService:
    def __init__(self, storage: StorageService):
        self.user_models: Dict[str, str] = {}
        self.storage = storage
        
    def load_user_state(self, user_id: str) -> None:
        """Load user state from storage"""
        data = self.storage.load_user_data(user_id)
        if data and 'model' in data:
            self.user_models[user_id] = data['model']
            
    def save_user_state(self, user_id: str) -> None:
        """Save user state to storage"""
        data = {
            'model': self.user_models.get(user_id, 'openai')
        }
        self.storage.save_user_data(user_id, data)
        
    def get_user_model(self, user_id: str) -> str:
        """Get user's current model (default to OpenAI)"""
        if user_id not in self.user_models:
            self.load_user_state(user_id)
        return self.user_models.get(user_id, "openai")
    
    def set_user_model(self, user_id: str, model: str) -> None:
        """Set user's preferred model and save state"""
        if model not in ["openai", "gemini"]:
            raise ValueError(f"Unsupported model: {model}")
        self.user_models[user_id] = model
        self.save_user_state(user_id)