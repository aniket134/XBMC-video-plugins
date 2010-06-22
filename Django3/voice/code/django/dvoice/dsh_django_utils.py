from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.forms.fields import email_re
import sys,os,subprocess,shutil,datetime,time,logging,operator
import dvoice.db.models
#from dvoice.db.models import Organization, Person, Item, KeyWord, Event
import dsh_django_config,dsh_django_utils2
dsh_django_utils2.append_to_sys_path(
    dsh_django_config.lookup('DSH_VOICE_CODE_DIR'))
import dsh_utils,dsh_config,dsh_agi
import dsh_common_db,dsh_common_agi



def unknown_thumbnail(obj):
    if isinstance(obj, dvoice.db.models.Person):
        return dsh_django_config.lookup('DSH_UNKNOWN_HEAD_URL')
    elif isinstance(obj, dvoice.db.models.Organization):
        return dsh_django_config.lookup('DSH_UNKNOWN_ORG_URL')
    else:
        raise Exception('dsh_django_utils.unknown_thumbnail(): fix me')
    


def thumbnail(self, picField):
    """Display thumbnail-size image of ImageField named mugshot.
    Assumes images are not very large (i.e. no manipulation of
    the image is done on backend).
    Requires constant named MAX_THUMB_LENGTH to limit longest axis.
    taken and modified from:
    http://www.djangosnippets.org/snippets/162/
    this is displayed only in the list view.
    in the edit view, it's handled elsewhere.
    """

    if not picField:
        return unknown_thumbnail(self)
        
    url = picField.url
    fsPath = dsh_agi.url_to_fs_path(url)
    debug_event('dsh_django_utils.thumbnail(): fsPath: ' + fsPath, 9)
    if not dsh_utils.is_valid_file(fsPath, silent=True):
        error_event('dsh_django_utils.thumbnail(): missing thumbnail: ' +\
                    fsPath, errorLevel='WRN', item=self)
        return unknown_thumbnail(self)    
    
    width = picField.width
    height = picField.height
    maxCurrDim = max(width, height)
    maxDim = dsh_django_config.lookup('MAX_THUMB_DIMENSION')
    ratio = maxCurrDim > maxDim and float(maxCurrDim) / maxDim or 1
    thumbWidth = width / ratio
    thumbHeight = height / ratio

    return ('<center><img src="%s" width="%s" height="%s" title="%s" />' +
            '</center>') % (url, thumbWidth, thumbHeight, '')



def is_mp3(url):
    return url.endswith('.mp3') or url.endswith('.MP3')



def mp3_widget(url, owner=None, fileName=''):
    text = ''
    if owner:
        text = owner
    elif fileName:
        text = fileName
    if is_mp3(url):
        #
        # answer1 uses the mp3 player with a graphic play and pause sign.
        # not good enough: because you can't go back to beginning.
        # can't seek.
        # if I want to use this, I must modify base.html to
        # include the javascripts that are commented out.
        #
        answer1 = ('<ul class="graphic"><li style="list-style-type:none">' +
                   '<a href="%s">%s</a></li></ul>') % \
                   (url, text)
        #
        # answer2 uses the page-player, has a seek bar. so can go back.
        # need to deal with base.html javascript includes if want to
        # switch to some other player.
        #
        # used to use the owner as the link anchor.
        #
        #answer2 = ('<ul class="playlist"><li>' +
        #           '<a href="%s"><font size=2>%s</font></a></li></ul>') % \
        #           (url, text)
        playPauseIcon = dsh_django_config.lookup('PLAY_PAUSE_ICON')
        answer2 = ('<ul class="playlist"><li>' +
                   '<a href="%s"><font size=2>%s</font></a></li></ul>') % \
                   (url, playPauseIcon)
        return answer2
    displayText = os.path.basename(url)
    fileIcon = dsh_django_config.lookup('FILE_ICON')
    #return '<a href="%s">%s</a>' % (url,displayText)
    return '<center><a href="%s">%s</a></center>' % (url,fileIcon)



def item_file_list(self, fileField, spokenName=False):
    """modeled after thumbnail() above.
    eventually replaced by an embedded player for mp3.
    spokenName=True when called by the displayed fields from Person and
    Organization.
    """
    
    if not fileField:
        return ''
    url = fileField.url
    #return '<a href="%s">%s</a>' % (url,url)
    if spokenName:
        owner = None
    else:
        owner = self.owner
    return mp3_widget(url, owner)
    


#
# the next two functions taken from:
# http://www.psychicorigami.com/2009/06/20/django-simple-admin-imagefield-thumbnail/
#
# for displaying picture on the edit object page.
#
class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            imageUrl = value.url
            fileName=str(value)
            output.append((u' <a href="%s" target="_blank">' +
                          u'<img src="%s" alt="%s" /></a> %s ') % \
                          (imageUrl, imageUrl, fileName, _('Change:')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))



def displayEditImageField(selfObj, dbField, kwargs, imageFieldName, superObj,
                          widgetType='image'):
    if dbField.name == imageFieldName:
        if widgetType == 'image':
            kwargs['widget'] = AdminImageWidget
        elif widgetType == 'mp3':
            kwargs['widget'] = AdminMp3Widget
        else:
            raise Exception('displayEditImageField: unknown widget type')
        try:
            del kwargs['request']
        except KeyError:
            pass
        return dbField.formfield(**kwargs)
    return superObj.formfield_for_dbfield(dbField, **kwargs)



def displayEditImageField2(selfObj, dbField, kwargs, superObj,
                           fieldName1, widgetType1,
                           fieldName2, widgetType2):
    """called by admin.PersonAdmin.
    modeled after displayEditImageField() above.
    but now allows two fields: one thumbnail and one spoken_name.
    """

    if dbField.name == fieldName1:
        return displayEditImageField(selfObj, dbField, kwargs,
                                     fieldName1, superObj, widgetType1)

    if dbField.name == fieldName2:
        return displayEditImageField(selfObj, dbField, kwargs,
                                     fieldName2, superObj, widgetType2)

    return superObj.formfield_for_dbfield(dbField, **kwargs)



class AdminMp3Widget(AdminFileWidget):
    """modeled after the AdminImageWidget above.
    for displaying an mp3 player widget on the object edit page.
    used by admin.ItemAdmin."""
    
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            mp3Url = value.url
            fileName=str(value)
            spaces = '&nbsp;&nbsp;&nbsp;&nbsp;'
            output.append((mp3_widget(mp3Url, None, fileName) + '%s %s ') %
                          (spaces,_('Change:')))
            #output.append((u' <a href="%s" target="_blank">' +
            #              u'<img src="%s" alt="%s" /></a> %s ') % \
            #              (imageUrl, imageUrl, fileName, _('Change:')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))



def org_link(org):
    """called by Item and Person list views to display links to orgs."""
    if not org:
        return ''
    orgID = str(org.id)
    orgAlias = org.alias
    url = dsh_django_config.lookup('ORG_URL') + orgID
    url = '<a href=%s>%s</a>' % (url, orgAlias)
    return url
    


def person_link(person):
    """called by Item list view to display a link to the person."""
    if not person:
        return ''
    personID = str(person.id)
    personName = person.first_name + ' ' + person.last_name
    url = dsh_django_config.lookup('PERSON_URL') + personID
    url = '<a href=%s>%s</a>' % (url, personName)
    return url



def insert_event_after_upload_item(self, sessionID=''):
    event = dvoice.db.models.Event(etype='INF',
                                   action='UPLD',
                                   owner=self.owner,
                                   phone_number=self.owner.phone_number,
                                   rec_duration=self.rec_duration,
                                   call_duration=self.call_duration,
                                   dsh_uid_concerned=self.dsh_uid,
                                   session=sessionID)
    event.description = self.item_to_text()
    event.save()
    


def insert_event_after_delete_item(self, sessionID=''):
    event = dvoice.db.models.Event(etype='INF',
                                   action='IDEL',
                                   owner=self.owner,
                                   phone_number=self.owner.phone_number,
                                   rec_duration=self.rec_duration,
                                   call_duration=self.call_duration,
                                   dsh_uid_concerned=self.dsh_uid,
                                   session=sessionID)
    event.description = self.item_to_text()
    event.save()
    


def insert_event_after_org_add(self, sessionID=''):
    event = dvoice.db.models.Event(etype='INF',
                                   action='ORGN',
                                   dsh_uid_concerned=self.dsh_uid,
                                   session=sessionID)
    event.description = self.org_to_text()
    event.save()

    

def insert_event_after_org_del(self, sessionID=''):
    event = dvoice.db.models.Event(etype='INF',
                                   action='ORGD',
                                   dsh_uid_concerned=self.dsh_uid,
                                   session=sessionID)
    event.description = self.org_to_text()
    event.save()

    

def insert_event_after_person_add(self, sessionID=''):
    event = dvoice.db.models.Event(etype='INF',
                                   action='PRSN',
                                   dsh_uid_concerned=self.dsh_uid,
                                   phone_number=self.phone_number,
                                   session=sessionID)
    event.description = self.person_to_text()
    event.save()



def insert_event_after_person_del(self, sessionID=''):
    event = dvoice.db.models.Event(etype='INF',
                                   action='PRSD',
                                   dsh_uid_concerned=self.dsh_uid,
                                   phone_number=self.phone_number,
                                   session=sessionID)
    event.description = self.person_to_text()
    event.save()



def insert_event_after_keyword_add(self, sessionID=''):
    event = dvoice.db.models.Event(etype='INF',
                                   action='KEYW',
                                   dsh_uid_concerned=self.dsh_uid,
                                   session=sessionID)
    event.description = self.keyword_to_text()
    event.save()
    


