import sys,os,subprocess,logging,os.path,shutil,datetime,time
import dsh_common_config,dsh_common_utils,dsh_common_agi

dsh_common_utils.add_to_sys_path(dsh_common_config.lookup('django_sys_paths'))
__import__(dsh_common_config.lookup('APP_NAME_MODELS'))
import dsh_utils,dsh_agi,dsh_config
import dsh_django_config,dsh_django_utils,dsh_db_config



def init_log(quiet=False):
    """copied from dsh_django2.py"""
    logdir = dsh_config.lookup('log_file_dir')
    logName = dsh_config.lookup('log_file_name')
    dsh_utils.check_logging(logdir, logName, quiet=quiet)



def get_active_broadcast_item(itemTable, keyWordTable,
                              sessionID,
                              keyWordObj=None,
                              keyWordStr=None):
    """
    added for DIET.
    the idea is this:
    broadcast item will have key words associated with them.
    'DIET' in this case.
    for the DIET callers, will only look for broadcast items of this
    key word.
    itemTable is dvoice.Item.  it's passed in as an argument because
    this code is in 'common' so it can't assume to know the db definition.
    similar for keyWordTable.
    the whole thing started from the original code that only has this line:
    activeBroadcastItems = Item.objects.filter(active=True, itype='B')
    
    """

    dsh_utils.db_print('get_active_broadcast_item: entered...', 136)

    #
    # get the key word object, from the database, if necessary.
    #
    if keyWordObj:
        keyWord = keyWordObj
        keyWordStr = keyWord.key_word
        dsh_utils.db_print('get_active_broadcast_item: given key: ' +\
                           repr(keyWord), 136)
    else:
        keyWord = None
    
        if keyWordStr:
            keyWords = keyWordTable.objects.filter(key_word=keyWordStr)
            if keyWords:
                dsh_utils.db_print(
                    'get_active_broadcast_item: found keyword: '+ \
                    repr(keyWords), 136)
                keyWord = keyWords[0]
            else:
                message = 'dsh_common_db.get_active_broadcast_item: ' + \
                          'failed to locate this key word: ' + keyWordStr
                dsh_utils.give_bad_news(message, logging.error)
                dsh_agi.report_event(message, reportLevel='ERR',
                                     sessionID=sessionID)
                return None

    if keyWord:
        dsh_utils.db_print('get_active_broadcast_item: has key word: ' +\
                           repr(keyWord), 136)
        broadcastItems = itemTable.objects.filter(
            active=True, itype='B', key_words=keyWord)
    else:
        dsh_utils.db_print('get_active_broadcast_item: no key word.', 136)
        broadcastItems = itemTable.objects.filter(
            active=True, itype='B')
        broadcastItems = remove_org_keyed_from_bcast_items(broadcastItems)
                                 
    if not broadcastItems:
        message = 'dsh_common_db.get_active_broadcast_item: ' + \
                  "can't find active broadcast message. "
        if keyWordStr:
            message += 'with this keyword: ' + keyWordStr
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel='ERR',
                             sessionID=sessionID)
        return None
    else:
        dsh_utils.db_print('get_active_broadcast_item: found broadcast msg:'+\
                           repr(broadcastItems), 136)

    return broadcastItems



def get_active_broadcast_item_for_caller(caller,
                                         itemTable, keyWordTable,
                                         sessionID):
    """
    like get_active_broadcast_item(), but uses caller -> org -> org_key_word
    to decide what broadcast item to look for.
    """
    
    bcstKeyWord = caller.organization.org_key_word
    bItems = get_active_broadcast_item(itemTable, keyWordTable, sessionID,
                                       keyWordObj=bcstKeyWord)
    dsh_utils.db_print('get_active_broadcast_item_for_caller: '+ \
                       repr(bItems), 136)
    return bItems



def get_peer_shared_item_for_caller(caller,
                                    itemTable,
                                    keyWordTable,
                                    sessionID,
                                    getOwn=False):
    """
    like the above but get peer-shared stuff instead.
    getOwn is True when we are getting one's own peer-shared items.
    used to be a line like:
    sharedList = Item.objects.filter(peer_shared=True)
    or
    sharedList = Item.objects.filter(peer_shared=True, owner=caller)
    to be called from dsh_django2.py
    """

    dsh_utils.db_print(
        'get_peer_shared_item_for_caller: entered, for own: ' +\
        repr(getOwn), 136)
    
    keyWord = caller.organization.org_key_word
    keyWordStr = None
    
    if keyWord:
        keyWordStr = keyWord.key_word

        if getOwn:
            peerItems = itemTable.objects.filter(
                peer_shared=True, owner=caller,
                owner__organization__org_key_word=keyWord)
        else:
            peerItems = itemTable.objects.filter(
                peer_shared=True,
                owner__organization__org_key_word=keyWord)
            dsh_utils.db_print(
                'get_peer_shared_item_for_caller: purely peer items: ' +\
                str(len(peerItems)), 136)
                
            #
            # if we turn a Khomeini message into peer-shared,
            # she won't belong to that keyed org.
            # so we have to look for the bcast key flag.
            #
            moreItems = itemTable.objects.filter(
                peer_shared=True,
                key_words=keyWord)
            dsh_utils.db_print(
                'get_peer_shared_item_for_caller: extra items: ' +\
                str(len(moreItems)), 136)
            peerItems = peerItems | moreItems
            peerItems = peerItems.distinct()
            #peerItems = chain(peerItems, moreItems)
            dsh_utils.db_print(
                'get_peer_shared_item_for_caller: total items: ' +\
                str(len(peerItems)), 136)
            
    else:
        #
        # the caller does not belong to a keyed org.
        #
        if getOwn:
            peerItems = itemTable.objects.filter(
                peer_shared=True, owner=caller)
        else:
            #
            # the caller does not belong to a keyed org.
            # so the returned peer-shared messages can't belong to keyed org.
            #
            peerItems = itemTable.objects.filter(
                peer_shared=True,
                owner__organization__org_key_word__isnull=True)
        
    if peerItems:
       dsh_utils.db_print(
           'get_peer_shared_item_for_caller: key word: ' +\
           repr(keyWordStr) + ', items: ' + repr(peerItems), 136)
       dsh_utils.db_print(
           'get_peer_shared_item_for_caller: number of shared items: ' +\
           str(len(peerItems)), 136)

    return peerItems



def models_org_key_link(me):
    """used to be in models.py.
    from Organization.org_key_link(self)
    """
    
    keyWord = me.org_key_word
    if not keyWord:
        return ''

    keyWordLookupURL = dsh_django_config.lookup('KEY_WORD_URL')
    keyWordLookupURL += str(keyWord.id)
    return '<a href="%s">%s</a>' % (keyWordLookupURL, keyWord.key_word)



def models_keyword_org_key_icon(me):
    """
    called by models.KeyWord.org_key_icon().
    modeled after models.KeyWord.keyed_items().
    """

    if not me.org_key:
        return ''

    url = dsh_common_config.lookup2('KEYED_ORGS_URL') + str(me.id)
    icon = dsh_common_config.lookup2('KEYED_ORGS_ICON')
    ans = ('<a href="%s" ' + \
          'title="organizations that are keyed by this group keyword">' +\
          '%s</a>') % (url, icon)
    spaces = dsh_django_config.lookup('ICON_SPACES')
    return ans + spaces



def remove_org_keyed_from_bcast_items(items):
    """
    called by get_active_broadcast_item().
    if an item in the list has an org key, remove it from the list.
    this is necessary, so that the default people don't hear DIET broadcasts.
    """

    ans = []

    for item in items:
        if item.key_words.filter(org_key=True):
            #
            # in this item, we found at least one key word
            # that is an org key.
            # so this doesn't belong in the list.
            #
            dsh_utils.db_print(
                'remove_org_keyed_from_bcast_items: removed item: ' + \
                repr(item), 135)
            continue
        ans.append(item)

    dsh_utils.db_print(
        'remove_org_keyed_from_bcast_items: returning: ' + repr(ans), 136)
    return ans



def deactivate_after_save(item, itemTable, recurse=False):
    """called by dsh_django_utils.deactivate().
    this is done whenever we save an item.
    try to deactivate old active items.
    the two cases here mirror the two cases in
    get_active_broadcast_item().
    """
    
    if (not item.active) or (item.itype != 'B') or recurse:
        return

    init_log(quiet=True)

    orgKeys = item.key_words.filter(org_key=True)

    if not orgKeys:
        #
        # find all the previously active broadcasts
        # that don't have org keys.
        # this is similar to the old case.
        #
        oldActives = itemTable.objects.filter(
            active=True, itype='B')
        #dsh_utils.db_print('deactivate: list 1: ' + \
        #                   repr(oldActives), 136)
        dsh_utils.db_print('deactivate: how many 1: ' + \
                           str(len(oldActives)), 136)
        oldActives = remove_org_keyed_from_bcast_items(oldActives)
        dsh_utils.db_print('deactivate: list 2: ' + \
                           repr(oldActives), 136)
        dsh_utils.db_print('deactivate: how many 2: ' + \
                           str(len(oldActives)), 136)
        deactivate_olds(item, oldActives)
        return
    
    #
    # we now know we have org keys.
    #
    for orgKey in orgKeys:
        oldActives = itemTable.objects.filter(
            active=True, itype='B', key_words=orgKey)
        dsh_utils.db_print('deactivate: list 3: ' + \
                           repr(oldActives), 136)
        dsh_utils.db_print('deactivate: how many 3: ' + \
                           str(len(oldActives)), 136)
        deactivate_olds(item, oldActives)



