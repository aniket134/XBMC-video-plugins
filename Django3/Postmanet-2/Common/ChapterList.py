import sys, os
import su
import logging, ryw
import pickle
#import win32file
#import win32con
#import win32security
#import win32api
#import pywintypes
import Flock
import ryw_meta
import urllib
import ryw_view
import copy



#
# name of the file that holds the chapter list.
#
CHAPTER_LIST_NAME = 'chapter_list'



def create_and_initialize(objstr, reqList, searchFile, reverseLists,
                          chapterFullName):
    """10/24/08: called by ChapterListForm.py"""

    chapterList = ChapterList(objstr)
    success = chapterList.initialize_with_meta_list(
        reqList, searchFile, reverseLists)

    if not success:
        ryw.give_bad_news('ChapterList.create_and_initialize: ' +
                          'initialize_with_meta_list failed.',
                          logging.error)
        return (False, None)

    success = chapterList.read_list_and_merge(chapterFullName)
    if not success:
        ryw.give_bad_news('ChapterList.create_and_initialize: ' +
                          'read_list_and_merge failed.',
                          logging.error)
        return (False, None)

    return (True,chapterList)
    


class ChapterList:
    def __init__(self, objstr):
        self.objstr = objstr

        #
        # the following two are set by initialize_with_meta_list() below.
        #
        self.chapterDict = None
        self.itemList = None
        self.metaList = None

        #
        # this is to be set by process_form().
        # 
        self.formEntries = None

        #
        # this will be set by compare_form_entries_against_meta()
        # in preparation for writing to disk.
        #
        # this is written to the disk in write_file().
        #
        # this is also where we put it after read from the disk.
        # 
        self.chapterList = None
        return



    def initialize_with_meta_list(self, reqList, searchFile, reverseLists):
        """called by ChapterListForm() to initialize chapter list from
        the meta data.
        modeled after ShowQueue.go_through_list().
        also called by ChapterListFormHandle()."""

        success = True
        
        if not searchFile or not reverseLists:
            raise NameError('ChapterList.initialize_with_meta_list:' +
                            'bad searchFile or bad reverseLists.')

        metaList = ryw_meta.get_meta_list(reqList, searchFile)
        searchFile.done()

        metaList = ryw.sortmeta_chapter_number(metaList)

        ryw.db_print2('initialize_with_meta_list: done sorting.', 38)

        numMatches = len(metaList)

        if numMatches <= 0:
            ryw.give_news('ChapterList: the selection is empty.<br>',
                          logging.error)
            success = False
        else:
            self.chapterDict = {}
            self.itemList = []
            self.metaList = metaList

            for meta in metaList:
                objID = meta['id']
                version = meta['version']
                objstr = objID + '#' + str(version)
                self.itemList.append(objstr)

                title = ''
                if meta.has_key('title'):
                    title = meta['title']

                chapter = None
                if meta.has_key('chapter_number'):
                    chapter = meta['chapter_number']

                alias = None
                if meta.has_key('content_alias'):
                    alias = meta['content_alias']

                self.chapterDict[objstr] = [alias, title, chapter]

            ryw.db_print2('chapterDict is: ' + repr(self.chapterDict), 41)
        
        return success


    
    def make_form_string(self):
        """called by ChapterListForm() to display the chapter edit form."""

        self.re_sort_items()
        
        pageStr1 = """
<BR>
<FORM ACTION="/cgi-bin/ChapterListFormHandle.py"
METHOD="post" ENCTYPE="multipart/form-data">

<INPUT TYPE="submit" VALUE="Save">
<P>

<INPUT TYPE="HIDDEN" NAME="objstr" VALUE="%(objstr)s">
<INPUT TYPE="HIDDEN" NAME="selection_length" VALUE="%(selectionLength)s">

%(itemLines)s

<BR>
<INPUT TYPE="submit" VALUE="Save">

</FORM>
"""

        selLen = len(self.itemList)
        dict = {}
        #
        # this is the objstr of the saved selection.
        #
        dict['objstr'] = self.objstr
        dict['selectionLength'] = str(selLen)

        itemLines = ''
        itemLines += '<TABLE CLASS=search>\n\n'

        #
        # BGCOLOR="bef7f7"
        #
        headerRow = """
<TR>
<TD class=search BGCOLOR="c3d9ff"><FONT SIZE=2><B>title</B></FONT></TD>
<TD class=search BGCOLOR="c3d9ff"><FONT SIZE=2><B>alias</B></FONT></TD>
<TD class=search BGCOLOR="c3d9ff"><FONT SIZE=2><B>chapter</B></FONT></TD>
<TD class=search BGCOLOR="c3d9ff" ALIGN=CENTER><FONT SIZE=2>
<B>id</B></FONT></TD>
</TR>"""
        itemLines += headerRow
        
        #
        # itemNumber is used to postfix field names.
        #
        itemNumber = 0
        for itemStr in self.itemList:
            itemLines += '<TR>\n'
            
            #
            # 5th is the title field.
            #
            itemLines += '<TD CLASS=search>\n'
            itemLines += '<FONT size=1>'
            titleField = ''
            if self.chapterDict.has_key(itemStr):
                title = self.chapterDict[itemStr][1]
                if title:
                    titleField = title
            itemLines += titleField + '</FONT>\n'
            itemLines += '</TD>\n'
            
            #
            # 4th is the alias field.
            #
            itemLines += '<TD CLASS=search>\n'
            itemLines += '<FONT size=1>'
            aliasField = ''
            if self.chapterDict.has_key(itemStr):
                alias = self.chapterDict[itemStr][0]
                if alias:
                    aliasField = alias
            itemLines += aliasField + '</FONT>\n'
            itemLines += '</TD>\n'

            #
            # 3rd is the text entry box for the chapter number, like:
            # <INPUT TYPE="TEXT" NAME="chapter_number0" SIZE="10" VALUE=foo>
            #
            chapterEntryField = '<INPUT TYPE="TEXT"' + \
                'NAME="%(fieldName)s" SIZE="10" VALUE="%(chapterValue)s">\n'
            d3 = {}
            d3['fieldName'] = 'chapter_number' + str(itemNumber)
            d3['chapterValue'] = ''
            ryw.db_print('itemStr is: ' + itemStr, 39)
            if self.chapterDict.has_key(itemStr):
                defaultChapter = self.chapterDict[itemStr][2]
                if defaultChapter:
                    ryw.db_print('found default chapter: ' + defaultChapter,
                                 39)
                    d3['chapterValue'] = defaultChapter
                else:
                    ryw.db_print('found no default chapter', 39)
            else:
                ryw.db_print('itemStr ' + itemStr + ' not found.', 39)
                    
            itemLines += '<TD CLASS=SEARCH>\n'
            itemLines += chapterEntryField % d3
            itemLines += '</TD>\n'
            itemLines += '\n'

            #
            # 1st is the objstr of the item, printed on the page.
            #
            # 09/12/20: now it's a link to a popup of the object.
            # the popup_js() is in ryw_view.py.
            #
            url = '/cgi-bin/DisplayObject.py?objstr=' + urllib.quote(itemStr)
            linkStr = """<a href="%s" onClick="return popup_js('%s', 950, 500);">%s</a>""" % (url, url, itemStr)
            itemLines += '<TD CLASS=search>\n'
            itemLines += '<FONT SIZE="1" FACE=COURIER>' + linkStr + '</FONT>'
            itemLines += '\n'

            #
            # 2nd is the hidden field for the objstr, like:
            # <INPUT TYPE="HIDDEN" NAME="item_objstr0" VALUE=objstr>
            #
            hiddenItemStrField = '<INPUT TYPE="HIDDEN" ' + \
                'NAME="%(fieldName)s" VALUE="%(itemStr)s">\n'
            d2 = {}
            d2['fieldName'] = 'item_objstr' + str(itemNumber)
            d2['itemStr'] = itemStr
            itemLines += hiddenItemStrField % d2
            itemLines += '</TD>\n'
            itemLines += '\n'
            
            itemLines += '</TR>\n'
            itemLines += '\n'
            itemNumber += 1


        itemLines += '\n</TABLE>\n'
        dict['itemLines'] = itemLines
        return pageStr1 % dict



    def process_form(self, form):
        """called by ChapterListFormHandle.py."""

        selLen = form.getfirst("selection_length", '')
        if selLen == '':
            ryw.give_bad_news('ChapterListFormHandle: ' +
                              'failed to get selection_length', logging.error)
            return (False, None)
        
        selLen = int(selLen)
        ryw.db_print2('process_form: selection length is: ' + str(selLen), 40)

        chapterList = {}

        for i in range(0,selLen):

            objField = 'item_objstr' + str(i)
            itemStr = form.getfirst(objField, '')
            if itemStr:
                ryw.db_print2('process_form: found objstr: ' + itemStr, 40)
            else:
                continue
        
            chapterField = 'chapter_number' + str(i)
            chapterStr = form.getfirst(chapterField, '')
            chapterStr = chapterStr.strip()
            if chapterStr:
                ryw.db_print2('process_form: found chapter: ' + itemStr, 40)
            else:
                continue
            chapterList[itemStr] = chapterStr
            ryw.db_print2('process_form: ' + itemStr + ' -> ' + chapterStr, 41)

        self.formEntries = chapterList
        return (True, chapterList)
    


    def compare_form_entries_against_meta(self):
        """compared the chapter numbers entered in a form
        against what's in the meta.  if it's the same as the
        default contained in meta, then we don't need to
        write that down in the local chapter list.
        called by ChapterListFormHandle.py."""

        formEntries = self.formEntries
        self.chapterList = copy.copy(formEntries)

        if self.chapterList == {}:
            return
        
        for objstr,chapterStr in formEntries.iteritems():

            #
            # if the form has nothing for this object, then skip it.
            #
            if not formEntries.has_key(objstr):
                continue
            else:
                ryw.db_print2('compare_form_entries_against_meta: ' +
                              'form entry says: ' + formEntries[objstr], 41)

            #
            # if the meta data somehow says it has nothing,
            # then there's no need to for me delete anything from the
            # form entry list.
            #
            if not self.chapterDict.has_key(objstr):
                ryw.db_print2('compare_form_entries_against_meta: ' +
                              'objstr not found in chapterDict: ' + objstr,
                              41)
                continue
            metaChapter = self.chapterDict[objstr][2]
            if metaChapter:
                ryw.db_print2('compare_form_entries_against_meta: ' +
                              'meta chapter is: ' + metaChapter, 41)
            else:
                continue
            
            #
            # both the form entry and the metadata says something.
            # so we should compare them to see if I should omit the form
            # entry in case they are the same thing.
            #
            if (formEntries[objstr] == metaChapter):
                ryw.db_print2('compare_form_entries_against_meta: ' +
                              'found to be same: ' + metaChapter, 41)
                del self.chapterList[objstr]
            else:
                ryw.db_print2('compare_form_entries_against_meta: ' +
                              'found to be different: ' + metaChapter, 41)
                continue
            
        ryw.db_print2('compare_form_entries_against_meta: ' +
                      'the list to be written is: ' +
                      repr(self.chapterList), 41)



    def write_file(self, fullFileName):
        """10/24/08, called by ChapterListFormHandle.py."""

        if self.chapterList == None or self.chapterList == {}:
            #
            # then we remove the chapter list file.
            #
            ryw.db_print_info_browser('ChapterList.write_file: ' + \
                                      'chapterList is empty.', 41)
                              
            if ryw.cleanup_path(fullFileName,
                                'ChapterList.write_file'):
                return True
                
            ryw.give_bad_news('ChapterList.write_file:' +
                              'failed to remove file', logging.error)
            return False

        try:
            su.pickdump(self.chapterList, fullFileName)
        except:
            ryw.give_bad_news('ChapterList.write_file: pickdump failed: ' +
                              fullFileName, logging.error)
            return False
                
        ryw.db_print_info_browser('ChapterList.write_file success: ' +
                                  fullFileName, 41)
        return True



    def read_file(self, fullFileName):
        """called by read_list_and_merge() below."""

        if not os.path.exists(fullFileName):
            self.chapterList = None
            return True

        try:
            self.chapterList = su.pickload(fullFileName)
        except:
            ryw.give_bad_news('ChapterList.read_file: pickload failed: ' +
                              fullFileName, logging.error)
            return False

        ryw.db_print2('ChapterList.read_file succes: ' + fullFileName, 41)
        ryw.db_print2('ChapterList.read_file: ' + repr(self.chapterList), 41)
        return True
        
                
            
    def read_list_and_merge(self, fullFileName):
        """10/24/08: called by ChapterListForm.py."""

        if not self.read_file(fullFileName):
            ryw.give_bad_news('read_list_and_merge: read_file failed: ' +
                              fullFileName, logging.error)
            return False

        if self.chapterList == None or self.chapterList == {}:
            return True

        for objstr,chapterStr in self.chapterList.iteritems():

            if not self.chapterDict.has_key(objstr):
                ryw.db_print_info_browser(
                    'read_list_and_merge: objstr in chapter ' +
                    'list but not in meta list: ' + objstr, 41)
                continue

            self.chapterDict[objstr][2] = chapterStr

        return True



    def patch_meta_list_with_chapters(self, metaList=None):
        """10/24/08: called by ShowQueue.go_through_list() when
        it's initiated by DisplaySelection.py.
        metaList is sent in from ShowQueue.go_through_list().
        it's otherwise None."""

        if not metaList:
            metaList = self.metaList

        if not metaList:
            ryw.give_bad_news('patch_meta_list_with_chapters: ' +
                              'unexpected empty metaList.', logging.critical)
            return

        for meta in metaList:
            objstr = meta['id'] + '#' + str(meta['version'])
            ryw.db_print2('patch_meta_list_with_chapters: objstr: ' + objstr,
                          41)

            if not self.chapterDict.has_key(objstr):
                continue

            chapter = self.chapterDict[objstr][2]
            if chapter:
                meta['chapter_number'] = chapter
                ryw.db_print2('patch_meta_list_with_chapters: ' +
                              'chapter patched: ' + chapter, 41)
        


    def re_sort_items(self):
        """10/24/08: called before displaying the chapter edit form.
        so that the edit form is sorted.
        called by make_form_string()"""

        self.patch_meta_list_with_chapters()
        self.metaList = ryw.sortmeta_chapter_number(self.metaList)

        itemList = []
        for meta in self.metaList:
            objID = meta['id']
            version = meta['version']
            objstr = objID + '#' + str(version)
            itemList.append(objstr)
            
        self.itemList = itemList
