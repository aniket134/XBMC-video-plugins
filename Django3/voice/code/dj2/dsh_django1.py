#!/usr/bin/python -u

import sys,logging,os,signal,subprocess,datetime,time
import dsh_agi,dsh_utils,dsh_config,dsh_bizarro



#
# django-specific initializations.
#
os.environ['DJANGO_SETTINGS_MODULE'] = dsh_config.lookup(
    'DJANGO_SETTINGS_MODULE')
sys.path += dsh_config.lookup('django_sys_paths')
from dv2.db.models import Person,Organization,Item,Event



#
# global variables for the signal handler.
#
globals4signal = {}



def init_log():
    global globals4signal

    #
    # set up logging.
    #
    logdir = dsh_config.lookup('log_file_dir')
    logName = dsh_config.lookup('log_file_name')
    dsh_utils.check_logging(logdir, logName)
    dsh_utils.give_news('dsh_django1: entered --------------------',
                        logging.info)
    #dsh_agi.debug_event('dsh_django1: entered --------------------', 97)
    globals4signal['log_dir'] = logdir



def init_unknown_org_person():
    """if the database doesn't have a default unknown organization, make one.
    if the database doesn't have a default unknown person (for no number),
    make one."""

    #
    # see if we could find the unknown org.  if not, make one.
    #
    unknownOrgAlias = dsh_config.lookup('UNKNOWN_ORG_ALIAS')
    unknownOrgs = Organization.objects.filter(alias=unknownOrgAlias)
    if unknownOrgs:
        unknownOrg = unknownOrgs.latest()
        if len(unknownOrgs) > 1:
            message = 'dsh_django1.init_unknown_org_person: ' + \
                      'more than one unknown org found.'
            dsh_utils.give_news(message, logging.warning)
            dsh_agi.report_event(message, reportLevel='WRN')
        dsh_utils.db_print('dsh_django1: found existing unknown org.', 99)
    else:
        unknownOrg = Organization(
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
    unknownPersons = Person.objects.filter(
        first_name=unknownPersonName, phone_number=unknownNumber)
    if unknownPersons:
        unknownPerson = unknownPersons.latest()
        if len(unknownPersons) > 1:
            message = 'dsh_django1.init_unknown_org_person: ' + \
                      'more than one unknown person found.'
            dsh_utils.give_news(message, logging.warning)
            dsh_agi.report_event(message, reportLevel='WRN',
                                 phone_number=unknownPerson.phone_number)
        dsh_utils.db_print('dsh_django1: found existing unknown person.', 99)
    else:
        unknownPerson = Person(
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
                


def get_outgoing_voice_from_db():
    #
    # look up in the django database.
    # look for items that are "active" and are of the "broadcast" type.
    #
    activeBroadcastItems = Item.objects.filter(active=True, itype='B')
    if not activeBroadcastItems:
        message = 'dsh_django1.get_outgoing_voice_from_db: ' + \
                  'no currently active broadcast message.'
        dsh_agi.report_event(message, reportLevel='ERR')
        dsh_utils.give_bad_news(message, logging.error)
        return None
    
    item = activeBroadcastItems[0]
    dsh_utils.db_print('dsh_django1.get_outgoing_voice_from_db: ' +
                       repr(item), 97)

    chopped = get_sln_path_for_asterisk(item)
    if chopped == None:
        return None
        
    return (item,chopped)
    


def lookup_number_in_db(env, debugCheat=False):
    """lookup the caller info in the django database.  returns the tuple
    (pObj, phoneNumber)"""

    if debugCheat:
        env['agi_callerid'] = '06935237794'

    if not env.has_key('agi_callerid'):
        message = 'dsh_django1.lookup_number_in_db: ' + \
                  ' no phone number given by Asterisk.'
        dsh_utils.give_news(message, logging.info)
        dsh_agi.report_event(message, reportLevel='WRN')
        return None
    
    phoneNumber = env['agi_callerid']
    
    persons = Person.objects.filter(phone_number=phoneNumber)
    if not persons:
        message = 'dsh_django1.lookup_number_in_db: ' + \
                  ' phone number not found in database: ' + phoneNumber
        dsh_utils.give_news(message, logging.info)
        dsh_agi.report_event(message, reportLevel='WRN',
                             phone_number=phoneNumber)
        return (None, phoneNumber)

    if len(persons) > 1:
        message = 'dsh_django1.lookup_number_in_db: ' + \
                  'more than one person in the db has this number: ' + \
                  phoneNumber + \
                  ', the list of people are: ' + \
                  repr(persons)
        dsh_utils.give_news(message, logging.info)
        dsh_agi.report_event(message, reportLevel='INF',
                             phone_number=phoneNumber)

    #p = persons[0]
    p = persons.latest()
    answer = (p, phoneNumber)
    dsh_utils.db_print('dsh_django1.lookup_number_in_db: ' +
                       repr(answer), 98)
    return answer



def determine_unknown_caller(unknownOrg, unknownPerson,
                             phoneNumberLookupResult):
    """if the caller's phone number is not known at all, we say the caller is
    unknownPerson from the unknownOrg.
    if the caller's phone number is known but not in the database,
    we add the caller to the database, and make her belong to unknownOrg."""

    if not phoneNumberLookupResult:
        #
        # we don't know the guy's phone number.
        #
        return unknownPerson

    person,phoneNumber = phoneNumberLookupResult

    if person:
        return person

    #
    # we have a phone number. but the person is not in the database.
    # we should put the person in.
    #
    unknownPersonName = dsh_config.lookup('UNKNOWN_PERSON_NAME')
    newUnknownPerson = Person(
        first_name=unknownPersonName,
        phone_number=phoneNumber,
        organization=unknownOrg,
        ptype='OTH',
        gender='F',
        description="""This unknown caller was automatically added by Asterisk.""")
    newUnknownPerson.save()
    message = 'dsh_django1.determine_caller: ' + \
              'added unknown caller to database with number: ' + \
              phoneNumber
    dsh_utils.give_news(message, logging.info)
    dsh_agi.report_event(message, reportLevel='INF',
                         phone_number=phoneNumber)
    return newUnknownPerson



def hangup_signal_handler(signum, frame):
    """attempt to do file format conversion upon a hangup.
    from .wav to .mp3.
    after conversion, we put it in the django database."""
    
    dsh_utils.db_print2('dsh_django1.signal_handler: entered...', 101)


    #
    # get the name of the file that was just recorded.
    #
    if not globals4signal.has_key('in_file'):
        dsh_utils.give_news('dsh_django1.hangup_signal_handler: ' +
                            'hangup before recording.', logging.info)
        sys_exit(0)

    inputFile = globals4signal['in_file']


    #
    # the recorded format is wav? if not, we don't convert.
    #
    fileFormat = dsh_config.lookup('record_file_format')
    if fileFormat != 'wav':
        message = 'dsh_django1.hangup_signal_handler: ' + \
                  "can't convert non-wav file: " + inputFile
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel='ERR')
        sys_exit(1)


    #
    # does the .wav file exist and is it non-zero sized?
    #
    inputWav = inputFile + '.wav'
    success,bytes = dsh_utils.get_file_size(inputWav)
    if not success:
        message = 'dsh_django1.hangup_signal_handler: ' + \
                  'no input file to convert: ' + \
                  inputWav
        dsh_utils.give_news(message, logging.info)
        #
        # looks like we could get this far even if there's
        # a hangup before record.  that's because the
        # signal doesn't seem to be delivered fast enough.
        # so globals4signal['in_file'] gets set anyhow.
        #
        #dsh_agi.report_event(message, reportLevel='ERR')
        sys_exit(1)
    if bytes == 0:
        message = 'dsh_django1.hangup_signal_handler: ' + \
                  'inputfile size 0: ' + inputWav
        dsh_utils.give_news(message, logging.info)
        dsh_agi.report_event(message, reportLevel='WRN')
        sys_exit(1)

    dsh_utils.db_print2('dsh_django1.signal_handler: ready to convert: ' +
                        inputWav, 101)


    #
    # where's the lame binary?
    #
    lamePath = dsh_config.lookup('lame_location')
    if not dsh_utils.is_valid_file(lamePath,
                                   msg='dsh_django1.hangup_signal_handler:'):
        message = 'dsh_django1.hangup_signal_handler: ' + \
                  'need to install lame.'
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel='CRT')
        sys_exit(1)


    #
    # stdout and stderr redirected to the log directory.
    #
    stdLogs = dsh_bizarro.stdio_logs_open(globals4signal['log_dir'])
    if not stdLogs:
        sys_exit(1)
    stdout,stderr = stdLogs


    #
    # the conversion command should be:
    # lame --resample 22.05 -b 24 test.wav test4.mp3
    #
    mp3Quality = dsh_config.lookup('lame_mp3_quality')
    outputMp3 = inputFile + '.mp3'
    #command = ffmpegPath + ' -i ' + inputWav + mp3Quality + outputMp3
    command = lamePath + mp3Quality + inputWav + ' ' + outputMp3

    try:
        ret = subprocess.call(command, shell=True,
                              stdout=stdout, stderr=stderr)
    except:
        ret = -1
        
    if ret != 0:
        message = 'dsh_django1.signal_handler: ' + \
                  'error in format conversion: ' + \
                  command
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel='CRT')
        sys_exit(1)

    dsh_utils.give_news('dsh_django1.signal_handler: conversion success: ' +
                        command, logging.info)

    dsh_utils.chmod_tree2(outputMp3, recurse=False)
    
    if not dsh_utils.cleanup_path(inputWav, 'dsh_django1.signal_handler'):
        message = 'dsh_django1.signal_handler: ' + \
                  'failed to remove original wav: ' + \
                  inputWav
        dsh_utils.give_bad_news(message, logging.warning)
        dsh_agi.report_event(message, reportLevel='WRN')


    #
    # calculate some more fields for saving in the database.
    #
    callDur,recDur = calculate_durations()
    dsh_utils.db_print2('dsh_django1.signal_handler: durations are: ' +
                        str(callDur) + ', ' + str(recDur), 101)


    #
    # dirPrefix is: /u/rywang/phone_data/django/
    # chop that off.
    # so what's left is:  /media/voice/09/07/090729_215817_85983050_08935237794_unknown-org_no-name.mp3
    # no, need to chop of '/media/' as well!
    # otherwise deletes don't work!
    #
    dirPrefix = dsh_config.lookup('PHONE_DATA_DJANGO_PATH')
    choppedFileName = outputMp3.replace(dirPrefix, '/')
    #chopAbsURLPrefix = dsh_config.lookup('ABS_URL_PREFIX_CHOP')
    #choppedFileName = choppedFileName.replace(chopAbsURLPrefix, '')
    choppedFileName = dsh_agi.abs_url_to_relative(choppedFileName)
    dsh_utils.db_print2('dsh_django1.signal_handler: choppedFileName is: '+\
                        choppedFileName, 105)


    #
    # FINALLY save the object in the django database!
    #
    item = globals4signal['db_in_obj']
    item.file = choppedFileName
    item.call_duration = callDur
    item.rec_duration = recDur
    try:
        item.save()
        dsh_utils.db_print2('dsh_django1.signal_handler: item saved: ' +
                            choppedFileName, 101)
    except:
        message = 'dsh_django1.signal_handler: saving in django failed: ' + \
                  choppedFileName, 101
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT')
        sys_exit(1)

    #
    # no point continuing execution after hangup.
    #
    sys_exit(0)



