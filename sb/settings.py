class Settings:
    
    def __init__(self, dict):
        
        for key in dict:
            setattr(self, key, dict[key])