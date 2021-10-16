from app.user.models import *
from app.user.controllers import *
from app.database import *
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse


router = APIRouter(
    prefix="/user",
)


@router.get("/", response_model=User, tags=["user"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post('/', tags=["user"])
async def add_user(new_user: User, current_user: User = Depends(get_current_user), tags=["user"]):
    if(get_user(users_db, new_user.username)):
        raise HTTPException(
            status_code=404, detail=f'Username is not available'
        )
    new_password = get_password_hash(new_user.password)
    new_data = {"username": new_user.username, "password": new_password,
                "full_name": new_user.full_name, "disabled": new_user.disabled, "email": new_user.email}
    users_db[new_user.username] = new_data

    with open("./app/user.json", "w") as write_user:
        json.dump(users_data, write_user, indent=4)
    write_user.close()
    return new_data
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )
