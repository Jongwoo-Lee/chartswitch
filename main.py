import signal
from util import logger, configure_logging 
from app import WebsocketManager, WindowManager, start_threads


def signal_handler(sig, frame):
    logger.info(f"Signal {sig} received. Shutting down gracefully...")

    WebsocketManager().cleanup()


def main(production_mode = False):
    logger.info(production_mode)
    configure_logging(production_mode)

    logger.info("############## Starting new Chartswitch ##############")

    # Register the cleanup functions to be called on exit
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    start_threads()
   
    try:
        WindowManager().start_window()
    except KeyboardInterrupt:
        print("Interrupted by user")

    logger.debug("Websocket threads are closed successfully")
    logger.info("Exiting main...")

if __name__ == "__main__":
    import argparse
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run the application.')
    parser.add_argument('--prod', action='store_true', help='Run in production mode without debug logging')
    args = parser.parse_args()

    # Start main
    main(production_mode=args.prod)