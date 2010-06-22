config = {
    #
    # controls what debug info to print.
    # current max was 45.
    #
    'DEBUG_PRINT_TAG': 45,
    #
    # sqlite database is in here.  used by settings.py.
    # and dsh_django_utils, extract duration: file path.
    #
    #'PHONE_DATA_DJANGO_PATH': '/home/rywang/phone_data/db2/',
    #
    # get the value from dsh_config.py instead, at the end of this file.
    #
    

    #
    # also used by settings.py
    #
    'TEMPLATE_DIR': '/home/rywang/voice/code/django/dv2/templates',


    #
    # common code dir.
    #
    'COMMON_CODE_DIR': ['/home/rywang/voice/code/common/',
                        '/home/rywang/voice/code/django/'],
    
    #
    # get stuff like dsh_utils.py from here.
    # used by db/models.py
    #
    'DSH_VOICE_CODE_DIR': '/home/rywang/voice/code/dj2/',

    #
    # used by dsh_django_utils.py
    # determins the maximum dimension of thumbnail on the list view.
    #
    'MAX_THUMB_DIMENSION': 70,

    #
    # unknown head icon.
    # unknown organization icon.
    # used by dsh_django_utils.thumbnail().
    #
    #'DSH_UNKNOWN_HEAD_URL': '<center><img src=/icons/unknown_head.jpg width=50 height=50 title="" /></center>',
    #'DSH_UNKNOWN_ORG_URL': '<center><img src=/icons/house.jpg width=50 height=50 title="" /></center>',
    'DSH_UNKNOWN_HEAD_URL': '<center><img src=/icons/genericfriendicon60b.png width=60 height=60 title="" /></center>',
    'DSH_UNKNOWN_HEAD_URL_NOT_CENTERED': '<img src=/icons/genericfriendicon60b.png width=60 height=60 title="" />',
    'DSH_UNKNOWN_ORG_URL': '<center><img src=/icons/home.png width=70 height=70 title="" /></center>',

    #
    # permission denied icon.
    # used by dsh_django_request.py
    # which is in turn called by stuff like patched admin_list.py
    #
    #'DSH_PERM_DENIED_URL': '/icons/stop.png',
    #'DSH_PERM_DENIED_URL': '/beroot',

    #
    # play pause icons.
    # used by dsh_django_utils.py.
    # for the mp3 player widgets.
    #
    'PLAY_PAUSE_ICON': '<span style="white-space: nowrap;"><img src=/icons/Play1Normal.png border=0 width=24 height=24>&nbsp;&nbsp;<img src=/icons/PauseDisabled.png border=0 width=24 height=24></span>',

    #
    # star icon.
    #
    'STAR_ICON': '<img src=/icons/star_icons13.gif title=starred border=0 width=13 height=13>',

    #
    # selected icon.
    #
    'SELECTED_ICON': '<img src=/icons/ok.gif title=selected border=0 width=11 height=11>',

    #
    # select box icon.
    #
    'SELECT_BOX_ICON': '/icons/box.gif',

    #
    # select URL.
    #
    'SELECT_URL': '/select/',

    #
    # how many trailing digits of a phone number to hide.
    #
    #'HIDE_PHONE_DIGITS': 4,
    # now sucked in from dsh_config.py at the end of the file.

    #
    # URL for looking up items.
    # used by models.py to point to objects that 'this' is following up to.
    #
    'ITEM_URL': '/admin/db/item/?id=',

    #
    # small green up arrow, used to denote followup_to link.
    # used in models.py
    #
    'FOLLOWUP_TO_ICON': '<img src=/icons/up44.gif title="followup to previous" border=0 width=8 height=8>',
    
    #
    # small blue downright arrow, used to denote broadcast.
    # used in models.py
    #
    'BROADCAST_ICON': '<img src=/icons/br43.gif title="type: broadcast" border=0 width=8 height=8>',

    'BROADCAST_URL': '/admin/db/item/?itype__exact=B',

    #
    # small green up left arrow, used to denote incoming.
    # used in models.py
    #
    'INCOMING_ICON': '<img src=/icons/tl44.gif title="type: incoming" border=0 width=8 height=8>',

    'INCOMING_URL': '/admin/db/item/?itype__exact=I',

    #
    # spaces between icons.
    # used by models.py
    #
    'ICON_SPACES': '&nbsp;&nbsp;',

    #
    # line breaks separating icons from the rest.
    # used by models.py
    #
    'ICON_LINE_BREAKS': '<br><br>',

    #
    # URL for looking up who's following up on this message.
    # used by models.py.
    #
    'FOLLOWING_ITEM_URL': '/admin/db/item/?followup_to=',

    #
    # small blue down arrow, used to denote who's following me.
    # used in models.py
    #
    'FOLLOWED_BY_ICON': '<img src=/icons/down43.gif title="followed by" border=0 width=8 height=8>',

    #
    # small right arrow icon. denotes currently active broadcast message.
    # used in models.py
    #
    'ACTIVE_ICON': '<img src=/icons/right26.gif title="currently active" border=0 width=10 height=10>',
    
    #
    # URL for looking up a person.
    # used by models.Item to point to owner.
    # moved to dsh_config.py
    # patched at the end of this file.
    # no, not necessary to move.
    'PERSON_URL': '/admin/db/person/?id=',

    #
    # URL for looking up an organization.
    # used by models.Item to point to the organization.
    #
    'ORG_URL': '/admin/db/organization/?id=',

    'ORG_PIN_URL': '/admin/db/organization/?dsh_uid=',

    #
    # used by dsh_django_utils.check_spoken_names().
    #
    'ORG_DETAIL_URL': '/admin/db/organization/',

    #
    # URL for looking up key words.
    # used by models.Item to point to query of the same key words.
    #
    'KEY_WORD_URL': '/admin/db/item/?key_words__id__exact=',

    #
    # small dotted arrow icon. denotes having intended audience.
    # used in models.py
    #
    'INTENDED_AUDIENCE_ICON': '<img src=/icons/dotarr.gif title="intended audience of personalized message" border=0 width=12 height=12>',

    #
    # the above rotated 180 degrees. on person page.
    # denotes personalized messages for this person.
    # used in models.py
    #
    'PERSONAL_MESSAGES_ICON': '<img src=/icons/dotarr2.gif title="personalized messages" border=0 width=12 height=12>',

    #
    # url for personal message on people page, goes with the above icon.
    #
    'PERSONAL_MESSAGES_HREF': '/admin/db/item/?intended_audience__id__exact=',

    #
    # reverse link from item to intended audience.
    #
    'INTENDED_AUDIENCE_URL': '/admin/db/person/?message_for_me=',

    #
    # file icon, for uploaded non-mp3 files.
    # used in models.py
    #
    'FILE_ICON': '<img src=/icons/file.gif title="file uploaded" border=0 width=20 height=23>',

    #
    # ffmpeg path
    # used by dsh_django_utils to extract voice file duration.
    #
    'FFMPEG_PATH': '/usr/local/bin/ffmpeg',

    #
    # sox path
    # used by dsh_django_utils to convert wav to sln for outgoing.
    #
    'SOX_PATH': '/usr/bin/sox',

    #
    # regular expression pattern for extracting duration from the
    # ffmpeg output.  used by dsh_django_utils to extract duration.
    #
    'FFMPEG_DURATION_PATTERN': r'Duration: ([0-9][0-9]):([0-9][0-9]):([0-9][0-9])\.',

    #
    # the subdirectory into which we generate database dumps.
    # used by dsh_dump.py
    # concatenated with lookup('PHONE_DATA_DJANGO_PATH')
    #
    'DB_DUMP_DIR': 'dump',

    #
    # tar path
    # used by dsh_dump to collect /media files in a tar ball.
    #
    'TAR_PATH': '/bin/tar',

    #
    # used as header of pages generated by functions in views.py
    #
    'VIEW_HEADER': """
<A HREF="/">
<IMG SRC="/icons/sh500.gif" WIDTH=482 HEIGHT=167 BORDER=0></A>
<BR>\n
""",

    #
    # on the key word list page.
    #
    'KEYWORD_ICON': '<img src=/icons/key1.png title="apply this key word to selected items" border=0 width=12 height=12>',
    'KEYWORD_DEL_ICON': '<img src=/icons/key2.png title="remove this key word from selected items" border=0 width=12 height=12>',
    'KEYED_ITEMS_ICON': '<img src=/icons/key3.png title="items that have this key word" border=0 width=12 height=12>',

    #
    # double arrow icon denoting synchronous call.
    #
    'SYNC_CALLEE_ICON': '<img src=/icons/double_arrow2.gif title="synchronous, callee" border=0 width=12 height=12>',

    # 
    # reply URL, used by models.py
    #
    'REPLY_URL': '/reply/',
    
    #
    # small right-angle blue icon, denoting reply.
    # used in models.py
    #
    'REPLY_ICON': '<img src=/icons/arr02.gif title="reply" border=0 width=11 height=11>',

    #
    # item detail edit URL
    # used by dsh_django_utils.save_red5_mp3_in_django()
    #
    'ITEM_DETAIL_URL': '/admin/db/item/',

    #
    # timed icon.  a clock.
    #
    'TIMED_ICON': '<img src=/icons/clock002.gif title="schedule auto-dialed call" border=0 width=10 height=10>',

    #
    # url for scheduling auto-dialed calls for one callee.
    #

    #
    # used by dsh_django_utils.py
    # for putting out a .call file for automatically scheduled outgoing calls.
    #
    'DOT_CALL_FILE_TEMPLATE': """
Channel: %(channel)s
MaxRetries: 0
RetryTime: 60
WaitTime: 30

Context: %(context)s
Extension: %(extension)s
Priority: 1
CallerID: %(callerid)s

Set: PassedInfo=%(dshuid)s

""",

    #
    # if the dot call file is made as a result of clicking the dial now
    # icon on the Person page, the "PassedInfo" above is followed by
    # this indicator.
    #
    'DIAL_NOW_INDICATOR': '__DIAL_NOW__',

    #
    # an icon for a shared phone.
    #
    'SHARED_PHONE_ICON': '<img src=/icons/handy005.gif title="shared phone" border=0 width=7 height=14>',

    #
    # an icon for a shared phone, displayed for the owner.
    #
    'SHARED_PHONE_OWNER_ICON': '<img src=/icons/handy006.gif title="owner of shared phone" border=0 width=7 height=14>',

    #
    # person icon.  for callee of a scheduled outgoing call.
    #
    'SCHEDULED_USER_ICON': '<img src=/icons/card025.gif title="callee" border=0 width=8 height=10>',

    #
    # look up the callee of a dot call file.
    #
    'SCHEDULED_USER_URL': '/admin/db/person/?dsh_uid=',

    #
    # sound icon.  for active personalized messages of
    # a scheduled outgoing call.
    #
    'SCHEDULED_MSG_ICON': '<img src=/icons/sound1.gif title="personalized messages" border=0 width=10 height=10>',

    #
    # look up the active personalized messages of a dot call file.
    #
    'SCHEDULED_MSG_URL': '/admin/db/item/?active__exact=1&itype__exact=P&intended_audience=',

    #
    # sound2 icon.  for active broadcast messages of
    # a scheduled outgoing call.
    #
    'SCHEDULED_BROADCAST_ICON': '<img src=/icons/sound2.gif title="broadcast messages" border=0 width=10 height=10>',

    #
    # look up the active broadcast messages of a dot call file.
    #
    'SCHEDULED_BROADCAST_URL': '/admin/db/item/?active__exact=1&itype__exact=B',

    #
    # not ok icon.  used to denote error on the .call list page.
    #
    'NOK_ICON': '<img src=/icons/nok.gif title="error" border=0 width=10 height=11>',

    #
    # blue cross icon, for deleting a dot call file.
    #
    'CROSS_ICON': '<img src=/icons/cross2.gif title="delete this schedule" border=0 width=11 height=11>',


    #
    # person item lookup URL.
    #
    'PERSON_ITEM_URL': '/admin/db/item/?owner__id__exact=',
    
    #
    # person item icon.
    #
    'PERSON_ITEM_ICON': '<img src=/icons/chat6.gif title="messages by this person" border=0 width=11 height=10>',

    #
    # org item lookup URL.
    #
    'ORG_ITEM_URL': '/admin/db/item/?owner__organization__id__exact=',

    #
    # org item icon.
    #
    'ORG_ITEM_ICON': '<img src=/icons/chat6.gif title="messages from this organization" border=0 width=11 height=10>',

    #
    # org people lookup URL.
    #
    'ORG_PERSON_URL': '/admin/db/person/?organization__id__exact=',

    #
    # org people icon.
    #
    'ORG_PERSON_ICON': '<img src=/icons/card025.gif title="people from this organization" border=0 width=8 height=10>',

    #
    # person detail URL:
    #
    'PERSON_DETAIL_URL': '/admin/db/person/',

    #
    # item: synchronous callee lookup URL.
    #
    'SYNC_CALLEE_URL': '/admin/db/item/?i05__id__exact=',

    #
    # for emailing selection.
    # called by models.Item.email_text()
    #
    'ITEM_DSH_UID_URL': '/admin/db/item/?dsh_uid=',
    'DSH_URL_PREFIX': 'http://dsh.cs.washington.edu:8080',

    'PIN_DSH_UID_ICON': '<img src=/icons/pin007.gif title="pin this object with dsh_uid" border=0 width=9 height=9>',

    #
    # auto dial disabled icon
    #
    'AUTO_DIAL_DISABLED_ICON': '<img src=/icons/sound050.gif title="auto dialing disabled" border=0 width=10 height=12>',

    #
    # triple pronged icon denoting peer-shared items.
    #
    'PEER_SHARED_ICON': '<img src=/icons/triple.gif title="peer-shared" border=0 width=11 height=11>',

    'PEER_SHARED_URL': '/admin/db/item/?peer_shared__exact=1',

    #
    # used by dsh_django_utils.dsh_uid_url().
    #
    'ORG_DSH_UID_URL': '/admin/db/item/?dsh_uid=',
    'EVENT_DSH_UID_URL': '/admin/db/event/?dsh_uid=',
    'KEYWORD_DSH_UID_URL': '/admin/db/keyword/?dsh_uid=',

    #
    # how long does the recording have to be in order to count as
    # a recorded item. to be overwritten by the same variable from
    # dsh_config.py
    #
    'RECORDED_THRESH': 15,

    #
    # icon on person page for dialing now.
    #
    'DIAL_NOW_ICON': '<img src=/icons/phone006.gif title="dial this person now" border=0 width=9 height=8>',
    'DIAL_NOW_ICON_STD': '<img src=/icons/phone017.gif title="STD: dial this person now" border=0 width=12 height=8>',

    #
    # used by dsh_django_utils.session_link()
    #
    'SESSION_ID_SEARCH_URL': '/admin/db/event/?session',
    'SESSION_ID_ICON': '<img src=/icons/file3.gif title="session that created this" border=0 width=10 height=10>',

    #
    # used by dsh_django_utils.people_heard_link()
    #
    'HEARD_PEOPLE_URL': '/heard/',
    'HEARD_PEOPLE_ICON': '<img src=/icons/card028.gif title="people who have heard this message" border=0 width=8 height=10>',
    'HEARD_PARTIAL_PEOPLE_ICON': '<img src=/icons/card024.gif title="people who have only partially heard this message" border=0 width=8 height=10>',
}



