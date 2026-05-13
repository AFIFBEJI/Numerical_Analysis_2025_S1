"""
ETAPE 1 : Lance ce script D'ABORD sur ta machine.
Il mesure les durées réelles de tes MP3 et affiche
les valeurs à copier dans anlyse.py

python mesure_durees.py
"""

import os, wave, struct

DIR = "audio_ip"

def mp3_duration_frames(path):
    """Lit les frame headers MP3 pour durée exacte."""
    BITRATES_V1_L3 = [0,32,40,48,56,64,80,96,112,128,160,192,224,256,320,0]
    SAMPLERATES    = [44100,48000,32000,0]
    total_ms = 0
    with open(path,"rb") as f:
        data = f.read()
    i = 0
    # Skip ID3
    if data[:3] == b"ID3":
        s = data[6:10]
        i = (((s[0]&0x7f)<<21)|((s[1]&0x7f)<<14)|((s[2]&0x7f)<<7)|(s[3]&0x7f)) + 10
    while i < len(data)-4:
        if data[i]==0xFF and (data[i+1]&0xE0)==0xE0:
            h = struct.unpack(">I", data[i:i+4])[0]
            layer   = 4 - ((h>>17)&3)
            br_idx  = (h>>12)&0xF
            sr_idx  = (h>>10)&0x3
            padding = (h>>9)&0x1
            if layer==3 and 0<br_idx<15 and sr_idx<3:
                br = BITRATES_V1_L3[br_idx]*1000
                sr = SAMPLERATES[sr_idx]
                if br>0 and sr>0:
                    frame_len = int(144*br/sr)+padding
                    total_ms += int(1152*1000/sr)
                    i += max(1,frame_len)
                    continue
        i += 1
    return total_ms/1000.0

if not os.path.exists(DIR):
    print(f"ERREUR: dossier '{DIR}' introuvable.")
    print("Lance d'abord: manim -p -qh anlyse.py IP")
    print("pour générer les MP3, puis relance ce script.")
    exit(1)

files = sorted(f for f in os.listdir(DIR) if f.endswith(".mp3"))
if not files:
    print(f"ERREUR: aucun MP3 dans '{DIR}'")
    exit(1)

print("# Copie ces valeurs dans DURATIONS de anlyse.py")
print("DURATIONS = {")
for fname in files:
    key  = fname.replace(".mp3","")
    path = os.path.join(DIR, fname)
    dur  = mp3_duration_frames(path)
    # Arrondi à 0.1s près, +0.5s de marge de sécurité
    safe = round(dur + 0.5, 1)
    print(f'    "{key}": {safe},   # réel={dur:.2f}s')
print("}")