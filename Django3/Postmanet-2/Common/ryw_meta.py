import sys, os, shutil
import su
import pickle
import logging
import cgi
import ryw, SearchFile, ryw_view, ryw_hindi, ryw_upload, ryw_customize
import objectstore
import ryw_upload
import urllib
import datetime



editableKeys = ['title', 'description', 'author_name', 'uploaded_by_name',
                'uploaded_by_site',
                'students', 'content_alias', 'related_content',
                'chapter_number']
transWords = ['title', 'description', 'teacher', 'author', 'uploaded_by',
              'students_concerned', 'content_alias', 'related_content',
              'uploaded_by_site', 'data_size', 'date_and_time',
              'chapter_number']



def open_search_file(RepositoryRoot, grabWriteLock = True, skipLock = False):
    success,searchFile = ryw.open_search_file(
        'ryw_meta.open_search_file:',
        os.path.join(RepositoryRoot, 'WWW', 'logs'),
        'upload.log',
        os.path.join(RepositoryRoot, 'SearchFile'),
        grabWriteLock,
        skipLk = skipLock)
    if not success:
        ryw.give_bad_news(
            'DeleteObject.open_search_file: failed to open search file.',
            logging.critical)
        return None

    return searchFile
    

    
def get_meta(searchFile, objID, version, repositoryRoot):
    success,meta = searchFile.get_meta(objID, version)
    if success:
        #
        # I'm doing this to hardwire all
        # places of gettting objectstoreroot.
        #
        #return (meta, meta['objectstore'])
        return (meta, ryw.hard_wired_objectstore_root())
    
    logging.warning(
        'ryw_meta.get_meta: not finding it in the SearchFile: ' +
        objID + ' # ' + str(version) + ', but attempting to continue')
    
    #
    # look for the hardwired objectstore root.  not nice but...
    #
    objroot = os.path.join(repositoryRoot, 'WWW', 'ObjectStore')
    if not os.path.exists(objroot):
        ryw.give_bad_news(
            'DeleteObject.get_meta: even the hardwired root does not exist: '+
            objroot, logging.critical)
        return (None, None)
    
    success,meta = ryw.get_meta(objroot, objID, version)
    if not success:
        logging.warning(
            'ryw.get_meta: failed to read metadata from objstore: '+
            objID + ' # ' + str(version))
        return (None, objroot)

    return (meta, objroot)



def get_meta2(repositoryRoot, objID, version, skipLk = False):

    searchFile = open_search_file(repositoryRoot, grabWriteLock = False,
                                  skipLock = skipLk)
    if not searchFile:
        return (False, None, None)

    meta,objroot = get_meta(searchFile, objID, version, repositoryRoot)
    if not meta or not objroot:
        logging.warning('get_meta2: no meta or no objroot, giving up...')
        searchFile.done()
        return (False, None, None)

    searchFile.done()
    return (True, meta, objroot)
    


def scrub_string_value(str):
    str = str.replace('"', '&quot;')
    return str

    

