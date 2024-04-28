from datetime import date

from pydantic import BaseModel


class PlantCreate(BaseModel):
    plant_name: str
    reference_humidity: float
    reference_temperature: float
    reference_minerals: float


class MeasurementCreate(BaseModel):
    plant_name: str
    date: date
    soil_moisture_content: float
    temperature_conditions: float
    amount_of_mineral_substance: float