def insert_event_after_keyword_del(self, sessionID=''):
    event = dvoice.db.models.Event(etype='INF',
                                   action='KEYD',
                                   dsh_uid_concerned=self.dsh_uid,
                                   session=sessionID)
    event.description = self.keyword_to_text()
    event.save()
    


def debug_event(message, tag, sessionID=''):
    currentPrintTag = dsh_django_config.lookup('DEBUG_PRINT_TAG')
    if tag != currentPrintTag:
        return
    event = dvoice.db.models.Event(etype = 'DBG',
                                   action = 'PRNT',
                                   debug_tag = tag,
                                   session=sessionID)
    event.description = message
    event.save()



def error_event(message, errorLevel='ERR', item=None, phone_number='',
                sessionID=''):
    if item:
        dsh_uid = item.dsh_uid
    else:
        dsh_uid = ''
    event = dvoice.db.models.Event(etype = errorLevel,
                                   action = 'RPRT',
                                   dsh_uid_concerned=dsh_uid,
                                   phone_number=phone_number,
                                   session=sessionID)
    event.description = message
    event.save()



def deactivate(item, recurse=False):
    """if the user is uploading an active object,
    we make all the previously active BROADCASTS inactive.
    used to be in Item.save()"""

    #oldActives = dvoice.db.models.Item.objects.filter(active=True, itype='B')
    dsh_common_db.deactivate(item, dvoice.db.models.Item, recurse=recurse)
    


def extract_duration(item):
    #
    # chicken out if can't be done.
    #
    if not item or not item.file:
        return
    ffmpegPath = dsh_django_config.lookup('FFMPEG_PATH')
    if not dsh_utils.is_valid_file(ffmpegPath, '', silent=True):
        error_event('dsh_django_utils.extract_duration: ' +
                    'ffmpeg does not exist: ' + ffmpegPath,
                    item=item)
        return
    

    #
    # get the file path.
    # path_prefix: /home/rywang/phone_data/django/
    # url: /media/voice/2009/07/test4_________.mp3
    # concatenate these two.
    #
    filePath = dsh_agi.make_abs_file_pathname(item.file.url)
    debug_event('dsh_django_utils.extract_duration: filePath: '+filePath, 5)

    #
    # construct the ffmpeg command and execute it.
    #
    command = ffmpegPath + ' -i ' + '"' + filePath + '"'
    debug_event('utils.extract_duration: command: ' + command, 4)
    ffmpegOut = dsh_utils.try_execute(command)
    if not ffmpegOut:
        error_event('dsh_django_utils.extract_duration: ffmpeg failed: ' +
                    command, item=item)
        return
    debug_event('utils.extract_durations: ffmpeg exec result: ' + ffmpegOut,
                4)

    #
    # try to extract.
    #
    durRegEx = dsh_django_config.lookup('FFMPEG_DURATION_PATTERN')
    durSeconds = dsh_utils.extract_duration(ffmpegOut, durRegEx)
    debug_event('utils.extract_durations: extracted result: ' +
                repr(durSeconds), 4)
    if durSeconds != None:
        item.rec_duration = durSeconds
    


def make_uploaded_file_name(item, filename):
    """called by models.Item after uploading a file."""

    #
    # the following is just a call to test the asterisk file name
    # generation path works.
    # we can't use this because i can't get all the details.
    # see below.
    #
    #return dsh_agi.make_full_unique_filename(
    #    item.dsh_uid, filename,
    #    phoneNumber='123', orgAlias='orgalias', name='myname', 
    #    startWithRoot=False, uploadType='asterisk')

    #
    # don't have the pointer to owner yet.
    # bummer.
    #
    #phoneNumber = item.owner.phone_number
    #if not phoneNumber:
    #    phoneNumber = dsh_config.lookup('UNKNOWN_PHONE_NUMBER')
    #
    #alias = item.owner.organization.alias
    #if not alias:
    #    alias = dsh_config.lookup('UNKNOWN_ORG_ALIAS')
    #alias = dsh_utils.strip_join_str(alias)
    #
    #name = item.owner.first_name + '-' + item.owner.last_name
    #if not name:
    #    name = 'UNKNOWN_PERSON_NAME'
    #name = dsh_utils.strip_join_str(alias)
    
    fullName = dsh_agi.make_full_unique_filename(
        item.dsh_uid, filename,
        startWithRoot=False,
        uploadType='django_voice')
    if not fullName:
        error_event('dsh_django_utils.make_uploaded_file_name failed:' +
                    filename, errorLevel='CRT', item=item)
        return filename
    return fullName



def make_uploaded_image_name(person, filename):
    """called by models.Person and Org after uploading a picture."""
    fullName = dsh_agi.make_full_unique_filename(
        person.dsh_uid, filename,
        name=person.__unicode__(),
        startWithRoot=False,
        uploadType='django_image')
    if not fullName:
        error_event('dsh_django_utils.make_uploaded_image_name failed: ' +
                    filename, errorLevel='CRT', item=person)
        return filename
    return fullName



def chmod_uploaded_file(field):
    """called by save() of Organization and Person."""

    if (not field) or (not field.file) or (not field.file.file) or \
           (not field.file.file.name):
        return

    fullName = field.file.file.name
    dsh_utils.chmod_tree2(fullName, recurse=False)
    debug_event('dsh_django_utils.chmod_uploaded_file: chmod: ' +\
                fullName, 20)



def convert_to_sln(item):
    convert_field_to_sln(item.file, item=item)
    return



def convert_field_to_sln(field, item=None):
    """rewritten from convert_to_sln().  used to take an argument of "item."
    now it takes a generic field, so I can use it for "spoken_name" of
    Person.
    when called from convert_to_sln(), item is not None.
    """
    
    debug_event('dsh_django_utils.convert_to_sln: entered...', 14)

    if not field or not field.url:
        return

    mp3FilePath = dsh_agi.make_abs_file_pathname(field.url)
    dsh_utils.chmod_tree2(mp3FilePath, recurse=False)
    debug_event('dsh_django_utils.convert_to_sln: chmod: ' + mp3FilePath, 20)

    if item:
        #
        # we only need to convert outgoing items.
        # so only "broadcast" or "personalized" messages need
        # to be converted.
        #
        if item.itype != 'B' and item.itype != 'P' and (not item.peer_shared):
            return
        
    url = field.url
    if not is_mp3(url):
        return
    debug_event('dsh_django_utils.convert_to_sln: going ahead: ' + url, 14)


    #
    # locate executables
    # we'll use ffmpeg to convert mp3 to wav.
    # then we'll use sox to convert wav to sln.
    #
    ffmpegPath = dsh_django_config.lookup('FFMPEG_PATH')
    if not dsh_utils.is_valid_file(ffmpegPath, '', silent=True):
        error_event('dsh_django_utils.convert_to_sln: ' +
                    'ffmpeg does not exist: ' + ffmpegPath,
                    item=item)
        return
    soxPath = dsh_django_config.lookup('SOX_PATH')
    if not dsh_utils.is_valid_file(soxPath, '', silent=True):
        error_event('dsh_django_utils.convert_to_sln: ' +
                    'sox does not exist: ' + soxPath,
                    item=item)
        return


    #
    # get the abs path of the containing dir.
    # make an sln subdir inside.
    #
    mp3FilePath = dsh_agi.make_abs_file_pathname(url)
    pathStuff = dsh_agi.figure_out_sln_names(url)
    if not pathStuff:
        error_event('dsh_django_utils.convert_to_sln: ' +
                    'convert_to_sln failed: cannot figure out paths: ' +
                    mp3FilePath,
                    errorLevel='CRT', item=item)
        return
    slnDir,slnBaseName,wavBaseName,fullSlnName,fullWavName = pathStuff
      
    if not dsh_utils.try_mkdir_ifdoesnt_exist(
        slnDir, 'dsh_django_utils.convert_to_sln: ' + slnDir):
        error_event('dsh_django_utils.convert_to_sln: ' +
                    'convert_to_sln failed: ' + slnDir,
                    errorLevel='CRT', item=item)
        return

    
    #
    # make ffmpeg command and try to execute it.
    #
    command = ffmpegPath + ' -i ' + '"' + mp3FilePath + '" ' + fullWavName
    debug_event('dsh_django_utils.convert_to_sln: ' +
                'ffmpeg command is: ' +
                command, 14)
    ffmpegResult = dsh_utils.try_execute(command)
    if not ffmpegResult:
        error_event('dsh_django_utils.convert_to_sln: ' +
                    'failed to execute ffmpeg: ' + command,
                    errorLevel='ERR', item=item)
        dsh_utils.cleanup_path(fullWavName, 'dsh_django_utils.convert_to_sln')
        return

    #
    # make sox command and try to execute it.
    #

    #
    # 09/12/13: on the Ideapad, the -w option doesn't seem to work.
    # according to the man page, it has something to do with "reverb."
    #
    #command = '%s %s -t raw -r 8000 -s -w -c 1 %s' % \
    #          (soxPath, fullWavName, fullSlnName)
    #
    command = '%s %s -t raw -r 8000 -s -c 1 %s' % \
              (soxPath, fullWavName, fullSlnName)
    debug_event('dsh_django_utils.convert_to_sln: ' +
                'sox command is: ' +
                command, 14)
    soxResult = dsh_utils.try_execute(command)
    if soxResult == None:
        error_event('dsh_django_utils.convert_to_sln: ' +
                    'failed to execute sox: ' + command,
                    errorLevel='ERR', item=item)
        dsh_utils.cleanup_path(fullSlnName, 'dsh_django_utils.convert_to_sln')
        
    dsh_utils.chmod_tree2(fullSlnName, recurse=False)
    debug_event('dsh_django_utils.convert_to_sln: chmod: ' + fullSlnName, 20)
    
    dsh_utils.cleanup_path(fullWavName, 'dsh_django_utils.convert_to_sln')



