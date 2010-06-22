#
# the process of generating translation.
#
# - for the current selection, in the browser, do "prepare for trans."
# - look at where the browser says the output php file is.
# - cd /u/rywang/Postmanet-2/misc/trans_hindi
#   cp /u/Postmanet/repository/Tmp-out/*9473 english_text.php
# - php trans_hindi.php
# - cp google_english2hindi.py /u/rywang/Postmanet-2/Common/
# - install-ubuntu (as the user named www-data)
#


import sys, os
import su
import pickle, cgi, cgitb, xmlrpclib, urllib
cgitb.enable()
import SearchFile, Search, Browse
import ryw,logging, ryw_view, ryw_meta
import ReverseLists
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import ShowQueue, DisplaySelection
import google_english2hindi



def open_output_text_file():
    """modeled after setting up temporary output file in rebuildSearchFile.py.
    """

    resourcesPath = os.path.join(RepositoryRoot, 'Resources.txt')
    try:
        resources = ryw.get_resources(resourcesPath)
        tmpOutDir = ryw.get_resource_str(resources, 'tmpout')
        if not tmpOutDir:
            ryw.give_bad_news('SelectTexts.py: failed to get tmpout resource.',
                              logging.error)
            return None
    except:
        ryw.give_bad_news('SelectTexts.py: failed to get resources.',
                          logging.error)
        return None

    dateTimeRand = ryw.date_time_rand()
    textfilePath = os.path.join(tmpOutDir, 'Texts2Trans' + dateTimeRand)
    ryw.give_news('PHP file is generated at: ', logging.info)
    ryw.give_news(textfilePath, logging.info)
    
    try:
        outf = open(textfilePath, 'w')
        outf.write('<?\n')
        outf.write('$trans_source = array(')
    except:
        ryw.give_bad_news('SelectTexts.py: unable to open output text file: '+
                          textfilePath, logging.error)
        return None

    return outf



def output_text(outputFile, meta, firstLine=False):
    """mirrors ryw_view.get_auto_hindi_translation_string()."""
    
    f = outputFile
    count = 0
    ryw.db_print_info_browser("\n", 89)
    
    for type in ['title', 'description']:
        if not meta.has_key(type):
            continue
        allText = meta[type]
        textList = ryw.split_content(allText)

        for text in textList:
            md5sum = ryw.md5sum(text)

            #
            # if it's already in the dictionary, don't bother.
            #
            autoDict = google_english2hindi.GOOGLE_AUTO_DICT
            if autoDict.has_key(md5sum):
                ryw.db_print_info_browser('already found in dictionary: ' +
                                          md5sum, 89)
                continue

            text = text.replace('"', '\\"')
            #text = text.replace("^M", "")
            outputStr = '"' + md5sum + '"' + ' => ' + '"' + text + '"'

            try:
                if not firstLine:
                    f.write(',')
                f.write('\n')

                f.write(outputStr)
                count += 1
                ryw.db_print2(outputStr, 89)
                firstLine = False
            except:
                ryw.give_bad_news('output_text: failed to write line: ' +
                                  outputStr, logging.error)
                return (False, count)

    return (True, count)



def close_output_file(outputFile):
    f = outputFile
    try:
        f.write('\n')
        f.write(');\n')
        #f.write('print_r($trans_source);\n')
        f.write('?>\n')
        f.close()
    except:
        ryw.give_bad_news('close_output_file: failed at the end of the file.',
                          logging.error)
        


def extract_texts(reqList, searchFile):
    """modeled after ShowQueue.go_through_list()."""

    metaList = ryw_meta.get_meta_list(reqList, searchFile)
    metaList = ryw.sortmeta_chapter_number(metaList)

    totalCount = 0
    outputFile = open_output_text_file()
    if outputFile == None:
        return False
    
    numMatches = len(metaList)
    if numMatches <= 0:
        ryw.give_news('SelectTexts: no object selected.<BR>', logging.error)
        success = False
    else:
        success = True
        firstLine = True
        for meta in metaList:
            success,count = output_text(outputFile, meta,
                                        firstLine = firstLine)
            totalCount += count
            if not success:
                break
            if count != 0:
                firstLine = False

    close_output_file(outputFile)
    searchFile.done()
    
    ryw.give_news(str(totalCount) + ' strings need to be translated.',
                  logging.info)
    return success



def main():
    """modeled after ShowQueue.py."""
    
    name = ShowQueue.init_log()
    ryw_view.print_header_logo()
    print '<TITLE>Prepare for Automated Hindi Translation</TITLE>'

    rfpath = os.path.join(RepositoryRoot, 'QUEUES', name)
    reqList = ShowQueue.read_list(rfpath)
    if not reqList:
        ryw.give_news('SelectText.py: no object selected.', logging.info)
        DisplaySelection.exit_now(0)

    success,searchFile,reverseLists = \
        ReverseLists.open_searchfile_reverselists('SelectTexts.main:')

    if not success:
        DisplaySelection.exit_now(0)

    extract_texts(reqList, searchFile)
        
    ryw.give_news('done.', logging.info)
    ryw_view.print_footer()
    searchFile.done()
    reverseLists.done()
    


if __name__ == '__main__':
    main()