def deactivate_olds(item, oldActives):
    """called by deactivate() above.  recursively calls deactivate() again."""
    
    for old in oldActives:
        #
        # don't have to worry about this current one,
        # because it's not in yet.
        #
        if old.dsh_uid == item.dsh_uid:
            continue
        old.active = False
        old.save(recurse=True)
        message = 'deactivate_olds: deactivated: ' + old.dsh_uid
        dsh_utils.give_news(message)
        dsh_agi.report_event(message, item=old)



def models_stash_saved_item(me):
    """
    called by Item.save()
    stashes the recently saved Item dsh_uid in Zobject01.
    for a later signal to use it to deactivate old active objects.
    had to do this because Many-to-Many relationship can't be
    used inside save() and couldn't get any Django signal
    to work.
    """

    dsh_db_config.set('just_saved_item_dsh_uid', me.dsh_uid)



def post_item_save_signal_handler(itemTable):
    """
    called by models.post_item_save_signal_handler().
    see the comments for models_stash_saved_item() above.
    """
    
    init_log(quiet=True)
    dsh_utils.db_print('post_item_save_signal_handler: entered...', 136)
    
    dshUid = dsh_db_config.get('just_saved_item_dsh_uid')
    dsh_db_config.set('just_saved_item_dsh_uid', None)

    if not dshUid:
        return
    
    dsh_utils.db_print('post_item_save_signal_handler: dsh_uid: ' + dshUid,
                       136)

    search = itemTable.objects.filter(dsh_uid = dshUid)
    if not search:
        message = 'post_item_save_signal_handler: unable to find dsh_uid: '+\
                  dshUid
        dsh_utils.give_bad_news(message, logging.critial)
        dsh_agi.report_event(message, reportLevel='CRT')
        return

    item = search[0]

    deactivate_after_save(item, itemTable, recurse=False)



def get_forward_outgoing_channel():
    """
    mISDN/3c or mISDN/4c
    called by something in dsh_django_utils.py and dsh_agi.py.
    at the beginning, I was doing a hack for Barney.
    in dsh_config.py, if I see the hostname is Barney, then
    it's rigged to do testing with IAX2.
    now I do it in a better way.
    the channel is stashed in the global config object
    in the database.
    if I can find it in the database, it has precedence.
    if not, then use the old dsh_config.py value.
    """

    init_log(quiet=True)
    channel = dsh_db_config.get('outgoing_channel')
    if not channel:
        channel = dsh_config.lookup('FORWARD_OUTGOING_CHANNEL')
    dsh_utils.db_print('get_forward_outgoing_channel: ' + channel, 142)
    return channel



def get_outgoing_context_extension():
    """
    similar to get_forward_outgoing_channel() above.
    used by generate_dot_call_file().
    but for context and extension.
    on pnet1:
    dvoice: misdnin 510
    dv2: portfour 515
    on barney:
    dvoice: demo 510
    dv2: portfour 515
    """

    init_log(quiet=True)

    context = dsh_db_config.get('asterisk_context')
    if not context:
        context = dsh_config.lookup('OUTGOING_CONTEXT')

    extension = dsh_db_config.get('asterisk_extension')
    if not extension:
        extension = dsh_common_config.lookup2('DEFAULT_EXTENSION')

    dsh_utils.db_print('get_outgoing_context_extension: ' + context + ', '+\
                       extension, 142)
    return (context,extension)



def append_database_name_str():
    """called by dsh_django_utils.determine_dot_call_file_name().
    append a unique database name to the dot calls in the
    /var/spool/asterisk/outgoing directory."""

    init_log(quiet=True)
    databaseName = dsh_db_config.get('database_name')
    if not databaseName:
        message = 'dsh_common_db.append_database_name_str: ' +\
                  'no database name found.'
        dsh_utils.give_bad_news(message, logging.warning)
        dsh_agi.report_event(message, reportLevel='WRN')
        return ''

    databaseName = dsh_utils.strip_join_str(databaseName)
    answer = '___' + databaseName + '___'
    dsh_utils.db_print('append_database_name_str: ' + answer, 143)
    return answer



def filter_listdir_with_dbname(fileList):
    """
    called from places in dsh_django_utils.py.
    for the purpose of distinguishing dot files belonging to
    different databases in the spool directory
    /var/spool/asterisk/outgoing.
    if an item in the fileList doesn't have the database name
    as a substring, then we remove it from the list.
    """

    answer = []
    dbName = append_database_name_str()
    for fileName in fileList:
        if fileName.find(dbName) != -1:
            answer.append(fileName)
        else:
            dsh_utils.db_print('filter_listdir_with_dbname: tossing: ' +\
                               fileName, 143)
    dsh_utils.db_print('filter_listdir_with_dbname: returning: ' +
                       repr(answer), 143)
    return answer



def model_event_org(event):
    """
    add an org column for the event table.
    called from models.Event.org_link().
    """

    if not event.owner:
        return ""

    return dsh_django_utils.org_link(event.owner.organization)



def dot_call_id_to_caller(dshUid, personTable, sessionID):
    """
    10/02/27:
    called by dsh_django2.lookup_number_in_db().
    __DOT_CALL__ dsh_uid
    returns (success, caller)
    """

    caller = dsh_django_utils.get_foreign_key(personTable, dshUid)
    if not caller:
        message = 'dsh_common_db.dot_call_id_to_caller: ' +\
                  'no such caller found: ' + dshUid
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel = 'ERR', sessionID=sessionID)
        return (False, None)

    message = 'dsh_common_db.dot_call_id_to_caller: ' +\
              caller.__unicode__() + ' -- ' +\
              caller.organization.alias + ' -- ' +\
              repr(caller.phone_number)
    dsh_utils.give_news(message, logging.info)
    return (True, caller)



def model_item_reply_upload_icon(item):
    """
    10/03/06: for uploading a doctor's reply.
    modeled after models.reply_icon().
    called by models.reply_upload_icon().
    """
    url = dsh_common_config.lookup2('REPLY_UPLOAD_URL') + item.dsh_uid
    icon = dsh_common_config.lookup2('REPLY_UPLOAD_ICON')
    url = '<a href=%s title="upload reply">%s</a>' % (url, icon)
    spaces = dsh_django_config.lookup('ICON_SPACES')
    return url + spaces

        

def copy_blank_reply_into_django(djangoFullName):
    """
    called by dsh_django_utils.save_red5_mp3_in_django().
    used to copy a blank mp3 file (instead of a red5 file) into django.
    this was first initiated by views.reply_upload().
    returns (success, response)
    """

    response = ''
    
    blankReplyPath = blank_reply_path()

    if not dsh_utils.is_valid_file(blankReplyPath, silent=True):
        message = 'dsh_common_db.copy_blank_reply_into_django: ' +\
                  'blank reply does not exist: ' + blankReplyPath
        dsh_django_utils.error_event(message, errorLevel='CRT')
        response += dsh_utils.red_error_break_msg(message)
        return (False, response)

    shutil.copy(blankReplyPath, djangoFullName)
    try:
        shutil.copy(blankReplyPath, djangoFullName)
    except:
        message = 'dsh_common_db.copy_blank_reply_into_django: ' +\
                  'copy failed: ' + blankReplyPath + ' -> ' + djangoFullName
        dsh_django_utils.error_event(message, errorLevel='CRT')
        response += dsh_utils.red_error_break_msg(message)
        return (False, response)

    return (True, '')



def blank_reply_path():
    """
    used by copy_blank_reply_into_django() and
    dsh_django_utils.save_red5_mp3_in_django().
    """
    soundDir = dsh_common_config.lookup('DSH_PROMPT_DIR')
    blankReplyMp3 = dsh_common_config.lookup2('BLANK_REPLY_MP3')
    blankReplyPath = os.path.join(soundDir, blankReplyMp3)
    return blankReplyPath



def check_one_timed_call_time(callee, timed, timedType):
    """
    10/03/10:
    moved from dsh_django_utils.py.
    
    used to be schedule_next_call_time(callee),
    changed to account for which timedx field to look at.
    
    called by auto_schedule_one_callee().
    based on what the callee has specified, let's figure out
    when he should receive an auto-dialed outgoing call.
    returns (scheduled, scheduledTime)
    """

    timed1 = timed
    if not timed1 or callee.auto_dial_disabled:
        return (False, None)
    timed1Type = timedType

    now = datetime.datetime.now()

    if (timed1 < now) and (timed1Type == None or timed1Type == 'NONE'):
        #
        # scheduled to be played in the past,
        # but there's no repetition.
        # so we do nothing.
        #
        return (False, None)

    if timed1 > now:
        #
        # the first scheduled time is still in the future.
        # just schedule that time.  easy enough.
        #
        return (True, timed1)

    #
    # if we get here, timed1 is in the past.
    # and there is some sort of repetition spec:
    # hourly, daily, weekly, or monthly.
    #
    diffHour = 60*60
    diffDay = diffHour * 24
    diffWeek = diffDay * 7
    diff2Weeks = diffWeek * 2
    diffMonth = diffWeek * 4
    
    if timed1Type == 'HOUR':
        diff = diffHour
        delta = datetime.timedelta(hours=1)
    elif timed1Type == 'DAIL':
        diff = diffDay
        delta = datetime.timedelta(days=1)
    elif timed1Type == 'WEEK':
        diff = diffWeek
        delta = datetime.timedelta(days=7)
    elif timed1Type == 'BIWK':
        diff = diff2Weeks
        delta = datetime.timedelta(days=14)
    elif timed1Type == 'MONT':
        diff = diffMonth
        delta = datetime.timedelta(days=28)
    else:
        return (False, None)
    
    deltaNow = now - timed1
    diffNow = deltaNow.days * diffDay + deltaNow.seconds
    
    howManyUnits = diffNow / diff + 1
    return (True, timed1 + delta * howManyUnits)



