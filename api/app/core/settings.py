import os
import logging
from pathlib import Path

import requests
from pydantic import BaseSettings
from urllib3.exceptions import InsecureRequestWarning

logging.getLogger("urllib3").setLevel(logging.WARNING)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class Settings(BaseSettings):
    # app info
    app_name : str = "In-place File Translation"
    app_version: str = "0.0.1"
    app_description: str

# relative path to `documentation.md`
settings = Settings(
    app_description=(
        Path(__file__).parent.parent / "static/documentation.md"
    ).read_text(encoding="utf-8")
)