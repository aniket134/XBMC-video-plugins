import logging,sys,re,time,random,os,os.path
import dsh_common_config,dsh_common_utils,dsh_common_agi

dsh_common_utils.add_to_sys_path(dsh_common_config.lookup('django_sys_paths'))
__import__(dsh_common_config.lookup('APP_NAME_MODELS'))
import dsh_agi,dsh_config,dsh_utils,dsh_django2
import dsh_common_agi, dsh_common_db
os.environ['DJANGO_SETTINGS_MODULE'] = dsh_common_config.lookup(
    'DJANGO_SETTINGS_MODULE')



def test_call_say_time(caller):
    """called by handler_staff_caller().
    test spoken dates.
    """

    dsh_utils.db_print('test_call: entered...', 134)
    answer = dsh_django2.get_outgoing_voice_from_db(caller)
    if not answer:
        dsh_utils.give_bad_news(
            'test_call: get_outgoing_voice_from_db() failed.',
            logging.critical)
        return False
    outVobj,outgoingVoice,allSharedHeard,playShared = answer
    dsh_utils.db_print('test_call: outgoingVoice: ' + outgoingVoice, 134)
    time = outVobj.modify_datetime
    timeStr = time.strftime('%#Y-%#m-%#d')
    dsh_utils.db_print('test_call: timeStr: ' + timeStr, 134)
    dsh_common_agi.say_date(outVobj)
    return True



def test_DIET(caller, itemTable, keyWordTable, sessionID):
    """called by handler_staff_caller().
    test DIET-related features.
    """

    #
    # test when the supplied key word is not defined.
    #
    #dsh_common_db.get_active_broadcast_item(
    #    itemTable, keyWordTable, sessionID, keyWordStr='no such thing')

    #
    # test using keyWordStr
    #
    #dsh_common_db.get_active_broadcast_item(
    #    itemTable, keyWordTable, sessionID, keyWordStr='DIET')
    
    #
    # test with keyWordObj
    #dsh_common_db.get_active_broadcast_item_for_caller(
    #    caller, itemTable, keyWordTable, sessionID)

    #
    # test peer-shared
    #
    dsh_common_db.get_peer_shared_item_for_caller(
        caller, itemTable, keyWordTable, sessionID)
    return True



def patch_caller_as_DIET(caller, keyWordStr, keyWordTable, sessionID):
    """called by handle_staff_caller().
    pretend the caller to be for DIET.
    patch its organization to add a DIET flag.
    somewhat modeled after: get_active_broadcast_item().
    returns the patched caller.
    """

    keyWords = keyWordTable.objects.filter(key_word=keyWordStr)
    if keyWords:
        dsh_utils.db_print(
            'patch_caller_as_DIET: found keyword: '+ \
            repr(keyWords), 136)
        keyWord = keyWords[0]
    else:
        message = 'dsh_common_test.patch_caller_as_DIET: ' + \
                  'failed to locate this key word: ' + keyWordStr
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel='ERR',
                             sessionID=sessionID)
        return None

    caller.organization.org_key_word = keyWord
    dsh_utils.db_print('patch_caller_as_DIET: caller patched!', 136)
    return caller



def test_caller_has_any_message_at_all(caller,
                                       itemTable, keyWordTable, eventTable,
                                       sessionID=''):
    """
    called by dsh_django2.handle_staff_caller().
    tests dsh_common_agi.person_has_any_message_at_all().
    """

    hasStuff,message = dsh_common_agi.person_has_any_message_at_all(
        caller, itemTable, keyWordTable, eventTable, sessionID=sessionID)

    dsh_utils.db_print(
        'test_caller_has_any_message_at_all: ' + repr(hasStuff), 165)
    dsh_utils.db_print(
        'test_caller_has_any_message_at_all: ' + message, 165)

    return True



def test_demo_reply(caller, itemTable, keyWordTable, eventTable, sessionID):
    """
    10/04/09: called by dsh_django2.handler_staff_caller().
    """
    return dsh_common_agi.demo_reply(
        itemTable, keyWordTable, eventTable,
        fromPhone=True, sessionID=sessionID)
