import sys,os,subprocess,logging
import dvoice.db.models
#from dvoice.db.models import Organization, Person, Item, KeyWord, Event
import dsh_django_config,dsh_django_utils,dsh_dump_models
import dsh_django_utils2
dsh_django_utils2.append_to_sys_path(
    dsh_django_config.lookup('DSH_VOICE_CODE_DIR'))
import dsh_utils,dsh_config,dsh_agi
from django.utils.encoding import smart_str, smart_unicode



def config_obj():
    """we need just one object in ZObject01.
    if it's not there, make one."""

    objs = dvoice.db.models.ZObject01.objects.all()
    if len(objs) > 0:
        return objs[0]

    configObj = dvoice.db.models.ZObject01()
    configObj.save()
    return configObj



def get(field):
    config = config_obj()

    if not config:
        dsh_django_utils.error_event(
            'dsh_db_config.get: no config obj', errorLevel='CRT')
        return None

    try:
        value = getattr(config, field)
    except:
        dsh_django_utils.error_event(
            'dsh_db_config.get: failed to get this field: ' + field,
            errorLevel='CRT')
        return None

    return value



def set(field, value):
    config = config_obj()

    if not config:
        dsh_django_utils.error_event(
            'dsh_db_config.set: no config obj', errorLevel='CRT')
        return

    try:
        oldVal = getattr(config, field)
        if oldVal == value:
            return
        setattr(config, field, value)
        config.save()
    except:
        dsh_django_utils.error_event(
            'dsh_db_config.set: failed to get this field: ' + field +\
            ' <- ' + repr(value), errorLevel='CRT')
        return
