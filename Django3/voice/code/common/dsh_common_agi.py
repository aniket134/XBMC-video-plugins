#!/usr/bin/python -u
#
# broken out from dsh_agi.py (09/12/31)
# 

import logging,sys,re,time,random,os,os.path,datetime
import dsh_common_config,dsh_common_utils,dsh_common_db

dsh_common_utils.add_to_sys_path(dsh_common_config.lookup('django_sys_paths'))
__import__(dsh_common_config.lookup('APP_NAME_MODELS'))
import dsh_agi,dsh_config,dsh_utils
os.environ['DJANGO_SETTINGS_MODULE'] = dsh_common_config.lookup(
    'DJANGO_SETTINGS_MODULE')
import dsh_db_config,dsh_django_utils



def say_date(item):
    """called by dsh_django2.test_call_say_time(), and
    dsh_django2.say_person_name().
    """

    time = item.modify_datetime
    
    soundDir = dsh_common_config.lookup('DSH_PROMPT_DIR')
    datesDir = os.path.join(soundDir, 'dates')
    
    thisMessage = os.path.join(datesDir, 'this_message')
    wasRecorded = os.path.join(datesDir, 'was_recorded')
    
    dateDir = os.path.join(datesDir, 'dates')
    monthDir = os.path.join(datesDir, 'months')
    yearDir = os.path.join(datesDir, 'year')

    yStr = time.strftime('%#y')
    mStr = time.strftime('%#m')
    dStr = time.strftime('%#d')

    testDate = os.path.join(dateDir, dStr)
    testMonth = os.path.join(monthDir, mStr)
    testY2k = os.path.join(yearDir, '2000')
    testYear = os.path.join(dateDir, yStr)

    dsh_agi.say_it(thisMessage)
    dsh_agi.say_it(testDate)
    dsh_agi.say_it(testMonth)
    dsh_agi.say_it(testY2k)
    dsh_agi.say_it(testYear)
    dsh_agi.say_it(wasRecorded)



def chop_prefix_digits_for_local(callNum, callee):
    """
    10/02/02: chopping of the leading zero is moved from
    dsh_django_utils.generate_dot_call_file().
    also adding code to remove 0522.
    """

    dsh_common_db.init_log(quiet=True)

    #if callee.phone_std:
        #
        # 10/03/13:
        # dial as is.
        #
        #return callNum

    dsh_utils.db_print(
        'chop_prefix_digits_for_local: enter: callNum: ' + callNum, 152)
    if len(callNum) > 1 and (not callee.phone_std) and \
       (not callee.phone_landline) and callNum[0] == '0' and \
       (callNum[1] == '9' or callNum[1] == '8'):
        #
        # it looks like Asterisk doesn't like the leading 0
        # for cell phone numbers, chop it off.
        # 10/03/14:
        # now dealing with phone numbers that start with 8.
        #
        callNum = callNum[1:]
        dsh_utils.db_print(
            'chop_prefix_digits_for_local: return1: callNum: ' + callNum, 152)
        return callNum

    localLandLinePrefix = dsh_db_config.get('local_land_line_prefix')
    if not localLandLinePrefix:
        message = 'chop_prefix_digits_for_local: no local land line prefix.'
        dsh_utils.give_bad_news(message, logging.warning)
        dsh_agi.report_event(message, reportLevel='WRN')
        #
        # try_remove_prefix() will deal with null prefix
        # so no need to worry about anything else than logging message.

    #
    # 10/03/14:
    # should look at the callee.phone_landline flag.
    # but I'm not: it's still legit to look for 0522 and kill it
    # even if it was not explicitly marked as a landline.
    #
    callNum = try_remove_prefix(callNum, localLandLinePrefix)

    dsh_utils.db_print(
        'chop_prefix_digits_for_local: returned ' + callNum, 152)
    return callNum



def try_remove_prefix(phoneNum, prefix):
    """
    called by chop_prefix_digits_for_local() above.
    does phoneNum have a leading 0?  if not, try adding one.
    does prefix have a leading 0?  if not, try adding one.
    chop off the prefix if there's a match.
    if there's no match, do nothing to phoneNum
    """

    original = phoneNum

    if not prefix:
        return original
    
    l1 = len(phoneNum)
    if l1 < 2:
        #
        # I'm going to look at the first character so it better be at
        # at least that long.
        #
        return original

    if phoneNum[0] != '0':
        #
        # "normalize" the phone number, by adding a '0'
        #
        phoneNum = '0' + phoneNum

    l1 = len(phoneNum)

    if prefix[0] != '0':
        #
        # "normalize" the prefix too.
        #
        prefix = '0' + prefix

    l2 = len(prefix)
    
    if l1 <= l2:
        return phoneNum

    if phoneNum.startswith(prefix):
        phoneNum = phoneNum[l2:]
        dsh_utils.db_print(
            'try_remove_prefix: chopped to: ' + phoneNum, 139)
        return phoneNum

    #
    # there's no match, do nothing to the original number.
    #
    dsh_utils.db_print('try_remove_prefix: no chop: ' + original, 139)
    return original



