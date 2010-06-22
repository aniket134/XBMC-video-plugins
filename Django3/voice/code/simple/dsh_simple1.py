#!/usr/bin/python -u

import sys,logging,os,signal,subprocess,datetime
import dsh_agi,dsh_utils,dsh_config,dsh_map,dsh_bizarro



#
# global variables for the signal handler.
#
globals4signal = {}



def setup_dirs():
    """make voice directories if they don't exist already."""

    outDir = dsh_config.lookup('voice_data_dir_out')

    if not dsh_utils.try_mkdir_ifdoesnt_exist(outDir,
                                              'dsh_simple1.setup_dirs: ' +
                                              'outgoing dir '):
        return (False,None,None)

    miscDict = dsh_utils.get_misc_dict()
    yearMonth = miscDict['year_month']

    inDir = dsh_config.lookup('voice_data_dir_in')
    inDir = os.path.join(inDir, yearMonth)
    
    if not dsh_utils.try_mkdir_ifdoesnt_exist(inDir,
                                              'dsh_simple1.setup_dirs: ' +
                                              'incoming dir '):
        return (False,None,None)

    return (True,outDir,inDir)



def sound_exists(prefix):
    """see if prefix.gsm or prefix.sln exists."""
    if dsh_utils.is_valid_file(prefix + '.sln', 'dsh_utils.sound_exists:',
                               silent=True) or \
       dsh_utils.is_valid_file(prefix + '.gsm', 'dsh_utils.sound_exists:',
                               silent=True):
        return True
    dsh_utils.give_bad_news('dsh_simple1.sound_exists: no out file: ' +
                            prefix, logging.error)
    return False



def init_dirs():
    global globals4signal

    #
    # set up logging.
    #
    logdir = dsh_config.lookup('log_file_dir')
    logName = dsh_config.lookup('log_file_name')
    dsh_utils.check_logging(logdir, logName)
    dsh_utils.give_news('dsh_simple1: entered --------------------',
                        logging.info)

    #
    # set up directories.
    #
    success,outDir,inDir = setup_dirs()
    if not success:
        return (False,None,None,None)
    dsh_utils.db_print('dsh_simple1.init_dirs: ' +
                       'outdir: ' + outDir + ', indir: ' + inDir, 94)

    #
    # check existence of output file.
    #
    outFile = dsh_config.lookup('outgoing_voice_file')
    outFile = os.path.join(outDir, outFile)
    if not sound_exists(outFile):
        return (False,None,None,None)
    dsh_utils.db_print('dsh_simple1.init_dirs: ' + 'outFile: ' + outFile, 94)

    globals4signal['log_dir'] = logdir
    
    return (True,inDir,outDir,outFile)



def lookup_number(env):
    """lookup the caller info in our map."""
    if env.has_key('agi_callerid'):
        phoneNumber = env['agi_callerid']
        #
        #cheat for testing.
        #
        #phoneNumber = '09935237793'
        #phoneNumber = '099'
    else:
        phoneNumber = 'unknown'
    return (phoneNumber,dsh_map.lookup(phoneNumber))



