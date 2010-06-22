#
# initially modeled after dsh_selection.py (10/01/12)
#
import sys,os,subprocess,logging
import dsh_django_config,dsh_django_utils,dsh_db_config
import dsh_django_utils2
dsh_django_utils2.append_to_sys_path(
    dsh_django_config.lookup('DSH_VOICE_CODE_DIR'))
import dsh_utils,dsh_agi
import dsh_common_db,dsh_common_agi



def process_selection(selectedItems, fieldStr, action='set'):
    """
    called by dsh_selection.process_selection().
    initially modeled after dsh_selection.star().
    selectedItems is a list of selected items.
    passed in as arguments because we are selecting different types of
    objects.
    filedStr is something like "starred" or "active" or "peer_shared".
    they are fields defined in db/models.py.
    action is either "set" or "clear".
    returns the html response string to be displayed.
    """
    
    response = ''
    
    if not selectedItems:
        response += dsh_utils.red_error_break_msg(
            'no item selected currently.')
        return response

    count = 0
    changedIds = []
    for item in selectedItems:

        try:
            valCurr = getattr(item, fieldStr)
        except:
            message = 'dsh_common_selection.process_selection(): ' + \
                      'getattr() failed: ' + item.dsh_uid + ', fieldStr: ' +\
                      fieldStr
            dsh_django_utils.error_event(message, errorLevel='CRT')
            response += dsh_utils.red_error_break_msg(message)
            return response

        valChange = False
        if action == 'set':
            if valCurr:
                continue
            valNew = True
            valChange = True
        else:
            #
            # it's 'clear'.
            #
            if not valCurr:
                continue
            valNew = False
            valChange = True

        if not valChange:
            #
            # not really necessary...
            #
            continue
        try:
            setattr(item, fieldStr, valNew)
            item.save(noLogging=True)
            count += 1
            changedIds.append(item.dsh_uid)
        except:
            message = 'dsh_common_selection.process_selection: ' +\
                      'failed to save: ' +\
                      item.dsh_uid + ', fieldStr: ' + fieldStr
            dsh_django_utils.error_event(message, errorLevel='CRT')
            response += dsh_utils.red_error_break_msg(message)
            return response

    if action == 'set':
        actDone = 'set'
    else:
        actDone = 'cleared'
        

    message = '%s item(s) %s. ' % (str(count), actDone)
    messageLog = 'dsh_common_selection.process_selection(): ' + message
    messageLog += 'fieldStr: ' + fieldStr + '. '
    if count:
        messageLog += 'items: ' + repr(changedIds)
    response += dsh_utils.black_break_msg(message)
    dsh_agi.report_event(messageLog)

    return response



def keyword_select(dshUid, keyWordTable, itemTable, action='select'):
    """
    10/03/14:
    called by dsh_common_views.keyword_select().
    add the keyworded items to the current selection.
    returns (success, response)
    """

    response = ''

    keyword = dsh_django_utils.get_foreign_key(keyWordTable, dshUid)
    if not keyword:
        message = 'dsh_common_selection.keyword_select: no such dsh_uid: ' +\
                  dshUid
        response += dsh_utils.red_error_break_msg(message)
        dsh_django_utils.error_event(message, errorLevel='ERR')
        return (False, response)

    response += dsh_utils.black_break_msg(
        'The key word is: "' + keyword.key_word + '".')

    items = itemTable.objects.filter(key_words__dsh_uid__exact=dshUid)
    if not items:
        message = 'dsh_common_selection.keyword_select: ' +\
                  'no messages with this key word.'
        response += dsh_utils.red_error_break_msg(message)
        return (False, response)

    response += dsh_utils.black_break_msg(
        'Number of messages with this key word: ' + str(len(items)) + '.')

    #
    # the stuff below is copied from dsh_selection.keyword_select_starred().
    #
    count = 0
    for item in items:

        if action == 'deselect':
            if not item.u17:
                continue
            item.u17 = False
        else:
            if item.u17:
                continue
            item.u17 = True

        try:
            item.save(noLogging=True)
            count += 1
        except:
            message = 'dsh_common_selection.keyword_select: failed to save: '+\
                      item.dsh_uid
            dsh_django_utils.error_event(message, errorLevel='CRT')
            response += dsh_utils.red_error_break_msg(message)
            return (False, response)

    if action == 'deselect':
        message = 'Items removed from the selection: '
    else:
        message = 'Items added to the selection: '
    message += str(count) + '.'
    response += dsh_utils.black_break_msg(message)
    dsh_agi.report_event(message)
    
    return (True, response)



