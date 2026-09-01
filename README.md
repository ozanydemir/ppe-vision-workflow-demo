# PPE Vision Workflow Demo

> **Status:** This project is currently under active development. Evaluation rules, event schemas,
> and interface details may change as the prototype evolves.

A public-safe demonstration of the workflow around an industrial PPE detection model. It validates
synthetic detection events, aggregates helmet/no-helmet observations, identifies low-confidence
items for review, and exposes the evidence through FastAPI and a responsive index dashboard.

This repository contains no private workplace image, employee, face, identity, camera, site, dataset,
label file, video, model weight, or production metric. One credited Pexels stock photo provides
presentation context only; the demo never analyzes it and all detections are synthetic.

## Interface

<p align="center">
  <img src="docs/screenshots/index-desktop.png" width="73%" alt="PPE review workflow with licensed reference photo on desktop">
  <img src="docs/screenshots/index-mobile.png" width="23%" alt="PPE review workflow with licensed reference photo on mobile">
</p>

## Media boundary

The page uses one credited Pexels photo only as presentation context. The API never receives it; no
inference, identity, or safety conclusion is made from the image. See `ASSET_CREDITS.md`.

## Architecture

```mermaid
flowchart LR
    A[Synthetic detections] --> B[Schema validation]
    B --> C[Confidence policy]
    C --> D[PPE event aggregation]
    D --> E[Review queue]
    D --> F[Compliance summary]
```

## Demonstrated concepts

- typed bounding-box events;
- confidence thresholds and review states;
- person/helmet/no-helmet aggregation without identity tracking;
- class and coordinate validation;
- synthetic visual overlay and automated tests.

No accuracy percentage is claimed because no public benchmark dataset is shipped with this demo.

## Run

```bash
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
pytest
ruff check .
```

Open `http://127.0.0.1:8000` or inspect `/docs`.