def newest_red5_stream():
    """called by views.reply()."""

    streamDir = dsh_config.lookup('RED5_STREAMS_DIR')
    newest = dsh_utils.newest_file_in_dir(streamDir, '.flv')
    return newest



def get_host_port(request):
    meta = request.META
    if not meta.has_key('HTTP_HOST'):
        return None
    hostPort = meta['HTTP_HOST']
    if not hostPort:
        return None
    two = hostPort.split(':')
    if len(two) != 2:
        return None
    return two
    


def convert_red5_flv_to_mp3(name):
    
    response = ''
    red5Dir = dsh_config.lookup('RED5_STREAMS_DIR')
    flvPath = os.path.join(red5Dir, name + '.flv')

    if not dsh_utils.is_valid_file(flvPath, silent=True):
        message = 'file does not exist: ' + flvPath
        error_event(message, errorLevel='ERR')
        response += dsh_utils.red_error_break_msg(message)
        return (False,response,None)
    
    red5TmpDir = os.path.join(red5Dir, 'tmp')
    
    if not dsh_utils.try_mkdir_ifdoesnt_exist(
        red5TmpDir, 'dsh_django_utils.convert_red5_flv_to_mp3: '):
        message = 'dsh_django_utils.convert_red5_flv_to_mp3: ' + \
                  'failed to make tmp dir: ' + red5TmpDir
        error_event(message, errorLevel='CRT')
        response += dsh_utils.red_error_break_msg(message)
        return (False, response, None)

    wavPath = os.path.join(red5TmpDir, name + '.wav')
    ffmpegPath = dsh_config.lookup('ffmpeg_location')
    command = ffmpegPath + ' -i ' + flvPath + ' ' + wavPath
    ffmpegResult = dsh_utils.try_execute(command)

    if not ffmpegResult:
        message = 'dsh_django_utils.convert_red5_flv_to_mp3: ffmpeg failed: '+\
                  command
        error_event(message, errorLevel='CRT')
        response += dsh_utils.red_error_break_msg(message)
        return (False, response, None)
    
    response += dsh_utils.black_break_msg_debug(
        'dsh_django_utils.convert_red5_flv_to_mp3: wav success: ' + wavPath,
        113)

    mp3Path = os.path.join(red5TmpDir, name + '.mp3')
    lamePath = dsh_config.lookup('lame_location')
    mp3Quality = dsh_config.lookup('lame_mp3_quality')
    command = lamePath + mp3Quality + wavPath + ' ' + mp3Path
    lameResult = dsh_utils.try_execute(command)

    if not lameResult:
        message = 'dsh_django_utils.convert_red5_flv_tomp3: lame failed: ' +\
                  command
        error_event(message, errorLevel='CRT')
        response += dsh_utils.red_error_break_msg(message)
        return (False, response, None)
    
    response += dsh_utils.black_break_msg_debug(
        'dsh_django_utils.convert_red5_flv_to_mp3: mp3 success: ' + mp3Path,
        113)

    return (True, response, mp3Path)



def get_foreign_key(whatKind, dshUid, quiet=False):
    """called by load_one().  locate a foreign key object.
    moved from dsh_dump()."""
    objs = whatKind.objects.filter(dsh_uid=dshUid)
    l = len(objs)
    if l == 0:
        if not quiet:
            dsh_utils.give_bad_news(
                'dsh_dump.get_foreign_key: dsh_uid not found: ' + dshUid,
                logging.error)
        return None
    if l > 1:
        dsh_utils.give_bad_news(
            'dsh_dump.get_foreign_key: non-unique dsh_uid: ' + dshUid,
            logging.critical)
        return None
    return objs[0]    
    


def get_original_message_owner(originalItemDshUid):
    """called by save_red5_mp3_in_django()."""
    response = ''
    item = get_foreign_key(dvoice.db.models.Item, originalItemDshUid)
    if not item:
        message = 'dsh_django_utils.get_original_message_owner: ' +\
                  'failed to find original owner: ' + originalItemDshUid
        response += dsh_utils.red_error_break_msg(message)
        error_event(message, errorLevel='CRT')
        return (False, response, None, item)
    response = dsh_utils.black_break_msg_debug(
        'dsh_django_utils.get_original_message_owner: original owner: ' +
        item.owner.dsh_uid, 113)
    return (True, response, item.owner, item)



def save_red5_mp3_in_django(mp3Path, originalItemDshUid=None,
                            copyBlankReply=False):
    """called by views.reply_submit() and views.save_submit().
    originalItemDshUid is None if from save_submit().
    10/03/06: copyBlankReply=True when this is called by
    dsh_common_views.reply_upload_submit().
    """

    response = ''


    #
    # get the original owner.
    #
    if originalItemDshUid:
        success,resp,originalOwner,originalItem = \
            get_original_message_owner(originalItemDshUid)
        response += resp
        if not success:
            audienceList = []
        else:
            audienceList = [originalOwner]
    else:
        audienceList = []
        originalItem = None
        

    #
    # need to init the log because of the next call to
    # init_unknown_org_person(), which uses the log.
    # need to get the unknown person because that's needed
    # as an owner of the django item, which is in turn
    # required to get a dsh_uid, which is in turn
    # required to make the file name.
    #
    dsh_agi.init_log()
    unknownOrg,unknownPerson = dsh_agi.init_unknown_org_person()


    #
    # figure out the destination directory:
    # final resting place in the django database.
    #
    item = dvoice.db.models.Item(
        owner = unknownPerson,
        itype = 'P')

    
    #
    # figure out what file name to use.
    #
    if mp3Path:
        useThisName = mp3Path
    else:
        useThisName = dsh_common_db.blank_reply_path()
    baseName = os.path.basename(useThisName)
    shortName = make_uploaded_file_name(item, baseName)


    response += dsh_utils.black_break_msg_debug(
        'dsh_django_utils.save_red5_mp3_in_django: voice name: ' +
        shortName, 113)
    mediaDir = dsh_config.lookup('MEDIA_DIR')
    djangoFullName = os.path.join(mediaDir, shortName)


    #
    # try to move from red5 into django.
    #
    if not dsh_utils.try_mkdir_ifdoesnt_exist(
        os.path.dirname(djangoFullName),
        'dsh_django_utils.save_red5_mp3_in_django: '):
        message = 'dsh_django_utils.save_red5_mp3_in_django: ' + \
                  'try_mkdir_ifdoesnt_exist failed: ' + \
                  os.path.dirname(djangoFullName)
        response += dsh_utils.red_error_break_msg(message)
        error_event(message, errorLevel='CRT')
        return (False, response)

    
    #
    # 10/03/06:
    # copy blank reply instead of from red5
    #
    if copyBlankReply:
        success,copyResp = dsh_common_db.copy_blank_reply_into_django(
            djangoFullName)
        if not success:
            response += copyResp
            return (False, response)
        else:
            pass
    else:
        #
        # we are not copying blank reply, so we're copying from red5.
        #
        try:
            shutil.move(mp3Path, djangoFullName)
        except:
            message = 'dsh_django_utils.save_red5_mp3_in_django: ' +\
                      'file move failed: ' + mp3Path + ' -> ' + djangoFullName
            response += dsh_utils.red_error_break_msg(message)
            error_event(message, errorLevel='CRT')
            return (False, response)


    #
    # save the django object in the database.
    #
    item.file = shortName
    try:
        item.save()
        if audienceList and originalItem:
            item.followup_to = originalItem
            item.intended_audience = audienceList
            item.save()
    except:
        message = 'dsh_django_utils.save_red5_mp3_in_django: ' +\
                  'django save failed: ' + djangoFullName

    response += dsh_utils.black_break_msg_debug(
        'dsh_django_utils.convert_red5_flv_to_mp3: saved: ' +\
        djangoFullName, 113)

    urlPart = dsh_django_config.lookup('ITEM_DETAIL_URL') + str(item.id)
    response += dsh_utils.black_break_msg(
        'Message successfully saved. ' +
        'Please <a href="%s">edit details<a> of this message.'% \
        (urlPart,))

    return (True, response)



def cleanup_red5_conversion(success, name):
    """clean up the red5 stream directory.
    if it was successful, remove the .flv as well.
    otherwise, just remove the .wav and .mp3."""

    red5Dir = dsh_config.lookup('RED5_STREAMS_DIR')
    flvPath = os.path.join(red5Dir, name + '.flv')
    wavPath = os.path.join(red5Dir, 'tmp', name + '.wav')
    mp3Path = os.path.join(red5Dir, 'tmp', name + '.mp3')
    metaPath = flvPath + '.meta'
    
    dsh_utils.cleanup_path(wavPath, 'dsh_django_utils.cleanup_red5_conversion')
    dsh_utils.cleanup_path(mp3Path, 'dsh_django_utils.cleanup_red5_conversion')
    if success:
        dsh_utils.cleanup_path(flvPath,
                               'dsh_django_utils.cleanup_red5_conversion')
        dsh_utils.cleanup_path(metaPath,
                               'dsh_django_utils.cleanup_red5_conversion')



def check_auto_timed_calls_for_all_persons(noLogging=False):
    """called by views.schedulecalls()."""
    
    debug_event('dsh_django_utils.check_auto_timed_calls_for_all_persons: ' +\
                'noLogging: ' + repr(noLogging), 30)

    persons = dvoice.db.models.Person.objects.filter(timed1__isnull=False)
    for callee in persons:
        if callee.auto_dial_disabled:
            continue
        check_auto_timed_calls_for_person(callee, noLogging=noLogging)



