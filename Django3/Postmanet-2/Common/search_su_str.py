import ryw_customize



pageStrx = """<HTML>
<HEAD>
<TITLE>Search the Content Repository</TITLE>
</HEAD>

<BODY>

<CENTER>
<A HREF="/index.html">
<IMG SRC="%(smallLogoFileName)s" BORDER=0 %(smallLogoDimension)s></A>
<BR>

<H3>Search the Content Repository</H3>

Specify the attributes you want to search on.
<P>

<TABLE BORDER=0 WIDTH=800><TR><TD>

<FORM ACTION="/cgi-bin/search_su.py" METHOD="post"
ENCTYPE="multipart/form-data">

<CENTER>
<INPUT TYPE="submit" VALUE="Search"> <INPUT type="reset" value="Clear All">
<P>
</CENTER>
<BR>


<TABLE BORDER=0>
<TR><TD WIDTH=1></TD>
<TD>

<UL>

<!-- textfield contains any/all of the words -->
<LI>
<U>all fields</U>:
<INPUT TYPE="TEXT" NAME="all_keys_concatenated" SIZE=120>
<BR>
<INPUT TYPE="RADIO" NAME="all_keys_concatenated_match_any_or_all" checked value="all"> Match all words
<INPUT TYPE="RADIO" NAME="all_keys_concatenated_match_any_or_all" value="any"> Match any word
<BR>
<INPUT TYPE="RADIO" NAME="all_keys_concatenated_case" checked value="insensitive"> Case-Insensitive
<INPUT TYPE="RADIO" NAME="all_keys_concatenated_case" value="sensitive"> Case-Sensitive
<P>


<!-- textfield contains any/all of the words -->
<LI>
<U>title</U>:
<INPUT TYPE="TEXT" NAME="title" SIZE=120>
<BR>
<INPUT TYPE="RADIO" NAME="title_match_any_or_all" checked value="all"> Match all words
<INPUT TYPE="RADIO" NAME="title_match_any_or_all" value="any"> Match any word
<BR>
<INPUT TYPE="RADIO" NAME="title_case" checked value="insensitive"> Case-Insensitive
<INPUT TYPE="RADIO" NAME="title_case" value="sensitive"> Case-Sensitive
<P>

<!-- textfield contains any/all of the words -->
<LI>
<U>description</U>:
<INPUT TYPE="TEXT" NAME="description" SIZE=120>
<BR>
<INPUT TYPE="RADIO" NAME="description_match_any_or_all" checked value="all"> Match all words
<INPUT TYPE="RADIO" NAME="description_match_any_or_all" value="any"> Match any word
<BR>
<INPUT TYPE="RADIO" NAME="description_case" checked value="insensitive"> Case-Insensitive
<INPUT TYPE="RADIO" NAME="description_case" value="sensitive"> Case-Sensitive
<P>

<!-- listvalue contains any/all checked -->
<LI>
<U>subjects</U>:
<BR>
English <INPUT type=checkbox name=subject_English>, 
Hindi <INPUT type=checkbox name=subject_Hindi>, 
Sanskrit <INPUT type=checkbox name=subject_Sanskrit>, <BR>
science <INPUT type=checkbox name=subject_science>
(physics <INPUT type=checkbox name=subject_physics>,
chemistry <INPUT type=checkbox name=subject_chemistry>,
astronomy <INPUT type=checkbox name=subject_astronomy>,
biology <INPUT type=checkbox name=subject_biology>,
geology <INPUT type=checkbox name=subject_geology>),<BR>
mathematics <INPUT type=checkbox name=subject_mathematics>
(arithmetic <INPUT type=checkbox name=subject_arithmetic>,
algebra <INPUT type=checkbox name=subject_algebra>
geometry <INPUT type=checkbox name=subject_geometry>),<BR>
history <INPUT type=checkbox name=subject_history>,
social studies <INPUT type=checkbox name=subject_social_studies>,
home science <INPUT type=checkbox name=subject_home_science>,
agriculture <INPUT type=checkbox name=subject_agriculture>,
general knowledge <INPUT type=checkbox name=subject_general_knowledge>,<BR>
food and nutrition <INPUT type=checkbox name=subject_food_and_nutrition>,
arts and crafts <INPUT type=checkbox name=subject_arts_and_crafts>,
computer literacy <INPUT type=checkbox name=subject_computer_literacy>,
games <INPUT type=checkbox name=subject_games>,
stories <INPUT type=checkbox name=subject_stories>,
plays <INPUT type=checkbox name=subject_plays>,
with vocabulary <INPUT type=checkbox name=subject_with_vocabulary>,
environmental science<INPUT type=checkbox name=subject_environmental_science>,

health care<INPUT type=checkbox name=subject_health_care>,
(nursing <INPUT type=checkbox name=subject_nursing>,
reproductive health<INPUT type=checkbox name=subject_reproductive_health>,
children health<INPUT type=checkbox name=subject_children_health>),

women rights<INPUT type=checkbox name=subject_women_rights>,

Kannada <INPUT type=checkbox name=subject_Kannada>,
Tamil <INPUT type=checkbox name=subject_Tamil>,
Bengali <INPUT type=checkbox name=subject_Bengali>,
Marathi <INPUT type=checkbox name=subject_Marathi>,
Punjabi <INPUT type=checkbox name=subject_Punjabi>,
<BR>
other subject (specify):
<INPUT TYPE="TEXT" NAME="subject_other" SIZE="20">
<BR>
<INPUT TYPE="RADIO" NAME="subjects_match_any_or_all" checked value="all"> Match all
<INPUT TYPE="RADIO" NAME="subjects_match_any_or_all" value="any"> Match any
<P>

<!-- equals, if not unknown -->
<LI>
<U>content type</U>:
<SELECT NAME="content_type" VALUE="unknown">
<OPTION>unknown
<OPTION>lecture
<OPTION>courseware
<OPTION>practicals
<OPTION>experiments
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
<OPTION>teacher_training
<OPTION>staff_training
<OPTION>community_training
<OPTION>chat
<OPTION>interview
<OPTION>student_projects
<OPTION>compilation
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
<P>

<!-- listvalue contains any/all checked -->
<LI>
<U>languages</U>:
English <INPUT type=checkbox name=language_English>, 
Hindi <INPUT type=checkbox name=language_Hindi>,
Kannada <INPUT type=checkbox name=language_Kannada>,
Tamil <INPUT type=checkbox name=language_Tamil>,
Bengali <INPUT type=checkbox name=language_Bengali>,
Marathi <INPUT type=checkbox name=language_Marathi>,
Punjabi <INPUT type=checkbox name=language_Punjabi>,
Telegu <INPUT type=checkbox name=language_Telegu>,
Gujarati <INPUT type=checkbox name=language_Gujarati>,
Kashmiri <INPUT type=checkbox name=language_Kashmiri>,
Other language (specify):
<INPUT TYPE="TEXT" NAME="language_other" SIZE="20">
<BR>
<INPUT TYPE="RADIO" NAME="languages_match_any_or_all" checked value="all"> Match all
<INPUT TYPE="RADIO" NAME="languages_match_any_or_all" value="any"> Match any
<P>

<!-- equals, if not unknown -->
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


<!-- bracket -->
<!-- IGNORED
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
IGNORED -->

<!-- listvalue contains any/all checked -->
<LI>
<U>media type</U>:
video <INPUT type=checkbox name=media_video>, 
(DVD <INPUT type=checkbox name=media_DVD>, 
VCD <INPUT type=checkbox name=media_VCD>,
extracted by firewire <INPUT type=checkbox name=media_extracted_by_firewire>,
recorded by Plextor <INPUT type=checkbox name=media_recorded_by_Plextor>,
recorded from TV <INPUT type=checkbox name=media_recorded_from_TV>,
VHS tape digitized <INPUT type=checkbox name=media_VHS_tape_digitized>,
recorded by webcam <INPUT type=checkbox name=media_recorded_by_webcam>,
recorded by Mustek <INPUT type=checkbox name=media_recorded_by_Mustek>,
recorded by Aiptek <INPUT type=checkbox name=media_recorded_by_Aiptek>,
recorded by CamStudio <INPUT type=checkbox name=media_recorded_by_CamStudio>,
created by ProShow <INPUT type=checkbox name=media_created_by_ProShow>,
has subtitle <INPUT type=checkbox name=media_has_subtitle>,
SMIL <INPUT type=checkbox name=media_SMIL>),
audio (without video) <INPUT type=checkbox name=media_audio_without_video>,<BR>
flash <INPUT type=checkbox name=media_Flash>, 
images <INPUT type=checkbox name=media_images>, 
powerpoint <INPUT type=checkbox name=media_powerpoint>, 
documents <INPUT type=checkbox name=media_documents>,
executables <INPUT type=checkbox name=media_executables>,
slideshows <INPUT type=checkbox name=media_slideshows>,
<br>
other type (specify):
<INPUT TYPE="TEXT" NAME="media_other" SIZE="20">
<BR>
<INPUT TYPE="RADIO" NAME="media_match_any_or_all" checked value="all"> Match all
<INPUT TYPE="RADIO" NAME="media_match_any_or_all" value="any"> Match any
<P>

<!-- equals, if not unknown -->
<LI>
<U>video resolution</U>:
<SELECT NAME="video_resolution" VALUE="unknown">
<OPTION>unknown
<OPTION>320
<OPTION>350
<OPTION>640
<OPTION>720
<OPTION>1024
<OPTION>huge
</SELECT>
<P>

<!-- bracket -->
<LI>
<U>content duration</U>:
<INPUT TYPE="RADIO" NAME="duration_constraint" checked value="at_least"> At least
<INPUT TYPE="RADIO" NAME="duration_constraint" value="equals"> Equals
<INPUT TYPE="RADIO" NAME="duration_constraint" value="at_most"> At most
<SELECT NAME="duration_hours" VALUE="unknown">
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
hours
<SELECT NAME="duration_minutes" VALUE="unknown">
<OPTION>unknown
<OPTION>0
<OPTION>10
<OPTION>20
<OPTION>30
<OPTION>40
<OPTION>50
</SELECT>
minutes
<P>

<!-- nocase, contains all words -->
<LI>
<U>author</U> (person name):<INPUT TYPE="TEXT" NAME="author_name" SIZE="40">
<P>

<!-- nocase, contains all words -->
<LI>
<U>uploaded by</U> (person name):<INPUT TYPE="TEXT" NAME="uploaded_by_name" SIZE="40">
<P>

<LI>
<U>object ID</U>:
<INPUT TYPE="TEXT" NAME="object_ID" SIZE="40">
<P>

<LI>
<U>uploaded on or after</U>:
Year <SELECT NAME="uploaded_after_year" VALUE="None">
<OPTION>None <OPTION>2005 <OPTION>2006 <OPTION>2007
</SELECT>
Month <SELECT NAME="uploaded_after_month" VALUE="None">
<OPTION>None <OPTION>1 <OPTION>2 <OPTION>3 <OPTION>4 <OPTION>5 <OPTION>6
<OPTION>7 <OPTION>8 <OPTION>9 <OPTION>10 <OPTION>11 <OPTION>12
</SELECT>
Day <SELECT NAME="uploaded_after_day" VALUE="None">
<OPTION>None
<OPTION>1 <OPTION>2 <OPTION>3 <OPTION>4 <OPTION>5 <OPTION>6 <OPTION>7 <OPTION>8 <OPTION>9 <OPTION>10
<OPTION>11 <OPTION>12 <OPTION>13 <OPTION>14 <OPTION>15 <OPTION>16 <OPTION>17 <OPTION>18 <OPTION>19 <OPTION>20
<OPTION>21 <OPTION>22 <OPTION>23 <OPTION>24 <OPTION>25 <OPTION>26 <OPTION>27 <OPTION>28 <OPTION>29 <OPTION>30
<OPTION>31
</SELECT>
<P>

<LI>
<U>uploaded on or before</U>:
Year <SELECT NAME="uploaded_before_year" VALUE="None">
<OPTION>None <OPTION>2005 <OPTION>2006 <OPTION>2007
</SELECT>
Month <SELECT NAME="uploaded_before_month" VALUE="None">
<OPTION>None <OPTION>1 <OPTION>2 <OPTION>3 <OPTION>4 <OPTION>5 <OPTION>6
<OPTION>7 <OPTION>8 <OPTION>9 <OPTION>10 <OPTION>11 <OPTION>12
</SELECT>
Day <SELECT NAME="uploaded_before_day" VALUE="None">
<OPTION>None
<OPTION>1 <OPTION>2 <OPTION>3 <OPTION>4 <OPTION>5 <OPTION>6 <OPTION>7 <OPTION>8 <OPTION>9 <OPTION>10
<OPTION>11 <OPTION>12 <OPTION>13 <OPTION>14 <OPTION>15 <OPTION>16 <OPTION>17 <OPTION>18 <OPTION>19 <OPTION>20
<OPTION>21 <OPTION>22 <OPTION>23 <OPTION>24 <OPTION>25 <OPTION>26 <OPTION>27 <OPTION>28 <OPTION>29 <OPTION>30
<OPTION>31
</SELECT>
<P>

<LI>
<U>Sort results by</U>:
<INPUT TYPE="RADIO" NAME="sort_order" checked value="increasing"> Increasing
<INPUT TYPE="RADIO" NAME="sort_order" value="decreasing"> Decreasing
<SELECT NAME="sort_field" VALUE="Upload_Time">
<OPTION>Upload_Time
<OPTION>Title
<OPTION>Author_Name
</SELECT>
<P>


</UL>

</TD>
</TR>
</TABLE>


<CENTER>
<INPUT TYPE="submit" VALUE="Search"> <INPUT type="reset" value="Clear All">
</center>

<INPUT TYPE="HIDDEN" NAME="start_index" VALUE="0">

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


pageStr = pageStrx % ryw_customize.dict

