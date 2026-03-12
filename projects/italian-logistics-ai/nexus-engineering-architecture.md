# NEXUS Engine MVP: Engineering Architecture Prototype

This document outlines the initial engineering plan for the "Italian Logistics AI Dispatcher" (NEXUS Engine) that we are selling on `logistics.autoflow-solutions.com`. 

The goal is to build an MVP (Minimum Viable Product) that delivers on our core promises: zero manual paperwork, automated WhatsApp dispatching, and optimized regional routing (ZTL/historical centers considered).

## Core Architecture Overview

The system will act as an intelligent layer between the Dispatcher, the Driver, and the Client, utilizing common communication channels (WhatsApp) combined with a smart routing backend.

### 1. The Dispatcher Interface (Web Dashboard)
- **Role:** Central command center for the fleet manager.
- **Tech Stack:** Next.js (React), Tailwind CSS, TypeScript.
- **Features:**
  - Drag-and-drop daily load uploading (CSV/Excel or ERP integration).
  - Visual map showing live truck locations and active routes.
  - "Magic Button": 'Generate Optimal Routes' which triggers the AI backend.
  - Exception handling (e.g., driver reports a traffic jam, system recalculates).

### 2. The AI Routing Engine (Backend)
- **Role:** The brain. Solves the complex Vehicle Routing Problem (VRP) specifically tuned for Italian geography.
- **Tech Stack:** Python (FastAPI), PostgreSQL (PostGIS for spatial data), Google OR-Tools or Valhalla (open-source routing engine).
- **Features:**
  - Ingests delivery points, time windows, and truck capacities.
  - Calculates routes avoiding known ZTLs (Zone a Traffico Limitato) and narrow historical centers where applicable.
  - Outputs the most fuel and time-efficient sequence for each truck.

### 3. The Driver Interface (WhatsApp Bot)
- **Role:** Frictionless communication for drivers. No app installation required.
- **Tech Stack:** Twilio (WhatsApp API), LangChain/LLM (for parsing natural language).
- **Features:**
  - Morning Dispatch: Sends a WhatsApp message with the day's optimized route sequence and Google Maps links.
  - Automated Check-ins: Driver replies "Consegnato" (Delivered) or sends a photo of the signed BOL (Bill of Lading).
  - Issue Reporting: Driver texts "Traffico in tangenziale" -> LLM parses intent -> alerts dispatcher dashboard -> optionally triggers route recalculation.

### 4. The Client Interface (Tracking Link)
- **Role:** Eliminates the "Where is my truck?" phone calls.
- **Tech Stack:** Serverless functions, simple mobile-friendly web view.
- **Features:**
  - SMS/Email to the receiving client containing a tracking link (similar to Amazon/Uber).
  - Shows dynamic ETA based on the truck's current position and traffic.

## Phased Development Approach

**Phase 1: Core Automated MVP (Days 1 - 30)**
*Focus on building the real automation foundations immediately.*
- Build the Dispatcher Dashboard UI (Next.js).
- Implement a simplified routing engine using existing APIs (like Google Maps Route Optimization API) to get functional, automated routing without the complexity of a custom VRP solver right away.
- Set up Twilio to send automated WhatsApp messages.
- Hook up a basic LLM to parse standard driver replies (e.g., "Consegnato") and update the dashboard automatically.
- *Goal:* Secure the first paying client by showing them a functional, end-to-end automated system.

**Phase 2: Advanced Routing Engine (Days 30 - 60)**
*Upgrading the brain of the operation.*
- Transition from basic APIs to Google OR-Tools or Valhalla to solve complex Vehicle Routing Problems (VRP) in-house.
- Add constraints specifically for Italian geography (ZTLs, narrow roads, bridge heights).
- Implement dynamic route recalculation based on real-time traffic or exceptions.

**Phase 3: Deep Customization & Scale (Days 60+)**
*Tailoring and optimizing at scale.*
- Integrate custom map layers for granular control over historical centers.
- Implement predictive loading/unloading times based on historical data.

---
*Prepared by the Engineering Team.*