def should_auto_dial_broadcast(callee):
    """if the callee is a Person that should receive auto-dialed broadcasts,
    return the broadcast message.
    return None otherwise.
    called by check_auto_timed_calls_for_person(callee) below.
    called by dsh_django2.handle_regular_caller() as well.
    """

    if not callee.phone_number:
        return None

    if not callee.timed1:
        return None

    if callee.auto_dial_disabled:
        return None

    if not callee.timed_broadcast:
        return None
    
    #actives = dvoice.db.models.Item.objects.filter(active=True, itype='B')
    actives = dsh_common_db.get_active_broadcast_item_for_caller(
        callee, dvoice.db.models.Item, dvoice.db.models.KeyWord, None)
    if not actives:
        return None

    #
    # there should be just one active broadcast for now, but
    # i'm going to pretend that there may be more, for the future.
    #
    for active in actives:
        heardEvents = dvoice.db.models.Event.objects.filter(
            action='HERD',owner=callee.id, dsh_uid_concerned=active.dsh_uid)
        if not heardEvents:
            return active
        #
        # now we know it's been heard before.
        #
        if callee.ptype == 'LEA':
            #
            # the leader types don't hear messages that have been heard.
            #
            debug_event('leader type, already heard.', 27)
            continue
        if not active.play_once:
            #
            # teachers get called repeatedly, even for heard messages.
            #
            debug_event("don't just play once.", 27)
            return active
        #
        # if we get here, the callee is not a leader.
        # and the message is meant to be played just once.
        # and the message has been heard.
        # we don't play it again.
        # the "continue" is unnecessary, but I'm just making it explicit.
        #
        debug_event("not leader, play once, heard, don't play again: "+\
                    callee.dsh_uid, 27)
        continue

    #
    # if we get here, all active broadcasts have been heard by this person.
    #
    return None
    


def check_auto_timed_calls_for_person(callee, noLogging=False,
                                      sessionID=''):
    """right after a Person is saved.  just like check_auto_timed_calls(item).
    but for person.
    We don't do this at the time of Person.save() any more.
    so this is only called by check_auto_timed_calls_for_all_persons() above.
    now, also triggered by the little clock icon on the Person page:
    called by views.schedule_one_callee().
    sessionID is set by dsh_failed.hangup_signal_handler() only for logging.
    10/03/23:
    instead of returning nothing, I'm going to return something now.
    returns (scheduled, stringMsg)
    """

    debug_event('dsh_django_utils.check_auto_timed_calls_for_person: ' +\
                'noLogging: ' + repr(noLogging), 42)

    activeBroadcastMsg = should_auto_dial_broadcast(callee)
    if activeBroadcastMsg and not activeBroadcastMsg.dummy:
        debug_event(
            'dsh_django_utils.check_auto_timed_calls_for_person: ' +\
            'schedule this person for broadcast: ' +\
            callee.dsh_uid, 25)
        success,scheduled = auto_schedule_one_callee(
            activeBroadcastMsg, callee, force=True, noLogging=noLogging,
            sessionID=sessionID)
        return (scheduled, 'attempted to schedule for a broadcast message.')

    if not callee.phone_number:
        return (False, 'no phone number.')
    
    if not callee.timed1 or callee.auto_dial_disabled:
        return (False, 'no auto-dial.')


    peerShared = dsh_common_db.should_auto_dial_for_peer_share(
        callee,
        dvoice.db.models.Item,
        dvoice.db.models.KeyWord,
        dvoice.db.models.Event,
        noLogging=noLogging,
        sessionID=sessionID)
    if peerShared:
        success,scheduled = auto_schedule_one_callee(
            peerShared, callee, noLogging=noLogging, sessionID=sessionID)
        return (scheduled, 'attempted to schedule for peer-shared message.')
        

    messages = callee.message_for_me.all()
    if not messages:
        return (False, 'no personalized message.')

    for msg in messages:
        if not (msg.itype == 'P' and msg.active):
            continue
        
        #
        # 10/03/31:
        # a fix.
        #
        eventTable = dvoice.db.models.Event
        heardEvents = eventTable.objects.filter(
            action='HERD', owner=callee.id, dsh_uid_concerned=msg.dsh_uid)
        if heardEvents:
            continue

        debug_event('dsh_django_utils.check_auto_timed_calls_for_person: '+\
                    'has personalized message.', 42)
                    
        success,scheduled = auto_schedule_one_callee(msg, callee,
                                                     noLogging=noLogging,
                                                     sessionID=sessionID)
        if (not success) or scheduled:
            #
            # when this person receives a scheduled call,
            # it'll go through all the messages.
            # so there's no need to schedule more than once.
            #
            return (scheduled,
                    'attempted to schedule for a personalized message.')

    #
    # 10/03/31:
    # in the dv2 version, this is where we do a scheduling for people
    # in the CDS.  I'm not doing that here.
    #
    return (False, 'no active personalized message.')

        

def check_auto_timed_calls(item):
    """right after an item is saved, check to see if we want to schedule
    automatic outgoing calls for intended audience members who have
    specified when they want to receive timed calls.
    called by the save() method of Item.

    because at the time of creating an item,
    the many-to-many intended_audience is not visible,
    so I'm giving up on the idea of doing this at item save time.
    this function is no longer used.
    """

    debug_event('dsh_django_utils.check_auto_timed_calls: entered: ' +\
                item.dsh_uid, 18)

    #
    # for now, let's just only do this for "personalized" messages.
    #
    if not (item.itype == 'P' and item.active):
        return

    allAudience = item.intended_audience.all()

    if not allAudience:
        debug_event('dsh_django_utils.check_auto_timed_calls: no audience: ',
                    18)
        return

    for callee in allAudience:
        if not callee.timed1 or callee.auto_dial_disabled:
            debug_event('dsh_django_utils.check_auto_timed_calls: skip: ' +\
                callee.dsh_uid, 18)
            continue
        success,scheduled = auto_schedule_one_callee(item, callee)



def auto_schedule_one_callee(item, callee, force=False, noLogging=False,
                             sessionID=''):
    """called by check_auto_timed_calls().
    force=True when this is triggered by playing a broadcast message.
    returns (success, whether an auto call is scheduled).
    """

    debug_event('dsh_django_utils.auto_schedule_one_callee: entered: ' +\
                item.dsh_uid + ',  noLogging: ' + repr(noLogging), 30)
    
    #scheduledEvents = dvoice.db.models.Event.objects.filter(
    #    action='SCHE', owner=callee.id, dsh_uid_concerned=item.dsh_uid)
    #if scheduledEvents:
    #    return (True, False)

    if not force:
        heardEvents = dvoice.db.models.Event.objects.filter(
            action='HERD',owner=callee.id, dsh_uid_concerned=item.dsh_uid)
        if heardEvents:
            return (True, False)

    scheduled,callTime = schedule_next_call_time(callee)

    if not scheduled:
        debug_event(
            'dsh_django_utils.auto_schedule_one_callee: nothing scheduled.',
            16)
        return (True, False)
    debug_event('dsh_django_utils.auto_schedule_one_callee: scheduled: ' +\
                repr(callTime), 16)

    success = generate_dot_call_file(callee, callTime, item,
                                     noLogging=noLogging,
                                     sessionID=sessionID)
    if not success:
        scheduled = False
    return (success, scheduled)



def schedule_next_call_time(callee):
    """called by auto_schedule_one_callee().
    based on what the callee has specified, let's figure out
    when he should receive an auto-dialed outgoing call.
    returns (scheduled, scheduledTime)
    """

    checkList = [
        (callee.timed1, callee.timed1_type),
        (callee.timed2, callee.timed1_type),
        (callee.timed3, callee.timed1_type),
    ]

    resultScheduled = False
    resultTime = None
    for checkThis in checkList:
        checkTime,checkType = checkThis
        scheduled,scheduledTime = check_one_timed_call_time(
            callee, checkTime, checkType)
        if not resultScheduled and scheduled:
            resultScheduled = True
            resultTime = scheduledTime
            continue
        if not scheduled:
            continue
        #
        # resultScheduled == True and scheduled == True
        #
        debug_event('dsh_django_utils.schedule_next_call_time(): ' +\
                    'result: ' +  repr(resultTime) + ' ..  ' +\
                    'scheduled: ' + repr(scheduledTime), 23)
        if scheduledTime < resultTime:
            resultTime = scheduledTime

    debug_event('dsh_django_utils.schedule_next_call_time(): ' +\
                repr(resultScheduled) + ' -- ' + repr(resultTime), 23)
    return (resultScheduled,resultTime)



def check_one_timed_call_time(callee, timed, timedType):
    """
    used to be schedule_next_call_time(callee),
    changed to account for which timedx field to look at.
    
    called by auto_schedule_one_callee().
    based on what the callee has specified, let's figure out
    when he should receive an auto-dialed outgoing call.
    returns (scheduled, scheduledTime)
    """
    return dsh_common_db.check_one_timed_call_time(callee, timed, timedType)



