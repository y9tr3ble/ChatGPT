import json
import os
from typing import Dict, List
import logging

class StorageService:
    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = storage_dir
        self.ensure_storage_dir()
        
    def ensure_storage_dir(self):
        """Create storage directory if it doesn't exist"""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
    def _get_user_file_path(self, user_id: str) -> str:
        """Get path to user's data file"""
        return os.path.join(self.storage_dir, f"user_{user_id}.json")
        
    def save_user_data(self, user_id: str, data: Dict) -> None:
        """Save user data to file, merging with existing data"""
        try:
            file_path = self._get_user_file_path(user_id)
            
            # Load existing data
            existing_data = {}
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            
            # Merge new data with existing data
            existing_data.update(data)
            
            # Save merged data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
                
            logging.info(f"Saved user data for {user_id}: {existing_data}")
            
        except Exception as e:
            logging.error(f"Error saving user data: {e}")
            
    def load_user_data(self, user_id: str) -> Dict:
        """Load user data from file"""
        try:
            file_path = self._get_user_file_path(user_id)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logging.info(f"Loaded user data for {user_id}: {data}")
                    return data
        except Exception as e:
            logging.error(f"Error loading user data: {e}")
        return {} 