def get_sln_path_for_asterisk(item, sessionID=None):
    return field_to_sln_path(item.file, sessionID=sessionID)



def field_to_sln_path(field, sessionID=None):
    """
    moved from dsh_django2.py
     fix up the file name: from the database, it's an mp3 URL.
     django should have taken the trouble of converting it to sln alredy.
     we call some function to get the path name of the sln file.
    """
    
    #mp3FilePath = item.file.url
    mp3FilePath = field.url
    pathStuff = dsh_agi.figure_out_sln_names(mp3FilePath)
    if not pathStuff:
        message = 'dsh_django1.get_sln_path_for_asterisk: ' + \
                  'failed to find path stuff for: ' + repr(mp3FilePath)
        dsh_agi.report_event(message, reportLevel='CRT',
                             sessionID=sessionID)
        dsh_utils.give_bad_news(message, logging.critical)
        return None
    slnDir,slnBaseName,wavBaseName,fullSlnName,fullWavName = pathStuff
    dsh_utils.db_print('dsh_django1.get_sln_path_for_asterisk: ' +
                       fullSlnName, 97)

    #
    # do a sanity check of the .sln file.
    #
    if not dsh_utils.is_valid_file(fullSlnName, msg='', silent=True):
        message = 'dsh_django.get_sln_path_for_asterisk: ' + \
                  'not a valid file: ' + fullSlnName
        dsh_agi.report_event(message, reportLevel='ERR',
                             sessionID=sessionID)
        dsh_utils.give_bad_news(message, logging.error)
        return None
    
    #
    # Asterisk doesn't like to be told the .sln extension so get rid of it.
    #
    chopped = fullSlnName.replace('.sln', '')
    dsh_utils.db_print('dsh_django1.get_sln_path_for_asterisk: success: ' +
                       chopped, 108)
    return chopped



def say_caller_name(caller, sayThisMessageIsForPath, sayFromPath,
                    endSentencePath=None):
    """called by dsh_django2.py.
    says the mp3 name of the caller if there is one.
    modeled after dsh_django2.say_person_name()
    """

    if not caller:
        return

    if not caller.spoken_name:
        return

    spokenName = field_to_sln_path(caller.spoken_name)
    if not spokenName:
        return

    #
    # "this message"
    #
    dsh_agi.say_it(sayThisMessageIsForPath)
    #
    # "Randy"
    #
    dsh_agi.say_it(spokenName)
    #
    # "is for"
    #
    dsh_agi.say_it(sayFromPath)

    if caller.organization and \
       caller.organization.spoken_name:
        placeSpokenName = field_to_sln_path(caller.organization.spoken_name)
    else:
        return

    dsh_agi.say_it(placeSpokenName)

    if endSentencePath:
        #
        # end of sentence thingie.
        #
        dsh_agi.say_it(endSentencePath)



def say_doctor_name(msg, sessionID=None, doctor=None):
    """
    called by check_personalized_message().
    give the personalized message sent by a doctor.
    the difference here is that no extra before and after snippets.
    we'll play the doctor's self-introduction by itself.
    modeled after say_caller_name().
    doctor is not None when called by dsh_django2.welcome_doctor().
    """

    if doctor:
        owner = doctor
    else:
        owner = msg.owner
        
    if not owner:
        return
    if not owner.spoken_name:
        return
    spokenName = field_to_sln_path(owner.spoken_name, sessionID=sessionID)
    if not spokenName:
        return
    dsh_agi.say_it(spokenName)    



def say_message_from_name(msg, sayThisMessagePath, sayIsFromPath,
                          endSentencePath=None):
    """
    like say_caller_name() above, which says the name of the caller.
    this one says who recorded the played message.
    originally was dsh_django2.say_person_name().
    but that one was tangled up in the old version where
    it said the intro-DSH message too.
    so I'm not messing with that any more.
    just starting anew.
    besides, it's supposed to use Hindi prompts as above.
    """

    say_caller_name(msg.owner, sayThisMessagePath, sayIsFromPath,
                    endSentencePath=endSentencePath)



