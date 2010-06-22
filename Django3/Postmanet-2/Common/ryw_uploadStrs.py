import ryw_hindi,ryw



######################################################################
repositoryStr1 = """
<HTML>
<HEAD>
<TITLE>Add Content To the Repository</TITLE>
</HEAD>

<BODY>
<CENTER>
<A HREF="/index.html">
<IMG SRC="/icons/sh500.gif" BORDER=0 WIDTH=482 HEIGHT=167></A>
<BR>

<H3>Add Content To the Repository</H3>

If you're unsure about any fields on this page, leave them blank.
<P>

<TABLE BORDER=0 WIDTH=800><TR><TD>

<FORM ACTION="/cgi-bin/WebUpload_ryw.py" METHOD="post"
ENCTYPE="multipart/form-data">

"""



######################################################################
villageStr1 = """
<HTML>
<HEAD>
<TITLE>Submit Content To the Central Repository</TITLE>
</HEAD>

<BODY>

<!-- ##################################################
The following is identical to the repository side. -->

<CENTER>
<A HREF="/index.html">
<IMG SRC="/icons/sh500.gif" BORDER=0></A>
<BR>

<H3>Submit Content To the Central Repository<br>
%(trans_submit_title)s</H3>

If you're unsure about any fields on this page, leave them blank.<BR>
%(trans_leave_blank)s
<P>

<TABLE BORDER=0 WIDTH=800><TR><TD>

<FORM ACTION="/cgi-bin/repository/Upload_ryw.py" METHOD="post"
ENCTYPE="multipart/form-data">

"""

villageStr1 = ryw_hindi.replace_size4_hindi_html(villageStr1, \
    ['submit_title', 'leave_blank'])                                


######################################################################
bothStr2 = """
<CENTER>
<INPUT TYPE="submit" VALUE="Upload">
<INPUT TYPE="submit" VALUE="%(trans_upload)s" %(trans_txt_style)s>
<BR>
</CENTER>
<P>
<BR>


<B><I>required fields %(trans_required_fields)s :</I></B>
<P>


<TABLE BORDER=0>
<TR><TD WIDTH=1></TD>
<TD>

<UL>
<LI>
<U>title</U>:
<INPUT TYPE="TEXT" NAME="title" SIZE=80>
<P>

%(trans_title)s:
<INPUT TYPE="TEXT" NAME="hindi_title" SIZE=80 %(trans_txt_style)s>
<P>

<LI>
<U>local file</U> to upload [%(trans_file_to_upload)s]:<input type=file name="local_filename" SIZE=60>
<P>
</UL>

</TD>
</TR>
</TABLE>

<BR>

"""

bothStr2 = ryw_hindi.replace_hindi_plain_and_html(bothStr2, \
    ['file_to_upload', 'title', 'required_fields'], ['upload'])



######################################################################
villageStudentsStr = """
<!-- ##################################################
The following is unique to the village side. -->

<B><I>optional fields for the village side:</I></B>
<P>

<TABLE BORDER=0>
<TR><TD WIDTH=1></TD>
<TD>

<UL>
<LI>
<U>students concerned</U>:
<INPUT TYPE="TEXT" NAME="students" SIZE=80>
<P>

%(trans_students_concerned)s:
<INPUT TYPE="TEXT" NAME="hindi_students" SIZE=80 %(trans_txt_style)s>
<P>

</UL>

</TD>
</TR>
</TABLE>

<BR>
"""
villageStudentsStr = ryw_hindi.replace_size4_hindi_html(
    villageStudentsStr, ['students_concerned'])



