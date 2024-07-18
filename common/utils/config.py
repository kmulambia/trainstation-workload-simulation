from dotenv import load_dotenv
import os
from common.utils.logger import get_logger

load_dotenv()
logger = get_logger()

def get_config(name):
    try:
        value = os.getenv(name)

        if value is None:
            raise Exception(f"Environment variable {name} not configured")
        return str(value)
    
    except Exception as e:

        raise Exception(f"Failed to get environment variable {name} with error: {str(e)}")