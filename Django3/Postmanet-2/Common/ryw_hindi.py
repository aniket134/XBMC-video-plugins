import ryw,ryw_view
from ryw_hindi_dict import dictionary



dictPrintHeader = """
#
# format:
#     {key: (English, Hindi)}
#
dictionary = {
"""

UNTRANSLATED_STRING = 'XXX'



hindi_to_english_dictionary = {}

def hindi_to_english_dict(dict):
    for (x,y) in dict.values():
        hindi_to_english_dictionary[y] = \
            hindi_to_english_dictionary.get(y,[]) + [x]

hindi_to_english_dict(dictionary)



def hindi_to_english(hindi,all = False):
    if all:
        return hindi_to_english_dictionary[hindi]
    else:
        return hindi_to_english_dictionary[hindi][0]



#HINDI_TEXT_ATTR = 'STYLE="font-family: Shusha; font-size: 18; color: blue;"'
#HINDI_FONT_ATTR = '<FONT FACE=Shusha COLOR=blue '
HINDI_TEXT_ATTR = 'STYLE="font-family: Kundli; font-size: 18; color: blue;"'
HINDI_FONT_ATTR = '<FONT FACE=Kundli COLOR=blue '



def access_dictionary(englishKey):
    hindi = dictionary[englishKey][1]
    if hindi == 'XXX':
        hindi = ''
    return hindi

    

def size_html(hindiTxt, size):
    size = str(size)
    return HINDI_FONT_ATTR + 'SIZE=' + size + '>' + hindiTxt + '</FONT>'



def size4_bold_html(englishKey):
        
    return '<B>' + size_html(hindi, 4) + '</B>'



def size4_html(englishKey):
    hindi = access_dictionary(englishKey)
    return size_html(hindi, 4)



def size3_html_key(englishKey):
    hindi = access_dictionary(englishKey)
    return size_html(hindi, 3)



def html_key(englishKey):
    hindi = access_dictionary(englishKey)
    return HINDI_FONT_ATTR + '>' + hindi + '</FONT>'



def size4_bold_html2(hindiTxt):
    return '<B>' + size_html(hindiTxt, 4) + '</B>'



def size2_html(hindiTxt):
    return size_html(hindiTxt, 2)



def size3_html(hindiTxt):
    return size_html(hindiTxt, 3)



def html(hindiTxt):
    return HINDI_FONT_ATTR + '>' + hindiTxt + '</FONT>'



def truncate_size4_bold_html(hindiTxt, limit):
    trunc = ryw_view.truncate_string2(hindiTxt, limit)
    head,tail = trunc
    resultStr = size4_bold_html2(head)
    if tail:
        resultStr += '<FONT SIZE=4><B>' + tail + '</B></FONT>'
    return resultStr



def truncate_size2_html(hindiTxt, limit):
    trunc = ryw_view.truncate_string2(hindiTxt, limit)
    head,tail = trunc
    resultStr = size2_html(head)
    if tail:
        resultStr += '<FONT SIZE=2>' + tail + '</FONT>'
    return resultStr



def truncate_size3_html(hindiTxt, limit):
    trunc = ryw_view.truncate_string2(hindiTxt, limit)
    head,tail = trunc
    resultStr = size3_html(head)
    if tail:
        resultStr += '<FONT SIZE=3>' + tail + '</FONT>'
    return resultStr



def truncate_html(hindiTxt, limit):
    trunc = ryw_view.truncate_string2(hindiTxt, limit)
    head,tail = trunc
    resultStr = html(head)
    if tail:
        resultStr += tail
    return resultStr



def attr(meta, attrName):
    if meta.has_key('hindi'):
        hindi = meta['hindi']
        if hindi.has_key(attrName):
            return hindi[attrName]

    return ''



def replace_size4_hindi_html(str, keys):
    dict = dict_size4_hindi_html(keys)
    return str % dict



def replace_hindi(str, keys):
    dict = dict_hindi(keys)
    return str % dict



def dict_size4_hindi_html(keys):
    dict = {}
    for key in keys:
        dict['trans_' + key] = size4_html(key)
    dict['trans_txt_style'] = HINDI_TEXT_ATTR
    return dict



#
# same as the above, except blanked out hindi strings.
# 
def dict_size4_blank_html(keys):
    dict = {}
    for key in keys:
        dict['trans_' + key] = ''
    dict['trans_txt_style'] = ''
    return dict



def dict_hindi1(key):
    return access_dictionary(key)



def dict_hindi(keys):
    dict = {}
    dict['year'] = ryw.get_year()
    for key in keys:
        dict['trans_' + key] = dict_hindi1(key)
    dict['trans_txt_style'] = HINDI_TEXT_ATTR
    return dict



#
# same as above, except all strings are blanked out.
#
def dict_blank(keys):
    dict = {}
    dict['year'] = ryw.get_year()
    for key in keys:
        dict['trans_' + key] = ''
    dict['trans_txt_style'] = ''
    return dict



def give_plain_and_html_dict(keys1, keys2):
    dict1 = dict_size4_hindi_html(keys1)
    dict2 = dict_hindi(keys2)
    dict1.update(dict2)
    return dict1



def replace_hindi_plain_and_html(str, keys1, keys2, otherDict = {}):
    dict = give_plain_and_html_dict(keys1, keys2)
    if otherDict:
        dict.update(otherDict)
    return str % dict



def print_dict():
    print dictPrintHeader
    for dictKey,dictStrs in dictionary.iteritems():
        print "    " + repr(dictKey) + ': ' + repr(dictStrs) + ','
    print "}"
