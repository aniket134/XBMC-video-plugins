import sys,os,subprocess,logging
import dsh_dump
import dv2.db.models
#from dv2.db.models import Organization, Person, Item, KeyWord, Event
import dsh_django_config,dsh_django_utils,dsh_dump_models
import dsh_django_utils2
dsh_django_utils2.append_to_sys_path(
    dsh_django_config.lookup('DSH_VOICE_CODE_DIR'))
import dsh_utils,dsh_config,dsh_agi
from django.utils.encoding import smart_str, smart_unicode
import dsh_common_selection



def keyword_add_del(dshUid, action='add'):
    """called by views.keyword_add() and views.keyword_del()."""
    
    errorMsg = ''
    keyWord = dsh_dump.get_foreign_key(dv2.db.models.KeyWord, dshUid)
    if not keyWord:
        message = 'dsh_selection.keyword_add_del: bad key word dshUid: ' +\
                  repr(dshUid)
        dsh_django_utils.error_event(message, errorLevel='ERR')
        errorMsg += dsh_utils.red_error_break_msg(message)
        return errorMsg

    selectedItems = dv2.db.models.Item.objects.filter(u17=True)
    if not selectedItems:
        errorMsg += dsh_utils.red_error_break_msg(
            'no item selected currently.')
        return errorMsg

    count = 0
    for item in selectedItems:
        kwList = item.key_words.all()
        if action == 'add':
            if keyWord in kwList:
                continue
            try:
                item.key_words.add(keyWord)
                item.save(noLogging=True)
                count += 1
            except:
                message = 'dsh_selection.key_word_add_del: key word add ' +\
                          'failed: ' + repr(dshUid)
                dsh_django_utils.error_event(message, errorLevel='CRT')
                errorMsg += dsh_utils.red_error_break_msg(message)
                return errorMsg
        elif action == 'del':
            if not (keyWord in kwList):
                continue
            try:
                item.key_words.remove(keyWord)
                item.save(noLogging=True)
                count += 1
            except:
                message = 'dsh_selection.key_word_add_del: key word del ' +\
                          'failed: ' + repr(dshUid)
                dsh_django_utils.error_event(message, errorLevel='CRT')
                errorMsg += dsh_utils.red_error_break_msg(message)
                return errorMsg
        else:
            return dsh_utils.red_error_break_msg('bad action: ' + action)

    if action == 'add':
        actDone = 'added to'
        logAction = 'KADD'
    elif action == 'del':
        actDone = 'removed from'
        logAction = 'KDEL'
    else:
        return dsh_utils.red_error_break_msg('bad action: ' + action)

    keyStr = keyWord.key_word
    message = 'key word "%s" %s %s items.' % (keyStr, actDone, str(count))
    errorMsg += dsh_utils.black_break_msg(message)

    dsh_agi.report_event(
        message,
        action=logAction,
        item=keyWord)
    
    return errorMsg



