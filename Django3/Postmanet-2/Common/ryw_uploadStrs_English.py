import ryw, ryw_customize



#uploadQueue
######################################################################
uploadSelStr1x = """
<HTML>
<HEAD>
<TITLE>Add Selected List To the Repository</TITLE>
</HEAD>

<BODY>
<CENTER>
<A HREF="/index.html">
<IMG SRC="%(smallLogoFileName)s" BORDER=0 %(smallLogoDimension)s></A>
<BR>

<H3>Add Selected List To the Repository</H3>

<TABLE BORDER=0 WIDTH=800><TR><TD>

<FORM ACTION="/cgi-bin/UploadQueue.py" METHOD="post"
ENCTYPE="multipart/form-data">

"""
uploadSelStr1 = uploadSelStr1x % ryw_customize.dict



######################################################################
repositoryStr1x = """
<HTML>
<HEAD>
<TITLE>Add Content To the Repository</TITLE>
<script type="text/javascript">
function cloneFilename(id, cloneid)
{
var fname = document.getElementById(id).value;
document.getElementById(cloneid).value = fname;
}
function clearField(id)
{
document.getElementById(id).value = "";
}
</script>
</HEAD>

<BODY>
<CENTER>
<A HREF="/index.html">
<IMG SRC="%(smallLogoFileName)s" BORDER=0 %(smallLogoDimension)s></A>
<BR>

<H3>Add Content To the Repository</H3>

If you're unsure about any fields on this page, leave them blank.
<P>

<TABLE BORDER=0 WIDTH=800><TR><TD>

<FORM ACTION="/cgi-bin/WebUpload_ryw.py" METHOD="post"
ENCTYPE="multipart/form-data">

"""
repositoryStr1 = repositoryStr1x % ryw_customize.dict



######################################################################
villageStr1x = """
<HTML>
<HEAD>
<TITLE>Submit Content To the Central Repository</TITLE>
</HEAD>

<BODY>

<!-- ##################################################
The following is identical to the repository side. -->

<CENTER>
<A HREF="/index.html">
<IMG SRC="%(smallLogoFileName)s" BORDER=0></A>
<BR>

<H3>Submit Content To the Central Repository</H3>

If you're unsure about any fields on this page, leave them blank.
<P>

<TABLE BORDER=0 WIDTH=800><TR><TD>

<FORM ACTION="/cgi-bin/repository/Upload_ryw.py" METHOD="post"
ENCTYPE="multipart/form-data">

"""
villageStr1 = villageStr1x % ryw_customize.dict



#uploadQueue
######################################################################
uploadSelStr2 = """
<CENTER>
<INPUT TYPE="submit" VALUE="Upload"> <INPUT type="reset" value="Clear All">
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
<INPUT TYPE="TEXT" NAME="title" SIZE=80>
<P>

</UL>

</TD>
</TR>
</TABLE>

<BR>

"""



######################################################################
bothStr2 = """
<CENTER>
<INPUT TYPE="submit" VALUE="Upload"> <INPUT type="reset" value="Clear All">
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
<INPUT TYPE="TEXT" NAME="title" SIZE=80>
<P>

<LI>
<U>local file</U> to upload:
<input type=file name="local_filename" id="local_name" SIZE=60><img
width=16 height=16 border=0 src="/icons/delete.ico" title="clear"
onclick="clearField('local_name')">
<P>
</UL>

</TD>
</TR>
</TABLE>

<BR>

"""



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

</UL>

</TD>
</TR>
</TABLE>

<BR>
"""



######################################################################
bothStr3part = """
<B><I>optional fields:</I></B>
<P>


<TABLE BORDER=0>
<TR><TD WIDTH=1></TD>
<TD>

<UL>

<LI>
<U>repeat local file name</U> for faster local upload (directory name
allowed):<BR>
<input type="TEXT" name="repeat_local_filename" SIZE=90><BR>
<P>


