"""Log viewing and comparison utilities"""

# Standard libraries
import os
import re
import shutil
import subprocess
import sys
import tempfile


# Matches log timestamps like: [ 03-09-2026  12:34:56.78 ]
_TIMESTAMP_RE = re.compile(
    r" \[ [01]\d-[0-3]\d-[12][90]\d{2}  [012]\d:[0-6]\d[.:]\d{2}(\.\d{3})? \] "
)


def catlog_text(text):
    """Replace log timestamps in text with [***]."""
    return _TIMESTAMP_RE.sub(" [***] ", text)


def catlog_file(filepath):
    """Return catlog-processed content of a file."""
    with open(filepath, "r") as fh:
        return catlog_text(fh.read())


def catloglast_file(filepath):
    """Return catlog-processed content of the last run section in a file."""
    with open(filepath, "r") as fh:
        lines = fh.readlines()

    last_hdr = None
    for i, line in enumerate(lines):
        if " Run number: " in line:
            last_hdr = i  # 0-indexed

    if last_hdr is None or last_hdr == 0:
        return catlog_text("".join(lines))
    return catlog_text("".join(lines[last_hdr:]))


def logdiff(file1, file2, diff_opts=None, use_last=False):
    """
    Diff two log files after processing with catlog.

    Arguments
    ---------
    file1, file2 : paths to log files
    diff_opts    : list of extra options passed to diff (uses sdiff by default)
    use_last     : if True, use catloglast instead of catlog
    """
    cat_func = catloglast_file if use_last else catlog_file

    content1 = cat_func(file1)
    content2 = cat_func(file2)

    cols = shutil.get_terminal_size().columns

    if diff_opts:
        diff_cmd = ["diff"] + diff_opts
        less_opts = ["-i"]
    else:
        diff_cmd = ["sdiff", "-ibW", f"-w{cols}"]
        less_opts = ["-i", "-p", "( [>|][\t]| [<|]$)"]

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".log", delete=False
    ) as t1, tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as t2:
        t1.write(content1)
        t2.write(content2)
        tmp1, tmp2 = t1.name, t2.name

    try:
        if sys.stdout.isatty():
            result = subprocess.run(diff_cmd + [tmp1, tmp2], stdout=subprocess.PIPE)
            subprocess.run(["less"] + less_opts, input=result.stdout)
        else:
            subprocess.run(diff_cmd + [tmp1, tmp2])
    finally:
        os.unlink(tmp1)
        os.unlink(tmp2)
