#
# initially modeled after views.py (10/01/12)
#
import sys,os,logging,datetime
from django.template.loader import get_template
from django.template import Context
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
import dsh_django_request,dsh_django_utils,dsh_django_config,dsh_db_config
import views,dsh_selection
import dsh_common_db,dsh_common_selection,dsh_common_agi
import dsh_utils,dsh_agi



def selection_deactivate(request):
    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('de-activate the selected items')
    response += dsh_selection.process_selection('active', action='clear')
    response += views.page_footer()
    return HttpResponse(response)



def selection_activate(request):
    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('activate the selected items')
    response += dsh_selection.process_selection('active', action='set')
    response += views.page_footer()
    return HttpResponse(response)



def selection_share(request):
    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('peer-share the selected items')
    response += dsh_selection.process_selection('peer_shared', action='set')
    response += views.page_footer()
    return HttpResponse(response)



def selection_unshare(request):
    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('unshare the selected items')
    response += dsh_selection.process_selection('peer_shared', action='clear')
    response += views.page_footer()
    return HttpResponse(response)



def tutorials(request):
    """broken out of views.tutorials()."""
    response = views.page_header('instructions with screenshots')

    response += """
<table border=1>

<tr>
<td><span style="white-space: nowrap;">2010-04-14</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/4f954d87cd6676cc">a person's latest event</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-04-11</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/17191f1abddc0d4d">scheduling 1st broadcast for Lokarpit Voice</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-04-10</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/9457bde938d72867">field trip demo without carrying a computer</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-04-04</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/48ebce3685cd3387">multiple answers per doctor call</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-31</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/7c4d1a80df2adbde">un-hear a message</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-30</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/88fcdcad4aefb62e">change the behavior of Current Dial Set</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-29</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/fc0d5473d4245e3d">look at the event table, un-answer a deleted answer</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-28</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/6f9d9eed2d85635d">display conversation (thread) history and un-answer</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-27</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/566d3bb36f881f3c">un-answer a previously answered question</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-24</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/e6c6370d35f9630c">doctors' phone interface</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-22</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/d5c5c8445eb64bbb">keeping track of the people to be called when auto-dial is disabled</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-19</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/5619dbdd2090e229">prevent wiping of an existing schedule during reschedule</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-18</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/fbe0630bdbbc4e23">how to email messages with a certain key word</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-18</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/a42ff67320fa5fa">schedule a doctor's reply without turning on global auto-dial</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-16</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/23cdfb1b697f98a5#">IAX soft phone: Zoiper or Kiax</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-14</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/bda548b8d00cb5b7">dealing with mobile numbers that start with 8</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-14</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/72a7d4f6faa7b7e4">enter people's age</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-03-08</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/5d8b20d6e2581a3b">upload a reply message for a particular question</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-02-14</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/8d33c50c992ab63b">mark a message as "play-once"</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-02-12</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/a16be72bdfb235a0">get the system to call yourself, then you press 2 to call someone else</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-02-11</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/e77d6b26484d3a90">how to add a new person to the auto-dialed schedule</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-01-20</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/a12c8891e237c49e">use "group key words" to tag broadcast messages and recipient organizations (for DIET)</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2010-01-12</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/4371480738fb9ae1">new bulk operations</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2009-11-24</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/dc5759719ed20afc">list of listeners</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2009-09-25</span></td>
<td>
<a href="http://dsh.cs.washington.edu:8000/Projects/StudyHall_Discuss/upload/090925-213545.14640.check_spoken_screen.jpg">check spoken names of authors and organizations of shared messages</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2009-09-21</span></td>
<td>
<a href="http://groups.google.com/group/dsh-discuss/browse_thread/thread/942d6f3fa78c3d54">direct peer-shared messages</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2009-09-12</span></td>
<td>
<a href="http://dsh.cs.washington.edu:8000/Projects/StudyHall_Discuss/upload/090912-032439.17307.auto_dial_instruction.jpg">schedule auto-dialed broadcast calls</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2009-08-29</span></td>
<td>
<a href="http://dsh.cs.washington.edu:8000/Projects/StudyHall_Discuss/upload/090829-113802.10451.email_voice_instruction.jpg">email selected voice messages</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2009-08-27</span></td>
<td>
<a href="http://dsh.cs.washington.edu:8000/Projects/StudyHall_Discuss/upload/090827-113910.30533.spam_call_instruction.jpg">schedule auto-dialed personalized calls</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2009-08-24</span></td>
<td>
<a href="http://dsh.cs.washington.edu:8000/Projects/StudyHall_Discuss/upload/090824-033021.14763.shared_number_instruction.jpg">phone numbers shared by multiple people</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2009-08-11</span></td>
<td>
<a href="http://dsh.cs.washington.edu:8000/Projects/StudyHall_Discuss/upload/090811-135652.16467.keyword_selection_instruction.jpg">apply or remove key words from selected items</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2009-08-10</span></td>
<td>
<a href="http://dsh.cs.washington.edu:8000/Projects/StudyHall_Discuss/upload/090810-073240.3275.personalized_message_instruction.jpg">personalized messages</a>
</td>
</tr>

<tr>
<td><span style="white-space: nowrap;">2009-07-29</span></td>
<td>
<a href="http://dsh.cs.washington.edu:8000/Projects/StudyHall_Discuss/upload/090729-162817.26326.django_asterisk_instruction.jpg">first: basic operations on the item list page</a>
</td>
</tr>

</table>

<BR>
"""
    response += views.page_footer()
    return HttpResponse(response)



