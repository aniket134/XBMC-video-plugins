from django.template.loader import get_template
from django.template import Context
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
import datetime
import dv2.db.models
import dsh_dump_models,dsh_dump,dsh_selection,dsh_stats
import dsh_django_config,dsh_django_request,dsh_django_utils,dsh_db_config
import dsh_django_utils2
dsh_django_utils2.append_to_sys_path(
    dsh_django_config.lookup('DSH_VOICE_CODE_DIR'))
import sys,os
import dsh_utils,dsh_config,dsh_agi
import dsh_common_views



def page_header(title, includeMp3Player=False):
    response = '<head>\n'
    response += '<title>%s | Lokarpit voice</title>\n' % (title,)
    response += """
<script type="text/javascript" src="/media/js2/dsh_utils.js"></script>
<link rel="stylesheet" type="text/css" href="/media/css/base.css" />    
<link rel="stylesheet" type="text/css" href="/media/css/dashboard.css" />
<meta name="robots" content="NONE,NOARCHIVE" />
"""

    if includeMp3Player:
        #
        # copied from templates/admin/base.html
        #
        response += """
<!--RYW begin -->

<link rel="stylesheet" type="text/css" 
href="/media/sm2/demo/page-player/css/page-player.css" />

<script type="text/javascript" 
src="/media/sm2/script/soundmanager2.js"></script>

<script type="text/javascript" 
src="/media/sm2/demo/page-player/script/page-player.js"></script>

<script type="text/javascript">
// directory where SM2 .SWFs live
soundManager.url = '/media/sm2/swf/soundmanager2.swf'; 
soundManager.debugMode = false;
</script>

<!-- RYW end -->
"""

    response += """</head>
<body class="dashboard">
<div id="container">
  <div id="header">
    <div id="branding">
        <h1 id="site-name">Lokarpit voice</h1>
    </div>
    <div id="user-tools"><a href="/admin/logout/">Log out</a></div>
  </div> <!-- end header -->

<div class="breadcrumbs">
     <a href="/admin">Home</a> &rsaquo;
     <a href="/admin/db">Db</a> &rsaquo; 
     <a href="/admin/db/item">Item</a>
</div>

<!-- Content -->
<div id="content" class="colM">

    """
    #response += dsh_django_config.lookup('VIEW_HEADER')
    response += '<H1>%s</H1>\n<P><BR>\n' % (title,)
    return response



def page_footer():

    response = """
<br class="clear" />
</div> <!-- END content -->
<div id="footer"></div>
</div> <!-- END container -->
"""
    response += dsh_django_config.lookup('VIEW_FOOTER')
    response += """
</body>
"""    
    return response



def please_log_in():
    response = page_header('permission denied')
    response += '\n'
    response += """please <a href=/admin/logout/>log in</a>
as the super-user (root)."""
    response += page_footer()
    return HttpResponse(response)



def be_root(request):
    return please_log_in()



def red5_frame_page(request, dict):
    """frames the record and play pages from red5.
    called by red5_record() and red5_play().
    the input dict contains keys for:
    'title', 'url', 'width', 'height'.
    """
    
    #if dsh_django_request.deny_it(request):
    #    return please_log_in()

    response = page_header(dict['title'])
    response += '\n'

    hostPort = dsh_django_utils.get_host_port(request)
    if hostPort == None:
        message = 'unable to determine host name.'
        dsh_django_utils.error_event(message, errorLevel='CRT')
        response += dsh_utils.red_error_break_msg(message)
        response += page_footer()
        return HttpResponse(response)    

    dict['hostname'] = hostPort[0]
    
    response += """
<table cellpadding=0 cellspacing=0 height=%(height)s width=%(width)s border=0>
<tr height="1%%">
<td style="top:0;width:100%%">
<iframe scrolling=auto id=rf
src="http://%(hostname)s:5080/%(url)s"
frameborder=0 allowtransparency=true style="width:100%%;height:100%%">
</iframe>
</td></tr></table>
""" % dict

    response += page_footer()
    return HttpResponse(response)




def red5_record(request):
    """from urls.py.  frames the red5 publisher demo."""
    
    dict = {
        'title': 'record a message in your browser',
        'url': 'demos/publisher.html',
        'width': '940',
        'height': '700',
    }

    return red5_frame_page(request, dict)
    