def calculate_age(person):
    """called by demographics()."""
    if not person.date_birth:
        return 0
    today = datetime.date.today()
    diff = today - person.date_birth
    days = diff.days
    years = days / 365
    if days % 365:
        years += 1
    return years



def models_person_demographics(person):
    """
    called by models.Person().
    """
    answer = ''

    url = dsh_common_config.lookup2('DEMOGRAPHIC_URL') + person.dsh_uid
    icon = dsh_common_config.lookup2('DEMOGRAPHIC_ICON')
    url = '<a href=%s title="demographics">%s</a>' % (url, icon)
    answer += url
    answer += '<BR><BR>'
    
    if person.gender:
        answer += person.gender

    if person.date_birth:
        years = calculate_age(person)
        if answer:
            answer += ', '
        answer += str(years)

    return answer



def models_save_blank_out_bod_changes(person):
    """
    called by models_save_birth_date().
    blanks out the editable fields for the next edit.
    """
    person.date_birth_change = None
    person.birth_date_approximate_change = False
    person.age = 0



def models_save_birth_date(person):
    """
    called by models.Person.save().
    """

    if person.birth_date_approximate_change:
        person.birth_date_approximate = True
    if person.date_birth_change:
        person.date_birth = person.date_birth_change
        person.birth_date_approximate = person.birth_date_approximate_change
        models_save_blank_out_bod_changes(person)
        return

    if person.age and person.age > 0:
        today = datetime.date.today()
        birthYear = today.year - person.age
        birthDate = datetime.date(birthYear, 6, 1)
        person.date_birth = birthDate
        person.birth_date_approximate = True
        models_save_blank_out_bod_changes(person)
        


def models_keyed_sel(keyword):
    """
    called by models.KeyWord.keyed_sel().
    """
    url = dsh_common_config.lookup2('KEYWORD_SELECT_URL') + keyword.dsh_uid
    icon = dsh_common_config.lookup2('KEYWORD_SELECT_ICON')
    url = '<a href=%s title="select items with this key word">%s</a>' % \
          (url, icon)
    spaces = dsh_django_config.lookup('ICON_SPACES')
    url2 = dsh_common_config.lookup2('KEYWORD_DESEL_URL') + keyword.dsh_uid
    icon2 = dsh_common_config.lookup2('KEYWORD_DESEL_ICON')
    url2 = '<a href=%s title="de-select items with this key word">%s</a>' % \
           (url2, icon2)
    return url + spaces + url2 + spaces



def models_person_landline_link(person):
    """
    10/03/14.
    called by models.Person.landline_link().
    """
    if not person.phone_landline or not person.phone_number:
        return ''

    url = dsh_common_config.lookup2('LANDLINE_URL') + person.dsh_uid
    icon = dsh_common_config.lookup2('LANDLINE_ICON')
    url = '<a href=%s title="landline">%s</a>' % (url, icon)
    spaces = dsh_django_config.lookup('ICON_SPACES')
    return url + spaces



def models_person_current_dial_link(person):
    """
    10/03/22.
    called by models.Person.current_dial_link().
    """
    if not person.current_dial:
        return ''

    icon = dsh_common_config.lookup2('CURRENT_DIAL_ICON')
    url = '<a href="/scheduled/" title="in current dial set">%s</a>' % (icon,)
    spaces = dsh_django_config.lookup('ICON_SPACES')
    return url + spaces



def make_dsh_uid():
    """used to be in models.py"""
    return dsh_utils.date_time_rand()



def make_session_id():
    """used by dsh_common_selection.reschedule_script_call()"""
    return make_dsh_uid()



def models_persons_key_link(me):
    """
    10/03/22:
    modeled after models.Item.get_key_words()
    key words for persons
    """

    keyWords = me.person_key_words.all()
    displayKeyWords = ''
    for keyWord in keyWords:
        keyWordLookupURL = dsh_common_config.lookup2('PERSON_KEY_WORD_URL')
        keyWordLookupURL += keyWord.dsh_uid
        s = '<a href="%s">%s</a>' % (keyWordLookupURL, keyWord.key_word)
        displayKeyWords += s + ', '
    displayKeyWords = displayKeyWords.rstrip()
    displayKeyWords = displayKeyWords.rstrip(',')
    return displayKeyWords



def models_person_key_icons(key):
    """
    10/03/22:
    called by models.meta_display().
    modeled after itself.
    different set of links if the key word is for a person key.
    """
    noWrapStart = dsh_common_config.lookup2('NO_WRAP_OPEN')
    noWrapEnd = dsh_common_config.lookup2('NO_WRAP_END')
    spaces = dsh_django_config.lookup('ICON_SPACES')
    dshUid = key.dsh_uid
    
    answer = noWrapStart
    
    url = dsh_common_config.lookup2('PERSON_KEYWORD_SELECT_URL') + dshUid
    icon = dsh_common_config.lookup2('KEYWORD_SELECT_ICON')
    url = '<a href=%s title="select persons with this key word">%s</a>' % \
          (url, icon)
    answer += url + spaces

    url = dsh_common_config.lookup2('PERSON_KEYWORD_DESEL_URL') + dshUid
    icon = dsh_common_config.lookup2('KEYWORD_DESEL_ICON')
    url = '<a href=%s title="de-select persons with this key word">%s</a>' % \
          (url, icon)
    answer += url + spaces

    url = dsh_common_config.lookup2('PERSON_KEYWORD_PERSONS_URL') + dshUid
    icon = dsh_common_config.lookup2('PERSON_KEYWORD_PERSONS_ICON')
    url = '<a href=%s title="persons with this key word">%s</a>' % \
          (url, icon)
    answer += url + spaces

    url = dsh_common_config.lookup2('PERSON_KEYWORD_ADD_URL') + dshUid
    icon = dsh_django_config.lookup('KEYWORD_ICON')
    url = ('<a href=%s title="apply this key word to selected people">' +\
          '%s</a>') % (url, icon)
    answer += url + spaces
    
    url = dsh_common_config.lookup2('PERSON_KEYWORD_DEL_URL') + dshUid
    icon = dsh_django_config.lookup('KEYWORD_DEL_ICON')
    url = ('<a href=%s title="remove this key word to selected people">' +\
          '%s</a>') % (url, icon)
    answer += url + spaces

    answer += key.pin_dsh_uid()
    answer += key.selected_icon()
    answer += key.keyed_orgs()
    
    answer += noWrapEnd
    return answer



def models_item_dummy_icon(item):
    """
    10/03/23:
    icon for an dummy item.
    """

    if not item.dummy:
        return ''
    spaces = dsh_django_config.lookup('ICON_SPACES')
    return dsh_common_config.lookup2('DUMMY_ICON') + spaces



def should_auto_dial_for_peer_share(caller,
                                    itemTable, keyWordTable, eventTable,
                                    noLogging=False,
                                    sessionID=''):
    """
    called by dsh_django_utils.check_auto_timed_calls_for_person().
    to see if there are peer-shared messages to warrant the
    scheduling of an auto-dialed call.
    particularly relevant for DIET.
    partially modeled after dsh_django2.get_peer_shared().
    """

    init_log(quiet=True)

    dsh_utils.db_print('should_auto_dial_for_peer_share: entered.', 158)

    sharedList = get_peer_shared_item_for_caller(
        caller, itemTable, keyWordTable, sessionID)
    if not sharedList:
        dsh_utils.db_print('should_auto_dial_for_peer_share: no shared.', 158)
        return None

    for shared in sharedList:
        heardEvents = eventTable.objects.filter(
            action='HERD', owner=caller.id, dsh_uid_concerned=shared.dsh_uid)
        if not heardEvents:
            dsh_utils.db_print(
                'should_auto_dial_for_peer_share: not heard: ' +\
                shared.dsh_uid, 158)
            return shared

        dsh_utils.db_print(
            'should_auto_dial_for_peer_share: heard: ' + shared.dsh_uid, 158)

    dsh_utils.db_print('should_auto_dial_for_peer_share: all heard.', 158)
    return None



def add_key_word_to_item(item, keyStr, keyDesc, itemTable, keyWordTable,
                         sessionID=''):
    """
    10/03/24:
    add the key word "answers" to a newly recorded doctor reply.
    called by dsh_django2.add_doctor_answer_fields().
    returns success.
    """

    add_key_word_if_not_there(keyWordTable, keyStr, keyDesc,
                              sessionID=sessionID)
    
    keyWords = keyWordTable.objects.filter(key_word=keyStr)
    if not keyWords:
        message = 'dsh_common_db.add_key_word_to_item: no key word named: '+\
                  keyStr
        dsh_utils.give_bad_news(message, logging.error)
        dsh_agi.report_event(message, reportLevel='ERR', sessionID=sessionID)
        return False

    answerKey = keyWords[0]

    kwList = item.key_words.all()
    if answerKey in kwList:
        dsh_utils.db_print('add_key_word_to_item: key word already in.', 154)
        return True

    try:
        item.key_words.add(answerKey)
        item.save(noLogging=True, sessionID=sessionID)
    except:
        message = 'dsh_common_db.add_key_word_to_item: failed to save: '+\
                  item.dsh_uid
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT', sessionID=sessionID)
        return False

    dsh_utils.db_print('add_key_word_to_item: key word successfully added.',
                       154)
    return True



def add_key_word_if_not_there(keyWordTable, keyStr, keyDesc, sessionID=''):
    """
    10/03/24:
    called by add_key_word_to_item().
    if the "answers" key word is not already in the database, add it.
    returns success.
    """

    keyWords = keyWordTable.objects.filter(key_word=keyStr)
    if keyWords:
        dsh_utils.db_print(
            'add_key_word_if_not_there: alredy there: ' + keyStr, 154)
        return True

    keyWord = keyWordTable(key_word=keyStr, description=keyDesc)
    try:
        keyWord.save(sessionID=sessionID)
    except:
        message = 'dsh_common_db.add_key_word_if_not_there: ' +\
                  'failed to save: ' + keyStr
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT', sessionID=sessionID)
        return False

    dsh_utils.db_print(
        'add_key_word_if_not_there: key word successfully saved: ' + keyStr,
        154)
    return True



def patient_doctor_names(patient, doctor):
    """
    10/03/24:
    called by make_incoming_doctor_answer_personalized_reply().
    returns (patientName, doctorName)
    """
    return (patient.__unicode__(), doctor.__unicode__())



def make_incoming_doctor_answer_personalized_reply(item, sessionID=''):
    """
    10/03/24:
    change a bunch of fields to make an incoming doctor's message into
    an outgoing personalized reply to the original questioner.
    returns success.
    called by dsh_django2.add_doctor_answer_fields().
    """

    doctor = item.owner
    #
    # do it only if there was a questioner.
    #
    question = item.followup_to
    if not question:
        dsh_utils.db_print(
            'make_incoming_doctor_answer_personalized_reply: no question.',
            154)
        return True

    patient = question.owner
    patientName,doctorName = patient_doctor_names(patient, doctor)

    item.itype = 'P'
    item.description = ('A doctor has recorded a reply. The questioner was: '+\
                        '%s.  The doctor was %s.') % (patientName, doctorName)

    audienceList = item.intended_audience.all()
    if not (patient in audienceList):
        item.intended_audience.add(patient)

    try:
        item.save(noLogging=True, sessionID=sessionID)
    except:
        message = \
            'dsh_common_db.make_incoming_doctor_answer_personalized_reply:' +\
            ' failed to save item: ' + item.dsh_uid
        dsh_utils.give_bad_news(message, logging.critical)
        dsh_agi.report_event(message, reportLevel='CRT', sessionID=sessionID)
        return False

    dsh_utils.db_print('make_incoming_doctor_answer_personalized_reply: '+\
                       'success.', 154)
    return True
    


def models_person_heard_messages_icon(person):
    """10/04/01."""
    spaces = dsh_django_config.lookup('ICON_SPACES')
    dshUid = person.dsh_uid
    answer = ''

    url = dsh_common_config.lookup2('PERSON_HEARD_URL') + dshUid + '/0'
    icon = dsh_common_config.lookup2('BLUE_EAR')
    url = '<a href=%s title="messages heard">%s</a>' % (url, icon)
    answer += url + spaces

    return answer



def models_person_more_icons(person):
    """10/03/25."""
    spaces = dsh_django_config.lookup('ICON_SPACES')
    dshUid = person.dsh_uid
    answer = ''
    #
    # the '/0' is the offset of how many items to skip.
    #
    url = dsh_common_config.lookup2('PERSON_ANSWERED_URL') + dshUid + '/0'
    icon = dsh_common_config.lookup2('PERSON_ANSWERED_ICON')
    url = '<a href=%s title="messages answered">%s</a>' % (url, icon)
    answer += url + spaces

    answer += models_person_heard_messages_icon(person)

    return answer



def person_row(personTable, dshUid, noDemographics=False):
    """
    10/03/25:
    called by dsh_common_views.person_answered().
    returns (success, response)
    noDemographics=True when called by dvoice side, from person_heard().
    """

    response = ''
    
    person = dsh_django_utils.get_foreign_key(personTable, dshUid)
    if not person:
        message = 'dsh_common_views.person_row: no person found: ' + dshUid
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='ERR')
        return (False, response)

    response += '<TABLE BORDER=1 WIDTH=980><TR>'
    response += '<TD>%s</TD>' %\
        (dsh_django_utils.thumbnail(person, person.mugshot),)
    response += '<TD>%s<BR><BR>%s</TD>' %\
        (dsh_django_utils.person_link(person),
         person.hide_phone_number(),)
    response += '<TD>%s<BR><BR>%s</TD>' %\
        (person.ptype,
         dsh_django_utils.org_link(person.organization),)
    if noDemographics:
        response += '<TD></TD>'
    else:
        response += '<TD>%s</TD>' % (person.demographics(),)
    response += '<TD>%s</TD>' % (person.spoken_name_display_field(),)
    response += '<TD><span style="white-space: nowrap;">%s</span>' %\
                (person.meta_display(),)
    response += '<BR><BR>%s</TD>' %\
                (dsh_utils.time_date_day_str(person.modify_datetime),)
    response += '<TD>%s</TD>' % (person.description,)
    response += '</TR></TABLE>'
    return (True, response)



def answered_message_list(personTable, eventTable, itemTable, dshUid, offset):
    """
    10/03/25:
    called by dsh_common_views.person_answered().
    returns (success, response)
    10/04/01:
    rewritten to call heard_or_answered_message_list()
    """

    return heard_or_answered_message_list(
        personTable, eventTable, itemTable, dshUid, offset,
        eventAction='ANSW')



def answered_event_list(dshUid, events,
                        personTable, eventTable, itemTable, offset):
    """
    10/03/25:
    called by answered_message_list().
    dshUid is used to make the URL for the prev and next page links.
    returns (success, response)
    """

    response = ''

    #
    # deal with offset in the list.
    #
    length = len(events)
    if offset >= length:
        response = dsh_utils.red_error_break_msg(
            'Offset too big: %s.' % (str(offset),))
        return (True, response)
    events = events[offset:]
    perPage = dsh_common_config.lookup2('ANSWERS_PER_PAGE')

    #
    # init the loop for the table rows.
    #
    response += '<TABLE BORDER=1 WIDTH=980>'

    errorQuestionList = []
    errorAnswerList = []
    count = 0
    
    #
    # the table of all the answered events.
    #
    response += between_rows()
    for event in events:
        count += 1
        if count > perPage:
            count -= 1
            break

        #
        # name the row with a count.
        #
        col0Count = '<B>%s</B>' % (str(offset+count),)

        #
        # get the question and answer objects.
        #
        question = dsh_django_utils.get_foreign_key(itemTable, event.dsh_uid2)
        if not question:
            errorQuestionList.append((col0Count, event.dsh_uid2, event))
            continue

        answer = dsh_django_utils.get_foreign_key(
            itemTable, event.dsh_uid_concerned)
        if not answer:
            errorAnswerList.append((col0Count, event.dsh_uid, event))
            continue

        #
        # make the row.
        #
        row = ''
        col0Count = '<BR><BR>' + col0Count
        iconCol = answered_event_icons(event)
        row += '<TR>%s</TR>' % (item_columns(question, col0=col0Count))
        row += '<TR BGCOLOR="EDF3FE">%s</TR>' % \
               (item_columns(answer, col0=iconCol),)
        row += between_rows()
        response += row
        
    response += '</TABLE>'

    response += make_error_dshuid_table(
        errorQuestionList, 'The following questions are not found:')
    response += make_error_dshuid_table(
        errorAnswerList, 'The following answers are not found:')

    #
    # print the prev and next page links at the bottom of the page.
    #
    #response += 'count is: ' + str(count) + '<br>'
    response += make_prev_next_page_links(dshUid, offset, count, events)
    return (True, response)



def make_prev_next_page_links(dshUid, offset, count, events, action='ANSW'):
    """
    10/03/26:
    called by answered_event_list.
    prints the next page and prev page links.
    10/04/01:
    action='HERD' if called by heard_event_list()
    10/04/02:
    action='answers_unheard' or 'questions_unanswered',
    called by print_undone_message_table().
    """

    response = ''
    response += dsh_utils.black_break_msg('')
    response += dsh_utils.black_break_msg('')

    if action == 'ANSW':
        urlhead = dsh_common_config.lookup2('PERSON_ANSWERED_URL') + dshUid
    elif action == 'HERD':
        urlhead = dsh_common_config.lookup2('PERSON_HEARD_URL') + dshUid
    elif action == 'answers_unheard':
        urlhead = '/answersunheard'
    elif action == 'questions_unanswered':
        urlhead = '/questionsunanswered'
    else:
        urlhead = 'saywhat'
    
    perPage = dsh_common_config.lookup2('ANSWERS_PER_PAGE')
    if offset >= perPage:
        url = urlhead
        url += '/' + str(offset - perPage)
        url = '<a href=%s>&#171 prev page</a>' % (url,)
        response += url
        response += dsh_django_config.lookup('ICON_SPACES')
        response += dsh_django_config.lookup('ICON_SPACES')
        response += dsh_django_config.lookup('ICON_SPACES')
    
    length = len(events)
    if count >= length:
        pass
    else:
        url = urlhead
        url += '/' + str(offset + count)
        url = '<a href=%s>next page &#187</a>' % (url,)
        response += url

    return response

    

def make_error_dshuid_table(dshUidList, message, action='ANSW'):
    """
    10/03/26:
    called by answered_event_list().
    10/04/01:
    action='HERD' if called by heard_message_list().
    """
    response = ''
    if dshUidList:
        response += dsh_utils.black_break_msg('')
        response += dsh_utils.black_break_msg(message)
        response += dsh_utils.black_break_msg('')
        response += dsh_uid_error_table(dshUidList, action=action)
    return response

    

