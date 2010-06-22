import sys, os, pickle, cgi, cgitb, xmlrpclib, objectstore, random, shutil
import logging, datetime, time, zipfile, cStringIO, shutil
import su, ryw, string, ryw_view, time, ryw_hindi, ryw_disc
import subprocess, re, math



"""gives up if free space falls below 100MB.
issues warning if free space falls below 1GB.
issues warning if free space falls below 4.7GB."""
FREE_SPACE_MB_GIVEUP = 100
FREE_SPACE_MB_WARN2  = 1024
FREE_SPACE_MB_WARN1  = 4.7 * 1024

FFMPEG_PATH_SUFFIX = os.path.join('etc', 'ffmpeg', 'bin', 'ffmpeg.exe')

"""if the free space falls below this threshold,
we'll clear up enough free disk to accommodate the
incoming data."""
FREE_SPACE_WATERMARK_MB_LOW  = 5 * 1024
#for testing: FREE_SPACE_WATERMARK_MB_LOW  = 20 * 1024


AUX_FIELD_TYPES = ('thumbnails', 'excerpts')
AUX_FIELD_ENTRIES = (('thumbnail_name1', 'thumbnails'),
                     ('thumbnail_name2', 'thumbnails'),
                     ('thumbnail_name3', 'thumbnails'),
                     ('thumbnail_name4', 'thumbnails'),
                     ('excerpt_name1', 'excerpts'),
                     ('excerpt_name2', 'excerpts'),
                     ('excerpt_name3', 'excerpts'),
                     ('excerpt_name4', 'excerpts'))


POSSIBLE_SUBJECTS = ['English', 'Hindi', 'Sanskrit', 'science',
                     'physics', 'chemistry', 'astronomy', 'biology',
                     'geology',
                     'mathematics', 'arithmetic', 'algebra',
                     'geometry', 'history', 'social_studies', 'home_science',
                     'agriculture', 'commerce',
                     'culture_and_customs',
                     'general_knowledge',
                     'food_and_nutrition', 'arts_and_crafts',
                     'computer_literacy', 'games', 'stories',
                     'plays', 'with_vocabulary',
                     'environmental_science',
                     'health_care',
                     'nursing',
                     'reproductive_health',
                     'children_health',
                     'women_rights',
                     'children_program',
                     'Kannada', 'Tamil', 'Bengali',
                     'Marathi', 'Punjabi', 'Urdu', 'Nepali']

POSSIBLE_CONTENT_TYPES = ['unknown', 'lecture',
                          'lesson_plan', 'test', 
                          'courseware',
                          'practicals', 'experiments', 
                          'textbook', 'course_materials',
                          'monitoring', 'visits', 'documentary',
                          'supplementary',
			  'compilation',
                          'public_awareness', 
                          'other_TV', 'workshop', 'radio_program',
                          'requests',
                          'support_software',
                          'teacher_training',
                          'staff_training', 'community_training',
                          'chat', 'interview',
                          'student_projects',
                          'homework_submission', 'homework_feedback',
                          'questions', 'answers',
                          'social_entertainment', 'exam', 'information',
                          'scratch_space', 'tmp',
                          'other']

POSSIBLE_LANGUAGES = ['English', 'Hindi', 'Kannada', 'Tamil', 'Bengali',
                      'Marathi', 'Punjabi', 'Urdu', 'Nepali',
                      'Telegu', 'Gujarati', 'Kashmiri']

POSSIBLE_SHOW = ['copyrighted', 'discreet']

POSSIBLE_CACHE = ['sticky']

POSSIBLE_CLASSES = ['unknown', 'preschool', '1', '2', '3', '4', '5', '6',
                    '7', '8', '9', '10', '11', '12', 'college']

POSSIBLE_AGES = ['unknown', 'preschool', '6', '7', '8', '9', '10', '11', '12',
                 '13', '14', '15', '16', '17', 'college']

POSSIBLE_MEDIA = ['video', 'DVD', 'VCD', 'recorded_by_Plextor',
                  'recorded_from_TV', 'VHS_tape_digitized',
                  'from_YouTube',
                  'extracted_by_firewire',
                  'recorded_by_webcam', 'recorded_by_Mustek',
                  'recorded_by_Aiptek', 
                  'recorded_by_CamStudio', 'created_by_ProShow',
                  'has_subtitle', 'SMIL', 'audio_without_video', 'Flash',
                  'images', 'powerpoint', 'documents', 'executables',
                  'slideshows']

POSSIBLE_VIDEO_SUBTYPES = ['video', 'DVD', 'VCD',
                           'extracted_by_firewire',
                           'recorded_by_Plextor',
                           'recorded_from_TV',
                           'from_YouTube',
                           'VHS_tape_digitized', 
                           'recorded_by_webcam', 'recorded_by_Mustek',
                           'recorded_by_Aiptek',
                           'recorded_by_CamStudio', 'created_by_ProShow']

POSSIBLE_VIDEO_RESOLUTION = ['unknown', '320', '350', '640', '720', '1024',
                             '> 1024']

POSSIBLE_SIZE_UNIT = ['MB', 'KB', 'B']

def from_0_to_59_strs():
    ans = []
    for i in range(0, 60):
        ans.append(str(i))
    return ans

POSSIBLE_HOURS = ['unknown', '0', '1', '2', '3', '4', '5', '6', '7', '8',
                  'more']
POSSIBLE_MINUTES = ['unknown'] + from_0_to_59_strs()
                    
POSSIBLE_SECONDS = POSSIBLE_MINUTES



def pretty_much_out_of_space(kB, freeKB):
    return 1024*FREE_SPACE_MB_GIVEUP + kB > freeKB