def red5_play(request):
    """from urls.py.  frames the red5 oflaDemo page."""

    dict = {
        'title': 'play messages in the scratch space',
        'url': 'demos/ofla_demo.html',
        'width': '750',
        'height': '745',
    }

    return red5_frame_page(request, dict)



def lookup_phone_number(request, personDshUid):
    if dsh_django_request.deny_it(request):
        return please_log_in()
    
    response = page_header('lookup a phone number')
    response += '\n'
    
    persons = dv2.db.models.Person.objects.filter(dsh_uid=personDshUid)
    if not persons or len(persons) > 1:
        message = 'views.lookup_phone_number: bad DshUid: ' + personDshUid
        response += dsh_utils.red_error_break_msg(message)
        dsh_django_utils.error_event(message, errorLevel='CRT')
        response += page_footer()
        return HttpResponse(response)

    person = persons[0]

    phoneNumber = person.phone_number
    message = '<BR><B><FONT SIZE=3>Phone number: %s</FONT></B>' % \
              (phoneNumber,)
    response += dsh_utils.black_break_msg(message)
    response += '<BR>'
    response += dsh_utils.black_break_msg('People who share this number are:')
    response += '<BR>'

    response += """
<table cellpadding=0 cellspacing=0 border=0 height=600 width=1000>
<tr height="1%%">
<td style="top:0;width:100%%">
<iframe scrolling=auto id=rf
src="http:/admin/db/person/?phone_number=%s"
frameborder=0 allowtransparency=true style="width:100%%;height:100%%">
</iframe>
</td></tr></table>
""" % (phoneNumber,)

    response += page_footer()
    return HttpResponse(response)
        
    

def entrance(request):
    """ coming here when people hit /.
    not really necessary to do the redirection here.
    could have just re-directed in urls.py.
    but put in here just in case we want our own root page in the future."""
    
    response = page_header('Lokarpit voice')

    response += """
<script language="JavaScript" type="text/javascript">
<!--Comment tag so old browsers wont see code.
    window.location = "/admin/";
// end comment for old browsers -->
</script>"""
    
    response += page_footer()
    return HttpResponse(response)



def reply_submit(request):
    """processes a reply form submission."""

    if dsh_django_request.deny_it(request):
        return please_log_in()
    
    response = page_header('process reply')

    if not 'from_red5' in request.POST or \
       not request.POST['from_red5'] or \
       not 'dsh_uid' in request.POST or \
       not request.POST['dsh_uid']:
        response += dsh_utils.red_error_break_msg('invalid submission.')
        response += page_footer()
        return HttpResponse(response)    

    dshUid = request.POST['dsh_uid']
    name = request.POST['from_red5']

    success,msgs,mp3Path = dsh_django_utils.convert_red5_flv_to_mp3(name)
    response += msgs

    if not success:
        response += page_footer()
        dsh_django_utils.cleanup_red5_conversion(success, name)
        return HttpResponse(response)

    success,msgs = dsh_django_utils.save_red5_mp3_in_django(
        mp3Path, originalItemDshUid=dshUid)
    response += msgs
    dsh_django_utils.cleanup_red5_conversion(success, name)

    response += page_footer()
    return HttpResponse(response)    
    


def save_submit(request):
    """processes a red5 save.  very much like reply_submit().
    only simpler."""

    if dsh_django_request.deny_it(request):
        return please_log_in()
    
    response = page_header('process save')

    if not 'from_red5' in request.POST or \
       not request.POST['from_red5']:
        response += dsh_utils.red_error_break_msg('invalid submission.')
        response += page_footer()
        return HttpResponse(response)    

    name = request.POST['from_red5']

    success,msgs,mp3Path = dsh_django_utils.convert_red5_flv_to_mp3(name)
    response += msgs

    if not success:
        response += page_footer()
        dsh_django_utils.cleanup_red5_conversion(success, name)
        return HttpResponse(response)

    success,msgs = dsh_django_utils.save_red5_mp3_in_django(mp3Path)
    response += msgs
    dsh_django_utils.cleanup_red5_conversion(success, name)

    response += page_footer()
    return HttpResponse(response)    
    


