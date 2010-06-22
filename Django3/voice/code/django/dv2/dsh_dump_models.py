#
# these are the "definition" files used by dsh_dump.py.
# they are tied to db/models.py.
# it's repetition but this is easier for me to understand and manage.
# 



#
# this corresponds to the parent abstract object.
# it contains the fields common to all other object types.
#
DshObjectDef = {
    'dsh_uid': ['StrType'],
    'add_datetime': ['DateType'],
    'save_datetime': ['DateType'],
    'modify_datetime': ['DateType'],
    'description': ['StrType'],
    'comments': ['StrType'],
    'discreet': ['BoolType'],
    'u17': ['BoolType'],
}


KeyWordDef = {
    'key_word': ['StrType'],
}


OrgDef = {
    'name': ['StrType'],
    'alias': ['StrType'],
    'picture': ['FileType'],
    'language': ['StrType'],
    'phone_number': ['StrType'],
    'url': ['StrType'],
    'address': ['StrType'],
    'city_dist': ['StrType'],
    'state_province': ['StrType'],
    'country': ['StrType'],
    'pin': ['StrType'],
    'spoken_name': ['FileType'],
}


PersonDef = {
    'first_name': ['StrType'],
    'last_name': ['StrType'],
    'phone_number': ['StrType'],
    'phone_owner': ['BoolType'],
    'mugshot': ['FileType'],
    'organization': ['RequiredForeignOrgType'],
    'ptype': ['StrType'],
    'gender': ['StrType'],
    'email': ['StrType'],
    'url': ['StrType'],
    'spoken_name': ['FileType'],
    'timed_broadcast': ['BoolType'],
    'auto_dial_disabled': ['BoolType'],
    'timed1': ['DateType'],
    'timed1_type': ['StrType'],
    'timed2': ['DateType'],
    'timed2_type': ['StrType'],
    'timed3': ['DateType'],
    'timed3_type': ['StrType'],
    'timed4': ['DateType'],
    'timed4_type': ['StrType'],
}


ItemDef = {
    'file': ['FileType'],
    'owner': ['RequiredForeignPersonType'],
    'itype': ['StrType'],
    'active': ['BoolType'],
    'starred': ['BoolType'],
    'peer_shared': ['BoolType'],
    'play_once': ['BoolType'],
    'call_duration': ['IntType'],
    'rec_duration': ['IntType'],
    'key_words': ['OptionalKeyWordsType'],
    'followup_to': ['OptionalFollowUpsType'],
    'intended_audience': ['OptionalPersonsType'],
    'i05': ['OptionalOwnerType'],
}


EventDef = {
    'etype': ['StrType'],
    'action': ['StrType'],
    'owner': ['OptionalOwnerType'],
    'call_duration': ['IntType'],
    'rec_duration': ['IntType'],
    'dsh_uid_concerned': ['StrType'],
    'debug_tag': ['IntType'],
    'phone_number': ['StrType'],
}
