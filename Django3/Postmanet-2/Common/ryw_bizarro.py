import os



if os.name == 'posix':
    from ryw_linux import *
elif os.name == 'nt':
    from ryw_xp import *
else:
    raise 'ryw_bizaro: unknown OS'



def append_path_trailing_slash(path):
    """called by install-repository-lai.py, for writing Resources.txt.
    pulled out of OS-specific files."""
    separator = os.sep
    if path[-1] != separator:
        path = path + separator
    return path