def reply(request, dshUid):
    """displays a form for replying.
    fills the form with a default red5 message name."""

    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('reply to a message')

    newest_stream = dsh_django_utils.newest_red5_stream()
    if newest_stream == None:
        newest_stream = ''
    newest_stream = newest_stream[:-4]
    
    response += """
<FORM ACTION="/replysubmit/" METHOD="post">
<BR>
red5 message just recorded:<br>
<INPUT TYPE="HIDDEN" NAME="dsh_uid" VALUE="%(dsh_uid)s">
<INPUT TYPE="TEXT" NAME="from_red5" VALUE="%(newest_stream)s" SIZE=40><br>

<br>
<INPUT TYPE="submit" VALUE="submit">
</FORM>
""" % {'dsh_uid': dshUid, 'newest_stream': newest_stream}
    
    response += page_footer()
    return HttpResponse(response)    



def reply_upload(request, dshUid):
    """
    10/03/06:
    modeled after ^reply/dsh_uid
    displays a page for confirming replying.
    """
    return dsh_common_views.reply_upload(request, dshUid)



def reply_upload_submit(request, dshUid):
    """
    10/03/06:
    modeled after ^replysubmit/dsh_uid
    a temporary reply is put in.
    """
    return dsh_common_views.reply_upload_submit(request, dshUid)



def red5_save(request):
    """displays a form for saving
    a red5 message that's just saved.
    very much like reply(), only simpler.
    minus the dsh_uid of the original message."""

    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('save a recorded message in the database')

    newest_stream = dsh_django_utils.newest_red5_stream()
    if newest_stream == None:
        newest_stream = ''
    newest_stream = newest_stream[:-4]
    
    response += """
<FORM ACTION="/savesubmit/" METHOD="post">
<BR>
red5 message just recorded:<br>
<INPUT TYPE="TEXT" NAME="from_red5" VALUE="%(newest_stream)s" SIZE=40><br>

<br>
<INPUT TYPE="submit" VALUE="submit">
</FORM>
""" % {'newest_stream': newest_stream}
    
    response += page_footer()
    return HttpResponse(response)    



def red5_clear(request):
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('clear files in red5 scratch space')

    keepList = ['9.flv', '9.flv.meta',
                'toystory3.flv', 'toystory3.flv.meta',
                'test_randy.flv', 'test_randy.flv.meta', ]

    red5Dir = dsh_config.lookup('RED5_STREAMS_DIR')
    red5TmpDir = os.path.join(red5Dir, 'tmp')

    dsh_utils.empty_dir(red5Dir, keepList)
    dsh_utils.empty_dir(red5TmpDir)

    response += dsh_utils.black_break_msg('Cleared.')
    response += page_footer()

    return HttpResponse(response)



def schedule_outgoing_calls(request):
    if dsh_django_request.deny_it(request):
        return please_log_in()
    response = page_header('schedule auto-dialed outgoing calls')
    #response += dsh_utils.black_break_msg('generating...')
    dsh_django_utils.check_auto_timed_calls_for_all_persons()
    response += dsh_utils.black_break_msg('done.')
    response += dsh_utils.black_break_msg(
        'see the <a href=/scheduled>schedule</a>.')
    response += page_footer()
    return HttpResponse(response)



def schedule_list(request):
    if dsh_django_request.deny_it(request):
        return please_log_in()
    response = page_header('schedule of auto-dialed outgoing calls')
    output = dsh_django_utils.auto_schedule_list()
    response += output
    response += page_footer()
    return HttpResponse(response)



def schedule_del(request, fileName):
    if dsh_django_request.deny_it(request):
        return please_log_in()
    response = page_header('delete an auto-dialed outgoing call')
    output = dsh_django_utils.auto_schedule_delete(fileName)
    response += output
    response += page_footer()
    return HttpResponse(response)



def schedule_del_all(request):
    if dsh_django_request.deny_it(request):
        return please_log_in()
    response = page_header('delete all auto-dialed outgoing calls')
    output = dsh_django_utils.auto_schedule_delete_all(force=True)
    response += output
    response += page_footer()
    return HttpResponse(response)



def reschedule(request):
    """a combination of delete all and active."""

    return dsh_common_views.reschedule(request, dv2.db.models.Person)



def scheduled_slots(request):
    """slots taken by people."""
    if dsh_django_request.deny_it(request):
        return please_log_in()
    response = page_header('all scheduled slots')
    response += dsh_django_utils.scheduled_slots()
    response += page_footer()
    return HttpResponse(response)



def deselect_all(request):
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('deselecting objects')
    response += dsh_dump.deselect_all()
    response += page_footer()

    return HttpResponse(response)



