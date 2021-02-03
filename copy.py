"""
module to implement progress barwith file copy
"""
import shutil
import sys
import argparse
from pathlib import Path
from pymitter import EventEmitter


COPY_BUFSIZE = 1024*1024
ee = EventEmitter()

def copyfileobj(fsrc, fdst, length=0):
    """
    ovverridden version of shutil's copyfileobj which emits events for data copied
    copy data from file-like object fsrc to file-like object fdst
    """
    # Localize variable access to minimize overhead.
    if not length:
        length = COPY_BUFSIZE
    fsrc_read = fsrc.read
    fdst_write = fdst.write
    total_buf = 0
    while True:        
        buf = fsrc_read(length)
        if not buf:
            break
        fdst_write(buf)
        total_buf += len(buf)
        ee.emit('onfilecopy', total_buf, size)


shutil.copyfileobj = copyfileobj

@ee.on('onfilecopy')
def _handler_onfilecopy(count,total):
    progress(count, total)

def progress(count, total, status=''):
    """
    https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("src", help="source file path ")
    argParser.add_argument("dest", help="destination file path")
    args = argParser.parse_args()

    size = Path(args.src).stat().st_size        
    shutil.copyfile(args.src, args.dest)
