import ac
import sys

class Logger:
    @staticmethod
    def info(msg):
        """Log to AC internal log and Python Console"""
        formatted_msg = "[Pinheirinho] {}".format(msg)
        ac.log(formatted_msg)
        ac.console(formatted_msg) # Shows in Python Apps Debug
        # Also print to stdout for external debuggers if attached
        # print(formatted_msg) 

    @staticmethod
    def error(msg):
        formatted_msg = "[Pinheirinho ERROR] {}".format(msg)
        ac.log(formatted_msg)
        ac.console(formatted_msg)