def check_required_fields(form, checkFile = True):
    """get and check required fields of the upload form."""

    if checkFile:
        if not check_upload_file_request(form, 'local_filename'):
            ryw.give_bad_news('user_error: invalid local file to upload.',
                              logging.info)
            return False

        logging.debug('local_filename: '+form['local_filename'].filename)

    if (not form.has_key('title')) or \
        form.getfirst('title', '') == '':
        ryw.give_bad_news('user_error: no title given', logging.info)
	return False

    logging.debug('check_required_fields passed')
    return True



def attempt_read_uploaded_file(form, fieldname):
    """attempt to read the uploaded file data.
    returns the first buffer-full of data if successful."""

    buf = form[fieldname].file.read(4096)
    
    if (not buf) or (len(buf) == 0):
        ryw.give_bad_news('user_error: uploaded empty file.', logging.info)
        return None

    logging.debug('attempt_read_uploaded_file passed')
    return buf



def check_upload_file_request(form, fieldname):
    if (not form.has_key(fieldname)) or \
        form[fieldname].filename == '' or \
	not form[fieldname].file:
        logging.debug('check_upload_file_validity: not found: ' + fieldname)
	return False

    logging.debug('check_upload_file_request: '+form[fieldname].filename)
    return True



def check_free_space(prefix, supressWarning = False):
    """check how much free space is available and issue warnings."""

    freeMB = ryw.free_MB(prefix)
    #logging.debug('check_free_space: MB available: ' + repr(freeMB))
    
    if freeMB < FREE_SPACE_MB_GIVEUP:
        ryw.give_bad_news(
            'user_error: nearly out of space: '+repr(freeMB)+' MB. operation aborted.',
            logging.error)
        freeMB = 0
    elif freeMB < FREE_SPACE_MB_WARN2 and (not supressWarning):
        ryw.give_bad_news(
            'warning: free disk space critically low: '+repr(freeMB)+' MB. (successful operation may still be possible.)',
            logging.warning)
    elif freeMB < FREE_SPACE_MB_WARN1 and (not supressWarning):
        ryw.give_bad_news(
            'warning: free disk space low: '+repr(freeMB)+' MB. (successful operation may still be possible.)',
            logging.warning)
    return freeMB



def make_tmp_name(prefix1, prefix2, suffix):
    """
    prefix1 = oldDir = mywww = c:\Postmanet\nihao\WWW\repository?
    prefix2 = 'SearchFile_incoming'
    suffix = ''
    objPrefix = 'SearchFile_incoming' + dateTimeRand
    tmpdir = c:\Postmanet\nihao\WWW\repository\'SearchFile_incoming' + dateTimeRand
    """
    
    dateTimeRand = ryw.date_time_rand()
    objPrefix = prefix2 + dateTimeRand
    tmpdir = os.path.join(prefix1, objPrefix + suffix)
    return (tmpdir, objPrefix)



def attempt_just_make_tmpdir(prefix1, prefix2, suffix):
    """attempts to make a temporary directory."""
    
    dateTimeRand = ryw.date_time_rand()

    objPrefix = prefix2 + dateTimeRand
    tmpdir = os.path.join(prefix1, objPrefix + suffix)

    try:
        os.makedirs(tmpdir)
    except:
        ryw.give_bad_news('fatal_error: failed to make temporary directory:'
                          + tmpdir, logging.critical)
        return (None, None)

    logging.debug('attempt_just_make_tmpdir: ' + tmpdir)
    return (tmpdir, objPrefix)



def attempt_make_tmpdir(prefix):
    """attempt to make a temporary directory.
    returns the directory name made."""

    if not os.path.exists(prefix):
        try:
            os.makedirs(prefix)
        except:
            ryw.give_bad_news(
                'fatal_error: failed to create temporary upload directory: '+
                prefix, logging.critical)
            return None

    if check_free_space(prefix) <= 0:
        return None

    tmpdir,objPrefix = attempt_just_make_tmpdir(prefix, 'Upload_', '')
    if not tmpdir:
        return None

    logging.debug('attempt_make_tmpdir passed')
    return tmpdir



def fix_IE_file_name(fName):
    fName = os.path.normpath(fName)
    fName = os.path.basename(fName)
    return fName



def decide_tmp_data_file_name(form, localPath = None, isLocalDir = False):
    """pick a name for the temporary data file."""

    if localPath:
        filename = fix_IE_file_name(localPath)
    else:
        filename = fix_IE_file_name(form['local_filename'].filename)
    
    if filename == '':
        ryw.give_bad_news('fatal_error: empty original file name.',
                          logging.critical)
        return ''

    unzip = form.getfirst('unzip', '')
    if isLocalDir:
        if unzip:
            ryw.give_bad_news(
                'decide_tmp_data_file_name: local directory given, ' +
                'cannot unzip directory: ' + localPath,
                logging.error)
            return ''
        return filename
    
    pair = os.path.splitext(filename)
    ext1 = string.capwords(pair[1])

    remoteName = form.getfirst('repository_filename', '')

    if remoteName != '':
        # enforce that the two names have the same extensions.
        pair = os.path.splitext(remoteName)
        ext2 = string.capwords(pair[1])
        if ext1 != ext2:
            ryw.give_bad_news(
                'user_error: the two file names supplied must have same extensions.',
                logging.info)
            return ''
        filename = remoteName

    if unzip:
        if ext1 != '.zip':
            ryw.give_bad_news('user_error: you cannot unzip a non-zip file.',
                              logging.error)
            return ''

    logging.debug('file name to be stored in the repository: '+filename)
    return filename
    