def answered_event_icons(event, noBr=False):
    """
    10/03/26:
    called by answered_event_list().
    icons preceding the answers.
    this is where we get to un-answer the event.
    noBr=True when called by dsh_uid_error_table().
    """
    
    response = ''

    if not noBr:
        response += '<BR>'
    
    spaces = dsh_django_config.lookup('ICON_SPACES')
    url = dsh_django_config.lookup('EVENT_DSH_UID_URL') + event.dsh_uid
    icon = dsh_common_config.lookup2('ANSWERED_EVENT_ICON')
    url = '<a href=%s title="answered event detail">%s</a>' % (url, icon)
    response += url

    if False and event.session:
        response += '<BR><BR>'
        url = dsh_django_config.lookup('SESSION_ID_SEARCH_URL') +\
              '=' + event.session
        icon = dsh_django_config.lookup('SESSION_ID_ICON')
        url = '<a href=%s title="session of the answer event">%s</a>' %\
              (url, icon)
        response += url

    if not noBr:
        response += '<BR><BR>'
    else:
        response += dsh_django_config.lookup('ICON_SPACES')
        
    url = dsh_common_config.lookup2('UNANSWER_URL') + event.dsh_uid
    icon = dsh_common_config.lookup2('UNANSWER_ICON')
    url = '<a href=%s title="un-answer this">%s</a>' % (url, icon)
    response += url
    
    return response
    


def dsh_uid_error_table(errorDshUidList, action='ANSW'):
    """
    10/03/25:
    called by answered_event_list().
    just prints a table of dsh_uid's that have errors.
    the input is a list of pairs.
    the first element of the pair is a counter, that gets printed too.
    the second is the dshUid.
    10/04/01:
    action='HERD' if called by heard_event_list().
    """

    response = ''
    response += '<TABLE BORDER=1>'
    for error in errorDshUidList:
        col0,col1,event = error
        if action == 'ANSW':
            icons = answered_event_icons(event, noBr=True)
        elif action == 'HERD':
            icons = heard_event_icons(event, noBr=True)
        else:
            icons = 'say what'
        response += '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>' %\
                    (col0, icons, col1)
    response += '</TABLE>'
    return response



def between_rows():
    """
    10/03/26:
    called by answered_event_list().
    prints an empty row after an answer.
    the number 9 needs to correspond to number of columns in
    item_columns() below.
    """
    return '<TR BGCOLOR="C5D5FC"><TH COLSPAN=9></TH></TR>'



def item_columns(item, col0=''):
    """
    10/03/25:
    a bunch of columns of an item.
    called by answered_event_list().
    """

    question = item

    row = ''
    row += '<TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD>'
    row += '<TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD>'
    col1,col2,col3,col4,col5,col6,col7,col8 = ('','','','','','','','')

    #
    # thumbnail of the questioner.
    #
    patient = question.owner
    thumb = patient.thumbnail()
    url = dsh_django_config.lookup('ITEM_DETAIL_URL') + str(question.id)
    col1 = "<a href=%s>%s</a>" % (url, thumb)

    #
    # col2: mp3 widget of the question.
    # col3: owner links
    # col4: org links
    # col5: meta icons
    # col6: date, time
    # col7: key words
    # col8: description
    #
    col2 = question.item_url()
    col3 = question.owner_link_plus_phone()
    col4 = question.org_link()
    col5 = question.meta_display()
    col6 = dsh_utils.time_date_day_str(question.modify_datetime)
    col7 = question.get_key_words()
    col8 = question.description

    row = row % (col0,col1,col2,col3,col4,col5,col6,col7,col8)
    return row



def put_doctor_answer_event(item, eventTable, sessionID='', noDuplicate=True):
    """
    10/03/25:
    moved from dsh_django2.py
    so it can be called by models.Item.save()
    for adding an answered event for web upload.
    noDuplicate=True in that case.
    10/03/24:
    called by hangup_signal_handler().
    if it was a doctor recording a reply, and if the recorded duration is
    long enough, we should put an answered event in the Event table.
    returns True if it's indeed an answer event and it's successfully put in.
    """

    init_log(quiet=True)
    dsh_utils.db_print('put_doctor_answer_event: entered. session='+\
                       sessionID, 154)
    dsh_utils.db_print('put_doctor_answer_event: item dsh_uid: ' +\
                       item.dsh_uid, 154)

    #
    # 10/03/25:
    # if called by models.Item.save()
    # should check that we're indeed dealing with a doctor.
    #
    if item.owner.ptype != dsh_config.lookup('DOCTOR_TYPE'):
        dsh_utils.db_print('put_doctor_answer_event: not a doc.', 154)
        return False
    
    #
    # if the recording is less than 15 seconds long,
    # it's probably not a real answer.
    #
    if item.rec_duration and \
        item.rec_duration < dsh_config.lookup('RECORDED_THRESH'):
        dsh_utils.db_print('put_doctor_answer_event: duration too short.', 154)
        return False

    #
    # if there's no followup_to field, then we're not answering any questions.
    # in which case, there's no need to continue (to put in an answered event).
    #
    question = item.followup_to
    if not question:
        return False

    #
    # just get people's names to put in the logged event.
    #
    doctor = item.owner
    patient = None
    if question:
        patient = question.owner

    docName = doctor.__unicode__()
    patientName = ''
    if patient:
        patientName = patient.__unicode__()

    message = 'a doctor has recorded a reply. patient: %s. doctor: %s.' %\
              (patientName, docName)
    message += ' question: %s. answer: %s.' % (repr(question), repr(item))
    if item.followup_to:
        dshUid2 = item.followup_to.dsh_uid
    else:
        dshUid2 = ''

    alreadyIn = False
    if noDuplicate:
        alreadyIn = already_answered_event(eventTable, item)

    dsh_utils.db_print(
        'put_doctor_answer_event: %s %s %s: ' %\
        (repr(noDuplicate), repr(alreadyIn),
         repr((not noDuplicate) or (not alreadyIn))), 154)

    if (not noDuplicate) or (not alreadyIn):
        dsh_agi.report_event(
            message,
            item=item,
            action='ANSW',
            phone_number=doctor.phone_number,
            owner=doctor,
            call_duration=item.call_duration,
            rec_duration=item.rec_duration,
            dsh_uid2=dshUid2,
            sessionID=sessionID)
        dsh_utils.give_news(message, logging.info)
    else:
        dsh_utils.db_print('put_doctor_answer_event: not put in.', 154)
    
    if question:
        maybe_deactivate_patient_question(
            question, eventTable, sessionID=sessionID)

    return True



def already_answered_event(eventTable, item):
    """
    10/03/25:
    if there's already an answered event corresponding to this item,
    then don't put it in again.
    called by put_doctor_answer_event().
    """
    doctor = item.owner
    question = item.followup_to
    qDshUid = ''
    if question:
        qDshUid = question.dsh_uid
    answeredEvents = eventTable.objects.filter(
        action='ANSW',
        owner=doctor.id,
        dsh_uid_concerned=item.dsh_uid,
        dsh_uid2=qDshUid)
    return answeredEvents



def message_answered(msg, doctor, eventTable):
    """
    10/03/25:
    moved from dsh_django2.py
    10/03/20:
    has this message been answered by this doctor?
    """
    answeredEvents = eventTable.objects.filter(
        action='ANSW', owner=doctor.id, dsh_uid2=msg.dsh_uid)
    return answeredEvents



def maybe_deactivate_patient_question(item, eventTable, sessionID=''):
    """
    10/03/25:
    moved from dsh_django2.py
    10/03/20:
    if this message has been answered by all the doctors assigned,
    then we deactivate it.
    it's modeled after maybe_deactivate_personal_message().
    """

    dsh_utils.db_print(
        'maybe_deactivate_patient_question: entered.', 154)
    
    if not item.active:
        return

    allAudience = item.intended_audience.all()
    if not allAudience:
        dsh_utils.db_print(
            'maybe_deactivate_patient_question: no audience: ' +
            item.dsh_uid, 154)
        item.active = False
        item.save(sessionID=sessionID)
        return

    for caller in allAudience:
        answered = message_answered(item, caller, eventTable)
        if not answered:
            dsh_utils.db_print(
                'maybe_deactivate_patient_question: not answered by: ' +\
                caller.dsh_uid, 154)
            return

    item.active = False
    item.save(sessionID=sessionID)
    message = 'dsh_common_db.maybe_deactivate_patient_question: ' +\
              'deactivated: '+ item.dsh_uid
    dsh_utils.give_news(message, logging.info)
    dsh_agi.report_event(message, item=item, sessionID=sessionID)



def unanswer(dshUid, eventTable, itemTable):
    """
    10/03/26:
    called by dsh_common_views.unanswer().
    change an earlier ANSW event to NOAN.
    add a new UNAN event.
    10/04/04:
    activate the question.
    """

    response = ''
    
    event = dsh_django_utils.get_foreign_key(eventTable, dshUid)
    if not event:
        response += dsh_utils.red_error_break_msg(
            'dsh_common_db.unanswer: no such event: ' + dshUid)
        return response

    if event.action != 'ANSW':
        response += dsh_utils.red_error_break_msg(
            'dsh_common_db.unanswer: this event is not an "answer" event: '+\
            dshUid)
        return response

    event.action = 'NOAN'
    try:
        event.save()
    except:
        message = 'Failed to change an "answer" event to "un-answer" ' +\
                  'event: ' + event.dsh_uid
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='CRT')
        return response

    response += activate_message(event.dsh_uid2, itemTable)

    doctorName = ''
    if event.owner:
        doctorName = event.owner.__unicode__()
    message = 'unanswer a reply by: ' + doctorName
    dsh_agi.report_event(
        message,
        action='UNAN',
        item=event,
        sessionID=event.session)

    response += dsh_utils.black_break_msg('Done.')
    if not event.session:
        response += dsh_utils.black_break_msg(
            'Look at the <a href="/admin/db/event">event table</a>.')
    else:
        url = dsh_django_config.lookup('SESSION_ID_SEARCH_URL')
        response += dsh_utils.black_break_msg(
            'Look at the <a href="%s=%s">relevant events</a>.' % \
            (url, event.session))
        
    return response