def show_meta_edit_page(meta, editScriptName, objstr,
                        titleStr="Edit Existing Content Information"):
    """called by both ShowObject.py and CloneVersion_form.py"""

    #######################################################################
    # the following is just the html page for editing meta data.
    #######################################################################
    
    page = """
<HTML>
<HEAD>
<TITLE>%(titleStr)s</TITLE>
</HEAD>

<BODY>

%(begin_java_script)s

<CENTER>
<A HREF="/index.html">
<IMG SRC="%(smallLogoFileName)s" BORDER=0 %(smallLogoDimension)s></A>
<BR>

<H3>%(titleStr)s</H3>

If you're unsure about any fields on this page, leave them unchanged.
<P>

<TABLE BORDER=0 WIDTH=800><TR><TD>

<FORM ACTION="%(script_name)s" METHOD="post"
ENCTYPE="multipart/form-data">

<CENTER>
<INPUT TYPE="submit" VALUE="Update">
</CENTER>
<P>
<BR>

<B><I>required fields:</I></B>
<P>

<TABLE BORDER=0>
<TR><TD WIDTH=1></TD>
<TD>

<UL>
<LI>
<U>title</U>:
<INPUT TYPE="TEXT" NAME="title" SIZE=80 VALUE="%(title)s">
<P>

%(trans_title)s:
<INPUT TYPE="TEXT" NAME="hindi_title" SIZE=80 VALUE="%(hindi_title)s"
%(trans_txt_style)s>
<P>


</UL>

</TD>
</TR>
</TABLE>

<BR>


<B><I>optional fields:</I></B>
<P>


<TABLE BORDER=0>
<TR><TD WIDTH=1></TD>
<TD>

<UL>

<LI>
<U>description:</U><BR>
<TEXTAREA NAME="description" ROWS=5 COLS=70>%(description)s</TEXTAREA>
<P>

%(trans_description)s:<BR>
<TEXTAREA NAME="hindi_description" ROWS=5 COLS=70 %(trans_txt_style)s>%(hindi_description)s</TEXTAREA>
<P>


<LI>
<U>file directories</U>:&nbsp;&nbsp;
%(file_directories)s
<P>

<LI>
<U>media attributes</U>:&nbsp;&nbsp;
re-extract
<INPUT type=checkbox name=med_reext CHECKED>
<P>


<LI>
<U>students concerned</U>:
<INPUT TYPE="TEXT" NAME="students" SIZE=80 VALUE="%(students)s">
<P>

%(trans_students_concerned)s:
<INPUT TYPE="TEXT" NAME="hindi_students" SIZE=80 VALUE="%(hindi_students)s"
%(trans_txt_style)s>
<P>





<LI>
<U>subjects</U> (check all that apply) [%(trans_subjects)s]:

English [%(trans_english)s]
<INPUT type=checkbox name=subjects value=English %(subject_English_value)s>,

Hindi [%(trans_hindi)s]
<INPUT type=checkbox name=subjects value=Hindi %(subject_Hindi_value)s>,

Sanskrit [%(trans_sanskrit)s]
<INPUT type=checkbox name=subjects value=Sanskrit %(subject_Sanskrit_value)s>,

science [%(trans_science)s]
<INPUT type=checkbox name=subjects value=science %(subject_science_value)s>

(
physics [%(trans_physics)s]
<INPUT type=checkbox name=subjects value=physics %(subject_physics_value)s>,

chemistry [%(trans_chemistry)s]
<INPUT type=checkbox name=subjects value=chemistry
%(subject_chemistry_value)s>,

astronomy [%(trans_astronomy)s]
<INPUT type=checkbox name=subjects value=astronomy
%(subject_astronomy_value)s>,

biology [%(trans_biology)s]
<INPUT type=checkbox name=subjects value=biology
%(subject_biology_value)s>
),

geology [%(trans_geology)s]
<INPUT type=checkbox name=subjects value=geology
%(subject_geology_value)s>
),

mathematics [%(trans_mathematics)s]
<INPUT type=checkbox name=subjects value=mathematics
%(subject_mathematics_value)s>

(
arithmetic [%(trans_arithmetic)s]
<INPUT type=checkbox name=subjects value=arithmetic
%(subject_arithmetic_value)s>,

algebra [%(trans_algebra)s]
<INPUT type=checkbox name=subjects value=algebra
%(subject_algebra_value)s>,

geometry [%(trans_geometry)s]
<INPUT type=checkbox name=subjects value=geometry
%(subject_geometry_value)s>
),

history [%(trans_history)s]
<INPUT type=checkbox name=subjects value=history
%(subject_history_value)s>,

social studies [%(trans_social_studies)s]
<INPUT type=checkbox name=subjects value="social_studies"
%(subject_social_studies_value)s>,

home science [%(trans_home_science)s]
<INPUT type=checkbox name=subjects value="home_science"
%(subject_home_science_value)s>,

agriculture [%(trans_agriculture)s]
<INPUT type=checkbox name=subjects value=agriculture
%(subject_agriculture_value)s>,

commerce [%(trans_commerce)s]
<INPUT type=checkbox name=subjects value=commerce
%(subject_commerce_value)s>,

culture and customs [%(trans_culture_and_customs)s]
<INPUT type=checkbox name=subjects value="culture_and_customs"
%(subject_culture_and_customs_value)s>,

general knowledge [%(trans_general_knowledge)s]
<INPUT type=checkbox name=subjects value="general_knowledge"
%(subject_general_knowledge_value)s>,

food and nutrition [%(trans_food_and_nutrition)s]
<INPUT type=checkbox name=subjects value="food_and_nutrition"
%(subject_food_and_nutrition_value)s>,

arts and crafts [%(trans_arts_and_crafts)s]
<INPUT type=checkbox name=subjects value="arts_and_crafts"
%(subject_arts_and_crafts_value)s>,

computer literacy [%(trans_computer_literacy)s]
<INPUT type=checkbox name=subjects value="computer_literacy"
%(subject_computer_literacy_value)s>,

games [%(trans_games)s]
<INPUT type=checkbox name=subjects value="games"
%(subject_games_value)s>,

stories [%(trans_stories)s]
<INPUT type=checkbox name=subjects value="stories"
%(subject_stories_value)s>,

plays [%(trans_plays)s]
<INPUT type=checkbox name=subjects value="plays"
%(subject_plays_value)s>,

with vocabulary [%(trans_with_vocabulary)s]
<INPUT type=checkbox name=subjects value="with_vocabulary"
%(subject_with_vocabulary_value)s>,

environmental science [%(trans_environmental_science)s]
<INPUT type=checkbox name=subjects value="environmental_science"
%(subject_environmental_science_value)s>,

health care [%(trans_health_care)s]
<INPUT type=checkbox name=subjects value="health_care"
%(subject_health_care_value)s>

(nursing [%(trans_nursing)s]
<INPUT type=checkbox name=subjects value="nursing"
%(subject_nursing_value)s>,

reproductive health [%(trans_reproductive_health)s]
<INPUT type=checkbox name=subjects value="reproductive_health"
%(subject_reproductive_health_value)s>,

children health [%(trans_children_health)s]
<INPUT type=checkbox name=subjects value="children_health"
%(subject_children_health_value)s>),

women rights [%(trans_women_rights)s]
<INPUT type=checkbox name=subjects value="women_rights"
%(subject_women_rights_value)s>,

Kannada [%(trans_kannada)s]
<INPUT type=checkbox name=subjects value="Kannada"
%(subject_Kannada_value)s>,

Tamil [%(trans_tamil)s]
<INPUT type=checkbox name=subjects value="Tamil"
%(subject_Tamil_value)s>,

Bengali [%(trans_bengali)s]
<INPUT type=checkbox name=subjects value="Bengali"
%(subject_Bengali_value)s>,

Marathi [%(trans_marathi)s]
<INPUT type=checkbox name=subjects value="Marathi"
%(subject_Marathi_value)s>,

Punjabi [%(trans_punjabi)s]
<INPUT type=checkbox name=subjects value="Punjabi"
%(subject_Punjabi_value)s>,

Urdu [%(trans_urdu)s]
<INPUT type=checkbox name=subjects value="Urdu"
%(subject_Urdu_value)s>,

Nepali [%(trans_nepali)s]
<INPUT type=checkbox name=subjects value="Nepali"
%(subject_Nepali_value)s>,

children program [%(trans_children_program)s]
<INPUT type=checkbox name=subjects value="children_program"
%(subject_children_program_value)s>,

other subject (specify):
<INPUT TYPE="TEXT" NAME="subject_other" SIZE=20
VALUE="%(subject_other_value)s">

&nbsp;&nbsp;

%(trans_other_subject)s:
<INPUT TYPE="TEXT" NAME="subject_other_hindi" SIZE=20 %(trans_txt_style)s
VALUE="%(hindi_subject_other_value)s">
<P>




<LI>
<U>content type</U>:
<SELECT NAME="content_type">
%(content_type_options)s
</SELECT>

&nbsp;&nbsp;&nbsp;

%(trans_content_type)s:
<SELECT NAME="hindi_content_type" %(trans_txt_style)s>
%(hindi_content_type_options)s
</SELECT>
<P>





<LI>
<U>language</U> (check all that apply) [%(trans_language)s]:
English [%(trans_english)s]
<INPUT type=checkbox name=languages value=English
%(language_English_value)s>,

Hindi [%(trans_hindi)s]
<INPUT type=checkbox name=languages value=Hindi
%(language_Hindi_value)s>,

Kannada [%(trans_kannada)s]
<INPUT type=checkbox name=languages value=Kannada
%(language_Kannada_value)s>,

Tamil [%(trans_tamil)s]
<INPUT type=checkbox name=languages value=Tamil
%(language_Tamil_value)s>,

Bengali [%(trans_bengali)s]
<INPUT type=checkbox name=languages value=Bengali
%(language_Bengali_value)s>,

Marathi [%(trans_marathi)s]
<INPUT type=checkbox name=languages value=Marathi
%(language_Marathi_value)s>,

Punjabi [%(trans_punjabi)s]
<INPUT type=checkbox name=languages value=Punjabi
%(language_Punjabi_value)s>,

Nepali [%(trans_nepali)s]
<INPUT type=checkbox name=languages value=Nepali
%(language_Nepali_value)s>,

Telegu [%(trans_telegu)s]
<INPUT type=checkbox name=languages value=Telegu
%(language_Telegu_value)s>,

Gujarati [%(trans_gujarati)s]
<INPUT type=checkbox name=languages value=Gujarati
%(language_Gujarati_value)s>,

Kashmiri [%(trans_kashmiri)s]
<INPUT type=checkbox name=languages value=Kashmiri
%(language_Kashmiri_value)s>,

other language (specify):
<INPUT TYPE="TEXT" NAME="language_other" SIZE="20"
VALUE="%(language_other_value)s">

&nbsp;&nbsp;

%(trans_other_language)s:
<INPUT TYPE="TEXT" NAME="language_other_hindi" SIZE="20" %(trans_txt_style)s
VALUE="%(hindi_language_other_value)s">
<P>




<LI>
<U>for class</U>:
<SELECT NAME="class">
%(class_options)s
</SELECT>

&nbsp;&nbsp;

%(trans_for_class)s:
<SELECT NAME="hindi_class" %(trans_txt_style)s>
%(hindi_class_options)s
</SELECT>
<P>






<LI>
<U>applicable age</U>: 
from
<SELECT NAME="age_from">
%(age_from_options)s
</SELECT>
to
<SELECT NAME="age_to">
%(age_to_options)s
</SELECT>
<P>

%(trans_applicable_age)s: 
%(trans_from)s
<SELECT NAME="hindi_age_from" %(trans_txt_style)s>
%(hindi_age_from_options)s
</SELECT>
%(trans_to)s
<SELECT NAME="hindi_age_to" %(trans_txt_style)s>
%(hindi_age_to_options)s
</SELECT>
<P>






<LI>
<U>media type</U> (check all that apply) [%(trans_media_type)s]:
video [%(trans_video)s] <INPUT type=checkbox name=media value=video
%(media_video_value)s>,

(DVD <INPUT type=checkbox name=media value=DVD %(media_DVD_value)s>,

VCD <INPUT type=checkbox name=media value=VCD %(media_VCD_value)s>,

extracted by firewire [%(trans_extracted_by_firewire)s]
<INPUT type=checkbox name=media value="extracted_by_firewire"
%(media_extracted_by_firewire_value)s>,

recorded by Plextor [%(trans_recorded_by_Plextor)s]
<INPUT type=checkbox name=media value="recorded_by_Plextor"
%(media_recorded_by_Plextor_value)s>,

recorded from TV [%(trans_recorded_from_TV)s]
<INPUT type=checkbox name=media value="recorded_from_TV"
%(media_recorded_from_TV_value)s>,

from YouTube [%(trans_from_YouTube)s]
<INPUT type=checkbox name=media value="from_YouTube"
%(media_from_YouTube_value)s>,

VHS tape digitized [%(trans_VHS_tape_digitized)s]
<INPUT type=checkbox name=media value="VHS_tape_digitized"
%(media_VHS_tape_digitized_value)s>,

recorded by webcam [%(trans_recorded_by_webcam)s]
<INPUT type=checkbox name=media value="recorded_by_webcam"
%(media_recorded_by_webcam_value)s>,

recorded by Mustek [%(trans_recorded_by_Mustek)s]
<INPUT type=checkbox name=media value="recorded_by_Mustek"
%(media_recorded_by_Mustek_value)s>,

recorded by Aiptek [%(trans_recorded_by_Aiptek)s]
<INPUT type=checkbox name=media value="recorded_by_Aiptek"
%(media_recorded_by_Aiptek_value)s>,

recorded by CamStudio [%(trans_recorded_by_CamStudio)s]
<INPUT type=checkbox name=media value="recorded_by_CamStudio"
%(media_recorded_by_CamStudio_value)s>,

created by ProShow [%(trans_created_by_ProShow)s]
<INPUT type=checkbox name=media value="created_by_ProShow"
%(media_created_by_ProShow_value)s>,

has subtitle [%(trans_has_subtitle)s]
<INPUT type=checkbox name=media value="has_subtitle"
%(media_has_subtitle_value)s>,

SMIL <INPUT type=checkbox name=media value=SMIL %(media_SMIL_value)s)>,

audio without video [%(trans_audio_without_video)s]
<INPUT type=checkbox name=media value="audio_without_video"
%(media_audio_without_video_value)s>,

Flash <INPUT type=checkbox name=media value=Flash %(media_Flash_value)s>,

images <INPUT type=checkbox name=media value=images %(media_images_value)s>,

powerpoint <INPUT type=checkbox name=media value=powerpoint
%(media_powerpoint_value)s>

documents [%(trans_documents)s]
<INPUT type=checkbox name=media value=documents %(media_documents_value)s>,

executables [%(trans_executables)s]
<INPUT type=checkbox name=media value=executables %(media_executables_value)s>,

slideshows [%(trans_slideshows)s]
<INPUT type=checkbox name=media value=slideshows %(media_slideshows_value)s>,

other type (specify):
<INPUT TYPE="TEXT" NAME="media_other" SIZE="20"
VALUE="%(media_other_value)s">
&nbsp;&nbsp;
%(trans_other_type)s:
<INPUT TYPE="TEXT" NAME="media_other_hindi" SIZE=20 %(trans_txt_style)s
VALUE="%(hindi_media_other_value)s">
<P>







<LI>
<U>video resolution</U> (width in pixels)
[%(trans_video_resolution)s]:
<SELECT NAME="video_resolution">
%(video_resolution_options)s
</SELECT>
<P>






<LI>
<U>content duration</U> [%(trans_content_duration)s]:

hours [%(trans_hours)s]
<SELECT NAME="time_length_hours">
%(time_length_hours_options)s
</SELECT>

minutes [%(trans_minutes)s]
<SELECT NAME="time_length_minutes">
%(time_length_minutes_options)s
</SELECT>

seconds [%(trans_seconds)s]
<SELECT NAME="time_length_seconds">
%(time_length_seconds_options)s
</SELECT>
<P>



<LI>
<U>data size</U> [%(trans_data_size)s]:
<INPUT TYPE="TEXT" NAME="size_text" SIZE="6" VALUE="%(size_text)s">
<SELECT NAME="size_unit">
%(data_size_options)s
</SELECT>
<P>





<LI>
<U>content alias</U> (9-character code) [%(trans_content_alias)s]:
<INPUT TYPE="TEXT" NAME="content_alias" SIZE="20" VALUE="%(content_alias)s">
<P>

<LI>
<U>chapter number</U> [%(trans_chapter_number)s]:
<INPUT TYPE="TEXT" NAME="chapter_number" SIZE="10" VALUE="%(chapter_number)s">
<P>

<LI>
<U>related content</U> [%(trans_related_content)s]:
<INPUT TYPE="TEXT" NAME="related_content" SIZE="40" VALUE="%(related_content)s">
<P>

<LI>
<U>show</U> [%(trans_show)s]:
copyrighted [%(trans_copyrighted)s]
<INPUT type=checkbox name=show value=copyrighted
%(show_copyrighted_value)s>,

discreet [%(trans_discreet)s]
<INPUT type=checkbox name=show value=discreet
%(show_discreet_value)s>
<P>

<LI>
<U>cache</U> [%(trans_cache)s]:
sticky [%(trans_sticky)s]
<INPUT type=checkbox name=cache value=sticky
%(cache_sticky_value)s>
<P>

<LI>
<U>teacher/author</U> (person name):<INPUT TYPE="TEXT" NAME="author_name" SIZE="40" VALUE="%(author_name)s">
<P>

%(trans_teacher)s
<FONT SIZE=4><B>/</B></FONT>
%(trans_author)s:
<INPUT TYPE="TEXT" NAME="hindi_author_name" SIZE="40"
VALUE="%(hindi_author_name)s"
%(trans_txt_style)s>
<P>

<LI>
<U>uploaded by</U> (person name):<INPUT TYPE="TEXT" NAME="uploaded_by_name" SIZE="40" VALUE="%(uploaded_by_name)s">
<P>

<!-- Hindi field temporarily commented out
%(trans_uploaded_by)s:
<INPUT TYPE="TEXT" NAME="hindi_uploaded_by_name" SIZE="40"
VALUE="%(hindi_uploaded_by_name)s" %(trans_txt_style)s>
<P>
-->

<LI>
<U>uploaded by</U> (site name):<INPUT TYPE="TEXT" NAME="uploaded_by_site" SIZE="40" VALUE="%(uploaded_by_site)s">
<P>


<!-- Hindi field temporarily commented out
%(trans_uploaded_by_site)s:
<INPUT TYPE="TEXT" NAME="hindi_uploaded_by_site" SIZE="40"
VALUE="%(hindi_uploaded_by_site)s" %(trans_txt_style)s>
<P>
-->



<LI>
<U>date and time</U> %(trans_date_and_time)s:
<INPUT TYPE="TEXT" NAME="uploaded_date_time" SIZE="14"
VALUE="%(uploaded_date_time_val)s">
<P>





</UL>

</TD>
</TR>
</TABLE>

<INPUT TYPE="hidden" NAME="objstr" VALUE="%(objstr)s">


<CENTER>
<INPUT TYPE="submit" VALUE="Update">
</CENTER>

</FORM>

</TD></TR></TABLE>

</CENTER>

<BR>

<HR WIDTH=75%%>

%(uploadFooter)s

<HR WIDTH=75%%>

</BODY>
</HTML>
"""

    #######################################################################
    # end of html page for editing meta data.
    #######################################################################

    ryw.print_header()
    dict = ryw_customize.dict
    dict['titleStr'] = titleStr
    dict['begin_java_script'] = ryw_view.begin_print_str()
    dict['script_name'] = editScriptName
    dict['objstr'] = objstr
    dict['year'] = ryw.get_year()

    if meta.has_key('creator') and meta['creator']:
        meta['uploaded_by_site'] = meta['creator']


    #
    # deal with data size.
    #
    make_data_size(meta, dict)

    #
    # deal with English fields.
    #
    for key in editableKeys:
        if meta.has_key(key):
            dict[key] = scrub_string_value(meta[key])
        else:
            dict[key] = ''

    #
    # deal with Hindi field labels. 
    # (may deal with different set of things to iterate over in the future.)
    #
    for key in transWords:
        dict['trans_' + key] = ryw_hindi.size4_html(key)
    dict['trans_txt_style'] = ryw_hindi.HINDI_TEXT_ATTR
        
    #
    # deal with Hindi field values.
    # (may deal with different set of things to iterate over in the future.)
    #
    for key in editableKeys:
        formStr = 'hindi_' + key
        dict[formStr] = ''
        if not meta.has_key('hindi'):
            continue
        hindi = meta['hindi']
        if hindi.has_key(key):
            dict[formStr] = scrub_string_value(hindi[key])

    #
    # deal with subjects
    #
    make_form_checkboxes(meta,
                         ['subjects', 'english', 'hindi',
                          'sanskrit', 'science', 'physics', 'chemistry',
                          'astronomy', 'biology', 'geology',
                          'mathematics', 'arithmetic',
                          'algebra', 'geometry', 'history', 'social_studies',
                          'home_science', 'agriculture', 'commerce',
                          'culture_and_customs',
                          'general_knowledge',
                          'food_and_nutrition', 'arts_and_crafts',
                          'computer_literacy',
                          'games', 'stories', 'plays', 'with_vocabulary',
                          'environmental_science',
                          'health_care',
                          'nursing', 
                          'reproductive_health',
                          'children_health',
                          'women_rights',
                          'children_program',
                          'kannada', 'tamil',
                          'bengali', 'marathi', 'punjabi', 'urdu', 'nepali',
                          'other_subject'],
                         'subjects',
                         ryw_upload.POSSIBLE_SUBJECTS, 'subject', dict)

    #
    # deal with content type
    #
    make_form_dropdown(meta, ['content_type'], 'content_type', 
                       ryw_upload.POSSIBLE_CONTENT_TYPES, dict)

    #
    # deal with language checkboxes
    #
    make_form_checkboxes(meta,
                         ['language', 'english', 'hindi', 'kannada',
                          'tamil', 'bengali', 'marathi', 'punjabi', 'urdu',
                          'nepali',
                          'telegu', 'gujarati', 'kashmiri', 
                          'other_language'],
                         'languages',
                         ryw_upload.POSSIBLE_LANGUAGES, 'language', dict)

    #
    # deal with show or no show checkboxes
    #
    make_form_checkboxes(meta,
                         ['show', 'copyrighted', 'discreet'], 'show',
                         ryw_upload.POSSIBLE_SHOW, 'show', dict)

    #
    # deal with cache sticky checkbox
    #
    make_form_checkboxes(meta,
                         ['cache', 'sticky'], 'cache',
                         ryw_upload.POSSIBLE_CACHE, 'cache', dict)

    #
    # deal with class
    #
    make_form_dropdown(meta, ['for_class'], 'class',
                       ryw_upload.POSSIBLE_CLASSES, dict)

    #
    # deal with applicable age
    #
    make_bracket_dropdowns(meta, ['applicable_age', 'from', 'to'], 'age',
                           'age_from', 'age_to',
                           ryw_upload.POSSIBLE_AGES, ryw_upload.POSSIBLE_AGES,
                           dict)

    #
    # deal with media type
    #
    make_form_checkboxes(meta,
                         ['media_type', 'video', 'other_type',
                          'extracted_by_firewire',
                          'recorded_by_Plextor',
                          'recorded_from_TV',
                          'from_YouTube',
                          'VHS_tape_digitized',
                          'recorded_by_webcam',
                          'recorded_by_Mustek', 'recorded_by_CamStudio',
                          'recorded_by_Aiptek',
                          'created_by_ProShow', 'has_subtitle',
                          'audio_without_video', 'images',
                          'documents', 'executables',
                          'slideshows'],
                         'media',
                         ryw_upload.POSSIBLE_MEDIA, 'media', dict)

    #
    # deal with video resolution
    #
    make_form_dropdown(meta, ['video_resolution'], 'video_resolution',
                       ryw_upload.POSSIBLE_VIDEO_RESOLUTION, dict,
                       noHindi = True)

    #
    # deal with content duration
    #
    make_bracket_dropdowns(meta, ['content_duration', 'hours', 'minutes'],
                           'time_length',
                           'time_length_hours', 'time_length_minutes',
                           ryw_upload.POSSIBLE_HOURS,
                           ryw_upload.POSSIBLE_MINUTES, dict, noHindi=True)

    #
    # deal with new seconds field
    #
    make_form_dropdown(meta, ['seconds'], 'time_length_seconds',
                       ryw_upload.POSSIBLE_SECONDS, dict,
                       noHindi = True)

    #
    # deal with file directories
    #
    dict['file_directories'] = make_dir_strs(meta)

    #
    # deal with upload time
    #
    dict['uploaded_date_time_val'] = make_date_time_val(meta)


    #
    # get rid of empty brackets left behind by untranslated Hindi strings.
    #
    page = page % dict
    page = page.replace('[<FONT FACE=Kundli COLOR=blue SIZE=4></FONT>]','')
       
    print page



