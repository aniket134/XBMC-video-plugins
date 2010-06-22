#!/usr/bin/python -u
#
# mostly copied from the starfish book. (07/01/09)
# 

import logging,sys,re,time,random,dsh_utils,dsh_config



def console_message(message):
    """prints to the Asterisk console window.
    called by print routines in dsh_utils.py"""
    message = message.strip()
    message = message + '\n'
    sys.stderr.write(message);
    sys.stderr.flush()
    


def console_message_log(message, log_type=logging.info):
    """called by the various give_message() functions in dsh_utils.py"""
    console_message(message)
    if log_type:
        message = message.strip()
        log_type(message)



def split_line(line):
    """split the lines for agi env variables.
    this is written to deal with something like this:
    agi_channel: IAX2/127.0.0.1:35456-14868"""
    try:
        #
        # this splits at most once.
        #
        key,data = line.split(':',1)
        if key != '':
            return (True,key,data)
        return (False,None,None)
    except:
        return (False,None,None)
        


def read_env(consoleMsg=True):
    """reads AGI environment variables at the beginning of a call."""
    env = {}
    while 1:
        line = sys.stdin.readline().strip()
        if line == '':
            break

        
        #
        # ryw:
        # bad format. not splittable.
        # this is because I found a line that looks like this:
        # agi_channel: IAX2/127.0.0.1:35456-14868
        #
        #key,data = line.split(':')
        success,key,data = split_line(line)
        if not success:
            info = 'dsh_agi.read_env: bad line: ' + line
            dsh_utils.give_bad_news2(info, logging.warning)
            continue
            
        if key[:4] <> 'agi_':
            #skip input that doesn't begin with agi_
            info = 'dsh_agi.read_env: invalid key: ' + key[:4]
            dsh_utils.give_bad_news2(info, logging.warning)
            continue
        key = key.strip()
        data = data.strip()
        if key <> '':
            env[key] = data

    keys2skip = ['agi_rdnis', 'agi_uniqueid', 'agi_language', 'agi_callington',
                 'agi_callingtns', 'agi_accountcode', 
                 'agi_enhanced', 'agi_callingpres', 'agi_callingani2',
                 'agi_dnid', 'agi_rdnis', 'agi_priority']
                 
    if consoleMsg:
        info = "dsh_agi.read_env: AGI Environment Dump:"
        dsh_utils.give_news(info, logging.info)
        for key in env.keys():
            if key in keys2skip:
                continue
            info = " -- %s = %s" % (key, env[key])
            dsh_utils.give_news(info, logging.info)

    return env



def check_result(params, consoleMsg=True):
    params = params.rstrip()
    if re.search('^200',params):
        result = re.search('result=(\d+)',params)
        if (not result):
            if consoleMsg:
                info = "dsh_agi.check_result: FAIL ('%s')" % params
                dsh_utils.give_bad_news2(info, logging.error)
            return -1
        else:
            result = result.group(1)
            if consoleMsg:
                info = "dsh_agi.check_result: PASS (%s)" % result
                dsh_utils.give_good_news(info, logging.info)
            return result
    else:
        if consoleMsg:
            info = "dsh_agi.check_result: " + \
                   "FAIL (unexpected result '%s')" % params
            dsh_utils.give_bad_news2(info, logging.error)
        return -2



def send_command(command, caller="", consoleMsg=True):
    if consoleMsg:
        dsh_utils.give_news(caller + command)
    sys.stdout.write(command)
    sys.stdout.flush()
    result = sys.stdin.readline().strip()
    res = check_result(result, consoleMsg)
    return res



def say_it(params, consoleMsg=True):
    command = "STREAM FILE %s \"\"\n" % str(params)
    res = send_command(command, "dsh_agi.sayit: ", consoleMsg)
    return res
        


def record(fileName, consoleMsg=True):
    timeLimit = dsh_config.lookup('record_time_limit')
    stopButton = dsh_config.lookup('record_stop_key')
    fileFormat = dsh_config.lookup('record_file_format')
    command = 'RECORD FILE ' + fileName + ' ' + fileFormat + ' ' + \
              stopButton + ' ' + str(timeLimit) + '\n'
    res = send_command(command, 'dsh_agi.record: ', consoleMsg)
    return res
