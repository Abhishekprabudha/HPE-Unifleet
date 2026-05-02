#!/usr/bin/env python3
import re
import subprocess
import tempfile
from pathlib import Path

html = Path('unifleet-narration.html').read_text(encoding='utf-8')
texts = re.findall(r'narrationText:\s*"([^"]+)"', html)
if not texts:
    raise SystemExit('No narrationText entries found')

intro = 'Hello everyone. Welcome.'
all_text = ' '.join([intro, *texts]).replace('HPE', 'H P E')
out = Path('audio/unifleet-complete-narration.mp3')
out.parent.mkdir(exist_ok=True)

with tempfile.TemporaryDirectory() as td:
    raw_mp3 = Path(td) / 'narration_raw.mp3'
    subprocess.check_call([
        'edge-tts',
        '--voice', 'en-GB-SoniaNeural',
        '--rate', '-8%',
        '--text', all_text,
        '--write-media', str(raw_mp3)
    ])
    subprocess.check_call([
        'ffmpeg', '-y', '-i', str(raw_mp3),
        '-codec:a', 'libmp3lame', '-q:a', '3', str(out)
    ])

print(f'Wrote {out}')