def lookup(what):
    return config[what]



import sys,dsh_django_utils2
dsh_django_utils2.append_to_sys_path(lookup('DSH_VOICE_CODE_DIR'))
import dsh_config



config['PHONE_DATA_DJANGO_PATH'] = dsh_config.lookup('PHONE_DATA_DJANGO_PATH')
config['HIDE_PHONE_DIGITS'] = dsh_config.lookup('HIDE_PHONE_DIGITS')
#config['PERSON_URL'] = dsh_config.lookup('PERSON_URL')
config['RECORDED_THRESH'] = dsh_config.lookup('RECORDED_THRESH')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = dsh_config.lookup(
    'DJANGO_SETTINGS_MODULE')


import datetime
config['YEAR'] = datetime.datetime.now().strftime('%Y')


#
# used as the footer of pages generated by views.py
#
config['VIEW_FOOTER_NOT_USED'] = """
<FONT SIZE=2 FACE=ARIAL>
&#169 2005-%s &nbsp;&nbsp;
<A HREF="http://dsh.cs.washington.edu">The Digital StudyHall</a>
</FONT>
""" % (config['YEAR'],)


#config['VIEW_FOOTER'] = """
#<BR><BR><TABLE BORDER=0 WIDTH=400><TR><TD><CENTER><HR><FONT SIZE=1 FACE=ARIAL>&#169 2005-%s &nbsp;&nbsp;<A HREF=http://dsh.cs.washington.edu>The Digital StudyHall</A></FONT><HR></CENTER></TD></TR></TABLE>"""  % (config['YEAR'],)



config['VIEW_FOOTER'] = """
<!-- RYW begin -->
    <div id="footer"> 
<font size=1>&#169 2005-%s &nbsp;
<a href="http://dsh.cs.washington.edu">The Digital StudyHall</a></font>
</div>

<img src="http://dsh.cs.washington.edu:8000/x/asterisk.xbm"
width=0 height=0 border=0>
<!-- RYW end -->
"""  % (config['YEAR'],)
