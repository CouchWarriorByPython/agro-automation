from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import inspect

Base = declarative_base()

def as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


class PlantBenchmark(Base):
    __tablename__ = "plant_benchmark"

    plant_name = Column(String, primary_key=True)
    reference_humidity = Column(Float)
    reference_minerals = Column(Float)
    reference_temperature = Column(Float)

    def as_dict(self):
        return as_dict(self)


class PlantDailyMeasurements(Base):
    __tablename__ = "plant_daily_measurements"

    id = Column(Integer, primary_key=True)
    plant_name = Column(String, ForeignKey("plant_benchmark.plant_name"))
    date = Column(Date)
    soil_moisture_content = Column(Float)
    amount_of_mineral_substance = Column(Float)
    temperature_conditions = Column(Float)
    plant = relationship("PlantBenchmark", back_populates="daily_measurements")

    def as_dict(self):
        return as_dict(self)

class PlantCorrections(Base):
    __tablename__ = "plant_corrections"

    id = Column(Integer, primary_key=True)
    plant_name = Column(String, ForeignKey("plant_benchmark.plant_name"))
    date = Column(Date)
    soil_moisture_content = Column(Float)
    amount_of_mineral_substance = Column(Float)
    temperature_conditions = Column(Float)
    plant = relationship("PlantBenchmark", back_populates="corrections")

    def as_dict(self):
        return as_dict(self)

PlantBenchmark.daily_measurements = relationship(
    "PlantDailyMeasurements", order_by=PlantDailyMeasurements.id, back_populates="plant"
)
PlantBenchmark.corrections = relationship(
    "PlantCorrections", order_by=PlantCorrections.id, back_populates="plant"
)
