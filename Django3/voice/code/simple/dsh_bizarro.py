#
# copied from Postmanet-2.
#

import os



if os.name == 'posix':
    from dsh_linux import *
elif os.name == 'nt':
    from dsh_xp import *
else:
    raise 'dsh_bizaro: unknown OS'



def append_path_trailing_slash(path):
    """called by install-repository-lai.py, for writing Resources.txt.
    pulled out of OS-specific files."""
    separator = os.sep
    if path[-1] != separator:
        path = path + separator
    return path