def quick_exit(exitCode):
    ryw_view.print_footer()
    sys.exit(exitCode)

    

def cleanup_and_exit(tmpdir, metafile, extractDir, exitCode,
                     successMessage = 'upload completed.'):
    """wipe out temporary files and directories, and exit."""
    ryw.cleanup_path(tmpdir,     'cleanup_and_exit, tmpdir:')
    ryw.cleanup_path(metafile,   'cleanup_and_exit, metafile:')
    ryw.cleanup_path(extractDir, 'cleanup_and_exit, extractDir:')
    if tmpdir:
        ryw.cleanup_path(tmpdir + '_AUXI', 'cleanup_and_exit, aux dir:')

    if (exitCode == 0):
        ryw.give_good_news(successMessage, logging.info)

    #print '<BR><BR><A HREF="/index.html">back to home</A><br>'
    ryw_view.print_footer()
            
    sys.exit(exitCode)



def open_tmp_data_file(tmpdir, filename):
    """read the uploaded file and put it in the temp directory."""

    try:
        fName = fix_IE_file_name(filename)
        fName = os.path.join(tmpdir, fName)
        outputFile = open(fName, 'wb')
    except:
        ryw.give_bad_news('fatal_error: failed to create temporary data file.',
                          logging.critical)
        return None

    if not outputFile:
        ryw.give_bad_news('fatal: failed to create temporary data file.',
                          logging.critical)
        return None

    return outputFile



def check_upload_file_validity(form, fieldname):
    result = {}
    if not check_upload_file_request(form, fieldname):
        logging.debug(
            'check_upload_file_validity: no request for: ' + fieldname)
        result['success'] = True
        result['exists']  = False
        result['buf'] = None
        return result
    
    buf = attempt_read_uploaded_file(form, fieldname)
    if not buf:
        ryw.give_bad_news(
            'check_upload_file_validity: check failed for: ' + fieldname,
            logging.info)
        result['success'] = False
        result['exists'] = False
        result['buf'] = None
        return result

    logging.debug('check_upload_file_validity: found valid upload request: '+
                  fieldname)
    result['success'] = True
    result['exists'] = True
    result['buf'] = buf
    return result



def check_aux_file_uploads(form, localExcerptStuff = None):
    """thumbnail and exerpt files."""

    #
    # the reason for passing in the localExcerptStuff:
    # if the basenames match, we'll ignore the file upload buttons.
    # this is to prevent uploading twice.
    #
    localBaseName = None
    if localExcerptStuff:
        localExcSuccess,localExcFound,localExcFilePath,localExcIsDir = \
            localExcerptStuff
        if localExcFound:
            localBaseName = fix_IE_file_name(localExcFilePath)
    else:
        localExcSuccess,localExcFound,localExcFilePath,localExcIsDir = \
            None,None,None,None
    
    aux = {}
    success = True
    exists = False
    for auxEntry in AUX_FIELD_ENTRIES:
        auxName,auxType = auxEntry

        #
        # this is to prevent uploading twice.
        #
        if localExcFound and form.has_key(auxName):
            auxBaseName = fix_IE_file_name(form[auxName].filename)
            if localBaseName == auxBaseName:
                aux[auxName] = {}
                aux[auxName]['success'] = True
                aux[auxName]['exists'] = False
                aux[auxName]['buf'] = None
                continue
        
        aux[auxName] = check_upload_file_validity(form, auxName)
        if not aux[auxName]['success']:
            return (False, None, None)
        if aux[auxName]['exists']:
            exists = True

    return (True, exists, aux)
        


def create_aux_dir(tmpdir):
    auxDir = tmpdir+'_AUXI'
    try:
        su.createdirpath(auxDir)
        ryw.db_print_info_browser('create_aux_dir: ' + auxDir, 27)
        for auxType in AUX_FIELD_TYPES:
            auxTypeDir = os.path.join(auxDir, auxType)
            su.createdirpath(auxTypeDir)
            logging.debug('create_aux_dir: ' + auxTypeDir)
    except:
        ryw.give_bad_news('create_aux_dir failed: ' + auxDir, logging.critical)
        return (False, None)

    return (True, auxDir)



def unzip_excerpt_files(auxDir):
    if not os.path.exists(auxDir):
        return True

    exDir = os.path.join(auxDir, 'excerpts')
    if not os.path.exists(exDir):
        return True

    exNames = os.listdir(exDir)
    if len(exNames) == 0:
        return True

    for exName in exNames:
        try:
            exPath = os.path.join(exDir, exName)
            pair = os.path.splitext(exName)
            ext = string.capwords(pair[1])
            if ext != '.zip':
                continue
            su.zipfile_extractall(exPath, exDir)
            logging.debug('unzip_excerpt_files: successfully unzipped ' +
                          exPath)
        except:
            ryw.give_bad_news('unzip_excerpt_files: failed to unzip ' + exPath,
                              logging.error)

    return True
        