######################################################################
bothStr3 = """
<B><I>optional fields:</I></B>
<P>


<TABLE BORDER=0>
<TR><TD WIDTH=1></TD>
<TD>

<UL>

<LI>
<U>unpack</U>?
check this if you are uploading a compressed file that must be unpacked at the
repository to recover the contents of the object.  this is used to
upload an object that consists of multiple files or directories.
(leave it blank if you don't know what this is for.)
[%(trans_unzip)s]
<INPUT type=checkbox name=unzip value=yes>
<P>

<LI>
<U>description:</U><BR>
<TEXTAREA NAME="description" ROWS=5 COLS=70></TEXTAREA>
<P>

%(trans_description)s:<BR>
<TEXTAREA NAME="hindi_description" ROWS=5 COLS=70 %(trans_txt_style)s>
</TEXTAREA>
<P>

<LI>
<U>thumbnail image 1</U> (recommended use: a small image):<BR>
[%(trans_thumbnail1)s]<BR>
<input type=file name="thumbnail_name1" SIZE=60>

<P>

<LI>
<U>thumbnail image 2</U> (recommended use: an author picture):<BR>
[%(trans_thumbnail2)s]<BR>
<input type=file name="thumbnail_name2" SIZE=60><BR>

<P>

<LI>
<U>thumbnail image 3</U> (recommended use: a larger image):<BR>
[%(trans_thumbnail3)s]<BR>
<input type=file name="thumbnail_name3" SIZE=60><BR>

<P>

<LI>
<U>thumbnail image 4</U> (recommended use: a larger image):<BR>
[%(trans_thumbnail4)s]<BR>
<input type=file name="thumbnail_name4" SIZE=60><BR>

<P>

<LI>
<U>excerpt file 1</U> [%(trans_excerpt1)s]:<BR>
<input type=file name="excerpt_name1" SIZE=60>
<P>

<LI>
<U>excerpt file 2</U> [%(trans_excerpt2)s]:<BR>
<input type=file name="excerpt_name2" SIZE=60>
<P>

<LI>
<U>excerpt file 3</U> [%(trans_excerpt3)s]:<BR>
<input type=file name="excerpt_name3" SIZE=60>
<P>

<LI>
<U>excerpt file 4</U> [%(trans_excerpt4)s]:<BR>
<input type=file name="excerpt_name4" SIZE=60>
<P>


<LI>
<U>subjects</U> (check all that apply) [%(trans_subjects)s]:
English [%(trans_english)s] <INPUT type=checkbox name=subject_English>, 
Hindi [%(trans_hindi)s] <INPUT type=checkbox name=subject_Hindi>, 
Sanskrit [%(trans_sanskrit)s] <INPUT type=checkbox name=subject_Sanskrit>, 
science [%(trans_science)s] <INPUT type=checkbox name=subject_science>
(physics [%(trans_physics)s] <INPUT type=checkbox name=subject_physics>,
chemistry [%(trans_chemistry)s] <INPUT type=checkbox name=subject_chemistry>,
astronomy [%(trans_astronomy)s] <INPUT type=checkbox name=subject_astronomy>,
biology [%(trans_biology)s] <INPUT type=checkbox name=subject_biology>,
geology [%(trans_geology)s] <INPUT type=checkbox name=subject_geology>),
mathematics [%(trans_mathematics)s]
<INPUT type=checkbox name=subject_mathematics>
(arithmetic [%(trans_arithmetic)s]
<INPUT type=checkbox name=subject_arithmetic>,
algebra [%(trans_algebra)s] <INPUT type=checkbox name=subject_algebra>,
geometry [%(trans_geometry)s] <INPUT type=checkbox name=subject_geometry>),
history [%(trans_history)s] <INPUT type=checkbox name=subject_history>,
social studies [%(trans_social_studies)s]
<INPUT type=checkbox name=subject_social_studies>,
home science [%(trans_home_science)s]
<INPUT type=checkbox name=subject_home_science>,
agriculture [%(trans_agriculture)s]
<INPUT type=checkbox name=subject_agriculture>,
commerce [%(trans_commerce)s]
<INPUT type=checkbox name=subject_commerce>,
general knowledge [%(trans_general_knowledge)s]
<INPUT type=checkbox name=subject_general_knowledge>,
food and nutrition [%(trans_food_and_nutrition)s]
<INPUT type=checkbox name=subject_food_and_nutrition>,
arts and crafts [%(trans_arts_and_crafts)s]
<INPUT type=checkbox name=subject_arts_and_crafts>,
computer literacy [%(trans_computer_literacy)s]
<INPUT type=checkbox name=subject_computer_literacy>,
games [%(trans_games)s]
<INPUT type=checkbox name=subject_games>,
stories [%(trans_stories)s]
<INPUT type=checkbox name=subject_stories>,
plays [%(trans_plays)s]
<INPUT type=checkbox name=subject_plays>,
with vocabulary [%(trans_with_vocabulary)s]
<INPUT type=checkbox name=subject_with_vocabulary>,
environmental science [%(trans_environmental_science)s]
<INPUT type=checkbox name=subject_environmental_science>,

health care [%(trans_health_care)s]
<INPUT type=checkbox name=subject_health_care>
(nursing [%(trans_nursing)s]
<INPUT type=checkbox name=subject_nursing>,
reproductive health [%(trans_reproductive_health)s]
<INPUT type=checkbox name=subject_reproductive_health>,
children health [%(trans_children_health)s]
<INPUT type=checkbox name=subject_children_health>),

women rights [%(trans_women_rights)s]
<INPUT type=checkbox name=subject_women_rights>,

Kannada [%(trans_kannada)s]
<INPUT type=checkbox name=subject_Kannada>,
Tamil [%(trans_tamil)s]
<INPUT type=checkbox name=subject_Tamil>,
Bengali [%(trans_bengali)s]
<INPUT type=checkbox name=subject_Bengali>,
Marathi [%(trans_marathi)s]
<INPUT type=checkbox name=subject_Marathi>,
Punjabi [%(trans_punjabi)s]
<INPUT type=checkbox name=subject_Punjabi>,
children program [%(trans_children_program)s]
<INPUT type=checkbox name=subject_Punjabi>,
<BR>
other subject (specify):
<INPUT TYPE="TEXT" NAME="subject_other" SIZE=20>
&nbsp;&nbsp;
%(trans_other_subject)s:
<INPUT TYPE="TEXT" NAME="subject_other_hindi" SIZE=20 %(trans_txt_style)s>
<P>


<LI>
<U>content type</U>:
<SELECT NAME="content_type" VALUE="unknown">
<OPTION>unknown
<OPTION>lecture
<OPTION>lesson_plan
<OPTION>test
<OPTION>courseware
<OPTION>practicals
<OPTION>experiments
<OPTION>teacher_training
<OPTION>staff_training
<OPTION>community_training
<OPTION>textbook
<OPTION>course_materials
<OPTION>monitoring
<OPTION>visits
<OPTION>documentary
<OPTION>public_awareness
<OPTION>other_TV
<OPTION>workshop
<OPTION>radio_program
<OPTION>requests
<OPTION>support_software
<OPTION>interview
<OPTION>chat
<OPTION>student_projects
<OPTION>homework_submission
<OPTION>homework_feedback
<OPTION>questions
<OPTION>answers
<OPTION>social_entertainment
<OPTION>exam
<OPTION>information
<OPTION>scratch_space
<OPTION>tmp
<OPTION>other
</SELECT>

&nbsp;&nbsp;&nbsp;

%(trans_content_type)s:
<SELECT NAME="hindi_content_type" VALUE="%(trans_unknown)s"
%(trans_txt_style)s>
<OPTION>%(trans_unknown)s
<OPTION>%(trans_lecture)s
<OPTION>%(trans_lesson_plan)s
<OPTION>%(trans_test)s
<OPTION>%(trans_courseware)s
<OPTION>%(trans_practicals)s
<OPTION>%(trans_experiments)s
<OPTION>%(trans_textbook)s
<OPTION>%(trans_course_materials)s
<OPTION>%(trans_monitoring)s
<OPTION>%(trans_visits)s
<OPTION>%(trans_documentary)s
<OPTION>%(trans_public_awareness)s
<OPTION>%(trans_other_TV)s
<OPTION>%(trans_workshop)s
<OPTION>%(trans_radio_program)s
<OPTION>%(trans_support_software)s
<OPTION>%(trans_teacher_training)s
<OPTION>%(trans_staff_training)s
<OPTION>%(trans_community_training)s
<OPTION>%(trans_chat)s
<OPTION>%(trans_interview)s
<OPTION>%(trans_student_projects)s
<OPTION>%(trans_homework_submission)s
<OPTION>%(trans_homework_feedback)s
<OPTION>%(trans_questions)s
<OPTION>%(trans_answers)s
<OPTION>%(trans_social_entertainment)s
<OPTION>%(trans_exam)s
<OPTION>%(trans_information)s
<OPTION>%(trans_scratch_space)s
<OPTION>%(trans_tmp)s
<OPTION>%(trans_other)s
</SELECT>
<P>

<LI>
<U>language</U> (check all that apply) [%(trans_language)s]:
English [%(trans_english)s] <INPUT type=checkbox name=language_English>, 
Hindi [%(trans_hindi)s] <INPUT type=checkbox name=language_Hindi>,
Kannada [%(trans_kannada)s] <INPUT type=checkbox name=language_Kannada>,
Tamil [%(trans_tamil)s] <INPUT type=checkbox name=language_Tamil>,
Bengali [%(trans_bengali)s] <INPUT type=checkbox name=language_Bengali>,
Marathi [%(trans_marathi)s] <INPUT type=checkbox name=language_Marathi>,
Punjabi [%(trans_punjabi)s] <INPUT type=checkbox name=language_Punjabi>,
Telegu [%(trans_telegu)s] <INPUT type=checkbox name=language_Telegu>,
Gujarati [%(trans_gujarati)s] <INPUT type=checkbox name=language_Gujarati>,
Kashmiri [%(trans_kashmiri)s] <INPUT type=checkbox name=language_Kashmiri>,
other language (specify):
<INPUT TYPE="TEXT" NAME="language_other" SIZE="20">
&nbsp;&nbsp;
%(trans_other_language)s:
<INPUT TYPE="TEXT" NAME="language_other_hindi" SIZE="20" %(trans_txt_style)s>
<P>

<LI>
<U>for class</U>:
<SELECT NAME="class">
<OPTION>unknown
<OPTION>preschool
<OPTION>1
<OPTION>2
<OPTION>3
<OPTION>4
<OPTION>5
<OPTION>6
<OPTION>7
<OPTION>8
<OPTION>9
<OPTION>10
<OPTION>11
<OPTION>12
<OPTION>college
</SELECT>

&nbsp;&nbsp;

%(trans_for_class)s:
<SELECT NAME="hindi_class"
%(trans_txt_style)s>
<OPTION>%(trans_unknown)s
<OPTION>%(trans_preschool)s
<OPTION>1
<OPTION>2
<OPTION>3
<OPTION>4
<OPTION>5
<OPTION>6
<OPTION>7
<OPTION>8
<OPTION>9
<OPTION>10
<OPTION>11
<OPTION>12
<OPTION>%(trans_college)s
</SELECT>
<P>


<LI>
<U>applicable age</U>: 
from
<SELECT NAME="age_from">
<OPTION>unknown
<OPTION>preschool
<OPTION>6
<OPTION>7
<OPTION>8
<OPTION>9
<OPTION>10
<OPTION>11
<OPTION>12
<OPTION>13
<OPTION>14
<OPTION>15
<OPTION>16
<OPTION>17
<OPTION>college
</SELECT>
to
<SELECT NAME="age_to">
<OPTION>unknown
<OPTION>preschool
<OPTION>6
<OPTION>7
<OPTION>8
<OPTION>9
<OPTION>10
<OPTION>11
<OPTION>12
<OPTION>13
<OPTION>14
<OPTION>15
<OPTION>16
<OPTION>17
<OPTION>college
</SELECT>
<P>

%(trans_applicable_age)s: 
%(trans_from)s
<SELECT NAME="hindi_age_from"
%(trans_txt_style)s>
<OPTION>%(trans_unknown)s
<OPTION>%(trans_preschool)s
<OPTION>6
<OPTION>7
<OPTION>8
<OPTION>9
<OPTION>10
<OPTION>11
<OPTION>12
<OPTION>13
<OPTION>14
<OPTION>15
<OPTION>16
<OPTION>17
<OPTION>%(trans_college)s
</SELECT>
%(trans_to)s
<SELECT NAME="hindi_age_to"
%(trans_txt_style)s>
<OPTION>%(trans_unknown)s
<OPTION>%(trans_preschool)s
<OPTION>6
<OPTION>7
<OPTION>8
<OPTION>9
<OPTION>10
<OPTION>11
<OPTION>12
<OPTION>13
<OPTION>14
<OPTION>15
<OPTION>16
<OPTION>17
<OPTION>%(trans_college)s
</SELECT>
<P>


<LI>
<U>media type</U> (check all that apply) [%(trans_media_type)s]:
video [%(trans_video)s] <INPUT type=checkbox name=media_video>, 
(DVD <INPUT type=checkbox name=media_DVD>, 
VCD <INPUT type=checkbox name=media_VCD>,
extracted by firewire [%(trans_extracted_by_firewire)s]
<INPUT type=checkbox name=media_extracted_by_firewire>,
recorded by Plextor [%(trans_recorded_by_Plextor)s]
<INPUT type=checkbox name=media_recorded_by_Plextor>,
recorded_from_TV [%(trans_recorded_from_TV)s]
<INPUT type=checkbox name=media_recorded_from_TV>,
VHS tape digitized [%(trans_VHS_tape_digitized)s]
<INPUT type=checkbox name=media_VHS_tape_digitized>,
recorded by webcam [%(trans_recorded_by_webcam)s]
<INPUT type=checkbox name=media_recorded_by_webcam>,
recorded by Mustek [%(trans_recorded_by_Mustek)s]
<INPUT type=checkbox name=media_recorded_by_Mustek>,
recorded by Aiptek [%(trans_recorded_by_Aiptek)s]
<INPUT type=checkbox name=media_recorded_by_Aiptek>,
recorded by CamStudio [%(trans_recorded_by_CamStudio)s]
<INPUT type=checkbox name=media_recorded_by_CamStudio>,
created by ProShow [%(trans_created_by_ProShow)s]
<INPUT type=checkbox name=media_created_by_ProShow>,
has subtitle [%(trans_has_subtitle)s]
<INPUT type=checkbox name=media_has_subtitle>,
SMIL <INPUT type=checkbox name=media_SMIL>),
audio (without video)
[%(trans_audio_without_video)s] <INPUT type=checkbox
name=media_audio_without_video>,
Flash <INPUT type=checkbox name=media_Flash>, 
images [%(trans_images)s] <INPUT type=checkbox name=media_images>, 
powerpoint <INPUT type=checkbox name=media_powerpoint>, 
documents [%(trans_documents)s] <INPUT type=checkbox name=media_documents>,
executables [%(trans_executables)s] <INPUT type=checkbox name=media_executables>,
slideshows [%(trans_slideshows)s] <INPUT type=checkbox name=media_slideshows>,
other type (specify):
<INPUT TYPE="TEXT" NAME="media_other" SIZE="20">
&nbsp;&nbsp;
%(trans_other_type)s:
<INPUT TYPE="TEXT" NAME="media_other_hindi" SIZE=20 %(trans_txt_style)s>
<P>

<LI>
<U>video resolution</U> (width in pixels)
[%(trans_video_resolution)s]:
<SELECT NAME="video_resolution">
<OPTION>unknown
<OPTION>320
<OPTION>350
<OPTION>640
<OPTION>720
<OPTION>1024
<OPTION> &gt; 1024
</SELECT>
<P>

<LI>
<U>content duration</U> [%(trans_content_duration)s]:
hours [%(trans_hours)s]
<SELECT NAME="time_length_hours">
<OPTION>unknown
<OPTION>0
<OPTION>1
<OPTION>2
<OPTION>3
<OPTION>4
<OPTION>5
<OPTION>6
<OPTION>7
<OPTION>8
<OPTION>more
</SELECT>
minutes [%(trans_minutes)s]
<SELECT NAME="time_length_minutes">
<OPTION>unknown
<OPTION>0
<OPTION>1
<OPTION>2
<OPTION>3
<OPTION>4
<OPTION>5
<OPTION>6
<OPTION>7
<OPTION>8
<OPTION>9
<OPTION>10
<OPTION>11
<OPTION>12
<OPTION>13
<OPTION>14
<OPTION>15
<OPTION>16
<OPTION>17
<OPTION>18
<OPTION>19
<OPTION>20
<OPTION>25
<OPTION>30
<OPTION>35
<OPTION>40
<OPTION>45
<OPTION>50
<OPTION>55
</SELECT>
<P>





<LI>
<U>data size</U> [%(trans_data_size)s]:
<INPUT TYPE="TEXT" NAME="size_text" SIZE="6">
<SELECT NAME="size_unit" VALUE="MB">
<OPTION>MB
<OPTION>KB
<OPTION>B
</SELECT>
<P>





<LI>
<U>content alias</U> [%(trans_content_alias)s]:
<INPUT TYPE="TEXT" NAME="content_alias" SIZE="20">
<P>

<LI>
<U>related content</U> [%(trans_related_content)s]:
<INPUT TYPE="TEXT" NAME="related_content" SIZE="40">
<P>

<LI>
<U>show</U> [%(trans_show)s]:
copyrighted [%(trans_copyrighted)s] <INPUT type=checkbox name=show_copyrighted>,
discreet [%(trans_discreet)s] <INPUT type=checkbox name=show_discreet>
<P>

<LI>
<U>cache</U> [%(trans_cache)s]:
sticky [%(trans_sticky)s] <INPUT type=checkbox name=cache_sticky>
<P>

<LI>
<U>teacher/author</U> (person name):<INPUT TYPE="TEXT" NAME="author_name" SIZE="40">
<P>

%(trans_teacher)s
<FONT SIZE=4>/</FONT>
%(trans_author)s:
<INPUT TYPE="TEXT" NAME="hindi_author_name" SIZE=40>
<P>

<LI>
<U>uploaded by</U> (person name):<INPUT TYPE="TEXT" NAME="uploaded_by_name" SIZE="40">
<P>

%(trans_uploaded_by)s:
<INPUT TYPE="TEXT" NAME="hindi_uploaded_by_name" SIZE=40>
<P>

<LI>
<U>uploaded by</U> (site name):<INPUT TYPE="TEXT" NAME="uploaded_by_site" SIZE="40" VALUE=%(userName)s>
<P>

%(trans_uploaded_by_site)s:
<INPUT TYPE="TEXT" NAME="hindi_uploaded_by_site" SIZE=40>
<P>




<LI>
<U>date and time</U> %(trans_date_and_time)s:
<INPUT TYPE="TEXT" NAME="uploaded_date_time" SIZE="14"
VALUE="%(uploaded_date_time_val)s">
<P>






</UL>

</TD>
</TR>
</TABLE>

<!--

<BR>
<B><I>obscure fields:</I></B>
<P>

<TABLE BORDER=0>
<TR><TD WIDTH=1></TD>
<TD>

Leave them blank if you don't know what these are for.


<UL>

<LI>
<U>optional object ID</U> (for specifying an old version to be
replaced, or for specifying sub-objects included in multi-file big
objects): <INPUT TYPE="TEXT" NAME="object_ID" SIZE="40">
<P>

<LI>
<U>optional path</U>, (the last component of which is a pointer file,
pointing to the repository object): <INPUT TYPE="TEXT" NAME="path" SIZE="40">
<P>

<LI>
<U>file name used in the repository</U> (defaults to the same as the local
name, include extension, such as movie.avi or sound.mp3.  the
extension must match that of the original file name):
<INPUT TYPE="TEXT" NAME="repository_filename" SIZE="40">
<P>

</UL>

</TD>
</TR>
</TABLE>

-->

<BR>


<CENTER>
<INPUT TYPE="submit" VALUE="Upload">
<INPUT TYPE="submit" VALUE="%(trans_upload)s" %(trans_txt_style)s>
</CENTER>

</FORM>

</TD></TR></TABLE>

</CENTER>

<BR>

<HR WIDTH=75%%>

<CENTER>
<FONT SIZE=2>
&#169 2005-%(year)s &nbsp;&nbsp;
<A HREF="/index.html">The Digital StudyHall</a>
</FONT>
</CENTER>

<HR WIDTH=75%%>

</BODY>
</HTML>
"""

