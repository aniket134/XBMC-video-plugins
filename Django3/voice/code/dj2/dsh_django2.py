#!/usr/bin/python -u

import sys,logging,os,signal,subprocess,datetime,time, random
import dsh_agi,dsh_utils,dsh_config,dsh_bizarro



#
# django-specific initializations.
#
os.environ['DJANGO_SETTINGS_MODULE'] = dsh_config.lookup(
    'DJANGO_SETTINGS_MODULE')
dsh_utils.add_to_sys_path(dsh_config.lookup('django_sys_paths'))
from dv2.db.models import Person,Organization,Item,Event,KeyWord
import dv2.db.models
import dsh_django_utils,dsh_db_config
import dsh_common_config
dsh_common_config.init(dsh_config)
import dsh_common_agi,dsh_common_test,dsh_common_db



#
# global variables for the signal handler.
#
# list of global variables used:
#
#   log_dir: for putting stdio and stderr logs, for file conversion.
#   dot_call_initiated: for re-arming an auto-dial, is the caller object.
#   in_file: recorded .wav file.
#   db_in_obj: the item to be saved in db: it was made early to get dsh_uid.
#   callee_dude: for synchronous callee put in item.
#   call_duration: if it were computed earlier.
#   start_time: for computing call duration.
#   rec_duration: if it were computed earlier.
#   start_record: for computing recorded duration.
#   caller_dude: for logging in sys_exit().
#   db_out_obj: the item that was played, for computing whether a partially
#       heard message and hung-up message should be considered "heard."
#   begin_play_time: for calculating whether it should be considered
#       partially heard.
#   dsh_said: used by say_person_name(), say DSH once.
#   playing_own_msg: set by play_own_peer_shared, to see if hung up
#       whether we should use a smaller threshold for being considered heard.
#   session_id: set at the beginning, and used throughout for logging.
#   doctor_record: if it's a doctor recording an answer, we may need to put
#       an event in the database indicating the question has been answered.
#   doctor_message_list_cache: caching the list of messages eligible to be
#       heard by a doctor in one go.  removing the ones that just got heard.
#
globals4signal = {}
globals4signal['dsh_said'] = False
globals4signal['playing_own_msg'] = False
globals4signal['session_id'] = ''
globals4signal['doctor_record'] = False



#
# this is for dsh_timed.py
#
def set_global(which, value):
    global globals4signal
    globals4signal[which] = value



def get_session():
    global globals4signal
    return globals4signal['session_id']



def init_log(msg=None):
    global globals4signal
    #
    # set up logging.
    #
    logdir = dsh_config.lookup('log_file_dir')
    logName = dsh_config.lookup('log_file_name')
    dsh_utils.check_logging(logdir, logName)
    if msg == None:
        msg = 'dv2/dsh_django2: entered, session: %s --------------------' % \
              (get_session(),)
    dsh_utils.give_news(msg, logging.info)
    globals4signal['log_dir'] = logdir



def say_first_prompt(sayDSH=True):
    global globals4signal

    promptDir = dsh_config.lookup('DSH_PROMPT_DIR')
    
    #
    # say this is DSH
    #
    if sayDSH and not globals4signal['dsh_said']:
        dshVoice = os.path.join(
            promptDir, dsh_config.lookup('DSH_PROMPT_DSH_VOICE'))
        dsh_utils.db_print('say_person_name: say dsh prompt.', 148)
        dsh_agi.say_it(dshVoice)
        globals4signal['dsh_said'] = True
    


def say_caller_name(caller):
    """
    it says:
    this message +
    randy +
    is for +
    DSH +
    endSentence
    """
    
    promptDir = dsh_config.lookup('DSH_PROMPT_DIR')
    sayThisMessageIsForPath = os.path.join(
        promptDir, dsh_config.lookup('DSH_PROMPT_MESSAGE_FOR'))
    sayFromPath = os.path.join(
        promptDir, dsh_config.lookup('DSH_PROMPT_FROM'))
    endSentencePath = os.path.join(
        promptDir, dsh_config.lookup('DSH_PROMPT_END_SENTENCE'))
    dsh_common_agi.say_caller_name(caller,
                                   sayThisMessageIsForPath,
                                   sayFromPath,
                                   endSentencePath=endSentencePath)



def say_message_from_name(caller):
    """
    it says:
    this message +
    randy +
    is from +
    DSH +
    endSentence
    
    like say_caller_name() above, which says the name of the caller.
    this one says who recorded the played message.
    originally was dsh_django2.say_person_name().
    but that one was tangled up in the old version where
    it said the intro-DSH message too.
    so I'm not messing with that any more.
    just starting anew.
    besides, it's supposed to use Hindi prompts as above.
    """
    promptDir = dsh_config.lookup('DSH_PROMPT_DIR')
    sayThisMessageIsForPath = os.path.join(
        promptDir, dsh_config.lookup('DSH_PROMPT_MESSAGE_FOR'))
    sayFromPath = os.path.join(
        promptDir, dsh_config.lookup('DSH_PROMPT_FROM2'))
    endSentencePath = os.path.join(
        promptDir, dsh_config.lookup('DSH_PROMPT_END_SENTENCE'))
    dsh_common_agi.say_caller_name(caller,
                                   sayThisMessageIsForPath,
                                   sayFromPath,
                                   endSentencePath=endSentencePath)

        

def say_person_name(shared, sayDSH=True):
    """called by handle_regular_caller().
    say the person's and the organization's spoken names."""

    global globals4signal

    dsh_utils.db_print('say_person_name: entered.', 148)

    promptDir = dsh_config.lookup('DSH_PROMPT_DIR')
    
    #
    # say this is DSH
    #
    say_first_prompt(sayDSH=sayDSH)

    #
    # 10/02/24:
    # disable everything below.
    # disable saying whom it's from,
    # and when it was recorded.
    #
    return


    #
    # say "a message by"
    #
    messageBy = os.path.join(
        promptDir, dsh_config.lookup('DSH_PROMPT_MESSAGE_BY'))
    dsh_agi.say_it(messageBy)

    #
    # say the teacher name.
    #
    personSpoken = None
    if shared.owner and shared.owner.spoken_name:
        personSpoken = field_to_sln_path(shared.owner.spoken_name)

    if not personSpoken:
        personSpoken = os.path.join(
            promptDir, dsh_config.lookup('DSH_PROMPT_A_TEACHER'))
    dsh_agi.say_it(personSpoken)

    #
    # say "from schoolname"
    #
    if shared.owner and shared.owner.organization and \
       shared.owner.organization.spoken_name:
        orgSpoken = field_to_sln_path(shared.owner.organization.spoken_name)
        fromSchool = os.path.join(
            promptDir, dsh_config.lookup('DSH_PROMPT_FROM'))
        school = os.path.join(
            promptDir, dsh_config.lookup('DSH_PROMPT_SCHOOL'))
        dsh_agi.say_it(fromSchool)
        dsh_agi.say_it(orgSpoken)    
        dsh_agi.say_it(school)
        
    #
    # say when the message was made.
    # 
    dsh_common_agi.say_date(shared)



def play_own_peer_shared(caller):
    """modeled afer get_peer_shared().
    get the peer-shared message previously recorded by this caller
    herself."""

    global globals4signal

    #sharedList = Item.objects.filter(peer_shared=True, owner=caller)
    sharedList = dsh_common_db.get_peer_shared_item_for_caller(
        caller, Item, KeyWord, get_session(), getOwn=True)
    if not sharedList:
        return None

    pick = None
    
    for shared in sharedList:
        heardEvents = Event.objects.filter(
            action='HERD', owner=caller.id, dsh_uid_concerned=shared.dsh_uid)
        if heardEvents:
            dsh_utils.db_print(
                'dsh_django2.play_own_peer_shared: heard: ' + shared.dsh_uid,
                121)
            continue
        pick = shared
        break

    if not pick:
        return None

    chopped = get_sln_path_for_asterisk(pick)
    if not chopped:
        message = 'dsh_django2.play_own_peer_shared: ' +\
                  'get_sln_path_for_asterisk failed: ' + repr(pick)
        dsh_agi.report_event(message, reportLevel='ERR',
                             sessionID=get_session())
        dsh_utils.give_bad_news(message, logging.error)
        return None    
    
    dsh_utils.db_print('dsh_django2.play_own_peer_shared: chopped sln: ' +\
                       chopped, 121)
    dsh_utils.give_news('dsh_django2.play_own_peer_shared: ' + chopped,
                        logging.info)

    #
    # modeled after check_personalized_messages().
    #

    #
    # this is for computing whether it should be considered "heard"
    # if hung up early.
    #
    globals4signal['db_out_obj'] = pick

    #
    # say the person's name.
    #
    say_person_name(pick)

    beginTime = datetime.datetime.now()
    globals4signal['begin_play_time'] = beginTime
    globals4signal['playing_own_msg'] = True

    dsh_agi.say_it(chopped)
    endTime = datetime.datetime.now()
    deltaSeconds = (endTime - beginTime).seconds
    time.sleep(1)

    #
    # remember the fact that this caller has heard this message.
    #
    dsh_agi.report_event(
        "heard one's own peer-shared message.",
        item=pick,
        action='HERD',
        phone_number=caller.phone_number,
        owner=caller,
        call_duration=deltaSeconds,
        sessionID=get_session())
    dsh_utils.give_news(
        'dsh_django2.play_own_peer_shared: heard: '+ chopped, logging.info)
    
    #
    # 10/02/13:
    # the following flag is for computing for a smaller threshold
    # for one's own messages in the hangup handler, now that we're
    # done, no need to keep it.
    #
    globals4signal['playing_own_msg'] = False

    #
    # beep twice at the end of each message.
    #
    dsh_agi.say_it('beep')
    dsh_agi.say_it('beep')
    return pick
    
    

