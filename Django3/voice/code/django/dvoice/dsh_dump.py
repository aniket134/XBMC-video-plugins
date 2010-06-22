#
# Why do I need to write my own dumper and loader?
# Lots of reasons...
# (1) need to be able to selectively dump and load, not wholesale...
#     this is necessary when I attempt to, say, take some items from...
#     dsh.cs and put it on pnet1.  can't copy the whole database.
# (2) need to dump the files in /media.
# (3) deal with fairly drastic db format changes.
# (4) make the dump file human readable and I can do whatever...
#     I want with the dump file.
# ...
# none of these requirements is met by the existing dumpers.
#



import sys,os,subprocess,logging
import dvoice.db.models
#from dvoice.db.models import Organization, Person, Item, KeyWord, Event
import dsh_django_config,dsh_django_utils,dsh_dump_models
import dsh_django_utils2
dsh_django_utils2.append_to_sys_path(
    dsh_django_config.lookup('DSH_VOICE_CODE_DIR'))
import dsh_utils,dsh_config,dsh_agi
from django.utils.encoding import smart_str, smart_unicode



allDbTables = {
    'keyword': [dvoice.db.models.KeyWord, 'key word(s)'],
    'organization': [dvoice.db.models.Organization, 'organization(s)'],
    'person': [dvoice.db.models.Person,'person(s)'],
    'item': [dvoice.db.models.Item, 'item(s)'],
    'event': [dvoice.db.models.Event, 'event(s)'],
}



def init_dump():
    """initializes the dump file."""

    #
    # makes the directory.
    #
    dumpDir = os.path.join(
        dsh_django_config.lookup('PHONE_DATA_DJANGO_PATH'),
        dsh_django_config.lookup('DB_DUMP_DIR'))
    if not dsh_utils.try_mkdir_ifdoesnt_exist(
        dumpDir, 'dsh_dump.init: ' + dumpDir):
        dsh_django_utils.error_event(
            'dsh_dump.init: failed to create dump dir: ' + dumpDir,
        errorLevel='CRT')
        return None

    #
    # determine the file name and open it.
    #
    randomName = dsh_utils.date_time_rand()
    fileName = randomName + '.py'
    tarName = randomName + '.tar'
    fullName = os.path.join(dumpDir, fileName)
    fullTarName = os.path.join(dumpDir, tarName)
    try:
        dumpFile = open(fullName, 'w')
        dumpFile.write('# -*- coding: latin-1 -*-\n')
        dumpFile.write('import datetime\n\n')
    except:
        dsh_django_utils.error_event(
            'dsh_dump.init: failed to open file: ' + fullName,
        errorLevel='CRT')
        return None
    return (dumpFile, fullName, fullTarName)    



