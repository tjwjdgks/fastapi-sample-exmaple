import os
from dotenv import load_dotenv


class EnvLoader:
    def __init__(self):
        self.env_mapping = {
            "local": ".env.local",
            "dev": ".env.dev",
        }
        self.env = os.getenv("APPS_ENV", "local")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.dotenv_path = os.path.join(
            self.current_dir, self.env_mapping.get(self.env, ".env.local")
        )

    def load(self):
        if not os.path.exists(self.dotenv_path):
            raise Exception(f"{self.dotenv_path} does not exist.")
        load_dotenv(self.dotenv_path)


env_loader = EnvLoader()