def calculate_durations():
    #
    # compute the duration of the call.
    #
    if globals4signal.has_key('call_duration'):
        callDur = globals4signal['call_duration']
    else:
        endTime = datetime.datetime.now()
        startTime = globals4signal['start_time']
        delta = endTime - startTime
        seconds = delta.seconds
        dsh_utils.db_print('dsh_django1.sys_exit: call duration: ' +
                           str(seconds) + 's.', 95)
        callDur = seconds
        globals4signal['call_duration'] = seconds

    #
    # compute the duration of the recording.
    #
    if globals4signal.has_key('rec_duration'):
        recDur = globals4signal['rec_duration']
    elif globals4signal.has_key('start_record'):
        startRecord = globals4signal['start_record']
        delta = endTime - startRecord
        seconds = delta.seconds
        dsh_utils.db_print('dsh_django1.sys_exit: record duration: ' +
                           str(seconds) + 's.', 95)
        recDur = seconds
        globals4signal['rec_duration'] = seconds
    else:
        recDur = None

    return (callDur,recDur)
    
    

def sys_exit(code):
    """a wrapper for sys.exit(), logs one line before exiting."""

    callDur,recDur = calculate_durations()

    #
    # repeats the caller info: phone number, school, name.
    #
    if globals4signal.has_key('caller_dude'):
        caller = globals4signal['caller_dude']
        logStr = '|| ' + caller.phone_number + ' || ' + \
                 caller.organization.alias + ' || ' + \
                 caller.__unicode__() + ' || '

        if recDur == None or recDur == 0:
            #
            # we know there's a caller, but there's no recDur.
            # that means the person hung up before recording.
            # we'll put a call without recording in the event table.
            #
            event = Event(
                owner=caller,
                phone_number=caller.phone_number,
                action='CALL',
                etype='INF',
                call_duration=callDur,
                description='hangup before recording.')
            event.save()        
    else:
        logStr = ''

    logStr += str(callDur) + ' || '
    if recDur:
        logStr += str(recDur)

    dsh_utils.give_news('dsh_django1.sys_exit: ' + logStr, logging.info)
    sys.exit(code)



