from util import logger, configure_logging 
from app import start_threads

def main(production_mode = False):
    logger.info(production_mode)
    configure_logging(production_mode)

    logger.info("############## Starting new Chartswitch ##############")

    start_threads()

    logger.info("Exiting main...")

if __name__ == "__main__":
    import argparse
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run the application.')
    parser.add_argument('--prod', action='store_true', help='Run in production mode without debug logging')
    args = parser.parse_args()

    # Start main
    main(production_mode=args.prod)