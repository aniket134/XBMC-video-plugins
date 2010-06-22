#!/usr/bin/python -u
#
# mostly copied from the starfish book. (07/01/09)
# 

import logging,sys,re,time,random,dsh_utils,dsh_config,os,os.path



#
# django-specific initializations.
#
os.environ['DJANGO_SETTINGS_MODULE'] = dsh_config.lookup(
    'DJANGO_SETTINGS_MODULE')
dsh_utils.add_to_sys_path(dsh_config.lookup('django_sys_paths'))
#from dv2.db.models import Person,Organization,Item,Event
import dv2.db.models
import dsh_common_db



def console_message(message):
    """prints to the Asterisk console window.
    called by print routines in dsh_utils.py"""
    message = message.strip()
    message = message + '\n'
    sys.stderr.write(message);
    sys.stderr.flush()
    


def console_message_log(message, log_type=logging.info):
    """called by the various give_message() functions in dsh_utils.py"""
    console_message(message)
    if log_type:
        message = message.strip()
        log_type(message)



def split_line(line):
    """split the lines for agi env variables.
    this is written to deal with something like this:
    agi_channel: IAX2/127.0.0.1:35456-14868"""
    try:
        #
        # this splits at most once.
        #
        key,data = line.split(':',1)
        if key != '':
            return (True,key,data)
        return (False,None,None)
    except:
        return (False,None,None)
        


def read_env(consoleMsg=True):
    """reads AGI environment variables at the beginning of a call."""
    env = {}
    while 1:
        line = sys.stdin.readline().strip()
        if line == '':
            break

        
        #
        # ryw:
        # bad format. not splittable.
        # this is because I found a line that looks like this:
        # agi_channel: IAX2/127.0.0.1:35456-14868
        #
        #key,data = line.split(':')
        success,key,data = split_line(line)
        if not success:
            info = 'dsh_agi.read_env: bad line: ' + line
            dsh_utils.give_bad_news2(info, logging.warning)
            continue
            
        if key[:4] <> 'agi_':
            #skip input that doesn't begin with agi_
            info = 'dsh_agi.read_env: invalid key: ' + key[:4]
            dsh_utils.give_bad_news2(info, logging.warning)
            continue
        key = key.strip()
        data = data.strip()
        if key <> '':
            env[key] = data

    keys2skip = ['agi_rdnis', 'agi_uniqueid', 'agi_language', 'agi_callington',
                 'agi_callingtns', 'agi_accountcode', 
                 'agi_enhanced', 'agi_callingpres', 'agi_callingani2',
                 'agi_dnid', 'agi_rdnis', 'agi_priority']
                 
    if consoleMsg:
        info = "dsh_agi.read_env: AGI Environment Dump:"
        dsh_utils.give_news(info, logging.info)
        for key in env.keys():
            if key in keys2skip:
                continue
            info = " -- %s = %s" % (key, env[key])
            dsh_utils.give_news(info, logging.info)

    return env



def check_result(params, consoleMsg=True):
    """copied from the star fish book.  looking for number results.
    the Asterisk response looks like '200 result=1'.
    """
    params = params.rstrip()
    if re.search('^200',params):
        result = re.search('result=(\d+)',params)
        if (not result):
            if consoleMsg:
                info = "dsh_agi.check_result: FAIL ('%s')" % params
                dsh_utils.give_bad_news2(info, logging.error)
            return -1
        else:
            result = result.group(1)
            if consoleMsg:
                info = "dsh_agi.check_result: PASS (%s)" % result
                dsh_utils.give_good_news(info, logging.info)
            return result
    else:
        if consoleMsg:
            info = "dsh_agi.check_result: " + \
                   "FAIL (unexpected result '%s')" % params
            dsh_utils.give_bad_news2(info, logging.error)
        return -2



def check_result2(params, consoleMsg=True):
    """just like check_result() above, except the result can be non-digits.
    or even empty.
    """
    params = params.rstrip()
    if re.search('^200',params):
        result = re.search('result=(.*)',params)
        if result:
            return result.group(1)
        return ''
    else:
        if consoleMsg:
            info = "dsh_agi.check_result: " + \
                   "FAIL (unexpected result '%s')" % params
            dsh_utils.give_bad_news2(info, logging.error)
        return None



def send_command(command, caller="", consoleMsg=True):
    if consoleMsg:
        dsh_utils.give_news(caller + command)
    sys.stdout.write(command)
    sys.stdout.flush()
    result = sys.stdin.readline().strip()
    res = check_result(result, consoleMsg)
    return res



def send_command2(command, caller="", consoleMsg=True):
    """just like send_command(), except it uses check_result2(),
    instead of check_result().  allows non-digit results.
    """
    if consoleMsg:
        dsh_utils.give_news(caller + command)
    sys.stdout.write(command)
    sys.stdout.flush()
    result = sys.stdin.readline().strip()
    res = check_result2(result, consoleMsg)
    return res



