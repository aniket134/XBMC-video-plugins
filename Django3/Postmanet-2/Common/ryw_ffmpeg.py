import sys, os, cgi, cgitb, objectstore, random, shutil
import logging, datetime, time, cStringIO, shutil
import su, ryw, string, ryw_view, time, ryw_hindi, math
import subprocess, re, ryw_bizarro



FFMPEG_INFO_TABLE = {
    'duration': ('Duration',
                 r'Duration: ([0-9][0-9]):([0-9][0-9]):([0-9][0-9])\.'),
    'bitrate': ('Bitrate', r'bitrate: ([0-9]+ kb/s)'),
    'video_codec': ('Video codec', r'Stream #0\.0: Video: (.[a-z|0-9]+),'),
    'audio_codec': ('Audio codec', r'Stream #0\.1: Audio: (.[a-z|0-9]+),'),
    'audio_codec0': ('Audio codec', r'Stream #0\.0: Audio: (.[a-z|0-9]+),'),
    'frequency': ('Audio frequency', r', ([0-9]+ Hz), '),
    'channels': ('Audio channels', r', (stereo|mono), '),
    'resolution': ('Resolution', r', yuv420p, ([0-9]+x[0-9]+) \[PAR'),
    'frame_rate': ('Frame rate', r'\], ([0-9]+\.[0-9]+) tb\(r\)'),
    'image': ('Image', r'Input #0, (image)'),
    'avi': ('AVI', r'Input #0, (avi),'),
    'mp3': ('MP3', r'Input #0, (mp3),')
}

FFMPEG_VIDEO_KEYS = ['bitrate', 'video_codec', 'audio_codec',
                     'frequency', 'channels', 'resolution', 'frame_rate']

FFMPEG_AUDIO_KEYS = ['bitrate', 'audio_codec0', 'frequency', 'channels']

FFMPEG_DONT_PRINT_KEYS = ['image', 'avi', 'mp3']



def verify_ffmpeg_existence(RepositoryRoot):
    return ryw_bizarro.verify_ffmpeg_existence(RepositoryRoot)



#
# returns (searchResult, group(1))
#
def extract_one_pattern(ffmpegOut, regex):
    regexComp = re.compile(regex)
    searchResult = regexComp.search(ffmpegOut)

    if searchResult == None:
        return (None, None)

    try:
        group1 = searchResult.group(1)
    except:
        ryw.give_bad_news('extract_one_pattern: trouble getting group(1): '+
                          regex + ' ___on___ ' + ffmpegOut, logging.critical)
        return (None, None)

    return (searchResult, group1)



def trunc_zero(str):
    if len(str) == 2 and str[0] == '0':
        return str[1]
    return str



def set_duration(meta, hours, minutes, seconds):
    if hours == '00' and minutes == '00' and seconds == '00':
        return

    hours = trunc_zero(hours)
    minutes = trunc_zero(minutes)
    seconds = trunc_zero(seconds)
    meta['time_length'] = [hours, minutes]
    meta['time_length_seconds'] = seconds



def extract_duration(meta, searchResult):
    if meta.has_key('time_length'):
        logging.info('extract_duration: duration already filled in.')
        return

    if searchResult == None:
        return

    try:
        hours = searchResult.group(1)
        minutes = searchResult.group(2)
        seconds = searchResult.group(3)
    except:
        ryw.give_bad_news('extract_duration: failed to find components: ' +
                          repr(searchResult), logging.critical)
        return
    
    set_duration(meta, hours, minutes, seconds)



def set_media_attrs(meta, mediaAttrName):
    if not meta.has_key('media') or meta['media'] == None:
        meta['media'] = []
    if mediaAttrName in meta['media']:
        return
    meta['media'].append(mediaAttrName)



def set_ffmpeg_attribute(meta, key, group1):
    if not meta.has_key('ffmpeg'):
        meta['ffmpeg'] = {}
    meta['ffmpeg'][key] = group1
    
    if group1 == 'image':
        set_media_attrs(meta, 'images')
    elif group1 == 'avi':
        set_media_attrs(meta, 'video')



def has_these_attrs(meta, listAttrs):
    if not meta.has_key('ffmpeg'):
        return False
    
    ffmpeg = meta['ffmpeg']
    answer = True
    for attr in listAttrs:
        if attr not in ffmpeg:
            return False

    return True



def extract_all(meta, ffmpegOut):
    for key, val in FFMPEG_INFO_TABLE.iteritems():
        if key == 'duration':
            continue
        description,regex = val
        searchResult,group1 = extract_one_pattern(ffmpegOut, regex)
        if group1 == None:
            continue
        ryw.give_news2(key + ' - ' + group1 + ', ', logging.info)
        set_ffmpeg_attribute(meta, key, group1)

    if has_these_attrs(meta, FFMPEG_VIDEO_KEYS):
        set_media_attrs(meta, 'video')
    elif has_these_attrs(meta, FFMPEG_AUDIO_KEYS):
        set_media_attrs(meta, 'audio_without_video')



def try_exec(RepositoryRoot, meta, tmpdir, uploadFileName):
    commandPath = verify_ffmpeg_existence(RepositoryRoot)
    if commandPath == None:
        return
    
    filePath = os.path.join(tmpdir, uploadFileName)
    executeThis = commandPath + ' -i ' + '"' + filePath + '"'

    ryw.give_news2('<BR>Invoking ffmpeg... ', logging.info)

    try:
        pipe = subprocess.Popen(executeThis, shell=True,
                                stderr=subprocess.PIPE)
        execResult = pipe.communicate()[1]
    except:
        ryw.give_bad_news('try_extract_duration: ffmpeg execution failed: '+
                          executeThis, logging.error)
        return

    #ryw.give_news(execResult, logging.info)

    extract_all(meta, execResult)

    if meta.has_key('ffmpeg') and meta['ffmpeg'].has_key('image'):
        if meta['ffmpeg'].has_key('frame_rate'):
            del meta['ffmpeg']['frame_rate']        
    else:
        searchResult,group1 = extract_one_pattern(
            execResult, FFMPEG_INFO_TABLE['duration'][1])
        extract_duration(meta, searchResult)

    #ryw.give_news('try_exec done: ' + repr(meta), logging.info)



def add_attrs_to_string(meta, partialStr):
    if not meta.has_key('ffmpeg'):
        return partialStr
    ffmpeg = meta['ffmpeg']
    
    for key, val in FFMPEG_INFO_TABLE.iteritems():
        if key in FFMPEG_DONT_PRINT_KEYS:
            continue
        description,regex = val
        if not ffmpeg.has_key(key):
            continue
        partialStr += '<LI><B>' + description + '</B>: '
        partialStr += ryw_view.scrub_js_string(ffmpeg[key])
    return partialStr



def has_resolution(meta):
    if not meta.has_key('ffmpeg'):
        return False
    ffmpeg = meta['ffmpeg']
    return ffmpeg.has_key('resolution')



def has_ffmpeg(meta):
    return meta.has_key('ffmpeg')