def hangup_signal_handler(signum, frame):
    """attempt to do file format conversion upon a hangup.
    from .wav to .mp3."""
    
    dsh_utils.db_print2('dsh_simple1.signal_handler: entered...', 94)


    #
    # get the name of the file that was just recorded.
    #
    if not globals4signal.has_key('in_file'):
        dsh_utils.give_news('dsh_simple1.hangup_signal_handler: ' +
                            'hangup before recording.', logging.info)
        sys_exit(0)

    inputFile = globals4signal['in_file']


    #
    # the recorded format is wav? if not, we don't convert.
    #
    fileFormat = dsh_config.lookup('record_file_format')
    if fileFormat != 'wav':
        dsh_utils.give_bad_news('dsh_simple1.hangup_signal_handler: ' +
                                "can't convert non-wav file: " + inputFile,
                                logging.error)

    #
    # does the .wav file exist and is it non-zero sized?
    #
    inputWav = inputFile + '.wav'
    success,bytes = dsh_utils.get_file_size(inputWav)
    if not success:
        dsh_utils.give_news('dsh_simple1.hangup_signal_handler: ' +
                            'no input file to convert: ' +
                            inputWav, logging.info)
        sys_exit(1)
    if bytes == 0:
        dsh_utils.give_news('dsh_simple1.hangup_signal_handler: ' +
                            'inputfile size 0: ' + inputWav, logging.info)
        sys_exit(1)

    dsh_utils.db_print2('dsh_simple1.signal_handler: ready to convert: ' +
                        inputWav, 94)

    #
    # where's the lame binary?
    #
    lamePath = dsh_config.lookup('lame_location')
    if not dsh_utils.is_valid_file(lamePath,
                                   msg='dsh_simple1.hangup_signal_handler:'):
        dsh_utils.give_bad_news('dsh_simple1.hangup_signal_handler: ' +
                                'need to install lame.', logging.error)
        sys_exit(1)


    #
    # stdout and stderr redirected to the log directory.
    #
    stdLogs = dsh_bizarro.stdio_logs_open(globals4signal['log_dir'])
    if not stdLogs:
        sys_exit(1)
    stdout,stderr = stdLogs


    #
    # the conversion command should be:
    # lame --resample 22.05 -b 24 test.wav test4.mp3
    #
    mp3Quality = dsh_config.lookup('lame_mp3_quality')
    outputMp3 = inputFile + '.mp3'
    #command = ffmpegPath + ' -i ' + inputWav + mp3Quality + outputMp3
    command = lamePath + mp3Quality + inputWav + ' ' + outputMp3

    ret = subprocess.call(command, shell=True, stdout=stdout, stderr=stderr)
    if ret != 0:
        dsh_utils.give_bad_news('dsh_simple1.signal_handler: ' +
                                'error in format conversion: ' +
                                command, logging.error)
        sys_exit(1)

    dsh_utils.give_news('dsh_simple1.signal_handler: conversion success: ' +
                        command, logging.info)
    if not dsh_utils.cleanup_path(inputWav, 'dsh_simple1.signal_handler'):
        dsh_utils.give_bad_news('dsh_simple1.signal_handler: ' +
                                'failed to remove original wav: ' +
                                inputWav, logging.warning)

    #
    # no point continuing execution after hangup.
    #
    sys_exit(0)



def sys_exit(code):
    """a wrapper for sys.exit()"""

    #
    # repeats the caller info: phone number, school, name.
    #
    if globals4signal.has_key('log_str'):
        logStr = globals4signal['log_str']
    else:
        logStr = ''

    #
    # compute the duration of the call.
    #
    endTime = datetime.datetime.now()
    startTime = globals4signal['start_time']
    delta = endTime - startTime
    seconds = delta.seconds
    dsh_utils.db_print('dsh_simple1.sys_exit: call duration: ' +
                       str(seconds) + 's.', 95)
    logStr += str(seconds) + ' || '

    #
    # compute the duration of the recording.
    #
    if globals4signal.has_key('start_record'):
        startRecord = globals4signal['start_record']
        delta = endTime - startRecord
        seconds = delta.seconds
        dsh_utils.db_print('dsh_simple1.sys_exit: record duration: ' +
                           str(seconds) + 's.', 95)
        logStr += str(seconds) + ' ||'

    dsh_utils.give_news('dsh_simple1.sys_exit: ' + logStr, logging.info)
    sys.exit(code)
    


def main():
    global globals4signal

    globals4signal['start_time'] = datetime.datetime.now()

    #
    # check the voice data directories.
    #
    success,inDir,outDir,outFile = init_dirs()
    if not success:
        sys_exit(1)

    #
    # get the AGI environment variables.
    #
    env = dsh_agi.read_env()
    if env == {}:
        dsh_utils.give_bad_news('dsh_simple1: failed to read agi envs.',
                                logging.error)
        sys_exit(1)

    #
    # log the caller info.
    # and construct a recorded file name based on caller info.
    #
    phoneNumber,callerInfo = lookup_number(env)
    logStr = dsh_map.log_caller_info(phoneNumber, callerInfo)
    globals4signal['log_str'] = logStr
    callerInfoStr = dsh_map.info2str(phoneNumber, callerInfo)
    callerInfoStr = dsh_utils.date_time_rand2() + '_' + callerInfoStr

    #
    # looks like: 090702_200101_38_09935237793_DSH_Randy-Wang.gsm
    #
    dsh_utils.db_print('dsh_simple1: callerInfoStr: ' + callerInfoStr, 94)


    #
    # setting up signal handler for hangup.
    # the handler will attempt to do the file format conversion.
    #
    signal.signal(signal.SIGHUP, hangup_signal_handler)
    

    #
    # play the out file.
    #
    dsh_agi.say_it(outFile)

    #
    # record it.
    #
    inFile = os.path.join(inDir, callerInfoStr)
    globals4signal['in_file'] = inFile
    globals4signal['start_record'] = datetime.datetime.now()
    dsh_agi.record(inFile)

    #
    # say it back.
    #
    #dsh_agi.say_it(inFile)

    dsh_utils.give_news('dsh_simple1: recording done.')

    #
    # convert file format too with a proper hangup (pressing the # key).
    #
    hangup_signal_handler(0, None)

    

if __name__ == '__main__':
    main()