def say_it(params, consoleMsg=True):
    #command = "STREAM FILE %s \"\"\n" % str(params)
    stopButton = dsh_config.lookup('play_stop_key')
    command = "STREAM FILE %s \"%s\"\n" % (str(params), stopButton)
    res = send_command(command, "dsh_agi.sayit: ", consoleMsg)
    return res
        


def record(fileName, consoleMsg=True, allowStopButton=False, stopButton=''):
    timeLimit = dsh_config.lookup('record_time_limit')
    if not stopButton:
        stopButton = dsh_config.lookup('record_stop_key')
    fileFormat = dsh_config.lookup('record_file_format')

    #
    # 10/04/04:
    # revive the stop button, to allow doctors to loop over questions.
    #
    if allowStopButton:
        command = 'RECORD FILE ' + fileName + ' ' + fileFormat + ' ' + \
                  stopButton + ' ' + str(timeLimit) + '\n'
    else:
        #
        # no stop button!
        # it seems to be causing trouble!
        #
        command = 'RECORD FILE ' + fileName + ' ' + fileFormat + ' ' + \
                  '""' + ' ' + str(timeLimit) + '\n'
    res = send_command(command, 'dsh_agi.record: ', consoleMsg)
    return res



def exec_com_test(consoleMsg=True):
    command = 'EXEC Monitor wav|/tmp/recordast2|m\n'
    res = send_command(command, 'dsh_agi.exec_com: ', consoleMsg)
    command = 'EXEC Dial IAX2/192.168.2.7:4569-2531\n'
    res = send_command(command, 'dsh_agi.exec: ', consoleMsg)
    return res



def get_digits_test(consoleMsg=True):
    command = 'GET DATA conf-getconfno 10000 10\n'
    result = send_command2(command, 'dsh_agi.get_digits: ', consoleMsg)
    return result



def get_digits(voicePrompt, numDigits, timeOut=10000, consoleMsg=True):
    timeOut = str(timeOut)
    numDigits = str(numDigits)
    command = 'GET DATA %s %s %s\n' % (voicePrompt, timeOut, numDigits)
    result = send_command2(command, 'dsh_agi.get_digits: ', consoleMsg)
    time.sleep(1)
    return result



def forward_call(fileName, callNum, consoleMsg=True, testCheat=False):
    fileFormat = dsh_config.lookup('record_file_format')
    command = 'EXEC Monitor %s|%s|m\n' % (fileFormat, fileName)
    res = send_command(command, 'dsh_agi.exec_com: ', consoleMsg)
    #channel = dsh_config.lookup('FORWARD_OUTGOING_CHANNEL')
    channel = dsh_common_db.get_forward_outgoing_channel()
    
    if testCheat and dsh_config.lookup('BARNEY_TEST'):
        callNum = dsh_config.lookup('BARNEY_TEST_JUNIOR_ZOIPER')
        
    command = 'EXEC Dial %s/%s\n' % (channel, callNum)
    #command = 'EXEC Dial %s/%s 60 of\n' % (channel, callNum)
    res = send_command(command, 'dsh_agi.forward_call: ', consoleMsg)
    command = 'EXEC StopMonitor\n'
    res = send_command(command, 'dsh_agi.forward_call: ', consoleMsg)
    return res
                


def check_dot_call_num(agiEnv):
    """called by dsh_django2.lookup_number_in_db().
    check to see if this is the result of a .call file.
    if yes, you have something like:
    agi_calleridname = __DOT_CALL__ phoneNum
    returns (found, phoneNum)
    """

    if not agiEnv.has_key('agi_calleridname'):
        return (False, None)

    callerIdName = agiEnv['agi_calleridname']
    prefixToCheck = dsh_config.lookup('DOT_CALL_INDICATOR')
    if not callerIdName.startswith(prefixToCheck):
        return (False, None)

    chopped = callerIdName.replace(prefixToCheck, '')
    chopped = chopped.strip()
    return (True, chopped)




############################################################
# the stuff above is about AGI.
# the stuff is more about interacting with django.
############################################################

def make_unique_voice_filename_asterisk(dshUid, phoneNumber, orgAlias, name):
    """file name made for voices recorded by asterisk.
    it looks like this:
    090727_195346_88888888_12356_orgalias_pname_test4.mp3
    """
    hiddenPhoneNumber = hide_phone_digits(phoneNumber)
    hiddenPhoneNumber = hiddenPhoneNumber.replace('x','')
    answer = dshUid + '_' + \
             hiddenPhoneNumber + '_' + \
             orgAlias + '_' + \
             name 
    return dsh_utils.strip_join_str(answer)