def make_date_time_val(meta):
    if not meta.has_key('upload_datetime'):
        logging.debug('make_date_time_val: error: no dateTime val: ')
        return ''
    dateTimeStr = meta['upload_datetime']

    try:
        dateTime = eval(dateTimeStr)
    except:
        logging.debug('make_date_time_val: error: bad dateTime val: ' +
                      dateTimeStr)
        return ''

    result = dateTime.strftime(ryw.uploadDateTimeFormat)
    return ryw.chop_datetime_leading_zeros(result)



def make_data_size(meta, dict):
    dict['size_text'] = ''
    dict['data_size_options'] = """
<OPTION SELECTED>MB
<OPTION>KB
<OPTION>B
"""    
    
    if not meta.has_key('bytes'):
        ryw.give_bad_news('make_data_size: no bytes field found.',
                          logging.critical)
        return

    bytes = meta['bytes']
    if bytes < 1024:
        displayNum = bytes
        unit = 'B'
    elif bytes < 1024 * 1024:
        displayNum = bytes / 1024
        unit = 'KB'
    else:
        displayNum = bytes/ 1024 / 1024
        unit = 'MB'

    optStr,hindiStr = make_options_strings(ryw_upload.POSSIBLE_SIZE_UNIT,
                                           unit, noHindi=True)

    dict['size_text'] = str(displayNum)
    dict['data_size_options'] = optStr




