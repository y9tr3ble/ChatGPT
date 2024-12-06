from typing import Dict

class UserService:
    def __init__(self):
        self.user_models: Dict[str, str] = {}
    
    def get_user_model(self, user_id: str) -> str:
        """Get user's current model (default to OpenAI)"""
        return self.user_models.get(user_id, "openai")
    
    def set_user_model(self, user_id: str, model: str) -> None:
        """Set user's preferred model"""
        if model not in ["openai", "gemini"]:
            raise ValueError(f"Unsupported model: {model}")
        self.user_models[user_id] = model 