def check_personalized_followup_to(caller, msg, sessionID,
                                   sayPersonNameFunc=None):
    """
    called by dsh_django2.check_personalized_messages().
    if the followup_to field of the personalized message points
    to caller himself, we want to play the original question
    that resulted in this personalized message.
    modeled after check_personalized_messages().
    sayPersonNameFunc is dsh_django2.say_message_from_name().
    """

    dsh_utils.db_print('check_personalized_followup_to: entered.', 151)
    if not msg or not caller or not msg.owner:
        dsh_utils.db_print('check_personalized_followup_to: nulls.', 151)
        return
    
    question = msg.followup_to
    if not question:
        dsh_utils.db_print('check_personalized_followup_to: no followup_to.',
                           151)
        return

    if question.owner.dsh_uid != caller.dsh_uid:
        #dsh_utils.db_print('check_personalized_followup_to: not same owner.',
        #                   151)
        #return
        pass

    if question.owner.ptype != 'USR':
        #
        # we will read the question back ONLY if the question
        # was left by a "user."
        #
        dsh_utils.db_print('check_personalized_followup_to: '+\
                           'question not by user type.', 151)
        return

    chopped = get_sln_path_for_asterisk(question)
    if not chopped:
        message = 'dsh_common_agi.check_personalized_followup_to: ' +\
                  'unable to find .sln file: ' + repr(question)
        dsh_agi.report_event(message, reportLevel='ERR', sessionID=sessionID)
        dsh_utils.give_bad_news(message, logging.error)
        return

    say_date(question)

    if sayPersonNameFunc:
        dsh_utils.db_print('check_personalized_followup_to: saying name.', 151)
        sayPersonNameFunc(question.owner)

    dsh_agi.say_it(chopped)
    dsh_agi.say_it('beep')



def auto_schedule_delete_all(force=False, sessionID=None):
    """
    moved from dsh_django_utils.py
    called by views.schedule_del_all().
    force=True when initiated by views.schedule_delete_all().
    """

    disableWipe = dsh_db_config.get('reschedule_wipe_disable')
    if not force and disableWipe:
        message = 'dsh_common_agi.auto_schedule_delete_all: ' +\
                  'note: wiping of existing schedule is disabled.'
        dsh_agi.report_event(message, sessionID=sessionID)
        return dsh_utils.black_break_msg(message)

    spoolDir = dsh_common_config.lookup('ASTERISK_DOT_CALL_DIR')
    if not dsh_utils.is_valid_dir(spoolDir, silence=True):
        message = 'dsh_common_agi.auto_schedule_delete_all: ' + \
                  'spool directory invalid: ' + spoolDir
        dsh_agi.report_event(message, reportLevel = 'CRT', sessionID=sessionID)
        return dsh_utils.red_error_break_msg(message)
    
    message = 'dsh_common_agi.auto_schedule_delete_all: ' +\
              'listdir() failed: ' + spoolDir
    try:
        listing = os.listdir(spoolDir)
        listing = dsh_common_db.filter_listdir_with_dbname(listing)
    except:
        dsh_agi.report_event(message, reportLevel = 'CRT', sessionID=sessionID)
        return dsh_utils.red_error_break_msg(message)

    message = dsh_utils.black_break_msg('deleting...')
    
    for one in listing:
        full = os.path.join(spoolDir, one)
        if not one:
            continue
        if os.path.isdir(full):
            continue
        if not dsh_utils.is_valid_file(full):
            continue
        if not one.endswith('.call'):
            continue

        dsh_utils.cleanup_path(
            full, 'dsh_common_agi.auto_schedule_delete_all: ')
        message += dsh_utils.black_break_msg(full)

    message += dsh_utils.black_break_msg('done.')
    return message



def person_has_any_message_at_all(caller, 
                                  itemTable, keyWordTable, eventTable,
                                  noLogging=False,
                                  sessionID=''):
    """
    10/03/30:
    called by somewhere from the signal handler in dsh_django2.py.
    called by remove_from_current_dial_if_no_message().
    modeled after dsh_django_utils.check_auto_timed_calls_for_person().
    same idea, except we won't actually put out .call files.
    the idea is this.
    we'll put people in the CDS.
    they get called once.
    if they have no message of any kind waiting for them,
    and they have signed up for auto-dial,
    and they picked up the phone,
    after this one call, we will remove them from the CDS.
    returns (hasMessage, strExplainReason)
    note100331
    """

    dsh_common_db.init_log(quiet=True)
    
    activeBroadcast = dsh_django_utils.should_auto_dial_broadcast(caller)
    if activeBroadcast and activeBroadcast.dummy:
        activeBroadcast = None

    if activeBroadcast:
        return (True, 'broadcast')

    #
    # 10/03/31:
    # the peer-shared issue need to be thought through for doctors.
    # right now, we don't have peer-shared messages,
    # so we don't much care.
    #
    peerShared = dsh_common_db.should_auto_dial_for_peer_share(
        caller, itemTable, keyWordTable, eventTable,
        noLogging=True, sessionID=sessionID)

    if peerShared:
        return (True, 'peer-shared')

    hasPersonal = dsh_common_db.person_has_personalized_message(
        caller, eventTable)

    if hasPersonal:
        return (True, 'personalized')

    return (False, 'nothing')



def remove_from_current_dial_if_no_message(
    caller, itemTable, keyWordTable, eventTable,
    noLogging=False, sessionID=''):
    """
    called by somewhere from the signal handler in dsh_django2.py.
    see note100331.
    """
    
    dsh_common_db.init_log(quiet=True)

    if not caller.current_dial:
        dsh_utils.db_print('remove_from_current_dial_if_no_message: ' +\
                           'not in CDS.', 165)
        return
    
    hasMessage,whatStr = person_has_any_message_at_all(
        caller, itemTable, keyWordTable, eventTable,
        noLogging=noLogging, sessionID=sessionID)

    if hasMessage:
        dsh_utils.db_print('remove_from_current_dial_if_no_message: ' +\
                           'has messages: ' + whatStr, 165)
        return

    caller.current_dial = False

    try:
        caller.save(noLogging=noLogging)
    except:
        message = 'dsh_common_agi.remove_from_current_dial_if_no_message: ' +\
                  'failed to save person: ' + caller.dsh_uid
        dsh_django_utils.error_event(message, item=person, errorLevel='CRT')
        dsh_utils.give_bad_news(message, reportLevel='CRT')
        return

    message = 'dsh_common_agi.remove_from_current_dial_if_no_message: ' +\
              'removed from current dial: ' + caller.__unicode__()
    dsh_agi.report_event(
        message,
        action='RCDS',
        owner=caller,
        sessionID=sessionID)
    dsh_utils.give_news(message, logging.info)



def change_call_num_to_zoiper_test(callee, callNum):
    """
    10/04/09:
    called by dsh_django_utils.generate_dot_call_file().
    if I'm doing testing on home laptops,
    change the call number to a fellow laptop's Zoiper number.
    normally, it's just callee.phone_number.
    in the Zoiper case, it'll be something like:
    192.168.2.14:4569-753
    see models.py 10/04/09.
    """

    calleeNum = callee.phone_number
    physChannel = dsh_db_config.get('outgoing_channel')
    if not physChannel:
        return callNum
    if physChannel != dsh_config.lookup('FORWARD_OUTGOING_CHANNEL_IAX2'):
        return callNum
    zoiperNumber = dsh_db_config.get('zoiper_number')
    if not zoiperNumber:
        return callNum
    zoiperNumber = zoiperNumber.strip()
    return zoiperNumber
    


def say_digits(number):
    """
    10/04/09: called by read_back_caller_number().
    says the phone numbers
    """

    dsh_common_db.init_log(quiet=True)
    funcName = 'dsh_common_agi.say_digits:'
    number = number.strip()

    soundDir = dsh_common_config.lookup('DSH_PROMPT_DIR')
    sorrySound = dsh_config.lookup('DSH_PROMPT_SORRY')
    sorrySound = os.path.join(soundDir, sorrySound)
    
    if not number:
        dsh_agi.say_it(sorrySound)
        return

    try:
        inumber = int(number)
    except:
        message = '%s not a number: %s.' % (funcName, number)
        dsh_agi.report_event(message, reportLevel='ERR')
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.say_it(sorrySound)
        return

    datesDir = os.path.join(soundDir, 'dates')
    dateDir = os.path.join(datesDir, 'dates')

    for digit in number:
        digit = '0' + digit
        sound = os.path.join(dateDir, digit)
        dsh_agi.say_it(sound)



def demo_reply(itemTable, keyWordTable, eventTable,
               fromPhone=False, sessionID=''):
    """
    10/04/09.
    send a demo reply to the most recent caller.
    called by dsh_common_views.send_demo_reply_now() and
    dsh_common_test.test_demo_reply().
    fromPhone=True when invoked from the phone interface.
    False when invoked from the web interface.
    """
    dsh_common_db.init_log(quiet=True)
    response = ''
    recent,msg = dsh_common_db.get_most_recent_message(
        itemTable, sessionID=sessionID)
    response += msg
    success,msg = read_back_caller_number(
        recent, fromPhone=fromPhone, sessionID=sessionID)
    response += msg

    if not success:
        return (False, response)

    #
    # when called from dsh_common_test.test_demo_reply(),
    # it's initiated from the phone.  it will go through this and
    # "go all the way."
    # when it's called by dsh_common_views.send_demo_reply_now(),
    # it's initiated from the web interface.  it doesn't continue here.
    # it'll require a confirmation link, and it will continue in
    # demo_reply_prompt_confirm() where it meets the continuation of the
    # code below.
    #
    if fromPhone:
        demo_reply_prompt_confirm(
            recent, itemTable, keyWordTable, eventTable, sessionID=sessionID)
        
    return (True, response)



