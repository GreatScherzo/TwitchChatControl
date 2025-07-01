import logging
import logging.config
import sys

"""
class to store logging settings
"""
class LogSettings:
    def __init__(self):
        self.dictLogConfig = {
            "version": 1 ,
            # "handlers": {
            #     "fileHandler":
            #         {
            #             "class": "logging.FileHandler",
            #             "formatter": "myFormatter",
            #             "filename": r"./program.log"
            #         },
            #         # "consoleHandler": {
            #         #     "class": "logging.StreamHandler",
            #         #     "formatter": "myFormatter"
            #         # },
            # },
            # "loggers": {
            #     "wxApp": {
            #         "handlers": ["fileHandler", "consoleHandler"],
            #         "level": "INFO"
            #     }
            # },
            "formatters": {
                "myFormatters": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            }
        }

        self.logger = None

    def InitializeLogSettings(self):
        logging.config.dictConfig(self.dictLogConfig)

    def InitializeBasicLogSettings(self):
        logging.basicConfig(filename="program.log",
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filemode='a',
                            )

        # Setting the threshold of logger to DEBUG
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        self.logger.addHandler(consoleHandler)
