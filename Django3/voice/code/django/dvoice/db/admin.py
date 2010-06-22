from django.contrib import admin
from dvoice.db.models import Organization, Person, Item, KeyWord, Event
from dvoice.db.models import ZObject01
from dvoice import dsh_django_utils
from dvoice import dsh_django_request



unused_fields_spec = ('unused fields',
                      {'fields': ['u01', 'u02', 'u03', 'u04', 'u05', 'u06',
                                  'u07', 'u08', 'u09', 'u10', 'u11', 'u12',
                                  'u13', 'u14', 'u15', 'u16', 'u17', 'u18',
                                  'u19', 'u20', 'u21', 'u22', 'u23', 'u24',
                                  'u25', 'u26', 'u27', 'u28'],
                       'classes': ['collapse']})

admin_fields_spec = (None, {'fields': ['u17']})



class StrictPermission(admin.ModelAdmin):
    """this is a super-class used by the real admin classes below.
    tries to deny permission to the non-root user for doing any
    modifications."""


    #
    # this doesn't quite work.  it ends up disabling everything.
    # 
    #def has_change_permission(self, request, obj=None):
    #    return False


    def has_add_permission(self, request):
        return not dsh_django_request.deny_it(request)


    def has_delete_permission(self, request, obj=None):
        return not dsh_django_request.deny_it(request)



class PersonAdmin(StrictPermission):
    list_display = ('thumbnail',
                    'first_name', 'last_name',
                    'hide_phone_number',
                    'org_link',
                    'ptype',
                    'person_key_link',
                    'spoken_name_display_field',
                    'meta_display',
                    'latest_event',
                    'modify_datetime',
                    'description', 
                    )
    list_display_links = ('thumbnail',)
    search_fields = ('first_name', 'last_name', 'phone_number',
                     'description', 'comments',)
    list_filter = ['organization', 'ptype',
                   'phone_std',
                   'phone_landline',
                   'timed_broadcast',
                   'current_dial',
                   'auto_dial_disabled',
                   'person_key_words',
                   'u17']
    fieldsets = [
        (None, {'fields': ['first_name', 'last_name',
                           'phone_number',
                           'phone_owner', 'phone_std',
                           'phone_landline',
                           'current_dial',
                           'mugshot',
                           'spoken_name',
                           'organization', 'ptype', 'gender',
                           'email',
                           'url', 'modify_datetime']}),
        (None, {'fields': ['description', 'comments', 'person_key_words',]}),
        ('auto-dial times', {'fields': ['timed1', 'timed1_type',
                                        'timed_broadcast',
                                        'timed2', 'timed3',
                                        'auto_dial_disabled'],
                             'classes': ['collapse']}),
        #unused_fields_spec,
        admin_fields_spec,
        ]
    filter_horizontal = ('person_key_words',)
    ordering = ('organization', )


    def formfield_for_dbfield(self, dbField, **kwargs):
        """this displays the mugshot field on the object edit page."""
        return dsh_django_utils.displayEditImageField2(
            self, dbField, kwargs, super(PersonAdmin, self),
            'mugshot', 'image', 'spoken_name', 'mp3')



class OrganizationAdmin(StrictPermission):
    list_display = ('thumbnail', 'name', 'alias', 'city_dist',
                    'org_key_link',
                    'spoken_name_display_field',
                    'meta_display',
                    'modify_datetime', 'description', ) 
    list_display_links = ('thumbnail',)
    list_filter = ['org_key_word', 'u17']
    search_fields = ('name', 'alias', 'phone_number', 'address', 'city_dist',
                     'state_province', 'country', 'description', 'comments')
    fieldsets = [
        (None, {'fields': ['name', 'alias', 'picture',
                           'spoken_name',
                           'org_key_word',
                           'language',
                           'modify_datetime']}),
        (None, {'fields': ['description', 'comments',]}),
        ('contact', {'fields': ['phone_number', 'address', 'city_dist',
                                'state_province', 'country', 'pin',
                                'url'],
                     'classes': ['collapse']}),         
        #unused_fields_spec,
        admin_fields_spec,
        ]
    ordering = ('alias',)


    def formfield_for_dbfield(self, dbField, **kwargs):
        """this displays the mugshot field on the object edit page."""
        return dsh_django_utils.displayEditImageField2(
            self, dbField, kwargs, super(OrganizationAdmin, self),
            'picture', 'image', 'spoken_name', 'mp3')



