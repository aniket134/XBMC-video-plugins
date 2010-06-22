#!/usr/bin/python -u
#
# called by the failed extension of extensions.conf
# for handling .call files that are not picked up.
#


import sys,logging,os,signal,subprocess,datetime,time
import dsh_agi,dsh_utils,dsh_config,dsh_bizarro,dsh_django2



#
# django-specific initializations.
#
os.environ['DJANGO_SETTINGS_MODULE'] = dsh_config.lookup(
    'DJANGO_SETTINGS_MODULE')
dsh_utils.add_to_sys_path(dsh_config.lookup('django_sys_paths'))
from dvoice.db.models import Person,Organization,Item,Event
import dvoice.db.models
import dsh_django_utils,dsh_django_config

    
    
#
# global variables for the signal handler.
#
globals4signal = {}
globals4signal['session_id'] = ''



def is_triggered_by_dial_now(dshUid):
    """
    the indicator is like: '__DIAL_NOW__'
    if this is triggered as "dial now," the indicator is postfixed by
    the real dsh_uid.
    """
    
    dialNowIndicator = dsh_django_config.lookup('DIAL_NOW_INDICATOR')
    indicLen = len(dialNowIndicator)
    prefix = dshUid[:indicLen]
    postfix = dshUid[indicLen:]
    
    if prefix == dialNowIndicator:
        #
        # this dot call is triggered as a result of hitting the
        # dial-now icon.  we're not re-arming.
        #
        message = 'dsh_failed.is_triggered_by_dial_now: ' + postfix
        dsh_agi.report_event(message, sessionID=get_session())
        dsh_utils.give_news(message, logging.info)
        return True

    return False
    


def hangup_signal_handler(signum, frame):
    """called after the hangup signal is received."""

    global globals4signal
    
    dsh_utils.db_print2('dsh_failed.signal_handler: entered...', 116)
    time.sleep(1)
    
    calleeDshUid = globals4signal['callee_dsh_uid']

    if is_triggered_by_dial_now(calleeDshUid):
        sys.exit(0)
    
    callee = dsh_django_utils.get_foreign_key(Person, calleeDshUid)
    if not callee:
        message = 'dsh_failed: no such callee found: ' + calleeDshUid
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel = 'ERR',
                             sessionID=get_session())
        sys.exit(1)
    else:
        dsh_utils.db_print('dsh_failed: found callee: ' + repr(callee), 116)

    event = Event(
        owner=callee,
        phone_number=callee.phone_number,
        action='NOPU',
        etype='INF',
        description='.call not picked up. re-arming.',
        session=get_session())
    event.save()
    dsh_django_utils.check_auto_timed_calls_for_person(
        callee, sessionID=get_session())

    calleeInfo = dsh_django_utils.callee_info(callee)    
    
    dsh_utils.give_news('dsh_failed.signal_handler: rearming callee: '+\
                        calleeInfo, logging.info)



def get_session():
    global globals4signal
    return globals4signal['session_id']



def main():
    global globals4signal

    globals4signal['session_id'] = dvoice.db.models.assign_dsh_uid()

    dsh_django2.init_log(
        'dsh_failed: entered, session %s --------------------' % \
        (get_session(),))


    #
    # get the AGI environment variables.
    # chicken out if it's not due to .call failure.
    #
    env = dsh_agi.read_env()
    if env == {}:
        message = 'dsh_failed: failed to read agi envs.'
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel = 'ERR',
                             sessionID=get_session())
        sys.exit(1)

    if not env.has_key('agi_channel'):
        message = 'dsh_failed: no agi_channel.'
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel = 'ERR',
                             sessionID=get_session())
        sys.exit(1)

    if env['agi_channel'] != 'OutgoingSpoolFailed':
        message = 'dsh_failed: unexpected agi_channel: ' + env['agi_channel']
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel = 'ERR',
                             sessionID=get_session())
        sys.exit(1)

    dsh_config.init(env)


    #
    # get the dsh_uid of the callee from the command argument.
    #
    dsh_utils.db_print('dsh_failed: arguments are: ' + repr(sys.argv), 116)
    if len(sys.argv) < 2:
        message = 'dsh_failed: not enough arguments.'
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel = 'ERR',
                             sessionID=get_session())
        sys.exit(1)

    calleeDshUid = sys.argv[1].strip()
    if not calleeDshUid:
        message = 'dsh_failed: no dshUid found.'
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel = 'ERR',
                             sessionID=get_session())
        sys.exit(1)
    
    dsh_utils.db_print('dsh_failed: calleeDshUid: ' + calleeDshUid, 116)
    globals4signal['callee_dsh_uid'] = calleeDshUid


    #
    # let's sever ties with Asterisk.
    # this ensures the old .call file is deleted.
    #
    signal.signal(signal.SIGHUP, hangup_signal_handler)
    dsh_agi.send_command('HANGUP\n', caller='dsh_failed:')
    
    sys.exit(0)
    

    
if __name__ == '__main__':
    main()
