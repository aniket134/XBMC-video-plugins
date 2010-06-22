import sys,datetime,os,os.path,time
from django.db import models
from dv2 import dsh_django_utils,dsh_django_config,dsh_django_utils2
from dv2 import dsh_db_config
dsh_django_utils2.append_to_sys_path(
    dsh_django_config.lookup('DSH_VOICE_CODE_DIR'))
import dsh_utils,dsh_config,dsh_agi
from django.utils.encoding import smart_str, smart_unicode
import dsh_common_db,dsh_common_config
import django.core



def assign_dsh_uid():
    """each object is given a 20-digit ID"""
    #return dsh_utils.date_time_rand3()
    #return dsh_utils.date_time_rand()
    return dsh_common_db.make_dsh_uid()



def dsh_uid_length():
    """called by dsh_django_utils.auto_schedule_list()."""
    return len(assign_dsh_uid())



def assign_current_datetime():
    """default date time set to now."""
    return datetime.datetime.now()



#
# parent class of the different types of real models later.
#
class DshObject(models.Model):
    dsh_uid = models.CharField(max_length=64,
                               default=assign_dsh_uid,
                               editable=False,
                               verbose_name='unique dsh id')

    #
    # add_datetime: creation time.
    # save_datetime: when the object is modified and saved again.
    # they are automatically populated.
    # not editable.
    #
    add_datetime = models.DateTimeField(auto_now_add=True,
                                        verbose_name='when added')
    save_datetime = models.DateTimeField(auto_now=True,
                                         verbose_name='when changed')

    #
    # this one is editable.
    # if it's blank, it's set to save_datetime.
    # it should never be null.
    # this allows us to fudge the date.
    #
    modify_datetime = models.DateTimeField(verbose_name='when',
                                           default=assign_current_datetime,
                                           null=True,
                                           blank=True)


    description = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    discreet = models.BooleanField(default=False, blank=True, null=True)

    #
    # this one is used now.  for denoting selection.
    #
    u17 = models.BooleanField(default=False, blank=True, null=True,
                              verbose_name='selected')
    
    #
    # unused extra fields.
    #
    u01 = models.CharField(max_length=20, blank=True)
    u02 = models.CharField(max_length=20, blank=True)
    u03 = models.CharField(max_length=20, blank=True)
    u04 = models.CharField(max_length=20, blank=True)

    u05 = models.CharField(max_length=80, blank=True)
    u06 = models.CharField(max_length=80, blank=True)
    u07 = models.CharField(max_length=80, blank=True)
    u08 = models.CharField(max_length=80, blank=True)

    u09 = models.TextField(blank=True)
    u10 = models.TextField(blank=True)
    u11 = models.TextField(blank=True)
    u12 = models.TextField(blank=True)

    u13 = models.IntegerField(default=0, blank=True, null=True)
    u14 = models.IntegerField(default=0, blank=True, null=True)
    u15 = models.IntegerField(default=0, blank=True, null=True)
    u16 = models.IntegerField(default=0, blank=True, null=True)

    u18 = models.BooleanField(default=False, blank=True, null=True)
    u19 = models.BooleanField(default=False, blank=True, null=True)
    u20 = models.BooleanField(default=False, blank=True, null=True)

    u21 = models.BooleanField(default=False,
                              null=True,
                              blank=True)
    u22 = models.BooleanField(default=False,
                              null=True,
                              blank=True)
    u23 = models.BooleanField(default=False,
                              null=True,
                              blank=True)
    u24 = models.BooleanField(default=False,
                              null=True,
                              blank=True)
    
    u25 = models.DateTimeField(verbose_name='when',
                               default=assign_current_datetime,
                               null=True,
                               blank=True)
    u26 = models.DateTimeField(verbose_name='when',
                               default=assign_current_datetime,
                               null=True,
                               blank=True)
    u27 = models.DateTimeField(verbose_name='when',
                               default=assign_current_datetime,
                               null=True,
                               blank=True)
    u28 = models.DateTimeField(verbose_name='when',
                               default=assign_current_datetime,
                               null=True,
                               blank=True)


    def selected_icon(self, whatKind=None):
        if not whatKind:
            return 'Error!'
        spaces = dsh_django_config.lookup('ICON_SPACES')
        if self.u17:
            return dsh_django_config.lookup('SELECTED_ICON') + spaces
        selectBoxIcon = dsh_django_config.lookup('SELECT_BOX_ICON')
        selectIcon = """<img src=%s border=0 title="select this"
width=11 height=11
onmouseover="this.style.cursor='pointer';"
onClick="select_obj('%s', '%s',this)">
""" % (selectBoxIcon, whatKind, self.dsh_uid)
        return selectIcon
    selected_icon.short_description = 'sel.'
    selected_icon.allow_tags = True


    def save(self):
        if self.modify_datetime == None:
            self.modify_datetime = self.save_datetime
        if self.modify_datetime == None:
            self.modify_datetime = self.add_datetime
        if self.modify_datetime == None:
            self.modify_datetime = datetime.datetime.now()
        super(DshObject, self).save()

        
    class Meta:
        abstract = True
    


#
# taken from the unused tables.  for global database config.
#
class ZObject01(DshObject):
    name = models.CharField(max_length=80,unique=True,
                            default='global config options')
    
    auto_dial_disable = models.BooleanField(default=False,
                                            null=True,
                                            blank=True)

    scratch_phone_number1 = models.CharField(
        max_length=80, blank=True,
        default='', null=True,
        verbose_name='scratch phone number')
    

    #
    # 10/01/19: stash the dsh_uid of the recently saved item.
    # for the purpose of de-activating earlier active broadcast messages.
    # this has to be done here because I couldn't get
    # many-to-many relationship inside Item.save() to work.
    #
    just_saved_item_dsh_uid = models.CharField(
        max_length=64, blank=True,
        default='', null=True, editable=False,
        verbose_name='just saved item dsh_uid')
    
    #
    # 10/02/02:
    # local landline prefix like 522 or 0522 should get chopped off
    # 
    local_land_line_prefix = models.CharField(
        max_length=80, blank=True,
        default='', null=True, editable=True,
        verbose_name='local landline prefix')
    
    #
    # 10/02/13:
    # after getting the 2nd ISDN line, need to know what channel
    # to put outgoing calls on.
    #
    outgoing_channel = models.CharField(
        max_length=80, blank=True,
        default='', null=True, editable=True,
        verbose_name='outgoing channel')

    #
    # 10/04/09:
    # for testing on laptops.
    # send a dot call to Zoiper on a fellow laptop.
    # the "Channel" line of the dot call should look like this:
    # Channel: IAX2/192.168.2.14:4569-753
    # instead of:
    # Channel: mISDN/4c/9839686230
    # in the "normal" case.
    # the bit of "4569-753" is gotten by looking at the Asterisk
    # console log when a Zoiper phone calls in.
    # this field is used only when "outgoing_channel" above is "IAX2".
    # again, only for testing purposes.
    # normally, this field should be left blank.
    #
    zoiper_number = models.CharField(
        max_length=80, blank=True,
        default='', null=True, editable=True,
        verbose_name='Zoiper number')
    
    asterisk_context = models.CharField(
        max_length=80, blank=True,
        default='', null=True, editable=True,
        verbose_name='asterisk context')
    
    asterisk_extension = models.CharField(
        max_length=80, blank=True,
        default='', null=True, editable=True,
        verbose_name='asterisk extension')

    #
    # 10/02/14:
    # this is appended to the dot file names
    # in the /var/spool/asterisk/outgoing
    # directory so that dvoice and dv2 know which files
    # are whose.
    #
    database_name = models.CharField(
        max_length=80, blank=True,
        default='', null=True, editable=True,
        verbose_name='database name')

    #
    # 10/03/06:
    # port number used for emailed url links. only for dsh.cs
    #
    port = models.CharField(
        max_length=80, blank=True,
        default='', null=True, editable=True,
        verbose_name='dsh.cs port')

    #
    # 10/03/18:
    # pnet1 port number used for emailed url links. 
    #
    port_lko = models.CharField(
        max_length=80, blank=True,
        default='', null=True, editable=True,
        verbose_name='pnet1 port')

    #
    # 10/03/19:
    # do not wipe the /var/spool/asterisk/outgoing directory
    # prior to any reschedule.
    # this is necessary to prevent doctors' answers from being wiped
    # when global auto-dial is disabled.
    #
    reschedule_wipe_disable = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='disable reschedule wipe')



    def __unicode__(self):
        return u'database config'
	
	class Meta:
            ordering = [name]



