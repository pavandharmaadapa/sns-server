# # `server.py` -- Core SNS server functionality

# This is just a copy and paste from FastAPI docs on [security](https://fastapi.tiangolo.com/tutorial/security/).
#
# TODO: define a user model and a function to authenticate users.
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    return {"token": token}
