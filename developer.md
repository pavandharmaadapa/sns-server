# Developer documentation

## Use

### Installation

1.  [Install](https://www.python.org/downloads/) Python 3.12 or higher.
2.  [Install](https://python-poetry.org/docs/#installation) Poetry.
3.  From the `sns_server/` directory of this repo, execute `poetry install`.

### Execution

From the `sns_server/` directory of this repo, execute
`poetry fastapi dev sns_server/server.py`.

### Development

From the `sns_server/` directory of this repo, execute `poetry shell`. Then:

- Format the source code using `black .`
- Before a commit, run python `pre_commit_check.py`.

TODO: a VSCode setup to run Black, isort, flake8 on save.

## Requirements

1.  Support posting files only; no support for text messages.
2.  Support sending from one user to another; no group messages/Facebook-like
    home pages.
3.  Support sending/receiving files, but not streaming audio/video.
4.  Support test modes -- drop packets, delay packets, etc.

## Implementation

1.  Build a simple SNS server with basic authentication using
    [FastAPI](https://fastapi.tiangolo.com/), a Python framework. Use its
    [security](https://fastapi.tiangolo.com/tutorial/security/) framework to
    implement authentication. Use websockets to support push connections. Use
    apache/nginx for an HTTPS connection.
2.  Use a SQL database for persistent storage. Records:
    1.  User (userid, password, friend list?)
    2.  File metadata (name, sender userid, receiver userid, timestamp, number
        of packets?)
    3.  File data (package number, binary data)
