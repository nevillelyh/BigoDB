import base64
import hashlib
import os
import shlex
import subprocess

import config

def run(args):
    child = subprocess.Popen(args,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            close_fds=True)
    out = child.stdout.readlines()
    ret = child.wait()
    return ret, out

def evalz(val):
    val = val.lstrip('0')
    if val:
        return eval(val)
    else:
        return 0

def parse_duration(duration):
    ts, ms = duration.split('.')
    hour, minute, sec = ts.split(':')
    return evalz(hour)*3600+evalz(minute)*60+evalz(sec)+evalz(ms)/100.0

def extract_duration(line):
    return line[line.find(':')+1:line.find(',')].strip()

def get_info(path):
    args = shlex.split('ffmpeg -i')
    args.append(path)
    info = { 'duration': 0, 'stream': [] }

    ret, out = run(args)

    for l in out:
        l = l.strip()
        if l.startswith('Duration: '):
            info['duration'] = extract_duration(l)
        elif l.startswith('Stream #'):
            info['stream'].append(l)
    return info

def get_snapshot_path(path):
    hashstr = base64.b64encode(hashlib.md5(path).digest(), '_-')
    filename = 'S%s.jpg' % hashstr.rstrip('=')
    return os.path.join(config.STATIC_DIR, 'snapshot', filename)

def take_snapshot(vfile, offset, sfile):
    args = shlex.split('ffmpeg -y -vframes 1')
    args.append('-ss')
    args.append('%d' % offset)
    args.append('-i')
    args.append(vfile)
    args.append('-f')
    args.append('image2')
    args.append(sfile)
    ret, out = run(args)

def take_release_snapshot(dirpath):
    fileinfo = []
    for filename in sorted(os.listdir(dirpath)):
        root, ext = os.path.splitext(filename)
        if ext not in ['.avi', '.mkv', '.mp4']:
            continue

        vfile = os.path.join(dirpath, filename)
        sfile = get_snapshot_path(vfile)
        info = get_info(vfile)

        if info['duration'] == 0 or len(info['stream']) == 0:
            continue

        offset = parse_duration(info['duration']) / 2
        take_snapshot(vfile, offset, sfile)

        fileinfo.append({
            'path': vfile,
            'snapshot': os.path.basename(sfile),
            'info': info,
            })
    return fileinfo