def resize_thumbnails(auxDir, forced = True):

    if not os.path.exists(auxDir):
        return True

    thumbsDir = os.path.join(auxDir, 'thumbnails')
    if not os.path.exists(thumbsDir):
        return True

    thumbNames = os.listdir(thumbsDir)
    if len(thumbNames) == 0:
        return True

    for thumbName in thumbNames:
        if thumbName == 'Thumbs.db':
            continue
        thumbPath = os.path.join(thumbsDir, thumbName)
        if not ryw_view.is_image(thumbPath):
            ryw.give_bad_news(
                'resize_thumbnails: probably not an image file: ' +
                thumbPath, logging.error)
            return False

    scaledDir = os.path.join(auxDir, 'thumbs_scaled')
    if os.path.exists(scaledDir) and not forced:
        return True
    
    ryw.cleanup_path(scaledDir, 'ryw_upload.resize_thumbnails:')
    
    try:
        su.createdirpath(scaledDir)
        for thumbName in thumbNames:
            if thumbName == 'Thumbs.db':
                continue
            thumbPath = os.path.join(thumbsDir, thumbName)
            thumbDest = os.path.join(scaledDir, thumbName)
            if not ryw_view.resize_image(thumbPath, thumbDest):
                ryw.give_bad_news('resize_thumbnails: failed: ' +
                                  thumbPath + ' -> ' + thumbDest,
                                  logging.error)
                return False
    except:
        ryw.give_bad_news('failed to resize thumbnails.', logging.error)

    return True



def read_aux_files(form, aux, tmpdir, exists, localExcerptStuff = None):
    localBaseName = None
    if localExcerptStuff:
        localExcSuccess,localExcFound,localExcFilePath,localExcIsDir = \
            localExcerptStuff
        if localExcFound:
            localBaseName = fix_IE_file_name(localExcFilePath)
    else:
        localExcSuccess,localExcFound,localExcFilePath,localExcIsDir = \
            None,None,None,None
    
    auxInfo = {}

    if exists or localExcFound:
        logging.debug('read_aux_files: aux file exists.')
    else:
        logging.debug('read_aux_files: no aux files.')
        return (True, None, auxInfo)

    success,auxDir = create_aux_dir(tmpdir)
    if not success:
        return (False, None, None)


    if localExcFound:
        localSuccess,localFound,localBytes = \
            copy_local_file_for_upload(
                form, os.path.join(auxDir, 'excerpts'),
                localBaseName, localExcFound,
                localExcFilePath, localExcIsDir,
                isCopyingExcerpt = True)
        if not localSuccess:
            ryw.give_bad_news(
                'read_aux_files: copy_local_file_for_upload failed: ' +
                localExcFilePath, logging.error)
            return (False, None, None)
        if auxInfo.has_key('excerpts'):
            auxInfo['excerpts'].append(localBaseName)
        else:
            auxInfo['excerpts'] = [localBaseName]
        if not unzip_excerpt_files(auxDir):
            ryw.give_bad_news(
                'read_aux_files: unzip_excerpt_files failed: ' +
                auxDir, logging.error)
            return (False, None, None)
            

    #
    # only local excerpt upload, no remote.
    #
    if not exists:
        return (True, auxDir, auxInfo)


    i = 0
    for auxEntry in AUX_FIELD_ENTRIES:
        i += 1
        auxName,auxType = auxEntry
        if not aux[auxName]['exists']:
            continue
        success,kB = read_aux_file(form, aux, auxDir, auxName, auxType, i)
        if not success:
            return (False, None, None)
        fileName = form[auxName].filename
        fileName = os.path.normpath(fileName)
        fileName = os.path.basename(fileName)
        
        if auxInfo.has_key(auxType):
            auxInfo[auxType].append(fileName)
        else:
            auxInfo[auxType] = [fileName]

    logging.debug('read_aux_files: auxInfo: ' + repr(auxInfo))

    if not resize_thumbnails(auxDir):
        return (False, None, None)

    if not unzip_excerpt_files(auxDir):
        return (False, None, None)
    
    return (True, auxDir, auxInfo)



def read_aux_file(form, aux, auxDir, auxName, auxType, i):
    logging.debug('read_aux_file: dir, name, type: ' +
                  auxDir + ' ' + auxName + ' ' + auxType)
    kB,bytes = read_uploaded_file(form,
                                  aux[auxName]['buf'],
                                  os.path.join(auxDir, auxType),
                                  str(i) + '_' + form[auxName].filename,
                                  auxName)
    if kB == 0:
        return (False, 0)

    logging.debug('read_aux_file: successfully read: ' + auxType + ' ' +
                  form[auxName].filename)
    return (True, kB)



def add_aux_attributes(meta, auxInfo):
    logging.debug('add_aux_attributes: ' + repr(auxInfo))
    for auxType in AUX_FIELD_TYPES:
        if auxInfo.has_key(auxType):
            meta['aux_'+auxType] = auxInfo[auxType]
    logging.debug('add_aux_attributes: ' + repr(meta))
    return meta



def read_uploaded_file(form, buf, tmpdir, filename, field):
    """read the uploaded file and put it in the temp directory.
    returns the number of KB read, rounded to 4KB chunks."""

    filename = fix_IE_file_name(filename)
    tmpDataFile = open_tmp_data_file(tmpdir, filename)
    if not tmpDataFile:
        return (0, 0)

    freeKB = ryw.free_MB(tmpdir) * 1024
    kB = long(0)

    try:
        while buf:
            kB += 4
            if pretty_much_out_of_space(kB, freeKB):
                ryw.give_bad_news(
                    'user_error: nearly out of space while writing uploaded file, file kB seen so far: ' + repr(kB), logging.error)
                raise NameError('file write: out of space.')
            
            tmpDataFile.write(buf)
            buf = form[field].file.read(4096)

            #ryw.give_bad_news('read_uploaded_file: test wait for 60s.',
            #                  logging.error)
            #time.sleep(60)

        tmpDataFile.flush()
        tmpDataFile.close()
        logging.debug('temporary data file written')
        bytes = os.path.getsize(os.path.join(tmpdir, filename))
        return (kB, bytes)
    except:
        ryw.give_bad_news(
            'fatal_error: writing of temporary data file failed.',
            logging.critical)
        return (0, 0)



#uploadQueue
#  returns bytes
def copy_queue_file(tmpdir, name):
    
    rfpath = os.path.join(RepositoryRoot, 'QUEUES', name)
    if not ryw.is_valid_file(rfpath, 'copy_queue_file'):
        ryw.give_bad_news('copy_queue_file: queue file invalid: ' + rfpath,
                          logging.error)
        return (0, '')
    
    freeKB = ryw.free_MB(tmpdir) * 1024
    success,bytes = ryw.get_file_size(rfpath)
    if not success:
        return (0, '')
    kB = math.ceil(bytes / 1024.0)

    if pretty_much_out_of_space(kB, freeKB):
        ryw.give_bad_news(
            'user_error: nearly out of space while uploading queue, KB: ' + repr(kB), logging.error)
        return (0, '')

    #appendedName = name + '_selection'
    appendedName = 'saved_selection'
    tmpFileName = os.path.join(tmpdir, appendedName)
    try:
        shutil.copyfile(rfpath, tmpFileName)
    except:
        ryw.give_bad_news('copy_queue_file: failed to copy queue file: ' +
                          rfpath + ' -> ' + tmpFileName,
                          logging.critical)
        return (0, '')

    return (bytes, appendedName)



#
# returns (Success, Found, localName, IsDir)
#
def check_local_file(form, fieldName = 'repeat_local_filename'):
    if not form.has_key(fieldName):
        return (True, False, None, False)

    localName = form.getfirst(fieldName, '')
    if localName == '':
        return (True, False, None, False)

    success,isFile,isDir = ryw.is_valid_file_or_dir(
        localName, msg='check_local_file')
    if not success:
        return (False, False, None, False)
    localName = os.path.normpath(localName)

    if isFile:
        success,bytes = ryw.get_file_size(localName)
        if not success:
            return (False, False, None, False)
        if bytes == 0:
            ryw.give_bad_news('check_local_file: zero-sized file: '+
                              localName, logging.error)
            return (False, False, None, False)
        return (True, True, localName, False)

    return (True, True, localName, True)

    
    
#local file upload acceleration
#  returns (Success, Found, bytes)
def copy_local_file_for_upload(form, tmpdir, uploadFileName,
                               localFound, localPath, localDir,
                               isCopyingExcerpt = False):
    if not localFound:
        return (True, False, 0)

    if localDir:
        dirKB = ryw_disc.getRecursiveSizeInKB(localPath)
        bytes = dirKB * 1024
        if bytes == 0:
            ryw.give_bad_news(
                'copy_local_file_for_upload: 0-sized local directory: '+
                localPath, logging.error)
            return (False, False, 0)
    else:
        success,bytes = ryw.get_file_size(localPath)
        if not success:
            return (False, False, 0)

    #if uploadFileName != truncateLocalName:
    #    ryw.give_bad_news(
    #        'copy_local_file_for_upload: repeated local file name does<BR>' +
    #        ' not match the name of the local file to be uploaded.<BR>' +
    #        uploadFileName + '<BR>' + localName,
    #        logging.error)
    #    return (False, False, 0)
    
    freeKB = ryw.free_MB(tmpdir) * 1024
    kB = math.ceil(bytes / 1024.0)

    if pretty_much_out_of_space(kB, freeKB):
        ryw.give_bad_news(
            'copy_local_file_for_upload: nearly out of space ' +
            'while uploading queue, KB: ' + repr(kB), logging.error)
        return (False, False, 0)

    tmpFileName = os.path.join(tmpdir, uploadFileName)
    try:
        if localDir:
            ryw.give_news2('<BR>Copying local directory: ' + localPath,
                           logging.info)
            if isCopyingExcerpt:
                #
                # don't want the "excerpts" directory to contain
                # just a lone directory inside in the common case.
                # copy the content into the "excerpts" directory directly.
                # "tmpdir" in this case is the "excerpts" directory.
                # su.copytree tolerates an existing destination directory
                # and doesn't wipe out what's already in it.
                #
                tmpFileName = os.path.normpath(tmpdir)
                su.copytree(localPath, tmpFileName)
            else:
                shutil.copytree(localPath, tmpFileName)
        else:
            ryw.give_news2('<BR>Copying local file: ' + localPath,
                           logging.info)
            shutil.copyfile(localPath, tmpFileName)
            #shutil.copyfile(
            #    os.path.join(RepositoryRoot, 'Tmp-in', 'foo.txt'),
            #    tmpFileName)
    except:
        ryw.give_bad_news('copy_local_file_for_upload: ' +
                          'failed to copy data: ' +
                          localPath + ' -> ' + tmpFileName,
                          logging.critical)
        return (False, False, 0)

    logging.debug('copy_local_file_for_upload: ' +
                  'succeeded copying local data: ' +
                  localPath + ' -> ' + tmpFileName, logging.info)
    return (True, True, bytes)
    
    
    
#uploadQueue
def add_set_attrs(meta, attrName, attrValue):
    if not meta.has_key(attrName):
        meta[attrName] = set([])
    meta[attrName].add(attrValue)



def process_checkboxes(form, possibilities, prefix, categoryName, meta):
    """processes checkboxes, that have a text 'other' field at the end."""

    checked = []
    for possibility in possibilities:
        key = prefix + '_' + possibility
        value = form.getfirst(key, '')
        if value == 'on':
            checked.append(possibility)

    value = form.getfirst(prefix + '_other', '')
    if value != '': checked.append(value)

    value = form.getfirst(prefix + '_other_hindi', '')
    if value!= '':
        add_hindi_attribute(meta, categoryName, [value])

    if checked != []: meta[categoryName] = checked



