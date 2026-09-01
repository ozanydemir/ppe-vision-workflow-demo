from app.models import DetectionClass, DetectionReview, FrameRequest, FrameResult


def evaluate_frame(frame: FrameRequest) -> FrameResult:
    reviewed = [
        DetectionReview(**item.model_dump(), needs_review=item.confidence < frame.review_threshold)
        for item in frame.detections
    ]
    people = sum(item.label is DetectionClass.PERSON for item in frame.detections)
    helmets = sum(item.label is DetectionClass.HELMET for item in frame.detections)
    no_helmet = sum(item.label is DetectionClass.NO_HELMET for item in frame.detections)
    return FrameResult(
        frame_id=frame.frame_id,
        people=people,
        helmets=helmets,
        no_helmet=no_helmet,
        review_items=sum(item.needs_review for item in reviewed),
        compliance_observations=helmets + no_helmet,
        detections=reviewed,
    )