def get_peer_shared(caller):
    """called by should_play_peer_shared().
    gets a peer-shared message.
    return (sharedObj, choppedSlnName, allSharedHeard)
    """
    
    #sharedList = Item.objects.filter(peer_shared=True)
    sharedList = dsh_common_db.get_peer_shared_item_for_caller(
        caller, Item, KeyWord, get_session())
    if not sharedList:
        return None

    pick = None
    allSharedHeard = False
    notHeardList = []
    
    for shared in sharedList:
        heardEvents = Event.objects.filter(
            action='HERD', owner=caller.id, dsh_uid_concerned=shared.dsh_uid)
        if heardEvents:
            dsh_utils.db_print(
                'dsh_django2.get_peer_shared: heard: ' + shared.dsh_uid, 121)
            continue
        notHeardList.append(shared)

    if notHeardList:
        random.seed()
        l = len(notHeardList)
        r = random.randint(0, l-1)
        dsh_utils.db_print('dsh_django2.get_peer_shared: ' + 'l: ' + str(l)+\
                           ', r: ' + str(r), 123)
        pick = notHeardList[r]
        dsh_utils.db_print('dsh_django2.get_peer_shared: ' +\
                           'not heard randomly picked: ' +\
                           pick.dsh_uid, 121)
        dsh_utils.db_print('total unheard: ' + str(l), 121)
        dsh_utils.db_print('random index: ' + str(r), 121)

    if pick:
        dsh_utils.db_print('dsh_django2.get_peer_shared: found not heard: ' +\
                           pick.dsh_uid, 121)

    if not pick:
        #
        # all the peer-shared messages have been heard,
        # so I'm going to randomly pick a shared message that's already heard.
        #
        allSharedHeard = True
        random.seed()
        l = len(sharedList)
        r = random.randint(0, l-1)
        pick = sharedList[r]
        dsh_utils.db_print('dsh_django2.get_peer_shared: randomly picked: ' +\
                           pick.dsh_uid, 121)

    chopped = get_sln_path_for_asterisk(pick)
    if not chopped:
        message = 'dsh_django2.get_peer_shared: get_sln_path_for_asterisk' +\
                  ' failed: ' + repr(pick)
        dsh_agi.report_event(message, reportLevel='ERR',
                             sessionID=get_session())
        dsh_utils.give_bad_news(message, logging.error)
        return None    
    
    dsh_utils.db_print('dsh_django2.get_peer_shared: chopped sln: ' +\
                       chopped, 121)
    return (pick, chopped, allSharedHeard)



def should_play_peer_shared(caller, broadcastItem):
    """called by get_outgoing_voice_from_db()."""

    if broadcastItem:
        heardEvents = Event.objects.filter(
            action='HERD',
            owner=caller.id,
            dsh_uid_concerned=broadcastItem.dsh_uid)
        if not heardEvents:
            #
            # there's a broadcast item and it's not been heard.
            # we shouldn't play a peer-shared message.
            #
            dsh_utils.db_print(
                'dsh_django2.should_play_peer_shared: broadcast not heard: '+\
                broadcastItem.dsh_uid, 121)
            return None

    #
    # to get here, either broadcastItem==None, or heardEvents.
    #
    playShared = get_peer_shared(caller)
    if not playShared:
        #
        # there's no peer-shared message to play.
        #
        dsh_utils.db_print(
            'dsh_django2.should_play_peer_shared: no peer-shared msg.', 121)
        return None

    shared,slnChopped,allSharedHeard = playShared
    dsh_utils.give_news(
        'dsh_django2.should_play_peer_shared: will play peer-shared.' +\
        shared.dsh_uid + ',  ' + 'allSharedHeard: ' + repr(allSharedHeard),
        logging.info)
    return playShared
        


def get_outgoing_voice_from_db(caller):
    """
    look up in the django database.
    look for items that are "active" and are of the "broadcast" type.
    returns (item, chopped, allSharedHeard, playShared)
    """
    dsh_utils.db_print('dsh_django2.get_outgoing_voice_from_db: ' +
                       'entered.', 125)
    #activeBroadcastItems = Item.objects.filter(active=True, itype='B')
    activeBroadcastItems = dsh_common_db.get_active_broadcast_item_for_caller(\
        caller, Item, KeyWord, get_session())
    if not activeBroadcastItems:
        message = 'dsh_django1.get_outgoing_voice_from_db: ' + \
                  'no currently active broadcast message.'
        dsh_agi.report_event(message, reportLevel='ERR',
                             sessionID=get_session())
        dsh_utils.give_bad_news(message, logging.error)


        #
        # this bit is added, to consider playing shared peer messages.
        # 09/09/20
        #
        shouldPlayPeerShared = should_play_peer_shared(caller, None)
        if shouldPlayPeerShared:
            dsh_utils.db_print('dsh_django2.get_outgoing_voice_from_db: ' +
                               'play shared 1', 125)
            shared,chopped,allSharedHeard = shouldPlayPeerShared
            return (shared,chopped,allSharedHeard,True)
        else:
            #
            # no broadcast item.  no shared peer message.  no nothing.
            #
            message = 'dsh_django2.get_outgoing_voice_from_db: ' +\
                      'no broadcast, no shared, no nothing.'
            dsh_utils.give_news(message)
            dsh_agi.report_event(message, sessionID=get_session())
            return None

    
    item = activeBroadcastItems[0]
    dsh_utils.db_print('dsh_django1.get_outgoing_voice_from_db: ' +
                       repr(item), 125)


    #
    # this bit is added, to consider playing shared peer messages.
    # 09/09/20
    #
    shouldPlayPeerShared = should_play_peer_shared(caller, item)
    if shouldPlayPeerShared:
        shared,chopped,allSharedHeard = shouldPlayPeerShared
        return (shared,chopped,allSharedHeard,True)
    

    dsh_utils.db_print('dsh_django2.get_outgoing_voice_from_db: ' +\
                       'play broadcast: ' + item.dsh_uid, 125)
    
    chopped = get_sln_path_for_asterisk(item)
    if chopped == None:
        return None
        
    return (item,chopped,False,False)
    


def lookup_number_in_db(env, debugCheat=False, useThisNumber=None):
    """lookup the caller info in the django database.  returns the tuple
    (pObj, phoneNumber, callType),
    where callType can be one of 'regular', 'forward', 'dotcall'.
    if called when handling staff caller, useThisNumber is the number
    entered by the staff with the keypad."""

    callType = 'regular'
    
    if useThisNumber:
        phoneNumber = useThisNumber
        callType = 'forward'
    else:
        if debugCheat:
            env['agi_callerid'] = '09935237794'

        #
        # check to see if this is the result of a .call file.
        # if yes, you have something like:
        # agi_calleridname = __DOT_CALL__ phoneNum
        #
        # 10/02/27:
        # instead of phone number, now we're looking for dsh_uid.
        #
        #found,phoneNumber = dsh_agi.check_dot_call_num(env)
        found,dotDshUid = dsh_agi.check_dot_call_num(env)
        phoneNumber = None
        
        if found:
            callType = 'dotcall'
            message = 'dsh_django2.lookup_number_in_db: ' + \
                      '.call received: ' + dotDshUid
            dsh_agi.report_event(message, reportLevel='INF',
                                 sessionID=get_session())
            dsh_utils.give_news(message, logging.info)

            #
            # 10/02/27:
            #
            success,caller = dsh_common_db.dot_call_id_to_caller(
                dotDshUid, Person, get_session())
            if success:
                return (caller, caller.phone_number, callType)
            return None
            
        else:
            if not env.has_key('agi_callerid'):
                message = 'dsh_django1.lookup_number_in_db: ' + \
                          ' no phone number given by Asterisk.'
                dsh_utils.give_news(message, logging.info)
                dsh_agi.report_event(message, reportLevel='WRN',
                                     sessionID=get_session())
                return None
            phoneNumber = env['agi_callerid']
    
    persons = Person.objects.filter(phone_number=phoneNumber)
    if not persons and phoneNumber and phoneNumber[0] != '0':
        #
        # prefix with a zero and try again.
        # when dialing out for synchronous calls, we don't have a 0.
        #
        persons = Person.objects.filter(phone_number='0'+phoneNumber)
    elif not persons and phoneNumber and phoneNumber[0] == '0':
        #
        # if a callee without a 0 gets into the database first,
        # we need to chop off the 0 from a regular caller to check.
        #
        persons = Person.objects.filter(phone_number=phoneNumber[1:])
        
    if not persons:
        message = 'dsh_django1.lookup_number_in_db: ' + \
                  ' phone number not found in database: ' + phoneNumber
        dsh_utils.give_news(message, logging.info)
        dsh_agi.report_event(message, reportLevel='INF',
                             phone_number=phoneNumber,
                             sessionID=get_session())
        return (None, phoneNumber, callType)

    foundOwner = None
    if len(persons) > 1:
        message = 'dsh_django1.lookup_number_in_db: ' + \
                  'more than one person in the db has this number: ' + \
                  phoneNumber + \
                  ', the list of people are: ' + \
                  repr(persons)
        dsh_utils.give_news(message, logging.info)
        dsh_agi.report_event(message, reportLevel='INF',
                             phone_number=phoneNumber,
                             sessionID=get_session())
        
        for onep in persons:
            if onep.phone_owner:
                foundOwner = onep
                break
    
    if foundOwner:
        p = foundOwner
    else:
        #p = persons[0]
        p = persons.latest()
        
    answer = (p, phoneNumber, callType)
    dsh_utils.db_print('dsh_django1.lookup_number_in_db: ' +
                       repr(answer), 98)
    dsh_utils.give_news('dsh_django2.lookup_number_in_db: ' +\
                        p.__unicode__() + ' -- ' +\
                        p.organization.alias + ' -- ' +\
                        phoneNumber,
                        logging.info)
    return answer



