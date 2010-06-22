#!/usr/bin/python -u

import dsh_agi, dsh_utils, dsh_config



def main():
    prefix = dsh_config.lookup('log_file_dir')
    logName = dsh_config.lookup('log_file_name')
    
    dsh_utils.check_logging(prefix, logName)
    dsh_utils.db_print('dsh_test1: entered...', 93)
    
    dsh_agi.read_env()

    testOut1 = prefix + 'test_out1'
    testOut2 = prefix + 'test_tanuja'
    testIn1 = prefix + 'test_in1'
    dsh_agi.say_it(testOut1)
    #dsh_agi.say_it(testOut2)
    #dsh_agi.say_it('/var/lib/asterisk/sounds/demo-congrats')
    dsh_agi.record(testIn1)
    dsh_agi.say_it(testIn1)
    dsh_utils.give_news('dsh_test1: done.')

    

if __name__ == '__main__':
    main()