##################################################
# the following has to do with the file directories
##################################################



def make_dir_strs(meta):
    try:
        pdrive = False
        sAddr = os.environ['SERVER_ADDR']
        rAddr = os.environ['REMOTE_ADDR'] 
        if sAddr != rAddr:
            if not ryw.same_subnet(sAddr, rAddr):
                #
                # remote user: no mucking with directories.
                #
                return '(editing currently disabled for remote user.)'
            pdrive = True

        #
        # it was a mistake
        # just disable it.
        #
        pdrive = False

        #
        # make the thumbnail strings.
        #
        success,dataURL,auxiURL,auxiDir = ryw_view.get_server_URLs(meta)
        thumbURLs = ryw_view.get_thumb_URLs(meta, auxiURL, auxiDir)

        smallThumb1URL = thumbURLs[0]
        bigThumb1URL   = thumbURLs[3]

        thumb1Str = make_thumb_string(bigThumb1URL, smallThumb1URL,
                                      'thumbnail 1', pdrive=pdrive)

        smallThumb2URL = thumbURLs[1]
        bigThumb2URL   = thumbURLs[2]

        thumb2Str = make_thumb_string(bigThumb2URL, smallThumb2URL,
                                      'thumbnail 2', pdrive=pdrive)

        if thumb1Str == '' and thumb2Str == '':
            #
            # no thumbnail strings were found.
            # put in the strings that would allow addition of new thumbnails.
            #
            thumb1Str = make_new_thumb_string(
                meta, auxiDir,
                'Do you want to add thumbnails?',
                'add new thumbnails',
                '/cgi-bin/CreateNewThumbDir.py?objstr=%(objstr)s')
            
        #
        # make data folder string.
        #
        dataStr = make_dir_string(dataURL, '/icons/folder.open.gif', 'data')

        #
        # make excerpt string.
        #
        excerptStr = make_excerpt_string(auxiURL, auxiDir)

        if excerptStr == '':
            #
            # no excerpt string was found.
            # put in the string that would allow addition of new excerpts.
            #
            excerptStr = make_new_thumb_string(
                meta, auxiDir,
                'Do you want to add excerpt files?',
                'add new excerpt files',
                '/cgi-bin/CreateNewExcerptDir.py?objstr=%(objstr)s')

        #
        # make the cut-and-paste string for the P drive.
        #
        pDriveStr = ryw_view.make_explorer_lan_popup_string(dataURL)

        result = ''
        for str in [thumb1Str, thumb2Str, dataStr, excerptStr, pDriveStr]:
            if not str:
                continue
            result = result + ' &nbsp;&nbsp; ' + str

        return result
    except:
        ryw.give_bad_news('make_dir_strs: bad stuff happened, meta: ' +
                          repr(meta), logging.critical)
        return ''