def determine_unknown_caller(unknownOrg, unknownPerson,
                             phoneNumberLookupResult,
                             syncCallee=False):
    """if the caller's phone number is not known at all, we say the caller is
    unknownPerson from the unknownOrg.
    if the caller's phone number is known but not in the database,
    we add the caller to the database, and make her belong to unknownOrg."""

    if not phoneNumberLookupResult:
        #
        # we don't know the guy's phone number.
        #
        return unknownPerson

    person,phoneNumber,callType = phoneNumberLookupResult

    if person:
        return person

    #
    # we have a phone number. but the person is not in the database.
    # we should put the person in.
    #
    unknownPersonName = dsh_config.lookup('UNKNOWN_PERSON_NAME')
    if syncCallee:
        personDescr = 'callee'
    else:
        personDescr = 'caller'
    personText = 'This unknown %s was automatically added by Asterisk.' %\
                 (personDescr,)
        
    newUnknownPerson = Person(
        first_name=unknownPersonName,
        phone_number=phoneNumber,
        organization=unknownOrg,
        ptype='USR',
        gender='F',
        description=personText)
    newUnknownPerson.save(sessionID=get_session(), setSession=True)
    message = 'dsh_django1.determine_caller: ' + \
              'added unknown caller to database with number: ' + \
              phoneNumber
    dsh_utils.give_news(message, logging.info)
    dsh_agi.report_event(message, reportLevel='INF',
                         phone_number=phoneNumber,
                         sessionID=get_session())
    return newUnknownPerson



def consider_partial_heard():
    """called by hangup_signal_handler().
    if hung-up early, should we consider the message heard?
    it looks at globals4signal['db_out_obj'].
    """

    dsh_utils.db_print('dsh_django2.consider_partial_heard: entered.', 123)
    
    if globals4signal.has_key('caller_dude') and globals4signal['caller_dude']:
        caller = globals4signal['caller_dude']
    else:
        caller = None        


    if not globals4signal.has_key('db_out_obj') or \
           not globals4signal['db_out_obj']:
        message = 'dsh_django2.consider_partial_heard: no db_out_obj.'
        dsh_utils.give_news(message, logging.info)
        #dsh_agi.report_event(message, reportLevel='WRN',
        #                     sessionID=get_session())
        dsh_agi.report_event(message,
                             call_duration=1,
                             action='UNHR',
                             owner=caller,
                             sessionID=get_session())
        return
    item = globals4signal['db_out_obj']

    if not globals4signal.has_key('begin_play_time') or \
       not globals4signal['begin_play_time']:
        message = 'dsh_django2.consider_partial_heard: no begin_play_time.'
        dsh_utils.give_news(message, logging.info)
        #dsh_agi.report_event(message, reportLevel='WRN',
        #                     sessionID=get_session())
        dsh_agi.report_event(message,
                             item=item,
                             action='UNHR',
                             call_duration=1,
                             owner=caller,
                             sessionID=get_session())
        return
    
    #
    # I'm calculating durations like this instead of calling
    # calculate_durations() because
    # in the case of peer-shared messages, there's a bunch of
    # prompt stuff at the beginning.
    # globals4signal['begin_play_time'] is set right before
    # playing the real message so it's more accurate.
    #
    beginPlayTime = globals4signal['begin_play_time']
    endTime = datetime.datetime.now()
    deltaSeconds = (endTime - beginPlayTime).seconds

    if not globals4signal.has_key('caller_dude') or \
           not globals4signal['caller_dude']:
        message = 'dsh_django2.consider_partial_heard: no caller_dude.'
        dsh_utils.give_bad_news(message, logging.warning)
        dsh_agi.report_event(message, reportLevel='WRN',
                             sessionID=get_session())
        dsh_agi.report_event(message,
                             item=item,
                             action='UNHR',
                             call_duration=1,
                             sessionID=get_session())
        return
    caller = globals4signal['caller_dude']

    #
    # if already heard, no need to do it again.
    #
    heardEvents = Event.objects.filter(
        action='HERD', owner=caller.id, dsh_uid_concerned=item.dsh_uid)
    if heardEvents:
        dsh_utils.db_print(
            'dsh_django2.consider_partial_heard: already heard: ' +\
            caller.dsh_uid + ' <- ' + item.dsh_uid, 123)
        #
        # 10/02/13:
        # hangup during recording after having heard in entirety.
        #
        #message = 'dsh_django2.consider_partial_heard: already heard. '  +\
        #          caller.dsh_uid + ' <- ' + item.dsh_uid
        #dsh_utils.give_bad_news(message, logging.warning)
        #dsh_agi.report_event(message, reportLevel='WRN',
        #                     sessionID=get_session())
        return
    
    itemDur = item.rec_duration
    if itemDur == 0:
        #
        # no divide by zero error please.
        #
        message = 'dsh_django2.consider_partial_heard: itemDur=0.'
        dsh_utils.give_bad_news(message, logging.warning)
        dsh_agi.report_event(message, reportLevel='WRN',
                             sessionID=get_session())
        dsh_agi.report_event(message,
                             item=item,
                             action='UNHR',
                             phone_number=caller.phone_number,
                             owner=caller,
                             call_duration=1,
                             sessionID=get_session())
        return
    
    callDur = deltaSeconds
    threshold = dsh_config.lookup('PARTIAL_HEARD')
    if globals4signal['playing_own_msg']:
        threshold = dsh_config.lookup('PARTIAL_OWN_HEARD')

    #
    # if the call length is greater than 70%,
    # we consider it heard.
    #
    fractionHeard = 1.0 * callDur / itemDur
    considerHeard = fractionHeard > threshold
    if not considerHeard:
        message = 'dsh_django2.consider_partial_heard: NOT heard: ' + \
                  str(fractionHeard)
        dsh_utils.give_news(message, logging.info)
        dsh_agi.report_event(message, sessionID=get_session())
        dsh_agi.report_event(
            message,
            item=item,
            action='UNHR',
            phone_number=caller.phone_number,
            owner=caller,
            call_duration=callDur,
            sessionID=get_session())
        return

    message = 'dsh_django2.consider_partial_heard: heard: ' + \
              str(fractionHeard)

    dsh_agi.report_event(
        message,
        item=item,
        action='HERD',
        phone_number=caller.phone_number,
        owner=caller,
        call_duration=callDur,
        sessionID=get_session())

    dsh_utils.give_news(message, logging.info)



def maybe_remove_from_current_dial():
    """
    10/03/31:
    called by hangup_signal_handler.
    see note100331
    """

    caller = None
    if globals4signal.has_key('caller_dude'):
        caller = globals4signal['caller_dude']

    if not caller:
        return

    dsh_common_agi.remove_from_current_dial_if_no_message(
        caller, Item, KeyWord, Event, noLogging=True, sessionID=get_session())
    


def hangup_signal_handler(signum, frame, hungup=True):
    """
    10/04/04:
    pushed the substance into hangup_signal_handler_wrapped().
    so that it can be called without exiting
    by record_doctor_reply().
    """
    retCode,logCall = hangup_signal_handler_wrapped(
        signum, frame, hungup=hungup)
    sys_exit(retCode, logCall=logCall, hungup=hungup)
    
    
    