def show_selected(request):
    response = page_header('selected objects')
    response += """
<UL>
<LI><a href="/admin/db/item/?u17__exact=1">items</a> (%(item)s)
<LI><a href="/admin/db/person/?u17__exact=1">persons</a> (%(person)s)
<LI><a href="/admin/db/organization/?u17__exact=1">organizations</a>
(%(organization)s)
<LI><a href="/admin/db/keyword/?u17__exact=1">key words</a> (%(keyword)s)
<LI><a href="/admin/db/event/?u17__exact=1">events</a> (%(event)s)
</UL>""" % dsh_dump.count_all_selected()
    response += page_footer()
    return HttpResponse(response)
    


def dump_all(request):
    return dump(request, dumpAll=True)



def dump_all_persons(request):
    return dump(request, dumpPersons=True)



def dump(request, dumpAll=False, dumpPersons=False):
    """dumps either all or selected objects in to a big python file
    so that things can be re-loaded.
    also puts relevant /media files in a .tar file."""
    
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('dump report')
    
    dumpWhere = dsh_dump.init_dump()
    if not dumpWhere:
        return HttpResponse('failed to open dump file.')

    dumpFile,dumpPath,tarPath = dumpWhere
    response += 'dumping to:<br>' + dumpPath + '<br>\n'

    success,errorMsg = dsh_dump.dump_selected(dumpFile, dumpPath, tarPath,
                                              dumpAll=dumpAll,
                                              dumpPersons=dumpPersons)
    dumpFile.close()

    if errorMsg:
        response += '<br>' + errorMsg + '<br>\n'

    if success:
        response += '<font color=green><b>dump successful.</b></font>\n'
    else:
        response += '<font color=red><b>dump failed.</b></font>\n'

    response += page_footer()
    return HttpResponse(response)
    


def select_one(request, whatKind, dshUid):
    """this is called by the javascript responding to clicking on
    a selection box.
    the javascript expects to see the string of either
    'True' or 'False'
    if 'True', the javascript changes the icon to a checkmark.
    'whatKind' is like 'item' or 'person'.
    """
    #
    # I'm going to allow non-root to select.
    # they can even show selections.
    # but they can't dump.
    #
    #if dsh_django_request.deny_it(request):
    #    return HttpResponse('False')

    dsh_django_utils.debug_event(
        'views.select_one: entered: ' + whatKind + ' ' + dshUid, 12)

    if not dsh_dump.allDbTables.has_key(whatKind):
        dsh_django_utils.error_event(
            'views.select_one: wrong kind: ' + repr(whatKind),
            errorLevel='CRT')
        return HttpResponse('False')
    
    dbTable = dsh_dump.allDbTables[whatKind][0]
    
    if dsh_dump.select_box(dbTable, dshUid):
        return HttpResponse('True')
    return HttpResponse('False')



def keyword_del(request, dshUid):
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('remove key word from selected items')
    response += dsh_selection.keyword_add_del(dshUid, action='del')
    response += page_footer()
    return HttpResponse(response)



def keyword_add(request, dshUid):
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('add key word to selected items')
    response += dsh_selection.keyword_add_del(dshUid, action='add')
    response += page_footer()
    return HttpResponse(response)



def email_confirm(request):
    """displays a simple form for confirming emailing the selection.
    modeled after red5_save()."""

    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('email the selected items?')

    response += """
<FORM ACTION="/email/" METHOD="post">

email addresses: <INPUT TYPE="TEXT" NAME="email_addresses" SIZE="80"
value="%s, "><br><br>

comments:<BR>
<TEXTAREA NAME="comments" ROWS=5 COLS=70></TEXTAREA><br><br>

attach voice? <INPUT TYPE=checkbox NAME=attach_voice>
&nbsp;&nbsp;&nbsp;
include dsh.cs URLs? <INPUT TYPE=checkbox NAME=dsh_url><br><br>

<!--
include pnet1-LAN URLs? <INPUT TYPE=checkbox NAME=lan_url>
&nbsp;&nbsp;&nbsp;
include pnet1-VPN URLs? <INPUT TYPE=checkbox NAME=vpn_url>
<br><br>
-->

<INPUT TYPE="submit" VALUE="send">
</FORM>
""" % (dsh_config.lookup('GMAIL_DEFAULT_RECIPIENT'),)
    
    response += page_footer()
    return HttpResponse(response)    



