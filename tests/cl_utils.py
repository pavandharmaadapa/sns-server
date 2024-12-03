# `cl_utils.py` - Utilities supporting common command-line statements
# ===================================================================
#
# Imports
# -------
# These are listed in the order prescribed by [PEP
# 8](http://www.python.org/dev/peps/pep-0008/#imports).
#
# ### Standard library
import os
import subprocess
import sys
from pathlib import Path
from types import TracebackType
from typing import Any, Literal

# ### Local imports
# None.

# OS detection
# ------------
# This follows the [Python
# recommendations](https://docs.python.org/3/library/sys.html#sys.platform).
is_win = sys.platform == "win32"
is_linux = sys.platform.startswith("linux")
is_darwin = sys.platform == "darwin"

# Copied from the [Python
# docs](https://docs.python.org/3.5/library/platform.html#cross-platform).
is_64bits = sys.maxsize > 2**32


# Support code
# ------------
# ### xqt
# Pronounced "execute": provides a simple way to execute a system command.
def xqt(
    # Commands to run. For example, `'foo -param firstArg secondArg', 'bar |
    # grep alpha'`.
    *cmds: str,
    # This is passed directly to `subprocess.run`.
    check: bool = True,
    # This is passed directly to `subprocess.run`.
    shell: bool = True,
    # Optional keyword arguments to pass on to
    # [subprocess.run](https://docs.python.org/3/library/subprocess.html#subprocess.run).
    **kwargs: Any,
) -> subprocess.CompletedProcess | list[subprocess.CompletedProcess]:
    ret = []
    # Although the
    # [docs](https://docs.python.org/3/library/subprocess.html#subprocess.Popen)
    # state, "The only time you need to specify `shell=True` on Windows is when
    # the command you wish to execute is built into the shell (e.g. **dir** or
    # **copy**). You do not need `shell=True` to run a batch file or
    # console-based executable.", use `shell=True` to both allow shell commands
    # and to support simple redirection (such as `blah > nul`, instead of
    # passing `stdout=subprocess.DEVNULL` to `check_call`).
    for cmd in cmds:
        # Per
        # [SO](http://stackoverflow.com/questions/15931526/why-subprocess-stdout-to-a-file-is-written-out-of-order),
        # the `run` below will flush stdout and stderr, causing all the
        # subprocess output to appear first, followed by all the Python output
        # (such as the print statement above). So, flush the buffers to avoid
        # this.
        wd = kwargs.get("cwd", os.getcwd())
        flush_print(f"{wd}$ {cmd}")
        # Use bash instead of sh, so that `source` and other bash syntax works.
        # See
        # [subprocess.popen](https://docs.python.org/3/library/subprocess.html#subprocess.Popen).
        executable = "/bin/bash" if is_linux or is_darwin else None
        try:
            cp = subprocess.run(
                cmd, shell=shell, executable=executable, check=check, **kwargs
            )
        except subprocess.CalledProcessError as e:
            flush_print(f"{e.stderr or ''}{e.stdout or ''}")
            raise
        ret.append(cp)

    # Return a list only if there were multiple commands to execute.
    return ret[0] if len(ret) == 1 else ret


# ### env
# Transforms `os.environ["ENV_VAR"]` to the more compact `env.ENV_VAR`. Returns
# `None` if the env var doesn't exist.
class EnvType(type):
    def __getattr__(cls, name: str) -> str | None:
        return os.environ.get(name)

    def __setattr__(cls, name: str, value: Any) -> None:
        os.environ[name] = value


class env(metaclass=EnvType):
    pass


# ### pushd
# A context manager for pushd.
class pushd:
    """This is a context manager for pushd.  It will remember where you were
    and take you back there when you exit the context manager.

    :param path: The path to change to upon entering the context manager.
    :type path: str | Path
    """

    def __init__(
        self,
        # The path to change to upon entering the context manager.
        path: str | Path,
        verbose: bool = False,
    ):
        self.path = path
        self.verbose = verbose

    def __enter__(self) -> None:
        if self.verbose:
            flush_print(f"pushd {self.path}")
        self.cwd = os.getcwd()
        os.chdir(str(self.path))

    def __exit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        if self.verbose:
            flush_print(f"popd - returning to {self.cwd}.")
        os.chdir(str(self.cwd))
        return False


# ### chdir
def chdir(path: str | Path) -> None:
    flush_print(f"cd {path}")
    os.chdir(str(path))


# ### mkdir
def mkdir(path: str | Path, *args: Any, **kwargs: Any) -> None:
    flush_print(f"mkdir {path}")
    Path(path).mkdir(*args, **kwargs)


# ### flush_print
# Anything sent to `print` won't be printed until Python flushes its buffers,
# which means what CI logs report may be reflect what's actually being executed
# -- until the buffers are flushed.
def flush_print(*args: Any, **kwargs: Any) -> None:
    print(*args, **kwargs)
    # Flush both buffers, just in case there's something in either one.
    sys.stdout.flush()
    sys.stderr.flush()


# ### isfile
def isfile(f: str | Path) -> bool:
    _ = Path(f).is_file()
    flush_print(f"File {f} {'exists' if _ else 'does not exist'}.")
    return _


# ### isdir
def isdir(f: str | Path) -> bool:
    _ = Path(f).is_dir()
    flush_print(f"Directory {f} {'exists' if _ else 'does not exist'}.")
    return _
