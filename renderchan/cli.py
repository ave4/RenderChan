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

    parser.add_option("--profile", dest="profile",
            action="store",
            help=_("Set rendering profile."))
    parser.add_option("--stereo", dest="stereo",
            action="store",
            help=_("Enable stereo-3D rendering. Possible values for STEREO:\n\n"
                   "'vertical' or 'v', "
                   "'horizontal' or 'h', "
                   "'left' or 'l', "
                   "'right' or 'r'. "
                    ))

    # TODO: Not implemented
    parser.add_option("--width", dest="width",
            action="store",
            help=_("Output width."))
    # TODO: Not implemented
    parser.add_option("--height", dest="height",
            action="store",
            help=_("Output height."))

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
    parser.add_option("--allocate", dest="allocateOnly",
            action="store_true",
            default=False,
            help=_("Don't do the actual render, just allocate a placeholder for file."))

    options, args = parser.parse_args()

    return options, args


def main(argv):
    options, args = process_args()

    if len(args)<1:
        print "Please specify filename for rendering."
        sys.exit(0)

    filename = os.path.abspath(args[0])

    renderchan = RenderChan()
    if options.profile:
        renderchan.projects.setProfile(options.profile)

    useDispatcher=False
    if options.dispatcherHost:
        renderchan.setHost(options.dispatcherHost)
        if options.dispatcherPort:
            renderchan.setPort(options.dispatcherPort)
        useDispatcher=True
    elif options.dispatcherPort:
        print "WARNING: No dispatcher host specified. Ignoring --dispatcher-port parameter."

    taskfile = RenderChanFile(filename, renderchan.modules, renderchan.projects)
    renderchan.submit(taskfile, useDispatcher, options.dependenciesOnly, options.allocateOnly, options.stereo)