def email_selection(request):
    """emails the selected items."""

    if dsh_django_request.deny_it(request):
        return please_log_in()
    
    response = page_header('email the selected items')

    if not 'email_addresses' in request.POST or \
       not request.POST['email_addresses']:
        response += dsh_utils.red_error_break_msg('no email address given.')
        response += page_footer()
        return HttpResponse(response)    

    response += dsh_utils.black_break_msg_debug(
        'emails: ' + repr(request.POST['email_addresses']), 117)

    if ('comments' in request.POST) and request.POST['comments']:
        comments = request.POST['comments']
    else:
        comments = ''        

    attachVoice = False
    if 'attach_voice' in request.POST:
        response += dsh_utils.black_break_msg_debug(
            'attach: ' + repr(request.POST['attach_voice']), 117)
        if request.POST['attach_voice']:
            attachVoice = True
    else:
        response += dsh_utils.black_break_msg_debug('attach: not found.', 117)


    fields = {'dsh_url': False, 'lan_url': False, 'vpn_url': False}
    for varStr,varVal in fields.iteritems():
        if varStr in request.POST and request.POST[varStr]:
            fields[varStr] = True
    

    returnMsg,emailAddrs = dsh_django_utils.check_valid_email_addresses(
        request.POST['email_addresses'])
    if not emailAddrs:
        response += returnMsg
        response += page_footer()
        return HttpResponse(response)
    else:
        response += dsh_utils.black_break_msg_debug(
            'email addresses are: ' + repr(emailAddrs), 117)

    response += dsh_selection.email_selections(emailAddrs, attachVoice,
                                               comments, urlFields=fields)

    response += page_footer()
    return HttpResponse(response)    



def unknown_list(request):
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('list of unknown people')
    response += dsh_django_utils.unknown_list()
    response += page_footer()
    return HttpResponse(response)


    
def phone_number_list(request):
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('phone number list')
    response += dsh_django_utils.phone_number_list()
    response += page_footer()
    return HttpResponse(response)


    
def star_selection(request):
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('add stars to selected items')
    response += dsh_selection.star()
    response += page_footer()
    return HttpResponse(response)


    
def destar_selection(request):
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('remove stars from selected items')
    response += dsh_selection.star(action='del')
    response += page_footer()
    return HttpResponse(response)



def schedule_one_callee(request, personDshUid):
    """triggerred by clicking the little clock icon on the Person page.
    for scheduling auto-dialed call for one person."""
    
    if dsh_django_request.deny_it(request):
        return please_log_in()
    
    response = page_header('schedule auto-dialed call for one callee')
    response += '\n'

    disabled = dsh_db_config.get('auto_dial_disable')
    if disabled:
        response += dsh_utils.black_break_msg(
            'auto-dial is currently <font color=red><b>disabled</b></font>.')
        #response += page_footer()
        #return HttpResponse(response)
        #
        # 10/03/18:
        # I'm going to schedule a call anyways.
        # for sending out doctor replies even though global auto-dial
        # has been turned off.
        #
        response += dsh_utils.black_break_msg(
            "but we are scheduling a call anyhow.")
    
    persons = dv2.db.models.Person.objects.filter(dsh_uid=personDshUid)
    if not persons or len(persons) > 1:
        message = 'views.schedule_one_callee: bad DshUid: ' + personDshUid
        response += dsh_utils.red_error_break_msg(message)
        dsh_django_utils.error_event(message, errorLevel='CRT')
        response += page_footer()
        return HttpResponse(response)

    person = persons[0]
    
    scheduled,respStr = dsh_django_utils.check_auto_timed_calls_for_person(
        person)
    response += dsh_utils.black_break_msg(respStr)
    if scheduled:
        response += dsh_utils.black_break_msg('scheduled.')
    else:
        response += dsh_utils.black_break_msg('not scheduled.')
    
    response += dsh_utils.black_break_msg('done.')
    response += dsh_utils.black_break_msg(
        'see the <a href=/scheduled>schedule</a>.')

    response += page_footer()
    return HttpResponse(response)

        
    
def tutorials(request):
    return dsh_common_views.tutorials(request)



def auto_dial_status(request):
    return dsh_common_views.auto_dial_status(request)



def auto_dial_enable(request):
    return dsh_common_views.auto_dial_enable(request)
    


def auto_dial_disable(request):
    return dsh_common_views.auto_dial_disable(request)



