import ryw_view



#
# format:
#     {key: (English, Hindi)}
#
dictionary = {
    'title': ('title', 'SaIYa-k'),
    'description': ('description', 'ivavarNa'),
    'teacher': ('teacher', 'AQyaapk'),
    'author': ('author', 'rcanaakar'),
    'uploaded_by': ('uploaded by', 'jamaa krnao vaalao ka naama'),
    'author_unknown': ('author unknown', 'rcanaakar ka naama AnauplabQa'),
    'teacher_author': ('teacher/author', 'AQyaapk À rcanaakar'),
    'file_to_upload': ('file to upload', 'jamaa krnao hotu Ôa[-la'),
    'students_concerned': ('students concerned', 'saMbainQat ivaVaqaI-'),
    'unzip': ('unzip? check this if you are uploading a zip file that must be unziped at the repository to recover the contents of the object.  this is used to upload an object that consists of multiple files or directories. (leave it blank if you don\'t know what this is for.)', 'fix this XXX'),
    'submit_title': ('Submit Content To the Central Repository',
                     'kond`Iya kaoYa maoM saamaga`I jamaa kroM'), #Confirm
    'upload': ('Upload', 'jamaa kroM'),
    'clear_all': ('Clear All', 'saba imaTaeÐ'),
    'leave_blank':("If you're unsure about any fields on this page, leave them blank.", 'fix this XXX'),
    'thumbnail1': ('thumbnail image 1 (recommended use: a small image):',
                   'fix this XXX'),
    'thumbnail2': ('thumbnail image 2 (recommended use: an author picture):',
                   'fix this XXX'),
    'thumbnail3': ('thumbnail image 3 (recommended use: a larger image):',
                   'fix this XXX'),
    'thumbnail4': ('thumbnail image 4 (recommended use: a larger image):',
                   'fix this XXX'),
    'excerpt1': ('excerpt file 1', 'fix this XXX'),
    'excerpt2': ('excerpt file 2', 'fix this XXX'),
    'excerpt3': ('excerpt file 3', 'fix this XXX'),
    'excerpt4': ('excerpt file 4', 'fix this XXX'),
    'subjects': ('subjects (check all that apply)', 'ivaYaya ³jaao laagaU haoM vao saba caunaoM´'),
    'english': ('English', 'Aga`oj,aI'),
    'hindi': ('Hindi', 'ihndI'),
    'sanskrit': ('Sanskrit', 'saMskRt'),
    'science': ('science', 'iva&ana'),
    'physics': ('physics', 'BaaOitk Saas~'),
    'chemistry': ('chemistry', 'rsaayana Saas~'),
    'astronomy': ('astronomy', 'Kgaaola Saas~'),
    'biology': ('biology', 'jaIva iva&ana'),
    'mathematics': ('mathematics', 'gaiNat'),
    'arithmetic': ('arithmetic', 'AMk gaiNat'),
    'algebra': ('algebra', 'baIja gaiNat'),
    'geometry': ('geometry', 'roKa gaiNat'),
    'history': ('history', '[ithasa'),
    'social_studies': ('social studies', 'saamaaijak iva&ana'),
    'home_science': ('home science', 'gaRh iva&ana'),
    'agriculture': ('agriculture', 'kRiYa iva&ana'),
    'general_knowledge': ('general knowledge', 'saamaanya &ana'),
    'food_nutrition': ('food and nutrition', 'Baaojana va paoYaNa'),
    'arts_craft': ('arts and craft and bookcraft', 'hst evaM pustk klaa'),
    'computer_literacy': ('computer literacy', 'kmaPyaUTr iSaxaa'),
    'games': ('games', 'Kola'),
    'stories': ('stories', 'khainayaaÐ'),
    'other_subject': ('other subject (specify)', 'Anya ivaYaya ³]llaoK kroM´'),
    'content_type': ('content type', 'ivaYaya saamaga`I ka p`kar'),
    'unknown': ('unknown', 'A&at'),
    'lecture': ('lecture', 'Aa#yaana'),
    'courseware': ('courseware', 'paz\ya saamaga`I'),
    'communication': ('communication', 'vaata-laap'),
    'chat': ('chat', 'fix: chat'),
    'student_projects': ('student_projects', 'ivaVaqaI-yaaoM kI p`aojao@T'),
    'homework_submission': ('homework_submission', 'kaya- jamaa kroM'),
    'homework_feedback': ('homework_feedback', 'gaRh kaya- saMbainQat iTPpNaI'),
    'questions': ('questions', 'p`Sna'),
    'answers': ('answers', ']<ar'),
    'social_entertainment': ('social_entertainment', 'saamaaijak manaaorMjana'),
    'exam': ('exam', 'prIxaa'),
    'information': ('information', 'saUcanaa'),
    'scratch_space': ('scratch_space', 'fix'),
    'tmp': ('tmp', 'fix'),
    'other': ('other', 'Anya'),
    'language': ('language (check all that apply)', 'BaaYaa ³jaao laagaU haoM vao saba caunaoM´'), #Confirm
    'other_language': ('other language (specify)', 'Anya BaaYaa ³]llaoK kroM´'),
    'for_class': ('for class', 'iksa kxaa hotu'),
    'preschool': ('preschool', 'fix preschool'),
    '0': ('0', '0'),
    '1': ('1', '1'),
    '2': ('2', '2'),
    '3': ('3', '4'),
    '4': ('4', '4'),
    '5': ('5', '5'),
    '6': ('6', '6'),
    '7': ('7', '7'),
    '8': ('8', '8'),
    '9': ('9', '9'),
    '10': ('10', '10'),
    '11': ('11', '11'),
    '12': ('12', '12'),
    '13': ('13', '13'),
    '14': ('14', '14'),
    '15': ('15', '15'),
    '16': ('16', '16'),
    '17': ('17', '17'),
    'college': ('college', 'fix college'),
    'applicable_age': ('applicable age', 'fix this'),
    'from': ('from', 'fix'),
    'to': ('to', 'fix'),
    'media_type': ('media type (check all that apply)', 'fix this XXX'),
    'video': ('video', 'fix'),
    'recorded_plextor': ('recorded by Plextor', 'fix this XXX'),
    'recorded_webcam': ('recorded by webcam', 'fix this XXX'),
    'recorded_camstudio': ('recorded by camstudio', 'fix this XXX'),
    'audio_no_video': ('audio (without video)', 'fix this XXX'),
    'images': ('images', 'fix'),
    'documents': ('documents', 'fix'),
    'other_type': ('other type (specify)', 'fix this (XXX)'),
    'video_resolution': ('video resolution (width in pixels)', 'fix this'),
    'content_duration': ('content duration', 'fix this'),
    'hours': ('hours', 'fix'),
    'minutes': ('minutes', 'fix')    
}



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

    

def size_html(hindiTxt, size):
    size = str(size)
    return HINDI_FONT_ATTR + 'SIZE=' + size + '>' + hindiTxt + '</FONT>'



def size4_bold_html(englishKey):
    hindi = dictionary[englishKey][1]
    return '<B>' + size_html(hindi, 4) + '</B>'



def size4_html(englishKey):
    hindi = dictionary[englishKey][1]
    return size_html(hindi, 4)



def size3_html_key(englishKey):
    hindi = dictionary[englishKey][1]
    return size_html(hindi, 3)



def html_key(englishKey):
    hindi = dictionary[englishKey][1]
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



def dict_hindi(keys):
    dict = {}
    for key in keys:
        dict['trans_' + key] = dictionary[key][1]
    dict['trans_txt_style'] = HINDI_TEXT_ATTR
    return dict



def replace_hindi_plain_and_html(str, keys1, keys2):
    dict1 = dict_size4_hindi_html(keys1)
    dict2 = dict_hindi(keys2)
    dict1.update(dict2)
    return str % dict1
