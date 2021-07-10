import subprocess

OUT_FILE = "/tmp/anki.json"
LETTER = 6

try:
    p = subprocess.Popen(["energy", "-b"], stdout=subprocess.PIPE)
    energy, err = p.communicate()
    energy = int(energy)
except Exception as e:
    print(e)
    energy = 100