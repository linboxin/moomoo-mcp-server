import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class OpenDConfig(BaseModel):
    host: str = Field(default="127.0.0.1", description="OpenD Host")
    port: int = Field(default=11111, description="OpenD Port")
    pwd: str = Field(default="", description="OpenD Unlock Password")
    env: str = Field(default="paper", description="Environment: paper or live")

    @classmethod
    def from_env(cls) -> "OpenDConfig":
        return cls(
            host=os.getenv("OPEND_HOST", "127.0.0.1"),
            port=int(os.getenv("OPEND_PORT", "11111")),
            pwd=os.getenv("OPEND_PWD", ""),
            env=os.getenv("MOOMOO_ENV", "paper"),
        )

config = OpenDConfig.from_env()
