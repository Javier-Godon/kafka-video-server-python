import json
from typing import Annotated

from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from pydantic import ValidationError

from app.file_chunks.usecases.send_video_by_chunks.rest.video_data_request import VideoDataRequest
from app.file_chunks.usecases.send_video_by_chunks.send_video_by_chunks_handler import read_file_by_chunks

router = APIRouter()


# @router.post("/video/send/")
# async def split_and_send_video(video_data_request: VideoDataRequest,video: Annotated[bytes, File()]):
#     return await read_file_by_chunks(video_data_request.sha_id,
#                                      video_data_request.element_id, video_data_request.element_alias,
#                                      video_data_request.unix_epoch_start, video_data_request.unix_epoch_end,
#                                      video_data_request.video_path,video)

@router.post("/video/send/")
async def split_and_send_video(video_data_request: Annotated[str, Form(...)], video: UploadFile = File(...)):
    try:
        # Parse and validate the JSON string into the Pydantic model
        parsed_request = VideoDataRequest.model_validate(json.loads(video_data_request))
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")
    return await read_file_by_chunks(parsed_request.sha_id,
                                     parsed_request.element_id, parsed_request.element_alias,
                                     parsed_request.unix_epoch_start, parsed_request.unix_epoch_end,
                                     parsed_request.video_path, video.file)
