"""Approved public profile overlays; private intake never enters the site build."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

PUBLIC_KEYS={'name','bio','socialLinks','photo','mode'}
PHOTO_KEYS={'src','width','height','kind'}

def public_links(values):
    if not isinstance(values,list) or len(values)>4: raise ValueError('Use up to four public links')
    for value in values:
        if not isinstance(value,str) or len(value)>500 or re.search(r'[\x00-\x20\x7f]',value): raise ValueError('Invalid public URL')
        parsed=urlsplit(value)
        if parsed.scheme!='https' or not parsed.hostname or parsed.username or parsed.password: raise ValueError('Use public HTTPS links')
    return values

def validate_profile(value):
    if not isinstance(value,dict) or set(value)-PUBLIC_KEYS: raise ValueError('Private or unknown profile field')
    if value.get('mode') not in ('new','update'): raise ValueError('Invalid profile mode')
    for key,limit in [('name',120),('bio',5000)]:
        if not isinstance(value.get(key),str) or not value[key].strip() or len(value[key])>limit: raise ValueError('Invalid '+key)
    if re.search(r'[\r\n\x00-\x1f\x7f]',value['name']): raise ValueError('Invalid author name')
    public_links(value.get('socialLinks',[]))
    photo=value.get('photo')
    if photo is not None:
        if not isinstance(photo,dict) or set(photo)!=PHOTO_KEYS or photo.get('kind')!='journal_photo' or not re.fullmatch(r'assets/writers/submitted-[0-9]+-[a-f0-9]{12}\.webp',photo.get('src','')): raise ValueError('Invalid public photo')
        if not all(isinstance(photo.get(k),int) and 0<photo[k]<=1200 for k in ['width','height']): raise ValueError('Invalid image dimensions')
    return value

def load_submission_profiles(root, writers):
    path=Path(root)/'data/writer-submission-profiles.json'
    updates=json.loads(path.read_text()) if path.exists() else {}
    by_id={p['id']:p for p in writers}
    for key,value in updates.items():
        if not re.fullmatch(r'[1-9][0-9]{0,7}',key): raise ValueError('Invalid author ID')
        ident=int(key);validate_profile(value)
        if ident in (1,43): raise ValueError('Editor profiles require the separate editorial profile workflow')
        if ident not in by_id:
            if value['mode']!='new': raise ValueError('Profile update has no existing author')
            writer={'id':ident,'name':value['name'],'biography':value['bio'],'works':[],'biography_kind':'author_supplied_reviewed'}
            writers.append(writer);by_id[ident]=writer
        else:
            by_id[ident]['name']=value['name'];by_id[ident]['biography']=value['bio']
        by_id[ident]['submission_profile']=value
        if value.get('photo') and not (Path(root)/value['photo']['src']).is_file(): raise ValueError('Missing approved profile photo')
    return writers