def hangup_signal_handler_wrapped(signum, frame, hungup=True):
    """attempt to do file format conversion upon a hangup.
    from .wav to .mp3.
    after conversion, we put it in the django database.
    10/04/04:
    rewritten to get rid of the sys_exits and replace them with returns.
    because we are getting called by record_doctor_reply()
    for recording multiple doctor questions and answers.
    hungup=False when it's called by record_doctor_reply()
    instead of sys_exit, we return(returnCode, logCall)
    """
    
    dsh_utils.db_print2('dsh_django1.signal_handler: entered...', 101)


    #
    # 10/03/31:
    # people get put in CDS, and they get called at least once.
    # if they have no message of any kind, but they picked up the phone
    # or called in, we will remove them from the CDS.
    # note100331
    #
    maybe_remove_from_current_dial()

    #
    # if hung-up early, should we consider the message heard?
    # it looks at globals4signal['db_out_obj'].
    #
    consider_partial_heard()


    #
    # if this whole thing was initiated because of a dot call file,
    # but we didn't finish till the end, check to see if we should
    # "re-arm" the dot call file.
    #
    if hungup and globals4signal.has_key('dot_call_initiated') and \
       globals4signal['dot_call_initiated'] != None:

        callee = globals4signal['dot_call_initiated']
        #
        # 10/03/18:
        # doctor's reply might be pushed out even when
        # global auto-dial is off. if that were the case,
        # make sure we don't re-arm.
        #
        disabled = dsh_db_config.get('auto_dial_disable')
        if disabled:
            message = 'dsh_django2.signal_handler: auto-dial disabled, ' +\
                      'so no-rearming.'
            dsh_utils.give_news(message, logging.info)
            dsh_agi.report_event(message,
                                 phone_number=callee.phone_number,
                                 owner=callee,
                                 sessionID=get_session())
        else:
            
            dsh_utils.db_print('dsh_django2.signal_handler: sleeping... ', 116)
            #10/04/05:
            time.sleep(1)
            dsh_django_utils.check_auto_timed_calls_for_person(
                callee, sessionID=get_session())
            calleeInfo = dsh_django_utils.callee_info(callee)    
            message = 'dsh_django2.signal_handler: re-arming callee: ' +\
                      calleeInfo
            dsh_utils.db_print(message, 116)
            dsh_agi.report_event(message,
                                 action='RARM',
                                 phone_number=callee.phone_number,
                                 owner=callee,
                                 sessionID=get_session())
            dsh_utils.give_news(message, logging.info)

    #
    # the stuff below all has to do with format conversion and
    # saving the mp3 file in the database.
    #
    
    #
    # get the name of the file that was just recorded.
    #
    if not globals4signal.has_key('in_file'):
        dsh_utils.give_news('dsh_django1.hangup_signal_handler: ' +
                            'hangup before recording.', logging.info)
        #sys_exit(0)
        return (0, False)

    inputFile = globals4signal['in_file']


    #
    # the recorded format is wav? if not, we don't convert.
    #
    fileFormat = dsh_config.lookup('record_file_format')
    if fileFormat != 'wav':
        message = 'dsh_django1.hangup_signal_handler: ' + \
                  "can't convert non-wav file: " + inputFile
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT',
                             sessionID=get_session())
        #sys_exit(1)
        return (1, False)


    #
    # does the .wav file exist and is it non-zero sized?
    #
    time.sleep(1)
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

        #
        # earlier, there was no "logCall=True"
        # the problem is that we don't put in an event log entry.
        # this messes up with stats counting.
        # we get here quite often.
        #
        #sys_exit(1, logCall=True)
        return (1, True)
    if bytes == 0:
        message = 'dsh_django1.hangup_signal_handler: ' + \
                  'inputfile size 0: ' + inputWav
        dsh_utils.give_news(message, logging.info)
        dsh_agi.report_event(message, reportLevel='WRN',
                             sessionID=get_session())
        #
        # as far as I can tell from the log, this hasn't happened.
        #
        #sys_exit(1, logCall=True)
        return (1, True)

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
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT',
                             sessionID=get_session())
        #sys_exit(1)
        return (1, False)


    #
    # stdout and stderr redirected to the log directory.
    #
    stdLogs = dsh_bizarro.stdio_logs_open(globals4signal['log_dir'])
    if not stdLogs:
        message = 'dsh_django2.hangup_signal_handler: failed to set stdLogs'
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT',
                             sessionID=get_session())
        #sys_exit(1)
        return (1, False)
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
        dsh_agi.report_event(message, reportLevel='CRT',
                             sessionID=get_session())
        #sys_exit(1, logCall=True)
        return (1, True)

    dsh_utils.give_news('dsh_django1.signal_handler: conversion success: ' +
                        command, logging.info)

    dsh_utils.chmod_tree2(outputMp3, recurse=False)
    
    if not dsh_utils.cleanup_path(inputWav, 'dsh_django1.signal_handler'):
        message = 'dsh_django1.signal_handler: ' + \
                  'failed to remove original wav: ' + \
                  inputWav
        dsh_utils.give_bad_news(message, logging.warning)
        dsh_agi.report_event(message, reportLevel='WRN',
                             sessionID=get_session())


    #
    # calculate some more fields for saving in the database.
    #
    callDur,recDur = calculate_durations(allowCache=False, hungup=hungup)
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
    if globals4signal.has_key('callee_dude') and \
       globals4signal['callee_dude']:
        item.i05 = globals4signal['callee_dude']
        item.itype = 'S'
        
    try:
        item.save(sessionID=get_session(), setSession=True)
        dsh_utils.db_print2('dsh_django1.signal_handler: item saved: ' +
                            choppedFileName, 101)
    except:
        message = 'dsh_django1.signal_handler: saving in django failed: ' + \
                  choppedFileName, 101
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT',
                             sessionID=get_session())
        #sys_exit(1)
        return (1, False)

    #
    # 10/03/24:
    #
    answered = put_doctor_answer_event(item, sessionID=get_session())
    if answered:
        add_doctor_answer_fields(item, sessionID=get_session())

    #
    # no point continuing execution after hangup.
    #
    #sys_exit(0)
    return (0, False)



def calculate_durations(allowCache=True, hungup=True):
    #
    # compute the duration of the call.
    #
    global globals4signal

    allowCache = False
    if not allowCache:
        if globals4signal.has_key('call_duration'):
            del globals4signal['call_duration']
        if globals4signal.has_key('rec_duration'):
            del globals4signal['rec_duration']
    
    if globals4signal.has_key('call_duration'):
        callDur = globals4signal['call_duration']
        dsh_utils.db_print('calculate_durations: using cached version: '+\
                           repr(callDur), 154)
    else:
        endTime = datetime.datetime.now()
        startTime = globals4signal['start_time']
        delta = endTime - startTime
        seconds = delta.seconds
        dsh_utils.db_print('dsh_django1.sys_exit: call duration: ' +
                           str(seconds) + 's.', 95)
        callDur = seconds
        globals4signal['call_duration'] = seconds
        dsh_utils.db_print('calculate_durations: calculated: '+\
                           repr(callDur), 154)

    if not hungup:
        callDur = 0

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
    
    

def sys_exit(code, logCall=False, hungup=True):
    """a wrapper for sys.exit(), logs one line before exiting.
    logHangup is set to True when, for example, we thought we had some
    recording to convert, but we found nothing to convert---in a "bug" earlier,
    in such a case, recDur has been set to non-zero, so as a result, we
    skip logging such an event, which screws up stats calculation.
    10/04/04:
    hungup=True when called by hangup_signal_handler() invoked from
    record_doctor_reply().
    """
    global globals4signal

    callDur,recDur = calculate_durations(hungup=hungup)

    #
    # repeats the caller info: phone number, school, name.
    #
    if globals4signal.has_key('caller_dude'):
        caller = globals4signal['caller_dude']
        logStr = '|| ' + caller.phone_number + ' || ' + \
                 caller.organization.alias + ' || ' + \
                 caller.__unicode__() + ' || '

        if logCall or recDur == None or recDur == 0:
            #
            # we know there's a caller, but there's no recDur.
            # that means the person hung up before recording.
            # we'll put a call without recording in the event table.
            #
            # see the comment string of this function to see when
            # logCall is set to True
            #
            eventDescription = 'hangup before recording.'
            if logCall:
                eventDescription = 'call completed but no recording.'
            if not recDur:
                recDur = 0
            if globals4signal.has_key('db_out_obj') and \
               globals4signal['db_out_obj']:
                dshUid = globals4signal['db_out_obj'].dsh_uid
            else:
                dshUid = ''
            event = Event(
                owner=caller,
                phone_number=caller.phone_number,
                action='CALL',
                etype='INF',
                call_duration=callDur,
                rec_duration = recDur,
                description=eventDescription,
                dsh_uid_concerned = dshUid,
                session=get_session())
            event.save()

            if logCall:
                dsh_utils.give_news(
                    'dsh_django2.sys_exit: ' + eventDescription,
                    logging.info)
    else:
        logStr = ''

    logStr += str(callDur) + ' || '
    if recDur:
        logStr += str(recDur)

    dsh_utils.give_news('dsh_django1.sys_exit: ' + logStr, logging.info)
    if hungup:
        sys.exit(code)



def determine_recorded_file_name(caller, outgoingItem=None):
    """outgoingItem is used for filling in the followup_to field
    of incoming items.  it could be None when called from places
    other than handling regular incoming calls."""
    
    #
    # I need to make a new item because that's where the new dsh_uid is.
    #
    if outgoingItem:
        item = Item(
            owner=caller,
            itype='I',
            followup_to=outgoingItem)
    else:
        item = Item(
            owner=caller,
            itype='I')
        

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
        dsh_agi.report_event(message, reportLevel='CRT',
                             sessionID=get_session())
        return (item, None)

    dsh_utils.chmod_tree2(dirName, recurse=False)

    slnDir = os.path.join(dirName, 'sln')
    if not dsh_utils.try_mkdir_ifdoesnt_exist(
        slnDir, 'dsh_django1.determine_recorded_file_name: '):
        message = 'dsh_django1.dsh_utils.try_mkdir_ifdoesnt_exist failed: '+\
                  'on slnDir: ' + slnDir
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT',
                             sessionID=get_session())
        return (item, None)
    dsh_utils.chmod_tree2(slnDir, recurse=False)
    
    return (item,incomingFullName)



def get_sln_path_for_asterisk(item):
    return field_to_sln_path(item.file)



def field_to_sln_path(field):
    """
     fix up the file name: from the database, it's an mp3 URL.
     django should have taken the trouble of converting it to sln alredy.
     we call some function to get the path name of the sln file.
    """

    return dsh_common_agi.field_to_sln_path(field, sessionID=get_session())



