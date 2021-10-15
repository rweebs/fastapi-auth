import json
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse

with open("menu.json",'r+') as read_file:
    data = json.load(read_file)
app = FastAPI()

class Item(BaseModel):
    name: str

@app.get('/')
async def root():
    return RedirectResponse("/docs")

@app.get('/menu')
async def get_all_menu():
    return data
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.get('/menu/{item_id}')
async def get_menu(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.patch('/menu/{item_id}')
async def update_menu(item_id: int,item:Item):
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
async def delete_menu(item_id: int):
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
async def add_menu(item:Item):
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
