__author__ = 'Dani'
import os


######## The next two functions were taken form stackoverflow
# http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python

def decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif item is None:
            value = None
        elif isinstance(item, list):
            item = decode_list(item)
        elif isinstance(item, dict):
            item = decode_dict(item)
        rv.append(item)
    return rv


def decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif value is None:  # ??
            value = None
        elif isinstance(value, list):
            value = decode_list(value)
        elif isinstance(value, dict):
            value = decode_dict(value)
        rv[key] = value
    return rv

##############


def rel_path_to_file(rel_path, base_file):
    """
    Ir receives a relative path and the path to the file in which it was written.
    It returns the absolute path obtained from calculating a rel_path from base_file.
    Example:

    base_file: /root/something/project/test/a_test.py
    real_path: ../files/a_file.txt

    result ---> /root/something/project/files/a_file.txt

    """
    steps_behind = max(rel_path.count("../"),
                       rel_path.count("..\\"))

    dir_target = os.path.dirname(base_file)
    while steps_behind != 0:
        if dir_target[-1] in ['/', '\\']:
            dir_target = dir_target[:-1]
        dir_target = os.path.dirname(dir_target)
        steps_behind -= 1

    path_forward = rel_path.replace("../", "").replace("..\\", "")

    # print os.path.normpath(os.path.join(dir_target, path_forward))
    return os.path.normpath(os.path.join(dir_target, path_forward))


