from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class DetectionClass(StrEnum):
    PERSON = "person"
    HELMET = "helmet"
    NO_HELMET = "no_helmet"


class Detection(BaseModel):
    detection_id: str = Field(pattern=r"^SYN-[A-Z0-9-]{3,30}$")
    label: DetectionClass
    confidence: float = Field(ge=0, le=1)
    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)
    width: float = Field(gt=0, le=1)
    height: float = Field(gt=0, le=1)

    @model_validator(mode="after")
    def inside_frame(self) -> "Detection":
        if self.x + self.width > 1 or self.y + self.height > 1:
            raise ValueError("bounding box must stay inside the normalized frame")
        return self


class FrameRequest(BaseModel):
    frame_id: str = Field(pattern=r"^SYN-FRAME-[0-9]{3,6}$")
    review_threshold: float = Field(default=0.7, ge=0.3, le=0.95)
    detections: list[Detection] = Field(min_length=1, max_length=100)


class DetectionReview(Detection):
    needs_review: bool


class FrameResult(BaseModel):
    frame_id: str
    people: int
    helmets: int
    no_helmet: int
    review_items: int
    compliance_observations: int
    detections: list[DetectionReview]
    identity_tracking: bool = False
