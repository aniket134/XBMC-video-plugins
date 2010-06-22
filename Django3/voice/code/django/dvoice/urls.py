from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import dvoice
from dvoice.views import hello, current_datetime, hours_ahead, display_meta
from dvoice.db import views as db_views
#from dvoice.contact import views as contact_views

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
    (r'^$', dvoice.views.entrance),

    #
    # dump selected or all objects to a dump file in Python syntax.
    #
    (r'^dump/$', dvoice.views.dump),
    (r'^dumpall/$', dvoice.views.dump_all),

    #
    # permission denied and asks the user to log on as root.
    # 
    (r'^beroot/$', dvoice.views.be_root),

    #
    # de-select everything.
    #
    (r'^deselect/$', dvoice.views.deselect_all),

    #
    # show selected objects, group by table types, and show selected counts.
    #
    (r'^showselect/$', dvoice.views.show_selected),

    #
    # called by javascript to select one object.
    # the stuff in the 2nd parenthesis is the dsh_uid.
    #
    (r'^select/(item)/(.*)/$', dvoice.views.select_one),
    (r'^select/(person)/(.*)/$', dvoice.views.select_one),
    (r'^select/(organization)/(.*)/$', dvoice.views.select_one),
    (r'^select/(keyword)/(.*)/$', dvoice.views.select_one),
    (r'^select/(event)/(.*)/$', dvoice.views.select_one),

    #
    # add/del this key word to/from the selection
    #
    (r'^keywordadd/(.*)$', dvoice.views.keyword_add),
    (r'^keyworddel/(.*)$', dvoice.views.keyword_del),

    #
    # displays a form for replying
    #
    (r'^reply/(.*)$', dvoice.views.reply),

    #
    # processes a reply form submit.
    #
    (r'^replysubmit/$', dvoice.views.reply_submit),

    #
    # frames the red5 record page.
    # frames the red5 play page.
    #
    (r'^record/$', dvoice.views.red5_record),
    (r'^preview/$', dvoice.views.red5_play),
    (r'^playscratch/$', dvoice.views.red5_play),

    #
    # clean up the red5 stream directory.
    #
    (r'^clearstreams/$', dvoice.views.red5_clear),
                       
    #
    # displays a form for saving from red5.
    #
    (r'^save/$', dvoice.views.red5_save),

    #
    # processes a reply form submit.
    #
    (r'^savesubmit/$', dvoice.views.save_submit),

    #
    # lookup a phone number.  called by dsh_django_utils.display_phone_link()
    #
    (r'^lookupphone/(.*)$', dvoice.views.lookup_phone_number),

    #
    # schedule auto-dialed outgoing calls.
    #
    (r'^schedulecalls/$', dvoice.views.schedule_outgoing_calls),

    #
    # list of auto-scheduled outgoing calls.
    #
    (r'^scheduled/$', dvoice.views.schedule_list),

    #
    # for deleting one dot call file.
    #
    (r'^scheduledel/(.*)$', dvoice.views.schedule_del),

    #
    # for deleting all dot call files.
    #
    (r'^scheduledelall/$', dvoice.views.schedule_del_all),

    #
    # combined delete all and reschedule.
    #
    (r'^reschedule/$', dvoice.views.reschedule),

    #
    # combined delete all and reschedule.
    #
    (r'^scheduledslots/$', dvoice.views.scheduled_slots),

    #
    # for confirming emailing the selection.
    #
    (r'^emailconfirm/$', dvoice.views.email_confirm),

    #
    # responds to /emailconfirm/
    #
    (r'^email/$', dvoice.views.email_selection),

    #
    # list all the unknown people
    #
    (r'^unknown/$', dvoice.views.unknown_list),

    #
    # list all phone numbers
    #
    (r'^phonelist/$', dvoice.views.phone_number_list),

    #
    # add/del star to/from selected objects.
    #
    (r'^star/$', dvoice.views.star_selection),
    (r'^starless/$', dvoice.views.destar_selection),

    #
    # dump all persons and organizations
    #
    (r'^dumppersons/$', dvoice.views.dump_all_persons),
                       
    #
    # schedule auto-dialed call for one person.
    #
    (r'^schedulecallee/(.*)$', dvoice.views.schedule_one_callee),
                       
    #
    # list of graphical tutorials.
    #
    (r'^tutorials/$', dvoice.views.tutorials),

    #
    # global auto-dial options
    #
    (r'^autodialdisable/$', dvoice.views.auto_dial_disable),
    (r'^autodialenable/$', dvoice.views.auto_dial_enable),
    (r'^autodialstatus/$', dvoice.views.auto_dial_status),

    #
    # check spoken name voices.
    #
    (r'^checkspokennames/$', dvoice.views.check_spoken_names),

    #
    # statistics.  the argument is the "sortBy" criteria.
    #
    (r'^stats/(.*)$', dvoice.views.stats),

    #
    # added starred items to the selection
    #
    (r'^selectstarred/$', dvoice.views.select_starred),

    #
    # called by javascript to select one object.
    # the stuff in the 2nd parenthesis is the dsh_uid.
    #
    (r'^dialnow/(.*)/$', dvoice.views.dial_now),
    (r'^dialnowconfirm/(.*)/$', dvoice.views.dial_now_confirm),
                       
    #
    # pointed to by "people who have heard this" icon on Item page.
    #
    (r'^heard/(.*)/$', dvoice.views.heard),

    #
    # activate/deactivate/share/unshare selected objects.
    #
    (r'^selectactivate/$', dvoice.views.selection_activate),
    (r'^selectdeactivate/$', dvoice.views.selection_deactivate),
    (r'^selectshare/$', dvoice.views.selection_share),
    (r'^selectunshare/$', dvoice.views.selection_unshare),

    #
    # 10/03/06:
    # modeled after ^reply/dsh_uid
    # displays a page for confirming replying.
    #
    (r'^replyupload/(.*)$', dvoice.views.reply_upload),
    (r'^replyuploadsubmit/(.*)$', dvoice.views.reply_upload_submit),

    #
    # 10/03/13:
    #
    (r'^keywordsel/(.*)$', dvoice.views.keyword_select),
    (r'^keyworddesel/(.*)$', dvoice.views.keyword_deselect),
                       
    #
    # 10/03/22:
    # stuff having to do with the current dial set.
    #                       
    (r'^setcurrentdialsel/$', dvoice.views.set_current_dial_sel),
    (r'^clearcurrentdialsel/$', dvoice.views.clear_current_dial_sel),
    (r'^selectcurrentdial/$', dvoice.views.select_current_dial_set),
    (r'^deselectcurrentdial/$', dvoice.views.deselect_current_dial_set),
    (r'^clearcurrentdial/$', dvoice.views.clear_current_dial_set),

    #
    # 10/03/22:
    # stuff having to do with person key words.
    #                       
    (r'^personkeywordsel/(.*)$', dvoice.views.select_keyed_persons),
    (r'^personkeyworddesel/(.*)$', dvoice.views.deselect_keyed_persons),
    (r'^personkeywordadd/(.*)$', dvoice.views.add_person_keyword),
    (r'^personkeyworddel/(.*)$', dvoice.views.del_person_keyword),
                       
    #
    # 10/04/01:
    # stuff having to do with un-hearing heard messages.
    # first argument is dsh_uid of the person.
    # second is offset of how many items to skip, like 0, or 10.
    #
    (r'^personheard/(.*)/(.*)$', dvoice.views.person_heard),
    (r'^unhear/(.*)$', dvoice.views.unhear),



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