def determine_recorded_file_name(caller, outgoingItem):
    #
    # I need to make a new item because that's where the new dsh_uid is.
    #
    item = Item(
        owner=caller,
        itype='I',
        followup_to=outgoingItem)

    #
    # the name has to be computed for placing in the django database.
    # so it's not done lightly.
    #
    incomingFullName = dsh_agi.make_full_unique_filename(
        item.dsh_uid,
        '',
        phoneNumber=caller.phone_number,
        orgAlias=caller.organization.alias,
        name=caller.__unicode__(),
        startWithRoot=True,
        uploadType='asterisk')

    dirName = os.path.dirname(incomingFullName)
    if not dsh_utils.try_mkdir_ifdoesnt_exist(
        dirName, 'dsh_django1.determine_recorded_file_name: '):
        message = 'dsh_django1.dsh_utils.try_mkdir_ifdoesnt_exist failed: '+\
                  dirName
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT')
        return (item, None)

    dsh_utils.chmod_tree2(dirName, recurse=False)

    slnDir = os.path.join(dirName, 'sln')
    if not dsh_utils.try_mkdir_ifdoesnt_exist(
        slnDir, 'dsh_django1.determine_recorded_file_name: '):
        message = 'dsh_django1.dsh_utils.try_mkdir_ifdoesnt_exist failed: '+\
                  'on slnDir: ' + slnDir
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT')
        return (item, None)
    dsh_utils.chmod_tree2(slnDir, recurse=False)
    
    return (item,incomingFullName)



