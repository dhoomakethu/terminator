"""
@author: dhoomakethu
"""
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import json
import shutil


def banner(text, ch='=', length=80, pad=True):
    bstr = " %s " % text if pad else "%s" % text
    return bstr.center(length, ch) + "\n"


def path(name=""):
    """
    Retrieve the relative filepath to a supplied name from the BrightEdge
    root directory. If the name begins with a "/", then consider the supplied
    name to be an absolute path.

    Example:
    If BrightEdge Root is: /home/vagrant/mydir
    path() will return "/home/vagrant/mydir"
    path("dir1/subdir1") will return "/home/vagrant/mydir/dir1/subdir1"
    path("/usr/bin/python") will return "/usr/bin/python"
    """
    if name.startswith(os.path.sep):
        return name
    actual = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)[:-1]
    if name:
        actual.extend(name.split(os.path.sep))
    return os.path.join(os.path.sep, *actual)


def from_this_dir(cur_dir, filename=""):
    """
    Returns the absolute path to a relative `filename` by joining it with
    the absolute dir from `cur_dir`.

    If the filename starts with the os path separator, it is considered an
    absolute path and returned as is.

    Args:
        cur_dir: The path to a dir whose directory name must be
            used as the base.
        filename: The relative filename or path which must be joined with
            cur_dir.

    """
    if filename.startswith(os.path.sep):
        return filename
    else:
        return os.path.join(os.path.abspath(cur_dir), filename)


def from_this_file(cur_file, filename=""):
    """
    Returns the absolute path to a relative `filename` by joining it with
    the absolute dir from `cur_file`. To get a file in the current script's
    directory call `from_this_file(__file__, "filename")`.

    If the filename starts with the os path separator, it is considered an
    absolute path and returned as is.

    Args:
        cur_file: The path to a file whose directory name must be
            used as the base.
        filename: The relative filename or path which must be joined to the
            cur_file's dirname.

    """
    cur_dir = os.path.dirname(cur_file)
    return from_this_dir(cur_dir, filename)


def from_cwd(filename=""):
    """
    Returns the absolute path to a relative `filename` by joining it with
    the current working directory.

    If the filename starts with the os path separator, it is considered an
    absolute path and returned as is.

    Args:
        filename: The relative filename or path which must be joined with
            the current working directory.

    """
    if filename.startswith(os.path.sep):
        return filename
    else:
        return os.path.join(os.getcwd(), filename)


def make_dir(name):
    """
    mkdir -p <name> if it doesn't exist.
    """
    if not os.path.exists(name):
        os.makedirs(name)


def remove_file(name):
    if os.path.exists(name):
        os.remove(name)


def remove_dir(name):
    """
    rm -rf <name> if it exists.
    """
    if os.path.exists(name):
        shutil.rmtree(name)


def files(path):
    files = []
    if os.path.exists(path):
        for _file in os.listdir(path):
            files.append(os.path.join(path, _file))
    return files


def basename(path):
    return os.path.basename(path)


def json_dump(contents, name=None, indent=4, as_list=False, default=repr):
    repr_data = []
    if name is not None:
        repr_data = [name]
    try:
        json_data = json.dumps(
            contents, sort_keys=True, indent=indent, default=default
        ).split("\n")
        repr_data.extend(json_data)
    except Exception:
        repr_data.append(contents)
    if as_list is True:
        return repr_data
    else:
        for line in repr_data:
            print line


class ValueStore(object):

    def to_json(self, sort_keys=True, indent=4, default=repr, **kwargs):
        return json.dumps(
            self.to_dict(),
            sort_keys=sort_keys,
            indent=indent,
            default=default,
            **kwargs
        )

    def to_dict(self):
        return self.__dict__.copy()

    def clone(self):
        return self.__class__(**self.to_dict())

    def pprint(self):
        print self.to_json()

    def __repr__(self):
        items = self.__dict__.items()
        elems = ["%s=%s" % (k, v) for k, v in items if v is not None]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(elems))


class Color:

    # STYLES
    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CSELECTED = '\33[7m'

    # COLORS
    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

COLOR_DICT = {
    "red": Color.CRED,
    "green": Color.CGREEN,
    "blue": Color.CBLUE,
    "black": Color.CBLACK,
    "yellow": Color.CYELLOW,
    "violet": Color.CVIOLET,
    "beige": Color.CBEIGE,
    "white": Color.CWHITE
}

STYLE_DICT = {
    "bold": Color.CBOLD,
    "italic": Color.CITALIC,
    "underline": Color.CURL,
    "select": Color.CSELECTED
}


def colored_print(msg, color="blue", style='bold', newline=True):
    """
    Prints a colored message on supported terminal
    :param msg: Message to be printed
    :param color: red, green, yellow, blue, violet, beige
    :param style: bold, italic, underlined, selected
    :param newline: True/False inserts newline after msg
    :return: None
    """
    color = COLOR_DICT.get(color, Color.CWHITE)
    style = STYLE_DICT.get(style, Color.CEND)
    try:
        print(color + style + msg + Color.CEND)
    except Exception:
        print msg
    if newline:
        print

