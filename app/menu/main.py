from app.menu.models import Item
from app.database import *
from app.user.controllers import get_current_active_user
from app.user.models import User
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse


data = read_menu()
router = APIRouter(
    prefix="/menu",
)


@router.get('/', tags=["menu"])
async def get_all_menu(current_user: User = Depends(get_current_active_user)):
    return data
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )


@router.get('/{item_id}', tags=["menu"])
async def get_menu(item_id: int, current_user: User = Depends(get_current_active_user)):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )


@router.patch('/{item_id}', tags=["menu"])
async def update_menu(item_id: int, item: Item, current_user: User = Depends(get_current_active_user)):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            menu_item['name'] = item.name
            read_file.close()
            with open("./app/menu.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            write_file.close()
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )


@router.delete('/{item_id}', tags=["menu"])
async def delete_menu(item_id: int, current_user: User = Depends(get_current_active_user)):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            data["menu"].remove(menu_item)
            read_file.close()
            with open("./app/menu.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            write_file.close()
            return JSONResponse(
                jsonable_encoder(
                    {
                        "message": "Data Menu:"+str(item_id)+" Deleted Successfully",
                    })
            )
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )


@router.post('/', tags=["menu"])
async def add_menu(item: Item, current_user: User = Depends(get_current_active_user)):
    id = 1
    if(len(data["menu"]) > 0):
        id = data["menu"][len(data["menu"])-1]["id"]+1
    new_data = {"id": id, "name": item.name}
    data['menu'].append(dict(new_data))
    read_file.close()
    with open("./app/menu.json", "w") as write_file:
        json.dump(data, write_file, indent=4)
    write_file.close()
    return new_data
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )
