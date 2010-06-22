from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
import sys,os,subprocess,shutil,datetime,time,logging,operator
import dvoice.db.models
#from dvoice.db.models import Organization, Person, Item, KeyWord, Event
import dsh_django_config,dsh_django_utils,dsh_django_utils2
dsh_django_utils2.append_to_sys_path(
    dsh_django_config.lookup('DSH_VOICE_CODE_DIR'))
import dsh_utils,dsh_config,dsh_agi
from django.forms.fields import email_re



def table_header():
    """called by stats() below.  the header of sorted stats table.
    basically just a string constant."""

    response = ''
    response += '<TR>\n'
    response += '<TD><b><p align=center>rank</p></b></TD>\n'
    response += '<TD><b><p align=center>mug</p></b></TD>\n'
    response += '<TD><b><p align=left>who</p></b></TD>\n'

    #
    # all calls.
    #
    response += '<TD><p align=right><b><a href="/stats/calls" ' +\
                'title="all calls">calls</a></b></p></TD>\n'

    #
    # long recorded items.
    #
    response += '<TD><p align=right><b><a href="/stats/recorded" ' +\
                'title="long recorded items">recorded</a></b></p></TD>\n'

    #
    # total number of recorded items.
    #
    response += '<TD><p align=right><b><a href="/stats/items" ' + \
                'title="all items">items</a></b></p></TD>\n'

    #
    # calls made without recordings.
    # 
    response += '<TD><p align=right><b><a href="/stats/callsnorec" ' +\
                'title="calls made without recording">listen ' +\
                'only</a></b></p></TD>\n'

    #
    # starred items.
    #
    response += '<TD><p align=right><b><a href="/stats/starred" ' +\
                'title="starred items">starred</a></b></p></TD>\n'


    #
    # item rec. duration.
    #
    response += '<TD><p align=right><b><a href="/stats/recdur" ' +\
                'title="record duration">record duration (s)</a></b></p>' +\
                '</TD>\n'
    
    #
    # total call duration.
    #
    response += '<TD><p align=right><b><a href="/stats/calldur" ' +\
                'title="call duration">call duration (s)</a></b></p></TD>\n'
    
    response += '</TR>\n'

    return response



def person_tuple_list(person):
    """called by stats() below.
    makes a tuple for each person for sorting."""
    
    #
    # count of items longer than 10 seconds.
    #
    recThresh= dsh_django_config.lookup('RECORDED_THRESH')
    recCount = dvoice.db.models.Item.objects.filter(
        owner=person, rec_duration__gt=recThresh).count()

    #
    # count of total items.
    #
    itemCount = dvoice.db.models.Item.objects.filter(
        owner=person).count()

    #
    # count of calls without recording.
    # basically copied from dsh_django2.py
    #
    callsNoRec = dvoice.db.models.Event.objects.filter(
        owner=person,
        phone_number=person.phone_number,
        action='CALL',
        etype='INF').count()

    #
    # total number of calls is recorded items plus calls without recording.
    #
    callCount = itemCount + callsNoRec

    #
    # starred item count.
    #
    starCount = dvoice.db.models.Item.objects.filter(
        starred=True,owner=person).count()

    #
    # record duration.
    #
    recDur = 0
    callDur = 0
    items = dvoice.db.models.Item.objects.filter(owner=person)
    for item in items:
        recDur += item.rec_duration
        callDur += item.call_duration

    #
    # total call duration.
    #
    events = dvoice.db.models.Event.objects.filter(
        owner=person,
        phone_number=person.phone_number,
        action='CALL',
        etype='INF')
    for event in events:
        callDur += event.call_duration

    return (person, recCount, itemCount, callsNoRec, callCount, starCount,
            recDur, callDur)
    


