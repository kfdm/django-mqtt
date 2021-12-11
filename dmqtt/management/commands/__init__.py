import logging

from django.core.management.color import supports_color
from django.utils.termcolors import colorize, make_style

if supports_color():
    logging.addLevelName(logging.ERROR, colorize("ERROR", fg="red", opts=("bold",)))
    logging.addLevelName(logging.WARN, colorize("WARNING", fg="yellow", opts=("bold",)))
    logging.addLevelName(logging.INFO, colorize("INFO", fg="white", opts=("bold",)))
    logging.addLevelName(logging.DEBUG, colorize("DEBUG", fg="cyan", opts=("bold",)))

    green = make_style(fg="green")
    red = make_style(fg="red")
else:

    def green(x):
        return x

    def red(x):
        return x
