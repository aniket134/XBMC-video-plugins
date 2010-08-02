import _sphinx3, sys, os, osc

host = "localhost"	
portout = 9000

osc.init()
osc.sendMsg("/ready","1",host,portout)

_sphinx3.parse_argdict({'samprate': '16000', 'hmm': sys.path[0]+'/dic', 'dict': sys.path[0]+'/dic/pd.dic', 'fdict': sys.path[0]+'/dic/filler', 'lm': sys.path[0]+'/dic/pd.dmp'})
_sphinx3.init()
data = open("/tmp/r16k.raw").read()
words = _sphinx3.decode_raw(data)

osc.sendMsg("/words",str.lower(words[0]),host,portout)
