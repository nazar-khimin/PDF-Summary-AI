import os
import logging
from datetime import datetime

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=f"logs/{datetime.now().strftime('%Y_%m_%d_%H:%M:%S')}",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)
