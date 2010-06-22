from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import dv2
from dv2.views import hello, current_datetime, hours_ahead, display_meta
from dv2.db import views as db_views
#from dv2.contact import views as contact_views

urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    #
    # the root page has a javascript to redirect.
    #
    (r'^$', dv2.views.entrance),

    #
    # dump selected or all objects to a dump file in Python syntax.
    #
    (r'^dump/$', dv2.views.dump),
    (r'^dumpall/$', dv2.views.dump_all),

    #
    # permission denied and asks the user to log on as root.
    # 
    (r'^beroot/$', dv2.views.be_root),

    #
    # de-select everything.
    #
    (r'^deselect/$', dv2.views.deselect_all),

    #
    # show selected objects, group by table types, and show selected counts.
    #
    (r'^showselect/$', dv2.views.show_selected),

    #
    # called by javascript to select one object.
    # the stuff in the 2nd parenthesis is the dsh_uid.
    #
    (r'^select/(item)/(.*)/$', dv2.views.select_one),
    (r'^select/(person)/(.*)/$', dv2.views.select_one),
    (r'^select/(organization)/(.*)/$', dv2.views.select_one),
    (r'^select/(keyword)/(.*)/$', dv2.views.select_one),
    (r'^select/(event)/(.*)/$', dv2.views.select_one),

    #
    # add/del this key word to/from the selection
    #
    (r'^keywordadd/(.*)$', dv2.views.keyword_add),
    (r'^keyworddel/(.*)$', dv2.views.keyword_del),

    #
    # displays a form for replying
    #
    (r'^reply/(.*)$', dv2.views.reply),

    #
    # processes a reply form submit.
    #
    (r'^replysubmit/$', dv2.views.reply_submit),

    #
    # frames the red5 record page.
    # frames the red5 play page.
    #
    (r'^record/$', dv2.views.red5_record),
    (r'^preview/$', dv2.views.red5_play),
    (r'^playscratch/$', dv2.views.red5_play),

    #
    # clean up the red5 stream directory.
    #
    (r'^clearstreams/$', dv2.views.red5_clear),
                       
    #
    # displays a form for saving from red5.
    #
    (r'^save/$', dv2.views.red5_save),

    #
    # processes a reply form submit.
    #
    (r'^savesubmit/$', dv2.views.save_submit),

    #
    # lookup a phone number.  called by dsh_django_utils.display_phone_link()
    #
    (r'^lookupphone/(.*)$', dv2.views.lookup_phone_number),

    #
    # schedule auto-dialed outgoing calls.
    #
    (r'^schedulecalls/$', dv2.views.schedule_outgoing_calls),

    #
    # list of auto-scheduled outgoing calls.
    #
    (r'^scheduled/$', dv2.views.schedule_list),

    #
    # for deleting one dot call file.
    #
    (r'^scheduledel/(.*)$', dv2.views.schedule_del),

    #
    # for deleting all dot call files.
    #
    (r'^scheduledelall/$', dv2.views.schedule_del_all),

    #
    # combined delete all and reschedule.
    #
    (r'^reschedule/$', dv2.views.reschedule),

    #
    # combined delete all and reschedule.
    #
    (r'^scheduledslots/$', dv2.views.scheduled_slots),

    #
    # for confirming emailing the selection.
    #
    (r'^emailconfirm/$', dv2.views.email_confirm),

    #
    # responds to /emailconfirm/
    #
    (r'^email/$', dv2.views.email_selection),

    #
    # list all the unknown people
    #
    (r'^unknown/$', dv2.views.unknown_list),

    #
    # list all phone numbers
    #
    (r'^phonelist/$', dv2.views.phone_number_list),

    #
    # add/del star to/from selected objects.
    #
    (r'^star/$', dv2.views.star_selection),
    (r'^starless/$', dv2.views.destar_selection),

    #
    # dump all persons and organizations
    #
    (r'^dumppersons/$', dv2.views.dump_all_persons),
                       
    #
    # schedule auto-dialed call for one person.
    #
    (r'^schedulecallee/(.*)$', dv2.views.schedule_one_callee),
                       
    #
    # list of graphical tutorials.
    #
    (r'^tutorials/$', dv2.views.tutorials),

    #
    # global auto-dial options
    #
    (r'^autodialdisable/$', dv2.views.auto_dial_disable),
    (r'^autodialenable/$', dv2.views.auto_dial_enable),
    (r'^autodialstatus/$', dv2.views.auto_dial_status),

    #
    # check spoken name voices.
    #
    (r'^checkspokennames/$', dv2.views.check_spoken_names),

    #
    # statistics.  the argument is the "sortBy" criteria.
    #
    (r'^stats/(.*)$', dv2.views.stats),

    #
    # added starred items to the selection
    #
    (r'^selectstarred/$', dv2.views.select_starred),

    #
    # called by javascript to select one object.
    # the stuff in the 2nd parenthesis is the dsh_uid.
    #
    (r'^dialnow/(.*)/$', dv2.views.dial_now),
    (r'^dialnowconfirm/(.*)/$', dv2.views.dial_now_confirm),
                       
    #
    # pointed to by "people who have heard this" icon on Item page.
    #
    (r'^heard/(.*)/$', dv2.views.heard),

    #
    # activate/deactivate selected objects.
    #
    (r'^selectactivate/$', dv2.views.selection_activate),
    (r'^selectdeactivate/$', dv2.views.selection_deactivate),
    (r'^selectshare/$', dv2.views.selection_share),
    (r'^selectunshare/$', dv2.views.selection_unshare),

    #
    # 10/03/06:
    # modeled after ^reply/dsh_uid
    # displays a page for confirming replying.
    #
    (r'^replyupload/(.*)$', dv2.views.reply_upload),
    (r'^replyuploadsubmit/(.*)$', dv2.views.reply_upload_submit),

    #
    # 10/03/13:
    # 
    (r'^demographics/(.*)$', dv2.views.demographics),

    (r'^keywordsel/(.*)$', dv2.views.keyword_select),
    (r'^keyworddesel/(.*)$', dv2.views.keyword_deselect),
                       
    #
    # 10/03/22:
    # stuff having to do with the current dial set.
    #                       
    (r'^setcurrentdialsel/$', dv2.views.set_current_dial_sel),
    (r'^clearcurrentdialsel/$', dv2.views.clear_current_dial_sel),
    (r'^selectcurrentdial/$', dv2.views.select_current_dial_set),
    (r'^deselectcurrentdial/$', dv2.views.deselect_current_dial_set),
    (r'^clearcurrentdial/$', dv2.views.clear_current_dial_set),

    #
    # 10/03/22:
    # stuff having to do with person key words.
    #                       
    (r'^personkeywordsel/(.*)$', dv2.views.select_keyed_persons),
    (r'^personkeyworddesel/(.*)$', dv2.views.deselect_keyed_persons),
    (r'^personkeywordadd/(.*)$', dv2.views.add_person_keyword),
    (r'^personkeyworddel/(.*)$', dv2.views.del_person_keyword),
                       
    #
    # 10/03/25:
    # stuff having to do with un-answering answered messages.
    # first argument is dsh_uid of the person.
    # second is offset of how many items to skip, like 0, or 10.
    #
    (r'^personanswered/(.*)/(\d+)$', dv2.views.person_answered),
    (r'^unanswer/(.*)$', dv2.views.unanswer),

    #
    # 10/03/28:
    # displays the entire history of a conversation.
    #
    (r'^conversationhistory/(.*)$', dv2.views.conversation_history),
                       
    #
    # 10/04/01:
    # stuff having to do with un-hearing heard messages.
    # first argument is dsh_uid of the person.
    # second is offset of how many items to skip, like 0, or 10.
    #
    (r'^personheard/(.*)/(\d+)$', dv2.views.person_heard),
    (r'^unhear/(.*)$', dv2.views.unhear),

    #
    # 10/04/02:
    # questions unanswered
    # answers unheard
    #
    (r'^questionsunanswered/(\d+)$', dv2.views.questions_unanswered),
    (r'^answersunheard/(\d+)$', dv2.views.answers_unheard),
                       
    #
    # 10/04/09:
    # send a demo reply to the most recent caller now.
    #
    (r'^senddemoreply/$', dv2.views.send_demo_reply_now),
    (r'^senddemoreplyconfirmed/(.*)$', dv2.views.send_demo_reply_confirmed),

    #
    # the stuff below was by Raghuvansh.
    # not used.
    #
    (r'^hello/$', hello),
    (r'^time/$', current_datetime),
    (r'^time/plus/(\d{1,2})/$', hours_ahead),
    (r'^meta/$', display_meta),
    #(r'^search-form/$', books_views.search_form),
    #(r'^search/$', db_views.search),
    #(r'^contact/$', contact_views.contact),
    # ...
)