def check_personalized_messages(caller):
    """does this caller have any unheard personalized messages?
    returns the first personalized message heard.
    """

    global globals4signal
    

    #
    # does this caller have any personal messages intended for him?
    #
    #messages = caller.message_for_me.all()

    messages = caller.message_for_me.filter(itype='P', active=True)
    
    dsh_utils.db_print('dsh_django1.check_personalized_message: msg: ' +\
                       repr(messages), 168)
    if not messages:
        return None

    firstHeard = None
    sayDSH = True
    for msg in messages:
        #
        # the message needs to be "personalized" and it needs to be "active."
        #
        maybe_deactivate_personal_message(msg)

        #if not msg.active:
        #    dsh_utils.db_print('not active.', 108)
        #    continue
        #if msg.itype != 'P':
        #    dsh_utils.db_print('not personalized: ' + msg.itype, 108)
        #    continue

        #if msg.dummy:
        #    dsh_utils.db_print('is dummy.', 168)
        #    continue

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
            dsh_agi.report_event(message, reportLevel='ERR',
                                 sessionID=get_session())
            dsh_utils.give_bad_news(message, logging.error)
            continue



        dsh_common_agi.check_personalized_followup_to(
            caller, msg, get_session(), say_message_from_name)
        


        #
        # now play the personalized message and compute how long it lasted.
        #

        #
        # this is for computing whether it should be considered "heard"
        # if hung up early.
        #
        globals4signal['db_out_obj'] = msg

        #
        # say the person's name.
        #
        #say_person_name(msg, sayDSH=sayDSH)
        #sayDSH = False
        #
        # 10/03/06:
        # say the doctor's name
        #
        dsh_common_agi.say_date(msg)
        dsh_common_agi.say_doctor_name(msg, sessionID=get_session())
        
        
        beginTime = datetime.datetime.now()
        globals4signal['begin_play_time'] = beginTime

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
            call_duration=deltaSeconds,
            sessionID=get_session())
        dsh_utils.give_news('dsh_django1.check_personalized_message: heard: '+\
                            msg.dsh_uid, logging.info)
        if firstHeard == None:
            firstHeard = msg

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
        
    return firstHeard



def message_answered(msg, doctor):
    """
    10/03/25:
    moved to dsh_common_db.py
    10/03/20:
    has this message been answered by this doctor?
    """
    return dsh_common_db.message_answered(msg, doctor, Event)



def maybe_deactivate_patient_question(item):
    """
    10/03/25:
    moved to dsh_common_db.py
    10/03/20:
    if this message has been answered by all the doctors assigned,
    then we deactivate it.
    it's modeled after maybe_deactivate_personal_message().
    """
    return dsh_common_db.maybe_deactivate_patient_question(
        item, Event, sessionID=get_session())



def maybe_deactivate_personal_message(item):
    """if all the intended audience has heard this item,
    de-activate it."""

    if not item.active:
        return
    
    allAudience = item.intended_audience.all()
    if not allAudience:
        dsh_utils.db_print('dsh_django1.maybe_deactivate_personal_message: '+\
                           item.dsh_uid, 108)
        item.active = False
        item.save(sessionID=get_session())
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
    item.save(sessionID=get_session())
    message = 'dsh_django1.maybe_deactivate_personal_message: deactivated: '+\
              item.dsh_uid
    dsh_utils.give_news(message, logging.info)
    dsh_agi.report_event(message, item=item,
                         sessionID=get_session())



def handle_regular_caller(caller, callType=None):
    """a regular caller hears a message and records a message."""

    global globals4signal

    funcName = 'dsh_django2.handler_regular_caller:'

    say_first_prompt(sayDSH=True)
    say_caller_name(caller)

    if callType and callType=='dotcall':
        globals4signal['dot_call_initiated'] = caller

    autoBroadcast = dsh_django_utils.should_auto_dial_broadcast(caller)
    dsh_utils.db_print(
        '%s autoBroadcast: %s.' % (funcName, repr(autoBroadcast)), 169)
    

    #
    # 10/03/24:
    # the original intention:
    # for someone like Calcutta, if we find out their
    # auto-dial broadcast flag is not on, then we don't play the broadcast.
    # the problem I discovered today, for DIET, and for play-once message,
    # we intentionally get trapped in here.
    # I'm going to disable the if part. note100324.
    #
    if False and callType and callType=='dotcall' and not autoBroadcast:
        #
        # for dot calls we don't play the broadcast outgoing message.
        #
        outVobj = None
        playShared = False
    else:
        #
        # get the outgoing voice from the database.
        #
        answer = get_outgoing_voice_from_db(caller)
        if not answer:
            #sys_exit(1)
            return False
        outVobj,outgoingVoice,allSharedHeard,playShared = answer
        dsh_utils.db_print(
            '%s outVobj: %s, outgoingVoice: %s.' % \
            (funcName, repr(outVobj), repr(outgoingVoice)), 169)


    if not (caller.ptype == 'STF' or caller.ptype == 'TST'):
        #
        # play one's own peer-shared message.
        # 
        play_own_peer_shared(caller)
    else:
        dsh_utils.db_print(
            'dsh_django2.handle_regular_caller: skip play own shared: ' +\
            caller.__unicode__(), 127)
                
    
    #
    # check whether there're any personalized messages for this caller.
    # for establishing follow_up_to link, I think.
    #
    firstHeard = check_personalized_messages(caller)
    if firstHeard and outVobj == None:
        outVobj = firstHeard

    #
    # 10/03/18:
    # set the followupTo field of the new item to the personalized
    # message instead of the broadcast message.
    # previously, it's always been set to outVobj, which is the
    # broadcast message if there were one.  In our case, it's been
    # the silent blank message from me.  Not useful.
    #
    if firstHeard:
        followUpTo = firstHeard
    else:
        followUpTo = outVobj


    #
    # set this global variable for considering whether a hung-up message
    # should be considered "heard."
    #
    # if we get this far, the personalized message(s) should have been
    # heard in their entireties.  and that should have put heard events
    # in the Event table already.  inside check_personalized_messages()
    # we have already set this global variable.  if the personalized
    # message was hung-up, we won't be here.  so if we get here, we
    # can/should overwrite it.  so we'll consider the broadcast message.
    #
    if outVobj:
        globals4signal['db_out_obj'] = outVobj
        

    #####
    # testing...
    #####
    #result = dsh_agi.get_digits()
    #dsh_utils.give_news('dsh_test1: digits: ' + result, logging.info)
    #sys.exit(0)
    #dsh_agi.exec_com()
    #dsh_utils.give_news('dsh_test1: exit!', logging.info)
    #sys.exit(0)


    # 
    # see note100324 above.
    # 
    if False and callType and callType == 'dotcall' and not autoBroadcast:
        #
        # for dot calls we don't play the broadcast outgoing message.
        #
        pass
    elif (not autoBroadcast) and outVobj and outVobj.itype == 'B' and \
         outVobj.play_once:
        #
        # 10/04/14:
        # yes, this is getting really ugly, I know.
        #
        # prevents play_once broadcast messages from being played.
        # I'm not stopping it using the if statement above,
        # because that one would have stopped peer-shared messages.
        #
        # this has not been an issue on the DSH forum side, because
        # in the play_once broadcast case, they will find a peer-shared
        # message to play so this has not been triggered.
        #
        dsh_utils.db_print(
            '%s not playing play_once broadcast message.' % (funcName,), 169)
        pass
    else:

        #
        # if we're playing a shared peer message,
        # we will say the teacher's name and the org's name.
        #
        if playShared:
            message = 'peer-shared message played: ' + outgoingVoice +\
                      '.   caller: ' + caller.__unicode__()
            dsh_agi.report_event(message,
                                 item=outVobj,
                                 action='PEER',
                                 phone_number=caller.phone_number,
                                 owner=caller,
                                 sessionID=get_session())
            dsh_utils.give_news(message, logging.info)
        else:
            message = 'broadcast message played: ' + outgoingVoice +\
                      '.   caller: ' + caller.__unicode__()
            dsh_agi.report_event(message,
                                 item=outVobj,
                                 action='BRCT',
                                 phone_number=caller.phone_number,
                                 owner=caller,
                                 sessionID=get_session())
            dsh_utils.give_news(message, logging.info)
            
        #
        # 09/12/28: used to be inside the "if playShared:" above.
        # now taking it out.
        #
        if outVobj:
            say_person_name(outVobj)
            
        #
        # play the outgoing file.
        # the global variable is for considering whether partially heard
        # should be considered "heard."
        #
        globals4signal['begin_play_time'] = datetime.datetime.now()
        dsh_agi.say_it(outgoingVoice)

        #
        # if we don't have the sleep, upon a hangup, despite triggering
        # the signal handler, it might just execute a little beyond here.
        #
        time.sleep(1)
        
        #
        # put a "heard" event in.
        #
        endTime = datetime.datetime.now()
        deltaSeconds = (endTime - globals4signal['begin_play_time']).seconds
        dsh_agi.report_event(
            'message heard in entirety.',
            item=outVobj,
            action='HERD',
            phone_number=caller.phone_number,
            owner=caller,
            call_duration=deltaSeconds,
            sessionID=get_session())
        


    #
    # this ensures that we don't "re-arm" a dot call.
    # if it's hung up on us, the dot call gets "re-armed".
    #
    # I'm commenting this out---I always want to re-check...
    # these days, for most people, I always need to re-arm...
    # if there's nothing to re-arm, it won't generate a dot call file anyways.
    #
    #globals4signal['dot_call_initiated'] = None

    #
    # say one more prompt for recording.
    #
    promptDir = dsh_config.lookup('DSH_PROMPT_DIR')
    pleaseRecord = os.path.join(
        promptDir, dsh_config.lookup('DSH_PROMPT_PLEASE_RECORD'))
    dsh_agi.say_it(pleaseRecord)
    dsh_agi.say_it('beep')
    dsh_agi.say_it('beep')
    time.sleep(1)

    #
    # determine the input file name for recording.
    #
    # 09/10/05: this was mistakenly placed before the previous chunk
    # of code.  this has the effect of setting the 'in_file' global
    # variable prematurely while the prompt is being read.
    # this in turn makes it more likely to get the "no file to
    # convert" thing in the hangup signal handler.
    #
    # 10/03/18:
    # the followup_to field of the new item is set correctly
    # to the personalized message instead of the broadcast.
    # this is necessary for patient's new message to follow up to
    # a doctor's reply.
    #
    #prepareResult = prepare_input_file(caller, outVobj)
    prepareResult = prepare_input_file(caller, followUpTo)
    if not prepareResult:
        return False

    #
    # record it.
    #
    globals4signal['start_record'] = datetime.datetime.now()
    inVobj,incomingFullName = prepareResult
    dsh_agi.record(incomingFullName)
    time.sleep(1)
    dsh_utils.db_print('dsh_django1: record call ends.', 101)
    dsh_utils.give_news('dsh_django1: recording call ends, no hangup.')
    say_goodbye()

    #
    # these days, I only get here when time limit is exhausted.
    # need to manually hangup.
    # otherwise, re-arming the .call file doesn't work, because...
    # the current .call file is still alive and will be deleted after hangup.
    # copied from dsh_failed.py
    #
    dsh_agi.send_command('HANGUP\n', caller='dsh_django2:')
    time.sleep(2)

    #
    # we shouldn't get here any more. because of the hangup above.
    # convert file format too with a proper hangup (pressing the # key).
    #
    message = "dsh_django2.handle_regular_caller: unexpected: " +\
              "after forced hangup."
    dsh_utils.give_bad_news(message, logging.warning)
    dsh_agi.report(message, reportLevel='CRT')
    hangup_signal_handler(0, None)
    return True