def make_new_thumb_string(meta, auxiDir, message, title, script):
    notUsedString = """
<IMG SRC="/icons/trash.gif" BORDER=0 title="add new thumbnails"
onmouseover="this.style.cursor='pointer';"
onClick='createNewThumb("%(objstr)s")'>"""


    newThumbStr = """
<A HREF="%(url)s" %(popup)s>
<IMG SRC="/icons/folder_gray.gif" BORDER=0 title="%(title)s"></A>"""

    urlStr = script
    d2 = {}
    objStr = urllib.quote(meta['id'] + '#' + str(meta['version']))
    d2['objstr'] = objStr
    url = urlStr % d2
    
    dict = {}
    dict['url'] = url
    dict['popup'] = ryw_view.make_confirmed_popup_string(url,
                                                         message,
                                                         defaultSize=(400,300))
    dict['title'] = title
    logging.debug('make_new_thumb_string: answer is: ' + newThumbStr % dict)
    return newThumbStr % dict



def make_thumb_string(bigThumbURL, smallThumbURL, name, pdrive=False):
    if not bigThumbURL:
        return ''

    bigThumbURL = bigThumbURL + '/../'

    thumbStr = """
<A HREF="%(thumb_url)s" %(popup)s>%(anchor)s</A>
"""
    
    dict = {}
    dict['thumb_url'] = bigThumbURL
    dict['popup'] = ryw_view.make_explorer_popup_string(
        bigThumbURL, (ryw_view.POPUP_DIR_WIDTH, ryw_view.POPUP_DIR_HEIGHT),
        pdrive = pdrive)
    
    if smallThumbURL:
        imgAnchorStr = """
<IMG SRC="%(small_thumb_url)s" BORDER=0 TITLE="%(thumb_name)s">"""
        d2 = {}
        d2['thumb_name'] = name
        d2['small_thumb_url'] = smallThumbURL
        dict['anchor'] = imgAnchorStr % d2
    else:
        dict['anchor'] = name
        
    return thumbStr % dict