def reply_upload(request, dshUid):
    """
    10/03/06:
    called by views.reply_upload().
    displays a page asking for confirming to make a blank reply.
    modeled after views.reply()
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('reply to a message')
    response += """
<BR>
You're about to create a blank reply, which needs to be further refined.
<a href='/replyuploadsubmit/%s'>Confirm</a>?
<BR>
""" % (dshUid,)
    response += views.page_footer()
    return HttpResponse(response)
    


def reply_upload_submit(request, dshUid):
    """
    10/03/06:
    called by views.reply_upload_submit().
    a temporary reply has been put in.
    modeled after views.reply_submit()
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('a reply is initiated')

    success,msgs = dsh_django_utils.save_red5_mp3_in_django(
        None, originalItemDshUid=dshUid, copyBlankReply=True)
    response += msgs

    response += views.page_footer()
    return HttpResponse(response)



def demographics(request, dshUid, personTable):
    """
    10/03/13:
    called by views.demographics().
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('demographics', includeMp3Player=True)
    person = dsh_django_utils.get_foreign_key(personTable, dshUid)

    if not person:
        message = 'dsh_common_views.demographics: no person found: ' + dshUid
        response += dsh_utils.red_error_break_msg(message)
        dsh_django_utils.error_event(message, errorLevel='ERR')
        response += page_footer()
        return HttpResponse(response)

    personEditUrl = dsh_django_config.lookup('PERSON_DETAIL_URL') + \
                    str(person.id)
    thumb = dsh_django_utils.thumbnail(
        person, person.mugshot, noCenter=True)
    url = '<a href=%s title="edit person details">%s</a>' % \
          (personEditUrl, thumb)

    response += url

    response += '<BR><BR>'
    response += '<TABLE BORDER=1>'

    name = person.__unicode__()
    if name:
        response += '<TR><TD>name</TD><TD>%s</TD></TR>' % (name,)

    if person.spoken_name:
        spokenName = person.spoken_name_display_field()
        if spokenName:
            response += '<TR><TD>spoken name</TD><TD>%s</TD></TR>' % \
                        (spokenName)

    response += '<TR><TD>dsh uid</TD><TD>%s</TD></TR>' % (person.dsh_uid,)

    if person.phone_number:
        response += '<TR><TD>phone</TD><TD>%s</TD></TR>' % \
                    (person.phone_number,)

    if person.organization and person.organization.alias:
        response += '<TR><TD>org.</TD><TD>%s</TD></TR>' % \
                    (person.organization.alias,)

    if person.ptype:
        response += '<TR><TD>type</TD><TD>%s</TD></TR>' % (person.ptype,)

    if person.gender:
        response += '<TR><TD>gender</TD><TD>%s</TD></TR>' % (person.gender,)
        
    if person.date_birth:
        if person.birth_date_approximate:
            dateStr = str(person.date_birth.year)
        else:
            dateStr = person.date_birth.isoformat()
        response += '<TR><TD>birth date</TD><TD>%s</TD></TR>' % (dateStr,)

    if person.birth_date_approximate:
        response += '<TR><TD>birth date approximate</TD><TD>True</TD></TR>'

    if person.date_birth:
        years = dsh_common_db.calculate_age(person)
        if years:
            response += '<TR><TD>age</TD><TD>%s</TD></TR>' % (str(years),)

    if person.modify_datetime:
        timeStr = person.modify_datetime.strftime(
            '%#Y-%#m-%#d %#H:%#M:%#S')
        response += '<TR><TD>modify time</TD><TD>%s</TD></TR>' % (timeStr,)
    
    response += '</TABLE>'
    
    response += views.mp3_widget_control()
    response += views.page_footer()
    return HttpResponse(response)



def keyword_select(request, dshUid, keyWordTable, itemTable):
    """called by views.keyword_select().
    add the keyworded items to the current selection.
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('select items with this key word')

    success,msgs = dsh_common_selection.keyword_select(
        dshUid, keyWordTable, itemTable)
    response += msgs

    response += views.page_footer()
    return HttpResponse(response)