def dump_one(obj, define, tarPath):
    """called by dump_selected() below, dumps one django object into a
    dump file.
    obj is an object retrieved from django db.
    each dumped object is a dictionary.  of the form:
    FieldName: [FieldType, FieldValue],
    'define' is the object definition coming from dsh_dump_models.py.
    it's a dictionary, of the form:
    FieldName: [FieldType],
    """

    errorMsg = ''
    ans = '{\n'
    for fieldName,specs in define.iteritems():
        fieldType = specs[0]

        errorMsg += dsh_utils.black_break_msg_debug(
            'loop iteration: ' + fieldName + ' - ' + fieldType, 124)
        
        try:
            value = getattr(obj, fieldName)
        except:
            message = 'dsh_dump.dump_one: exception: ' + fieldName + '.  '
            dsh_django_utils.error_event(message, errorLevel='CRT')
            errorMsg += dsh_utils.red_error_break_msg(message)
            continue

        if fieldType == 'StrType':
            if not value:
                continue
            #
            # escape the double quote character.
            #
            value = value.replace('"', '\\"')
            oneField = "    '%s': ['%s', \"\"\"%s\"\"\"],\n" % \
                       (fieldName, fieldType, value)
            ans += oneField
            continue
            
        if fieldType == 'BoolType':
            oneField = "    '%s': ['%s', %s],\n" % \
                       (fieldName, fieldType, repr(value))
            ans += oneField
            continue

        if fieldType == 'IntType':
            oneField = "    '%s': ['%s', %s],\n" % \
                       (fieldName, fieldType, str(value))
            ans += oneField
            continue

        if fieldType == 'DateType':
            if not value:
                continue
            oneField = "    '%s': ['%s', %s],\n" % \
                       (fieldName, fieldType, repr(value))
            ans += oneField
            continue

        if fieldType == 'FileType':
            if not value:
                continue
            dumpFileName = dsh_agi.abs_url_to_relative(value.url)
            dsh_django_utils.debug_event(
                'dsh_dump.dump_one: url: ' + dumpFileName, 8)
            dsh_django_utils.debug_event(
                'dsh_dump.dump_one: tarPath: ' + tarPath, 8)

            success,tarMsg = add_to_tar(dumpFileName, tarPath)
            errorMsg += tarMsg
            if success:
                errorMsg += dsh_utils.black_break_msg(
                    'tar: ' + tarPath + \
                    '&nbsp;&nbsp;&nbsp;&#171;&nbsp;&nbsp;&nbsp;' + \
                    dumpFileName)
            else:
                errorMsg += dsh_utils.red_error_break_msg(
                    'tar command failed on: ' + dumpFileName)
                continue
            
            oneField = "    '%s': ['%s', \"\"\"%s\"\"\"],\n" % \
                       (fieldName, fieldType, dumpFileName)
            ans += oneField
            continue

        if fieldType == 'RequiredForeignOrgType' or \
               fieldType == 'RequiredForeignPersonType':
            if not value:
                errorMsg += dsh_utils.red_error_break_msg(
                    'missing required foreign org. or person.')
                continue
            foreignDshUid = value.dsh_uid

            oneField = "    '%s': ['%s', \"\"\"%s\"\"\"],\n" % \
                       (fieldName, fieldType, foreignDshUid)
            ans += oneField
            continue

        if fieldType == 'OptionalFollowUpsType' or \
               fieldType == 'OptionalOwnerType':
            #
            # like the above, except it's optional.
            # so if it's blank, we don't freak out.
            #
            if not value:
                continue
            foreignDshUid = value.dsh_uid

            oneField = "    '%s': ['%s', \"\"\"%s\"\"\"],\n" % \
                       (fieldName, fieldType, foreignDshUid)
            ans += oneField
            continue

        if fieldType == 'OptionalKeyWordsType' or \
           fieldType == 'OptionalPersonsType':
            #
            # the intended_audience field can be dealt with like this too.
            #
            if not value:
                continue
            dshUidList = get_dsh_uid_list(value)
            if not dshUidList:
                continue
            oneField = "    '%s': ['%s', %s],\n" % \
                       (fieldName, fieldType, repr(dshUidList))
            ans += oneField
            continue

        errorMsg += dsh_utils.red_error_break_msg(
            'unknown field type: ' + fieldType)
        

    ans += '}'
    return (ans, errorMsg)



def get_dsh_uid_list(listField):
    """called by dump_one().
    used to retrieve, for example, a list of key word dsh_uids.
    """
    ans = []
    objs = listField.all()
    for obj in objs:
        ans.append(obj.dsh_uid)
    return ans

    

def add_to_tar(fileToAdd, tarFilePath):
    """adds fileToAdd to tarFilePath."""

    tarBin = dsh_django_config.lookup('TAR_PATH')
    mediaDir = dsh_config.lookup('MEDIA_DIR')
    
    try:
        os.chdir(mediaDir)

        if not dsh_utils.is_valid_file(fileToAdd, silent=True):
            message = 'dsh_dump.add_to_tar: invalid file: ' + fileToAdd
            tarMsg = dsh_utils.red_error_break_msg(message)
            dsh_django_utils.error_event(message, errorLevel='ERR')
            return (False, tarMsg)
        
        command = tarBin + ' rf ' + tarFilePath + ' ' + fileToAdd
        dsh_django_utils.debug_event(
            'dsh_dump.add_to_tar: command: ' + command, 8)
        result = dsh_utils.try_execute(command)
        if result == None:
            message = 'dsh_dump.add_to_tar: tar problem: ' + command
            dsh_django_utils.error_event(message, errorLevel='CRT')
            return (False, dsh_utils.red_error_break_msg(message))
        return (True, '')
    
    except:
        message = 'dsh_dump.add_to_tar: unknown tar problem: ' + command
        dsh_django_utils.error_event(message, errorLevel='CRT')
        return (False, dsh_utils.red_error_break_msg(message))
        


