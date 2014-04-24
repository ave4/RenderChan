__author__ = 'Konstantin Dmitriev'

from gettext import gettext as _
from optparse import OptionParser
import os.path

from renderchan.core import RenderChan
from renderchan.file import RenderChanFile


def process_args():
    parser = OptionParser(
        usage=_("""
    %prog [FILE]               """))

    parser.add_option("--width", dest="width",
            action="store",
            help=_("Output width."))
    parser.add_option("--height", dest="height",
            action="store",
            help=_("Output height."))

    parser.add_option("--use-dispatcher", dest="useDispatcher",
            action="store_true",
            default=False,
            help=_("Use dispatcher for renderfarm rendering."))
    parser.add_option("--dispatcher-host", dest="dispatcherHost",
            action="store",
            help=_("Set remote dispatcher host."))
    parser.add_option("--dispatcher-port", dest="dispatcherPort",
            action="store",
            help=_("Set remote dispatcher port."))

    parser.add_option("--deps", dest="dependenciesOnly",
            action="store_true",
            default=False,
            help=_("Render dependencies, but not file itself."))
    options, args = parser.parse_args()

    return options, args


def main(argv):
    options, args = process_args()
    filename = os.path.abspath(args[0])

    renderchan = RenderChan()
    if options.useDispatcher:
        if options.dispatcherHost:
            renderchan.setHost(options.dispatcherHost)
        if options.dispatcherPort:
            renderchan.setPort(options.dispatcherPort)

    taskfile = RenderChanFile(filename, renderchan.modules, renderchan.projects)
    renderchan.submit(taskfile, options.useDispatcher, options.dependenciesOnly)