def get_sln_path_for_asterisk(item):
    """
     fix up the file name: from the database, it's an mp3 URL.
     django should have taken the trouble of converting it to sln alredy.
     we call some function to get the path name of the sln file.
    """
    
    mp3FilePath = item.file.url
    pathStuff = dsh_agi.figure_out_sln_names(mp3FilePath)
    if not pathStuff:
        message = 'dsh_django1.get_sln_path_for_asterisk: ' + \
                  'failed to find path stuff for: ' + repr(mp3FilePath)
        dsh_agi.report_event(message, reportLevel='CRT')
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
        dsh_agi.report_event(message, reportLevel='ERR')
        dsh_utils.give_bad_news(message, logging.error)
        return None
    
    #
    # Asterisk doesn't like to be told the .sln extension so get rid of it.
    #
    chopped = fullSlnName.replace('.sln', '')
    dsh_utils.db_print('dsh_django1.get_sln_path_for_asterisk: success: ' +
                       chopped, 108)
    return chopped



def check_personalized_messages(caller):
    """does this caller have any unheard personalized messages?"""

    #
    # does this caller have any personal messages intended for him?
    #
    messages = caller.message_for_me.all()
    dsh_utils.db_print('dsh_django1.check_personalized_message: msg: ' +\
                       repr(messages), 108)
    if not messages:
        return
    
    for msg in messages:
        #
        # the message needs to be "personalized" and it needs to be "active."
        #
        maybe_deactivate_personal_message(msg)
        if not msg.active:
            dsh_utils.db_print('not active.', 108)
            continue
        if msg.itype != 'P':
            dsh_utils.db_print('not personalized: ' + msg.itype, 108)
            continue

        #
        # has this caller heard this before?
        #
        heardEvents = Event.objects.filter(
            action='HERD', owner=caller.id, dsh_uid_concerned=msg.dsh_uid)
        if heardEvents:
            dsh_utils.db_print('already heard, skipping: ' + msg.dsh_uid, 108)
            continue

        #
        # find out the .sln file path name.
        #
        chopped = get_sln_path_for_asterisk(msg)
        dsh_utils.db_print(
            'dsh_django1.check_personalized_message: sln path: ' +\
            repr(chopped), 108)

        if not chopped:
            message = 'dsh_django1.check_personalized_message: ' +\
                      'unable to find .sln file: ' + repr(msg)
            dsh_agi.report_event(message, reportLevel='ERR')
            dsh_utils.give_bad_news(message, logging.error)
            continue

        #
        # now play the personalized message and compute how long it lasted.
        #
        beginTime = datetime.datetime.now()
        dsh_agi.say_it(chopped)
        endTime = datetime.datetime.now()
        time.sleep(1)
        deltaSeconds = (endTime - beginTime).seconds

        #
        # remember the fact that this caller has heard this message.
        #
        dsh_agi.report_event(
            'personalized message heard.',
            item=msg,
            action='HERD',
            phone_number=caller.phone_number,
            owner=caller,
            call_duration=deltaSeconds)
        dsh_utils.give_news('dsh_django1.check_personalized_message: heard: '+\
                            msg.dsh_uid, logging.info)

        #
        # if everyone has heard this personalized message,
        # we should just deactivate it.
        #
        maybe_deactivate_personal_message(msg)

        #
        # beep twice at the end of each message.
        #
        dsh_agi.say_it('beep')
        dsh_agi.say_it('beep')