def mp3_widget_control():
    """copied from templates/admin/base.html.
    at the end of the page. for displaying mp3 player widget.
    """
    return """
<!-- RYW begin -->

 <div id="control-template">
  <!-- control markup inserted dynamically after each link -->
  <div class="controls">
   <div class="statusbar">
    <div class="loading"></div>
     <div class="position"></div>
   </div>
  </div>
  <div class="timing">
   <div id="sm2_timing" class="timing-data">
    <span class="sm2_position">%s1</span> / <span class="sm2_total">%s2</span></div>
  </div>
  <div class="peak">
   <div class="peak-box"><span class="l"></span><span class="r"></span>
   </div>
  </div>
 </div>

 <div id="spectrum-container" class="spectrum-container">
  <div class="spectrum-box">
   <div class="spectrum"></div>
  </div>
 </div> 

<!-- RYW end -->
"""    



def check_spoken_names(request):
    """triggered by urls.py."""
    
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('check spoken names', includeMp3Player=True)
    response += dsh_django_utils.check_spoken_names(kind = 'peer_shared')
    response += '<BR>'
    response += dsh_django_utils.check_spoken_names(kind = 'personalized')
    response += mp3_widget_control()
    response += page_footer()
    return HttpResponse(response)
    


def stats(request, sortBy=None):
    """triggered by urls.py"""
    response = page_header('stats')

    if not sortBy:
        sortBy = dsh_config.lookup('STATS_SORT_BY')
        
    response += dsh_stats.stats(sortBy=sortBy)
    response += page_footer()
    
    return HttpResponse(response)

    

def select_starred(request):
    """triggered by urls.py."""
    
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('select starred items')
    response += dsh_selection.select_starred()
    response += page_footer()
    return HttpResponse(response)

    

def dial_now(request, dshUid):
    """triggered by urls.py."""
    
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('dial a person now?')
    resStr,callee = dsh_django_utils.dial_now(dshUid)
    response += resStr
    response += page_footer()
    return HttpResponse(response)



def dial_now_confirm(request, dshUid):
    """triggered by urls.py."""
    
    if dsh_django_request.deny_it(request):
        return please_log_in()

    response = page_header('dialing now...')
    response += dsh_django_utils.dial_now_confirm(dshUid)
    response += page_footer()
    return HttpResponse(response)



def heard(request, dshUid):
    """triggered by urls.py."""
    
    response = page_header('people who have heard this message',
                           includeMp3Player=True)
    response += dsh_django_utils.people_heard_list(dshUid)
    response += '\n<br>\n'
    response += dsh_django_utils.people_heard_list(dshUid,
                                                   printUnheard=True)
    response += mp3_widget_control()
    response += page_footer()
    return HttpResponse(response)



def selection_deactivate(request):
    return dsh_common_views.selection_deactivate(request)

def selection_activate(request):
    return dsh_common_views.selection_activate(request)

def selection_share(request):
    return dsh_common_views.selection_share(request)

def selection_unshare(request):
    return dsh_common_views.selection_unshare(request)



def demographics(request, dshUid):
    """triggered by urls.py"""
    return dsh_common_views.demographics(
        request, dshUid, dv2.db.models.Person)



def keyword_select(request, dshUid):
    """triggered by urls.py.
    add the keyworded items to the current selection."""
    return dsh_common_views.keyword_select(
        request, dshUid, dv2.db.models.KeyWord, dv2.db.models.Item)



def keyword_deselect(request, dshUid):
    """triggered by urls.py.
    remove the keyworded items from the current selection."""
    return dsh_common_views.keyword_deselect(
        request, dshUid, dv2.db.models.KeyWord, dv2.db.models.Item)



def set_current_dial_sel(request):
    """
    10/03/22:
    triggered by urls.py
    add the selected people to the current dial set.
    """
    return dsh_common_views.set_current_dial_sel(
        dv2.db.models.Person, request)



def clear_current_dial_sel(request):
    """
    10/03/22:
    triggered by urls.py
    clear the selected people from the current dial set.
    """
    return dsh_common_views.set_current_dial_sel(
        dv2.db.models.Person, request, action='clear')



def select_current_dial_set(request):
    """
    10/03/22:
    triggered by urls.py
    select the people in the current dial set.
    """

    return dsh_common_views.select_current_dial_set(
        dv2.db.models.Person, request)



def deselect_current_dial_set(request):
    """
    10/03/22:
    triggered by urls.py
    de-select the people in the current dial set.
    """

    return dsh_common_views.select_current_dial_set(
        dv2.db.models.Person, request, action='clear')