def write_dump_file(dumpFile, dumpPath, content):
    try:
        content = smart_str(content)
        dumpFile.write(content)
        return True
    except:
        dsh_django_utils.error_event(
            'dsh_dump.write_dump_file: failed to write file: ' + dumpPath,
        errorLevel='CRT')
        return False
        


def dump_one_table(dumpFile, dumpPath, tarPath, whatKind, dumpDefinition,
                  dumpedVarName, dumpAll=False):
    """called by dump_selected().
    whatKind is something like db.models.KeyWord.
    dumpDefinition is something like the union of:
    dsh_dump_models.DshObjectDef and dsh_dump_models.KeyWordDef.
    dumpedVarName is something like 'SelectedKeyWords',
    the global variable name of the dictionary used in the dumped file.
    """

    if dumpAll:
        selectedObjs = whatKind.objects.all()
    else:
        selectedObjs = whatKind.objects.filter(u17=True)
        
    ans = dumpedVarName + ' = [\n'
    errorMsg = ''
    for obj in selectedObjs:
        dumpStr,errStr = dump_one(obj, dumpDefinition, tarPath)
        ans += dumpStr
        ans += ',\n'
        errorMsg += errStr
    ans += ']\n'

    dumpSuccess = write_dump_file(dumpFile, dumpPath, ans)
    if dumpSuccess:
        result = 'success'
    else:
        result = 'failure'
    errorMsg += dsh_utils.black_break_msg(
        result + ':  ' + str(len(selectedObjs)) + ' objects dumped.')
    errorMsg += '<br>\n'
    return (dumpSuccess, errorMsg)



def dump_selected(dumpFile, dumpPath, tarPath, dumpAll=False,
                  dumpPersons=False):
    """called by views.dump().
    dumps selected items from each table.
    if dumpPersons is True,
    we're dumping all persons and organizations, nothing else."""

    totalSuccess = True
    errorMsg = ''

    if not dumpAll:
        propagate_selections()

    #
    # key words.
    #
    errorMsg += dsh_utils.black_break_msg('dumping KeyWord table...')
    keyWordDef = dsh_utils.union_dict(
        dsh_dump_models.DshObjectDef,
        dsh_dump_models.KeyWordDef)
    success,errMsg = dump_one_table(dumpFile, dumpPath, tarPath,
                                    dvoice.db.models.KeyWord,
                                    keyWordDef, 'SelectedKeyWords',
                                    dumpAll=dumpAll)
    totalSuccess = totalSuccess and success
    errorMsg += errMsg


    #
    # organizations.
    #
    errorMsg += dsh_utils.black_break_msg('dumping Organization table...')
    orgDef = dsh_utils.union_dict(
        dsh_dump_models.DshObjectDef,
        dsh_dump_models.OrgDef)
    success,errMsg = dump_one_table(dumpFile, dumpPath, tarPath,
                                    dvoice.db.models.Organization,
                                    orgDef, 'SelectedOrgs',
                                    dumpAll=dumpAll or dumpPersons)
    totalSuccess = totalSuccess and success
    errorMsg += errMsg


    #
    # persons.
    #
    errorMsg += dsh_utils.black_break_msg('dumping Person table...')
    personDef = dsh_utils.union_dict(
        dsh_dump_models.DshObjectDef,
        dsh_dump_models.PersonDef)
    success,errMsg = dump_one_table(dumpFile, dumpPath, tarPath,
                                    dvoice.db.models.Person,
                                    personDef, 'SelectedPersons',
                                    dumpAll=dumpAll or dumpPersons)
    totalSuccess = totalSuccess and success
    errorMsg += errMsg


    #
    # items.
    #
    errorMsg += dsh_utils.black_break_msg('dumping Item table...')
    itemDef = dsh_utils.union_dict(
        dsh_dump_models.DshObjectDef,
        dsh_dump_models.ItemDef)
    success,errMsg = dump_one_table(dumpFile, dumpPath, tarPath,
                                    dvoice.db.models.Item,
                                    itemDef, 'SelectedItems',
                                    dumpAll=dumpAll)
    totalSuccess = totalSuccess and success
    errorMsg += errMsg
    

    #
    # events.
    #
    errorMsg += dsh_utils.black_break_msg('dumping Event table...')
    eventDef = dsh_utils.union_dict(
        dsh_dump_models.DshObjectDef,
        dsh_dump_models.EventDef)
    success,errMsg = dump_one_table(dumpFile, dumpPath, tarPath,
                                    dvoice.db.models.Event,
                                    eventDef, 'SelectedEvents',
                                    dumpAll=dumpAll)
    totalSuccess = totalSuccess and success
    errorMsg += errMsg
    
    return (totalSuccess, errorMsg)



def check_new_or_old(dump, whatKind, overWrite, itemsToSkip=None):
    """upon loading, see if we need to make a new object, or
    we are overwriting an existing old object.
    returns (success, newObj, obj)
    called by load_one() and load_pointers_for_one()"""

    #
    # check the dsh_uid.
    # to see if it's already in the database.
    #
    if not dump.has_key('dsh_uid'):
        dsh_utils.give_bad_news('dsh_dump.check_new_or_old: ' + \
                                'failed to find dsh_uid',
                                logging.critical)
        return (False, False, None)

    dshUid = dump['dsh_uid'][1]

    existingObjs = whatKind.objects.filter(dsh_uid=dshUid)
    howMany = len(existingObjs)
    if howMany > 1:
        dsh_utils.give_bad_news(
            'dsh_dump.check_new_or_old: found multiple dsh_uids: ' + \
            dshUid, logging.critical)
        if itemsToSkip != None:
            itemsToSkip.append(dshUid)
        return (False, False, None)


    #
    # if it's already in the database...
    #
    if howMany == 1:
        dsh_utils.db_print('dsh_dump.check_new_or_old: dsh_uid found 1: ' + \
                           dshUid, 105)
        if not overWrite:
            #
            # give up if we don't want to overwrite it.
            #
            dsh_utils.give_news(
                'dsh_dump.check_new_or_old: not overwriting dsh_uid: ' + \
                dshUid, logging.info)
            if itemsToSkip != None:
                itemsToSkip.append(dshUid)
            return (True, False, None)

        #
        # we will overwrite the existing object.
        #
        dsh_utils.give_news(
            'dsh_dump.check_new_or_old: ' + \
            'overwriting dsh_uid: ' + dshUid, logging.info)
        obj = existingObjs[0]
        return (True, False, obj)
    else:
        #
        # it's not in the existing database.
        # so we'll make a new one.
        #
        dsh_utils.give_news('dsh_dump.check_new_or_old: dsh_uid to save: ' + \
                            dshUid, logging.info)
        obj = whatKind()
        return (True, True, obj)