def sort_key(sortBy):
    """called by stats() below.  which key in the tuple is sort key?
    corresponds to stats_person_tuple_list() above.
    """
    if not sortBy:
        sortBy = dsh_config.lookup('STATS_SORT_BY')
    if sortBy == 'recorded':
        sortKey = operator.itemgetter(1)
    elif sortBy == 'items':
        sortKey = operator.itemgetter(2)
    elif sortBy == 'callsnorec':
        sortKey = operator.itemgetter(3)
    elif sortBy == 'calls':
        sortKey = operator.itemgetter(4)
    elif sortBy == 'starred':
        sortKey = operator.itemgetter(5)
    elif sortBy == 'recdur':
        sortKey = operator.itemgetter(6)
    elif sortBy == 'calldur':
        sortKey = operator.itemgetter(7)
    else:
        return None
    return sortKey

    

def one_row(tuple, i, totals):
    """called by stats() below.
    prints one row of the stats table.
    accumulates the total as well.
    """

    response = ''
    person,recCount,itemCount,callsNoRec,calls,starCount,recDur,callDur = tuple
    totalCalls,totalRecorded,totalItems,totalListen,totalStars,\
        totalRecDur,totalCallDur = totals
    

    #
    # mugshot column
    #
    thumb = dsh_django_utils.thumbnail(person, person.mugshot)
    href = dsh_django_config.lookup('PERSON_DETAIL_URL') + str(person.id)
    mugLink = '<a href="%s">%s</a>' % (href, thumb)

    #
    # who column
    #
    name = person.__unicode__()
    href = dsh_django_config.lookup('PERSON_URL') + str(person.id)
    nameLink = '<a href="%s">%s</a>' % (href, name)

    org = person.organization
    orgName = org.alias
    href = dsh_django_config.lookup('ORG_URL') + str(org.id)
    orgLink = '<a href="%s">%s</a>' % (href, orgName)

    messagesIcon = person.person_item_link()

    whoLinks = nameLink + '<BR><BR>' + messagesIcon + '<BR><BR>' + orgLink

    #
    # all columns of one row.
    #
    response += '<TR>\n'
    response += '<TD><p align=center>%s</p></TD>\n' % (str(i),)
    response += '<TD>%s</TD>\n' % (mugLink,)
    response += '<TD>%s</TD>\n' % (whoLinks)

    #
    # total number of calls.
    #
    response += '<TD><p align=right>%s</p></TD>\n' % (str(calls),)
    totalCalls += calls

    #
    # long recorded items.
    # eg.:
    # /admin/db/item/?owner__id__exact=51&rec_duration__gt=10
    #
    href = '/admin/db/item/?rec_duration__gt=%s&owner__id__exact=%s' %\
           (dsh_django_config.lookup('RECORDED_THRESH'),
            str(person.id))
    recLink = '<a href="%s" title="long recorded items">%s</a>' %\
              (href, str(recCount))
    response += '<TD><p align=right>%s</p></TD>\n' % (recLink,)
    totalRecorded += recCount

    #
    # total count of items.
    # eg.:
    # /admin/db/item/?owner__id__exact=16
    #
    href = '/admin/db/item/?owner__id__exact='
    href += str(person.id)
    itemLink = '<a href="%s" title="all recorded items">%s</a>' %\
               (href, str(itemCount))
    response += '<TD><p align=right>%s</p></TD>\n' % (itemLink,)
    totalItems += itemCount

    #
    # calls without recording.
    # eg.:
    # /admin/db/event/?owner__id__exact=3&action__exact=CALL
    #
    href = '/admin/db/event/?action__exact=CALL&owner__id__exact='
    href += str(person.id)
    listenLink = '<a href="%s" title="listen without recording">%s</a>' %\
                 (href, str(callsNoRec))
    response += '<TD><p align=right>%s</p></TD>\n' % (listenLink,)
    totalListen += callsNoRec

    #
    # starred.
    # eg.:
    # /admin/db/item/?starred__exact=1&owner__id__exact=16
    #
    href = '/admin/db/item/?starred__exact=1&owner__id__exact='
    href += str(person.id)
    starLink = '<a href="%s" title="starred items">%s</a>' %\
               (href, str(starCount))
    response += '<TD><p align=right>%s</p></TD>\n' % (starLink,)
    totalStars += starCount

    #
    # record duration.
    #
    response += '<TD><p align=right>%s</p></TD>\n' % (str(recDur),)
    totalRecDur += recDur

    #
    # call duration.
    #
    response += '<TD><p align=right>%s</p></TD>\n' % (str(callDur),)
    totalCallDur += callDur

    response += '</TR>\n'

    totals = totalCalls,totalRecorded,totalItems,totalListen,totalStars,\
             totalRecDur,totalCallDur
    
    return (response,totals)



