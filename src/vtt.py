"""This module is used to run the vtt server or the control client (which can be used to manage the server from the
command line)"""

import argparse
import logging
import server


def run_server(settings: server.ServerSettings):
    srv = server.Server(settings)
    srv.run()


if __name__ == '__main__':
    LOG_LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    parser = argparse.ArgumentParser("vtt", description="Run the vtt server or run the cli client",
                                     epilog="In server mode, the address and port are where the server is bound to.\n"
                                            "In client mode they are the ip and port of the server to connect to.")
    parser.add_argument("mode", action='store', choices=['server', 'cli_client'])
    parser.add_argument("-A", "--address", action='store', default="::1")
    parser.add_argument("-p", "--port", action='store', default=8080, type=int)
    parser.add_argument("-L", "--log-level", action='store', type=str, default='info')

    args = parser.parse_args()

    logging.getLogger().setLevel(LOG_LEVELS[args.log_level])

    if args.mode == 'server':
        logging.info("Running in server mode")
        settings = server.ServerSettings(bind_address=args.address, port=args.port)

        run_server(settings)
    elif args.mode == 'cli_client':
        logging.info("Running in CLI client mode")
