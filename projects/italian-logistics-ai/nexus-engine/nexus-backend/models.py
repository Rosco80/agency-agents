from sqlalchemy import Column, String, Float, DateTime, Enum, ForeignKey, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from database import Base
from datetime import datetime

# Helper function to generate UUIDs as strings if using SQLite fallback, 
# but technically schema design is geared toward PG.
def generate_uuid():
    return str(uuid.uuid4())

class DeliveryStatus(str, enum.Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"

class RouteStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class Truck(Base):
    __tablename__ = "trucks"

    id = Column(String, primary_key=True, default=generate_uuid)
    license_plate = Column(String, unique=True, index=True)
    driver_name = Column(String)
    driver_phone = Column(String) # E.164 format for WhatsApp
    capacity_kg = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)

    routes = relationship("Route", back_populates="truck")

class Route(Base):
    __tablename__ = "routes"

    id = Column(String, primary_key=True, default=generate_uuid)
    truck_id = Column(String, ForeignKey("trucks.id"))
    date = Column(Date)
    status = Column(Enum(RouteStatus), default=RouteStatus.PLANNED)
    estimated_distance_km = Column(Float, default=0.0)

    truck = relationship("Truck", back_populates="routes")
    deliveries = relationship("Delivery", back_populates="route")

class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(String, primary_key=True, default=generate_uuid)
    client_name = Column(String, index=True)
    address = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    time_window_start = Column(DateTime, nullable=True)
    time_window_end = Column(DateTime, nullable=True)
    status = Column(Enum(DeliveryStatus), default=DeliveryStatus.PENDING)
    route_id = Column(String, ForeignKey("routes.id"), nullable=True)
    
    # Metadata for sequence if assigned
    route_sequence = Column(Float, nullable=True) 

    route = relationship("Route", back_populates="deliveries")