def total_row(totals):
    """called by stats() below.
    prints the row of total sums.
    """
    totalCalls,totalRecorded,totalItems,totalListen,totalStars,\
        totalRecDur,totalCallDur= totals
    space = '&nbsp;'
    #
    # the first three columns are empty: rank, mug, who.
    #
    response = '<TR><TD><b>totals</b></TD><TD>%s</TD><TD>%s</TD>' %\
               (space,space)

    for total in totals:
        response += '<TD><p align=right><b>%s</b></p></TD>\n' % (str(total),)

    response += '</TR>'
    return response



def stats_calculate(sortBy=None, logAction='STT2', textLog=False):
    """called by views.stats().
    possible values of sortedBy are:
    'recorded'
    'items'
    'callsnorec'
    'calls'
    'starred'
    'recdur'
    'calldur'
    returns (success,response,totals)
    when triggered from daily cron job in dsh_stats_log,
    logAction=='STT1' and textLog=True.
    otherwise, the default value here.
    """

    #
    # fill the tuple list of people and their counts.
    #
    people = dvoice.db.models.Person.objects.all()
    tupleList = []
    for person in people:
        tuple = person_tuple_list(person)
        tupleList.append(tuple)
        

    #
    # what key do we sort it by? and sort it!
    #
    if not sortBy:
        sortBy = dsh_config.lookup('STATS_SORT_BY')

    sortKey = sort_key(sortBy)
    if not sortKey:
        resp = dsh_utils.red_error_break_msg('invalid sort field: ' +
                                             repr(sortBy))
        return (False, resp, None)
        
    sortedTupleList = sorted(tupleList, key=sortKey, reverse=True)


    #
    # just prints a message at the beginning of the page.
    #
    sortStr = sortBy
    if sortBy == 'callsnorec':
        sortStr = 'calls without recording'
    elif sortBy == 'recdur':
        sortStr = 'record duration'
    elif sortBy == 'calldur':
        sortStr = 'call duration'

    response = ''
    response += dsh_utils.black_break_msg(
        'click the column headings to sort by different criteria.')
    response += dsh_utils.black_break_msg(
        'currently sorted by <b><i>%s</i></b>:' % (sortStr,))
    response += '<BR>'


    #
    # table header.
    #
    i = 1
    response += '<TABLE border=1>\n'
    response += table_header()

    #
    # to be replaced.
    #
    response += '<!-- total row -->'

    #
    # the body of the table.
    #
    totals = (0, 0, 0, 0, 0, 0, 0)
    for tuple in sortedTupleList:
        oneRow,totals = one_row(tuple, i, totals)
        response += oneRow
        i += 1

    totalRow = total_row(totals)
    response += totalRow
    response += table_header()
    
    response += '</TABLE>'

    response = response.replace('<!-- total row -->', totalRow)

    log_event(totals, logAction=logAction, textLog=textLog)
    return (True, response, totals)



def log_event(totals, logAction='STT2', textLog=False):
    """
    puts the stats in the event table.
    """

    message = ('calls: %s, recorded: %s, items: %s, callsnorec: %s, ' +\
               'starred: %s, recdur: %s, calldur: %s') % \
               (str(totals[0]), str(totals[1]), str(totals[2]), str(totals[3]),
                str(totals[4]), str(totals[5]), str(totals[6]))
    dsh_agi.report_event(message, action=logAction)
    if textLog:
        dsh_utils.give_news(message, logging.info)
    


def stats(sortBy=None):
    """called by views.stats()."""
    
    success,response,totals = stats_calculate(sortBy=sortBy)
    return response
