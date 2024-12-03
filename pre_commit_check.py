#!/usr/bin/env python3
# # `pre_commit_check.py` - Run a series of checks that should all pass before submitting a pull request
# In a perfect world, these would also pass before every commit.
#
#
# Imports
# =======
# These are listed in the order prescribed by [PEP 8](https://peps.python.org/pep-0008/).
#
# Standard library
# ----------------
# None.
#
# Third-party imports
# -------------------
# None.
#
# Local application imports
# -------------------------
from tests.cl_utils import xqt


# Checks
# ======
def checks() -> None:
    xqt(
        # fmt: off
        "black --check .",
        "flake8",
        "mypy --install-types --non-interactive",
        "pytest",
        # fmt: on
    )


if __name__ == "__main__":
    checks()