def read_back_caller_number(item, fromPhone=False, sessionID=''):
    """
    10/04/09: called by demo_reply().  read back the phone number of the
    most recent caller.
    """

    response = ''
    funcName = 'dsh_common_agi.read_back_caller_number:'
    
    caller = item.owner
    phoneNumber = caller.phone_number

    if not phoneNumber:
        message = '%s no phone number: %s.' % (funcName, caller.dsh_uid)
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='ERR', sessionID=sessionID)
        dsh_utils.give_bad_news(message, logging.error)
        return (False, response)

    message = 'Send an immediate reply to %s @ %s? ' %\
              (caller.__unicode__(), phoneNumber)
    message += '<a href="/senddemoreplyconfirmed/%s">Confirm</a>?' %\
               (item.dsh_uid,)
    response += dsh_utils.black_break_msg(message)

    if fromPhone:
        promptDir = dsh_common_config.lookup('DSH_PROMPT_DIR')
        last4 = dsh_common_config.lookup('DSH_PROMPT_DEMO_LAST4')
        dsh_agi.say_it(os.path.join(promptDir, last4))
        howManyDigits = dsh_config.lookup('HIDE_PHONE_DIGITS')
        lastDigits = phoneNumber[-howManyDigits:]
        dsh_utils.give_news(
            'demo to phone: %s, last 4 digits: %s.' %\
            (phoneNumber, lastDigits), logging.info)
        say_digits(lastDigits)

    return (True, response)
    


def say_goodbye():
    time.sleep(1)
    dsh_agi.say_it('auth-thankyou')
    dsh_agi.say_it('vm-goodbye')
    time.sleep(1)



def demo_reply_prompt_confirm(recent, itemTable, keyWordTable, eventTable,
                              sessionID=''):
    """
    10/04/09: called by demo_reply().
    modeled after dsh_django2.handle_staff_caller().
    """

    funcName = 'dsh_common_agi.demo_reply_prompt_confirm:'
    count = 0
    promptDir = dsh_common_config.lookup('DSH_PROMPT_DIR')
    demoPress1 = dsh_common_config.lookup('DSH_PROMPT_DEMO_PRESS1_SEND')
    demoPress1 = os.path.join(promptDir, demoPress1)
    timeOut1 = dsh_config.lookup('DSH_PROMPT_WAIT1')
    maxRetries = dsh_common_config.lookup2('STAFF_RETRIES')
    demoSending = dsh_common_config.lookup('DSH_PROMPT_DEMO_SENDING_IN8')
    demoSending = os.path.join(promptDir, demoSending)

    while True:
        count += 1

        if count > maxRetries:
            say_goodbye()
            return True

        choice = dsh_agi.get_digits(demoPress1, 1, timeOut=timeOut1)
        dsh_utils.db_print('%s the choice is: %s.' % (funcName, repr(choice)),
                           168)

        if choice == None or choice == '' or choice == '*':
            say_goodbye()
            return True

        if choice == '1':
            dsh_common_db.attempt_demo_reply_now(
                recent, itemTable, keyWordTable, eventTable,
                sessionID=sessionID)
            dsh_agi.say_it(demoSending)
            say_goodbye()
            return True

        continue

    return True




def make_dot_call_file(callee, sessionID=''):
    """
    10/04/10:
    called by dsh_common_db.attempt_demo_reply_now() and
    dsh_django2.dial_now().
    """

    now = datetime.datetime.now()
    wait = dsh_common_config.lookup2('DEMO_REPLY_DELAY')
    delta = datetime.timedelta(seconds=wait)
    callTime = now + delta
    success = dsh_django_utils.generate_dot_call_file(
        callee, callTime, None, dialNow=True, sessionID=sessionID)

    if success:
        response = dsh_utils.black_break_msg(
            'Calling %s @ %s...' % (callee.__unicode__(),
                                    callee.phone_number))
    else:
        response = dsh_utils.red_error_break_msg('Something wrong happened.')

    return (success, response)
    
