"""
Base classes for writing management commands (named commands which can
be executed through ``django-admin.py`` or ``manage.py``).

"""

import os
import sys
from optparse import make_option, OptionParser

import django
from django.core.exceptions import ImproperlyConfigured
from django.core.management.color import color_style
from django.core.management.base import CommandError

def copy_helper(style, base, name, directory, other_name=''):
    """
    Copies either a Django application layout template or a Django project
    layout template into the specified directory.

    """
    # style -- A color style object (see django.core.management.color).
    # base -- The GLAMkit toolkit which provides base classes for the app.
    # name -- The name of the application or project.
    # directory -- The directory to which the layout template should be copied.
    # other_name -- When copying an application layout, this should be the name
    #               of the project.
    import re
    import shutil
    other = 'project'
    if not re.search(r'^[_a-zA-Z]\w*$', name): # If it's not a valid directory name.
        # Provide a smart error message, depending on the error.
        if not re.search(r'^[_a-zA-Z]', name):
            message = 'make sure the name begins with a letter or underscore'
        else:
            message = 'use only numbers, letters and underscores'
        raise CommandError("%r is not a valid %s name. Please %s." % (name, app_or_project, message))
    top_dir = os.path.join(directory, name)
    try:
        os.mkdir(top_dir)
    except OSError, e:
        raise CommandError(e)

    # Determine where the app or project templates are. Use
    # django.__path__[0] because we don't know into which directory
    # django has been installed.
    template_dir = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app_templates', base))

    for d, subdirs, files in os.walk(template_dir):
        relative_dir = d[len(template_dir)+1:].replace('%s_name' % base, name)
        if relative_dir:
            os.mkdir(os.path.join(top_dir, relative_dir))
        for i, subdir in enumerate(subdirs):
            if subdir.startswith('.'):
                del subdirs[i]
        for f in files:
            if not f.endswith('.py'):
                # Ignore .pyc, .pyo, .py.class etc, as they cause various
                # breakages.
                continue
            path_old = os.path.join(d, f)
            path_new = os.path.join(top_dir, relative_dir, f.replace('%s_name' % base, name))
            fp_old = open(path_old, 'r')
            fp_new = open(path_new, 'w')
            fp_new.write(fp_old.read().replace('{{ %s_name }}' % base, name).replace('{{ %s_name }}' % other, other_name))
            fp_old.close()
            fp_new.close()
            try:
                shutil.copymode(path_old, path_new)
                _make_writeable(path_new)
            except OSError:
                sys.stderr.write(style.NOTICE("Notice: Couldn't set permission bits on %s. You're probably using an uncommon filesystem setup. No problem.\n" % path_new))

def _make_writeable(filename):
    """
    Make sure that the file is writeable. Useful if our source is
    read-only.
    
    """
    import stat
    if sys.platform.startswith('java'):
        # On Jython there is no os.access()
        return
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)