#
# several more unused tables for possible future expansion.
#
class ZObject02(DshObject):
    name = models.CharField(max_length=80,unique=True)

    def __unicode__(self):
        return self.name
	
	class Meta:
            ordering = [name]


class ZObject03(DshObject):
    name = models.CharField(max_length=80,unique=True,default='')

    def __unicode__(self):
        return self.name
	
	class Meta:
            ordering = [name]


class ZObject04(DshObject):
    name = models.CharField(max_length=80,unique=True)

    def __unicode__(self):
        return self.name
	
	class Meta:
            ordering = [name]


class ZObject05(DshObject):
    name = models.CharField(max_length=80,unique=True)

    def __unicode__(self):
        return self.name
	
	class Meta:
            ordering = [name]


class ZObject06(DshObject):
    name = models.CharField(max_length=80,unique=True)

    def __unicode__(self):
        return self.name
	
	class Meta:
            ordering = [name]


class ZObject07(DshObject):
    name = models.CharField(max_length=80,unique=True)

    def __unicode__(self):
        return self.name
	
	class Meta:
            ordering = [name]


class ZObject08(DshObject):
    name = models.CharField(max_length=80,unique=True)

    def __unicode__(self):
        return self.name
	
	class Meta:
            ordering = [name]



class KeyWord(DshObject):
    key_word = models.CharField(max_length=80,unique=True)

    org_key = models.BooleanField(default=False,
                                  null=True,
                                  blank=True,
                                  verbose_name='group key')
    
    #
    # 10/03/22:
    #
    person_key = models.BooleanField(default=False,
                                     null=True,
                                     blank=True,
                                     verbose_name='person key')


    def __unicode__(self):
        return self.key_word
	
	class Meta:
            ordering = [key_word]


    def keyword_to_text(self):
        description = ''
        if self.key_word:
            description += 'key: ' + self.key_word + ', '
        if self.description:
            description += 'description: ' + self.description + ', '
        if self.comments:
            description += 'comments: ' + self.comments + ', '
        if self.u17:
            description += 'selected, '
        description = description.rstrip()
        description = description.rstrip(',')
        return description


    def save(self, noLogging=False, sessionID=''):
        super(KeyWord, self).save()
        if not noLogging:
            dsh_django_utils.insert_event_after_keyword_add(
                self, sessionID=sessionID)


    def delete(self, sessionID=''):
        dsh_django_utils.insert_event_after_keyword_del(
            self, sessionID=sessionID)
        super(KeyWord, self).delete()


    def selected_icon(self):
        return super(KeyWord, self).selected_icon('keyword')
    selected_icon.short_description = 'sel.'
    selected_icon.allow_tags = True


    def apply_to_selection_icons(self):
        
        addKeyIcon = dsh_django_config.lookup('KEYWORD_ICON')
        addKey = """<a href="/keywordadd/%s"
title="apply this key word to selected items">%s</a>""" % \
        (self.dsh_uid, addKeyIcon)

        delKeyIcon = dsh_django_config.lookup('KEYWORD_DEL_ICON')
        delKey = """<a href="/keyworddel/%s"
title="remove this key word from selected items">%s</a>""" % \
        (self.dsh_uid, delKeyIcon)

        spaces = dsh_django_config.lookup('ICON_SPACES')

        return addKey + spaces + delKey + spaces
    
    apply_to_selection_icons.short_description = 'apply'
    apply_to_selection_icons.allow_tags = True


    def meta_display(self):
        if self.person_key:
            return dsh_common_db.models_person_key_icons(self)
        noWrapStart = dsh_common_config.lookup2('NO_WRAP_OPEN')
        noWrapEnd = dsh_common_config.lookup2('NO_WRAP_END')
        return noWrapStart + \
               self.keyed_sel() + \
               self.keyed_items() + \
               self.apply_to_selection_icons() + \
               self.pin_dsh_uid() + \
               self.selected_icon() + \
               self.keyed_orgs() + \
               noWrapEnd
    meta_display.short_description = 'action'
    meta_display.allow_tags = True


    def keyed_orgs(self):
        return dsh_common_db.models_keyword_org_key_icon(self)
    keyed_orgs.short_description = 'grouped orgs'
    keyed_orgs.allow_tags = True


    def pin_dsh_uid(self):
        spaces = dsh_django_config.lookup('ICON_SPACES')
        icon = dsh_django_config.lookup('PIN_DSH_UID_ICON')
        href = dsh_django_config.lookup('KEYWORD_DSH_UID_URL') + self.dsh_uid
        link = '<a href="%s" title="pin this key word with dsh_uid">%s</a>' % \
               (href, icon)
        return link + spaces
    pin_dsh_uid.short_description = 'pin this key word with dsh_uid'
    pin_dsh_uid.allow_tags = True
    

    def keyed_items(self):
        """which items have this key word."""
        url = dsh_django_config.lookup('KEY_WORD_URL') + str(self.id)
        icon = dsh_django_config.lookup('KEYED_ITEMS_ICON')
        ans = '<a href="%s" title="items that have this key word">%s</a>' %\
               (url, icon)
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return ans + spaces
    keyed_items.short_description = 'items'
    keyed_items.allow_tags = True


    def keyed_sel(self):
        return dsh_common_db.models_keyed_sel(self)
    keyed_sel.short_description = 'select these'
    keyed_sel.allow_tags = True
            


LANGUAGE_TYPE = (
	('HIN', 'Hindi'),
        ('ENG', 'English'),
        ('BEN', 'Bengali'),
        ('MAR', 'Marathi'),
        ('URD', 'Urdu'),
        ('KAN', 'Kannada'),
        ('TAM', 'Tamil'),
        ('TEL', 'Telegu'),
        ('GUJ', 'Gujarati'),
        ('KAS', 'Kashmiri'),
        ('OTH', 'Other'),
)



