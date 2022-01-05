import requests as rq
from math import log, ceil

from discord import Member, Embed, Color

from constants import PERMISSION_LEVELS, STAFF_ROLE, FCRUI_ROLE, Done, InProgress, NotStarted

def make_error_embed(desc:str):
    return Embed(title="Erreur",
                        description=desc,
                        color=Color.red())

def get_member_permission_level(mb : Member):
    roles_id = {str(r.id).strip() for r in mb.roles}
    if STAFF_ROLE in roles_id : return 'staff'
    if FCRUI_ROLE in roles_id : return 'fcrui'
    return 'member'

def is_perm_authorized(member_level:str, perm_level:str):
    member_perm_index = PERMISSION_LEVELS.index(member_level)
    cmd_perm_index = PERMISSION_LEVELS.index(perm_level)
    return member_perm_index >= cmd_perm_index

def get_command_permission_level(cmd):
    return cmd.__dict__['__original_kwargs__'].get('permission_level') or 'member'

def is_command_authorized(mb:Member, command):
    return is_perm_authorized(get_member_permission_level(mb), get_command_permission_level(command))

def get_last_chapter_data():
    url = "https://api.mangadex.org/manga/4f9eab7d-a2b2-4ee5-9d59-6744f0df4e12/feed"
    params = {
        "limit": 1,
        "translatedLanguage[]": 'fr',
        "order[publishAt]": "desc"
    }

    r = rq.get(url, params=params)
    return r.json()['data'][0]

def get_mangadex_id(chap_number:str):
    chap_number = str(chap_number)
    url = f"https://api.mangadex.org/manga/4f9eab7d-a2b2-4ee5-9d59-6744f0df4e12/aggregate" \
          f"?translatedLanguage[]=fr"

    resp = rq.get(url)
    data = resp.json()['volumes']
    chapid = None
    for volume in data.values():
        if chap_number in volume['chapters']:
            chapid = volume['chapters'][chap_number]["id"]
            break

    return chapid

def alphabet_pos_to_char(pos:int):
    return chr(ord('A')-1 + pos)  # from 1 to 26

def char_to_alphabet_pos(char:str):
    return ord(char.upper()) - ord('A') + 1  # from 1 to 26

def int_to_sheet_row(n:int):

    """
    Up to ZZ (702)
    """
    if n < 26:
        return alphabet_pos_to_char(n)

    row = ''
    while n > 26:
        char = (n-1) // 26
        while char > 26:
            char = char//26

        n -= char*26
        row += alphabet_pos_to_char(char)
    row += alphabet_pos_to_char(n)

    return row

def rgb_to_chap_state(rgb):
    if rgb.green == 1:
        return Done
    if rgb.red == 1:
        if rgb.green > 0:
            return InProgress
        return NotStarted