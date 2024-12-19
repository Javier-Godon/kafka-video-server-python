from fastapi import APIRouter

from app.file_chunks.usecases.send_video_by_chunks.rest.video_data_request import VideoDataRequest
from app.file_chunks.usecases.send_video_by_chunks.send_video_by_chunks_handler import read_file_by_chunks

router = APIRouter()


@router.post("/video/send/")
async def split_and_send_video(video_data_request: VideoDataRequest):
    return await read_file_by_chunks(video_data_request.sha_id,
                                     video_data_request.element_id, video_data_request.element_alias,
                                     video_data_request.unix_epoch_start, video_data_request.unix_epoch_end,
                                     video_data_request.video_path)