def make_excerpt_string(auxiURL, auxiDir):
    subDir = ryw_view.excerpt_exists(auxiURL, auxiDir)
    if not subDir:
        return ''
    return ryw_view.make_excerpt_icon_str(subDir, auxiURL, auxiDir)



def make_dir_string(dURL, iconName, name):
    if not dURL:
        return ''


    #isLan = ryw.is_lan()
    isLan = False

    dStr = """<A HREF="%(d_url)s" %(popup)s>%(anchor)s</A>"""

    dict = {}
    dict['d_url'] = dURL
    dict['popup'] = ryw_view.make_explorer_popup_string(
        dURL, (ryw_view.POPUP_DIR_WIDTH, ryw_view.POPUP_DIR_HEIGHT),
        pdrive=isLan)

    iconImgStr = """
<IMG SRC="%(icon_name)s" BORDER=0 TITLE="%(title_name)s">"""
    d2 = {}

    if isLan:
        d2['icon_name'] = '/icons/p_folder.open.gif'
    else:
        d2['icon_name'] = iconName
    d2['title_name'] = name

    dict['anchor'] = iconImgStr % d2

    return dStr % dict

    
                                                        
##################################################
# the above has to do with the file directories
##################################################



def make_bracket_dropdowns(meta, transWords, categoryName, key1, key2,
                           possibilities1, possibilities2, dict,
                           noHindi=False):
    dict1 = ryw_hindi.dict_size4_hindi_html(transWords)
    dict.update(dict1)

    val1,val2 = ['unknown', 'unknown']
    if meta.has_key(categoryName):
        try:
            val1,val2 = meta[categoryName]
        except:
            val1,val2 = ['unknown', 'unknown']

    optStr1,hindiOptStr1 = make_options_strings(possibilities1, val1,
                                                noHindi=noHindi)
    optStr2,hindiOptStr2 = make_options_strings(possibilities2, val2,
                                                noHindi=noHindi)

    #
    # replace %(age_from_options)s
    # and %(hindi_age_from_options)s
    #
    dict[key1 + '_options'] = optStr1
    dict[key2 + '_options'] = optStr2
    if not noHindi:
        dict['hindi_' + key1 + '_options'] = hindiOptStr1
        dict['hindi_' + key2 + '_options'] = hindiOptStr2
    


def make_options_strings(possibilities, value, noHindi=False):        
    optionString = ''
    hindiOptionString = ''
    for poss in possibilities:
        if value == poss:
            thisOpt = '<OPTION SELECTED>'
        else:
            thisOpt = '<OPTION>'
        thisLine = thisOpt + poss + '\n'
        optionString += thisLine
        if not noHindi:
            thisHindiLine = thisOpt + ryw_hindi.dict_hindi1(poss) + '\n'
            hindiOptionString += thisHindiLine
    return [optionString, hindiOptionString]    



