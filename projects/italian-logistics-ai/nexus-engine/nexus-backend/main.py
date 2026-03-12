from fastapi import FastAPI, Depends, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn

import database
import models
import schemas
from services.google_maps import google_maps_service
from services.twilio_whatsapp import twilio_service
from services.openai_task_parser import openai_parser
from fastapi import Form, UploadFile, File
import csv
import io

# Create all database tables based on models
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="NEXUS Engine AI Dispatcher API", version="1.0.0")

# Enable CORS for the local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthCheckResponse(BaseModel):
    status: str
    message: str

@app.get("/", response_model=HealthCheckResponse)
def read_root():
    return HealthCheckResponse(status="ok", message="NEXUS Engine Backend is running.")

@app.get("/health", response_model=HealthCheckResponse)
def health_check(db: Session = Depends(database.get_db)):
    db_status = "Connected" if db else "Disconnected"
    return HealthCheckResponse(status="ok", message=f"Healthy - DB: {db_status}")

@app.post("/dispatch/{truck_id}")
def dispatch_to_driver(truck_id: str, db: Session = Depends(database.get_db)):
    """
    Workflow B: The Automated Dispatch
    Sends the optimized route stops to the driver via WhatsApp.
    """
    truck = db.query(models.Truck).filter(models.Truck.id == truck_id).first()
    if not truck:
        return {"error": "Truck not found"}
    
    # Placeholder for actual route fetching logic
    message = f"Buongiorno {truck.driver_name}. Ecco il tuo giro di oggi..."
    result = twilio_service.send_whatsapp_message(truck.driver_phone, message)
    return {"status": "dispatched", "twilio_result": result}

@app.post("/upload-deliveries")
async def upload_deliveries(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    """
    Dispatcher uploads a CSV of the day's deliveries.
    Format: client_name, address, time_window_start, time_window_end
    """
    contents = await file.read()
    decoded = contents.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))
    
    new_deliveries = []
    for row in reader:
        delivery = models.Delivery(
            client_name=row.get('client_name'),
            address=row.get('address'),
            # In a production app, we'd geocode the address here or in the background
            lat=float(row.get('lat', 0)), 
            lng=float(row.get('lng', 0)),
            status=models.DeliveryStatus.PENDING
        )
        db.add(delivery)
        new_deliveries.append(delivery)
    
    db.commit()
    return {"status": "success", "count": len(new_deliveries)}

@app.post("/optimize")
def run_optimization(db: Session = Depends(database.get_db)):
    """
    Workflow A: Daily Load Upload & Optimization
    Hits the Google Maps API to sequence PENDING deliveries.
    """
    pending = db.query(models.Delivery).filter(models.Delivery.status == models.DeliveryStatus.PENDING).all()
    trucks = db.query(models.Truck).all()
    
    if not pending or not trucks:
        return {"error": "No pending deliveries or trucks available"}
    
    # Simple assignment logic for MVP: Assign all to first truck
    truck = trucks[0]
    waypoints = [d.address for d in pending]
    
    # Real optimization call
    # Note: Need real API key to avoid error
    opt_result = google_maps_service.optimize_route(
        origin="Milano, Italy", # Dummy depot
        destination="Milano, Italy",
        waypoints=waypoints
    )
    
    return {
        "status": "optimized", 
        "truck": truck.license_plate, 
        "sequence": opt_result
    }

@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    db: Session = Depends(database.get_db)
):
    """
    Workflow C: The AI-Parsed Reply
    Receives messages from Twilio, parses them with AI, and updates the database.
    """
    # 1. Identify driver by phone number
    # Twilio From is in format "whatsapp:+39..."
    phone_number = From.replace("whatsapp:", "")
    truck = db.query(models.Truck).filter(models.Truck.driver_phone == phone_number).first()
    
    if not truck:
        return {"status": "error", "message": "Driver not found"}

    # 2. Extract intent using OpenAI
    # In a full impl, we'd fetch the active route context here
    parse_result = openai_parser.parse_driver_reply(Body, context=f"Driver: {truck.driver_name}, Truck ID: {truck.id}")
    
    # 3. Handle result (Mocking the DB update for the MVP logic)
    if "new_status" in parse_result:
        # Here we would update the delivery entry in models.Delivery
        return {
            "status": "success",
            "parsed": parse_result,
            "message": f"Updated status to {parse_result['new_status']}"
        }
    
    return {"status": "unrecognized", "raw_message": Body}

@app.post("/seed")
def seed_data(db: Session = Depends(database.get_db)):
    """
    Utility endpoint to populate sample data for testing.
    """
    # Create a test truck
    test_truck = models.Truck(
        license_plate="AA123BB",
        driver_name="Marco Rossi",
        driver_phone="+393331234567",
        capacity_kg=1500.0
    )
    db.add(test_truck)
    
    # Create sample deliveries
    deliveries = [
        models.Delivery(client_name="Centro Edile", address="Via Roma 1, Milano", lat=45.4642, lng=9.1900),
        models.Delivery(client_name="Ferramenta Bianchi", address="Corso Buenos Aires 10, Milano", lat=45.4781, lng=9.2106)
    ]
    for d in deliveries:
        db.add(d)
        
    db.commit()
    return {"message": "Sample data seeded", "truck_id": test_truck.id}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
