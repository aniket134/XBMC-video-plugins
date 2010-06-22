"""
python bizarro.py posix
python bizarro.py nt

returns with 0 error code if the OS name is as expected.
"""

import sys, os


if __name__ == '__main__':
    osArgName = sys.argv[1]
    if osArgName == os.name:
        sys.exit(0)
    sys.exit(1)