def make_form_dropdown(meta, transWords, categoryName, possibilities, dict,
                       noHindi=False):
    dict1 = ryw_hindi.dict_size4_hindi_html(transWords)
    dict.update(dict1)

    value = 'unknown'
    if meta.has_key(categoryName):
        value = meta[categoryName]
    if value == '':
        value = 'unknown'

    optionString,hindiOptionString = make_options_strings(
        possibilities, value, noHindi=noHindi)

    #
    # replaces %(content_type_options)s
    # and %(hindi_content_type_options)s
    #
    dict[categoryName + '_options'] = optionString
    if not noHindi:
        dict['hindi_' + categoryName + '_options'] = hindiOptionString

    

def process_dropdown(form, meta, categoryName):
    oVal = ryw_upload.process_English_dropdown(categoryName, form, meta)
    ryw_upload.process_hindi_dropdown(categoryName, form, meta, oldVal = oVal)



def process_bracket(form, meta, categoryName, key1, key2,
                    hindiKey1, hindiKey2):
    oPair = ryw_upload.process_bracket(form, key1, key2, categoryName, meta)
    ryw_upload.process_hindi_bracket(form, hindiKey1, hindiKey2,
                                     categoryName, meta, oldPair = oPair)
                        
    

def make_form_checkboxes(meta, transWords, categoryName, possibleValues,
                         prefix, dict):
    #
    # fill in all literal Hindi strings
    #
    for transWord in transWords:
        dict['trans_' + transWord] = ryw_hindi.size4_html(transWord)

    #
    # turn on or off checkboxes
    #
    if meta.has_key(categoryName):
        existingVals = meta[categoryName]
    else:
        existingVals = []

    listWithBlanks = []
    for possibility in possibleValues:
        # valName is something like 'subj_Hindi_value'
        valName = prefix + '_' + possibility + '_value'
        poss2 = possibility
        poss2 = poss2.replace('_', ' ')
        listWithBlanks.append(poss2)
        if (possibility in existingVals) or (poss2 in existingVals):
            dict[valName] = 'CHECKED'
        else:
            dict[valName] = ''

    #
    # fill in value of the other text value
    #
    otherVals = set(existingVals) - set(possibleValues) - set(listWithBlanks)
    otherStr = ryw.sequence_to_string(otherVals)
    dict[prefix + '_other_value'] = otherStr

    #
    # fill in value of the other Hindi text value
    #
    valName = 'hindi_' + prefix + '_other_value'
    hindiAttrs = ryw_upload.get_hindi_attributes(meta)
    if hindiAttrs and hindiAttrs.has_key(categoryName):
        hindiStr = ryw.sequence_to_string(hindiAttrs[categoryName])
        dict[valName] = hindiStr
    else:
        dict[valName] = ''
    


def process_checkboxes(form, meta, categoryName, prefix):
    #cgi.print_form(form)

    #if categoryName == 'cache':
    #    logging.debug('process_checkboxes: cache attribute edit entered.')
        
    checked = form.getlist(categoryName)

    #if categoryName == 'cache':
    #    logging.debug('process_checkboxes: checked: ' + repr(checked))
    
    value = form.getfirst(prefix + '_other', '')
    if value != '':
        checked.append(value)
    if checked != []: meta[categoryName] = checked

    if checked == [] and meta.has_key(categoryName):
        logging.debug('process_checkboxes: deleting attribute: ' +categoryName)
        del meta[categoryName]

    value = form.getfirst(prefix + '_other_hindi', '')
    if value != '':
        ryw_upload.add_hindi_attribute(meta, categoryName, [value])

    #if categoryName == 'cache':
    #    logging.debug('process_checkboxes: meta: ' + repr(meta))

        

def check_required_fields(form):
    if not form.has_key('title') and not form.has_key('hindi_title'):
        ryw.give_bad_news(
            'check_required_fields: needs at least one title field filled.',
            logging.error)
        return False
    return True



def process_fields(form, meta):
    for key in editableKeys:
        value = form.getfirst(key, '')
        if value != '':
            meta[key] = value
        elif key == 'title':
            meta[key] = ' '

    if meta.has_key('uploaded_by_site') and meta['uploaded_by_site'] != '':
        meta['creator'] = meta['uploaded_by_site']

    for key in editableKeys:
        formStr = 'hindi_' + key
        value = form.getfirst(formStr, '')
        if value == '':
            continue
        if meta.has_key('hindi'):
            hindi = meta['hindi']
        else:
            hindi = {}
            meta['hindi'] = hindi
        hindi[key] = value

    process_checkboxes(form, meta, 'subjects', 'subject')
    process_dropdown(form, meta, 'content_type')
    process_checkboxes(form, meta, 'languages', 'language')
    process_checkboxes(form, meta, 'show', 'show')
    process_checkboxes(form, meta, 'cache', 'cache')
    process_dropdown(form, meta, 'class')
    process_bracket(form, meta, 'age', 'age_from', 'age_to',
                    'hindi_age_from', 'hindi_age_to')
    process_checkboxes(form, meta, 'media', 'media')
    ryw_upload.process_English_dropdown('video_resolution', form, meta)
    ryw_upload.process_bracket(form, 
                               'time_length_hours', 'time_length_minutes',
                               'time_length', meta)
    ryw_upload.process_English_dropdown('time_length_seconds', form, meta)
    resize_thumbnails(meta)



def process_error_fields(form, meta):
    if not ryw_upload.process_data_size(form, meta):
        return False
    if not ryw_upload.process_date_time(form, meta):
        return False
    return True



def resize_thumbnails(meta, forced = True):
    try:
        ostore = ryw.get_objectstore(meta)
        if not ostore:
            return
        paths = objectstore.name_version_to_paths_aux(
            ostore, meta['id'], meta['version'])
        auxiDir = paths[2]
        ryw_upload.resize_thumbnails(auxiDir, forced)
    except:
        ryw.give_bad_news('ryw_meta.resize_thumbnails: failed, meta: ' +
                          repr(meta), logging.error)



def get_paths1(objroot, objID, version):
    assert(objroot)
    prefix = objectstore.nameversiontoprefix(objroot, objID, version)
    pair   = os.path.split(os.path.normpath(prefix))
    parent = pair[0]
    paths  = objectstore.name_version_to_paths_aux(objroot, objID, version)
    paths  = list(paths)
    paths.append(parent)
    return paths



def get_paths(objroot, objID, version, meta, repositoryRoot):

    paths = get_paths1(objroot, objID, version)
    
    if not meta:
        paths.append(None)
        return paths
    if not meta.has_key('path'):
        ryw.give_bad_news('DeleteObject.get_paths: missing path attribute: '+
                          repr(meta), logging.error)
        paths.append(None)
        return paths

    path = meta['path']
    try:
        resources = su.parseKeyValueFile(
            os.path.join(repositoryRoot, 'Resources.txt'))
        viewroot = resources['viewroot']
    except:
        ryw.give_bad_news('DeleteObject.get_paths: failed to get view root.',
                          logging.critical)
        paths.append(None)
        return paths
    
    viewpath = os.path.join(viewroot, path)
    paths.append(viewpath)
    logging.debug('DeleteObject.get_paths: ' + repr(paths))
    return paths    



"""
Notes for re-writing meta data file:
(0) check for sanity (in ShowObject and EditObject). (done if gotten from meta)
(1) copy existing meta file to _BAK. (if dies here, good meta is still there.)
(2) move DONE or MDON flag to _BAK. (if dies here, later code gets it back.)
(3) write new metadata. (if dies here, later code gets _BAK back.)
(4) restore DONE or MDON flag.
(5) wipe out _BAK.
(.) places that read meta files should generally call
    good_repo_paths(), which tries to do restoration.
"""

def rewrite_meta(objroot, objID, version, meta, paths=None):
    """when called by reformat_ntfs.py, we supply the paths directly.
    otherwise, paths is none."""

    if paths == None: 
        logging.debug('rewrite_meta entered: ' + objID + '#' + str(version))
        paths = get_paths1(objroot, objID, version)
        paths = paths[:-1]

        #
        # (0) sanity checking.
        #
        if not ryw.good_repo_paths(paths):
            ryw.give_bad_news('rewrite_meta: failed ' +
                              'initial path sanity check: ' +
                              repr(paths), logging.error)
            return False
    
    dataPath,metaPath,auxiPath,donePath,mdonPath = paths

    #
    # (1) backup old meta file.
    #
    if not ryw.move_to_bak(metaPath, copyInsteadOfMove=True):
        ryw.give_bad_news('rewrite_meta: failed to backup meta file: ' +
                          metaPath, logging.error)
        return False
    logging.debug('rewrite_meta: successfully backed up old meta file: ' +
                  metaPath)

    #
    # (2) backup done flag.
    #
    if os.path.exists(donePath):
        doneFlagToMove = donePath
    elif os.path.exists(mdonPath):
        doneFlagToMove = mdonPath
    else:
        ryw.give_bad_news('rewrite_meta: unexpected missing done flag: ' +
                          donePath + '  or  ' + mdonPath, logging.critical)
        return False
        
    if not ryw.move_to_bak(doneFlagToMove):
        ryw.give_bad_news('rewrite_meta: failed to move done flag: ' +
                          doneFlagToMove, logging.error)
        return False
    logging.debug('rewrite_meta: successfully moved done flag to bak: ' +
                  doneFlagToMove)

    #
    # (3) write new meta file.
    #
    if not write_meta(metaPath, meta, paths):
        ryw.give_bad_news('rewrite_meta: write_meta failed: ' + metaPath,
                          logging.error)
        return False
    logging.debug('rewrite_meta: successfully written meta data: ' + metaPath)

    retVal = True
    #
    # (4) restore the done flag.
    #
    doneFlagBak = doneFlagToMove + '_BAK'
    try:
        shutil.move(doneFlagBak, doneFlagToMove)
    except:
        ryw.give_bad_news('rewrite_meta: failed to restore done flag: ' +
                          doneFlagToMove, logging.critical)
        #
        # last ditch effort to rewrite a new done flag.
        #
        if not write_new_done_flag(doneFlagToMove):
            ryw.give_bad_news('rewrite_meta: failed to write new flag: ' +
                              doneFlagToMove, logging.critical)
            retVal = False
            pass  # in any case we proceed to next step.
        pass # in any case we proceed to next step.

    #
    # (5) wipe out _BAK meta.
    #
    ryw.cleanup_path(metaPath + '_BAK', 'rewrite_meta:')
    
    return retVal



def write_meta(metaPath, meta, paths):
    #
    # if this fails, we need to restore the old meta file and old done flag.
    #
    try:
        su.pickdump(meta, metaPath)
        ryw.db_print_info_browser('write_meta: ' + repr(meta), 101)
    except:
        ryw.give_bad_news('write_meta: su.pickdump failed: ' + metaPath,
                          logging.critical)
        restore_old_meta(paths, metaPath)
        return False
        
    logging.debug('write_meta: metadata successfully written: ' + metaPath)
    return True



def restore_old_meta(paths, metaPath):
    #
    # first wipe out the bad current meta file.
    #
    ryw.cleanup_path(metaPath, 'restore_old_meta:')
    attempt_repair_repo_paths(paths)



def write_new_done_flag(doneFlag):
    try:
        f = open(doneFlag, 'w')
        f.close()
        logging.debug('write_new_done_flag: written done flag: ' + doneFlag)
        return True
    except:
        ryw.give_bad_news('write_new_done_flag failed: ' + doneFlag,
                          logging.critical)
        return False



def get_objectstore_root(repositoryRoot, meta):
    if meta and meta.has_key('objectstore'):
        #
        # I'm doing this to hardwire all
        # places of gettting objectstoreroot.
        #
        #return meta['objectstore']
        return ryw.hard_wired_objectstore_root()

    logging.warning('get_objectstore_root: meta has no objstore root! ')
    return os.path.join(repositoryRoot, 'WWW', 'ObjectStore')



def isList(meta):
    return meta and meta.has_key('sys_attrs') and 'isList' in meta['sys_attrs']



def get_meta_list(reqList, searchFile):
    """broken out of ShowQueue.py, used by ShowQueue, DisplaySelection,
    and ChapterListForm."""

    metaList = []

    for item in reqList:
        try:
            objname, version = item.split('#')
            version = int(version)
        except:
            ryw.give_bad_news('ryw_meta.get_meta_list: ' +
                              'ill-formed line: ' + item,
                              logging.critical)
            continue

        success,d = searchFile.get_meta(objname, version)
        if not success:
            ryw.give_bad_news2(
                'ryw_meta.get_meta_list: get_meta failed ' +
                '(possibly because object has been ' +
                'deleted from objectstore): ' +
                objname + ' ' + str(version), logging.error)
            continue

        metaList.append(d)

    return metaList
