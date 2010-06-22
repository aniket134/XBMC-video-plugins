#
# the "common" solution to dsh_config.py
#


config = {
    #
    # permission denied icon.
    # used by dsh_django_request.py
    # which is in turn called by stuff like patched admin_list.py
    #
    #'DSH_PERM_DENIED_URL': '/icons/stop.png',
    'DSH_PERM_DENIED_URL': '/beroot',

    #
    # used by dsh_common_db.models_keyword_org_key_icon()
    # modeled after dsh_django_config: 'KEY_WORD_URL'
    # in the key word table, display a house icon to link orgs.
    #
    'KEYED_ORGS_URL': '/admin/db/organization/?org_key_word__id__exact=',
    'KEYED_ORGS_ICON': '<img src=/icons/home047.gif title="organizations that are keyed by this group keyword" border=0 width=10 height=10>',

    #
    # used by the icons displayed on the keyword page.
    # to prevent line-wrapping.
    #
    'NO_WRAP_OPEN': '<span style="white-space: nowrap;">',
    'NO_WRAP_END':  '</span>',

    #
    # used by dsh_common_db.get_outgoing_context_extension().
    # for dot files.
    #
    'DEFAULT_EXTENSION': '510',


    #
    # 10/03/06:
    # upload reply url, for doctor's reply.
    # kind of like dsh_django_config 'REPLY_URL'.
    #
    'REPLY_UPLOAD_URL': '/replyupload/',

    #
    # kind of like dsh_django_config 'REPLY_ICON'.
    #
    'REPLY_UPLOAD_ICON': '<img src=/icons/dotarr3.gif title="upload reply" border=0 width=12 height=12>',

    #
    # 10/03/06:
    # the blank reply is put in the place of a reply to begin with.
    #
    'BLANK_REPLY_MP3': 'mp3/blank_reply.mp3',

    #
    # 10/03/14:
    # demographic icon and link.
    #
    'DEMOGRAPHIC_URL': '/demographics/',
    'DEMOGRAPHIC_ICON': '<img src=/icons/card004.gif title="demographics" border=0 width=14 height=11>',

    'KEYWORD_SELECT_URL': '/keywordsel/',
    'KEYWORD_SELECT_ICON': '<img src=/icons/ok2.gif title="select items with this keyword" border=0 width=9 height=9>',

    'KEYWORD_DESEL_URL': '/keyworddesel/',
    'KEYWORD_DESEL_ICON': '<img src=/icons/ok_not.gif title="de-select items with this keyword" border=0 width=9 height=9>',

    'LANDLINE_URL': '/lookupphone/',
    'LANDLINE_ICON': '<img src=/icons/phone010.gif title="landline" border=0 width=13 height=13>',

    #
    # 10/03/20:
    # how many times to retry the prompt for staff calls.
    # used by dsh_django2.handle_staff_caller().
    #
    'STAFF_RETRIES': 5,

    #
    # 10/03/22:
    # an alarm clock icon. denotes that a person is in the "current dial" set.
    #
    'CURRENT_DIAL_ICON': '<img src=/icons/clock136.gif title="in current dial set" border=0 width=13 height=11>',

    #
    # 10/03/22:
    # used by dsh_common_db.models_persons_key_link().
    #
    'PERSON_KEY_WORD_URL': \
        '/admin/db/person/?person_key_words__dsh_uid__exact=',

    #
    # 10/03/22:
    # stuff having to do with person key words.
    #
    'PERSON_KEYWORD_SELECT_URL': '/personkeywordsel/',
    'PERSON_KEYWORD_DESEL_URL': '/personkeyworddesel/',
    'PERSON_KEYWORD_PERSONS_URL': '/admin/db/person/?person_key_words__dsh_uid__exact=',
    'PERSON_KEYWORD_PERSONS_ICON': '<img src=/icons/card025.gif title="persons with this key word" border=0 width=8 height=10>',
    'PERSON_KEYWORD_ADD_URL': '/personkeywordadd/',
    'PERSON_KEYWORD_DEL_URL': '/personkeyworddel/',

    #
    # 10/03/23:
    # used by dsh_common_db.models_item_dummy_icon().
    #
    'DUMMY_ICON': '<img src=/icons/sound043.gif title="dummy" border=0 width=10 height=12>',

    #
    # 10/03/25:
    # stuff having to do with un-answering questions.
    #
    'PERSON_ANSWERED_ICON': '<img src=/icons/mic008.gif title="messages answered" border=0 width=7 height=12>',
    'PERSON_ANSWERED_URL': '/personanswered/',
    #'ANSWERED_EVENT_ICON': '<img src=/icons/mic007.gif title="answered event detail" border=0 width=7 height=12>',
    'ANSWERED_EVENT_ICON': '<img src=/icons/mic004.gif title="answered event detail" border=0 width=7 height=12>',
    'UNANSWER_URL': '/unanswer/',
    #'UNANSWER_ICON': '<img src=/icons/sound050.gif title="un-answer this" border=0 width=10 height=12>',
    'UNANSWER_ICON': '<img src=/icons/mic010.gif title="un-answer this" border=0 width=7 height=12>',
    'ANSWERS_PER_PAGE': 10,

    #
    # 10/03/28:
    # stuff having to do with displaying the entire history of a conversation
    # thread.
    #
    'CONVERSATION_CHAIN_URL': '/conversationhistory/',
    'CONVERSATION_CHAIN_ICON': '<img src=/icons/arr10b.gif title="conversation history" border=0 width=11 height=11>',

    #
    # 10/04/01:
    # stuff having to do with the ear icons: messages heard.
    #
    'BLUE_EAR': '<img src=/icons/ear_blue.gif title="messages heard" border=0 width=11 height=11>',
    'RED_EAR': '<img src=/icons/ear_red.gif title="unhear this message" border=0 width=11 height=11>',
    'GREEN_EAR': '<img src=/icons/ear_green.gif title="details of the heard event" border=0 width=11 height=11>',
    'PERSON_HEARD_URL': '/personheard/',
    'UNHEAR_URL': '/unhear/',

    #
    # 10/04/02:
    # used by filter_questions_answers_not_done().
    # for answers that have no question and/or not heard.
    #
    'RED_QUESTION': '<img src=/icons/quest2.gif title="this answer has no question" border=0 width=11 height=11>',
    'RED_EAR2': '<img src=/icons/ear_red.gif title="this answer unheard" border=0 width=11 height=11>',

    #
    # 10/04/09:
    # used by dsh_common_db.get_demo_reply().
    # the key word string for demo reply messages.
    #
    'DEMO_REPLY_KEYWORD': 'demo_reply',
    #
    # how many seconds to wait for the dot call file generated.
    # a delay is desirable to free up the current phone line of the field
    # worker.
    #
    'DEMO_REPLY_DELAY': 15,
}


#
# this will become a copy of the local version of the "dsh_config" module.
# it will be fixed by init().
#
configModule = None



def init(localConfigModule):
    """localConfigModule is the "dsh_config" file from the
    different apps."""

    global configModule

    configModule = localConfigModule



def lookup(key):
    global configModule
    assert configModule
    return configModule.lookup(key)



def lookup2(key):
    return config[key]