def models_item_conversation_chain_icon(item):
    """
    10/03/28:
    called by models.Item.conversation_chain_icon().
    displays an entire thread of the conversation, chasing the
    followup_to field up and down the thread.
    """

    url = dsh_common_config.lookup2('CONVERSATION_CHAIN_URL') + item.dsh_uid
    icon = dsh_common_config.lookup2('CONVERSATION_CHAIN_ICON')
    url = '<a href=%s title="conversation history">%s</a>' % (url, icon)
    spaces = dsh_django_config.lookup('ICON_SPACES')
    return url + spaces



def chase_followup_to_links(thisItem):
    """
    10/03/28:
    called by conversation_history().
    chases the followup_to links to the end.
    returns listOfItems
    """

    #
    # keep track of things that have already been seen.
    # so we don't chase an infinite loop.
    #
    seenAlready = [thisItem]

    #
    # this is going to be the answer.
    #
    listBefore = []

    #
    # the current item for looping
    #
    currentItem = thisItem

    while True:
        nextItem = currentItem.followup_to
        if not nextItem:
            return listBefore
        if nextItem in seenAlready:
            return listBefore
        if nextItem.dummy:
            return listBefore
        seenAlready.append(nextItem)
        listBefore.append(nextItem)
        currentItem = nextItem

    return listBefore



def chase_followed_by_links(thisItem):
    """
    10/03/28:
    called by conversation_history().
    chase the followed_by links to the end.
    return listOfItems
    modeled after chase_followup_to_links()
    """

    seenAlready = [thisItem]
    listAfter = []
    currentItem = thisItem

    while True:
        followedBy = currentItem.followed_by
        if not followedBy:
            return listAfter
        followedByItems = followedBy.all()
        if not followedByItems:
            return listAfter
        #followedByItem = followedByItems[0]
        followedByItem = followedByItems.latest()
        if not followedByItem:
            return listAfter
        if followedByItem in seenAlready:
            return listAfter
        if followedByItem.dummy:
            return listAfter
        seenAlready.append(followedByItem)
        listAfter.append(followedByItem)
        currentItem = followedByItem

    return listAfter
    


def conversation_history(dshUid, itemTable, eventTable):
    """
    10/03/28:
    called by models.Item.conversation_chain_icon().
    displays an entire thread of the conversation, chasing the
    followup_to field up and down the thread.
    """

    response = ''

    thisItem = dsh_django_utils.get_foreign_key(itemTable, dshUid)

    if not thisItem:
        message = 'dsh_common_db.conversation_history: no such item: ' +\
                  dshUid
        response += dsh_utils.red_error_break_msg(message)
        return response

    response += dsh_utils.black_break_msg(
        '(The shaded message was the one that you clicked from.)')
    response += dsh_utils.black_break_msg('')

    listBefore = chase_followup_to_links(thisItem)
    response += dsh_utils.black_break_msg_debug(
        'conversation_history: number of items before: ' +\
        str(len(listBefore)), 163)

    #
    # do it in the reverse chronological order.
    #
    #listBefore = listBefore[::-1]

    listAfter = chase_followed_by_links(thisItem)
    response += dsh_utils.black_break_msg_debug(
        'conversation_history: number of items after: ' +\
        str(len(listAfter)), 163)

    #
    # do it in the reverse chronological order.
    #
    listAfter = listAfter[::-1]

    response += display_conversation_history_table(
        thisItem, listBefore, listAfter, eventTable)

    return response



def display_conversation_history_table(
    thisItem, listBefore, listAfter, eventTable):
    """
    10/03/28:
    called by conversation_history()
    the main thing.
    prints the table of the conversation thred.
    somewhat modeled after answered_event_list().
    """

    response = ''

    response += '<TABLE BORDER=1 WIDTH=980>'

    for item in listAfter:
        col0 = answer_icons_for_conversation_history(item, eventTable)
        row = '<TR>%s</TR>' % (item_columns(item, col0=col0),)
        response += row


    col0 = answer_icons_for_conversation_history(thisItem, eventTable)
    row = '<TR BGCOLOR="EDF3FE">%s</TR>' % \
          (item_columns(thisItem, col0=col0))
    response += row

    for item in listBefore:
        col0 = answer_icons_for_conversation_history(item, eventTable)
        row = '<TR>%s</TR>' % (item_columns(item, col0=col0),)
        response += row

    response += '</TABLE>'
    
    return response



def answer_icons_for_conversation_history(item, eventTable):
    """
    10/03/28:
    called by display_conversation_history_table().
    is this item an answer?
    if it's an answer that has generated an answer event,
    display icons for un-answering,
    in the first column.
    """

    events = eventTable.objects.filter(
        action='ANSW',
        dsh_uid_concerned=item.dsh_uid)

    if not events:
        return ''

    event = events[0]

    return answered_event_icons(event)



def person_has_personalized_message(caller, eventTable):
    """
    10/03/30: a chunk kind of copied from
    dsh_django_utils.check_auto_timed_calls_for_person().
    I'm too lazy to re-write that function.
    this function is getting called by
    dsh_common_test.person_has_any_message_at_all().
    """
    messages = caller.message_for_me.all()
    if not messages:
        return False

    for msg in messages:
        if not (msg.itype == 'P' and msg.active):
            continue
        heardEvents = eventTable.objects.filter(
            action='HERD', owner=caller.id, dsh_uid_concerned=msg.dsh_uid)
        if heardEvents:
            continue
        return True
        
    return False



def heard_or_answered_message_list(personTable, eventTable, itemTable,
                                   dshUid, offset,
                                   eventAction='ANSW'):
    """
    10/03/25:
    called by dsh_common_views.person_answered().
    returns (success, response)
    10/04/01:
    rewritten slightly to deal with both heard or answered events.
    eventActon='ANSW' for answered calls.  'HERD' for heard calls.
    """

    response = ''
    
    funcName = 'dsh_common_db.heard_or_answered_message_list: '
    if eventAction == 'ANSW':
        verb = 'answered'
    elif eventAction == 'HERD':
        verb = 'heard'
    else:
        verb = 'saywhat'

    #
    # validate offset.
    #
    validOffset = True
    try:
        offset = int(offset)
    except:
        validOffset = False

    if offset < 0:
        validOffset = False

    if not validOffset:
        message = 'Invalid offset: %s.' % (offset,)
        response += dsh_utils.red_error_break_msg(message)
        return (False, response)
        
    #
    # convert dshUid to person.
    #
    person = dsh_django_utils.get_foreign_key(personTable, dshUid)
    if not person:
        message = funcName + 'no person found: ' + dshUid
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='ERR')
        return (False, response)

    response += dsh_utils.black_break_msg('')

    #
    # get the events.
    #
    answeredEvents = eventTable.objects.filter(
        action=eventAction, owner=person)

    #
    # if we're doing heard events.
    # remove all the heard events of dummy messages.
    #
    if eventAction == 'HERD':
        answeredEvents = remove_dummy_message_events(answeredEvents, itemTable)
    

    if not answeredEvents:
        response += dsh_utils.black_break_msg(
            'This person has not %s any messages.' % (verb,))
        return (False, response)

    #
    # reverse the event list for reverse chronological order.
    #
    answeredEvents = answeredEvents[::-1]

    #
    # deal with offset in the list.
    #
    length = len(answeredEvents)
    if offset >= length:
        response += dsh_utils.red_error_break_msg(
            'Offset too big: %s.' % (str(offset),))
        return (True, response)
    perPage = dsh_common_config.lookup2('ANSWERS_PER_PAGE')
    lastCount = offset + perPage
    if lastCount > length:
        lastCount = length

    
    message = 'This person has %s %s messages. ' % (verb,str(length),)
    message+= 'This page displays %s - %s. ' % (str(offset+1), str(lastCount))
    response += dsh_utils.black_break_msg(message)
    if eventAction == 'ANSW':
        message = '(white rows: questions, shaded rows: answers.)'
        response += dsh_utils.black_break_msg(message)
    response += dsh_utils.black_break_msg('')

    #
    # go through the events.
    #
    if eventAction == 'ANSW':
        success,msg = answered_event_list(
            dshUid, answeredEvents, personTable, eventTable, itemTable, offset)
    elif eventAction == 'HERD':
        success,msg = heard_event_list(
            dshUid, answeredEvents, personTable, eventTable, itemTable, offset)
    response += msg
    return (True, response)



def heard_message_list(personTable, eventTable, itemTable, dshUid, offset):
    """
    10/04/01:
    modeled after answered_message_list().
    called by dsh_common_views.person_heard().
    """
    return heard_or_answered_message_list(
        personTable, eventTable, itemTable, dshUid, offset,
        eventAction='HERD')



def remove_dummy_message_events(events, itemTable):
    """
    10/04/01: called by heard_or_answered_message_list().
    remove all the heard events about hearing dummy messages.
    """
    answer = []
    for event in events:
        #
        # get heard item.
        #
        item = dsh_django_utils.get_foreign_key(
            itemTable, event.dsh_uid_concerned)
        if not item or item.dummy:
            continue
        answer.append(event)
    return answer



