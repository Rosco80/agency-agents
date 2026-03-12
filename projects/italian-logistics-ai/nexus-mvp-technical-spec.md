# NEXUS Engine MVP: Phase 1 Technical Specification

This document provides the foundational engineering blueprint for **Phase 1: Core Automated MVP**. It translates the business requirements of the Italian Logistics AI Campaign into a concrete technical plan for developers.

## 1. Tech Stack Selection
*   **Frontend (Dispatcher Dashboard):** Next.js (App Router), React, Tailwind CSS, Shadcn UI (for fast component development).
*   **Backend & API:** Python (FastAPI) - Chosen for its strong integration with data processing libraries and LLM ecosystems.
*   **Database:** PostgreSQL with PostGIS (for spatial/location queries), managed via Supabase or Render for speed.
*   **Third-Party APIs:**
    *   **Routing:** Google Maps Route Optimization API (provides enterprise grade sequencing out of the box).
    *   **Communication:** Twilio API for WhatsApp Business Messaging.
    *   **LLM Parsing:** OpenAI API (GPT-4o-mini is cost-effective and perfectly suited for parsing short Italian text replies).

## 2. Core Entities & Database Schema

We will start with a lean relational schema.

### `trucks` Table
The vehicles available for dispatch.
*   `id` (UUID, Primary Key)
*   `license_plate` (String)
*   `driver_name` (String)
*   `driver_phone` (String, E.164 format for WhatsApp)
*   `capacity_kg` (Decimal)

### `deliveries` Table
The daily stops uploaded by the dispatcher.
*   `id` (UUID, Primary Key)
*   `client_name` (String)
*   `address` (String)
*   `lat` (Decimal)
*   `lng` (Decimal)
*   `time_window_start` (DateTime)
*   `time_window_end` (DateTime)
*   `status` (Enum: `PENDING`, `ASSIGNED`, `DELIVERED`, `FAILED`)
*   `route_id` (UUID, Foreign Key)

### `routes` Table
The generated set of stops for a truck on a specific day.
*   `id` (UUID, Primary Key)
*   `truck_id` (UUID, Foreign Key)
*   `date` (Date)
*   `status` (Enum: `PLANNED`, `IN_PROGRESS`, `COMPLETED`)
*   `estimated_distance_km` (Decimal)

---

## 3. The Core Developer Workflows (User Journeys)

### Workflow A: Daily Load Upload & Optimization
1.  **Dispatcher Action:** Disptacher uploads a CSV of the day's deliveries `(client, address, time window)` into the Next.js dashboard.
2.  **API Action:** FastAPI backend parses the CSV and saves `deliveries` as `PENDING`.
3.  **Optimization Call:** The backend formats the delivery locations and active trucks into a JSON payload and sends it to the **Google Maps Route Optimization API**.
4.  **Result Processing:** Google returns the optimal sequence assigning stops to specific trucks. The FastAPI backend creates `routes`, updates the `deliveries` table with their assigned sequence, and pushes the data back to the Next.js dashboard for the dispatcher to review.

### Workflow B: The Automated Dispatch
1.  **Dispatcher Action:** Clicks "Approve & Dispatch" on the dashboard.
2.  **Twilio Action:** FastAPI backend generates a WhatsApp message template for each driver.
    *   *Example:* "Buongiorno Marco. Ecco il tuo giro di oggi: 1. Centro Edile (Via Roma) 2. Ferramenta Rossi (Corso Milano)... Rispondi 'Consegnato 1' quando finisci la prima fermata."
3.  **Twilio API:** Sends the messages to the drivers' phones via WhatsApp.

### Workflow C: The AI-Parsed Reply
1.  **Driver Action:** Driver types "Finito al centro edile, c'era un po' di coda" (Finished at the construction center, there was a bit of a queue) and sends it over WhatsApp to our Twilio number.
2.  **Twilio Webhook:** Twilio immediately forwards this text to our FastAPI webhook endpoint.
3.  **LLM Parsing:** Our backend sends the raw text and the driver's current active route context to OpenAI (GPT-4o-mini).
    *   *System Prompt:* "You are a logistics parser. Extract the status update from the following driver message. Reply ONLY with a JSON object containing `delivery_id` and `new_status`."
4.  **Database Update:** The LLM correctly identifies the intent as `DELIVERED` for stop 1. The backend updates the database. The Next.js dashboard (polling or via WebSockets) updates to show a green checkmark next to the delivery in real-time.

---

## Next Steps for the Engineering Team
1.  **Repository Setup:** Initialize the GitHub repositories for `nexus-frontend` (Next.js) and `nexus-backend` (FastAPI).
2.  **Infrastructure:** Spin up the PostgreSQL database (e.g., on Supabase).
3.  **API Keys:** Secure sandbox API keys for Google Maps Route Optimization, Twilio WhatsApp, and OpenAI.
4.  **Sprint 1 Goal:** Build Workflow A (upload CSV -> hit Google API -> Display routes on a rudimentary map).
