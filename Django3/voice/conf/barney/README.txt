relevant snippets from extensions.conf

----------

;
; RYW
; this is for testing the DSH voice forum.
;
exten => 510,1,Answer()
exten => 510,n,Wait(1)
exten => 510,n,AGI(/u/rywang/voice/code/simple/dsh_simple1.py)
exten => 510,n,Wait(1)
exten => 510,n,Hangup()


;
; RYW
; this is for testing briding two IAX phones.
; a Kiax phone on localhost (192.168.2.10), with username idefisk.
; a Zoiper phone on junior (192.168.2.6), with username sfone.
; the Kiax phone is logged on as idefisk@localhost.
; I use that phone to dial extension 520.
; Asterisk gets it and dials the Zoiper phone on the other end.
; now they speak to each other.
; if something bad happens, it plays the 'demo-nogo' sound.
;
exten => 520,1,Dial(IAX2/192.168.2.6:4573-8198)
exten => 520,n,Playback(demo-nogo)
exten => 520,n,Hangup()		

----------

The funny line in test.call:
Channel: IAX2/192.168.2.6:4573-8198

this info is gotten from making the soft phone dial Asterisk and
look at the console, particularly the :4573-8198 bit.

----------

the 1000, 600, 500 extensions are the original conf extensions to try.
1000 entrance point.
600 echo test.
500 connects to Asterisk at Digium.


------------------------------------------------------------

09/08/13:

test_outgoing.call
copy this to the asterisk outgoing .call directory
it calls the Zoiper phone on the VM.