def say_goodbye():
    dsh_common_agi.say_goodbye()



def forward_outgoing_call(caller, unknownOrg, unknownPerson):
    """called by handle_staff_caller()."""
    
    global globals4signal


    #
    # look up default settings for voice prompts.
    #
    timeOut11 = dsh_config.lookup('DSH_PROMPT_WAIT11')
    voicePrompt = os.path.join(
        dsh_config.lookup('DSH_PROMPT_DIR'),
        dsh_config.lookup('DSH_PROMPT_PHONE_NUMBER'))
    
    while True:

        #
        # get the callee number from the caller.
        #
        callNum = dsh_agi.get_digits(
            voicePrompt, 11, timeOut=timeOut11)
        if callNum == None or callNum == '':
            continue
        if callNum == '*':
            say_goodbye()
            return True

        dsh_utils.db_print('dsh_django2: the number is ' + callNum,
                           111)

        #
        # look up the callee in the database.
        #
        lookupResult = lookup_number_in_db(None, useThisNumber=callNum)
        callee = determine_unknown_caller(unknownOrg, unknownPerson,
                                          lookupResult, syncCallee=True)
        dsh_utils.db_print('dsh_django1: the callee determined to be: ' +
                           repr(callee), 111)
        globals4signal['callee_dude'] = callee
        
        #
        # set up file names to be saved in the database.
        #
        prepareResult = prepare_input_file(caller)
        if not prepareResult:
            return False
        inVobj,incomingFullName = prepareResult

        message = 'attempt to call ' + callNum
        dsh_agi.report_event(message, action='SYNC',
                             phone_number=caller.phone_number,
                             owner=caller,
                             sessionID=get_session())
        dsh_utils.give_news('dsh_django2: ' + message, logging.info)


        #
        # actually do the call and recording now.
        #
        #XXX
        dsh_agi.forward_call(incomingFullName, callNum, testCheat=True)
        #dsh_agi.forward_call(incomingFullName, callNum)
        dsh_utils.give_news('dsh_django2: forwarding ends.')
        say_goodbye()
        hangup_signal_handler(0, None)
        return True

    return True



def prepare_input_file(caller, outVobj=None):
    """creates a db object for the input file.
    set global variables, for conversion, and db saving, and
    duration calculation."""

    global globals4signal

    inVobj,incomingFullName=determine_recorded_file_name(
        caller, outgoingItem=outVobj)
    if incomingFullName == None:
        dsh_utils.give_bad_news(
            'dsh_django2: determine_recorded_file_name failed: ',
            logging.critical)
        return None
    dsh_utils.db_print('dsh_django2: incomingFullName: ' + incomingFullName,
                       101)
    globals4signal['db_in_obj'] = inVobj
    globals4signal['start_record'] = datetime.datetime.now()
    globals4signal['in_file'] = incomingFullName

    return (inVobj,incomingFullName)



def play_recent(caller):
    """called by handle_staff_caller().
    play the 3 most recent recordings.
    caller: only for the purpose of logging."""

    promptDir = dsh_config.lookup('DSH_PROMPT_DIR')

    #
    # get the 3 most recent recordings.
    #
    howMany = dsh_config.lookup('DSH_RECENT_HOWMANY')
    #recents = Item.objects.all()[::-1][:howMany]
    longRecs = Item.objects.filter(
        rec_duration__gt=dsh_config.lookup('RECORDED_THRESH'))
    recents = longRecs[::-1][:howMany]

    if not recents:
        #
        # say sorry, and give up.
        #
        sorry = os.path.join(
            promptDir,
            dsh_config.lookup('DSH_PROMPT_SORRY'))
        dsh_agi.say_it(sorry)
        dsh_agi.say_it('beep')
        dsh_agi.say_it('beep')
        return False

    #
    # say we're about to play recent messages.
    #
    recently = os.path.join(promptDir,
                            dsh_config.lookup('DSH_PROMPT_RECENTLY'))
    dsh_agi.say_it(recently)

    #
    # loop through each of the recent recordings.
    #
    for recent in recents:
        dsh_utils.db_print(
            'dsh_django2.play_recent: ' + recent.__unicode__(), 132)
        dsh_django_utils.convert_field_to_sln(recent.file)
        chopped = get_sln_path_for_asterisk(recent)
        if not chopped:
            message = 'dsh_django2.play_recent: get_sln_path_for_asterisk() '+\
                      'failed: ' + recent.__unicode__()
            dsh_agi.report_event(message, reportLevel='ERR',
                                 sessionID=get_session())
            dsh_utils.give_bad_news(message, logging.error)
            continue
        
        beginTime = datetime.datetime.now()
        say_person_name(recent, sayDSH=False)
        dsh_agi.say_it(chopped)
        endTime = datetime.datetime.now()
        deltaSeconds = (endTime - beginTime).seconds
        
        message = 'dsh_django2.play_recent: played: ' + chopped
        dsh_agi.report_event(
            message,
            item=recent,
            action='RPRT',
            phone_number=caller.phone_number,
            owner=caller,
            call_duration=deltaSeconds,
            sessionID=get_session())
        dsh_utils.give_news(message, logging.info)

        dsh_agi.say_it('beep')
        dsh_agi.say_it('beep')
        
    #
    # say we're done.
    #
    recentEnd = os.path.join(
        promptDir,
        dsh_config.lookup('DSH_PROMPT_RECENT_END'))
    dsh_agi.say_it(recentEnd)
    dsh_agi.say_it('beep')
    dsh_agi.say_it('beep')
    
    return True



def call_scratch_number(caller, unknownOrg, unknownPerson):
    """called by handle_staff_caller().
    calls the scratch_phone_number1 field of Zobject01."""

    scratch = dsh_db_config.get('scratch_phone_number1')
    promptDir = dsh_config.lookup('DSH_PROMPT_DIR')
    if not scratch:
        response = os.path.join(
            promptDir,
            dsh_config.lookup('DSH_PROMPT_NO_SCRATCH'))
        dsh_agi.say_it(response)
        return False

    response = os.path.join(
        promptDir,
        dsh_config.lookup('DSH_PROMPT_DIAL_SCRATCH'))
    dsh_agi.say_it(response)

    #
    # copied from forward_outgoing_call().
    #

    #
    # look up the callee in the database.
    #
    callNum = scratch
    
    lookupResult = lookup_number_in_db(None, useThisNumber=callNum)
    callee = determine_unknown_caller(unknownOrg, unknownPerson,
                                      lookupResult, syncCallee=True)
    globals4signal['callee_dude'] = callee

    #
    # set up file names to be saved in the database.
    #
    prepareResult = prepare_input_file(caller)
    if not prepareResult:
        return False
    inVobj,incomingFullName = prepareResult

    message = 'attempt to call ' + callNum
    dsh_agi.report_event(message, action='SYNC',
                         phone_number=caller.phone_number,
                         owner=caller,
                         sessionID=get_session())
    dsh_utils.give_news('dsh_django2: ' + message, logging.info)


    #
    # actually do the call and recording now.
    #
    #XXX
    dsh_agi.forward_call(incomingFullName, callNum, testCheat=True)
    #dsh_agi.forward_call(incomingFullName, callNum)
    dsh_utils.give_news('dsh_django2: forwarding ends.')
    say_goodbye()
    hangup_signal_handler(0, None)
    return True



def welcome_doctor(caller):
    """
    10/03/20.
    called by handle_doctor_caller().
    """
    welcomePrompt = os.path.join(
        dsh_config.lookup('DSH_PROMPT_DIR'),
        dsh_config.lookup('DSH_PROMPT_WELCOME_DOCTOR'))
    dsh_agi.say_it(welcomePrompt)
    dsh_common_agi.say_doctor_name(None, sessionID=get_session(),
                                   doctor=caller)