def make_unique_voice_filename_django(dshUid, uploadedFileName):
    """file name made for voices recorded by django.
    it looks like this:
    090727_195346_88888888_test4.mp3
    """
    answer = dshUid + '_' + uploadedFileName
    return dsh_utils.strip_join_str(answer)



def make_unique_image_filename_django(dshUid, name, uploadedFileName):
    """file name made for voices recorded by django.
    it looks like this:
    090727_195346_88888888_name_me.jpg
    """
    answer = dshUid + '_' + name + '_' + uploadedFileName
    return dsh_utils.strip_join_str(answer)



def make_full_unique_filename(dshUid,
                              uploadedFileName,
                              phoneNumber='',
                              orgAlias='',
                              name='',
                              startWithRoot=False,
                              uploadType='django_voice'):
    """when called by Asterisk, startWithRoot=True
    when called by django, startWithRoot=False.
    for django, it looks like this:
    voice/09/07/090727_195346_88888888_test4.mp3
    for asterisk, it looks like this:
    /u/rywang/phone_data/django/media/voice/09/07/090727_195346_88888888_123_alias_name_test4.mp3
    """

    if uploadedFileName:
        uploadedFileName = dsh_utils.strip_join_str(uploadedFileName)

    #
    # first determine the upper-level directory.
    # 
    if startWithRoot:
        #
        # called by Asterisk.
        # it's this: /u/rywang/phone_data/django/media/voice/
        # like:
        # /u/rywang/phone_data/django/media/voice/
        # or
        # voice/
        #
        inDir = dsh_config.lookup('VOICE_DIR')
    else:
        #
        # called by django.
        # from dsh_django_utils.py
        # it's this: voice/
        #
        if uploadType == 'django_voice':
            inDir = dsh_config.lookup('VOICE_SUBDIR')
        elif uploadType == 'django_image':
            inDir = dsh_config.lookup('IMG_SUBDIR')
        else:
            return None


    #
    # mid-level directory named after year and month.
    # like
    # 09/07/
    #
    dateStrFormat = dsh_config.lookup('DATE_FORMAT_DIR_STR')
    yearMonthSubDir = dsh_utils.get_misc_dict()['now'].strftime(dateStrFormat)


    #
    # finally leaf-level file name.
    #
    if uploadType == 'asterisk':
        #
        # this is called by asterisk.
        #
        fileName = make_unique_voice_filename_asterisk(
            dshUid, phoneNumber, orgAlias, name)
    elif uploadType == 'django_image':
        #
        # called by dsh_django_utils.make_uploaded_image_name()
        #
        fileName = make_unique_image_filename_django(
            dshUid, name, uploadedFileName)
    elif uploadType == 'django_voice':
        #
        # called by dsh_django_utils.make_uploaded_file_name()
        #
        fileName = make_unique_voice_filename_django(
            dshUid, uploadedFileName)
    else:
        return None
    
    return os.path.join(inDir, yearMonthSubDir, fileName)



#
# figure out the sln dir, given a parent dir.
# called by dsh_django_utils.py to convert to sln.
# called by asterisk side to play it.
# returns (slnDir, slnBaseName, wavBaseName, fullSlnName, fullWavName)
#
def figure_out_sln_names(mp3FilePath):
    mp3FilePath = make_abs_file_pathname(mp3FilePath)
    containingDir = os.path.dirname(mp3FilePath)
    mp3baseName = os.path.basename(mp3FilePath)
    slnDir = os.path.join(containingDir, 'sln')

    if mp3baseName.endswith('.mp3'):
        headName = mp3baseName.replace('.mp3', '')
    elif mp3baseName.endswith('.MP3'):
        headName = mp3baseName.replace('.MP3', '')
    else:
        return None

    slnBaseName = headName + '.sln'
    wavBaseName = headName + '.wav'

    fullSlnName = os.path.join(slnDir, slnBaseName)
    fullWavName = os.path.join(slnDir, wavBaseName)

    return (slnDir, slnBaseName, wavBaseName, fullSlnName, fullWavName)



def debug_event(message, tag, sessionID=''):
    currentPrintTag = dsh_utils.RYW_DEBUG_TAG
    if tag != currentPrintTag:
        return
    if not sessionID:
        sessionID = ''
    event = dv2.db.models.Event(
        etype = 'DBG', action = 'PRNT', debug_tag = tag, session=sessionID)
    event.description = message
    event.save()



