import pytest
from pydantic import ValidationError

from app.evaluator import evaluate_frame
from app.models import Detection, DetectionClass, FrameRequest


def detection(detection_id: str, label: DetectionClass, confidence: float) -> Detection:
    return Detection(
        detection_id=detection_id,
        label=label,
        confidence=confidence,
        x=0.1,
        y=0.1,
        width=0.2,
        height=0.3,
    )


def test_aggregates_compliance_without_identity() -> None:
    result = evaluate_frame(
        FrameRequest(
            frame_id="SYN-FRAME-001",
            detections=[
                detection("SYN-PERSON-1", DetectionClass.PERSON, 0.95),
                detection("SYN-HELMET-1", DetectionClass.HELMET, 0.88),
                detection("SYN-NOHELMET-1", DetectionClass.NO_HELMET, 0.61),
            ],
        )
    )
    assert result.people == 1
    assert result.compliance_observations == 2
    assert result.review_items == 1
    assert result.identity_tracking is False


def test_rejects_box_outside_frame() -> None:
    with pytest.raises(ValidationError):
        Detection(
            detection_id="SYN-BOX-1",
            label=DetectionClass.PERSON,
            confidence=0.9,
            x=0.9,
            y=0.9,
            width=0.2,
            height=0.2,
        )
