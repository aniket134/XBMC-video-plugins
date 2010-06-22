#
# called by:
# /usr/share/python-support/python-django/django/contrib/admin/
# sites.py, options.py, admin_list.py
#

import dsh_common_config
import dsh_config
dsh_common_config.init(dsh_config)



request = None



def set(req):
    global request
    request = req



def get():
    return request



def deny_it(request):
    if not request:
        return True
    return not request.user.is_superuser



def no_permission_reply():
    return dsh_common_config.lookup2('DSH_PERM_DENIED_URL')