class KeyWordAdmin(StrictPermission):
    list_display = ('key_word', 'meta_display', 'description', )
    search_fields = ('key_word', 'description',)
    list_filter = ['org_key', 'person_key', 'u17']
    fieldsets = [
        (None, {'fields': ['key_word', 'description', 'org_key',
                           'person_key']}),
        #unused_fields_spec,
        admin_fields_spec,
        ]
    ordering = ('key_word',)



class EventAdmin(StrictPermission):
    list_display = ('modify_datetime',
                    'etype', 'action', 'owner_link',
                    'org_link',
                    'phone_number',
                    'description',
                    'call_duration', 'rec_duration',
                    'debug_tag',
                    'meta_display',
                    'dsh_uid_link',
                    'session_id_link',
                    )
    search_fields = ('description', 'dsh_uid_concerned', 'session',
                     'phone_number')
    list_filter = ['modify_datetime', 'etype', 'action', 'u17', 'owner',
                   'debug_tag', ]
    date_hiearchy = 'modify_datetime'
    fieldsets = [
        (None, {'fields': ['etype', 'action', 'owner', 'description',
                           'call_duration', 'rec_duration',
                           'phone_number',
                           'dsh_uid_concerned',
                           'modify_datetime',
                           'session']}),
        #unused_fields_spec,
        admin_fields_spec,
        ]
    ordering = ('-modify_datetime',)



class ItemAdmin(StrictPermission):
    list_display = ('thumbnail',
                    'item_url',
                    'owner_link_plus_phone',
                    'org_link',
                    'meta_display',
                    'modify_datetime', 
                    'get_key_words',
                    'description',
                    )
    list_display_links = ('thumbnail',)
    search_fields = ('description',)
    list_filter = ['modify_datetime', 'starred', 'peer_shared', 'u17',
                   'itype', 'active', 'dummy', 'key_words',
                   'owner', ]
    # these two fields removed from list filters: 'intended_audience', 'i05'
    
    date_hierarchy = 'modify_datetime'
    fieldsets = [
        (None, {'fields': ['file', 'owner', 'itype', 'active', 'starred',
                           'peer_shared', 
                           'play_once',
                           'dummy',
                           'call_duration', 'rec_duration',
                           'description',]}),
        (None, {'fields': ['key_words',
                           'followup_to',
                           'intended_audience',
                           'i05',
                           'discreet',
                           'modify_datetime']}),
        #unused_fields_spec,
        admin_fields_spec,
        ]
    filter_horizontal = ('key_words', 'intended_audience')
    ordering = ('-modify_datetime', 'owner',)
    raw_id_fields = ('followup_to', 'i05')


    def formfield_for_dbfield(self, dbField, **kwargs):
        """this displays the mp3 player widget on the object edit page."""
        return dsh_django_utils.displayEditImageField(
            self, dbField, kwargs, 'file',
            super(ItemAdmin, self), widgetType='mp3')



#
# ZObject01: global database config.
#
class DbConfigAdmin(StrictPermission):
    list_display = ('name', 'auto_dial_disable',
                    'reschedule_wipe_disable',
                    'local_land_line_prefix',
                    'outgoing_channel',
                    'zoiper_number',
                    'asterisk_context',
                    'asterisk_extension',
                    'database_name',
                    'port',
                    'scratch_phone_number1')
    fieldsets = [
        (None, {'fields': ['auto_dial_disable',
                           'reschedule_wipe_disable',
                           'local_land_line_prefix',
                           'outgoing_channel',
                           'zoiper_number',
                           'asterisk_context',
                           'asterisk_extension',
                           'database_name',
                           'port',
                           'scratch_phone_number1']}),
        ]



admin.site.register(Person, PersonAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(KeyWord, KeyWordAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(ZObject01, DbConfigAdmin)