def email_selections(emailAddrs, attach, comments='', urlFields=None):
    """called by views.email_selection()."""

    returnMsg = ''


    #
    # display the email addresses.
    #
    returnMsg = dsh_utils.black_break_msg('<i><u>email(s) sent to:</u></i>\n')
    for email in emailAddrs:
        returnMsg += dsh_utils.black_break_msg(email)
    returnMsg += '<BR>\n'


    #
    # deal with comments: display them, include them.
    #
    emailText = ''
    if comments:
        returnMsg += '<i><u>comments:</u></i><br>\n'
        returnMsg += comments
        returnMsg += '<br><br>'
        emailText = '[comments:]\n\n%s\n' % (comments,)
        emailText += '\n---------------\n\n'


    #
    # now loop through all the selected items.
    #
    returnMsg += dsh_utils.black_break_msg('<i><u>items sent:</u></i><br>\n')
    
    selectedItems = dv2.db.models.Item.objects.filter(u17=True)
    if not selectedItems:
        returnMsg += dsh_utils.red_error_break_msg(
            'no item selected currently.')
        return returnMsg

    #
    # 09/11/14:
    # reverse it so it's in reverse chronological order.
    # for some reason, this didn't work...
    #
    #selectedItems.reverse()
    

    count = 0
    displayText = '<TABLE border=1>\n'
    fileList = []
    attachedFileList = []
    

    #
    # 09/11/14:
    # reverse it so it's in reverse chronological order.
    #
    for item in selectedItems[::-1]:

        emailText += smart_unicode(item.email_text(attach=attach,
                                                   urlFields=urlFields))
        emailText += '\n---------------\n\n'

        
        displayText += '<TR><TD>%s</TD></TR>\n' % \
                       (item.email_text(br=True, attach=attach,
                                        urlFields=urlFields,
                                        allowTags=True),)

        if attach:
            file = item.full_file_path()
            attachedFile = item.attachment_file_name()
        
            if file and attachedFile:
                fileList.append(file)
                attachedFileList.append(attachedFile)
            
    displayText += '</TABLE>\n'
    returnMsg += smart_unicode(displayText)
    
    returnMsg += dsh_utils.black_break_msg_debug('', 118)
    returnMsg += dsh_utils.black_break_msg_debug(repr(fileList), 118)
    returnMsg += dsh_utils.black_break_msg_debug('', 118)
    returnMsg += dsh_utils.black_break_msg_debug(repr(attachedFileList), 118)

    emailText = smart_unicode(emailText)
    emailText = smart_str(emailText)


    #
    # got everything.  ready to actually call gmail_send().
    #
    try:
        success,errorMsg = dsh_utils.gmail_send(
            dsh_config.lookup('GMAIL_SENDER_ADDRESS'),
            dsh_config.lookup('GMAIL_SENDER_PASSWORD'),
            emailAddrs,
            dsh_config.lookup('GMAIL_SENDER_SUBJECT'),
            emailText,
            attachedFiles=fileList,
            attachmentNames=attachedFileList)
        if success:
            message = 'selection emailed to: %s.  comments: %s.' %\
                      (', '.join(emailAddrs), comments)
            dsh_agi.report_event(message, action='EMAI')
            returnMsg += '<br>' + dsh_utils.black_break_msg('Message sent.')
        else:
            dsh_django_utils.error_event(errorMsg, errorLevel='ERR')
            returnMsg += '<br>' + dsh_utils.red_error_break_msg(errorMsg)
    except:
        message = 'dsh_selection.email_selections: gmail_send() failed. ' +\
                  'Unexpected error.  Tell Randy about this page.'
        dsh_django_utils.error_event(message, errorLevel='ERR')
        returnMsg += '<br>' + dsh_utils.red_error_break_msg(message)
        
    return returnMsg



def star(action='add'):
    """star the selection."""

    response = ''
    
    selectedItems = dv2.db.models.Item.objects.filter(u17=True)
    if not selectedItems:
        response += dsh_utils.red_error_break_msg(
            'no item selected currently.')
        return response

    count = 0
    for item in selectedItems:

        if action == 'add':
            if item.starred:
                continue
            item.starred = True
        else:
            if not item.starred:
                continue
            item.starred = False

        try:
            item.save(noLogging=True)
            count += 1
        except:
            message = 'dsh_selection.star: failed to save: ' +\
                      item.dsh_uid
            dsh_django_utils.error_event(message, errorLevel='CRT')
            response += dsh_utils.red_error_break_msg(message)
            return response

    if action == 'add':
        actDone = 'starred'
    else:
        actDone = 'de-starred'
        

    message = '%s item(s) %s.' % (str(count), actDone)
    response += dsh_utils.black_break_msg(message)
    dsh_agi.report_event(message, action='STAR')

    return response



def select_starred():
    """called by views.select_starred()."""

    response = ''

    starred = dv2.db.models.Item.objects.filter(starred=True)
    if not starred:
        response += dsh_utils.red_error_break_msg(
            'no starred item.')
        return response

    count = 0
    for item in starred:
        if item.u17:
            continue
        item.u17 = True

        try:
            item.save(noLogging=True)
            count += 1
        except:
            message = 'dsh_selection.select_starred: failed to save: ' +\
                      item.dsh_uid
            dsh_django_utils.error_event(message, errorLevel='CRT')
            response += dsh_utils.red_error_break_msg(message)
            return response

    message = '%s starred item(s) selected.' % (str(count),)
    response += dsh_utils.black_break_msg(message)
    dsh_agi.report_event(message)

    return response



def process_selection(fieldStr, action='set'):
    """
    initially modeled after star().
    filedStr is something like "starred" or "active" or "peer_shared".
    they are fields defined in db/models.py.
    action is either "set" or "clear".
    returns the html response string to be displayed.
    calls common/dsh_common_selection.process_selection() to do the real work.
    but need to first get the list of selected items.
    """

    selectedItems = dv2.db.models.Item.objects.filter(u17=True)
    return dsh_common_selection.process_selection(
        selectedItems, fieldStr, action=action)
