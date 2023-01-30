import re
import nuke
from glob import glob
from nukescripts.version import version_get, version_set

def detect_all_versions(node):
    # detect all versions that exists in node folder
    # nukescripts.version_latest() contains similar function
    # but it's only friendly with v+1
    # so if there's a version skip it stops at a certain version
    # not my prefer method
    versions = []
    file = nuke.filename(node)
    # regex patterns to replace versions and frame paddings to *
    # we will use glob later to search for all files
    versions_pattern = [r"v-?\d+"]
    frame_paddings = [r"%\d+[dD]", r"\#+"]

    for pattern in versions_pattern + frame_paddings:
        file = re.sub(pattern, "*", file)
    
    # make sure all v### found in files are the same number
    # don't know under what occasion you might have 2 different versions
    # in same file path, don't know what to do about it
    def all_same(items):
        return all(x == items[0] for x in items)
    # glob returns list of files that matches the pattern
    # in this case probably all the individual frames
    files = glob(file)
    versions = []
    for file in files:
        find_version = re.findall(versions_pattern[0], file)
        if find_version and all_same(find_version):
            if find_version[0] not in versions:
                versions.append(find_version[0])
    return versions

def latest_versions_for_all():
    # simply set all read to latest version
    for node in nuke.allNodes("Read"):
        (prefix, v) = version_get(nuke.filename(node), "v")
        # get the last in list as it should be latest version
        latest_version = detect_all_versions(node)[-1]
        latest_file = version_set(  node['file'].value(),
                                    "v",
                                    int(v),
                                    int(latest_version[1:]))
        node['file'].setValue(latest_file)