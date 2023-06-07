import pandas as pd
from lib.info import list_profiles
import re, string

def get_shadows(ver_group, sha_group, port):
    with open("sessions", "w") as f:
        pass
    with open("session_names", "w") as f:
        pass

    data = list_profiles(port)
    df = pd.DataFrame(data)
    locked_ver = df.loc[df['group'] == ver_group]
    locked_sha = df.loc[df['group'] == sha_group]

    return locked_sha, locked_ver


def lock(locked, s):
    if s == 1:
        set = "верифицированых"
    else:
        set = "не верифицированых"
    ids = locked["uuid"]
    len_ids = len(ids)
    print(f"Колво теневых {set} сессий: " , len_ids)
    names = locked["name"]
    for i in names:
        pattern = r'[' + string.punctuation + ']'
        name = re.sub(pattern, "", i)
        with open("session_names", "a", encoding="UTF-8") as f:
            f.write(name + "\n")


    for i in ids:
        with open("sessions", "a", encoding="UTF-8") as f:
            f.write(str(i) + "\n")


