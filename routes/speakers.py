from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID

from schemas.speakers import Speaker, SpeakerUpdate
from services.speakers import SpeakerService

# Create a global instance of SpeakerService.
speaker_service_instance = SpeakerService()

# Dependency function to provide the SpeakerService instance to route handlers.
def get_speaker_service() -> SpeakerService:
    return speaker_service_instance

router = APIRouter(prefix="/speakers", tags=["Speakers"])
@router.post("/", response_model=Speaker, status_code=status.HTTP_201_CREATED)
def create_speaker(speaker: Speaker, speaker_service: SpeakerService = Depends(get_speaker_service)):
    """
    Creates a new speaker.
    - **speaker**: Speaker object containing name and topic.
    """
    return speaker_service.create_speaker(speaker)

@router.get("/speakers/{speaker_id}", response_model=Speaker)
def read_speaker(speaker_id: str, speaker_service: SpeakerService = Depends(get_speaker_service)):
    """
    Retrieves a single speaker by ID.
    """
    speaker = speaker_service.get_speaker(speaker_id)
    if not speaker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Speaker not found")
    return speaker

@router.get("/speakers/", response_model=List[Speaker])
def read_all_speakers(speaker_service: SpeakerService = Depends(get_speaker_service)):
    """
    Retrieves a list of all speakers.
    """
    return speaker_service.get_all_speakers()

@router.put("/speakers/{speaker_id}", response_model=Speaker)
def update_speaker(speaker_id: str, speaker_update: SpeakerUpdate, speaker_service: SpeakerService = Depends(get_speaker_service)):
    """
    Updates a speaker's information.
    """
    speaker = speaker_service.update_speaker(speaker_id, speaker_update)
    if not speaker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Speaker not found")
    return speaker

@router.delete("/speakers/{speaker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_speaker(speaker_id: str, speaker_service: SpeakerService = Depends(get_speaker_service)):
    """
    Deletes a speaker by ID.
    """
    if not speaker_service.delete_speaker(speaker_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Speaker not found")
    return