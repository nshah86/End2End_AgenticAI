import os
from configparser import ConfigParser

class Config:
    def __init__(self, config_file='uiconfigfile.ini'):
        # Get the directory where this script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the config file
        config_path = os.path.join(current_dir, config_file)
        
        self.config = ConfigParser()
        self.config.read(config_path)
        
    def get(self, section, option, fallback=None):
        """Get a configuration value with optional fallback."""
        return self.config.get(section, option, fallback=fallback)
        
    def get_all(self, section):
        """Get all options in a section."""
        return dict(self.config.items(section))
        
    def get_model_options(self, llm_provider):
        """Get model options for a specific LLM provider."""
        option_key = f"{llm_provider.upper()}_MODEL_OPTIONS"
        options_str = self.get('Default', option_key, '')
        return [opt.strip() for opt in options_str.split(',') if opt.strip()]
        
    def get_llm_options(self):
        """Get all LLM-related options from the Default section."""
        return {
            'llm_option': self.get('Default', 'LLM_OPTION', ''),
            'model_options': {
                'groq': self.get_model_options('groq'),
                'openai': self.get_model_options('openai'),
                'anthropic': self.get_model_options('anthropic')
            },
            'temperature': float(self.get('Default', 'TEMPERATURE', '0.7')),
            'max_tokens': int(self.get('Default', 'MAX_TOKENS', '4096')),
            'top_p': float(self.get('Default', 'TOP_P', '0.95')),
            'frequency_penalty': float(self.get('Default', 'FREQUENCY_PENALTY', '0.0')),
            'presence_penalty': float(self.get('Default', 'PRESENCE_PENALTY', '0.0'))
        }