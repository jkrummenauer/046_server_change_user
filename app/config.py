import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

NETWORK_PATH = os.getenv("NETWORK_PATH")
DOMAIN = os.getenv("DOMAIN")

if NETWORK_PATH is None:
    raise ValueError("A variável NETWORK_PATH não foi encontrada no arquivo .env")

if DOMAIN is None:
    raise ValueError("A variável DOMAIN não foi encontrada no arquivo .env")
