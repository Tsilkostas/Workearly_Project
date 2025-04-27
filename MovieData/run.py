from main import MovieDataApp
import sys
import logging
from typing import NoReturn



def configure_logging() -> None:
    """Configure logging with both file and console output."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # File handler (rotating logs)
    file_handler = logging.FileHandler("movie_data.log", mode='a')
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Remove any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def main() -> int:
    """Main entry point with return codes.
    
    Returns:
        0 on success, 1 on error
    """
    configure_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting MovieData app...")
        app = MovieDataApp()
        app.fetch_and_store_movie_data()
        logger.info("Data fetch completed successfully!")
        return 0
    except Exception as e:
        logger.exception("Critical error occurred:")  # This logs the full traceback
        return 1
    finally:
        logging.shutdown()  # Ensure all logs are flushed

if __name__ == "__main__":
    sys.exit(main())