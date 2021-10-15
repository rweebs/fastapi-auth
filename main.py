import json
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "7049df34ffff4ea67ada6caa17b5d37941ec527c25588062afbb605d74cd2f8e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#Buka file menu.json
with open("user.json",'r+') as read_user:
    users_data=json.load(read_user)
    fake_users_db = users_data["user"]

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    password : str


class UserInDB(User):
    password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")





#Definisi model
class Item(BaseModel):
    name: str

#Buka file menu.json
with open("menu.json",'r+') as read_file:
    data = json.load(read_file)
app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/token", response_model=Token)

async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    if not user:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Incorrect username or password",

            headers={"WWW-Authenticate": "Bearer"},

        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(

        data={"sub": user.username}, expires_delta=access_token_expires

    )

    return {"access_token": access_token, "token_type": "bearer"}



@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post('/users')
async def add_user(new_user:User):
    if(get_user(fake_users_db, new_user.username)):
        raise HTTPException(
        status_code=404, detail=f'Username is not available'
    )
    new_password=get_password_hash(new_user.password)
    new_data={"username":new_user.username,"password":new_password,"full_name":new_user.full_name,"disabled":new_user.disabled,"email":new_user.email}
    fake_users_db[new_user.username]=new_data
    read_user.close()
    with open("user.json","w") as write_user:
            json.dump(users_data,write_user,indent=4)
    write_user.close()
    return new_data
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )
    
@app.get('/')
async def root():
    return RedirectResponse("/docs")

@app.get('/menu')
async def get_all_menu(current_user: User = Depends(get_current_user)):
    return data
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.get('/menu/{item_id}')
async def get_menu(item_id: int,current_user: User = Depends(get_current_user)):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.patch('/menu/{item_id}')
async def update_menu(item_id: int,item:Item,current_user: User = Depends(get_current_user)):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            menu_item['name'] = item.name
            read_file.close()
            with open("menu.json","w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.delete('/menu/{item_id}')
async def delete_menu(item_id: int,current_user: User = Depends(get_current_user)):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            data["menu"].remove(menu_item)
            read_file.close()
            with open("menu.json","w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()
            return JSONResponse(
                jsonable_encoder(
                    {
                        "message":"Data Menu:"+str(item_id)+" Deleted Successfully",
                    })
                )
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.post('/menu')
async def add_menu(item:Item,current_user: User = Depends(get_current_user)):
    id=1
    if(len(data["menu"])>0):
        id=data["menu"][len(data["menu"])-1]["id"]+1
    new_data={"id":id,"name":item.name}
    data['menu'].append(dict(new_data))
    read_file.close()
    with open("menu.json","w") as write_file:
            json.dump(data,write_file,indent=4)
    write_file.close()
    return new_data
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )
