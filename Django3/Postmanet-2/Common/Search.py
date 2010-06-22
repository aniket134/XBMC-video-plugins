import cgi, cgitb
cgitb.enable()

import sys, os
import pickle
import logging, datetime
import ryw, ryw_upload, ryw_view
import cnf_match
import ProcessDownloadReq
import ReverseLists
import Browse



NUM_OBJECTS_PER_PAGE = 10
DELETE_OLD_SEARCH_RESULT_SECONDS = 6000



def print_header():
    ryw_view.print_header_logo()
    print "<TITLE>Search the Repository</TITLE>"
    name = os.getenv("REMOTE_USER")
    #print '<P> Hello,', name
    #print '<BR>'
    return name



def setup_logging(logDir, logFile):
    """set up logging."""
    ryw.check_logging(logDir, logFile)
    logging.info('Search: entered...')



def parse_form(form):
    try:
        return parse_form_aux(form)
    except Exception, e:
        return None, None, None, None, 'Exception in parse_form: %s' % str(e)

def parse_keyword_search(form, query, search_attributes, html_key, meta_key):
    words = form.getfirst(html_key)
    if not words:
        return
    search_attributes[html_key] = words
    words = words.strip()
    words = words.split()

    case = form.getfirst(html_key + '_case')
    if case == 'insensitive':
        options = ['nocase']
        search_attributes[html_key + '_case'] = 'insensitive'
    else:
        options = []
        search_attributes[html_key + '_case'] = 'sensitive'

    any_or_all = form.getfirst(html_key + '_match_any_or_all')
    assert any_or_all in ['any', 'all']
    search_attributes[html_key + '_match_any_or_all'] = any_or_all

    if any_or_all == 'any': ## (title has word0 or title has word1 or ...)
        clause = []
        for word in words:
            literal = (meta_key, ['contains'] + options, word)
            clause.append(literal)
        query.append(clause)
    else:
        for word in words:
            literal = (meta_key, ['contains'] + options, word)
            clause = [literal]
            query.append(clause)

def parse_checkboxes_search(form, query, search_attributes, possibilities, prefix, categoryName):

    checked = []
    for possibility in possibilities:
        key = prefix + '_' + possibility
        value = form.getfirst(key, '')
        if value == 'on':
            checked.append(possibility)
            search_attributes[key] = value

    value = form.getfirst(prefix + '_other', '')
    if value != '':
        checked.append(value)
        search_attributes[prefix + '_other'] = value

    if not checked:
        return

    words = checked

    any_or_all = form.getfirst(categoryName + '_match_any_or_all')
    assert any_or_all in ['any', 'all']

    search_attributes[categoryName + '_match_any_or_all'] = any_or_all

    options = ['nocase']

    if any_or_all == 'any':
            clause = []
            for word in words:
                    literal = (categoryName, ['equals'] + options, word)
                    clause.append(literal)
            query.append(clause)
    else:
            for word in words:
                    literal = (categoryName, ['equals'] + options, word)
                    clause = [literal]
                    query.append(clause)

def parse_person_name_search(form, query, search_attributes, html_key, meta_key):
    words = form.getfirst(html_key)
    if not words:
        return
    search_attributes[html_key] = words
    words = words.strip()
    words = words.split()

    options = ['nocase']

    clause = []
    for word in words:
        literal = (meta_key, ['contains'] + options, word)
        clause.append(literal)
    query.append(clause)

def parse_equality_search(form, query, search_attributes, html_key, meta_key):
    value = form.getfirst(html_key)
    if not value or value == 'unknown':
        return
    search_attributes[html_key] = value

    query.append([(meta_key, 'equals', value)])

def parse_pair_value_search(form, query, search_attributes, operation_key, key_1, key_2, meta_key):
    value_1 = form.getfirst(key_1)
    value_2 = form.getfirst(key_2)

    if value_1 is None or value_2 is None or value_1 == 'unknown' or value_2 == 'unknown':
        return

    search_attributes[key_1] = value_1
    search_attributes[key_2] = value_2

    value = [value_1, value_2]

    operation = form.getfirst(operation_key)

    literal = None
    if operation == 'at_least':
        literal = (meta_key, '>=', value)
        search_attributes[operation_key] = operation
    elif operation == 'equals':
        literal = (meta_key, '==', value)
        search_attributes[operation_key] = operation
    elif operation == 'at_most':
        literal = (meta_key, '<=', value)
        search_attributes[operation_key] = operation

    if literal is not None:
        query.append([literal])

def get_datetime(form, search_attributes, year_key, month_key, day_key):
    svalues = [form.getfirst(key) for key in [year_key, month_key, day_key]]
    ivalues = []
    for s in svalues:
        try:
            i = int(s)
        except:
            ivalues = []
            break
        ivalues.append(i)
    if not ivalues:
        return None
    year, month, day = ivalues
    try:
        d = datetime.datetime(year, month, day)
    except:
        return None

    for key in [year_key, month_key, day_key]:
        search_attributes[key] = form.getfirst(key)

    return d

def parse_upload_datetime_range(form, query, search_attributes):
    lower_limit = get_datetime(form, search_attributes,
                               'uploaded_after_year', 'uploaded_after_month', 'uploaded_after_day')
    if lower_limit:
        query.append([('upload_datetime', '>= eval_value', lower_limit)])

    upper_limit = get_datetime(form, search_attributes,
                               'uploaded_before_year', 'uploaded_before_month', 'uploaded_before_day')
    if upper_limit:
        upper_limit = upper_limit + datetime.timedelta(days=1)
        query.append([('upload_datetime', '< eval_value', upper_limit)])

Subjects_possibilities = ['English', 'Hindi', 'Sanskrit', 'science',
                          'physics', 'chemistry', 'astronomy', 'biology',
                          'mathematics', 'arithmetic', 'algebra',
                          'geometry', 'history', 'social_studies',
                          'agriculture', 'general_knowledge',
                          'food_nutrition', 'art_craft',
                          'computer_literacy', 'games', 'stories']

Language_possibilities = ['English', 'Hindi']

Media_possibilities = ['video', 'DVD', 'VCD', 'Plextor', 'webcam',
                       'CamStudio', 'SMIL', 'audio', 'flash', 'images',
                       'powerpoint', 'documents']

def parse_form_aux(form):
    ## query, sort_tuple, start_index, search_attributes, error_message

    search_attributes = {}

    ## start_index
    start_index = form.getfirst('start_index')
    if start_index is None:
        start_index = 0
    else:
        start_index = int(start_index)

    ## sort_tuple
    if form.getfirst('sort_order') == 'decreasing':
        sort_order = 'decreasing'
        search_attributes['sort_order'] = 'decreasing'
    else:
        sort_order = 'increasing'
        search_attributes['sort_order'] = 'increasing'

    sort_field = form.getfirst('sort_field')
    assert sort_field
    search_attributes['sort_field'] = sort_field
    sort_tuple = (sort_field, sort_order)

    ## make query by parsing different parts of the search page
    query = []

    parse_keyword_search(form, query, search_attributes, 'all_keys_concatenated', 'all_keys_concatenated')
    parse_keyword_search(form, query, search_attributes, 'title', 'title')
    parse_keyword_search(form, query, search_attributes, 'description', 'description')

    parse_checkboxes_search(form, query, search_attributes, Subjects_possibilities, 'subject', 'subjects')
    parse_checkboxes_search(form, query, search_attributes, Language_possibilities, 'language', 'languages')
    parse_checkboxes_search(form, query, search_attributes, Media_possibilities, 'media', 'media')

    parse_equality_search(form, query, search_attributes, 'content_type', 'content_type')
    parse_equality_search(form, query, search_attributes, 'class', 'class')
    parse_equality_search(form, query, search_attributes, 'video_resolution', 'video_resolution')
    parse_equality_search(form, query, search_attributes, 'object_ID', 'id')

    ## I don't think age from/to search is meaningful
    ## One can imagine some kind of 'interval matching', but it seems beyond what's needed right now
    ## parse_pair_value_search(form, query, search_attributes, 'age_match', 'age_from', 'age_to', 'age')
    ## where hidden attribute 'age_match' is always 'interval_match', etc..

    parse_pair_value_search(form, query, search_attributes, 'duration_constraint', 'duration_hours', 'duration_minutes', 'time_length')

    parse_person_name_search(form, query, search_attributes, 'author_name', 'author_name')
    parse_person_name_search(form, query, search_attributes, 'uploaded_by_name', 'uploaded_by_name')

    parse_upload_datetime_range(form, query, search_attributes)

    return query, sort_tuple, start_index, search_attributes, None

def print_next_page_button1(search_attributes, next_start_index, scriptName,
                            numMatches):

    ## form_begin
    buttonStr = '''

    <HR><P>
    <FORM ACTION="%(scriptName)s" METHOD="post"
    ENCTYPE="multipart/form-data">

    <INPUT TYPE="submit" VALUE="matches %(beginIndex)s - %(endIndex)s">

    '''
    dict = {}
    dict['scriptName'] = scriptName
    dict['beginIndex'] = str(next_start_index + 1)
    dict['endIndex']   = str(next_start_index + NUM_OBJECTS_PER_PAGE)
    print buttonStr % dict

    ## search attributes as hidden fields
    for name, value in search_attributes.items():
        print '<INPUT TYPE="HIDDEN" NAME="%s" VALUE="%s">' % (name, value)

    print '<INPUT TYPE="HIDDEN" NAME="%s" VALUE="%s">' % ('start_index', next_start_index)

    ## form end
    #print '</FORM>'



def print_next_page_button1(search_attributes, next_start_index, scriptName,
                            numMatches):

    if next_start_index >= numMatches:
        return

    ## form_begin
    buttonStr = '''

    <BR>
    <FORM ACTION="%(scriptName)s" METHOD="post"
    ENCTYPE="multipart/form-data">

    <INPUT TYPE="submit" VALUE="next matches: %(beginIndex)s - %(endIndex)s">

    '''
    dict = {}
    dict['scriptName'] = scriptName
    dict['beginIndex'] = str(next_start_index + 1)
    dict['endIndex']   = str(next_start_index + NUM_OBJECTS_PER_PAGE)
    print buttonStr % dict

    ## search attributes as hidden fields
    for name, value in search_attributes.items():
        print '<INPUT TYPE="HIDDEN" NAME="%s" VALUE="%s">' % (name, value)

    print '<INPUT TYPE="HIDDEN" NAME="%s" VALUE="%s">' % ('start_index', next_start_index)

    print '<BR>'

    ## form end
    #print '</FORM>'



def print_next_page_button2(search_attributes, next_start_index, scriptName,
                            numMatches):

    if next_start_index >= numMatches:
        return

    buttonStr = '''
    <BR>
    <INPUT TYPE="submit" VALUE="next matches: %(beginIndex)s - %(endIndex)s">

    '''
    dict = {}
    dict['beginIndex'] = str(next_start_index + 1)
    dict['endIndex']   = str(next_start_index + NUM_OBJECTS_PER_PAGE)
    print buttonStr % dict

    print '</FORM>'
    


def read_index_file_to_get_metas(searchFile):
    try:
	return read_index_file_to_get_metas_aux(searchFile)
    except Exception, e:
	return None, 'Exception in read_index_file_to_get_metas: %s' % str(e)

def read_index_file_to_get_metas_aux(searchFile):
    ## TODO: Rewrite this using the new fancy SearchFile abstraction

    file_name = searchFile
    #RYW: changed to "rb"
    f = open(file_name, "rb")

    index = []

    while True:
	try:
            item = pickle.load(f)
        except ValueError:
            item,f = ryw.pickle_reopen_read(file_name, f, "rb")
	except EOFError:
            break
	except Exception, e:
            return None, 'Error in pickle.load of %s. Number of items successfully read %d. Error: %s' % (file_name, len(index), str(e))

	index.append(item)

    return index, None

def sort_matches(matches, sort_tuple):
    try:
	return sort_matches_aux(matches, sort_tuple)
    except Exception, e:
	return None, 'Exception in sort_matches: %s' % str(e)



def changed_time_key(meta):
    """returns the maximum (latest) of the three times."""
    uploadTime = eval(meta['upload_datetime'])

    #
    # this is a hack for a mistake.  it should never have been
    # None, but it is in some objects.
    #
    if meta.has_key('change_datetime') and meta['change_datetime'] != None:
        changeTime = eval(meta['change_datetime'])
    else:
        changeTime = uploadTime
    
    if meta.has_key('upload_datetime_real'):
        realTime = eval(meta['upload_datetime_real'])
    else:
        realTime = uploadTime
        
    if uploadTime < realTime:
        uploadTime = realTime

    if uploadTime < changeTime:
        uploadTime = changeTime

    return uploadTime

    

def sort_matches_aux(matches, sort_tuple):
    sort_field, sort_order = sort_tuple

    N = len(matches)

    temp = []

    if sort_field == 'Upload_Time':
	for i in range(N):
		match = matches[i]
		key = eval(match['upload_datetime'])
		temp.append((key, i, match))
    elif sort_field == 'Changed_Time':
	for i in range(N):
                match = matches[i]
                key = changed_time_key(match)
		temp.append((key, i, match))
    elif sort_field == 'Title':
	for i in range(N):
		match = matches[i]
		key = match['title']
		temp.append((key, i, match))
    elif sort_field == 'Author_Name':
	for i in range(N):
		match = matches[i]
		key = match['author_name']
		temp.append((key, i, match))
    else:
	return None, 'Invalid sort field specified'

    temp.sort()

    r = []
    if sort_order == 'decreasing':
	for i in range(N):
		dummy1, dummy2, match = temp[N - 1 - i]
		r.append(match)
    else:
	for i in range(N):
		dummy1, dummy2, match = temp[i]
		r.append(match)

    return r, None

def display_object(meta):
    ## TODO: rewrite this to do fancy formatting and adding hyperlinks for objects, etc.
    print '<HR>'
    print '<P>'
    keys = meta.keys()
    keys.sort()

    for key in keys:
        print '<BR> %s: %s' % (key, meta[key])



def main(logDir, logFile, searchFile, scriptName, resources = None):
    """main function processing search request."""

    # initialization.
    name = print_header()
    form = cgi.FieldStorage()
    setup_logging(logDir, logFile)

    ## cgi.print_form(form)

    ## parse the form to get: query, sorting information, start_index
    ## to know which subset of matches/results to return,
    ## search_attributes for the next_page_button
    query, sort_tuple, start_index, search_attributes, error_message = \
           parse_form(form)
    if query is None:
	print '<P> ERROR while parsing form and constructing ' + \
              'search query:', error_message
	sys.exit(1)

    ## print '<HR>Query:', query

    ## read index file to get the list of dictionaries:
    ## one dictionary for each version of each object, contains its meta-data

    #
    # used to open search file without read.
    # because Sobti is doing the read by himself below.
    # I have to change this because the SearchFile will be passed
    # onto the ReverseLists module for more later lookups.
    # this makes it necessary to do a real SearchFile open.
    #
    #success,searchFileLock = ryw.open_search_file(
    #    'Search:', logDir, logFile, searchFile, False, skipRead = True)
    success,searchFileLock = ryw.open_search_file(
        'Search:', logDir, logFile, searchFile, False, skipRead = False)
    if not success:
        ryw.give_bad_news('Search: failed to acquire search file lock: ' +
                          searchFile, logging.critical)
        ryw_upload.quick_exit(1)
    #else:
        #
        # mis-named: it's really not a searchFileLock, but searchFile itself.
        #
        #displayObject.set_search_file(searchFileLock)
        

    #
    # this is when Sobti used to do his own read, now replaced by mine.
    #
    #metas, error_message = read_index_file_to_get_metas(searchFile)
    metas = searchFileLock.convert_to_sobti_list()
    if metas is None:
	print '<P> ERROR while reading the index file to get ' + \
              'the meta-data dictionaries:', error_message
        searchFileLock.done()
        ryw_upload.quick_exit(1)

    ## build a list of metas that satisfy the given query
    matches = []
    for meta in metas:
        if not ryw_view.should_show_object(meta, resources):
            continue
	if cnf_match.matches_cnf(meta, query):
            matches.append(meta)
            ryw.db_print2('Search:main() ' + repr(meta), 53)

    num_matches = len(matches)

    ## sort the matches by the given sort tuple
    matches, error_message = sort_matches(matches, sort_tuple)
    if matches is None:
	print '<P> ERROR while sorting matches:', error_message
        searchFileLock.done()
        ryw_upload.quick_exit(1)


    #
    # save all current search results in a file for
    # possible inclusion in the current selection.
    #
    matchAllName = save_matches(matches)
    

    ## Return the start_index..(start_index + N) entries from the top
    if num_matches == 0 or start_index >= num_matches:
	num_items = 0
    else:
	start_index = max(0, start_index)
        assert start_index < num_matches

	end_index = start_index + NUM_OBJECTS_PER_PAGE - 1
	end_index = max(0, end_index)
	end_index = min(num_matches - 1, end_index)

	if not (0 <= start_index <= end_index < num_matches):
            print '<P> ASSERT ERROR: start_index, end_index, ' + \
                  'num_matches', start_index, end_index, num_matches
            searchFileLock.done()
            ryw_upload.quick_exit(1)

	num_items = end_index - start_index + 1

    ## num_items is the number of items that will actually be displayed
    ## num_items <= num_matches
    if num_items == 0:
	print '<P><H3>No objects to display</H3>'
        searchFileLock.done()
        ryw_upload.quick_exit(1)
    else:
	#print '<P><H3>%d objects satisfy the search criteria, ' + \
        #      'displaying %d of them</H3>' % (num_matches, num_items)
        print """
<BR><B><FONT SIZE=2>%d
object(s) satisfy the search criteria.</FONT></B>""" % \
              (num_matches)
        print """
<BR><B><FONT SIZE=2>displaying matches %d - %d.</FONT></B><BR>""" % \
              (start_index + 1, start_index + num_items)

        print_next_page_button1(search_attributes, end_index + 1, scriptName,
                                num_matches)

        shownMatches = []
        
        success,reverseLists = ReverseLists.open_reverse_lists(
            'Search:', '', '',
            os.path.join(RepositoryRoot, 'ReverseLists'), True,
            searchFile = searchFileLock,
            repositoryRoot = RepositoryRoot)
        if not (success and reverseLists):
            ryw.give_bad_news('Search.main: failed to open ReverseLists.',
                              logging.critical)
            if reverseLists:
                reverseLists.done()
            return False

        displayObject = ryw_view.DisplayObject(
            RepositoryRoot, calledByVillageSide = False,
            missingFileFunc=Browse.reqDownloadFunc,
            searchFile = searchFileLock,
            reverseLists = reverseLists)
        
        displayObject.begin_print()
	for i in range(start_index, end_index + 1):
            #display_object(matches[i])
            displayObject.show_an_object_compact(matches[i])
            shownMatches.append(matches[i])
        displayObject.end_print()
        reverseLists.done()

        #
        # save search results on this page in a file for
        # possible inclusion in the current selection.
        #
        matchThisPageName = save_matches(shownMatches)

        print_selection_links(matchAllName, matchThisPageName)
        
    	## Include a next-page button
	print_next_page_button2(search_attributes, end_index + 1, scriptName,
                                num_matches)

    searchFileLock.done()
    ryw_view.print_footer()


    
def search_for_objects(searchFile, query):
    # returns a list of matching metas

    # TODO: Add locking to searchFile, I am not comfortable dealing with your log files..
    # For my purposes, I'll do my own logging. So let this thing raise an exception if
    # there is an error.

    metas, error_message = read_index_file_to_get_metas(searchFile)
    if metas is None:
        raise Exception('Error reading searchFile %s: %s' % (searchFile, error_message))

    ## build a list of metas that satisfy the given query
    matches = []
    for meta in metas:
	if cnf_match.matches_cnf(meta, query):
		matches.append(meta)

    return matches



def decide_search_result_dir():
    resources = ryw.get_resources(
        os.path.join(RepositoryRoot,'Resources.txt'))
    if not resources:
        return None

    tmpOutDir = ryw.get_resource_str(resources, 'tmpout')
    if not tmpOutDir:
        ryw.give_bad_news('decide_search_result_dir: no tmpout directory.',
                          logging.error)
        return None

    tmpSearchResultDir = os.path.join(tmpOutDir, 'SearchResults')
    return tmpSearchResultDir



#
# returns (success, tmpDirName, name)
#
def get_save_search_name():

    badResult = (False, None, None)
    tmpSearchResultDir = decide_search_result_dir()
    if not tmpSearchResultDir:
        ryw.give_bad_news('decide_search_result_dir failed.', logging.error)
        return badResult

    if not os.path.exists(tmpSearchResultDir):
        try:
            os.makedirs(tmpSearchResultDir)
        except:
            ryw.give_bad_news(
                'get_save_search_name: failed to create temporary ' +
                'search results directory: '+
                tmpSearchResultDir, logging.critical)
            return badResult

    if ryw_upload.check_free_space(tmpSearchResultDir,
				   supressWarning = True) <= 0:
        ryw.give_bad_news(
            'get_save_search_name: failed space check :' +
            tmpSearchResultDir, logging.error)
        return badResult

    name = ryw.date_time_rand()
    return (True, tmpSearchResultDir, name)



def make_selection_list(matches):
    selList = []
    for match in matches:
        objstr = match['id'] + '#' + str(match['version'])
        selList.append(objstr)
    return selList