def process_selected_people_current_dial(personTable, action='set'):
    """
    10/03/22.
    called by dsh_common_views.set_current_dial_sel().
    set or clear the current_dial flag of the selected people.
    """

    response = ''

    people = personTable.objects.filter(u17=True)

    count = 0
    for person in people:
        if action == 'set':
            if person.current_dial:
                continue
            person.current_dial = True
        elif action == 'clear':
            if not person.current_dial:
                continue
            person.current_dial = False
        else:
            break

        try:
            person.save(noLogging=True)
            count += 1
        except:
            message = 'dsh_common_selection.' +\
                      'process_selected_people_current_dial: ' +\
                      'failed to save person: ' + person.dsh_uid
            dsh_django_utils.error_event(message, item=person,
                                         errorLevel='CRT')
            response += dsh_utils.red_error_break_msg(message)
            return response

    if action == 'set':
        message = 'People added to the current dial set: '
    elif action == 'clear':
        message = 'People removed from the current dial set: '
    else:
        message = ''

    if message:
        message += str(count) + '.'
    response += dsh_utils.black_break_msg(message)
    dsh_agi.report_event(message)

    return response



def select_current_dial_set(personTable, action='set'):
    """
    10/03/22.
    called by dsh_common_views.select_current_dial_set().
    add/remove the people in the current dial set to/from
    the current selection.
    basically copied from process_selected_people_current_dial().
    """
    
    response = ''

    people = personTable.objects.filter(current_dial=True)

    count = 0
    for person in people:
        if action == 'set':
            if person.u17:
                continue
            person.u17 = True
        elif action == 'clear':
            if not person.u17:
                continue
            person.u17 = False
        else:
            break

        try:
            person.save(noLogging=True)
            count += 1
        except:
            message = 'dsh_common_selection.' +\
                      'select_current_dial_set: ' +\
                      'failed to save person: ' + person.dsh_uid
            dsh_django_utils.error_event(message, item=person,
                                         errorLevel='CRT')
            response += dsh_utils.red_error_break_msg(message)
            return response

    if action == 'set':
        message = 'People added to the current selection: '
    elif action == 'clear':
        message = 'People removed from the current selection: '
    else:
        message = ''

    if message:
        message += str(count) + '.'

    response += dsh_utils.black_break_msg(message)
    dsh_agi.report_event(message)

    return response



def reschedule_current_dial_set(personTable,
                                tinyResponse=False,
                                sessionID=None):
    """
    10/03/22.
    called by dsh_common_views.reschedule().
    and dsh_reschedule.py
    tinyResponse==True when called by dsh_reschedule.py.
    it just returns the number of people scheduled in that case.
    """

    response = ''

    people = personTable.objects.filter(current_dial=True)

    if not people:
        response += dsh_utils.black_break_msg(
            'No person in the current dial set.')
        if tinyResponse:
            return 0
        return response

    dsh_utils.black_break_msg('Processing the following people...')

    count = 0
    for person in people:
        calleeInfo = '<span style="white-space: nowrap;">' +\
                     dsh_django_utils.callee_info(person) + '</span>'
        response += dsh_utils.black_break_msg(calleeInfo)
        scheduled,strMsg = dsh_django_utils.check_auto_timed_calls_for_person(
            person, noLogging=True)
        if scheduled:
            strMsg = '&nbsp;&nbsp;&nbsp;&nbsp; scheduled: ' + strMsg
        else:
            strMsg = '&nbsp;&nbsp;&nbsp;&nbsp; not scheduled: ' + strMsg
        response += dsh_utils.black_break_msg(strMsg)
        count += 1

    countMsg = dsh_utils.black_break_msg(
        'number of people in the dial set processed: ' +\
        str(count) + '.')
    response += countMsg
    dsh_agi.report_event(countMsg, sessionID=sessionID)

    if tinyResponse:
        return count
    return response



def reschedule_script_call(personTable):
    """
    10/03/22:
    called by dsh_reschedule.py
    which is in turn invoked by crontab
    """

    sessionID = dsh_common_db.make_session_id()
    dsh_common_agi.auto_schedule_delete_all(sessionID=sessionID)

    disabled = dsh_db_config.get('auto_dial_disable')
    if disabled:
        count = reschedule_current_dial_set(
            personTable, tinyResponse=True, sessionID=sessionID)
        message = 'dsh_reschedule.py: processing current dial set: ' +\
                  str(count)
        dsh_utils.give_news(message, logging.info)
    else:
        dsh_django_utils.check_auto_timed_calls_for_all_persons(noLogging=True)
        
    message = 'triggered by dsh_reschedule.py.  done'
    dsh_agi.report_event(message, action='RESC', sessionID=sessionID)
    dsh_utils.give_news(message, logging.info)