def process_bracket(form, key1, key2, categoryName, meta):
    """process an attribute that consists of a pair of values."""

    oPair = ['unknown', 'unknown']
    if meta.has_key(categoryName):
        oPair = meta[categoryName]        
    
    val1 = form.getfirst(key1, '')
    val2 = form.getfirst(key2, '')
    if val1 != 'unknown' and val2 != 'unknown':
        meta[categoryName] = [val1, val2]

    return oPair



def get_real_upload_date_time(meta):
    #
    # non-editable upload time.
    # like get_change_date_time() below.
    # this is redundant.  i have done this before,
    # choosing the same in fact.
    #
    if meta.has_key('upload_datetime_real'):
        return meta
    miscDict = ryw.get_misc_dict()
    dateTimeStr = process_date_time_str(miscDict['uploaded_date_time_val'])
    if dateTimeStr != None:
        meta['upload_datetime_real'] = dateTimeStr
    return meta



def get_change_date_time(meta):
    #
    # non-editable change time.
    # like get_real_upload_date_time() above.
    # called by EditObject.main().
    #
    miscDict = ryw.get_misc_dict()
    dateTimeStr =  process_date_time_str(miscDict['uploaded_date_time_val'])
    if dateTimeStr != None:
        meta['change_datetime'] = dateTimeStr
    return meta



def process_date_time(form, meta):

    #
    # non-editable upload time.
    #
    meta = get_real_upload_date_time(meta)
    
    if not form.has_key('uploaded_date_time'):
        return True
    dateTimeStr = form.getfirst('uploaded_date_time', '')
    dateTimeStrCopy = dateTimeStr
    if dateTimeStr == '' or dateTimeStr.isspace():
        return True

    dateTimeRepr = process_date_time_str(dateTimeStr)
    if dateTimeRepr == None:
        ryw.give_bad_news('user_error: invalid date time field: ' +
                          dateTimeStrCopy, logging.info)
        return False

    meta['upload_datetime'] = dateTimeRepr
    return True



def process_date_time_str(dateTimeStr):
    ryw.db_print_info_browser('process_date_time_str: input: ' +
                              dateTimeStr, 99)
    dateTimeStr = dateTimeStr.replace(' ', ',')
    dateTimeStr = dateTimeStr.replace('-', ',')
    dateTimeStr = dateTimeStr.replace(':', ',')
    dateTimeStr = dateTimeStr + ',0'
    #
    # ugly hack to fix bug for chopping leading zeros.
    #
    dateTimeStr = dateTimeStr.replace(',,', ',0,')
    dateTimeStr = 'datetime.datetime(' + dateTimeStr + ')'
    ryw.db_print_info_browser('process_date_time_str: after replacement: ' +
                              dateTimeStr, 99)

    try:
        dateTime = eval(dateTimeStr)
        #logging.debug('process_date_time: ' + repr(dateTime))
        ryw.db_print_info_browser('process_date_time_str: eval success: ' +
                                  repr(dateTime), 99)
        return repr(dateTime)
    except:
        ryw.db_print_info_browser('process_date_time_str: '+
                                  'eval failed!!!!!', 99)
        ryw.give_bad_news('ryw_upload.process_date_time_str: eval failed: ' +
                          repr(dateTimeStr), logging.error)
        return None



def process_tricky_attributes(form, meta, filename):
    """hidden and obscure attributes."""

    meta['upload_datetime'] = repr(datetime.datetime.now())
    meta['upload_datetime_real'] = repr(datetime.datetime.now())
    #meta['upload_datetime'] = datetime.datetime.now()
    logging.debug('process_tricky_attributes: ' +
                  repr(meta['upload_datetime']))

    if not process_date_time(form, meta):
        return False    
    
    objectID = form.getfirst('object_ID', '')
    if not objectID:
        try:
            objectID = objectstore.generateNewObjectID()
        except:
            ryw.give_bad_news('fatal_error: unable to obtain new object ID.',
                              logging.critical)
            return False
    meta['id'] = objectID

    path = form.getfirst('path', '')
    if not path:
        contentType = form.getfirst('content_type', '')
        if not contentType:
            ryw.give_bad_news('fatal_error: unable to determine content type.',
                              logging.critical)
            return False
        now = datetime.datetime.now()
        monthStr = now.strftime('%y%m/')

        dateTimeRand = ryw.date_time_rand()
        filename = dateTimeRand + '_' + filename
        
        path = os.path.join('/upload', monthStr, contentType, filename)
    meta['path'] = os.path.normpath(path)
    ryw.db_print2('process_tricky_attributes: path is: ' + meta['path'], 57)
    
    return True



def get_hindi_attributes(meta):
    if meta.has_key('hindi'):
        return meta['hindi']
    return None

        

def process_hindi_attributes(form, meta, keys):
    hindi = get_hindi_attributes(meta)
        
    for key in keys:
        formStr = 'hindi_' + key
        value = form.getfirst(formStr, '')
        if value != '':
            if hindi == None:
                hindi = {}
            hindi[key] = value
    if hindi:
        meta['hindi'] = hindi



def add_hindi_attribute(meta, attrName, attrValue):
    hindi = get_hindi_attributes(meta)
    if hindi == None:
        hindi = {}
    hindi[attrName] = attrValue
    meta['hindi'] = hindi
    logging.debug('add_hindi_attribute: ' + attrName + ' = ' + repr(attrValue))
    logging.debug('add_hindi_attribute: ' + repr(meta))