def generate_dot_call_file(callee, callTime, item, noLogging=False,
                           dialNow=False, sessionID=''):
    """returns success.
    dialNow=True when triggered by the dial now icon on the Person page.
    when called by dial_now_confirm().
    """
    
    dsh_config.init_for_dot_calls()
    #channelPhys = dsh_config.lookup('FORWARD_OUTGOING_CHANNEL')
    channelPhys = dsh_common_db.get_forward_outgoing_channel()
    #context = dsh_config.lookup('OUTGOING_CONTEXT')
    context,extension = dsh_common_db.get_outgoing_context_extension()
    hostname = dsh_config.lookup('HOSTNAME')
    
    if hostname == 'barney':
        #
        # for testing on the machine barney.
        # this is similar to dsh_agi.forward_call()
        #
        callNum = dsh_config.lookup('BARNEY_TEST_JUNIOR_ZOIPER')
        #callerID = 'dot'
        callerID = dsh_config.lookup('BARNEY_TEST_DOT_CALL_NUMBER')
    else:
        if not callee.phone_number:
            error_event('dsh_django_utils.generate_dot_call_file(): ' +\
                        'this callee has no phone number: ' +\
                        callee.dsh_uid, errorLevel='ERR')
            
            return False
        callNum = callee.phone_number
        callNum = dsh_common_agi.chop_prefix_digits_for_local(callNum, callee)
        callerID = callNum
        callNum = dsh_common_agi.change_call_num_to_zoiper_test(callee,callNum)
        
    channel = channelPhys + '/' + callNum

    #
    # 10/02/27:
    # instead of using the phone number here, we're switching to
    # the callee's dsh_uid.
    #
    #callerID = dsh_config.lookup('DOT_CALL_INDICATOR') + ' ' + callerID
    callerID = dsh_config.lookup('DOT_CALL_INDICATOR') + ' ' + callee.dsh_uid

    if dialNow:
        passedInfo = dsh_django_config.lookup('DIAL_NOW_INDICATOR')
        passedInfo += callee.dsh_uid
    else:
        passedInfo = callee.dsh_uid
        
    d = {'channel': channel, 'context': context, 'callerid': callerID,
         'extension': extension,
         'dshuid': passedInfo}
    dotCallContent = dsh_django_config.lookup('DOT_CALL_FILE_TEMPLATE') % d

    debug_event('dsh_django_utils.generate_dot_call_file(): .call content: '+\
                dotCallContent, 17)

    success = make_dot_call_file(dotCallContent, callTime, item, callNum,
                                 callee, noLogging=noLogging,
                                 dialNow=dialNow,
                                 sessionID=sessionID)
    
    return success



def determine_dot_call_file_name(callee, phoneNum, dialNow=False):
    """make up the .call file name"""
    dshUid = callee.dsh_uid
    if phoneNum:
        phoneNum = dsh_utils.strip_join_str(phoneNum)
    else:
        phoneNum = ''
    org = ''
    if callee.organization and callee.organization.alias:
        org = dsh_utils.strip_join_str(callee.organization.alias)
    name = dsh_utils.strip_join_str(callee.__unicode__())

    name += dsh_common_db.append_database_name_str()
    
    if dialNow:
        return dshUid + '_' + phoneNum + '_' + org + '_' + name + \
               '__NOW__.call'
    return dshUid + '_' + phoneNum + '_' + org + '_' + name + '.call'



def make_dot_call_file(fileContent, callTime, item, phoneNum, callee,
                       noLogging=False, dialNow=False,
                       sessionID=''):
    """called by generate_dot_call_file().
    noLogging=True when triggered by dsh_reschedule.py"""

    fileName = determine_dot_call_file_name(callee, phoneNum, dialNow=dialNow)
    tmpDir = dsh_config.lookup('TMP_DIR')
    fullName = os.path.join(tmpDir, fileName)
    asteriskDotCallDir = dsh_config.lookup('ASTERISK_DOT_CALL_DIR')

    dsh_utils.cleanup_path(fullName, 'dsh_django_utils.make_dot_call_file')
    dsh_utils.cleanup_path(os.path.join(
        asteriskDotCallDir,
        fileName), 'dsh_django_utils.make_dot_call_file')
    try:
        op = 'open'
        dotCallFile = open(fullName, 'w')
        op = 'write'
        dotCallFile.write(fileContent)
        op = 'close'
        dotCallFile.close()
        if not dialNow:
            op = 'time.mktime'
            setTime = time.mktime(callTime.timetuple())
            op = 'utime'
            os.utime(fullName, (setTime, setTime))
        op = 'chmod'
        dsh_utils.chmod_tree2(fullName, recurse=False)
        op = 'move: ' + fullName + ' -> ' + asteriskDotCallDir
        shutil.move(fullName, asteriskDotCallDir)
        op = 'done'
    except:
        error_event('dsh_django_utils.make_dot_call_file: ' + \
                    'failed to write .call file: ' + fullName + ' .  ' + \
                    'last attempted operation: ' + op + ' .  file content: '+\
                    fileContent, errorLevel = 'CRT')
        return False

    if not noLogging:
        if dialNow:
            actionStr = 'DNOW'
        else:
            actionStr = 'SCHE'
            
        dsh_agi.report_event(
            'outgoing call scheduled: ' + fullName + \
            ', scheduled time: ' + repr(callTime) + \
            ', file content: ' + \
            fileContent,
            item=item,
            action=actionStr,
            phone_number=phoneNum,
            owner=callee,
            sessionID=sessionID)

    return True



def display_phone_link(person):
    """called by Item list and Person list to display a phone number
    column. hides the last four digts of the phone numbers.
    displays icons for shared phones and phone owner."""

    phoneNumber = person.phone_number
    if not phoneNumber:
        return ''
    
    hiddenNumber = dsh_agi.hide_phone_digits(phoneNumber)
    persons = dvoice.db.models.Person.objects.filter(phone_number=phoneNumber)
    if not persons:
        return hiddenNumber
    howMany = len(persons)

    href = '/lookupphone/' + person.dsh_uid
    url1 = '<a href="%s" title="lookup phone number">%s</a>' % \
           (href, hiddenNumber)

    if howMany == 1:
        return url1

    spaces = dsh_django_config.lookup('ICON_SPACES')

    if person.phone_owner:
        icon = dsh_django_config.lookup('SHARED_PHONE_OWNER_ICON')
        url2 = '<a href="%s" title="owner of shared phone">%s</a>' % \
               (href, icon)
        return url1 + spaces + url2

    icon = dsh_django_config.lookup('SHARED_PHONE_ICON')
    url3 = '<a href="%s" title="shared phone">%s</a>' % \
           (href, icon)
    return url1 + spaces + url3
        


def make_me_phone_owner(person):
    """called by models.Person.save().  if I'm the owner of a phone,
    then the others can't be."""

    if not person.phone_owner:
        return
    
    phoneNumber = person.phone_number
    if not phoneNumber:
        return
    
    persons = dvoice.db.models.Person.objects.filter(phone_number=phoneNumber)
    if not persons:
        return
    howMany = len(persons)
    if howMany == 1:
        return
    
    for p in persons:
        if p.dsh_uid == person.dsh_uid:
            continue
        p.phone_owner = False
        p.save()



