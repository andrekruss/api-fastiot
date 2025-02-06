from beanie import PydanticObjectId
from fastapi import HTTPException

def validate_object_id(object_id: str) -> PydanticObjectId:
    """Validates if informed object id is valid."""
    try:
        return PydanticObjectId(object_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")