#!/usr/bin/python -u

import sys,re,time,random



def read_env():
    env = {}
    while 1:
        line = sys.stdin.readline().strip()
        if line == '':
            break
        key,data = line.split(':')
        if key[:4] <> 'agi_':
            #skip input that doesn't begin with agi_
            sys.stderr.write("Did not work!\n");
            sys.stderr.flush()
            continue
        key = key.strip()
        data = data.strip()
        if key <> '':
            env[key] = data

      
    sys.stderr.write("AGI Environment Dump:\n");
    sys.stderr.flush()
    for key in env.keys():
        sys.stderr.write(" -- %s = %s\n" % (key, env[key]))
        sys.stderr.flush()

    return env



def checkresult(params):
    params = params.rstrip()
    if re.search('^200',params):
        result = re.search('result=(\d+)',params)
        if (not result):
            sys.stderr.write("FAIL ('%s')\n" % params)
            sys.stderr.flush()
            return -1
        else:
            result = result.group(1)
            #debug("Result:%s Params:%s" % (result, params))
            sys.stderr.write("PASS (%s)\n" % result)
            sys.stderr.flush()
            return result
    else:
        sys.stderr.write("FAIL (unexpected result '%s')\n" % params)
        sys.stderr.flush()
        return -2



def sayit(params):
    sys.stderr.write("STREAM FILE %s \"\"\n" % str(params))
    sys.stderr.flush()
    sys.stdout.write("STREAM FILE %s \"\"\n" % str(params))
    sys.stdout.flush()
    result = sys.stdin.readline().strip()
    checkresult(result)



def send_command(command):
    sys.stderr.write(command)
    sys.stderr.flush()
    sys.stdout.write(command)
    sys.stdout.flush()
    result = sys.stdin.readline().strip()
    res = checkresult(result)
    return res
    


def record(fileName):
    command = 'RECORD FILE ' + fileName + ' gsm # 30000\n'
    send_command(command)



def main():
    read_env()
    prefix = '/u/rywang/voice/tmp/'
    testOut1 = prefix + 'test_out1'
    testOut2 = prefix + 'test_tanuja'
    testIn1 = prefix + 'test_in1'
    sayit(testOut1)
    #sayit(testOut2)
    #sayit('/var/lib/asterisk/sounds/demo-congrats')
    record(testIn1)
    sayit(testIn1)
    sayit(testIn1)

    

if __name__ == '__main__':
    main()