def load_one(dump, whatKind, overWrite, itemsToSkip=None):
    """called by dsh_load.py, to load one dumped object into the django db.
    'dump' is a dictionary, read from the dump file. of the form:
    fieldName: [fieldType, fieldValue],
    'whatKind' is the Class.  like: KeyWord, Organization, Person, Item.
    """
    
    dsh_utils.db_print('dsh_dump.load_one: entered... ' + repr(dump), 105)
    
    success,newObj,obj = check_new_or_old(dump, whatKind, overWrite,
                                          itemsToSkip=itemsToSkip)
    if not success or obj == None:
        return success
    dshUid = dump['dsh_uid'][1]


    #
    # take all the fields from the dump file.
    #
    for fieldName,fieldContent in dump.iteritems():
        
        fieldType,fieldValue = fieldContent

        #
        # some fields take some work to load.
        #
        if fieldType == 'RequiredForeignOrgType':
            #
            # fieldValue is a dsh_uid.
            # get the org that has this dsh_uid.
            #
            org = get_foreign_key(dvoice.db.models.Organization, fieldValue)
            if not org:
                dsh_utils.give_bad_news(
                    'dsh_dump.load_one: failed on RequiredForeignOrgType: '+\
                    fieldValue, logging.error)
                #
                # because it's a required field,
                # there's no point continuing---loading is aborted.
                #
                return False
            setattr(obj, fieldName, org)
            continue

        if fieldType == 'RequiredForeignPersonType':
            #
            # similar to the case above.
            #
            person = get_foreign_key(dvoice.db.models.Person, fieldValue)
            if not person:
                dsh_utils.give_bad_news(
                    'dsh_dump.load_one: ' +\
                    'failed on RequiredForeignPersonType: ' +\
                    fieldValue, logging.error)
                return False
            setattr(obj, fieldName, person)
            continue

        if fieldType == 'OptionalFollowUpsType' or \
           fieldType == 'OptionalKeyWordsType' or \
           fieldType == 'OptionalPersonsType':
            #
            # this is to be dealt with in a second round.
            # so we skip it in this round.
            # if I don't say something here, however,
            # it falls through the default case at the bottom.
            # the default case is for trivial field types.
            #
            continue

        if fieldType == 'OptionalOwnerType':
            #
            # this is used by the Event table.
            # like owner of the Item table.
            # except it's optional this time.
            #
            person = get_foreign_key(dvoice.db.models.Person, fieldValue)
            if not person:
                continue
            setattr(obj, fieldName, person)
            continue
            
        #
        # all other types of fields (like string and int) are easy to set.
        #
        setattr(obj, fieldName, fieldValue)

        
    dsh_utils.db_print('dsh_dump.load_one: obj is: ' + repr(obj), 105)


    #
    # finally, put it in the django database.
    #
    try:
        obj.save()
        dsh_utils.db_print('dsh_dump.load_one: obj is saved.', 105)
    except:
        dsh_utils.give_bad_news('dsh_dump.load_one: obj.save() failed: ' +\
                                dshUid, logging.critical)
        return False

    return True