def process_hindi_bracket(form, hindiKey1, hindiKey2,
                          englishCategoryName, meta,
                          oldPair = ['unknown', 'unknown']):
    hindiVal1 = form.getfirst(hindiKey1, '')
    hindiVal2 = form.getfirst(hindiKey2, '')
    if not hindiVal1 or not hindiVal2:
        return
    if hindiVal1 == ryw_hindi.UNTRANSLATED_STRING or \
       hindiVal2 == ryw_hindi.UNTRANSLATED_STRING:
        return
    englishVal1 = ryw_hindi.hindi_to_english(hindiVal1)
    englishVal2 = ryw_hindi.hindi_to_english(hindiVal2)
    if not englishVal1 or not englishVal2:
        ryw.give_bad_news(
            'process_hindi_bracket: warning: no hindi to english mapping: ' +
            ryw_hindi.html(hindiVal1) + ', ' + ryw_hindi.html(hindiVal2),
            logging.warning)
        return
    if englishVal1 == 'unknown' or englishVal2 == 'unknown':
        logging.debug('process_hindi_bracket: value is unknown: ' +
                      englishCategoryName)
        return

    if englishVal1 == oldPair[0] and englishVal2 == oldPair[1]:
        return
    
    meta[englishCategoryName] = [englishVal1, englishVal2]
    logging.debug('process_hindi_bracket: ' + englishCategoryName + ' = ' +
                  repr([englishVal1, englishVal2]))
    logging.debug('process_hindi_bracket: ' + repr(meta))



def process_English_dropdown(englishKey, form, meta):
    oldVal = 'unknown'
    if meta.has_key(englishKey):
        oldVal = meta[englishKey]
        if oldVal == '': 
            oldVal = 'unknown'
    
    value = form.getfirst(englishKey, '')
    if value != '' and value != 'unknown':
        meta[englishKey] = value

    return oldVal
    


def process_hindi_dropdown(englishKey, form, meta, oldVal = 'unknown'):
    hindiKey = 'hindi_' + englishKey
    hindiValue = form.getfirst(hindiKey, '')
    if hindiValue == '' or hindiValue == ryw_hindi.UNTRANSLATED_STRING:
        return
    englishValue = ryw_hindi.hindi_to_english(hindiValue)
    if englishValue == '':
        ryw.give_bad_news(
            'process_hindi_dropdown: warning: no hindi to english mapping: '+
            ryw_hindi.html(hindiValue), logging.warning)
        return
    if englishValue == 'unknown':
        logging.debug('process_hindi_dropdown: value is unknown: '+ englishKey)
        return

    if oldVal == englishValue:
        return
    
    meta[englishKey] = englishValue
    logging.debug('process_hindi_dropdown: ' + englishKey + ' = ' +
                  repr(englishValue))
    logging.debug('process_hindi_dropdown: ' + repr(meta))



def process_data_size(form, meta):
    if not form.has_key('size_text'):
        return True
    sizeStr = form.getfirst('size_text', '')
    if sizeStr == '' or sizeStr.isspace():
        return True

    if not sizeStr.isdigit():
        ryw.give_bad_news('user_error: invalid data size field: ' + sizeStr,
                          logging.info)
        return False
    
    try:
        sizeInt = int(sizeStr)
    except:
        ryw.give_bad_news('user_error: invalid data size field: ' + sizeStr,
                          logging.info)
        return False

    if not form.has_key('size_unit'):
        ryw.give_bad_news('error: no unit for data size.', logging.error)
        return False

    sizeUnit = form.getfirst('size_unit', '')

    if sizeUnit == 'B':
        bytes = sizeInt
    elif sizeUnit == 'KB':
        bytes = sizeInt * 1024
    elif sizeUnit == 'MB':
        bytes = sizeInt * 1024 * 1024
    else:
        ryw.give_bad_news('error: bad unit for data size: ' + sizeUnit,
                          logging.error)
        return False

    meta['bytes'] = bytes
    meta['kB'] = math.ceil(bytes / 1024.0)
    
    return True
    


def process_attributes(name, form, filename, kB, bytes):
    """produces the attribute dictionary."""
    
    meta = {}

    meta['filename'] = filename
    meta['creator'] = name
    meta['kB'] = kB
    meta['bytes'] = bytes

    if not process_data_size(form, meta):
        return None

    for key in ['title', 'description', 'author_name', 'uploaded_by_name',
                'content_alias', 'related_content', 'uploaded_by_site',
                'repeat_local_filename', 'chapter_number']:
        value = form.getfirst(key, '')
        if value != '': meta[key] = value

    if meta.has_key('uploaded_by_site') and meta['uploaded_by_site'] != '':
        meta['creator'] = meta['uploaded_by_site']

    # the Hindi free text counterparts.
    process_hindi_attributes(form, meta, \
        ['title', 'description', 'author_name', 'uploaded_by_name',
         'uploaded_by_site'])

    # attributes that can have an 'unknown' value that should be excluded.
    for key in ['content_type', 'class', 'video_resolution']:
        process_English_dropdown(key, form, meta)
        

    # the Hindi counter-parts.
    for key in ['content_type', 'class']:
        process_hindi_dropdown(key, form, meta)


    # subject checkboxes.
    process_checkboxes(form, POSSIBLE_SUBJECTS, 'subject', 'subjects', meta)

    # language checkboxes.
    process_checkboxes(form, POSSIBLE_LANGUAGES,
                       'language', 'languages', meta)

    # show or no show checkboxes
    process_checkboxes(form, POSSIBLE_SHOW, 'show', 'show', meta)

    # cache attribute checkbox.
    process_checkboxes(form, POSSIBLE_CACHE,
                       'cache', 'cache', meta)

    # age bracket.
    process_bracket(form, 'age_from', 'age_to', 'age', meta)
    process_hindi_bracket(form, 'hindi_age_from', 'hindi_age_to', 'age', meta)

    # media type.
    process_checkboxes(form, POSSIBLE_MEDIA, 'media', 'media', meta)

    # content duration
    process_bracket(form, 'time_length_hours', 'time_length_minutes',
                    'time_length', meta)

    # later added the seconds field
    process_English_dropdown('time_length_seconds', form, meta)

    if not process_tricky_attributes(form, meta, filename):
        #raise NameError('failed in process_tricky_attributes.')
        return None
        
    # print '<P>meta: ' + repr(meta)
    logging.debug('attribute dictionary: ' + repr(meta))
    return meta