def keyword_deselect(request, dshUid, keyWordTable, itemTable):
    """called by views.keyword_select().
    remove the keyworded items from the current selection.
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('de-select items with this key word')

    success,msgs = dsh_common_selection.keyword_select(
        dshUid, keyWordTable, itemTable, action='deselect')
    response += msgs

    response += views.page_footer()
    return HttpResponse(response)



def spool_wipe_status_message():
    """called by reschedule(), auto_dial_enable(), and auto_dial_disable().
    displays the current status of spool directory wiping."""
    
    response = ''
    disableWipe = dsh_db_config.get('reschedule_wipe_disable')
    if disableWipe:
        response += dsh_utils.black_break_msg(
            'note: wiping of existing schedule is disabled.')
    return response



def reschedule(request, personTable):
    """
    10/03/19: moved from views.py
    a combination of delete all and active."""
    
    if dsh_django_request.deny_it(request):
        return views.please_log_in()
    
    response = views.page_header('reschedule auto-dialed calls')
    dsh_common_agi.auto_schedule_delete_all()

    response += spool_wipe_status_message()

    disabled = dsh_db_config.get('auto_dial_disable')
    if disabled:
        response += dsh_utils.black_break_msg(
            'global auto-dial is currently ' +\
            '<font color=red><b>disabled</b></font>.')
        response += dsh_utils.black_break_msg(
            'processing people in the current dial set...')
        response += dsh_common_selection.reschedule_current_dial_set(
            personTable)
    else:
        response += dsh_utils.black_break_msg(
            'global auto-dial is currently ' +\
            '<font color=green><b>enabled</b></font>.')
        response += dsh_utils.black_break_msg(
            'processing all people...')
        dsh_django_utils.check_auto_timed_calls_for_all_persons(noLogging=True)

    response += dsh_utils.black_break_msg('done.')
    response += dsh_utils.black_break_msg(
        'see the <a href=/scheduled>schedule</a>.')

    response += views.page_footer()

    dsh_agi.report_event(
        'reschedule triggered by web interface.',
        action='RESC')
    
    return HttpResponse(response)



def auto_dial_status(request):
    """
    10/03/19: moved from views.py"""
    
    response = views.page_header('auto-dial status')

    response += spool_wipe_status_message()

    disabled = dsh_db_config.get('auto_dial_disable')
    if disabled:
        response += dsh_utils.black_break_msg(
            'auto-dial is currently <font color=red><b>disabled</b></font>.')
        response += dsh_utils.black_break_msg(
            '<a href="/autodialenable">enable</a>?')
    else:
        response += dsh_utils.black_break_msg(
            'auto-dial is currently <font color=green><b>enabled</b></font>.')
        response += dsh_utils.black_break_msg(
            '<a href="/autodialdisable">disable</a>?')
    
    response += views.page_footer()
    return HttpResponse(response)



def auto_dial_enable(request):
    """10/03/19: moved from view.py"""
    
    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('enable auto-dial')

    dsh_db_config.set('auto_dial_disable', False)
    disabled = dsh_db_config.get('auto_dial_disable')
    
    if disabled:
        message = 'views.auto_dial_enable: unexpected error.'
        response += dsh_utils.red_error_break_msg(message)
        dsh_django_utils.error_event(message, errorLevel='CRT')
        response += views.page_footer()
        return HttpResponse(response)

    response += spool_wipe_status_message()
    dsh_django_utils.auto_schedule_delete_all()
    dsh_django_utils.check_auto_timed_calls_for_all_persons(noLogging=True)

    response += dsh_utils.black_break_msg(
        'now <font color=green><b>enabled</b></font>. ' +\
        'wanna <a href="/autodialdisable">re-disable</a>?')

    response += views.page_footer()

    dsh_agi.report_event('auto-dial enabled.', action='RESC')
    
    return HttpResponse(response)



def auto_dial_disable(request):
    """10/03/19: moved from view.py"""

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('disable auto-dial')

    dsh_db_config.set('auto_dial_disable', True)
    disabled = dsh_db_config.get('auto_dial_disable')
    
    if not disabled:
        message = 'views.auto_dial_disable: unexpected error.'
        response += dsh_utils.red_error_break_msg(message)
        dsh_django_utils.error_event(message, errorLevel='CRT')
        response += views.page_footer()
        return HttpResponse(response)

    response += spool_wipe_status_message()
    dsh_django_utils.auto_schedule_delete_all()

    response += dsh_utils.black_break_msg(
        'now <font color=red><b>disabled</b></font>. ' +\
        'wanna <a href="/autodialenable">re-enable</a>?')
    
    response += views.page_footer()

    dsh_agi.report_event('auto-dial disabled.')

    return HttpResponse(response)



def set_current_dial_sel(personTable, request, action='set'):
    """
    10/03/22.  called by views.set_current_dial_sel() and
    views.clear_current_dial_sel().
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('add people to the current dial set')
    if action == 'clear':
        response = views.page_header('remove people from the current dial set')

    response += dsh_common_selection.process_selected_people_current_dial(
        personTable, action=action)
    response += views.page_footer()
    return HttpResponse(response)