class Organization(DshObject):
    name = models.CharField(max_length=80)
    alias = models.CharField(max_length=80,unique=True)
    #picture = models.ImageField(upload_to='pics/%Y/%m', blank=True)
    picture = models.ImageField(
        upload_to=dsh_django_utils.make_uploaded_image_name, blank=True)
    language = models.CharField(max_length=3, choices=LANGUAGE_TYPE,
                                default='HIN')

    phone_number = models.CharField(max_length=80, blank=True)
    url = models.URLField(blank=True, verbose_name = 'URL')
    
    address = models.CharField(max_length=256, blank=True)
    city_dist = models.CharField(max_length=80, blank=True,
                                 verbose_name = 'city/district')
    state_province = models.CharField(max_length=80, blank=True,
                                      verbose_name = 'state/province')
    country = models.CharField(max_length=80, blank=True)
    pin = models.CharField(max_length=6, blank=True,
                           verbose_name='Pin/zip')

    spoken_name = models.FileField(
        upload_to=dsh_django_utils.make_uploaded_image_name,
        null=True,
        blank=True,
        verbose_name='spoken name')    

    #
    # 10/01/17: for DIET.
    # people from this organization will only hear broadcast messages
    # with this key word.
    #
    org_key_word = models.ForeignKey(KeyWord,
                                     related_name='keyed_org',
                                     verbose_name='group key',
                                     blank=True,
                                     null=True)


    class Meta:
        get_latest_by = 'modify_datetime'


    def __unicode__(self):
        return self.alias
	
	class Meta:
            ordering = ['name']


    def thumbnail(self):
        return dsh_django_utils.thumbnail(self, self.picture)
    thumbnail.short_description = 'picture'
    thumbnail.allow_tags = True


    def org_to_text(self):
        description = ''
        if self.name:
            description += 'name: ' + self.name + ', '
        if self.alias:
            description += 'alias: ' + self.alias + ', '
        if self.picture:
            description += 'pic: ' + self.picture.url + ', '
        if self.language:
            description += 'lan: ' + self.language + ', '
        if self.phone_number:
            description += 'phone: ' + self.phone_number + ', '
        if self.url:
            description += 'url: ' + self.url + ', '
        if self.description:
            description += 'description: ' + self.description + ', '
        if self.comments:
            description += 'comments: ' + self.comments + ', '
        if self.address:
            description += 'addr: ' + self.address + ', '
        if self.city_dist:
            description += 'city/dist: ' + self.city_dist + ', '
        if self.state_province:
            description += 'state/prov: ' + self.state_province + ', '
        if self.country:
            description += 'country: ' + self.country + ', '
        if self.pin:
            description += 'pin: ' + self.pin + ', '
        if self.u17:
            description += 'selected, '
        description = description.rstrip()
        description = description.rstrip(',')
        return description


    def save(self, noLogging=False, sessionID=''):
        super(Organization, self).save()
        if not noLogging:
            dsh_django_utils.insert_event_after_org_add(
                self, sessionID=sessionID)
        dsh_django_utils.chmod_uploaded_file(self.picture)
        dsh_django_utils.convert_field_to_sln(self.spoken_name)


    def delete(self, sessionID=''):
        dsh_django_utils.insert_event_after_org_del(
            self, sessionID=sessionID)
        super(Organization, self).delete()


    def selected_icon(self):
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return super(Organization, self).selected_icon('organization') + spaces
    selected_icon.short_description = 'sel.'
    selected_icon.allow_tags = True

    
    def org_item_link(self):
        thisID = str(self.id)
        calls = Item.objects.filter(owner__organization=thisID)
        if not calls:
            return ''
        spaces = dsh_django_config.lookup('ICON_SPACES')
        href = dsh_django_config.lookup('ORG_ITEM_URL')
        href = href + thisID
        icon = dsh_django_config.lookup('ORG_ITEM_ICON')
        a = '<a href="%s" title="messages by this organization">%s</a>' %\
            (href,icon)
        return a +spaces


    def org_person_link(self):
        spaces = dsh_django_config.lookup('ICON_SPACES')
        href = dsh_django_config.lookup('ORG_PERSON_URL')
        href = href + str(self.id)
        icon = dsh_django_config.lookup('ORG_PERSON_ICON')
        a = '<a href="%s" title="people from this organization">%s</a>' %\
            (href,icon)
        return a +spaces


    def meta_display(self):
        return self.org_item_link() +\
               self.org_person_link() +\
               self.pin_dsh_uid() + \
               self.selected_icon()
    meta_display.short_description = 'attrs.'
    meta_display.allow_tags = True


    def pin_dsh_uid(self):
        spaces = dsh_django_config.lookup('ICON_SPACES')
        icon = dsh_django_config.lookup('PIN_DSH_UID_ICON')
        href = dsh_django_config.lookup('ORG_PIN_URL') + self.dsh_uid
        link = '<a href="%s" title="pin this org with dsh_uid">%s</a>' % \
               (href, icon)
        return link + spaces
    pin_dsh_uid.short_description = 'pin this org with dsh_uid'
    pin_dsh_uid.allow_tags = True
    

    def spoken_name_display_field(self):
        return dsh_django_utils.item_file_list(self, self.spoken_name,
                                               spokenName=True)
    spoken_name_display_field.short_description = 'spoken name'
    spoken_name_display_field.allow_tags = True


    def org_key_link(self):
        """modeled after Item.get_key_words()."""
        return dsh_common_db.models_org_key_link(self)
    org_key_link.short_description = 'group key'
    org_key_link.allow_tags = True

        

PERSON_TYPE = (
	('ADM', 'administrator'),
	('USR', 'user'),
        ('DOC', 'doctor'),
        ('STF', 'staff'),
	('GST', 'guest'),
	('MOD', 'moderator'),
	('TCH', 'teacher'),
        ('LEA', 'leader'),
	('STU', 'student'),
        ('TST', 'test'),
        ('TS2', 'test2'),
        ('OTH', 'other'),
)

GENDER_TYPE = (
	('M', 'male'),
        ('F', 'female'),
)

#
# for a timed outgoing call, what type?
# 
TIMED_REPEAT_TYPE = (
    ('NONE', 'none'),
    ('HOUR', 'hourly'),
    ('DAIL', 'daily'),
    ('WEEK', 'weekly'),
    ('BIWK', 'biweekly'),
    ('MONT', 'monthly'),
    ('TEST', 'test'),
)


