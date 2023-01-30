import os
import re
from glob import glob
path = '/home/jeangjenq/repository/read_up_version/media/checker_v001/checker_v001.%04d.exr'

versions_pattern = [r"v-?\d+"]
frame_paddings = [r"%\d+[dD]", r"\#+"]

for pattern in versions_pattern + frame_paddings:
    path = re.sub(pattern, "*", path)

def all_same(items):
    return all(x == items[0] for x in items)

files = glob(path)
print(files)
versions = []
for file in files:
    find_version = re.findall(versions_pattern[0], file)
    if find_version and all_same(find_version):
        if find_version[0] not in versions:
            versions.append(find_version[0])

print(versions)