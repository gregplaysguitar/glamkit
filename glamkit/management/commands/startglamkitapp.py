import os

from django.core.management.base import BaseCommand, CommandError, LabelCommand, make_option
from django.utils.importlib import import_module
from glamkit.management.base import copy_helper

class Command(LabelCommand):
    help = "Creates a GLAMkit blogtools app directory structure for the given app name in the current directory."
    args = "[appname]"
    label = 'application name'

    requires_model_validation = False
    # Can't import settings during this command, because they haven't
    # necessarily been created.
    can_import_settings = False

    option_list = BaseCommand.option_list + (
        make_option('--blog', '-b', dest='base', action="store_const", const='blogtools', help='Creates an app using GLAMkit blogtools'),
        make_option('--events', '-e', dest='base', action="store_const", const='eventtools', help='Creates an app using GLAMkit eventtools'),
    )

    def handle_label(self, app_name, directory=None, **options):
        if directory is None:
            directory = os.getcwd()
            
        base = options.get('base', None)
        # Determine the project_name by using the basename of directory,
        # which should be the full path of the project directory (or the
        # current directory if no directory was passed).
        project_name = os.path.basename(directory)
        if app_name == project_name:
            raise CommandError("You cannot create an app with the same name"
                               " (%r) as your project." % app_name)

        # Check that the app_name cannot be imported.
        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            raise CommandError("%r conflicts with the name of an existing Python module and cannot be used as an app name. Please try another name." % app_name)
            
        if base == None:
            raise CommandError("You must set a flag to specify the type of GLAMkit app you want")

        try:
            import_module(app_name)
        except ImportError:
            raise CommandError("%(app_type)s was not found in settings.INSTALLED_APPS. %(app_name)r requires %(app_type)s to be installed" % {'app_name': app_name, 'app_type': base})

        copy_helper(self.style, base, app_name, directory, project_name)