def report_event(message, reportLevel='INF', item=None, action='RPRT',
                 phone_number='', owner=None, call_duration=0,
                 sessionID='', rec_duration=0, dsh_uid2=''):

    #
    # 10/03/26:
    # fake dummy empty broadcast need not be logged.
    #
    if action == 'HERD' and item and item.itype == 'B' and item.dummy:
        return
    
    if item:
        dsh_uid = item.dsh_uid
    else:
        dsh_uid = ''

    if not sessionID:
        sessionID = ''
    
    event = dv2.db.models.Event(etype = reportLevel,
                                   action = action,
                                   dsh_uid_concerned=dsh_uid,
                                   phone_number=phone_number,
                                   session=sessionID)
    if owner != None:
        event.owner = owner
        event.phone_number = owner.phone_number
    if call_duration != 0:
        event.call_duration = call_duration
    if rec_duration != 0:
        event.rec_duration = rec_duration
    if dsh_uid2:
        event.dsh_uid2 = dsh_uid2
        
    event.description = message
    event.save()



def make_abs_file_pathname(url):
    #
    # get the file path.
    # path_prefix: /home/rywang/phone_data/django/
    # url: /media/voice/2009/07/test4_________.mp3
    # concatenate these two.
    #
    path_prefix = dsh_config.lookup('PHONE_DATA_DJANGO_PATH')
    strippedUrl = url.lstrip('/')
    filePath = os.path.join(path_prefix, strippedUrl)
    return filePath



def hide_phone_digits(phone):
    if phone == '':
        return ''
    hideDigits = dsh_config.lookup('HIDE_PHONE_DIGITS')
    l = len(phone)
    if (l <= hideDigits):
        return ''.rjust(l, 'x')
    return phone[:(l-hideDigits)] + 'xxxx'



def abs_url_to_relative(url):
    """turns '/media/voice/blah/blah' into 'voice/blah/blah'.
    called by dsh_django1.py.
    and dsh_dump.py.
    """
    chopAbsURLPrefix = dsh_config.lookup('ABS_URL_PREFIX_CHOP')
    url = url.replace(chopAbsURLPrefix, '')
    url = url.lstrip('/')
    return url



def url_to_fs_path(url):
    relUrl = abs_url_to_relative(url)
    fsPath = os.path.join(dsh_config.lookup('MEDIA_DIR'), relUrl)
    return fsPath



def init_log():
    logdir = dsh_config.lookup('log_file_dir')
    logName = dsh_config.lookup('log_file_name')
    dsh_utils.check_logging(logdir, logName)



def init_unknown_org_person(sessionID=''):
    """moved from dsh_django2.
    if the database doesn't have a default unknown organization, make one.
    if the database doesn't have a default unknown person (for no number),
    make one."""

    #
    # see if we could find the unknown org.  if not, make one.
    #
    unknownOrgAlias = dsh_config.lookup('UNKNOWN_ORG_ALIAS')
    unknownOrgs = dv2.db.models.Organization.objects.filter(
        alias=unknownOrgAlias)
    if unknownOrgs:
        unknownOrg = unknownOrgs.latest()
        if len(unknownOrgs) > 1:
            message = 'dsh_django1.init_unknown_org_person: ' + \
                      'more than one unknown org found.'
            dsh_utils.give_news(message, logging.warning)
            report_event(message, reportLevel='WRN', sessionID=sessionID)
        dsh_utils.db_print('dsh_django1: found existing unknown org.', 99)
    else:
        unknownOrg = dv2.db.models.Organization(
            name='Unknown Organization',
            alias=unknownOrgAlias,
            language='OTH',
            description="""This is a place holder organization for unknown callers, automatically added by Asterisk.""")
        unknownOrg.save()
        dsh_utils.db_print('dsh_django1: created new unknown org.', 99)

    dsh_utils.db_print('dsh_django1: unknownOrg: ' + repr(unknownOrg), 99)

    #
    # see if we could find the unknown person.  if not, make one.
    #
    unknownNumber = dsh_config.lookup('UNKNOWN_PHONE_NUMBER')
    unknownPersonName = dsh_config.lookup('UNKNOWN_PERSON_NAME')
    unknownPersons = dv2.db.models.Person.objects.filter(
        first_name=unknownPersonName, phone_number=unknownNumber)
    if unknownPersons:
        unknownPerson = unknownPersons.latest()
        if len(unknownPersons) > 1:
            message = 'dsh_django1.init_unknown_org_person: ' + \
                      'more than one unknown person found.'
            dsh_utils.give_news(message, logging.warning)
            report_event(message, reportLevel='WRN',
                         phone_number=unknownPerson.phone_number,
                         sessionID=sessionID)
        dsh_utils.db_print('dsh_django1: found existing unknown person.', 99)
    else:
        unknownPerson = dv2.db.models.Person(
            first_name=unknownPersonName,
            phone_number=unknownNumber,
            organization=unknownOrg,
            ptype='OTH',
            gender='F',
            description="""This is the place-holder person for callers whose phone numbers we don't know, automatically added by Asterisk.""")
        unknownPerson.save()
        dsh_utils.db_print('dsh_django1: created new unknown person.', 99)

    dsh_utils.db_print('dsh_django1: unknownPerson: ' + repr(unknownPerson),
                       99)

    return (unknownOrg,unknownPerson)