def auto_schedule_list():
    """called by views.schedule_list().  list the content of
    /var/spool/asterisk/outgoing/"""

    spoolDir = dsh_config.lookup('ASTERISK_DOT_CALL_DIR')
    if not dsh_utils.is_valid_dir(spoolDir, silence=True):
        message = 'dsh_django_utils.auto_schedule_list: ' + \
                  'spool directory invalid: ' + spoolDir
        error_event(message, errorLevel = 'CRT')
        return dsh_utils.red_error_break_msg(message)

    answer = '<TABLE BORDER=1>\n'

    message = 'dsh_django_utils.auto_schedule_delete_all: ' +\
              'listdir() failed: ' + spoolDir

    try:
        #listing = os.listdir(spoolDir)
        listing = dsh_utils.listdir_mtime(spoolDir)
        listing = dsh_common_db.filter_listdir_with_dbname(listing)
        if listing == None:
            error_event(message, errorLevel = 'CRT')
            return dsh_utils.red_error_break_msg(message)
    except:
        error_event(message, errorLevel = 'CRT')
        return dsh_utils.red_error_break_msg(message)

    listForCheckingConflicts = []

    count = 0
    for one in listing:
        full = os.path.join(spoolDir, one)
        if not one:
            continue
        if os.path.isdir(full):
            continue
        if not dsh_utils.is_valid_file(full):
            continue
        if not one.endswith('.call'):
            continue

        nokIcon = dsh_django_config.lookup('NOK_ICON')
        errorColumn = '<TD>%s</TD>\n' % (nokIcon,)
        

        answer += '<TR>\n'

        #
        # person thumbnail.
        #
        dshUidLen = dvoice.db.models.dsh_uid_length()
        dshUid = one[:dshUidLen]
        person = get_foreign_key(dvoice.db.models.Person, dshUid)

        if not person:
            answer += errorColumn
        else:
            thumb = thumbnail(person, person.mugshot)
            href = dsh_django_config.lookup('PERSON_DETAIL_URL') +\
                   str(person.id)
            url = '<a href="%s" title="callee details">%s</a>' % (href, thumb)
            answer += '<TD>%s</TD>\n' % (url,)

        if not person:
            answer += errorColumn
        else:
            answer += '<TD>%s</TD>\n' % (person.__unicode__(),)

        if not person or not person.organization or \
               not person.organization.alias:
            answer += errorColumn
        else:
            answer += '<TD>%s</TD>\n' % (person.organization.alias,)


        #
        # file name.
        #
        answer += '<TD>%s</TD>\n' % (one,)


        #
        # scheduled time.
        #
        time = None
        try:
            time = os.stat(full)[-2]
            time = datetime.datetime.fromtimestamp(time)
            #timeStr = time.strftime(dsh_utils.uploadDateTimeFormat)
            timeStr = time.strftime(
                '<span style="white-space: nowrap;">%#Y-%#m-%#d</span> ' +\
                '<span style="white-space: nowrap;">%#H:%#M:%#S</span>')
            answer += '<TD>%s</TD>\n' % (time.strftime('%a'),)
            answer += '<TD>%s</TD>\n' % (timeStr,)
        except:
            answer += errorColumn
            answer += errorColumn

        #
        # icon of the callee.
        #
        if not person:
            answer += errorColumn
        else:        
            href = dsh_django_config.lookup('SCHEDULED_USER_URL') + dshUid
            icon = dsh_django_config.lookup('SCHEDULED_USER_ICON')
            url = '<a href="%s" title="callee">%s</a>' % (href, icon)
            answer += '<TD>%s</TD>\n' % (url,)

        #
        # for checking conflicts at the end.
        #
        if time and person:
            listForCheckingConflicts.append((time, person))


        #
        # icon of the active personalized messages.
        #
        if not person:
            answer += errorColumn
        else:
            personID = str(person.id)
            personalMsgs = dvoice.db.models.Item.objects.filter(
                active=True, itype='P', intended_audience=personID)
            if personalMsgs:
                href = dsh_django_config.lookup('SCHEDULED_MSG_URL') +\
                       personID
                icon = dsh_django_config.lookup('SCHEDULED_MSG_ICON')
                url = '<a href="%s" title="personalized messages">%s</a>' %\
                      (href, icon)
                answer += '<TD>%s</TD>\n' % (url,)
            else:
                answer += '<TD>&nbsp;</TD>\n'


        #
        # icon of the active broadcast messages.
        #
        if not person:
            answer += errorColumn
        else:
            personID = str(person.id)
            if not person.timed_broadcast:
                answer += '<TD>&nbsp;</TD>\n'
            else:
                #broadcastMsgs = dvoice.db.models.Item.objects.filter(
                #    active=True, itype='B')
                broadcastMsgs = \
                    dsh_common_db.get_active_broadcast_item_for_caller(\
                        person,
                        dvoice.db.models.Item,
                        dvoice.db.models.KeyWord,
                        None)
                if broadcastMsgs:
                    href = dsh_django_config.lookup('SCHEDULED_BROADCAST_URL')
                    icon = dsh_django_config.lookup('SCHEDULED_BROADCAST_ICON')
                    url = '<a href="%s" title="broadcast messages">%s</a>' %\
                          (href, icon)
                    answer += '<TD>%s</TD>\n' % (url,)
                else:
                    answer += '<TD>&nbsp;</TD>\n'


        #
        # for deleting this one.
        #
        delIcon = dsh_django_config.lookup('CROSS_ICON')
        url = '<a href="/scheduledel/%s">%s</a>' % (one, delIcon)
        answer += '<TD>%s</TD>\n' % (url,)
        
        answer += '</TR>\n'
        count += 1

    answer += '</TABLE>\n<BR>\n'

    answer += dsh_utils.black_break_msg('%s outgoing call(s).' % (str(count),))

    answer += check_conflicting_slots(listForCheckingConflicts)
    
    return answer



def auto_schedule_delete(fileName):
    """called by views.schedule_del()."""

    spoolDir = dsh_config.lookup('ASTERISK_DOT_CALL_DIR')
    if not dsh_utils.is_valid_dir(spoolDir, silence=True):
        message = 'dsh_django_utils.auto_schedule_delete: ' + \
                  'spool directory invalid: ' + spoolDir
        error_event(message, errorLevel = 'CRT')
        return dsh_utils.red_error_break_msg(message)
    
    full = os.path.join(spoolDir, fileName)
    
    if not dsh_utils.is_valid_file(full):
        message = 'dsh_django_utils.auto_schedule_delete: ' + \
                  'file name invalid: ' + full
        error_event(message, errorLevel = 'ERR')
        return dsh_utils.red_error_break_msg(message)

    dsh_utils.cleanup_path(full, 'dsh_django_utils.auto_schedule_delete: ')
    return dsh_utils.black_break_msg('deleted: ' + full)



def auto_schedule_delete_all(force=False):
    """called by views.schedule_del_all().
    force=True when called by views.schedule_del_all()"""

    return dsh_common_agi.auto_schedule_delete_all(force=force)



def check_valid_email_addresses(addressString):
    """called by views.email_selection().
    input is a comma separated list of email addresses.
    returns a list of valid email addresses if everything is good.
    otherwise returns None.
    """

    returnMsg = ''
    
    if not addressString:
        returnMsg += dsh_utils.red_error_break_msg(
            'empty email address list.')
        return (returnMsg, None)

    splitList = addressString.split(',')
    answerList = []

    returnMsg += dsh_utils.black_break_msg_debug(
        'addr list: ' + repr(splitList), 117)

    for one in splitList:
        one = one.strip()
        if not one:
            continue
        if email_re.match(one):
            answerList.append(one)
            continue
        returnMsg += dsh_utils.red_error_break_msg(
            'invalid email address: ' + one)
        return (returnMsg, None)

    if not answerList:
        returnMsg += dsh_utils.red_error_break_msg(
            'no valid email address found.')
        return (returnMsg, None)
        
    return (returnMsg, answerList)



def unknown_list():
    """called by views.unknown_list().
    lists all the unknown people."""

    returnMsg = ''

    unknowns = dvoice.db.models.Person.objects.filter(first_name='no-name')
    if not unknowns:
        returnMsg += dsh_utils.black_break_msg('no unknown person.')
        return returnMsg

    returnMsg += '<TABLE BORDER=1>\n'
    for one in unknowns:
        phone = one.phone_number

        if phone == 'xxxx':
            continue
        
        returnMsg += '<TR>\n'

        if not phone:
            phone = '(no number)'

        href = dsh_django_config.lookup('PERSON_DETAIL_URL')
        href += str(one.id)
        url = '<a href="%s" title="edit person details">%s</a>' % (href, phone)
        
        returnMsg += '<TD>%s</TD>\n' % (url,)

        returnMsg += '<TD>%s %s</TD>\n' % (one.person_item_link(),
                                           one.sync_callee_link())

        time = one.modify_datetime
        if time:
            timeStr = time.strftime(dsh_utils.uploadDateTimeFormat)
        else:
            timeStr = ''

        returnMsg += '<TD>%s</TD>\n' % (timeStr,)

        returnMsg += '</TR>\n'

    returnMsg += '</TABLE>\n'
    return returnMsg



def get_file_size(obj, field):
    """called by models.Item.get_file_size()."""
    
    if (not field) or (not field.file) or (not field.file.file) or \
           (not field.file.file.name):
        error_event('dsh_django_utils.get_file_size: ' + \
                    'failed to get file field: ' + obj.dsh_uid,
                    errorLevel='CRT')
        return ''

    fullName = field.file.file.name
    sizeStr = dsh_utils.get_file_size_str(fullName)

    if sizeStr == '':
        error_event('dsh_django_utils.get_file_size: ' + \
                    'failed to get file size: ' + fullName,
                    errorLevel='CRT')
        return ''

    return sizeStr



def scheduled_slots():
    """called by views.scheduled_slots().
    modeled after schedule_next_call_time().
    """

    allSlots = get_all_scheduled_slots()
    response = ''
    response += '<TABLE border=1>\n'

    for slot in allSlots:
        time,callee = slot
        response += print_one_slot(time, callee)
        
        #if callee.auto_dial_disabled:
        #    disableIcon = dsh_django_config.lookup('AUTO_DIAL_DISABLED_ICON')
        #else:
        #    disableIcon = '&nbsp;'
        #
        #response += '<TD><center>%s</center></TD>\n' % (disableIcon,)

    response += '</TABLE>'

    response += check_conflicting_slots(allSlots)
    
    return response



def get_all_scheduled_slots():
    """called by scheduled_slots().
    """
    persons = dvoice.db.models.Person.objects.filter(timed1__isnull=False)
    allSlots = []
    
    for callee in persons:
        
        checkList = [
            (callee.timed1, callee.timed1_type),
            (callee.timed2, callee.timed1_type),
            (callee.timed3, callee.timed1_type),
            ]
        
        for checkThis in checkList:
            checkTime,checkType = checkThis
            scheduled,scheduledTime = check_one_timed_call_time(
                callee, checkTime, checkType)
            if not scheduled:
                continue
            allSlots.append((scheduledTime, callee,))

    allSlots.sort()
    return allSlots



def print_one_slot(slot, callee):
    """prints one row of a slot table."""

    response = ''
    response += '<TR>\n'
        
    response += '<TD>%s</TD>\n' % (slot.strftime('%a'),)
    response += '<TD>%s</TD>\n' % (slot.strftime('%#H:%#M:%#S'),)
    response += '<TD>%s</TD>\n' % (slot.strftime('%#Y-%#m-%#d'),)

    response += '<TD>%s</TD>\n' % (callee.__unicode__(),)
    response += '<TD>%s</TD>\n' % (callee.organization.alias,)
    response += '</TR>\n'
    return response