def load_pointers_for_one(dump, whatKind, overWrite, itemsToSkip):
    """going through the dumped object the second round to
    set all the pointers within.
    for example, the 'followup_to' field in the Item table.
    """
    
    dsh_utils.db_print('dsh_dump.load_pointers_for_one: entered... ' +\
                       repr(dump), 105)

    if not dump.has_key('dsh_uid'):
        return False
    dshUid = dump['dsh_uid'][1]

    #
    # this means that the first round of loading items has decided that
    # this item should not proceed to a second round.
    #
    if dshUid in itemsToSkip:
        return True

    #
    # set the "overWrite" arg to True.
    #
    success,newObj,obj = check_new_or_old(dump, whatKind, True)
    if not success or obj == None:
        dsh_utils.give_bad_news(
            'dsh_dump.load_pointers_for_one: check_new_or_old failed.',
            logging.error)
        return success


    #
    # take all the fields from the dump file.
    #
    for fieldName,fieldContent in dump.iteritems():
        
        fieldType,fieldValue = fieldContent

        if fieldType == 'OptionalFollowUpsType':
            #
            # fieldValue is a dsh_uid.
            # get the item that has this dsh_uid.
            #
            followItem = get_foreign_key(
                dvoice.db.models.Item, fieldValue)
            if not followItem:
                dsh_utils.give_bad_news(
                    'dsh_dump.load_pointers_for_one: ' + \
                    'cannot find followup_to item: '+\
                    fieldValue, logging.error)
                #
                # because it's optional, we'll just move on.
                # not a big deal.
                #
                continue
            setattr(obj, fieldName, followItem)
            continue

        if fieldType == 'OptionalKeyWordsType':
            #
            # instead of a single foreign key,
            # now we're dealing with a list of foreign keys
            # in a many-to-many relationship.
            #
            # this also has to be dealt with in a second round because...
            # it turns out I must do a save to obtain a primary key,
            # otherwise I can't set many-to-many attr.
            # and unfortunately, the dump "spec," which is just a dictionary,
            # when you iterate through it, it goes in an unpredictable order,
            # so the owner and such required keys could be encountered after
            # this field.
            # this is why this field is moved here.
            #
            keyWords = get_foreign_key_list(dvoice.db.models.KeyWord,
                                            fieldValue)
            if keyWords == None:
                #
                # this shouldn't happen. in the worst case, it should've
                # been an empty list.
                #
                dsh_utils.give_bad_news(
                    'dsh_dump.load_one: something bad happened with ' +\
                    'loading key words: ' + repr(keyWords),
                    logging.critical)
                continue
            if keyWords == []:
                continue
            #
            # it turns out I must do a save to obtain a primary key,
            # otherwise I can't set many-to-many attr.
            #
            #if newObj:
            #    obj.save()
            setattr(obj, fieldName, keyWords)
            continue
            
        if fieldType == 'OptionalPersonsType':
            #
            # like the KeyWord type above.
            # I should've tried to reduce repetition.
            #
            audience = get_foreign_key_list(dvoice.db.models.Person,
                                            fieldValue)
            if audience == None:
                #
                # this shouldn't happen. in the worst case, it should've
                # been an empty list.
                #
                dsh_utils.give_bad_news(
                    'dsh_dump.load_one: something bad happened with ' +\
                    'loading audience: ' + repr(audience),
                    logging.critical)
                continue
            if audience == []:
                continue
            #
            # it turns out I must do a save to obtain a primary key,
            # otherwise I can't set many-to-many attr.
            #
            #if newObj:
            #    obj.save()
            setattr(obj, fieldName, audience)
            continue
            

        #
        # do nothing with any other types of fields.
        #

    #
    # finally, put it in the django database.
    #
    try:
        obj.save()
        dsh_utils.db_print('dsh_dump.load_pointers_for_one: obj is saved.',
                           105)
    except:
        dsh_utils.give_bad_news(
            'dsh_dump.load_pointers_for_one: obj.save() failed: ' +\
            dshUid, logging.critical)
        return False

    return True



def get_foreign_key(whatKind, dshUid):
    """called by load_one().  locate a foreign key object."""
    return dsh_django_utils.get_foreign_key(whatKind, dshUid)
    


def get_foreign_key_list(whatKind, dshUidList, required=False):
    """called by load_one().  locate a list of foreign key objects.
    like a list of key words."""

    ansList = []
    for dshUid in dshUidList:
        obj = get_foreign_key(whatKind, dshUid)
        if not obj:
            if required:
                dsh_utils.give_bad_news(
                    'dsh_dump.get_foreign_key_list: missing required obj :'+\
                    dshUid, logging.error)
                return None
            #
            # if it's not required and we can't find it in the list.
            # this is like a missing key word, not a big deal.
            # but perhaps I should warn.
            #
            dsh_utils.give_bad_news(
                'dsh_dump.get_foreign_key_list: missing optional obj: ' +\
                dshUid, logging.warning)
            continue
        ansList.append(obj)
    return ansList
            
    

def load_all(allKeyWords, allOrgs, allPersons, allItems, allEvents, overWrite):
    """called by dsh_load.py"""

    #
    # key words.
    #
    dsh_utils.give_news('dsh_dump.load_all: loading key words...',
                        logging.info)
    for keyWord in allKeyWords:
        load_one(keyWord, dvoice.db.models.KeyWord, overWrite)

    #
    # organizations.
    #
    dsh_utils.give_news('dsh_dump.load_all: loading organizations...',
                        logging.info)
    for org in allOrgs:
        load_one(org, dvoice.db.models.Organization, overWrite)

    #
    # persons.
    #
    dsh_utils.give_news('dsh_dump.load_all: loading persons...',
                        logging.info)
    for person in allPersons:
        load_one(person, dvoice.db.models.Person, overWrite)

    #
    # items.
    #
    # if this item should not proceed to a second round,
    # put it in the itemsToSkip list.
    #
    itemsToSkip = []
    dsh_utils.give_news('dsh_dump.load_all: loading items...',
                        logging.info)
    for item in allItems:
        load_one(item, dvoice.db.models.Item, overWrite,
                 itemsToSkip=itemsToSkip)

    #
    # load the pointers within the Item table.
    #
    dsh_utils.give_news('dsh_dump.load_all: loading pointers within items...',
                        logging.info)
    for item in allItems:
        load_pointers_for_one(item, dvoice.db.models.Item, overWrite,
                              itemsToSkip)

    #
    # events.
    #
    dsh_utils.give_news('dsh_dump.load_all: loading events...',
                        logging.info)
    for event in allEvents:
        load_one(event, dvoice.db.models.Event, overWrite)



