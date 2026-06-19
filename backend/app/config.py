from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    skills_repo_url: str
    sync_interval_minutes: int = 60
    repo_local_path: str = "/app/repo"
    database_path: str = "/app/data/skills.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
