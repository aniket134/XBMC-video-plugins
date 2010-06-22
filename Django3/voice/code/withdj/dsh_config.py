CONFIG = {
    'APP_NAME': 'dvoice',
    'APP_NAME_MODELS': 'dvoice.db.models',
    
    'outgoing_voice_file': '090702_tanuja',
    #'outgoing_voice_file': '090702_me',
    
    'log_file_dir': '/home/rywang/phone_data/log/',
    #'log_file_name': 'simple1_log.txt',
    'log_file_name': 'withdj_log.txt',
    'timed_log_file_name': 'timed_log.txt',


    #
    # this also gets sucked into dsh_django_config.py
    #
    'PHONE_DATA_DJANGO_PATH': '/home/rywang/phone_data/django/',
    
    #
    # /media/ gets chopped of in dsh_django1.py.
    # it needs a relative path, like voice/09/07/blah
    #
    'ABS_URL_PREFIX_CHOP': '/media/',

    #
    # voice files are stored in:
    # /home/rywang/phone_data/django/media/voice/09/07/
    #
    'MEDIA_DIR': '/home/rywang/phone_data/django/media/',
    'VOICE_SUBDIR': 'voice/',
    #
    #CONFIG['VOICE_DIR'] = CONFIG['MEDIA_DIR'] + CONFIG['VOICE_SUBDIR'],
    # /home/rywang/phone_data/django/media/voice/
    # this is patched in at the bottom of this file.
    #
    'DATE_FORMAT_DIR_STR': '%y/%m',

    'IMG_SUBDIR': 'pic/',
    #
    #CONFIG['IMG_DIR'] = CONFIG['MEDIA_DIR'] + CONFIG['IMG_SUBDIR'],
    # this is patched in at the bottom of this file.
    #

    
    #'record_time_limit': 480000,        # in ms, that's 8 minutes.
    'record_time_limit': 300000,        # in ms, that's 8 minutes.
    #'record_time_limit': 3000,        # for testing.
    
    
    'record_stop_key': '#',
    'record_file_format': 'wav',
    'play_stop_key': '#',

    #
    # the following settings were for using ffmpeg
    # to convert wav to mp3.  I'm not using this any more.
    # turns out I have been actually converting to mp2.
    # now I'm going to use lame instead.
    #
    'ffmpeg_location': '/usr/local/bin/ffmpeg',
    'mp3_quality': ' -ar 22050 -ab 32000 ',


    #
    # use lame to convert wav to mp3.
    # the command looks like:
    # lame --resample 22.05 -b 24 test.wav test4.mp3
    # like ffmpeg, if I don't resample, I hear broken output.
    #
    'lame_location': '/usr/bin/lame',
    'lame_mp3_quality': ' --resample 22.05 -b 24 ',

    'django_sys_paths': ['/home/rywang/voice/code/common/',
                         '/home/rywang/voice/code/withdj/',
                         '/home/rywang/voice/code/django/',
                         '/home/rywang/voice/code/django/dvoice/'],
    'DJANGO_SETTINGS_MODULE': 'dvoice.settings',

    'UNKNOWN_PHONE_NUMBER': 'xxxx',
    'UNKNOWN_PERSON_NAME': 'no-name',
    'UNKNOWN_ORG_ALIAS': 'unknown-org',

    #
    # how many trailing digits of a phone number to hide.
    #
    'HIDE_PHONE_DIGITS': 4,


    #
    # directory where more voice prompts live.
    #
    'DSH_PROMPT_DIR': '/home/rywang/voice/conf/sound',

    #
    # voice prompt for staff member to enter choices.
    #
    #'DSH_PROMPT_ENTER_CHOICE': 'enter_choice3',
    'DSH_PROMPT_ENTER_CHOICE': 'press4',

    #
    # "the following messages have been recorded recently."
    #
    'DSH_PROMPT_RECENTLY': 'recently',
    'DSH_PROMPT_RECENT_END': 'recent_end',

    #
    # voice prompt for peer-shared messages.
    #
    'DSH_PROMPT_MESSAGE_BY': 'peer_message_by',
    'DSH_PROMPT_A_TEACHER': 'peer_a_teacher',
    'DSH_PROMPT_DSH_VOICE': 'peer_dsh_voice',
    'DSH_PROMPT_FROM': 'peer_from',
    'DSH_PROMPT_SCHOOL': 'peer_school',

    #
    # prompt
    #
    'DSH_PROMPT_PLEASE_RECORD': 'please_record',

    #
    # ask the user to enter a phone number.
    #
    'DSH_PROMPT_PHONE_NUMBER': 'enter_number',

    #
    # timeout for entering one digit. 10 seconds.
    #
    'DSH_PROMPT_WAIT1': 10000,
    
    #
    # timeout for entering 11 digits. 30 seconds.
    #
    'DSH_PROMPT_WAIT11': 30000,

    #
    # if we fail to play recent messages, say sorry.
    #
    'DSH_PROMPT_SORRY': 'ryw_sorry',

    #
    # when a staff presses 3, how many recent messages to play back.
    #
    'DSH_RECENT_HOWMANY': 3,

    #
    # forward call channel.
    #
    'FORWARD_OUTGOING_CHANNEL': 'mISDN/3c',
    'FORWARD_OUTGOING_CHANNEL_IAX2': 'IAX2',
    'FORWARD_OUTGOING_CHANNEL_MISDN': 'mISDN/3c',

    #
    # am I doing testing on Barney?
    #
    'BARNEY_TEST': False,
    'BARNEY_TEST_JUNIOR_ZOIPER': '192.168.2.7:4569',
    'BARNEY_TEST_DOT_CALL_NUMBER': 'dot',

    #
    # URL for looking up a person.
    # used by models.Item to point to owner.
    # no, not necessary to move.
    #
    #'PERSON_URL': '/admin/db/person/?id=',

    #
    # red5 stream dir.
    # this is where we deposit temporary recordings by red5.
    #
    'RED5_STREAMS_DIR': '/usr/share/red5/webapps/oflaDemo/streams',
    
    #
    # prefixed to callerID, indicating to the script that the
    # call is initiated by a .call file.
    # used by dsh_django_utils.generate_dot_call_file().
    # and most likely, dsh_django2.py
    #
    'DOT_CALL_INDICATOR': '__DOT_CALL__',

    #
    # used to make .call files.
    #
    'TMP_DIR': '/tmp',

    #
    # where to put the .call files for Asterisk to pick up.
    #
    'ASTERISK_DOT_CALL_DIR': '/var/spool/asterisk/outgoing',

    #
    # use this gmail account to send mail.
    #
    'GMAIL_SENDER_ADDRESS': 'dsh.voice@gmail.com',
    'GMAIL_SENDER_PASSWORD': 'virtuala',
    'GMAIL_SENDER_SUBJECT': 'DSH voice messages',
    'GMAIL_DEFAULT_RECIPIENT': 'dsh-lko-office@googlegroups.com',

    #
    # how long does a hung-up partial call has to last to be considered
    # "heard"?
    # we set it to 60% for now.
    # 12/12/09: changed to 0.30
    #
    'PARTIAL_HEARD': 0.30,

    #
    # threshold of how much needs to be played for one's own message
    # in order to be considered heard.
    #
    'PARTIAL_OWN_HEARD': 0.05,

    #
    # sort stats by which criteria.
    #
    'STATS_SORT_BY': 'calldur',

    #
    # how long does the recording have to be in order to count as
    # a recorded item.  used by both counting stats, and
    # playing recently recorded.
    #
    'RECORDED_THRESH': 15,

    #
    # for dialing the scratch number.
    #
    'DSH_PROMPT_NO_SCRATCH': 'no_scratch',
    'DSH_PROMPT_DIAL_SCRATCH': 'dial_scratch',
}