def check_conflicting_slots(allSlots):
    """called by scheduled_slots() to see if
    people have picked conflicting slots."""

    if not allSlots:
        return ''

    prevSlot = None
    prevCallee = None
    lastPrintedSlot = None
    lastPrintedCallee = None
    
    response = dsh_utils.black_break_msg('<br>checking conflicts...<br>')
    count = 0

    response += '<TABLE border=1>\n'
    
    for slot in allSlots:
        thisSlot,thisCallee = slot
        if prevSlot == None or prevSlot != thisSlot:
            prevSlot = thisSlot
            prevCallee = thisCallee
            continue
        #
        # if we get here,
        # we know this is not the first iteration.
        # and we know this slot equals to the previous slot.
        #
        count += 1
        
        if lastPrintedSlot == prevSlot and lastPrintedCallee == prevCallee:
            #
            # the previous slot has already been printed.
            # it's something like a sequence of three conflicts.
            # we don't print it again.
            #
            pass
        else:
            #
            # the previous slot hasn't been printed, so let's print it.
            #
            #response += dsh_utils.black_break_msg(
            #    repr(prevSlot) + ' : ' + prevCallee.__unicode__())
            response += print_one_slot(prevSlot, prevCallee)
            

        #response += dsh_utils.black_break_msg(
        #    repr(thisSlot) + ' : ' + thisCallee.__unicode__())
        response += print_one_slot(thisSlot, thisCallee)

        lastPrintedSlot = thisSlot
        lastPrintedCallee = thisCallee
        prevSlot = thisSlot
        prevCallee = thisCallee

    response += '</TABLE>'
    response += '<br>'
            
    if count == 0:
        response += dsh_utils.black_break_msg('no conflict found.')
    else:
        response += dsh_utils.red_error_break_msg(
            'found %s conflict(s).' % (str(count),))

    return response



def phone_number_list():
    """called by views.phone_number_list().
    lists all the phone numbers."""

    returnMsg = ''

    people = dvoice.db.models.Person.objects.all()

    pList = []
    for person in people:
        phoneNumber = person.phone_number
        if not phoneNumber:
            phoneNumber = '(none)'

        if not person.organization or not person.organization.alias:
            org = '(none)'
        else:
            org = person.organization.alias

        name = person.__unicode__()
        if not name:
            name = '(none)'

        pList.append((org, name, phoneNumber))

    pList.sort()
    count = 0
    returnMsg += '<TABLE BORDER=1>\n'
    
    for one in pList:
        count += 1
        org,name,phoneNumber = one
        returnMsg += '<TR>\n'
        returnMsg += '<TD>%s</TD>\n' % (name,)
        returnMsg += '<TD>%s</TD>\n' % (org,)
        returnMsg += '<TD>%s</TD>\n' % (phoneNumber,)
        returnMsg += '</TR>\n'

    returnMsg += '</TABLE>\n'
    returnMsg += '<BR>\n'
    returnMsg += '%s phone number(s).\n' % (str(count),)
    return returnMsg



def callee_info(callee):
    """for logging by dsh_django2.py and dsh_failed.py"""
    
    if not callee:
        return ''

    str = 'name: ' + callee.__unicode__() + ', '
    if callee.phone_number:
        str += 'phone: ' + callee.phone_number + ', '
    if callee.organization and callee.organization.alias:
        str += 'org: ' + callee.organization.alias + ', '
    str += 'dsh_uid: ' + callee.dsh_uid
    return str



def get_by_dsh_uid(dshUid):
    """called by dsh_uid_url()."""
    types = [
        [dvoice.db.models.Item, 'item'],
        [dvoice.db.models.Person,'person'],
        [dvoice.db.models.Organization, 'organization'],
        [dvoice.db.models.KeyWord, 'keyword'],
        [dvoice.db.models.Event, 'event'],
    ]

    answer = None
    for tuple in types:
        type,name = tuple
        obj = get_foreign_key(type, dshUid, quiet=True)
        if obj:
            answer = (obj, name)

    return answer



def dsh_uid_url(dshUid):
    """link to dshUid on Event page."""

    if not dshUid:
        return ''
    
    lookup = get_by_dsh_uid(dshUid)
    if not lookup:
        return dshUid

    obj,name = lookup

    #
    # the value are the names of the URL strings in dsh_django_config.py
    #
    lookTable = {
        'person': 'SCHEDULED_USER_URL',
        'item': 'ITEM_DSH_UID_URL',
        'organization': 'ORG_DSH_UID_URL',
        'event': 'EVENT_DSH_UID_URL',
        'keyword': 'KEYWORD_DSH_UID_URL',
    }

    if not lookTable.has_key(name):
        return dshUid

    configName = lookTable[name]
    href = dsh_django_config.lookup(configName) + dshUid
    return '<a href="%s" title="%s">%s</a>' % (href, name, dshUid)



def check_spoken_names(kind='peer_shared'):
    """called by views.check_spoken_names().
    kind can be "peer_shared" or "personalized".
    """

    response = ''
    
    if kind == 'peer_shared':
        itemList = dvoice.db.models.Item.objects.filter(peer_shared=True)
        if not itemList:
            return dsh_utils.black_break_msg('no peer-shared message.')
        else:
            response += dsh_utils.black_break_msg(
                'checking peer-shared messages...<br>')
    elif kind == 'personalized':
        itemList = dvoice.db.models.Item.objects.filter(
            active=True, itype='P')
        if not itemList:
            return dsh_utils.black_break_msg('no personalized message.')
        else:
            response += dsh_utils.black_break_msg(
                'checking personalized messages...<br>')
        
    else:
        return ''

    response += '<TABLE border=1>\n'
    response += '<TR><TD>&nbsp;</TD><TD><b>message</b></TD>\n'
    response += '<TD><b>person</b></TD><TD><b>name</b></TD>\n'
    response += '<TD><b>org</b></TD><TD><b>name</b></TD></TR>\n'
    
    nokIcon = dsh_django_config.lookup('NOK_ICON')
    nokIcon = '<p valign=middle><CENTER>' + nokIcon + '</CENTER></p>'
    
    for item in itemList:
        if not item.owner or not item.owner.organization:
            continue
        owner = item.owner
        org = owner.organization

        thumb = thumbnail(owner, owner.mugshot)
        href = dsh_django_config.lookup('ITEM_DETAIL_URL') + str(item.id)
        itemLink = '<a href="%s" title="message details">%s</a>' %\
                   (href,thumb)        

        itemSpoken = item_file_list(item, item.file, spokenName=False)
        if not itemSpoken:
            itemSpoken = nokIcon

        ownerName = owner.__unicode__()
        ownerHref = dsh_django_config.lookup('PERSON_DETAIL_URL')
        ownerHref += str(owner.id)
        ownerLink = '<a href=%s title="person details">%s</a>' % \
                    (ownerHref, ownerName)
        ownerSpoken = item_file_list(item, owner.spoken_name, spokenName=True)
        if not ownerSpoken:
            ownerSpoken = nokIcon

        orgName = org.alias
        orgHref = dsh_django_config.lookup('ORG_DETAIL_URL')
        orgHref += str(org.id)
        orgLink = '<a href=%s title="organization details">%s</a>' % \
                  (orgHref, orgName)
        orgSpoken = item_file_list(item, org.spoken_name, spokenName=True)
        if not orgSpoken:
            orgSpoken = nokIcon

        response += '<TR>\n'
        response += '<TD>%s</TD>\n' % (itemLink,)
        response += '<TD valign=middle>%s</TD>\n' % (itemSpoken,)
        response += '<TD>%s</TD>\n' % (ownerLink,)
        response += '<TD valign=middle>%s</TD>\n' % (ownerSpoken,)
        response += '<TD>%s</TD>\n' % (orgLink,)
        response += '<TD valign=middle>%s</TD>\n' % (orgSpoken,)
        response += '</TR>'

    response += '</TABLE>'
    return response



def dial_now(dshUid):
    """called by views.dial_now()
    returns the response for views.dial_now() and a Person obj
    for dial_now_confirm() below.
    """

    callee = get_foreign_key(dvoice.db.models.Person, dshUid, quiet=True)
    if not callee:
        response = dsh_utils.red_error_break_msg(
            'No person has this dsh_uid: ' + dshUid)
        return (response, None)

    name = callee.__unicode__()
    
    phoneNum = callee.phone_number
    if not phoneNum:
        response = dsh_utils.red_error_break_msg(
            'This person has no phone number: name: ' + name + \
            ', dsh_uid: ' + dshUid)
        return (response, None)
    
    response = dsh_utils.black_break_msg(
        'You are about to call: %s @ %s.' % (name, phoneNum),
        noBreak=True)
        
    response += '<a href="%s" title="are you sure?">Confirm</a>? ' % \
                ('/dialnowconfirm/' + dshUid,)
    return (response, callee)



def dial_now_confirm(dshUid):
    """called by views.dial_now_confirm()
    """

    response,callee = dial_now(dshUid)
    if not callee:
        return response

    success = generate_dot_call_file(callee, None, None, dialNow=True)

    if success:
        response = dsh_utils.black_break_msg(
            'Calling %s @ %s...' % (callee.__unicode__(),
                                    callee.phone_number))
        return response

    response = dsh_utils.red_error_break_msg('Something wrong happened.')
    return response



def session_link(session):
    """called by Item and Person for session links that
    created these objects."""
    
    if not session:
        return ''

    spaces = dsh_django_config.lookup('ICON_SPACES')
    url = dsh_django_config.lookup('SESSION_ID_SEARCH_URL')
    icon = dsh_django_config.lookup('SESSION_ID_ICON')
    href = '<a href="%s=%s">%s</a>' % (url, session, icon)
    return href + spaces



def people_heard_link(item):
    """called by models.Item.people_heard_link().
    give an icon to link to the list of people who have heard this."""

    heardEvents = dvoice.db.models.Event.objects.filter(
        action='HERD',
        dsh_uid_concerned=item.dsh_uid)

    if not heardEvents:
        unheardEvents = dvoice.db.models.Event.objects.filter(
            action='UNHR',
            dsh_uid_concerned=item.dsh_uid)
        
        if not unheardEvents:
            return ''

    url = dsh_django_config.lookup('HEARD_PEOPLE_URL')
    if heardEvents:
        icon = dsh_django_config.lookup('HEARD_PEOPLE_ICON')
    else:
        icon = dsh_django_config.lookup('HEARD_PARTIAL_PEOPLE_ICON')
    href = '<a href="%s%s">%s</a>' % (url, item.dsh_uid, icon)
    return href