#bothStr3 = ryw_hindi.replace_size4_hindi_html(bothStr3, \
bothStr3 = ryw_hindi.replace_hindi_plain_and_html(bothStr3, \
    ['description', 'teacher', 'author', 'uploaded_by', 'data_size',
     'content_alias',
     'uploaded_by_site', 'date_and_time',
     'related_content', 'unzip', 'thumbnail1',
     'thumbnail2', 'thumbnail3', 'thumbnail4', 'excerpt1', 'excerpt2',
     'excerpt3', 'excerpt4', 'subjects', 'english', 'hindi', 'sanskrit',
     'science', 'physics', 'chemistry', 'astronomy', 'biology', 'geology',
     'mathematics', 'arithmetic', 'algebra', 'geometry', 'history',
     'social_studies', 'home_science', 'agriculture', 'commerce',
     'general_knowledge',
     'food_and_nutrition', 'arts_and_crafts',
     'computer_literacy', 'games', 'stories',
     'plays', 'with_vocabulary',
     'environmental_science',
     'health_care', 'nursing', 'reproductive_health',
     'children_health', 'women_rights', 'children_program',
     'kannada', 'tamil', 'bengali', 'marathi',
     'punjabi', 
     'other_subject', 'content_type', 'language', 'other_language',
     'kannada', 'tamil', 'bengali', 'marathi', 'punjabi', 'telegu',
     'gujarati', 'kashmiri',
     'for_class', 'applicable_age', 'from', 'to', 'media_type', 'video',
     'extracted_by_firewire',
     'recorded_by_Plextor', 'recorded_from_TV', 'VHS_tape_digitized', 
     'recorded_by_webcam', 'recorded_by_CamStudio',
     'recorded_by_Mustek', 'recorded_by_Aiptek',
     'created_by_ProShow', 'has_subtitle', 
     'audio_without_video', 'images', 'documents', 'executables', 'slideshows',
     'other_type',
     'video_resolution', 'content_duration', 'hours', 'minutes',
     'cache', 'sticky', 'show', 'copyrighted', 'discreet'],
    ['upload', 'unknown', 'lecture', 'lesson_plan', 'test', 
     'courseware', 'practicals', 'experiments',
     'textbook', 'course_materials', 'monitoring', 'visits', 'documentary',
     'public_awareness', 
     'other_TV', 'workshop', 'radio_program',
     'requests',
     'support_software',
     'teacher_training',
     'staff_training', 'community_training', 
     'chat', 'interview', 'student_projects',
     'homework_submission', 'homework_feedback', 'questions', 'answers',
     'social_entertainment', 'exam', 'information', 'scratch_space', 'tmp',
     'other', 'preschool', 'college'],
    otherDict = ryw.get_misc_dict())
                                                  
# otherDict is for other replacements like name and year.