def find_question_for_doctor(caller):
    """
    10/03/20:
    called by check_doctor_assignments().
    10/04/04:
    modified to use a global variable of the "cached" messages for a doctor.
    we do the database lookup once, and remove the ones that just got played.
    and stash the result in the global variable.
    """

    global globals4signal
    
    #
    # does this doctor have any personal messages assigned to him?
    #
    #messages = caller.message_for_me.all()

    if globals4signal.has_key('doctor_message_list_cache'):
        messages = globals4signal['doctor_message_list_cache']
    else:
        messages = caller.message_for_me.filter(
            itype='P', active=True)
        globals4signal['doctor_message_list_cache'] = messages
        
    dsh_utils.db_print(
        'find_question_for_doctor: messages are: ' +\
        repr(messages), 154)
    if not messages:
        dsh_utils.db_print('find_question_for_doctor: no message for doc.',
                           154)
        return None

    playThis = None
    for msg in messages:
        
        #
        # 10/04/09:
        # I'm using dummy messages for fake replies during demos.
        #
        if msg.dummy:
            dsh_utils.db_print(
                'find_question_for_doctor: skipping dummy: ' +\
                msg.dsh_uid, 168)
            remove_from_doctor_message_list_cache(msg)
            continue
        
        maybe_deactivate_patient_question(msg)
        answered = message_answered(msg, caller)
        if answered:
            dsh_utils.db_print(
                'find_question_for_doctor: already answered, skipping: ' +\
                msg.dsh_uid, 154)
            remove_from_doctor_message_list_cache(msg)
            continue

        playThis = msg
        dsh_utils.db_print(
            'find_question_for_doctor: play this message: ' + msg.dsh_uid, 154)
        remove_from_doctor_message_list_cache(msg)
        break

    if not playThis:
        dsh_utils.db_print(
            'find_question_for_doctor: nothing to play.', 154)
        return None

    dsh_utils.db_print('find_question_for_doctor: about to play: ' +\
                       msg.dsh_uid, 154)
    return playThis



def play_question_to_doctor(caller, playThis, skipTimeName=False):
    """
    10/03/21:
    called by check_doctor_assignments().
    skipTimeName=True when the doctor presses 2 and hears it again.
    """

    chopped = get_sln_path_for_asterisk(playThis)
    dsh_utils.db_print('play_question_to_doctor: playing: ' +\
                       repr(chopped), 154)

    if not chopped:
        message = 'dsh_django2.play_question_to_doctor: ' +\
                  'unable to find .sln file: ' + repr(playThis)
        dsh_agi.report_event(message, reportLevel='ERR',
                             sessionID=get_session())
        dsh_utils.give_bad_news(message, logging.error)
        return None

    #
    # this is for computing whether it should be considered "heard"
    # if hung up early.
    globals4signal['db_out_obj'] = playThis

    if not skipTimeName:
        dsh_common_agi.say_date(playThis)
        say_message_from_name(playThis.owner)

    beginTime = datetime.datetime.now()
    globals4signal['begin_play_time'] = beginTime

    dsh_agi.say_it(chopped)
    endTime = datetime.datetime.now()
    time.sleep(1)
    deltaSeconds = (endTime - beginTime).seconds

    dsh_agi.report_event(
        'question message heard by a doctor.',
        item=playThis,
        action='HERD',
        phone_number=caller.phone_number,
        owner=caller,
        call_duration=deltaSeconds,
        sessionID=get_session())
    dsh_utils.give_news(
        'dsh_django2.play_question_to_doctor: question ' +\
        'heard by a doctor: ' + playThis.dsh_uid, logging.info)

    dsh_agi.say_it('beep')
    dsh_agi.say_it('beep')
    return playThis



def add_doctor_answer_fields(item, sessionID=''):
    """
    10/03/24:
    called by hangup_signal_handler().
    if it was a doctor recording a reply, we put a little more in the
    item to be saved.
    """
    global globals4signal
    
    if not globals4signal['doctor_record']:
        return
    
    dsh_common_db.add_key_word_to_item(
        item, 'answers', "doctor's answers",
        Item, KeyWord, sessionID=sessionID)
    dsh_common_db.make_incoming_doctor_answer_personalized_reply(
        item, sessionID=sessionID)



def put_doctor_answer_event(item, sessionID=''):
    """
    10/03/25:
    moved to dsh_common_db.py
    so it can also be called after uploading answer from the web.
    10/03/24:
    called by hangup_signal_handler().
    if it was a doctor recording a reply, and if the recorded ruation is
    long enough, we should put an answered event in the Event table.
    returns True if it's indeed an answer event and it's successfully put in.
    """
    global globals4signal
    
    if not globals4signal['doctor_record']:
        dsh_utils.db_print('put_doctor_answer_event: not from a doctor.', 154)
        return False

    return dsh_common_db.put_doctor_answer_event(
        item, Event, sessionID=sessionID)



def say_doctor_goodbye():
    """
    10/04/04
    """
    promptDir = dsh_config.lookup('DSH_PROMPT_DIR')
    finished = os.path.join(
        promptDir, dsh_config.lookup('DSH_PROMPT_DOCTOR_FINISHED'))
    dsh_agi.say_it(finished)
    dsh_utils.db_print('say_doctor_goodbye: hungup!', 154)
    dsh_agi.send_command('HANGUP\n', caller='dsh_django2:')
    time.sleep(2)
    dsh_utils.db_print('say_doctor_goodbye: shouldnt get here.', 154)
    


def record_doctor_reply(caller, playedThis, sayPress1=False):
    """
    10/03/21:
    called by check_doctor_assignments().
    records a reply by the doctor.
    playedThis was the question that was played.
    modeled after the bit for setting up recording in
    handle_regular_caller()
    returns success,
    result not really used.
    sayPress1=True when there are messages.
    """
    global globals4signal

    #
    # say one more prompt for recording.
    #
    promptDir = dsh_config.lookup('DSH_PROMPT_DIR')
    pleaseRecord = os.path.join(
        promptDir, dsh_config.lookup('DSH_PROMPT_DOCTOR_PLEASE_RECORD'))
    dsh_agi.say_it(pleaseRecord)

    dsh_utils.db_print('record_doctor_reply: press1: ' + repr(sayPress1), 154)
    if sayPress1:
        press1 = os.path.join(
            promptDir, dsh_config.lookup('DSH_PROMPT_DOCTOR_PRESS1_RECORD'))
        dsh_agi.say_it(press1)
    
    dsh_agi.say_it('beep')
    dsh_agi.say_it('beep')
    time.sleep(1)

    prepareResult = prepare_input_file(caller, playedThis)
    if not prepareResult:
        return False

    #
    # record it.
    #
    globals4signal['start_record'] = datetime.datetime.now()
    inVobj,incomingFullName = prepareResult
    dsh_agi.record(incomingFullName, allowStopButton=True, stopButton='1')

    #
    # I only get here when time limit is exhausted.
    # 10/04/04:
    # now we can get here because of the pushing of the stop button.
    #10/04/05
    #time.sleep(1)
    dsh_utils.give_news('dsh_django2.record_doctor_reply: recording ends, '+\
                        'no hangup.')
    #say_goodbye()

    #
    # forcing a hangup.
    # otherwise, possible re-arming the .call file doesn't work, because
    # the current .call file is still alive and will be deleted after
    # hangup.
    # 10/04/04:
    # no hangup due to looping.
    #
    #dsh_agi.send_command('HANGUP\n', caller='dsh_django2:')
    #10/04/05:
    #time.sleep(1)
    #
    # we shouldn't get here any more, because of the forced hangup above.
    #
    #message = 'dsh_django2.record_doctor_reply: unexpected: ' +\
    #          'after forced hangup.'
    #dsh_utils.give_bad_news(message, logging.warning)
    #dsh_agi.report(message, reportLevel='CRT')


    wait3sec = os.path.join(
        promptDir, dsh_config.lookup('DSH_PROMPT_DOCTOR_WAIT_3SEC'))
    dsh_agi.say_it(wait3sec)
    
    
    hangup_signal_handler(0, None, hungup=False)

    del globals4signal['start_record']
    
    #
    # XXX
    # stuff to do: need to add an "answered" event,
    # if the recorded stuff is long enough.
    # need to call record from the place that tried to play assignments:
    # still need to call record even if there were no assignments.
    #
    return True



def remove_from_doctor_message_list_cache(removeThis):
    """
    10/04/04
    called by find_question_for_doctor().
    remove the ones that just got heard in a series of questions played to
    a doctor.
    """
    global globals4signal

    if not globals4signal.has_key('doctor_message_list_cache'):
        return

    currentCache = globals4signal['doctor_message_list_cache']
    if not currentCache:
        return

    answer = []
    for msg in currentCache:
        if msg.dsh_uid == removeThis.dsh_uid:
            continue
        answer.append(msg)

    globals4signal['doctor_message_list_cache'] = answer
    


def check_doctor_assignments(caller, firstIteration=False):
    """
    10/03/20:
    called by handle_doctor_caller().
    check questions assigned to a doctor.
    modeled after check_personalized_messages().
    returns whether the calling function should try to record.
    if we already did record here, the calling function won't try to record.
    if we didn't, the calling function will try to record,
    because there was no question for this doctor so the
    doctor is just recording an unsolicited reply.
    10/04/04:
    rewritten to support looping.
    returns (nothingAtBeginning,keepGoing)
    """

    global globals4signal

    playThis = find_question_for_doctor(caller)
    if not playThis:
        #
        # no message for this doctor.
        # the calling function should try to record.
        #
        if firstIteration:
            return (True, False)
        #
        # we've looped over questions but now we're dry.
        # I should probably put some goodbye messages here.
        # (False, False) basically says parent shouldn't attempt to record
        # and the parent should stop looping.
        #
        #say_goodbye()
        say_doctor_goodbye()
        return (False, False)
    
    doctorChoicePrompt = os.path.join(
        dsh_config.lookup('DSH_PROMPT_DIR'),
        dsh_config.lookup('DSH_PROMPT_DOCTOR_PRESS2'))
    timeOut1 = dsh_config.lookup('DSH_PROMPT_WAIT1')
    skipTimeName = False
    
    while True:

        played = play_question_to_doctor(caller, playThis,
                                         skipTimeName=skipTimeName)
        if not played:
            #
            # something wrong happened during playing.
            # we should just end the call--no recording.
            #
            return (False, False)

        choice = dsh_agi.get_digits(doctorChoicePrompt, 1, timeOut=timeOut1)
        dsh_utils.db_print('check_doctor_assignments: choice is: ' +\
                           repr(choice), 154)

        if choice == None or choice == '' or choice == '*':
            say_goodbye()
            return (False, False)

        if choice == '1':
            break

        if choice == '2':
            #
            # play the question again.
            #
            skipTimeName = True
            continue

        #
        # if we get here, it's a timeout.
        # choice looks like something like "timeout".
        #
        break

    dsh_utils.db_print('check_doctor_assignments: about to record here.', 154)
    record_doctor_reply(caller, playThis, sayPress1=True)
    return (False, True)
            