def spaces_16():
    spaces = dsh_django_config.lookup('ICON_SPACES')
    spaces2 = spaces + spaces
    spaces4 = spaces2 + spaces2
    spaces8 = spaces4 + spaces4
    spaces16 = spaces8 + spaces8
    return spaces16



def print_one_item_table(item):
    """called by people_heard_list().
    prints one table representing the message in question.
    returns (success,htmlResponse).
    imitates the look of the built-in admin list look.
    mostly uses the existing methods of the Item type.
    """

    response = ''
    
    if not item.owner:
        message = 'dsh_django_utils.people_heard_list: ' + \
                  'no owner field. ' + dshUid
        response += dsh_utils.red_error_break_msg(message)
        error_event(message, errorLevel='CRT')
        return (False,response)

    response += dsh_utils.black_break_msg('the message:<BR>')
    response += '<TABLE BORDER=1>\n'

    bigSpaces = spaces_16()
    
    response += """
<TR>
<TD align=center><B>mug</B></TD>
<TD align=center><B>voice</B></TD>
<TD align=center><B>who</B></TD>
<TD align=center><B>org.</B></TD>
<TD align=center><B>attrs.</B></TD>
<TD align=center><B>when</B></TD>
<TD><B>key words</B></TD>
<TD align=center><B>%s</B></TD>
</TR>
""" % (dsh_utils.html_no_break(bigSpaces + 'description' + bigSpaces),)
    
    response += '<TR>\n'

    href = dsh_django_config.lookup('ITEM_URL') + str(item.id)
    mugLink = '<a href="%s">%s</a>' % (href, item.thumbnail())
    response += '<TD>%s</TD>\n' % (mugLink,)

    response += '<TD>%s</TD>\n' % (item.item_url(),)
    response += '<TD>%s</TD>\n' % (item.owner_link_plus_phone(),)
    response += '<TD>%s</TD>\n' % (item.org_link(),)
    response += '<TD>%s</TD>\n' % (item.meta_display(),)
    response += '<TD>%s</TD>\n' % (dsh_utils.time_date_day_str(
        item.modify_datetime))
    response += '<TD>%s</TD>\n' % (item.get_key_words(),)
    description = item.description
    if not description:
        description = ''
    response += '<TD>%s</TD>\n' % (description,)

    response += '</TR>\n'
    response += '</TABLE><BR>\n'
    return (True, response)



def session_includes_saved(person, sessionID):
    """called by people_heard_list().
    see if this person uploaded something during this listening session.
    returns two columns (TDs).
    """


    #
    # mirrors dsh_django_utils.insert_event_after_upload_item().
    #
    if not sessionID:
        saveEvents = None
    else:
        saveEvents = dvoice.db.models.Event.objects.filter(
            etype='INF',
            action='UPLD',
            owner=person,
            phone_number=person.phone_number,
            session=sessionID)


    #
    # the response is two columns.
    #
    response = """
<TD align=center>%s<br>%s</TD>
<TD align=left>%s</TD>
"""
    emptyResponse = response % ('', '', '')
    if not saveEvents:
        return emptyResponse


    #
    # get the event,
    # then get the item.
    #
    saveEvent = saveEvents[0]
    if not saveEvent:
        return emptyResponse

    dshUid = saveEvent.dsh_uid_concerned
    item = get_foreign_key(dvoice.db.models.Item, dshUid)
    if not item:
        return emptyResponse

    if not item.description:
        description = ''
    else:
        description = item.description


    #
    # make the duration string.  it points to Item.
    #
    durStr = str(item.rec_duration) + 's'
    href = dsh_django_config.lookup('ITEM_URL') + str(item.id)
    durLink = '<a href="%s" title="message details">%s</a>' % (href, durStr)


    #
    # the response: the playable widget, followed by seconds,
    # followed by description.
    #
    return response % (
        item.item_url(),
        durLink,
        description)
    


def people_heard_list(dshUid, printUnheard=False):
    """called by views.heard().
    print the list of people who have heard a particular message.
    09/12/13: added the optional argument of printUnheard,
    called again by views.heard(), to print only the "unheard" events
    in a table.
    10/04/01:
    add unhear icons.
    """

    response = ''


    #
    # get the Item.
    # quit if it's a bogus dsh_uid.
    #
    item = get_foreign_key(dvoice.db.models.Item, dshUid)
    if not item:
        message = 'dsh_django_utils.people_heard_list: ' + \
                  'failed to locate item: ' + dshUid
        response += dsh_utils.red_error_break_msg(message)
        error_event(message, errorLevel='ERR')
        return response


    #
    # print out this item.
    #
    success,itemResponse = print_one_item_table(item)
    if not printUnheard:
        response += itemResponse

    if not success:
        return response


    #
    # we will use this to calculate the fraction heard for
    # each person.
    #
    if item.rec_duration:
        itemLen = item.rec_duration
    else:
        itemLen = 0


    #
    # get all the "heard" events.
    # if we can't find any, we get out.
    #
    if not printUnheard:
        heardEvents = dvoice.db.models.Event.objects.filter(
            action='HERD',
            dsh_uid_concerned=dshUid)
    else:
        heardEvents = dvoice.db.models.Event.objects.filter(
            action='UNHR',
            dsh_uid_concerned=dshUid)

    if not heardEvents:
        if not printUnheard:
            return response + \
                   dsh_utils.black_break_msg('No one has heard this one.')
        else:
            return response + \
                   dsh_utils.black_break_msg('No partially heard events.')


    #
    # now we're ready to print the table of people who have heard this.
    #
    if not printUnheard:
        response += dsh_utils.black_break_msg(
            "%s person(s) heard this message:" % (str(len(heardEvents)),))
    else:
        response += dsh_utils.black_break_msg(
            "%s partially heard event(s):" % (str(len(heardEvents)),))
    response += '<BR>'


    #
    # the table header row.
    #
    response += """
<TABLE BORDER=1>
"""

    bigSpaces = spaces_16()

    if not printUnheard:
        #
        # 10/04/01:
        # added first column for un-hear columns.
        #
        response += """
<TR>
<TD align=center></TD>
<TD align=center><b>mug</b></TD>
<TD align=center><b>who</b></TD>
<TD align=right><b>listening<br>duration</b><br>(s, %%)</TD>
<TD align=center><b>when,<br>session</b></TD>
<TD align=center><b>response</b></TD>
<TD align=center><b>%s</b></TD>
</TR>
""" % (dsh_utils.html_no_break(bigSpaces + 'description' + bigSpaces),)
        
    else:
        #
        # for the unheard events table,
        # skip the last two columnns: response and description.
        #
        response += """
<TR>
<TD align=center><b>mug</b></TD>
<TD align=center><b>who</b></TD>
<TD align=right><b>listening<br>duration</b><br>(s, %%)</TD>
<TD align=center><b>when,<br>session</b></TD>
</TR>
"""


    #
    # now we loop through all the "heard" events.
    #
    for heard in heardEvents[::-1]:
        person = heard.owner
        if not person:
            debug_event('people_heard_list: event has no owner: ' +\
                        heard.dsh_uid, 39)
            continue

        response += '<TR>\n'


        #
        # 10/04/01:
        # added unhear icons.
        #
        if not printUnheard:
            response += '<TD align=center>%s</TD>\n' % \
                        (dsh_common_db.heard_event_icons(heard),)


        #
        # much of the below copied from dsh_stats.one_row().
        #


        #
        # the mug shot.
        #
        thumb = thumbnail(person, person.mugshot)
        href = dsh_django_config.lookup('PERSON_URL') + str(person.id)
        mugLink = '<a href="%s">%s</a>' % (href, thumb)
        response += '<TD align=center>%s</TD>\n' % (mugLink,)


        #
        # text of who it is.
        # which organization.
        #
        name = person.__unicode__()
        href = dsh_django_config.lookup('PERSON_URL') + str(person.id)
        nameLink = '<a href="%s">%s</a>' % (href, name)

        org = person.organization
        orgName = org.alias
        href = dsh_django_config.lookup('ORG_URL') + str(org.id)
        orgLink = '<a href="%s">%s</a>' % (href, orgName)

        response += '<TD>%s<BR><BR><BR>%s</TD>\n' % (nameLink, orgLink)


        #
        # listening duration.
        # calculate percentage too.
        #
        if not heard.call_duration:
            dur = 0
        else:
            dur = heard.call_duration

        if itemLen:
            frac = round(dur * 100.0 / itemLen, 1)
            if frac > 100.0:
                frac = 100.0
            frac = str(frac)
        else:
            frac = ''

        response += '<TD align=right>%ss<BR><BR><BR>%s%%</TD>\n' % \
                    (str(dur),frac)


        #
        # when was it heard?
        # make the link to the session ID too.
        #
        when = heard.modify_datetime
        whenStr = dsh_utils.time_date_day_str(when)
        
        session = heard.session
        if not session:
            sessionLink = ''
        else:
            sessionLink = heard.session_id_link()
        response += '<TD align=center>%s<br><br><br>%s</TD>\n' % \
                    (whenStr,sessionLink)


        if not printUnheard:
            #
            # get the recorded reply.
            # it's two columns.
            #
            savedResponse = session_includes_saved(person, session)
            response += savedResponse

        response += '</TR>\n'
        
    response += '</TABLE>\n'
    return response
