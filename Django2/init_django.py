import sys,django,os
from django.utils.importlib import import_module
import settings
#os.environ['DJANGO_SETTINGS_MODULE'] ='/home/sh1n0b1/.xbmc/plugins/video/Django2/settings.py'
#print(os.getenv('DJANGO_SETTINGS_MODULE'))
def setup_environ(settings_mod, original_settings_path=None):
    """
    Configures the runtime environment. This can also be used by external
    scripts wanting to set up a similar environment to manage.py.
    Returns the project directory (assuming the passed settings module is
    directly in the project directory).

    The "original_settings_path" parameter is optional, but recommended, since
    trying to work out the original path from the module can be problematic.
    """
    # Add this project to sys.path so that it's importable in the conventional
    # way. For example, if this file (manage.py) lives in a directory
    # "myproject", this code would add "/path/to/myproject" to sys.path.
    if '__init__.py' in settings_mod.__file__:
        p = os.path.dirname(settings_mod.__file__)
    else:
        p = settings_mod.__file__
    project_directory, settings_filename = os.path.split(p)
    if project_directory == os.curdir or not project_directory:
        project_directory = os.getcwd()
    project_name = os.path.basename(project_directory)

    # Strip filename suffix to get the module name.
    settings_name = os.path.splitext(settings_filename)[0]

    # Strip $py for Jython compiled files (like settings$py.class)
    if settings_name.endswith("$py"):
        settings_name = settings_name[:-3]

    # Set DJANGO_SETTINGS_MODULE appropriately.
    if original_settings_path:
        os.environ['DJANGO_SETTINGS_MODULE'] = original_settings_path
    else:
        os.environ['DJANGO_SETTINGS_MODULE'] = '%s.%s' % (project_name, settings_name)

    # Import the project module. We add the parent directory to PYTHONPATH to
    # avoid some of the path errors new users can have.
    sys.path.append(os.path.join(project_directory, os.pardir))
    project_module = import_module(project_name)
    sys.path.pop()

    return project_directory
def main():
	sys.path.append("/home/sh1n0b1/.xbmc/plugins/video/")
	sys.path.append("/home/sh1n0b1/.xbmc/plugins/video/Django2/")
	setup_environ(settings)
main()