def select_keyed_persons(request, dshUid):
    """
    10/03/22:
    select keyed persons.
    """
    return dsh_common_views.select_keyed_persons(
        request, dv2.db.models.Person, dv2.db.models.KeyWord, dshUid)



def deselect_keyed_persons(request, dshUid):
    """
    10/03/22:
    deselect keyed persons.
    """
    return dsh_common_views.select_keyed_persons(
        request, dv2.db.models.Person, dv2.db.models.KeyWord, dshUid,
        action='clear')



def add_person_keyword(request, dshUid):
    """
    10/03/22:
    add keyword to selected persons.
    """
    return dsh_common_views.add_person_keyword(
        request, dv2.db.models.Person, dv2.db.models.KeyWord, dshUid)



def del_person_keyword(request, dshUid):
    """
    10/03/22:
    add keyword to selected persons.
    """
    return dsh_common_views.add_person_keyword(
        request, dv2.db.models.Person, dv2.db.models.KeyWord, dshUid,
        action='clear')



def clear_current_dial_set(request):
    """
    10/03/22.
    """
    return dsh_common_views.clear_current_dial_set(
        request, dv2.db.models.Person)



def person_answered(request, dshUid, offset):
    """
    10/03/25:
    messages answered by this person.
    """
    return dsh_common_views.person_answered(
        request, dshUid, offset,
        dv2.db.models.Person,
        dv2.db.models.Event,
        dv2.db.models.Item)



def unanswer(request, dshUid):
    """
    10/03/26.
    """
    return dsh_common_views.unanswer(
        request, dshUid, dv2.db.models.Event, dv2.db.models.Item)



def conversation_history(request, dshUid):
    """
    10/03/28:
    displays the entire history of a conversation.
    """
    return dsh_common_views.conversation_history(
        request, dshUid, dv2.db.models.Item, dv2.db.models.Event)



def person_heard(request, dshUid, offset):
    """
    10/04/01.
    """
    return dsh_common_views.person_heard(
        request, dshUid, offset,
        dv2.db.models.Person,
        dv2.db.models.Event,
        dv2.db.models.Item)



def unhear(request, dshUid):
    """
    10/04/01.
    """
    return dsh_common_views.unhear(
        request, dshUid, dv2.db.models.Event, dv2.db.models.Item)



def questions_unanswered(request, offset):
    """
    10/04/02:
    questions un-answered.
    """
    return dsh_common_views.questions_answers_not_done(
        request, 'questions_unanswered', offset,
        dv2.db.models.Item,
        dv2.db.models.KeyWord,
        dv2.db.models.Event)



def answers_unheard(request, offset):
    """
    10/04/02:
    answers un-heard.
    """
    return dsh_common_views.questions_answers_not_done(
        request, 'answers_unheard', offset,
        dv2.db.models.Item,
        dv2.db.models.KeyWord,
        dv2.db.models.Event)



def send_demo_reply_now(request):
    """
    10/04/09: send a demo reply right now.
    """
    return dsh_common_views.send_demo_reply_now(
        request,
        dv2.db.models.Item,
        dv2.db.models.KeyWord,
        dv2.db.models.Event)



def send_demo_reply_confirmed(request, dshUid):
    """
    10/04/09.
    """
    return dsh_common_views.send_demo_reply_confirmed(
        request, dshUid,
        dv2.db.models.Item,
        dv2.db.models.KeyWord,
        dv2.db.models.Event)




#
# the stuff below was left by Raghuvansh.  not used.
#
def hello(request):
    now = datetime.datetime.now()
    n2 = datetime.datetime.utcnow()
    nowStr = now.strftime('%y%m%d_%H%M%S')
    n2str = n2.strftime('%y%m%d_%H%M%S')
    return HttpResponse("Hello World! " + nowStr + ' ' + n2str)

def current_datetime(request):
    now = datetime.datetime.now()
    #t = get_template('current_datetime.html')
    #html = t.render(Context({'current_date': now}))
    #return HttpResponse(html)
    return render_to_response('current_datetime.html', {'current_date': now})
	
#def current_datetime(request):
    #now = datetime.datetime.now()
    #html = "<html><body>It is now %s.</body></html>" % now
    #return HttpResponse(html)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    #assert True
    html = "<html><body>In %s hour (s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