def try_process_attributes(name, form, filename, kB, bytes):
    """outer-most function for getting all the attributes."""
    try:
        meta = process_attributes(name, form, filename, kB, bytes)
    except:
        ryw.give_bad_news('fatal_error: failed to process attributes',
                          logging.critical)
        meta = None
    return meta



def write_tmp_metafile(meta, tmpdir):
    """write the attributes to a temporary metafile."""

    metafile = tmpdir + '.META'

    try:
        su.pickdump(meta, metafile)
        logging.debug('temporary meta file written.')
        return (True, metafile)
    except:
        ryw.give_bad_news(
            'fatal_error: failed to write temporary metafile: '+metafile,
            logging.critical)
        return (False, metafile)

    

def try_unzip_file(form, tmpdir, filename, kB):
    """unzip the unploaded zip file.
    returns a tuple: the stuff to upload, and a temp extract directory
    that should be cleaned up."""
    
    extractDir = tmpdir + '.EXT'

    unzip = form.getfirst('unzip', '')
    
    if not unzip:
        return (os.path.join(tmpdir, filename), None)

    freeKB = ryw.free_MB(tmpdir) * 1024
    if pretty_much_out_of_space(kB, freeKB):
        ryw.give_bad_news(
            'user_error: nearly out of space while trying to unzip, zip file kB: ' + repr(kB), logging.error)
        return (None, extractDir)

    try:
        os.mkdir(extractDir)
    except:
        ryw.give_bad_news(
            'fatal_error: failed to make temporary extract directory.',
            logging.critical)
        return (None, extractDir)

    try:
        su.zipfile_extractall(os.path.join(tmpdir, filename), extractDir)
    except:
        ryw.give_bad_news('fatal_error: failed to extract zip file.',
                          logging.critical)
        return (None, extractDir)

    logging.debug('successfully extracted zipfile ' + filename + ' to ' +
                  extractDir)
    return (extractDir, extractDir)



def cleanup_incoming(tmpdir, jobFile):
    #ryw.cleanup_path(tmpdir,  'ReadIncomingCDStack.cleanup:')
    ryw.force_remove(tmpdir,  'ReadIncomingCDStack.cleanup:')
    ryw.cleanup_path(jobFile+'.JRQ', 'ReadIncomingCDStack.cleanup:')
    ryw.cleanup_path(jobFile+'.ERR', 'ReadIncomingCDStack.cleanup:')
    ryw.cleanup_path(jobFile+'.DON', 'ReadIncomingCDStack.cleanup:')



def check_robot_finished(jobFile):
    """returns doneFlag."""
    errExists  = os.path.exists(jobFile + '.ERR')
    doneExists = os.path.exists(jobFile + '.DON')
    if not errExists and not doneExists:
        return False
    if errExists:
        ryw.give_news(
            'check_robot_finished: .ERR file found: ' +
            jobFile, logging.warning)
    if doneExists:
        logging.debug('check_robot_finished: .DON file found: ' +
                      jobFile)
    return True



def verify_ffmpeg_existence(RepositoryRoot):
    commandPath = os.path.join(RepositoryRoot, FFMPEG_PATH_SUFFIX)
    if ryw.is_valid_file(commandPath, 'verify_ffmpeg_existence'):
        return commandPath
    ryw.give_news('Cannot find ffmpeg.  Advise you to install it.',
                  logging.info)
    return commandPath



def set_duration(meta, hours, minutes, seconds):
    meta['time_length'] = [hours, minutes]
    meta['time_length_seconds'] = seconds



def try_extract_duration(RepositoryRoot, meta, tmpdir, uploadFileName):
    commandPath = verify_ffmpeg_existence(RepositoryRoot)
    filePath = os.path.join(tmpdir, uploadFileName)
    executeThis = commandPath + ' -i ' + filePath

    if meta.has_key('time_length'):
        logging.info('try_extract_duration: duration already filled in.')
        return

    ryw.give_news('Invoking ffmpeg to extract duration...', logging.info)

    try:
        pipe = subprocess.Popen(executeThis, stderr=subprocess.PIPE)
        execResult = pipe.communicate()[1]
    except:
        ryw.give_bad_news('try_extract_duration: ffmpeg execution failed: '+
                          executeThis, logging.error)
        return

    ryw.give_news(execResult, logging.info)

    regex = r'Duration: ([0-9][0-9]):([0-9][0-9]):([0-9][0-9])\.'
    regexComp = re.compile(regex)
    searchResult = regexComp.search(execResult)

    if searchResult == None:
        return

    try:
        hours = searchResult.group(1)
        minutes = searchResult.group(2)
        seconds = searchResult.group(3)
    except:
        ryw.give_bad_news('try_extract_duration: regex failed on: ' +
                          execResult, logging.critical)
        return
    
    set_duration(meta, hours, minutes, seconds)