import os
os.environ['DJANGO_SETTINGS_MODULE'] = CONFIG['DJANGO_SETTINGS_MODULE']


CONFIG['VOICE_DIR'] = CONFIG['MEDIA_DIR'] + CONFIG['VOICE_SUBDIR']
CONFIG['IMG_DIR'] = CONFIG['MEDIA_DIR'] + CONFIG['IMG_SUBDIR'],



def lookup(key):
    return CONFIG[key]



def init_barney_test_channel():
    """called by init() and init2() below."""
    global CONFIG
    CONFIG['FORWARD_OUTGOING_CHANNEL'] = \
        CONFIG['FORWARD_OUTGOING_CHANNEL_IAX2']
    CONFIG['BARNEY_TEST'] = True



def init(agiEnv):
    """called by dsh_django2.py.  for forwarding calls."""
    global CONFIG
    if agiEnv.has_key('agi_context') and agiEnv['agi_context'] == 'demo':
        init_barney_test_channel()



import socket
def init_for_dot_calls():
    """called by dsh_django_utils.py, for automatically scheduled
    outgoing calls."""
    global CONFIG
    CONFIG['OUTGOING_CONTEXT'] = 'misdnin'
    hostName = socket.gethostname()
    CONFIG['HOSTNAME'] = hostName
    if hostName == 'barney':
        init_barney_test_channel()
        CONFIG['OUTGOING_CONTEXT'] = 'demo'

