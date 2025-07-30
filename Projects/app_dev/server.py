from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.responses import FileResponse
from redis_client import r_links
import os

app = FastAPI()


@app.get("/download/{token}")
async def download(token: str):
    key = f"link:{token}"
    if not await r_links.exists(key):
        raise HTTPException(status_code=404, detail="Ссылка не найдена или устарела")
    
    used = await r_links.hget(key, "used")
    if used == "true":
        raise HTTPException(status_code=410, detail="Ссылка уже использована")
    
    path = await r_links.hget(key, "path")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    # Пометить ссылку как использованную
    await r_links.hset(key, "used", "true")
    
    return FileResponse(path, filename=os.path.basename(path))

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )










