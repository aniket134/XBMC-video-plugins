CONFIG = {
    'outgoing_voice_file': '090803_tanuja',
    #'outgoing_voice_file': '090702_me',
    
    'log_file_dir': '/u/rywang/phone_data/log/',
    'log_file_name': 'simple1_log.txt',

    'voice_data_dir_in': '/u/rywang/phone_data/in_voice/',
    'voice_data_dir_out': '/u/rywang/phone_data/out_voice/',
    
    'record_time_limit': 600000,        # in ms, that's 10 minutes.
    'record_stop_key': '#',
    'record_file_format': 'wav',

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

    'django_sys_paths': ['/home/rywang/voice/code/django/',
                         '/home/rywang/voice/code/django/dvoice/'],
    'DJANGO_SETTINGS_MODULE': 'dvoice.settings',
}



def lookup(key):
    return CONFIG[key]
