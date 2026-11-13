#!/usr/bin/env python3
"""Check/apply a reviewed public author handoff locally. Never publishes or reads Firebase.
The operator must obtain the packet through the authorised editorial review desk;
JSON reviewer labels are provenance, not a cryptographic proof of identity.
"""
import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'projects/site'
spec=importlib.util.spec_from_file_location('author_submission_profiles',SITE/'author_submission_profiles.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
REVIEWERS={'ahimanikya@gmail.com','pbiswal804@gmail.com','pareshkpatnaik@gmail.com'}
PACKET_KEYS={'schemaVersion','submissionId','revision','sourceHash','reviewedBy','reviewedAt','status','profile'}

def prepare(packet,site=SITE,author_id=None,photo_path=None):
    if not isinstance(packet,dict) or set(packet)!=PACKET_KEYS or packet['schemaVersion']!=1 or packet['status']!='approved_for_handoff': raise ValueError('Use the exact reviewed profile handoff')
    if packet['reviewedBy'] not in REVIEWERS or not isinstance(packet['reviewedAt'],int) or packet['reviewedAt']<=0: raise ValueError('Missing review provenance')
    if not isinstance(packet['revision'],int) or packet['revision']<1 or not re.fullmatch(r'[A-Za-z0-9]{20}',packet['submissionId']) or not re.fullmatch(r'[a-f0-9]{64}',packet['sourceHash']): raise ValueError('Invalid handoff identity')
    p=packet['profile']
    if not isinstance(p,dict) or p.get('identityChecked') is not True or p.get('mode') not in ('reuse','update','new'): raise ValueError('Author identity must be reviewed')
    allowed={'mode','authorId','identityChecked'} if p['mode']=='reuse' else {'mode','authorId','identityChecked','name','bio','socialLinks','photo'}
    if set(p)!=allowed: raise ValueError('Private or unknown handoff field')
    existing={str(row['id']) for row in json.loads((site/'data/writer-profiles.json').read_text())}
    overlays=json.loads((site/'data/writer-submission-profiles.json').read_text())
    existing.update(overlays)
    if p['mode']=='new':
        if p['authorId']!='' or author_id is None: raise ValueError('Assign a new stable author ID explicitly')
        ident=str(author_id)
        if ident in existing: raise ValueError('New author ID is already in use')
    else:
        ident=p['authorId']
        if ident not in existing or (author_id is not None and str(author_id)!=ident): raise ValueError('Existing author ID does not match')
    if not re.fullmatch(r'[1-9][0-9]{0,7}',ident): raise ValueError('Invalid author ID')
    if p['mode']=='reuse':return {'authorId':ident,'mode':'reuse','profile':None,'derivative':None}
    if ident in ('1','43'): raise ValueError('Use the separate editor-profile workflow')
    public={key:p[key] for key in ['name','bio','socialLinks','mode']};public['photo']=overlays.get(ident,{}).get('photo')
    derivative=None;source=None
    if p['photo'] is not None:
        meta=p['photo']
        if not isinstance(meta,dict) or set(meta)!={'type','size','sha256','permission'} or meta['permission'] is not True or meta['type'] not in ('image/jpeg','image/png','image/webp') or not isinstance(meta['size'],int) or not 0<meta['size']<=5242880 or not re.fullmatch(r'[a-f0-9]{64}',meta['sha256']): raise ValueError('Invalid approved photo metadata')
        if photo_path is None: raise ValueError('Supply the reviewed original photo with --photo')
        source=Path(photo_path).read_bytes()
        if len(source)!=meta['size'] or hashlib.sha256(source).hexdigest()!=meta['sha256']: raise ValueError('Photo differs from the reviewed submission')
        from PIL import Image, ImageOps
        Image.MAX_IMAGE_PIXELS=20000000
        with Image.open(io.BytesIO(source)) as im:
            if im.format not in ('JPEG','PNG','WEBP') or im.width*im.height>20000000: raise ValueError('Unsupported or oversized image')
            clean=ImageOps.exif_transpose(im).convert('RGB');clean.thumbnail((1200,1200))
            out=io.BytesIO();clean.save(out,format='WEBP',quality=88,exif=b'');derivative=out.getvalue()
            public['photo']={'src':f'assets/writers/submitted-{ident}-{meta["sha256"][:12]}.webp','width':clean.width,'height':clean.height,'kind':'journal_photo'}
    elif photo_path is not None:raise ValueError('No submitted photo was approved in this handoff')
    module.validate_profile(public)
    return {'authorId':ident,'mode':p['mode'],'profile':public,'derivative':derivative,'source':source}

def apply(packet,result,site=SITE,root=ROOT):
    if result['mode']=='reuse':return 'existing_preserved'
    ident=result['authorId'];destination=root/'kb/production/author-profile-handoffs'/packet['submissionId']/f'revision-{packet["revision"]}'
    record=destination/'review.json'
    if record.exists():
        if json.loads(record.read_text())!=packet:raise ValueError('This review revision already has different provenance')
        return 'already_applied'
    history=root/'kb/production/author-profile-handoffs'/packet['submissionId']
    if history.exists():
        for prior in history.glob('revision-*/review.json'):
            if json.loads(prior.read_text())['revision']>=packet['revision']:raise ValueError('A newer profile review has already been applied')
    data_path=site/'data/writer-submission-profiles.json';updates=json.loads(data_path.read_text());destination.mkdir(parents=True)
    (destination/'before.json').write_text(json.dumps(updates.get(ident),ensure_ascii=False,indent=2)+'\n')
    if result.get('source') is not None:
        (destination/'source-photo').write_bytes(result['source'])
        (site/result['profile']['photo']['src']).parent.mkdir(parents=True,exist_ok=True)
        (site/result['profile']['photo']['src']).write_bytes(result['derivative'])
    updates[ident]=result['profile'];data_path.write_text(json.dumps(updates,ensure_ascii=False,indent=2)+'\n')
    record.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
    return 'applied_locally'

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('packet',type=Path);parser.add_argument('--author-id',type=int);parser.add_argument('--photo',type=Path)
    group=parser.add_mutually_exclusive_group(required=True);group.add_argument('--check',action='store_true');group.add_argument('--apply',action='store_true')
    args=parser.parse_args();packet=json.loads(args.packet.read_text());result=prepare(packet,author_id=args.author_id,photo_path=args.photo)
    status=apply(packet,result) if args.apply else 'ready_for_local_import'
    print(json.dumps({'status':status,'authorId':result['authorId'],'mode':result['mode'],'published':False}))
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,OSError) as error:raise SystemExit(str(error))
