#!/usr/bin/env python3
"""Build sys-sdweb's compact CFTITLE1 title-id/name index."""
import argparse, json, struct
from pathlib import Path

def load_overrides(path):
    out={}
    if not path or not Path(path).exists(): return out
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        tid,name=(line.split('\t',1)+[''])[:2]
        if len(tid)==16:
            try: int(tid,16); out[tid.upper()]=name.strip()
            except ValueError: pass
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('json'); ap.add_argument('output'); ap.add_argument('--overrides',default='overrides.tsv'); args=ap.parse_args()
    data=json.loads(Path(args.json).read_text(encoding='utf-8'))
    names={}
    for key,obj in data.items():
        # titledb currently uses an internal numeric product key while the
        # actual Switch title ID is the record's `id` field.  Accept both
        # layouts so older/local exports continue to work.
        tid = obj.get('id', key) if isinstance(obj, dict) else key
        tid=str(tid).upper()
        if len(tid)!=16:
            continue
        try: int(tid,16)
        except ValueError: continue
        name=obj.get('name') if isinstance(obj,dict) else obj
        if isinstance(name,str) and name.strip(): names[tid]=name.strip()
    names.update(load_overrides(args.overrides))
    records=[]; strings=bytearray()
    for tid in sorted(names):
        raw=names[tid].encode('utf-8','replace')[:512]
        off=len(strings); strings.extend(raw); strings.append(0)
        records.append((int(tid,16),off))
    string_offset=32+len(records)*0x30
    out=bytearray(struct.pack('<8sIIIQ',b'CFTITLE1',1,0x30,len(records),string_offset))
    for tid,off in records:
        rec=bytearray(0x30); struct.pack_into('<QII',rec,0,tid,off,0); struct.pack_into('<I',rec,44,1); out.extend(rec)
    out.extend(strings); Path(args.output).write_bytes(out)
    print(f'wrote {len(records)} titles, {len(out)} bytes')
if __name__=='__main__': main()