def cleanup_old_search_results(tmpDir, selName):
    isDir = ryw.is_valid_dir(tmpDir, msg='cleanup_old_search_results')
    if not isDir:
        logging.debug('cleanup_old_search_results: found no result dir.')

    try:
        files = os.listdir(tmpDir)

        latestFileName = os.path.join(tmpDir, selName)
        latestFileCtime = os.path.getctime(latestFileName)

        for oneFile in files:
            if oneFile == selName:
                continue
            oneFileName = os.path.join(tmpDir, oneFile)
            oneFileCtime = os.path.getctime(oneFileName)
            if latestFileCtime - oneFileCtime > DELETE_OLD_SEARCH_RESULT_SECONDS:
                ryw.cleanup_path(oneFileName, 'cleanup_old_search_results')
    except:
        ryw.give_bad_news('cleanup_old_search_results failed: ' +
                          tmpDir + ' -- ' + selName, logging.error)



#
# returns the random name identifying the saved selections.
#
def save_matches(matches):
    if matches == None or len(matches) == 0:
        ryw.give_news('save_matches: no match to save', logging.warning)
        return None

    success,tmpDir,selName = get_save_search_name()
    if not success:
        ryw.give_bad_news(
            'save_matches: failed to determine selection file name',
            logging.error)
        return None

    selList = make_selection_list(matches)

    #
    # copied from ProcessDownloadReq.py
    #
    success,tmppath,bakpath = ProcessDownloadReq.write_reqs(
        os.path.join(tmpDir, selName), set(selList))
    ProcessDownloadReq.cleanup(tmppath, bakpath)

    if not success:
        ryw.give_bad_news(
            'save_matches: ProcessDownloadReq.write_reqs failed: ' +
            os.path.join(tmpDir, selName), logging.error)
        return None

    cleanup_old_search_results(tmpDir, selName)

    return selName



def print_selection_links_text_not_used(matchAllName, matchThisPageName):

    name = os.getenv("REMOTE_USER")
    if name == '' or name == 'guest':
        return
    
    if matchAllName:
        linkStr = """
<BR>
<A HREF="/cgi-bin/AddSearchAll.py?sel=%(selName)s"
onClick="return confirm('Add all search results to the current selection?');">add
all search results to the current selection</A>
"""
        dict = {}
        dict['selName'] = matchAllName
        print linkStr % dict

    if matchThisPageName:
        linkStr = """
<BR>
<A HREF="/cgi-bin/AddSearchAll.py?sel=%(selName)s"
onClick="return confirm('Add search results on this page to the current selection?');">add
search results on this page to the current selection</A>
"""
        dict = {}
        dict['selName'] = matchThisPageName
        print linkStr % dict

    print '<BR>'



def print_selection_links(matchAllName, matchThisPageName):

    name = os.getenv("REMOTE_USER")
    if name == '' or name == 'guest':
        return

    print ryw_view.confirm_popup_js()

    if matchThisPageName:
        buttonStr = ryw_view.select_button_string(
            '/cgi-bin/AddSearchAll.py',
            'sel', matchThisPageName,
            'Add search results on this page to the current selection?',
	    ryw_view.CONFIRM_WIDTH,  ryw_view.CONFIRM_HEIGHT, 
            '/icons/select_add_page.png',
	    ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT, 
            'Add search results on this page to the current selection',
	    appendBlanks = True)
        print '<BR>'
        print buttonStr
    
    if matchAllName:
        buttonStr = ryw_view.select_button_string(
            '/cgi-bin/AddSearchAll.py',
            'sel', matchAllName,
            'Add all search results to the current selection?',
	    ryw_view.CONFIRM_WIDTH,  ryw_view.CONFIRM_HEIGHT, 
            '/icons/select_add_all.png',
	    ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT, 
            'Add all search results to the current selection',
            appendBlanks = True)
        print buttonStr

    clearSaveButtonStr = ryw_view.clear_save_sel_buttons(name)
    print clearSaveButtonStr

    if name == 'admin' and matchThisPageName:
        buttonStr = ryw_view.select_button_string2(
            '/cgi-bin/DelSearchAll.py?' + 'sel=' + matchThisPageName,
            'Danger: do you really want to destroy all the actual data '+
            'belonging to the objects on this page??!!',
            '/icons/page_star_equal_0.png',
	    ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT, 
            'Danger: destroy data belonging to objects on this page',
	    appendBlanks = True)
        print buttonStr
        
    if name == 'admin' and matchAllName:
        buttonStr = ryw_view.select_button_string2(
            '/cgi-bin/DelSearchAll.py?' + 'sel=' + matchAllName,
            'Danger: do you really want to destroy all the actual data '+
            'belonging to the objects found by this search??!!',
            '/icons/all_star_equal_0.png',
	    ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT, 
            'Danger: destroy data belonging to objects of this search',
	    appendBlanks = True)
        print buttonStr
        
    print '<BR>'