def heard_event_list(dshUid, events,
                     personTable, eventTable, itemTable, offset):
    """
    10/04/01:
    modeled after answered_event_list().
    answered_event_list() prints two rows for each event.
    in the case of heard messages here, we're printing just one row per event.
    called by heard_or_answered_message_list().
    returns (success, response)
    """

    response = ''

    #
    # deal with offset in the list.
    #
    length = len(events)
    if offset >= length:
        response = dsh_utils.red_error_break_msg(
            'Offset too big: %s.' % (str(offset),))
        return (True, response)
    events = events[offset:]
    perPage = dsh_common_config.lookup2('ANSWERS_PER_PAGE')

    #
    # init the loop for the table rows.
    #
    response += '<TABLE BORDER=1 WIDTH=980>'

    errorItemList = []
    count = 0
    
    #
    # the table of all the heard events.
    #
    for event in events:
        count += 1
        if count > perPage:
            count -= 1
            break

        #
        # name the row with a count.
        #
        col0Count = '<B>%s</B>' % (str(offset+count),)

        #
        # get heard item.
        #
        item = dsh_django_utils.get_foreign_key(
            itemTable, event.dsh_uid_concerned)
        if not item:
            errorItemList.append((col0Count, event.dsh_uid, event))
            continue

        #
        # we remove these ahead of time.
        #
        #if item.dummy:
        #    count -= 1
        #    continue

        #
        # make the row.
        #
        row = ''
        iconCol = col0Count + '<BR>' + heard_event_icons(event)
        row += '<TR>%s</TR>' % (item_columns(item, col0=iconCol),)
        response += row
        
    response += '</TABLE>'

    response += make_error_dshuid_table(
        errorItemList, 'The following messages are not found:',
        action='HERD')

    #
    # print the prev and next page links at the bottom of the page.
    #
    response += make_prev_next_page_links(
        dshUid, offset, count, events, action='HERD')
    return (True, response)



def heard_event_icons(event, noBr=False):
    """
    10/04/01:
    modeled after answered_event_icons().
    noBr=True when called by dsh_uid_error_table().
    """
    
    response = ''

    if not noBr:
        response += '<BR>'
    
    spaces = dsh_django_config.lookup('ICON_SPACES')
    url = dsh_django_config.lookup('EVENT_DSH_UID_URL') + event.dsh_uid
    icon = dsh_common_config.lookup2('GREEN_EAR')
    url = '<a href=%s title="heard event detail">%s</a>' % (url, icon)
    response += url

    if not noBr:
        response += '<BR><BR>'
    else:
        response += dsh_django_config.lookup('ICON_SPACES')
        
    url = dsh_common_config.lookup2('UNHEAR_URL') + event.dsh_uid
    icon = dsh_common_config.lookup2('RED_EAR')
    url = '<a href=%s title="un-answer this">%s</a>' % (url, icon)
    response += url
    
    return response



def unhear(dshUid, eventTable, itemTable):
    """
    10/04/01:
    modeled after unanswer().
    called by dsh_common_views.unhear().
    change an earlier HERD event to NOHR.
    add a new UNHE event.
    """

    response = ''
    
    event = dsh_django_utils.get_foreign_key(eventTable, dshUid)
    if not event:
        response += dsh_utils.red_error_break_msg(
            'dsh_common_db.unhear: no such event: ' + dshUid)
        return response

    if event.action != 'HERD':
        response += dsh_utils.red_error_break_msg(
            'dsh_common_db.unhear: this event is not an "heard" event: '+\
            dshUid)
        return response

    event.action = 'NOHR'
    try:
        event.save()
    except:
        message = 'Failed to change a "heard" event to an "un-hear" ' +\
                  'event: ' + event.dsh_uid
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='CRT')
        return response

    if event.dsh_uid_concerned:
        response += activate_message(event.dsh_uid_concerned, itemTable)

    personName = ''
    if event.owner:
        personName = event.owner.__unicode__()
    message = 'un-heard by: ' + personName
    dsh_agi.report_event(
        message,
        action='UNHE',
        item=event,
        sessionID=event.session)

    response += dsh_utils.black_break_msg('Done.')
    if not event.session:
        response += dsh_utils.black_break_msg(
            'Look at the <a href="/admin/db/event">event table</a>.')
    else:
        url = dsh_django_config.lookup('SESSION_ID_SEARCH_URL')
        response += dsh_utils.black_break_msg(
            'Look at the <a href="%s=%s">relevant events</a>.' % \
            (url, event.session))
        
    return response



def questions_answers_not_done(request, kind, offset,
                               itemTable, keyWordTable, eventTable):
    """
    10/04/02:
    called by dsh_common_views.questions_answers_not_done().
    """
    response = ''
    items,itemNotes,msg = get_questions_answers_not_done(
        kind, itemTable, keyWordTable, eventTable)
    response += msg
    if items:
        response += print_undone_message_table(items, itemNotes,
                                                        offset, kind)
    return response



def get_questions_answers_not_done(kind, itemTable, keyWordTable, eventTable):
    """
    10/04/02:
    called by questions_answers_not_done().
    get the question or answer items that are not done.
    returns (items, itemNotes, response)
    """

    response = ''
    funcName = 'dsh_common_db.get_questions_answers_not_done:'

    #
    # get the key word.
    #
    lookup = {'questions_unanswered': 'questions',
              'answers_unheard': 'answers'}

    searchKeyWordString = lookup[kind]
    keyWord,msg = get_key_word(keyWordTable, searchKeyWordString)
    response += msg
    if not keyWord:
        return (None, None, response)

    #
    # get the items with this key word.
    #
    items = itemTable.objects.filter(key_words=keyWord.id)
    if not items:
        message = "%s can't find items with this key word: %s" %\
                  (funcName, searchKeyWordString)
        response += dsh_utils.red_error_break_msg(message)
        return (None, None, response)

    #
    # prints how many items.
    #
    count = str(len(items))
    if kind == 'questions_unanswered':
        response += dsh_utils.black_break_msg(
            'Total number of questions: %s.' % (count,))
    elif kind == 'answers_unheard':
        response += dsh_utils.black_break_msg(
            'Total number of answers: %s.' % (count,))

    #
    # filter the items to get the undone ones.
    #
    items,itemNotes,msg = filter_questions_answers_not_done(
        items, kind, eventTable)
    response += msg

    #
    # prints how many items left.
    #
    count = str(len(items))
    if kind == 'questions_unanswered':
        response += dsh_utils.black_break_msg(
            'Questions unanswered: %s.' % (count,))
    elif kind == 'answers_unheard':
        response += dsh_utils.black_break_msg(
            'Answers unheard: %s.' % (count,))

    return (items, itemNotes, response)



def get_key_word(keyWordTable, searchKeyWordString):
    """
    10/04/02:
    called by get_questions_answers_not_done().
    gets the "questions" or "answers" key word.
    """

    response = ''
    funcName = 'dsh_common_db.get_key_word:'
    keyWords = keyWordTable.objects.filter(key_word=searchKeyWordString)

    if not keyWords:
        message = '%s key word %s not found.' % \
                  (funcName, searchKeyWordString,)
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='ERR')
        return (None, response)
    else:
        response += dsh_utils.black_break_msg_debug(
            funcName + ' key word found.', 166)

    keyWord = keyWords[0]
    return (keyWord, response)



def filter_questions_answers_not_done(items, kind, eventTable):
    """
    10/04/02:
    called by get_questions_answers_not_done().
    returns only questions unanswered or answers unheard.
    """

    funcName = 'dsh_common_db.filter_questions_answers_not_done:'
    response = ''
    answerItems = []
    itemNotes = {}    # indexed by dsh_uid of answer items
    items = items[::-1]
    
    for item in items:

        if kind == 'questions_unanswered':
            answerEvents = eventTable.objects.filter(
                action='ANSW', dsh_uid2=item.dsh_uid)
            if not answerEvents:
                answerItems.append(item)
            continue

        if kind == 'answers_unheard':
            question = item.followup_to
            if not question:
                #response += dsh_utils.red_error_break_msg(
                #    '%s answer has no question: %s.' %\
                #    (funcName, item.__unicode__()))

                #url = dsh_django_config.lookup('ITEM_DSH_UID_URL') +\
                #      item.dsh_uid
                #url = '<a href="%s">this answer</a> has no question.' % (url,)
                #response += dsh_utils.black_break_msg(url)
                
                answerItems.append(item)
                itemNote = '<BR>' + dsh_common_config.lookup2('RED_QUESTION')
                heardEvents = eventTable.objects.filter(
                    action='HERD', dsh_uid_concerned=item.dsh_uid)
                if not heardEvents:
                    itemNote += '<BR><BR>' +\
                                dsh_common_config.lookup2('RED_EAR2')
                itemNotes[item.dsh_uid] = itemNote
                continue

            heardEvents = eventTable.objects.filter(
                action='HERD', dsh_uid_concerned=item.dsh_uid,
                owner=question.owner.id)
            if not heardEvents:
                answerItems.append(item)
            continue

        response += dsh_utils.red_error_break_msg(
            '%s bad action: %s.' % (funcName, kind))
        break

    if not answerItems:
        if kind == 'questions_unanswered':
            response += dsh_utils.red_error_break_msg(
                'no un-answered questions.')
        elif kind == 'answers_unheard':
            response += dsh_utils.red_error_break_msg(
                'no unheard answers.')
    return (answerItems,itemNotes,response)



def print_undone_message_table(items, itemNotes, offset, kind):
    """
    10/04/02:
    called by questions_answers_not_done().
    the list of items is gotten, now we just need to print it.
    itemNotes is a dictionary indexed by dsh_uid's that have notes:
    answers that have no questions (in addition to being unheard).
    """

    response = ''

    #
    # validate offset.
    #
    validOffset = True
    try:
        offset = int(offset)
    except:
        validOffset = False

    if offset < 0:
        validOffset = False

    if not validOffset:
        message = 'Invalid offset: %s.' % (offset,)
        response += dsh_utils.red_error_break_msg(message)
        return response
        
    #
    # deal with offset in the list.
    #
    length = len(items)
    if offset >= length:
        response += dsh_utils.red_error_break_msg(
            'Offset too big: %s.' % (str(offset),))
        return response
    perPage = dsh_common_config.lookup2('ANSWERS_PER_PAGE')
    lastCount = offset + perPage
    if lastCount > length:
        lastCount = length

    message = 'This page displays %s - %s. ' % (str(offset+1), str(lastCount))
    message += '<BR>'
    response += dsh_utils.black_break_msg(message)


    #
    # init the loop.
    #
    items = items[offset:]
    response += '<TABLE BORDER=1 WIDTH=980>'
    count = 0

    for item in items:
        count += 1
        if count > perPage:
            count -= 1
            break

        countStr = str(offset+count)
        if itemNotes.has_key(item.dsh_uid):
            col0 = '<B>%s</B><BR>%s' % (countStr, itemNotes[item.dsh_uid])
        else:
            col0 = '<B>%s</B>' % (countStr,)

        row = '<TR>%s</TR>' % (item_columns(item, col0=col0),)
        response += row

    response += '</TABLE>'

    response += make_prev_next_page_links(
        '', offset, count, items, action=kind)
    return response