def mark_selected_foreign(thisTable, foreignKeyFieldName,
                          kind='single'):
    """thisTable is something like Person.
    foreignKeyFieldName is 'organization'.
    this function will mark all the parent organizations of the
    selected persons selected as well.
    kind is either 'single' or 'many'.
    'single for single foreign keys.
    'many' for many-to-many relationships.
    """
    
    selectedObjs = thisTable.objects.filter(u17=True)
    if not selectedObjs:
        return
    
    for obj in selectedObjs:
        try:
            fk = getattr(obj, foreignKeyFieldName)
        except:
            dsh_django_utils.error_event(
                'dsh_dump.mark_selected_foreign: getattr failed on: ' + \
                obj.dsh_uid, errorLevel='CRT')
            continue
        if not fk:
            #
            # maybe the foreign key is null, that could be ok sometimes.
            #
            dsh_django_utils.debug_event(
                'dsh_dump.mark_selected_foreign: no fk.', 11)
            continue

        #
        # finally mark the foreign key object(s) selected.
        #
        if kind == 'single':
            if fk.u17:
                continue
            fk.u17 = True
            fk.save()
            dsh_django_utils.debug_event(
                'dsh_dump.mark_selected_foreign: marking active: ' +
                fk.dsh_uid, 11)
            continue
        
        if kind == 'many':
            objs = fk.all()
            for obj in objs:
                if obj.u17:
                    continue
                obj.u17 = True
                obj.save()
            continue



def deselect_all():
    messages = ''
    
    for tableName,tableInfo in allDbTables.iteritems():
        thisTable = tableInfo[0]
        tableStr = tableInfo[1]
        selectedObjs = thisTable.objects.filter(u17=True)
        if not selectedObjs:
            continue
        howMany = len(selectedObjs)
        messages += dsh_utils.black_break_msg(
            'de-selecting ' + str(howMany) + ' ' + tableStr + '...')
        for obj in selectedObjs:
            obj.u17 = False
            obj.save(noLogging=True)

    messages += dsh_utils.black_break_msg('done.')
    return messages



def count_selected(table):
    selectedObjs = table.objects.filter(u17=True)    
    return len(selectedObjs)



def count_all_selected():
    dsh_django_utils.debug_event('count_all_selected: entered...', 11)
    propagate_selections()
    d = {}
    for tableName,tableInfo in allDbTables.iteritems():
        d[tableName] = count_selected(tableInfo[0])
    return d



def propagate_selections():
    #
    # mark parent organizations of selected persons selected.
    # need to do more.
    #
    mark_selected_foreign(dvoice.db.models.Item, 'owner')
    mark_selected_foreign(dvoice.db.models.Item, 'intended_audience',
                          kind='many')
    mark_selected_foreign(dvoice.db.models.Item, 'i05')
    dsh_django_utils.debug_event(
        'propagate_selections: mark event owner...', 11)
    mark_selected_foreign(dvoice.db.models.Event, 'owner')
    mark_selected_foreign(dvoice.db.models.Person, 'organization')
    mark_selected_foreign(dvoice.db.models.Item, 'key_words', kind='many')



def select_box(whatKind, dshUid):
    """called by views.select_one()."""
    obj = get_foreign_key(whatKind, dshUid)
    if not obj:
        return False
    if obj.u17:
        return True
    obj.u17 = True
    obj.save(noLogging=True)
    return True
