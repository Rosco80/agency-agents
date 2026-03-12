from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models import DeliveryStatus, RouteStatus
import uuid

# Base Schemas (Shared Properties)
class TruckBase(BaseModel):
    license_plate: str
    driver_name: str
    driver_phone: str
    capacity_kg: Optional[float] = 0.0

class RouteBase(BaseModel):
    truck_id: str
    date: datetime
    estimated_distance_km: Optional[float] = 0.0

class DeliveryBase(BaseModel):
    client_name: str
    address: str
    lat: float
    lng: float
    time_window_start: Optional[datetime] = None
    time_window_end: Optional[datetime] = None
    route_id: Optional[str] = None
    route_sequence: Optional[float] = None

# Create Schemas (For incoming requests)
class TruckCreate(TruckBase):
    pass

class RouteCreate(RouteBase):
    pass

class DeliveryCreate(DeliveryBase):
    pass

# Read Schemas (For sending responses)
class Delivery(DeliveryBase):
    id: str
    status: DeliveryStatus

    class Config:
        from_attributes = True

class Route(RouteBase):
    id: str
    status: RouteStatus
    deliveries: List[Delivery] = []

    class Config:
        from_attributes = True

class Truck(TruckBase):
    id: str
    is_active: bool
    routes: List[Route] = []

    class Config:
        from_attributes = True