def select_keyed_persons(personTable, keyWordTable, dshUid, action='set'):
    """
    10/03/22:
    modeled after keyword_select(). could've combined them but I'm lazy.
    called by dsh_common_views.select_keyed_persons().
    add the keyworded persons to the current selection.
    returns (success, response)
    """

    response = ''

    keyword = dsh_django_utils.get_foreign_key(keyWordTable, dshUid)
    if not keyword:
        message = 'dsh_common_selection.select_keyed_persons: ' +\
                  'no such dsh_uid: ' + dshUid
        response += dsh_utils.red_error_break_msg(message)
        dsh_django_utils.error_event(message, errorLevel='ERR')
        return (False, response)

    response += dsh_utils.black_break_msg(
        'The key word is: "' + keyword.key_word + '".')

    persons = personTable.objects.filter(
        person_key_words__dsh_uid__exact=dshUid)
    if not persons:
        message = 'dsh_common_selection.select_keyed_persons: ' +\
                  'no person with this key word.'
        response += dsh_utils.red_error_break_msg(message)
        return (False, response)

    response += dsh_utils.black_break_msg(
        'Number of persons with this key word: ' + str(len(persons)) + '.')

    #
    # the stuff below is copied from dsh_selection.keyword_select_starred().
    #
    count = 0
    for person in persons:

        if action == 'clear':
            if not person.u17:
                continue
            person.u17 = False
        else:
            if person.u17:
                continue
            person.u17 = True

        try:
            person.save(noLogging=True)
            count += 1
        except:
            message = 'dsh_common_selection.select_keyed_persons: ' +\
                      'failed to save: '+ item.dsh_uid
            dsh_django_utils.error_event(message, errorLevel='CRT')
            response += dsh_utils.red_error_break_msg(message)
            return (False, response)

    if action == 'clear':
        message = 'Items removed from the selection: '
    else:
        message = 'Items added to the selection: '
    message += str(count) + '.'
    response += dsh_utils.black_break_msg(message)
    dsh_agi.report_event(message)
    
    return (True, response)



def add_person_key_word(personTable, keyWordTable, dshUid, action='set'):
    """
    10/03/22:
    copied from dsh_selection.keyword_add_del()
    called by dsh_common_view.add_person_keyword()"""
    
    errorMsg = ''
    keyWord = dsh_django_utils.get_foreign_key(keyWordTable, dshUid)
    if not keyWord:
        message = 'dsh_common_selection.add_person_key_word: ' +\
                  'bad key word dshUid: ' + repr(dshUid)
        dsh_django_utils.error_event(message, errorLevel='ERR')
        errorMsg += dsh_utils.red_error_break_msg(message)
        return errorMsg

    selectedPersons = personTable.objects.filter(u17=True)
    if not selectedPersons:
        errorMsg += dsh_utils.red_error_break_msg(
            'no person selected currently.')
        return errorMsg

    count = 0
    for person in selectedPersons:
        kwList = person.person_key_words.all()
        if action == 'set':
            if keyWord in kwList:
                continue
            try:
                person.person_key_words.add(keyWord)
                person.save(noLogging=True)
                count += 1
            except:
                message = 'dsh_common_selection.add_person_key_word: ' +\
                          'key word add ' +\
                          'failed: ' + repr(dshUid)
                dsh_django_utils.error_event(message, errorLevel='CRT')
                errorMsg += dsh_utils.red_error_break_msg(message)
                return errorMsg
        elif action == 'clear':
            if not (keyWord in kwList):
                continue
            try:
                person.person_key_words.remove(keyWord)
                person.save(noLogging=True)
                count += 1
            except:
                message = 'dsh_common_selection.add_person_key_word: ' +\
                          'key word del ' +\
                          'failed: ' + repr(dshUid)
                dsh_django_utils.error_event(message, errorLevel='CRT')
                errorMsg += dsh_utils.red_error_break_msg(message)
                return errorMsg
        else:
            return dsh_utils.red_error_break_msg('bad action: ' + action)

    if action == 'set':
        actDone = 'added to'
        logAction = 'KADD'
    elif action == 'clear':
        actDone = 'removed from'
        logAction = 'KDEL'
    else:
        return dsh_utils.red_error_break_msg('bad action: ' + action)

    keyStr = keyWord.key_word
    message = 'key word "%s" %s %s persons.' % (keyStr, actDone, str(count))
    errorMsg += dsh_utils.black_break_msg(message)

    dsh_agi.report_event(
        message,
        action=logAction,
        item=keyWord)
    
    return errorMsg



def clear_current_dial_set(personTable):
    """
    10/03/22:
    called by dsh_common_views.clear_current_dial_set().
    """

    response = ''
    people = personTable.objects.filter(current_dial=True)

    count = 0
    for person in people:
        person.current_dial = False

        try:
            person.save(noLogging=True)
            count += 1
        except:
            message = 'dsh_common_selection.clear_current_dial_set: ' +\
                      'failed to save person: ' + person.dsh_uid
            dsh_django_utils.error_event(message, item=person,
                                         errorLevel='CRT')
            response += dsh_utils.red_error_break_msg(message)
            return response

    response += dsh_utils.black_break_msg(
        'number of people removed from the current dial set: ' +\
        str(count) + '.')
    return response