def handle_doctor_caller(caller, unknownOrg, unknownPerson):
    """
    10/03/20.
    let doctors listen to assigned messages,
    and record replies.
    10/04/04.
    change to allow multiple questions.
    """
    global globals4signal
    globals4signal['doctor_record'] = True
    welcome_doctor(caller)

    firstIteration = True
    while True:
        nothingAtBeginning,keepGoing = check_doctor_assignments(
            caller, firstIteration=firstIteration)
        if not keepGoing:
            break
        firstIteration = False

    if nothingAtBeginning:
        #
        # there was no message at all for the doctor from the beginning.
        # just go straight to recording.
        #
        record_doctor_reply(caller, None)
        say_doctor_goodbye()



def conference_call(caller, unknownOrg, unknownPerson):
    """called by handle_staff_caller().
    initially modeled after forward_outgoing_call()"""
    
    global globals4signal

    prepareResult = prepare_input_file(caller)
    if not prepareResult:
        return False
    inVobj,incomingFullName = prepareResult

    fileName = incomingFullName
    fileFormat = dsh_config.lookup('record_file_format')
    command = 'EXEC Monitor %s|%s|m\n' % (fileFormat, fileName)
    res = dsh_agi.send_command(command, 'dsh_agi.exec_com: ', True)
    
    command = 'EXEC MeetMe 236|dr\n'
    res = dsh_agi.send_command(command, 'conference_call: ', True)

    command = 'EXEC StopMonitor\n'
    res = dsh_agi.send_command(command, 'conference_call: ', True)
    
    say_goodbye()
    hangup_signal_handler(0, None)
    return res
        


def handle_staff_caller(caller, unknownOrg, unknownPerson):

    count = 0
    staffChoicePrompt = os.path.join(
        dsh_config.lookup('DSH_PROMPT_DIR'),
        dsh_config.lookup('DSH_PROMPT_ENTER_CHOICE'))
    timeOut1 = dsh_config.lookup('DSH_PROMPT_WAIT1')
    maxRetries = dsh_common_config.lookup2('STAFF_RETRIES')
    
    while True:
        count += 1

        if count > maxRetries:
            say_goodbye()
            return True
        
        choice = dsh_agi.get_digits(staffChoicePrompt, 1, timeOut=timeOut1)
        dsh_utils.db_print('dsh_django2: the choice is: ' + repr(choice),
                           110)
        if choice == None or choice == '' or choice == '*':
            say_goodbye()
            return True

        if choice == '1':
            result = handle_regular_caller(caller)
            return True

        if choice == '2':
            result = forward_outgoing_call(caller, unknownOrg, unknownPerson)
            return result

        if choice == '3':
            result = play_recent(caller)
            return result

        if choice == '4':
            caller = dsh_common_test.patch_caller_as_DIET(
                caller, 'DIET', KeyWord, get_session())
            result = handle_regular_caller(caller)
            return result

        if choice == '5':
            result = dsh_common_test.test_demo_reply(
                caller,
                dv2.db.models.Item,
                dv2.db.models.KeyWord,
                dv2.db.models.Event,
                get_session())
            return result

        if choice == '6':
            result = dial_now(
                caller, unknownOrg, unknownPerson,
                dv2.db.models,
                get_session())
            return result

        if choice == '7':
            result = conference_call(caller, unknownOrg, unknownPerson)
            return result

        if choice == '8':
            result = call_scratch_number(caller, unknownOrg, unknownPerson)
            return result

        if choice == '9':
            #result = dsh_common_test.test_call_say_time(caller)
            #result = dsh_common_test.test_caller_has_any_message_at_all(
            #    caller,
            #    dv2.db.models.Item,
            #    dv2.db.models.KeyWord,
            #    dv2.db.models.Event,
            #    sessionID=get_session())
            #result = dsh_common_test.test_demo_reply(
            #    caller,
            #    dv2.db.models.Item)
            say_goodbye()
            return result

        continue

    return True
    

    
def dial_now(caller, unknownOrg, unknownPerson, models, sessionID):
    """
    10/04/10: called by dsh_django2.handle_staff_caller().
    do a dial-now on the number entered in the key pad.
    modeled after dsh_django2.forward_out_going_call()
    """

    funcName = 'dsh_django2.dial_now:'
    timeOut11 = dsh_config.lookup('DSH_PROMPT_WAIT11')
    voicePrompt = os.path.join(
        dsh_config.lookup('DSH_PROMPT_DIR'),
        dsh_config.lookup('DSH_PROMPT_PHONE_NUMBER'))

    promptDir = dsh_common_config.lookup('DSH_PROMPT_DIR')
    demoSending = dsh_common_config.lookup('DSH_PROMPT_DEMO_DIAL_IN8')
    demoSending = os.path.join(promptDir, demoSending)
    
    while True:
    
        #
        # get the callee number from the caller.
        #
        callNum = dsh_agi.get_digits(
            voicePrompt, 11, timeOut=timeOut11)
        if callNum == None or callNum == '':
            continue
        if callNum == '*':
            say_goodbye()
            return True

        dsh_utils.db_print('%s: the number is %s' % (funcName, callNum), 168)

        #
        # look up the callee in the database.
        #
        lookupResult = lookup_number_in_db(None, useThisNumber=callNum)
        callee = determine_unknown_caller(unknownOrg, unknownPerson,
                                          lookupResult, syncCallee=True)
        dsh_utils.db_print('%s: the callee determined to be: %s' %\
                           (funcName, repr(callee)), 168)


        message = '%s phone number: %s, name: %s' %\
                  (funcName, callNum, callee.__unicode__())
        dsh_agi.report_event(
            message,
            action='DEM2',
            item=callee,
            phone_number=callNum,
            owner=caller,
            sessionID=sessionID)
        dsh_utils.give_news(message, logging.info)
        

        #
        # taken from later parts of dsh_common_db.attempt_demo_reply_now().
        #
        success,msg = dsh_common_agi.make_dot_call_file(
            callee, sessionID=sessionID)

        #
        # taken from later parts of dsh_common_agi.demo_reply_prompt_confirm()
        #
        dsh_agi.say_it(demoSending)
        say_goodbye()
        return success


        
def main():
    global globals4signal

    globals4signal['session_id'] = dv2.db.models.assign_dsh_uid()
    globals4signal['start_time'] = datetime.datetime.now()

    init_log()

    #
    # find or create unknown org and unknown person.
    #
    try:
        unknownOrg,unknownPerson = dsh_agi.init_unknown_org_person(
            sessionID = get_session())
    except:
        message = 'dsh_django: init_unknown_org_person failed.'
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT',
                             sessionID=get_session())
        sys_exit(1)

    #
    # get the AGI environment variables.
    #
    env = dsh_agi.read_env()
    if env == {}:
        dsh_utils.give_bad_news('dsh_django1: failed to read agi envs.',
                                logging.error)
        sys_exit(1)

    dsh_config.init(env)
    

    #
    # look up the phone number in the django database.
    # if not found in the database, we do something about unknown callers.
    # XXX
    #lookupResult = lookup_number_in_db(env, debugCheat=True)
    lookupResult = lookup_number_in_db(env)
    caller = determine_unknown_caller(unknownOrg, unknownPerson, lookupResult)
    dsh_utils.db_print('dsh_django1: the caller determined to be: ' +
                       repr(caller), 110)
    globals4signal['caller_dude'] = caller


    #
    # 10/04/14:
    # add an event for me to track the last time a person had done
    # something on the system.
    #
    dsh_agi.report_event(
        'call received.',
        action='ENTR',
        owner=caller,
        phone_number=caller.phone_number,
        sessionID=get_session())


    #
    # setting up signal handler for hangup.
    # the handler will attempt to do the file format conversion.
    # and then saving into the django database.
    #
    # note: the hangup handler attempts conversion.
    # note: sys_exit() attempts to calculation call duration and
    #       put event in the event table.
    #
    signal.signal(signal.SIGHUP, hangup_signal_handler)

    #
    #XXX
    #
    if caller.ptype == 'TST':
        success = handle_staff_caller(caller, unknownOrg, unknownPerson)
        if success:
            sys_exit(0)
        sys_exit(1)

    #if caller.ptype == 'DOC':
    if caller.ptype == dsh_config.lookup('DOCTOR_TYPE'):
        success = handle_doctor_caller(caller, unknownOrg, unknownPerson)
        if success:
            sys_exit(0)
        sys_exit(1)

    if lookupResult:
        callType = lookupResult[2]
    else:
        callType = None
    if not handle_regular_caller(caller, callType=callType):
        sys_exit(1)
    sys_exit(0)
        

    

if __name__ == '__main__':
    main()
