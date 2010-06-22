import ProcessDownloadReq
import cgi, cgitb, os, sys
cgitb.enable()
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import ShowQueue, DisplaySelection
import ryw_view, Search, ryw, logging



def get_curr_sel(name):
    queueName = os.path.join(RepositoryRoot,'QUEUES',name)
    currSel = ProcessDownloadReq.get_reqs(queueName)
    return (currSel, queueName)



def get_search_result():
    form = cgi.FieldStorage()
    selName = form.getfirst('sel', '')
    if not selName:
        ryw.give_bad_news(
            'AddSearchAll: failed to find current search result: ',
            logging.error)
        return None

    tmpSearchResultDir = Search.decide_search_result_dir()
    if not tmpSearchResultDir:
        ryw.give_bad_news('AddSearchAll: ' +
                          'decide_search_result_dir failed.',
                          logging.error)
        return None

    searchFileName = os.path.join(tmpSearchResultDir, selName)
    searchSel = ProcessDownloadReq.get_reqs(searchFileName)
    
    return searchSel



def union_and_write(currSel, searchSel, queueName):

    unionResults = currSel | searchSel

    #
    # copied from ProcessDownloadReq.py
    #
    success,tmppath,bakpath = ProcessDownloadReq.write_reqs(
        queueName, unionResults)
    ProcessDownloadReq.cleanup(tmppath, bakpath)

    if success:
        numResults = len(searchSel)
        ryw.give_news(str(numResults) +
                      ' objects added to the chosen selection.',
                      logging.info)
    else:
        ryw.give_bad_news('union_and_write: failed.', logging.error)
    


def main():
    name = ShowQueue.init_log()
    ryw_view.print_header_logo()
    
    currSel,queueName = get_curr_sel(name)

    searchSel = get_search_result()
    if not searchSel:
        ryw.give_bad_news(
            'AddSearchAll: failed to load current search result.',
            logging.error)
        DisplaySelection.exit_now(1)

    union_and_write(currSel, searchSel, queueName)
    DisplaySelection.exit_now(0)


    
if __name__ == '__main__':
    main()

