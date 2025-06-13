from typing import Dict, List, Optional
from schemas.speakers import Speaker, SpeakerBase, SpeakerUpdate
import uuid

class SpeakerService:
   
    def __init__(self):
        # In-memory storage for speakers, mapping speaker_id to SpeakerInDB objects.
        self.speakers: Dict[str, Speaker] = {}
        self._initialize_speakers() # Call initialization method on service creation

    def _initialize_speakers(self):
        
        speaker1 = Speaker(id=str(uuid.uuid4()), name="Dr. Mary Anne", topic="Future of AI")
        speaker2 = Speaker(id=str(uuid.uuid4()), name="Ms. Maria Rodriguez", topic="Sustainable Practices")
        speaker3 = Speaker(id=str(uuid.uuid4()), name="Mr. David Lee", topic="Cybersecurity Trends")
        
        self.speakers[speaker1.id] = speaker1
        self.speakers[speaker2.id] = speaker2
        self.speakers[speaker3.id] = speaker3

    def create_speaker(self, speaker_create: SpeakerUpdate) -> Speaker:
        new_speaker = Speaker(
            id=str(uuid.uuid4()), # Generate a unique ID for the new speaker
            name=speaker_create.name,
            topic=speaker_create.topic
        )
        self.speakers[new_speaker.id] = new_speaker 
        return new_speaker

    def get_speaker(self, speaker_id: str) -> Optional[Speaker]:
        # Retrieves a speaker by their ID.
        # Returns None if the speaker is not found.
    
        return self.speakers.get(speaker_id)

    def get_all_speakers(self) -> List[Speaker]:
        
        return list(self.speakers.values())

    def update_speaker(self, speaker_id: str, speaker_update: SpeakerUpdate) -> Optional[Speaker]:
        # Updates an existing speaker's information.
        # Only updates fields that are provided in speaker_update.
        # Returns the updated speaker or None if the speaker is not found.
      
        speaker = self.speakers.get(speaker_id)
        if not speaker:
            return None
        
        # Convert the Pydantic SpeakerUpdate model to a dictionary, excluding unset fields.
        update_data = speaker_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(speaker, key, value)
        
        self.speakers[speaker_id] = speaker # Re-store the updated speaker
        return speaker

    def delete_speaker(self, speaker_id: str) -> bool: #Deletes a speaker from the storage by their ID.Returns True if the speaker was deleted, False otherwise.
        if speaker_id in self.speakers:
            del self.speakers[speaker_id]
            return True
        return False