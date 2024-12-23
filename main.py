import uvicorn
from fastapi import FastAPI

from app.configuration.configuration import get_data
from app.file_chunks.usecases.send_video_by_chunks.rest.router import router

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
     style="{",
     datefmt="%Y-%m-%d %H:%M",
 )

app = FastAPI()

app.include_router(router=router)

port = get_data()['server']['port']


# @app.get("/")
# async def root():
#     return {"message": "Hello Bigger Applications!"}

if __name__ == "__main__":
    logger.info(f'Exposing port: {port}', exc_info=True)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