class Person(DshObject):
    first_name = models.CharField(max_length=80, default='unknown')
    last_name = models.CharField(max_length=80, blank=True)
    phone_number = models.CharField(max_length=80, blank=True)
    phone_owner = models.BooleanField(default=False,
                                      null=True,
                                      blank=True)
    phone_std = models.BooleanField(default=False,
                                    null=True,
                                    blank=True,
                                    verbose_name='STD')

    #
    # 10/03/14:
    #
    phone_landline = models.BooleanField(default=False,
                                         null=True,
                                         blank=True,
                                         verbose_name='landline')
        
    #mugshot = models.ImageField(upload_to='pics/%Y/%m', blank=True)
    mugshot = models.ImageField(
        upload_to=dsh_django_utils.make_uploaded_image_name, blank=True)
    organization = models.ForeignKey(Organization,
                                     related_name='person',
                                     verbose_name='org.')
    ptype = models.CharField(max_length=3, choices=PERSON_TYPE, default='TCH',
                             verbose_name='type')
    gender = models.CharField(max_length=1, choices=GENDER_TYPE, default='F')
    email = models.EmailField(blank=True, verbose_name='e-mail')
    url = models.URLField(blank=True)

    spoken_name = models.FileField(
        upload_to=dsh_django_utils.make_uploaded_image_name,
        null=True,
        blank=True,
        verbose_name='spoken name')    

    timed_broadcast = models.BooleanField(default=False,
                                          null=True,
                                          blank=True,
                                          verbose_name='auto-dialed broadcast')
    auto_dial_disabled = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='auto-dialing disabled')
    timed1_type = models.CharField(max_length=4,
                                   choices=TIMED_REPEAT_TYPE,
                                   default='NONE',
                                   blank=True,
                                   null=True,
                                   verbose_name='repeat?')
    timed1 = models.DateTimeField(verbose_name='timed call',
                                  default=None,
                                  null=True,
                                  blank=True)
    timed2_type = models.CharField(max_length=4,
                                   choices=TIMED_REPEAT_TYPE,
                                   default='NONE',
                                   blank=True,
                                   null=True,
                                   verbose_name='timed2 type')
    timed2 = models.DateTimeField(verbose_name='timed call2',
                                  default=None,
                                  null=True,
                                  blank=True)
    timed3_type = models.CharField(max_length=4,
                                   choices=TIMED_REPEAT_TYPE,
                                   default='NONE',
                                   blank=True,
                                   null=True,
                                   verbose_name='timed3 type')
    timed3 = models.DateTimeField(verbose_name='timed call3',
                                  default=None,
                                  null=True,
                                  blank=True)
    timed4_type = models.CharField(max_length=4,
                                   choices=TIMED_REPEAT_TYPE,
                                   default='NONE',
                                   blank=True,
                                   null=True,
                                   verbose_name='timed4 type')
    timed4 = models.DateTimeField(verbose_name='timed call4',
                                  default=None,
                                  null=True,
                                  blank=True)

    #
    # the session ID of the session in the Event table that resulted
    # in the recording of this item.
    #
    session = models.CharField(
        max_length=64, blank=True,
        default='', null=True,
        verbose_name='session')

    #
    # 10/03/13:
    # birth_date and birth_date_approximate are not editable.
    # they are supposed to be the "truth."
    #
    date_birth = models.DateField(
        verbose_name='birth date',
        editable = False,
        default=None,
        null=True,
        blank=True)
    birth_date_approximate = models.BooleanField(
        default=False,
        editable = False,
        null=True,
        blank=True,
        verbose_name='birth date approximate')

    #
    # the following are for data entry.
    #
    age = models.IntegerField(default=0, blank=True, null=True)
    date_birth_change = models.DateField(
        verbose_name='birth date',
        default=None,
        null=True,
        blank=True)
    birth_date_approximate_change = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='birth date approximate')
    
    #
    # 10/03/22
    #
    current_dial = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='in current dial schedule')


    #
    # 10/03/22: for saving a list of people, done at the same time of
    # current dial set.
    #
    person_key_words = models.ManyToManyField(
        KeyWord,
        related_name='keyed_persons',
        verbose_name='keys',
        blank=True,
        null=True)



    class Meta:
        get_latest_by = 'modify_datetime'
        

    def __unicode__(self):
        answer = self.first_name
        if not self.last_name:
            return answer
        return answer + ' ' + self.last_name
	
	class Meta:
            ordering = ['first_name', 'last_name']



    def thumbnail(self):
        """Display thumbnail-size image of ImageField named mugshot.
        Assumes images are not very large (i.e. no manipulation of
        the image is done on backend).
        Requires constant named MAX_THUMB_LENGTH to limit longest axis.
        taken and modified from:
        http://www.djangosnippets.org/snippets/162/        """

        return dsh_django_utils.thumbnail(self, self.mugshot)
    thumbnail.short_description = 'mug'
    thumbnail.allow_tags = True


    def hide_phone_number(self):
        #return dsh_agi.hide_phone_digits(self.phone_number)
        return dsh_django_utils.display_phone_link(self)
    hide_phone_number.short_description = 'phone'
    hide_phone_number.admin_order_field = 'phone_number'
    hide_phone_number.allow_tags = True


    def timed_link(self):
        if not self.timed1 or self.auto_dial_disabled:
            return ''
        spaces = dsh_django_config.lookup('ICON_SPACES')
        href = '/schedulecallee/' + self.dsh_uid
        icon = dsh_django_config.lookup('TIMED_ICON')
        a = '<a href="%s" title="schedule auto-dialed call">%s</a>' %\
            (href,icon)
        return  a + spaces
    timed_link.short_description = 'timed'
    timed_link.allow_tags = True


    def org_link(self):
        org = self.organization
        if not org:
            return ''
        return dsh_django_utils.org_link(org)
    org_link.short_description = 'where'
    org_link.allow_tags = True
    org_link.admin_order_field = 'organization'


    def demographics(self):
        return dsh_common_db.models_person_demographics(self)
    demographics.short_description = 'demo.'
    demographics.allow_tags = True


    def person_to_text(self):
        description = ''
        if self.first_name:
            description += 'first: ' + self.first_name + ', '
        if self.last_name:
            description += 'last: ' + self.last_name + ', '
        if self.phone_number:
            description += 'phone: ' + self.phone_number + ', '
        if self.mugshot:
            description += 'mug: ' + self.mugshot.url + ', '
        if self.organization and self.organization.alias:
            description += 'org: ' + self.organization.alias + ', '
        if self.ptype:
            description += 'type: ' + self.ptype + ', '
        if self.gender:
            description += 'gender: ' + self.gender + ', '
        if self.email:
            description += 'email: ' + self.email + ', '
        if self.url:
            description += 'url: ' + self.url + ', '
        if self.description:
            description += 'description: ' + self.description + ', '
        if self.comments:
            description += 'comments: ' + self.comments + ', '
        if self.u17:
            description += 'selected, '
        description = description.rstrip()
        description = description.rstrip(',')
        return description


    def save(self, noLogging=False, sessionID='', setSession=False):
        """setSession=True when called from dsh_django2.py
        when a new Person is created."""

        if sessionID and setSession:
            self.session = sessionID
        dsh_common_db.models_save_birth_date(self)
        super(Person, self).save()
        if not noLogging:
            dsh_django_utils.insert_event_after_person_add(
                self, sessionID=sessionID)
        #dsh_django_utils.check_auto_timed_calls_for_person(self)
        dsh_django_utils.make_me_phone_owner(self)
        dsh_django_utils.chmod_uploaded_file(self.mugshot)
        dsh_django_utils.convert_field_to_sln(self.spoken_name)


    def delete(self, sessionID=''):
        dsh_django_utils.insert_event_after_person_del(
            self, sessionID=sessionID)
        super(Person, self).delete()


    def selected_icon(self):
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return super(Person, self).selected_icon('person') + spaces
    selected_icon.short_description = 'sel.'
    selected_icon.allow_tags = True


    def personal_msgs_link(self):
        if not self.message_for_me:
            return ''
        msgs = self.message_for_me.all()
        if not msgs:
            return ''
        href = dsh_django_config.lookup('PERSONAL_MESSAGES_HREF')
        href = href + str(self.id)
        icon = dsh_django_config.lookup('PERSONAL_MESSAGES_ICON')
        a = '<a href="%s" title="personalized messages">%s</a>' % (href, icon)
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return a + spaces
    personal_msgs_link.short_description = 'personal messages'
    personal_msgs_link.allow_tags = True


    def person_item_link(self):
        thisID = str(self.id)
        calls = Item.objects.filter(owner=thisID)
        if not calls:
            return ''
        spaces = dsh_django_config.lookup('ICON_SPACES')
        href = dsh_django_config.lookup('PERSON_ITEM_URL')
        href = href + thisID
        icon = dsh_django_config.lookup('PERSON_ITEM_ICON')
        a = '<a href="%s" title="messages by this person">%s</a>' % (href,icon)
        return a +spaces


    def sync_callee_link(self):
        thisID = str(self.id)
        calls = Item.objects.filter(i05=thisID)
        if not calls:
            return ''
        icon = dsh_django_config.lookup('SYNC_CALLEE_ICON')
        href = dsh_django_config.lookup('SYNC_CALLEE_URL')
        href += thisID
        url = '<a href="%s" title="callee: synchronous calls">%s</a>' % \
              (href, icon)
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return url + spaces


    def landline_link(self):
        """10/03/14"""
        return dsh_common_db.models_person_landline_link(self)
    landline_link.short_description = 'landline'
    landline_link.allow_tags = True


    def current_dial_link(self):
        """10/03/22"""
        return dsh_common_db.models_person_current_dial_link(self)
    current_dial_link.short_description = 'in current dial set'
    current_dial_link.allow_tags = True
    

    def meta_display(self):
        return self.person_item_link() + \
               self.timed_link() + \
               self.sync_callee_link() + \
               self.personal_msgs_link() + \
               self.landline_link() + \
               self.current_dial_link() + \
               self.pin_dsh_uid() + \
               self.session_link() + \
               self.person_more_icons() + \
               self.dial_now_link() + \
               self.selected_icon()
    meta_display.short_description = 'attrs.'
    meta_display.allow_tags = True


    def person_more_icons(self):
        """10/03/25"""
        return dsh_common_db.models_person_more_icons(self)
    person_more_icons.short_description = 'more'
    person_more_icons.allow_tags = True
    

    def pin_dsh_uid(self):
        spaces = dsh_django_config.lookup('ICON_SPACES')
        icon = dsh_django_config.lookup('PIN_DSH_UID_ICON')
        href = dsh_django_config.lookup('SCHEDULED_USER_URL') + self.dsh_uid
        link = '<a href="%s" title="pin this person with dsh_uid">%s</a>' % \
               (href, icon)
        return link + spaces
    pin_dsh_uid.short_description = 'pin this person with dsh_uid'
    pin_dsh_uid.allow_tags = True
    

    def spoken_name_display_field(self):
        return dsh_django_utils.item_file_list(self, self.spoken_name,
                                               spokenName=True)
    spoken_name_display_field.short_description = 'spoken name'
    spoken_name_display_field.allow_tags = True


    def dial_now_link(self):
        if not self.phone_number:
            return ''
        if self.phone_std:
            icon = dsh_django_config.lookup('DIAL_NOW_ICON_STD')
            dtext = 'STD: dial this person now'
        else:
            icon = dsh_django_config.lookup('DIAL_NOW_ICON')
            dtext = 'dial this person now'
        href = '/dialnow/' + self.dsh_uid
        url = '<a href="%s" title="%s">%s</a>' % \
              (href, dtext, icon)
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return url + spaces
    dial_now_link.short_description = 'dial now'
    dial_now_link.allow_tags = True


    def session_link(self):
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return dsh_django_utils.session_link(self.session)
    session_link.short_description = 'creating session'
    session_link.allow_tags = True


    def person_key_link(self):
        """modeled after Organization.org_key_link()."""
        return dsh_common_db.models_persons_key_link(self)
    person_key_link.short_description = 'keys'
    person_key_link.allow_tags = True


    def latest_event(self):
        """10/04/14: the latest time the person had a meaningful event
        on the system."""
        return dsh_common_db.models_person_latest_event(self, Event)
    latest_event.short_description = 'latest'
    latest_event.allow_tags = True


                

#
# I couldn't get this to work with limit_choices_to() with more than
# one character encoding.
# the query constructed by django has commans between the characters.
#
ITEM_TYPE = (
	('I', 'incoming'),
        ('B', 'broadcast'),
        ('P', 'personalized'),
        ('S', 'synchronous'),
        ('O', 'other'),
)


#
#XXX
class Item(DshObject):
    #
    # 
    #file = models.FileField(upload_to='voice/%y/%m')
    # the file name looks like:
    # 
    file = models.FileField(
        upload_to=dsh_django_utils.make_uploaded_file_name)
    owner = models.ForeignKey(Person,
                              related_name='items',
                              verbose_name='caller')
    itype = models.CharField(max_length=3,
                             choices=ITEM_TYPE,
                             default='I',
                             verbose_name='type')
    #
    # an active message is the current outgoing message.
    #
    active = models.BooleanField(default=False, blank=True, null=True)
    starred = models.BooleanField(default=False)

    peer_shared = models.BooleanField(default=False,
                                      null=True,
                                      blank=True,
                                      verbose_name='shared with peers')

    play_once = models.BooleanField(default=False,
                                    null=True,
                                    blank=True,
                                    verbose_name='play once')

    call_duration = models.IntegerField(default=0, blank=True)
    rec_duration = models.IntegerField(default=0, blank=True,
                                       verbose_name='record duration')
    key_words = models.ManyToManyField(KeyWord, blank=True,
                                       related_name='items',)
    #
    # the previous message that this message follows up to.
    #
    followup_to = models.ForeignKey('self',
                                    blank=True,
                                    null=True,
                                    related_name='followed_by')
                                    #limit_choices_to={'itype': 'B'})
    
    #
    # intended audience of this message.
    #
    intended_audience = models.ManyToManyField(
        Person, blank=True, null=True, related_name='message_for_me',
        verbose_name='recipient')

    #
    # plucked from the unused fields.
    # used to store callee of a synchronous call.
    #
    i05 = models.ForeignKey(Person, blank=True, null=True,
                            related_name='i05_rel',
                            verbose_name='callee')    


    #
    # try adding columns, mistakenly.  not used.
    #
    timed1_type = models.CharField(max_length=4,
                                   choices=TIMED_REPEAT_TYPE,
                                   default='NONE',
                                   blank=True,
                                   null=True,
                                   verbose_name='timed1 type')
    timed1 = models.DateTimeField(verbose_name='timed call1',
                                  null=True,
                                  blank=True)

    #
    # the session ID of the session in the Event table that resulted
    # in the recording of this item.
    #
    session = models.CharField(
        max_length=64, blank=True,
        default='', null=True,
        verbose_name='session')

    #
    # 10/03/23:
    # for a dummy broadcast.
    #
    dummy = models.BooleanField(default=False,
                                null=True,
                                blank=True,
                                verbose_name='dummy')


    #
    # more unused fields for future.
    #
    i01 = models.ForeignKey('self', blank=True, null=True,
                            related_name='i01_rel')
    i02 = models.ForeignKey('self', blank=True, null=True,
                            related_name='i02_rel')
    i03 = models.ForeignKey('self', blank=True, null=True,
                            related_name='i03_rel')
    i04 = models.ForeignKey('self', blank=True, null=True,
                            related_name='i04_rel')
    i06 = models.ForeignKey(Person, blank=True, null=True,
                            related_name='i06_rel')
    i07 = models.ForeignKey(Person, blank=True, null=True,
                            related_name='i07_rel')
    i08 = models.ForeignKey(Person, blank=True, null=True,
                            related_name='i08_rel')
    i09 = models.ManyToManyField('self', blank=True, null=True,
                                 related_name='i09_rel')
    i10 = models.ManyToManyField('self', blank=True, null=True,
                                 related_name='i10_rel')
    i11 = models.ManyToManyField('self', blank=True, null=True,
                                 related_name='i11_rel')
    i12 = models.ManyToManyField('self', blank=True, null=True,
                                 related_name='i12_rel')
    i13 = models.ManyToManyField(Person, blank=True, null=True,
                                 related_name='i13_rel')
    i14 = models.ManyToManyField(Person, blank=True, null=True,
                                 related_name='i14_rel')
    i15 = models.ManyToManyField(Person, blank=True, null=True,
                                 related_name='i15_rel')
    i16 = models.ManyToManyField(Person, blank=True, null=True,
                                 related_name='i16_rel')

    
    
    class Meta:
        get_latest_by = 'modify_datetime'
        

    def __unicode__(self):
        return self.file.name


    def item_url(self):
        return dsh_django_utils.item_file_list(self, self.file)
    item_url.short_description = "voice 'n stuff"
    item_url.allow_tags = True


    def get_key_words(self):
        keyWords = self.key_words.all()
        displayKeyWords = ''
        for keyWord in keyWords:
            keyWordLookupURL = dsh_django_config.lookup('KEY_WORD_URL')
            keyWordLookupURL += str(keyWord.id)
            s = '<a href="%s">%s</a>' % (keyWordLookupURL, keyWord.key_word)
            displayKeyWords += s + ', '
        displayKeyWords = displayKeyWords.rstrip()
        displayKeyWords = displayKeyWords.rstrip(',')
        return displayKeyWords
    get_key_words.short_description = 'key words'
    get_key_words.allow_tags = True
    

    def thumbnail(self):
        return dsh_django_utils.thumbnail(self.owner, self.owner.mugshot)
    thumbnail.short_description = 'mug'
    thumbnail.allow_tags = True


    def durations(self):
        return str(self.call_duration) + ', ' + str(self.rec_duration)
    durations.short_description = 'durations'

    
    def organization(self):
        return self.owner.organization.alias
    organization.short_description = 'org.'


    def starred_icon(self):
        spaces = dsh_django_config.lookup('ICON_SPACES')
        if self.starred:
            return dsh_django_config.lookup('STAR_ICON') + spaces
        return ''
    starred_icon.short_description = 'starred'
    starred_icon.allow_tags = True


    def active_icon(self):
        if not self.active:
            return ''
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return dsh_django_config.lookup('ACTIVE_ICON') + spaces
    active_icon.short_description = 'active'
    active_icon.allow_tags = True


    def dummy_icon(self):
        return dsh_common_db.models_item_dummy_icon(self)
    dummy_icon.short_description = 'dummy'
    dummy_icon.allow_tags = True


    def intended_audience_icon(self):
        intended = self.intended_audience
        if not intended or len(intended.all())==0:
            return ''
        icon = dsh_django_config.lookup('INTENDED_AUDIENCE_ICON')
        urlPart = dsh_django_config.lookup('INTENDED_AUDIENCE_URL')
        url = urlPart + str(self.id)
        answer = '<a href=%s title="intended audience of personalized message">%s</a>' % (url, icon)
        return answer + dsh_django_config.lookup('ICON_SPACES')
    intended_audience_icon.short_description = 'intended audience'
    intended_audience_icon.allow_tags = True


    def followup_to_icon(self):
        followup = self.followup_to
        if not followup:
            return ''
        url = dsh_django_config.lookup('ITEM_URL') + str(followup.id)
        icon = dsh_django_config.lookup('FOLLOWUP_TO_ICON')
        url = '<a href=%s title="followup to">%s</a>' % (url, icon)
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return url + spaces
    followup_to_icon.short_description = 'followup to'
    followup_to_icon.allow_tags = True


    def followed_by_icon(self):
        thisID = str(self.id)
        followers = Item.objects.filter(followup_to=thisID)
        if not followers:
            return ''
        url = dsh_django_config.lookup('FOLLOWING_ITEM_URL') + thisID
        icon = dsh_django_config.lookup('FOLLOWED_BY_ICON')
        url = '<a href=%s title="followed by">%s</a>' % (url, icon)
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return url + spaces
    followed_by_icon.short_description = 'followed by'
    followed_by_icon.allow_tags = True


    def reply_icon(self):
        url = dsh_django_config.lookup('REPLY_URL') + self.dsh_uid
        icon = dsh_django_config.lookup('REPLY_ICON')
        url = '<a href=%s title="reply">%s</a>' % (url, icon)
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return url + spaces
    reply_icon.short_description = 'reply'
    reply_icon.allow_tags = True


    def reply_upload_icon(self):
        """
        10/03/06: for uploading a doctor's reply.
        modeled after models.reply_icon().
        """
        return dsh_common_db.model_item_reply_upload_icon(self)
    reply_upload_icon.short_description = 'reply upload'
    reply_upload_icon.allow_tags = True
        

    def itype_icon(self):
        itype = self.itype
        spaces = dsh_django_config.lookup('ICON_SPACES')
        if itype == 'B':
            icon = dsh_django_config.lookup('BROADCAST_ICON')
            href = dsh_django_config.lookup('BROADCAST_URL')
            answer = '<a href="%s" title="type: broadcast">%s</a>' % \
                     (href,icon)
            return  answer + spaces
        if itype == 'I':
            icon = dsh_django_config.lookup('INCOMING_ICON')
            href = dsh_django_config.lookup('INCOMING_URL')
            answer = '<a href="%s" title="type: incoming">%s</a>' % \
                     (href,icon)
            return answer + spaces
        if itype == 'S' and self.i05:
            calleeID = str(self.i05.id)
            url = dsh_django_config.lookup('PERSON_URL') + calleeID
            icon = dsh_django_config.lookup('SYNC_CALLEE_ICON')
            return ('<a href="%s" title="synchronous, callee">%s</a>' % \
                    (url, icon)) + spaces
        return ''
    itype_icon.short_description = 'type'
    itype_icon.allow_tags = True


    def peer_shared_icon(self):
        if not self.peer_shared:
            return ''
        icon = dsh_django_config.lookup('PEER_SHARED_ICON')
        href = dsh_django_config.lookup('PEER_SHARED_URL')
        answer = '<a href="%s" title="peer-shared">%s</a>' % (href, icon)
        spaces = dsh_django_config.lookup('ICON_SPACES')
        return  answer + spaces


    def meta_display(self):
        spaces = dsh_django_config.lookup('ICON_SPACES')
        breaks = dsh_django_config.lookup('ICON_LINE_BREAKS')
        return self.itype_icon() + \
               self.peer_shared_icon() + \
               self.intended_audience_icon() + \
               self.conversation_chain_icon() + \
               self.followup_to_icon() + \
               self.followed_by_icon() + \
               self.reply_upload_icon() + \
               self.reply_icon() + \
               self.pin_dsh_uid() + \
               self.session_link() + \
               self.people_heard_link() + \
               self.dummy_icon() + \
               self.active_icon() + \
               self.starred_icon() + \
               self.selected_icon() + breaks + \
               dsh_django_utils.get_file_size(self, self.file) + breaks +\
               self.durations()
    meta_display.short_description = 'attrs.'
    meta_display.allow_tags = True


    def conversation_chain_icon(self):
        """
        10/03/28:
        chase the up-and-down links of the followup_to field to
        display the entire thread of conversation.
        """
        return dsh_common_db.models_item_conversation_chain_icon(self)
    conversation_chain_icon.short_description = "conversation history"
    conversation_chain_icon.allow_tags = True


    def pin_dsh_uid(self):
        spaces = dsh_django_config.lookup('ICON_SPACES')
        icon = dsh_django_config.lookup('PIN_DSH_UID_ICON')
        href = dsh_django_config.lookup('ITEM_DSH_UID_URL') + self.dsh_uid
        link = '<a href="%s" title="pin this item with dsh_uid">%s</a>' % \
               (href, icon)
        return link + spaces
    pin_dsh_uid.short_description = 'pin this item with dsh_uid'
    pin_dsh_uid.allow_tags = True
    

    def session_link(self):
        return dsh_django_utils.session_link(self.session)
    session_link.short_description = 'creating session'
    session_link.allow_tags = True


    def people_heard_link(self):
        link = dsh_django_utils.people_heard_link(self)
        if link:
            spaces = dsh_django_config.lookup('ICON_SPACES')
            return dsh_django_utils.people_heard_link(self) + spaces
        return ''
    people_heard_link.short_description = 'people who have heard this'
    people_heard_link.allow_tags = True


    def testdv2(self):
        dsh_django_utils.debug_event('item.save.testdv2(): entered!', 33)


    def save(self, recurse=False, noLogging=False, sessionID='',
             setSession=False):
        """if the user is uploading an active object,
        we make all the previously active broadcasts inactive.
        setSession=True when called from dsh_django2.py
        when a new Item is created.
        """

        dsh_django_utils.debug_event('item.save: test this', 33)

        if not sessionID:
            sessionID = dsh_common_db.make_session_id()

        #
        # 10/03/26:
        # seems the only one using setSession=True is in dsh_django2.py
        # I don't see why it's needed.
        #
        #if sessionID and setSession:
        if sessionID:
            self.session = sessionID

        dsh_django_utils.debug_event('item.save(): enterd, recurse: ' +
                                     repr(recurse), 2)
        dsh_django_utils.extract_duration(self)
        dsh_django_utils.debug_event(
            'models.save: rec duration: ' + str(self.rec_duration), 4)
        #
        # need to call super().save() after saving the object.
        # otherwise, some fields are not accessible.
        #
        super(Item, self).save()
        if not recurse:
            #
            # 10/01/19: stash the recently saved item dsh_uid so that
            # we can use a signal later to deactivate the old active items.
            # this is because we can't get Many-to-Many relationship to
            # work inside save() and all other attempts have failed.
            #
            #dsh_django_utils.deactivate(self, recurse=recurse)
            dsh_common_db.models_stash_saved_item(self)
            if not noLogging:
                dsh_django_utils.insert_event_after_upload_item(
                    self, sessionID=sessionID)
            dsh_django_utils.debug_event('item.save: test this', 1)
            dsh_django_utils.convert_to_sln(self)
            #
            # 10/03/25:
            # put in an "answered" event if we're uploading an answer
            # by a doctor.
            #
            dsh_common_db.put_doctor_answer_event(
                self, Event, noDuplicate=True, sessionID=sessionID)


    def delete(self, sessionID=''):
        dsh_django_utils.insert_event_after_delete_item(
            self, sessionID=sessionID)
        super(Item, self).delete()
        


    def owner_link(self):
        return dsh_django_utils.person_link(self.owner)
    owner_link.short_description = 'who'
    owner_link.allow_tags = True
    owner_link.admin_order_field = 'owner'


    def person_item_link(self):
        ownerID = str(self.owner.id)
        owner = Person.objects.filter(id=ownerID)
        if not owner:
            return ''
        owner = owner[0]
        return owner.person_item_link()
    person_item_link.short_description = 'who'
    person_item_link.allow_tags = True


    def owner_link_plus_phone(self):
        ownerLink = dsh_django_utils.person_link(self.owner)

        personItems = self.person_item_link()
        if personItems:
            ownerLink += '<br><br>' + personItems
        
        phoneHidden = self.owner.hide_phone_number()
        if phoneHidden:
            ownerLink += '<br><br>' + '<font size=1>' + phoneHidden + \
                         '</font>'
        return ownerLink
    owner_link_plus_phone.short_description = 'who'
    owner_link_plus_phone.allow_tags = True
    owner_link_plus_phone.admin_order_field = 'owner'


    def org_link(self):
        owner = self.owner
        if not owner:
            return ''
        org = owner.organization
        orgStr = dsh_django_utils.org_link(org)
        
        moreIcons = ''
        orgItems = org.org_item_link()
        if orgItems:
            moreIcons += orgItems
        orgPeople = org.org_person_link()
        if orgPeople:
            moreIcons += orgPeople
        if moreIcons:
            orgStr += '<br><br>' + moreIcons
        return orgStr
    org_link.short_description = 'org.'
    org_link.allow_tags = True


    def item_to_text(self):
        description = ''
        if self.file:
            description += 'uploaded: ' + self.file.url + ', '
        if self.itype:
            description += 'itype: ' + self.itype + ', '
        if self.active:
            description += 'active, '
        if self.starred:
            description += 'starred, '
        if self.key_words and len(self.key_words.all()) != 0:
            description += 'key words: ' + self.get_key_words() + ', '
        if self.followup_to:
            description += 'followup to, '
        if self.intended_audience and len(self.intended_audience.all()) != 0:
            description += 'has intended audience, '
        if self.description:
            description += 'description: ' + self.description + ', '
        if self.comments:
            description += 'comments: ' + comments + ', '
        if self.u17:
            description += 'selected, '
        description = description.rstrip()
        description = description.rstrip(',')
        return description


    def email_text(self, br=False, attach=False, urlFields=None,
                   allowTags=False):
        """called by dsh_selection.email_selection()"""
        
        text = u''

        if self.owner:
            name = self.owner.__unicode__()
            text += 'By: %s\n' % (name,)
            if br:
                text += '<BR>'
            if self.owner.organization and self.owner.organization.alias:
                text += 'From: %s\n' % (self.owner.organization.alias,)
                if br:
                    text += '<BR>'
        if self.modify_datetime:
            time = self.modify_datetime
            timeStr = time.strftime(dsh_utils.uploadDateTimeFormat)
            text += 'Time: %s\n' % (timeStr,)
            if br:
                text += '<BR>'
        if self.description:
            text += '\n'
            #text += u'Description: %s\n' % (self.description,)
            text += u'Description: %s\n' % (self.description,)
            if br:
                text += u'<BR>'

        #
        # 10/03/18:
        # always True for sending URLs.
        #
        if True or urlFields and urlFields['dsh_url']:
            #
            # 10/03/06:
            # "http://dsh.cs.washington.edu:8090"
            #
            dshPrefix = dsh_db_config.get('port')
            if not dshPrefix:
                dshPrefix = dsh_django_config.lookup('DSH_URL_PREFIX')
            dshUidUrl = dsh_django_config.lookup('ITEM_DSH_UID_URL') +\
                        self.dsh_uid
            fullURL = dshPrefix + dshUidUrl
            url = 'Seattle: <a href="%s">%s</a>' % (fullURL, fullURL)
            text += '\n'
            if allowTags:
                text += url + '\n'
            else:
                text += 'Seattle: ' + fullURL + '\n'
            if br:
                text += u'<BR>'

            #
            # 10/03/18:
            # "http://10.8.0.14:8090"
            #
            dshPrefix2 = dsh_db_config.get('port_lko')
            if dshPrefix2:
                dshUidUrl = dsh_django_config.lookup('ITEM_DSH_UID_URL') +\
                            self.dsh_uid
                fullURL2 = dshPrefix2 + dshUidUrl
                url2 = 'VPN-LKO: <a href="%s">%s</a>' % (fullURL2, fullURL2)
                text += '\n'
                if allowTags:
                    text += url2 + '\n'
                else:
                    text += 'VPN-LKO: ' + fullURL2 + '\n'
                
        if attach:
            attachedFileName = self.attachment_file_name()
            if attachedFileName:
                text += 'Attached file: %s\n' % (attachedFileName,)
                if br:
                    text += '<BR>'

        return smart_str(text)


    def full_file_path(self):
        """called by dsh_selection.email_selections()."""
        field = self.file
        if (not field) or (not field.file) or (not field.file.file) or \
               (not field.file.file.name):
            return None

        return field.file.file.name


    def attachment_file_name(self):
        """called by dsh_selection.email_selections()."""
        field = self.file
        if (not field) or (not field.file) or (not field.file.file) or \
               (not field.file.file.name):
            return None

        prefix = ''
        if self.owner:
            prefix += self.owner.__unicode__() + '_'
            if self.owner.organization and self.owner.organization.alias:
                prefix += self.owner.organization.alias + '_'

        prefix = dsh_utils.strip_join_str(prefix)
        fileName = os.path.basename(field.file.file.name)
        dshUidLen = dsh_uid_length()
        dshUid = fileName[:dshUidLen]
        ext = fileName.split('.')[-1]
        
        return prefix + dshUid + '.' + ext
        
    
    def selected_icon(self):
        return super(Item, self).selected_icon('item')
    selected_icon.short_description = 'sel.'
    selected_icon.allow_tags = True



EVENT_TYPE = (
    ('DBG', 'debug'),
    ('INF', 'info'),
    ('WRN', 'warning'),
    ('ERR', 'error'),
    ('CRT', 'critical'),
    ('OTH', 'other'),
)


EVENT_TYPE2 = (
    ('CALL', 'call'),
    ('ENTR', 'call entered'),
    ('SYNC', 'sync. call'),
    ('HERD', 'message heard'),
    ('ANSW', 'question answered'),
    ('UNAN', 'un-answer'),
    ('NOAN', 'answer event deleted'),
    ('UNHR', 'message only partially heard'),
    ('NOHR', 'heard event deleted'),
    ('UNHE', 'un-hear'),
    ('DEM1', 'demo reply set'),
    ('DEM2', 'demo dial now'),
    ('BRCT', 'broadcast message played'),
    ('PEER', 'peer shared'),
    ('SCHE', 'call scheduled'),
    ('DNOW', 'dial now'),
    ('RESC', 'reschedule all'),
    ('NOPU', 'not picked up'),
    ('RARM', 'auto re-scheduled'),
    ('STT1', 'stats daily'),
    ('STT2', 'stats web'),
    ('UPLD', 'save'),
    ('RCDS', 'removed from CDS'),
    ('KADD', 'key word applied'),
    ('KDEL', 'key word removed'),
    ('STAR', 'starred selection'),
    ('EMAI', 'selection emailed'),
    ('IDEL', 'item deleted'),
    ('VIEW', 'view'),
    ('PRNT', 'print'),
    ('RPRT', 'report'),
    ('ORGN', 'organization saved'),
    ('ORGD', 'organization deleted'),
    ('PRSN', 'person saved'),
    ('PRSD', 'person deleted'),
    ('KEYW', 'key word saved'),
    ('KEYD', 'key word deleted'),
    ('OTHR', 'other')
)


class Event(DshObject):
    etype = models.CharField(max_length=3, choices=EVENT_TYPE,
                             default='INF',
                             verbose_name='type')
    action = models.CharField(max_length=3, choices=EVENT_TYPE2,
                              default='CALL', blank=True)
    owner = models.ForeignKey(Person, blank=True, null=True)
    call_duration = models.IntegerField(default=0, blank=True, null=True)
    rec_duration = models.IntegerField(default=0, blank=True, null=True,
                                       verbose_name='record duration')
    dsh_uid_concerned = models.CharField(
        max_length=64, blank=True, verbose_name='object id concerned')
    #
    # for debug print tags.
    #
    debug_tag = models.IntegerField(default=0, blank=True, null=True,
                                    verbose_name='tag')
    phone_number = models.CharField(max_length=80, blank=True,
                                    verbose_name='phone')

    session = models.CharField(
        max_length=64, blank=True,
        default='', null=True,
        verbose_name='session')

    #
    # 10/03/20:
    # for doctor replies.
    # questions and answers.
    #
    dsh_uid2 = models.CharField(
        max_length=64, blank=True,
        default='', null=True,
        verbose_name='dsh_uid2')
    


    class Meta:
        get_latest_by = 'modify_datetime'


    def __unicode__(self):
        return self.action
	
	class Meta:
            ordering = [modify_datetime]


    def meta_display(self):
        return self.pin_dsh_uid() + \
               self.selected_icon()
    meta_display.short_description = 'sel.'
    meta_display.allow_tags = True


    def pin_dsh_uid(self):
        spaces = dsh_django_config.lookup('ICON_SPACES')
        icon = dsh_django_config.lookup('PIN_DSH_UID_ICON')
        href = dsh_django_config.lookup('EVENT_DSH_UID_URL') + self.dsh_uid
        link = '<a href="%s" title="pin this event with dsh_uid">%s</a>' % \
               (href, icon)
        return link + spaces
    pin_dsh_uid.short_description = 'pin this event with dsh_uid'
    pin_dsh_uid.allow_tags = True
    

    def selected_icon(self):
        return super(Event, self).selected_icon('event')
    selected_icon.short_description = 'sel.'
    selected_icon.allow_tags = True


    def owner_link(self):
        return dsh_django_utils.person_link(self.owner)
    owner_link.short_description = 'who'
    owner_link.allow_tags = True
    owner_link.admin_order_field = 'owner'


    def org_link(self):
        return dsh_common_db.model_event_org(self)
    org_link.short_description = 'org'
    org_link.allow_tags = True


    def dsh_uid_link(self):
        if not self.dsh_uid_concerned:
            return ''
        return dsh_django_utils.dsh_uid_url(self.dsh_uid_concerned)
    dsh_uid_link.short_description = 'dsh uid'
    dsh_uid_link.allow_tags = True
    dsh_uid_link.admin_order_field = 'dsh_uid_concerned'


    def dsh_uid2_link(self):
        if not self.dsh_uid2:
            return ''
        return dsh_django_utils.dsh_uid_url(self.dsh_uid2)
    dsh_uid2_link.short_description = 'dsh uid2'
    dsh_uid2_link.allow_tags = True
    dsh_uid2_link.admin_order_field = 'dsh_uid2'


    def session_id_link(self):
        if not self.session:
            return ''
        url = dsh_django_config.lookup('SESSION_ID_SEARCH_URL')
        href = '<a href="%s=%s">%s</a>' % \
               (url, self.session, self.session)
        return href
    session_id_link.short_description = 'session'
    session_id_link.allow_tags = True
    session_id_link.admin_order_field = 'session'
    
    

def post_item_save_signal_handler(sender, **kwargs):
    """
    because we can't get many-to-many relationships to work inside save(),
    I have to resort to handling post-save events inside a
    request_started handler.
    see comments in dsh_common_db.models_stash_saved_item(),
    which is called from Item.save().
    """
    dsh_common_db.post_item_save_signal_handler(Item)

django.core.signals.request_started.connect(post_item_save_signal_handler)