def select_current_dial_set(personTable, request, action='set'):
    """
    10/03/22.  called by views.select_current_dial_set() and
    deselect_current_dial_set().
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('select people in the current dial set')
    if action == 'clear':
        response = views.page_header(
            'de-select people in the current dial set')

    response += dsh_common_selection.select_current_dial_set(
        personTable, action=action)
    response += views.page_footer()
    return HttpResponse(response)



def select_keyed_persons(request, personTable, keyWordTable, dshUid,
                         action='set'):
    """
    10/03/22.
    called by views.select_key_persons() and views.deselect_keyed_persons().
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('select persons with this key word')
    if action == 'clear':
        response = views.page_header(
            'de-select persons with this key word')

    success,msg = dsh_common_selection.select_keyed_persons(
        personTable, keyWordTable, dshUid, action=action)

    response += msg    

    response += views.page_footer()
    return HttpResponse(response)



def add_person_keyword(request, personTable, keyWordTable, dshUid,
                       action='set'):
    """
    10/03/22:
    called by views.add_person_keyword() and views.del_person_keyword().
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('add this key word to selected persons')
    if action == 'clear':
        response = views.page_header(
            'remove this key word from selected persons')

    response += dsh_common_selection.add_person_key_word(
        personTable, keyWordTable, dshUid, action=action)

    response += views.page_footer()
    return HttpResponse(response)
    


def clear_current_dial_set(request, personTable):
    """
    10/03/22:
    called by views.clear_current_dial_set().
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('clear the current dial set')

    response += dsh_common_selection.clear_current_dial_set(personTable)

    response += views.page_footer()
    return HttpResponse(response)