def activate_message(dshUid, itemTable):
    """
    10/04/04:
    called by unanswer().
    to activate the question that just got unanswered.
    """

    funcName = 'dsh_common_db.activate_message:'
    response = ''
    item = dsh_django_utils.get_foreign_key(itemTable, dshUid)
    if not item:
        message ="%s can't find this question: %s" % (funcName, dshUid)
        response += dsh_utils.red_error_break_msg(message)
        return response

    if item.active:
        return ''

    item.active = True

    try:
        item.save()
    except:
        message = '%s failed to save item: %s' % (funcName, dshUid)
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='CRT')

    return response



def get_most_recent_message(itemTable, sessionID=''):
    """
    10/04/09:
    called by demo_reply().
    partly copied from dsh_django2.play_recent().
    """

    response = ''
    funcName = 'dsh_common_db.get_most_recent_message:'
    
    longRecs = itemTable.objects.filter(
        rec_duration__gt=dsh_config.lookup('RECORDED_THRESH'))

    if not longRecs:
        message = '%s found nothing.' % (funcName,)
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='ERR', sessionID=sessionID)
        dsh_utils.give_bad_news(message, logging.error)
        return (None, response)

    message = '%s length: %s, first: %s, last: %s.' % \
              (funcName,
               str(len(longRecs)),
               longRecs[0].__unicode__(),
               longRecs[len(longRecs)-1].__unicode__())
    response += dsh_utils.black_break_msg_debug(message, 168)

    recent = longRecs[::-1][0]

    message = '%s most recent message is: %s' % (funcName,
                                                 recent.__unicode__())
    response += dsh_utils.black_break_msg_debug(message, 168)
    dsh_utils.db_print(message, 168)
    
    return (recent, response)



def send_demo_reply_confirmed(dshUid, itemTable, keyWordTable,
                              eventTable):
    """
    10/04/09: called by dsh_common_views.send_demo_reply_confirmed().
    """

    funcName = 'dsh_common_db.send_demo_reply_confirmed:'
    response = ''
    sessionID = make_dsh_uid()
    recent = dsh_django_utils.get_foreign_key(itemTable, dshUid)
    if not recent:
        message = '%s no such dsh_uid: %s.' % (funcName, dshUid)
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='ERR', sessionID=sessionID)
        return response

    response += attempt_demo_reply_now(
        recent, itemTable, keyWordTable, eventTable, sessionID=sessionID)
    return response



def attempt_demo_reply_now(recent, itemTable, keyWordTable, eventTable,
                           sessionID=''):
    """
    10/04/09: called by dsh_common_agi.demo_reply_prompt_confirm() and
    send_demo_reply_confirmed().
    """

    funcName = 'dsh_common_db.attempt_demo_reply_now:'
    response = ''

    init_log(quiet=True)
    dsh_utils.db_print('%s entered: %s.' % (funcName, recent.dsh_uid), 168)

    reply,msg = get_demo_reply(itemTable, sessionID=sessionID)
    response += msg

    if not reply:
        return response

    success,msg = set_demo_reply_fields(
        recent, reply, itemTable, keyWordTable, sessionID=sessionID)
    response += msg

    if not success:
        return response

    #
    # remove all the heard events of this person.
    # so we force it to be played.
    #
    response += unhear_demo_reply(recent, reply, eventTable,
                                  sessionID=sessionID)

    #
    # like dsh_django_utils.dial_now_confirm().
    #
    success,msg = dsh_common_agi.make_dot_call_file(
        recent.owner, sessionID=sessionID)
    response += msg

    return response



def get_demo_reply(itemTable, sessionID=''):
    """
    10/04/09: called by attempt_demo_reply_now().
    find the most recent message with the "demo_reply" key word.
    """

    funcName = 'get_demo_reply:'
    response = ''
    
    keyStr = dsh_common_config.lookup2('DEMO_REPLY_KEYWORD')

    demoReplies = itemTable.objects.filter(key_words__key_word=keyStr)
    if not demoReplies:
        message = '%s no demo replies.' % (funcName,)
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='ERR', sessionID=sessionID)
        dsh_utils.give_bad_news(message, logging.error)
        return (None, response)

    demoReply = demoReplies[len(demoReplies)-1]
    response += dsh_utils.black_break_msg_debug(
        '%s found demo reply: %s.' % (funcName, demoReply.__unicode__()), 168)

    return (demoReply, response)



def set_demo_reply_fields(recent, reply, itemTable, keyWordTable,
                          sessionID=''):
    """
    10/04/09: called by attempt_demo_reply_now()
    sets a bunch of fields of the demo reply item so it can be sent
    to the most recent caller.
    modeled after
    dsh_common_db.make_incoming_doctor_answer_personalized_reply().
    """

    funcName = 'dsh_common_db.set_demo_reply_fields:'
    response = ''

    questioner = recent.owner
    phoneNum = questioner.phone_number
    if not phoneNum:
        message = '%s questioner has no phone number: %s' %\
                  (funcName, questioner.dsh_uid)
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='ERR', sessionID=sessionID)
        dsh_utils.give_bad_news(message, logging.error)
        return (False, response)
    
    success = add_key_word_to_item(
        reply, 'answers', "doctor's answers",
        itemTable, keyWordTable, sessionID=sessionID)
    if not success:
        message = '%s failed to add answer key word to reply message: %s' %\
                  (funcName, reply.dsh_uid)
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='ERR', sessionID=sessionID)
        dsh_utils.give_bad_news(message, logging.error)
        return (False, response)

    reply.followup_to = recent
    reply.itype = 'P'
    reply.active = True
    #reply.dummy = True
    reply.description += 'sent to %s. ' % (phoneNum,)

    dsh_utils.db_print('%s zeroing intended audience set.' % (funcName,), 168)
    reply.intended_audience = []
    audienceList = reply.intended_audience.all()
    if not (questioner in audienceList):
        reply.intended_audience.add(questioner)

    try:
        reply.save(noLogging=True, sessionID=sessionID)
    except:
        message = '%s failed to save reply: %s.' % (funcName, reply.dsh_uid)
        response += dsh_utils.red_error_break_msg(message)
        dsh_agi.report_event(message, reportLevel='CRT', sessionID=sessionID)
        dsh_utils.give_bad_news(message, logging.critical)
        return (False, response)

    message = '%s phone number: %s, demo reply: %s.' %\
              (funcName, phoneNum, reply.__unicode__())
    dsh_agi.report_event(
        message,
        action='DEM1',
        item=reply,
        dsh_uid2=recent.dsh_uid,
        phone_number=phoneNum,
        owner=questioner,
        sessionID=sessionID)
    dsh_utils.give_news(message, logging.info)
    response += dsh_utils.black_break_msg_debug(message, 168)
    return (True, response)
    


def unhear_demo_reply(recent, reply, eventTable, sessionID=''):
    """
    10/04/09: called by attempt_demo_reply_now().
    remove all the heard events of the demo reply message for this questioner.
    so that we force the reply to be played.
    """

    funcName = 'dsh_common_db.unhear_demo_reply:'
    response = ''

    heardEvents = eventTable.objects.filter(
        action='HERD', owner=recent.owner.id, dsh_uid_concerned=reply.dsh_uid)
    
    if not heardEvents:
        dsh_utils.db_print(
            '%s no heard events: %s.' % (funcName, reply.dsh_uid), 168)
        return response

    count = 0
    for heard in heardEvents:
        heard.action = 'NOHR'
        try:
            heard.save()
            count += 1
        except:
            message = '%s failed to change a "heard" event to an "un-hear" '+\
                      'event: ' + heard.dsh_uid
            response += dsh_utils.red_error_break_msg(message)
            dsh_agi.report_event(message, reportLevel='CRT',
                                 sessionID=sessionID)
            dsh_utils.give_bad_news(message, logging.critical)

    dsh_utils.db_print(
        '%s number of heard events changed: %s.' % (funcName, str(count)), 168)
    return response



def person_latest_event(person, eventTable):
    """10/04/14: called by models_person_latest_event()."""
    actions = ['ENTR', 'CALL', 'HERD', 'UNHR', 'BRCT']
    events = eventTable.objects.filter(
        owner=person.id, action__in=actions)
    if events:
        return events.latest()
    return None



def models_person_latest_event(person, eventTable):
    """10/04/14: called by models.latest_event().
    the latest time the person had any event on the system."""

    funcName = 'dsh_common_db.models_person_latest_event:'
    
    latest = person_latest_event(person, eventTable)
    
    dsh_django_utils.debug_event(
        '%s: latest: %s' % (funcName, repr(latest)), 44)
    
    if not latest:
        return ''

    time = latest.modify_datetime
    dsh_django_utils.debug_event(
        '%s: %s' % (funcName, repr(time)), 44)

    dateTimeStr = dsh_utils.time_date_day_str(time)

    if latest.session:
        url = dsh_django_config.lookup('SESSION_ID_SEARCH_URL')
        url += '=' + latest.session
        answer = '<a href="%s">%s</a>' % (url, dateTimeStr)
    else:
        answer = dateTimeStr
    return answer
