import yaml
import os

class ConfigHandler:
    def __init__(self, config_file='config.yml'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                try:
                    return yaml.safe_load(file) or {}
                except yaml.YAMLError as e:
                    print(f"Error loading configuration: {e}")
                    return {}
        else:
            print(f"Config file {self.config_file} not found. Using default settings.")
            return {}

    def save_config(self):
        try:
            with open(self.config_file, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False)
            print(f"Configuration saved to {self.config_file}")
        except Exception as e:
            print(f"Error saving configuration: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def update(self, new_config):
        self.config.update(new_config)
        self.save_config()

    def print_config(self):
        print("Current configuration:")
        for key, value in self.config.items():
            print(f"{key}: {value}")

    def reset_to_default(self, default_config):
        self.config = default_config.copy()
        self.save_config()
        print("Configuration reset to default values.")