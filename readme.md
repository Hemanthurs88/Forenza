# AI-Assisted Forensic Facial Reconstruction System

## Overview

This project is a **product-oriented MVP** designed to assist law enforcement in reconstructing suspect faces from eyewitness descriptions.

Unlike generic image generation systems, this platform focuses on:

* **Deterministic control**
* **Identity consistency across iterations**
* **Structured facial parameter manipulation**

The system combines **parametric control, AI-assisted NLP, and generative models** to produce reproducible and refinable facial composites.

---

## Problem

Traditional forensic sketching:

* Requires skilled artists
* Is time-consuming
* Produces inconsistent outputs

Existing AI tools:

* Lack control
* Are non-deterministic
* Cannot preserve identity across edits

---

## Solution

A system that enables:

1. Natural language → structured facial parameters
2. Controlled face generation using latent representations
3. Iterative refinement without identity drift
4. Exportable high-resolution composites
5. Full audit trail for accountability

---

## Key Features

### 1. Controlled Face Generation

* Uses pretrained StyleGAN
* Parameter-driven modifications (10 core features)
* Deterministic outputs

---

### 2. Hybrid Interaction System

* **Sliders (primary control)**
* **Chat interface (assistive control)**

---

### 3. Identity Consistency

* Base latent vector is fixed per session
* Edits applied incrementally
* Same inputs → same output

---

### 4. NLP with Regional Language Support

* Input accepted in multiple languages
* Parsed via OpenAI API
* Converted into structured parameter updates

---

### 5. Audit Logging

* Structured, append-only logs
* Tracks:

  * parameter changes
  * timestamps
  * user actions
  * generated outputs

---

### 6. Exportable Outputs

* High-resolution face generation
* Reproducible via stored parameters

---

## System Architecture

### Monolithic but Modular Design

```
Client (React)
   ↓
Backend (FastAPI)

Modules:
- Auth
- Session Manager
- Parameter Engine
- NLP Parser
- Identity Engine
- Face Generator
- Audit Logger
- Storage Layer
```

---

## Core Modules

### 1. Session Manager

Maintains:

* base latent vector
* parameter state
* version history

---

### 2. Parameter Engine

* Validates inputs
* Normalizes values (0–1 range)
* Acts as system control layer

---

### 3. NLP Parser

* Converts text → parameters
* Supports regional languages via translation + LLM parsing

---

### 4. Identity Engine

Maintains consistency:

```
Z_current = Z_base + Σ(feature_directions × weights)
```

---

### 5. Face Generator

* Converts latent vectors → images
* Uses pretrained GAN

---

### 6. Audit Logger

Stores structured logs for every interaction.

---

### 7. Storage Layer

* PostgreSQL → metadata, sessions, logs
* Object storage (S3/GCS) → generated images

---

## Data Flow

### Parameter Update Flow

```
User Input (slider/chat)
   ↓
Parameter Engine
   ↓
Session Update
   ↓
Identity Engine
   ↓
Face Generator
   ↓
Storage
   ↓
Audit Log
   ↓
Response to UI
```

---

## Parameter Schema (Initial)

| Feature         | Description           |
| --------------- | --------------------- |
| jaw_width       | Face width            |
| chin_length     | Chin extension        |
| eye_size        | Eye scale             |
| eye_spacing     | Distance between eyes |
| nose_length     | Nose height           |
| nose_width      | Nose breadth          |
| lip_thickness   | Lip volume            |
| mouth_width     | Mouth span            |
| forehead_height | Upper face ratio      |
| skin_tone       | Tone variation        |

Range: **0.0 – 1.0**

---

## Tech Stack

### Frontend

* React
* Tailwind CSS

### Backend

* FastAPI (Python)

### AI / ML

* StyleGAN
* OpenAI API

### Storage

* PostgreSQL
* AWS S3 / GCP Storage

---

## Setup Instructions

### 1. Clone Repo

```
git clone <repo_url>
cd project
```

### 2. Backend Setup

```
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Frontend Setup

```
npm install
npm run dev
```

---

## Project Structure

```
/frontend
/backend
   /auth
   /session
   /parameters
   /nlp
   /identity
   /generator
   /audit
   /storage
```

---

## Success Criteria

* Deterministic face generation
* Identity preserved across edits
* Accurate NLP → parameter mapping
* Full audit traceability
* Usable UI for non-experts

---

## Limitations

* Not legally admissible evidence
* Limited parameter granularity (v1)
* Bias inherited from pretrained models

---

## Roadmap

### Phase 1 (MVP)

* Core generation + sliders
* NLP parsing
* Audit logging

### Phase 2

* Improved latent direction control
* Better parameter granularity

### Phase 3

* Database matching (using embeddings like ArcFace)
* Bias mitigation layer
* Advanced UI controls

---

## Differentiation

This system differs from standard AI generators by:

* Enforcing **deterministic control**
* Maintaining **identity across edits**
* Supporting **regional language input**
* Providing **audit-ready workflows**

---

## Disclaimer

This system is intended as an **investigative aid only**, not a definitive identification tool.

---

## Contributors

* Team of 4 (Control, Rendering, NLP, Infra)