def maybe_deactivate_personal_message(item):
    """if all the intended audience has heard this item,
    de-activate it."""
    allAudience = item.intended_audience.all()
    if not allAudience:
        dsh_utils.db_print('dsh_django1.maybe_deactivate_personal_message: '+\
                           item.dsh_uid, 108)
        return
    for caller in allAudience:
        heardEvents = Event.objects.filter(
            action='HERD',owner=caller.id, dsh_uid_concerned=item.dsh_uid)
        if not heardEvents:
            dsh_utils.db_print(
                'dsh_django1.maybe_deactivate_personal_message: ' +\
                'not heard by this caller yet: ' + caller.phone_number,
                108)
            return

    item.active = False
    item.save()
    message = 'dsh_django1.maybe_deactivate_personal_message: deactivated: '+\
              item.dsh_uid
    dsh_utils.give_news(message, logging.info)
    dsh_agi.report_event(message, item=item)


    
def main():
    global globals4signal

    globals4signal['start_time'] = datetime.datetime.now()

    init_log()

    #
    # find or create unknown org and unknown person.
    #
    try:
        unknownOrg,unknownPerson = init_unknown_org_person()
    except:
        message = 'dsh_django: init_unknown_org_person failed.'
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT')
        sys_exit(1)

    #
    # get the outgoing voice from the database.
    #
    answer = get_outgoing_voice_from_db()
    if not answer:
        sys_exit(1)
    outVobj,outgoingVoice = answer

    #
    # get the AGI environment variables.
    #
    env = dsh_agi.read_env()
    if env == {}:
        dsh_utils.give_bad_news('dsh_django1: failed to read agi envs.',
                                logging.error)
        sys_exit(1)

    #
    # look up the phone number in the django database.
    # if not found in the database, we do something about unknown callers.
    # XXX
    #lookupResult = lookup_number_in_db(env, debugCheat=True)
    lookupResult = lookup_number_in_db(env)
    caller = determine_unknown_caller(unknownOrg, unknownPerson, lookupResult)
    dsh_utils.db_print('dsh_django1: the caller determined to be: ' +
                       repr(caller), 100)
    globals4signal['caller_dude'] = caller
    
    #
    # setting up signal handler for hangup.
    # the handler will attempt to do the file format conversion.
    # and then saving into the django database.
    #
    signal.signal(signal.SIGHUP, hangup_signal_handler)


    #
    # check whether there're any personalized messages for this caller.
    #
    check_personalized_messages(caller)
    
    
    #
    # play the outgoing file.
    #
    # XXX
    dsh_agi.say_it(outgoingVoice)
    time.sleep(1)
    dsh_agi.say_it('beep')
    dsh_agi.say_it('beep')


    #
    # determine the input file name and record it.
    #
    inVobj,incomingFullName=determine_recorded_file_name(caller, outVobj)
    if incomingFullName == None:
        dsh_utils.give_bad_news(
            'dsh_django1: determine_recorded_file_name failed: ',
            logging.critical)
        sys_exit(1)
    dsh_utils.db_print('dsh_django1: incomingFullName: ' + incomingFullName,
                       101)
    globals4signal['db_in_obj'] = inVobj
    globals4signal['start_record'] = datetime.datetime.now()
    globals4signal['in_file'] = incomingFullName
    dsh_agi.record(incomingFullName)
    dsh_utils.db_print('dsh_django1: record call ends.', 101)
    time.sleep(1)
    dsh_utils.give_news('dsh_django1: recording done.')
    dsh_agi.say_it('auth-thankyou')
    dsh_agi.say_it('vm-goodbye')

    #
    # convert file format too with a proper hangup (pressing the # key).
    #
    hangup_signal_handler(0, None)

    

if __name__ == '__main__':
    main()
