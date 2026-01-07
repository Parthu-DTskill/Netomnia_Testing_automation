🧩 Netomnia Automation System
📌 Overview

The Netomnia Automation System is a Selenium-based automation framework designed to process Closure and Blockage features in the Netomnia web application.

The system:

Logs into the Netomnia UI

Navigates to Project → Build Layer → Features

Processes Closure and Blockage feature data from an API

Downloads images, PDFs, and PPTX files

Extracts embedded images from PDFs

Removes duplicate images

Compresses images for server-friendly storage

Organizes outputs into a clean folder structure

Tracks and reports rejected features

The framework is production-ready, server-safe, and CI/CD compatible.

🏗️ Architecture Principles

This project follows strict architectural rules:

Single Responsibility – each file does one job

One-direction imports – prevents circular dependencies

Pure Python – no OS-level binaries (Poppler / LibreOffice removed)

Deterministic Selenium actions – stable in headless/server runs

Failure isolation – one feature failure doesn’t stop the run

📂 Project Structure
Netomnia-Testing-Main/
│
├── main.py
├── requirements.txt
│
├── workflows/
│   ├── base_workflow.py
│   ├── closure.py
│   └── blockage.py
│
├── media/
│   ├── base_media.py
│   ├── closure_media.py
│   └── blockage_media.py
│
├── core/
│   ├── api.py
│   ├── browser.py
│   ├── login.py
│   ├── navigation.py
│   ├── rejection.py
│   ├── pdf_image_extract.py
│   ├── image_dedupe.py
│   ├── image_compress.py
│   └── pdf_media_processor.py
│
├── variables.py
├── conditions.py
└── data/

🚀 Execution Flow
main.py
 ├─ Create browser
 ├─ Login
 ├─ Navigate to project & build layer
 ├─ Fetch API data
 ├─ Split into Closure & Blockage
 ├─ Run ClosureWorkflow
 ├─ Run BlockageWorkflow
 ├─ Print rejections
 └─ Cleanup browser


main.py is orchestration only — it contains no business logic.

🧠 Core Components
🔹 Browser & Navigation (core/)

browser.py – creates Selenium WebDriver (headless-ready)

login.py – handles authentication

navigation.py – navigates through Netomnia UI

api.py – fetches feature data from backend API

rejection.py – collects rejected features with reasons

🔄 Workflow Layer (workflows/)
BaseWorkflow (base_workflow.py)

Shared functionality for all workflows:

Feature folder creation

Safe Ant Design dropdown selection

UI reset handling

Key method

force_select_ant_option()
Safely selects Closure / Blockage in Ant Design dropdowns (prevents click interception issues).

ClosureWorkflow (closure.py)

Processes Closure features:

Select Closure feature type

Enter Feature ID

Click Eye icon

Validate Build Status ≥ 7

If code = TST003 → download Power Meter images

Else → download closure media

Log rejections on failure

BlockageWorkflow (blockage.py)

Processes Blockage features:

Select Blockage feature type

Enter Feature ID

Validate Build Status

Validate Siebel Reference & Whereabouts

Download media

Log rejected features if validation fails

📁 Media Layer (media/)
BaseMedia (base_media.py)

Shared Selenium and HTTP helpers.

ClosureMedia (closure_media.py)

Handles all media downloading:

Inline images

PDF documents

PPTX documents

Power Meter image blocks

Each downloaded document is passed to the PDF Media Pipeline.

📄 PDF Media Pipeline (core/pdf_media_processor.py)

Orchestrates document processing:

PDF
 → Extract embedded images
 → Remove duplicates
 → Compress images
 → Final output


This file coordinates processing without owning logic.

🖼️ PDF Image Extraction (pdf_image_extract.py)

Uses PyMuPDF (fitz).

Opens PDF

Extracts embedded images only

No page rendering

Fast and memory-efficient

Server-safe

🧹 Duplicate Image Removal (image_dedupe.py)

Two-stage deduplication:

1. Exact duplicates

MD5 hash comparison

2. Near duplicates

Perceptual hash (pHash)

Removes visually similar images

Only unique images are retained.

📉 Image Compression (image_compress.py)

Uses Pillow

Compresses images to ≤ 300 KB

Multiple quality attempts

Resize fallback

Optional parallel processing

This module is a pure utility and imports nothing else.

🗂️ Output Folder Structure
Closure/
└── Assessor - Polygon Town Ref/
    └── CODE/
        └── FEATURE_ID/
            ├── image_1.jpg
            ├── image_2.jpg
            └── DOC_1/
                ├── raw/
                ├── unique/
                └── compressed/


Clear separation of:

Raw extracted images

Deduplicated images

Compressed final output

🧪 Validation Rules (conditions.py)

Validates:

Build Status

Siebel Reference

Whereabouts

Business rules are isolated from workflows.

✅ Production Readiness

✔ Pure Python
✔ No OS-level dependencies
✔ Headless compatible
✔ Deterministic Selenium interactions
✔ Modular & maintainable
✔ CI/CD and server friendly

🛠️ Requirements
selenium==4.16.0
requests==2.31.0
python-dotenv==1.0.0
webdriver-manager==4.0.1
pdf2image==1.17.0
Pillow==10.1.0
PyMuPDF==1.24.9
ImageHash==4.3.1
numpy
scipy

🧠 Mental Model (Simplified)
UI Automation
  ↓
Workflow Logic
  ↓
Media Download
  ↓
PDF Processing
  ↓
Image Cleanup
  ↓
Final Output


Each layer only communicates downward.