<LI>
<U>unpack</U>?
check this if you are uploading a compressed file that must be unpacked at the
repository to recover the contents of the object.  this is used to
upload an object that consists of multiple files or directories.
(leave it blank if you don't know what this is for.)
<INPUT type=checkbox name=unzip value=yes>
<P>

<LI>
<U>description:</U><BR>
<TEXTAREA NAME="description" ROWS=5 COLS=70></TEXTAREA>
<P>


<LI>
<U>thumbnail image 1</U>:
<input type=file name="thumbnail_name1" id="thumbnail_name1" SIZE=60><img
width=16 height=16 border=0 src="/icons/delete.ico" title="clear"
onclick="clearField('thumbnail_name1')">
<BR>
(recommended use: a small image.)
<P>

<LI>
<U>thumbnail image 2</U>:
<input type=file name="thumbnail_name2" id="thumbnail_name2" SIZE=60><img
width=16 height=16 border=0 src="/icons/delete.ico" title="clear"
onclick="clearField('thumbnail_name2')">
<BR>
(recommended use: an author picture.)
<P>

<LI>
<U>thumbnail image 3</U>:
<input type=file name="thumbnail_name3" id="thumbnail_name3" SIZE=60><img
width=16 height=16 border=0 src="/icons/delete.ico" title="clear"
onclick="clearField('thumbnail_name3')">
<BR>
(recommended use: a larger image.)
<P>

<LI>
<U>thumbnail image 4</U>:
<input type=file name="thumbnail_name4" id="thumbnail_name4" SIZE=60><img
width=16 height=16 border=0 src="/icons/delete.ico" title="clear"
onclick="clearField('thumbnail_name4')">
<BR>
(recommended use: a larger image.)
<P>

<LI>
<U>local exercept file</U> to upload (directory name allowed):<BR>
<input type="TEXT" name="local_excerpt_filename" SIZE=90><BR>
<P>

<LI>
<U>excerpt file 1</U>:
<input type=file name="excerpt_name1" id="excerpt_name1" SIZE=60><img
width=16 height=16 border=0 src="/icons/delete.ico" title="clear"
onclick="clearField('excerpt_name1')">
<P>

<LI>
<U>excerpt file 2</U>:
<input type=file name="excerpt_name2" id="excerpt_name2" SIZE=60><img
width=16 height=16 border=0 src="/icons/delete.ico" title="clear"
onclick="clearField('excerpt_name2')">
<P>

<LI>
<U>excerpt file 3</U>:
<input type=file name="excerpt_name3" id="excerpt_name3" SIZE=60><img
width=16 height=16 border=0 src="/icons/delete.ico" title="clear"
onclick="clearField('excerpt_name3')">
<P>

<LI>
<U>excerpt file 4</U>:
<input type=file name="excerpt_name4" id="excerpt_name4" SIZE=60><img
width=16 height=16 border=0 src="/icons/delete.ico" title="clear"
onclick="clearField('excerpt_name4')">
<P>


<LI>
<U>subjects</U> (check all that apply):
English <INPUT type=checkbox name=subject_English>, 
Hindi <INPUT type=checkbox name=subject_Hindi>, 
Sanskrit <INPUT type=checkbox name=subject_Sanskrit>, 
science <INPUT type=checkbox name=subject_science>
(physics <INPUT type=checkbox name=subject_physics>,
chemistry <INPUT type=checkbox name=subject_chemistry>,
astronomy <INPUT type=checkbox name=subject_astronomy>,
biology <INPUT type=checkbox name=subject_biology>,
geology <INPUT type=checkbox name=subject_geology>),
mathematics <INPUT type=checkbox name=subject_mathematics>
(arithmetic <INPUT type=checkbox name=subject_arithmetic>,
algebra <INPUT type=checkbox name=subject_algebra>,
geometry <INPUT type=checkbox name=subject_geometry>),
history <INPUT type=checkbox name=subject_history>,
social studies <INPUT type=checkbox name=subject_social_studies>,
home science <INPUT type=checkbox name=subject_home_science>,
agriculture <INPUT type=checkbox name=subject_agriculture>,
commerce <INPUT type=checkbox name=subject_commerce>,
culture and customs <INPUT type=checkbox name=subject_culture_and_customs>,
general knowledge <INPUT type=checkbox name=subject_general_knowledge>,
food and nutrition <INPUT type=checkbox name=subject_food_and_nutrition>,
arts and crafts <INPUT type=checkbox name=subject_arts_and_crafts>,
computer literacy <INPUT type=checkbox name=subject_computer_literacy>,
games <INPUT type=checkbox name=subject_games>,
stories <INPUT type=checkbox name=subject_stories>,
plays <INPUT type=checkbox name=subject_plays>,
with vocabulary <INPUT type=checkbox name=subject_with_vocabulary>,
environmental science <INPUT type=checkbox name=subject_environmental_science>,

health care <INPUT type=checkbox name=subject_health_care>
(nursing <INPUT type=checkbox name=subject_nursing>,
reproductive health <INPUT type=checkbox name=subject_reproductive_health>,
children health <INPUT type=checkbox name=subject_children_health>),

women rights <INPUT type=checkbox name=subject_women_rights>,

Kannada <INPUT type=checkbox name=subject_Kannada>,
Tamil <INPUT type=checkbox name=subject_Tamil>,
Bengali <INPUT type=checkbox name=subject_Bengali>,
Marathi <INPUT type=checkbox name=subject_Marathi>,
Punjabi <INPUT type=checkbox name=subject_Punjabi>,
Urdu <INPUT type=checkbox name=subject_Urdu>,
Nepali <INPUT type=checkbox name=subject_Nepali>,
children program <INPUT type=checkbox name=subject_children_program>,
<BR>
other subject (specify):
<INPUT TYPE="TEXT" NAME="subject_other" SIZE="20">
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
<OPTION>textbook
<OPTION>course_materials
<OPTION>monitoring
<OPTION>visits
<OPTION>documentary
<OPTION>supplementary
<OPTION>public_awareness
<OPTION>other_TV
<OPTION>workshop
<OPTION>radio_program
<OPTION>support_software
<OPTION>teacher_training
<OPTION>staff_training
<OPTION>community_training
<OPTION>interview
<OPTION>student_projects
<OPTION>compilation
<OPTION>homework_submission
<OPTION>homework_feedback
<OPTION>social_entertainment
<OPTION>information
<OPTION>chat
<OPTION>requests
<OPTION>questions
<OPTION>answers
<OPTION>exam
<OPTION>scratch_space
<OPTION>tmp
<OPTION>other
</SELECT>
<P>

<LI>
<U>language</U> (check all that apply):
English <INPUT type=checkbox name=language_English>, 
Hindi <INPUT type=checkbox name=language_Hindi>,
Kannada <INPUT type=checkbox name=language_Kannada>,
Tamil <INPUT type=checkbox name=language_Tamil>,
Bengali <INPUT type=checkbox name=language_Bengali>,
Marathi <INPUT type=checkbox name=language_Marathi>,
Punjabi <INPUT type=checkbox name=language_Punjabi>,
Urdu <INPUT type=checkbox name=language_Urdu>,
Nepali <INPUT type=checkbox name=language_Nepali>,
Telegu <INPUT type=checkbox name=language_Telegu>,
Gujarati <INPUT type=checkbox name=language_Gujarati>,
Kashmiri <INPUT type=checkbox name=language_Kashmiri>,
other language (specify):
<INPUT TYPE="TEXT" NAME="language_other" SIZE="20">
<P>

<LI>
<U>for class</U>:
<SELECT NAME="class" VALUE="unknown">
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
<P>


<LI>
<U>applicable age</U>: 
from
<SELECT NAME="age_from" VALUE="unknown">
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
<SELECT NAME="age_to" VALUE="unknown">
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

<LI>
<U>media type</U> (check all that apply):
video <INPUT type=checkbox name=media_video>, 
(DVD <INPUT type=checkbox name=media_DVD>, 
VCD <INPUT type=checkbox name=media_VCD>,
extracted by firewire <INPUT type=checkbox name=media_extracted_by_firewire>,
recorded by Plextor <INPUT type=checkbox name=media_recorded_by_Plextor>,
recorded from TV <INPUT type=checkbox name=media_recorded_from_TV>,
from YouTube <INPUT type=checkbox name=media_from_YouTube>,
VHS tape digitized <INPUT type=checkbox name=media_VHS_tape_digitized>,
recorded by webcam <INPUT type=checkbox name=media_recorded_by_webcam>,
recorded by Mustek <INPUT type=checkbox name=media_recorded_by_Mustek>,
recorded by Aiptek <INPUT type=checkbox name=media_recorded_by_Aiptek>,
recorded by CamStudio <INPUT type=checkbox name=media_recorded_by_CamStudio>,
created by ProShow <INPUT type=checkbox name=media_created_by_ProShow>,
has subtitle <INPUT type=checkbox name=media_has_subtitle>,
SMIL <INPUT type=checkbox name=media_SMIL>),
audio without video <INPUT type=checkbox name=media_audio_without_video>,
Flash <INPUT type=checkbox name=media_Flash>, 
images <INPUT type=checkbox name=media_images>, 
powerpoint <INPUT type=checkbox name=media_powerpoint>, 
documents <INPUT type=checkbox name=media_documents>,
executables <INPUT type=checkbox name=media_executables>,
slideshows <INPUT type=checkbox name=media_slideshows>,
<br>
other type (specify):
<INPUT TYPE="TEXT" NAME="media_other" SIZE="20">
<P>

<LI>
<U>video resolution</U> (width in pixels):
<SELECT NAME="video_resolution" VALUE="unknown">
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
<U>content duration</U>:
hour
<SELECT NAME="time_length_hours" VALUE="unknown">
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
minutes
<SELECT NAME="time_length_minutes" VALUE="unknown">
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

<OPTION>21
<OPTION>22
<OPTION>23
<OPTION>24
<OPTION>25
<OPTION>26
<OPTION>27
<OPTION>28
<OPTION>29
<OPTION>30

<OPTION>31
<OPTION>32
<OPTION>33
<OPTION>34
<OPTION>35
<OPTION>36
<OPTION>37
<OPTION>38
<OPTION>39
<OPTION>40

<OPTION>41
<OPTION>42
<OPTION>43
<OPTION>44
<OPTION>45
<OPTION>46
<OPTION>47
<OPTION>48
<OPTION>49
<OPTION>50

<OPTION>51
<OPTION>52
<OPTION>53
<OPTION>54
<OPTION>55
<OPTION>56
<OPTION>57
<OPTION>58
<OPTION>59

</SELECT>


seconds
<SELECT NAME="time_length_seconds">

<OPTION SELECTED>0
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

<OPTION>21
<OPTION>22
<OPTION>23
<OPTION>24
<OPTION>25
<OPTION>26
<OPTION>27
<OPTION>28
<OPTION>29
<OPTION>30

<OPTION>31
<OPTION>32
<OPTION>33
<OPTION>34
<OPTION>35
<OPTION>36
<OPTION>37
<OPTION>38
<OPTION>39
<OPTION>40

<OPTION>41
<OPTION>42
<OPTION>43
<OPTION>44
<OPTION>45
<OPTION>46
<OPTION>47
<OPTION>48
<OPTION>49
<OPTION>50

<OPTION>51
<OPTION>52
<OPTION>53
<OPTION>54
<OPTION>55
<OPTION>56
<OPTION>57
<OPTION>58
<OPTION>59

</SELECT>
<P>



<LI>
<U>data size</U>:
<INPUT TYPE="TEXT" NAME="size_text" SIZE="6">
<SELECT NAME="size_unit" VALUE="MB">
<OPTION>MB
<OPTION>KB
<OPTION>B
</SELECT>
<P>



<LI>
<U>content alias</U> (small number of characters):
<INPUT TYPE="TEXT" NAME="content_alias" SIZE="20">
<P>

<LI>
<U>chapter number</U>:
<INPUT TYPE="TEXT" NAME="chapter_number" SIZE="10">
<P>

<LI>
<U>related content</U>:
<INPUT TYPE="TEXT" NAME="related_content" SIZE="40">
<P>

<LI>
<U>show</U>: copyrighted <INPUT TYPE=checkbox NAME=show_copyrighted>,
discreet <INPUT TYPE=checkbox NAME=show_discreet>
<P>

<LI>
<U>cache</U>: sticky <INPUT TYPE=checkbox NAME=cache_sticky>
<P>

<LI>
<U>teacher/author</U> (person name):<INPUT TYPE="TEXT" NAME="author_name" SIZE="40">
<P>

<LI>
<U>uploaded by</U> (person name):<INPUT TYPE="TEXT" NAME="uploaded_by_name" SIZE="40">
<P>

<LI>
<U>uploaded by</U> (site name):<INPUT TYPE="TEXT" NAME="uploaded_by_site" SIZE="40" VALUE="%(userName)s">
<P>




<LI>
<U>date and time</U>:
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
<INPUT TYPE="submit" VALUE="Upload"> <INPUT type="reset" value="Clear All">
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

# this gets year and user name
dict = ryw.get_misc_dict()
dict.update(ryw_customize.dict)
bothStr3 = bothStr3part % dict