def person_answered(request, dshUid, offset,
                    personTable, eventTable, itemTable):
    """
    10/03/25:
    called by views.person_answered().
    """

    response = views.page_header(
        'messages answered by this person', includeMp3Player=True)

    success,msg = dsh_common_db.person_row(personTable, dshUid)
    response += msg
    if not success:
        response += views.mp3_widget_control()
        response += views.page_footer()
        return HttpResponse(response)

    success,msg = dsh_common_db.answered_message_list(
        personTable, eventTable, itemTable, dshUid, offset)
    response += msg
    if not success:
        response += views.mp3_widget_control()
        response += views.page_footer()
        return HttpResponse(response)

    response += views.mp3_widget_control()
    response += views.page_footer()
    return HttpResponse(response)



def unanswer(request, dshUid, eventTable, itemTable):
    """
    10/03/26:
    called by views.unanswer().
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('unanswer')
    response += dsh_common_db.unanswer(dshUid, eventTable, itemTable)
    response += views.page_footer()
    return HttpResponse(response)



def conversation_history(request, dshUid, itemTable, eventTable):
    """
    10/03/28:
    called by views.conversation_history().
    """

    response = views.page_header('conversation history', includeMp3Player=True)
    response += dsh_common_db.conversation_history(
        dshUid, itemTable, eventTable)
    response += views.mp3_widget_control()
    response += views.page_footer()
    return HttpResponse(response)



def person_heard(request, dshUid, offset, personTable, eventTable, itemTable,
                 noDemographics=False):
    """
    10/04/01.
    called by views.person_heard()
    modeled after person_answered().
    noDemographics=True when called by dvoice side.
    """

    response = views.page_header(
        'messages heard by this person', includeMp3Player=True)

    success,msg = dsh_common_db.person_row(
        personTable, dshUid, noDemographics=noDemographics)
    response += msg
    if not success:
        response += views.mp3_widget_control()
        response += views.page_footer()
        return HttpResponse(response)

    success,msg = dsh_common_db.heard_message_list(
        personTable, eventTable, itemTable, dshUid, offset)
    response += msg
    if not success:
        response += views.mp3_widget_control()
        response += views.page_footer()
        return HttpResponse(response)

    response += views.mp3_widget_control()
    response += views.page_footer()
    return HttpResponse(response)



def unhear(request, dshUid, eventTable, itemTable):
    """
    10/04/01:
    called by views.unhear().
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('unhear')
    response += dsh_common_db.unhear(dshUid, eventTable, itemTable)
    response += views.page_footer()
    return HttpResponse(response)



def questions_answers_not_done(request, kind, offset,
                               itemTable, keyWordTable, eventTable):
    """
    10/04/02:
    called by views.questions_unanswered() and
    views.answers_unheard().
    """

    if kind == 'questions_unanswered':
        pageTitle = 'questions unanswered'
    elif kind == 'answers_unheard':
        pageTitle = 'answers unheard'
    else:
        pageTitle = 'say what'

    response = views.page_header(pageTitle, includeMp3Player=True)

    msg = dsh_common_db.questions_answers_not_done(
        request, kind, offset, itemTable, keyWordTable, eventTable)
    response += msg

    response += views.page_footer()
    return HttpResponse(response)



def send_demo_reply_now(request, itemTable, keyWordTable, eventTable):
    """
    10/04/09: called by views.send_demo_reply_now()
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('send a demo reply now')
    sessionID = dsh_common_db.make_dsh_uid()
    success,msg = dsh_common_agi.demo_reply(
        itemTable, keyWordTable, eventTable, sessionID=sessionID)
    response += msg
    response += views.page_footer()
    return HttpResponse(response)



def send_demo_reply_confirmed(request, dshUid,
                              itemTable, keyWordTable, eventTable):
    """
    10/04/09: called by views.send_demo_reply_confirmed()
    """

    if dsh_django_request.deny_it(request):
        return views.please_log_in()

    response = views.page_header('sending a demo reply now')
    response += dsh_common_db.send_demo_reply_confirmed(
        dshUid, itemTable, keyWordTable, eventTable)
    response += views.page_footer()
    return HttpResponse(response)
