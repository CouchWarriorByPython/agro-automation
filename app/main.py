from datetime import date
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import SessionLocal, create_db_and_tables
from .models import PlantBenchmark, PlantCorrections, PlantDailyMeasurements
from .schemas import MeasurementCreate, PlantCreate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/html/index.html")

@app.post("/add-plant", response_model=PlantCreate)
async def add_plant(plant_data: PlantCreate, db: Session = Depends(get_db)):
    plant_name_lower = plant_data.plant_name.lower()
    existing_plant = db.query(PlantBenchmark).filter(PlantBenchmark.plant_name == plant_name_lower).first()
    if existing_plant:
        raise HTTPException(status_code=400, detail=f"Plant with name '{plant_data.plant_name}' already exists.")
    new_plant = PlantBenchmark(
        plant_name=plant_name_lower,
        reference_humidity=plant_data.reference_humidity,
        reference_temperature=plant_data.reference_temperature,
        reference_minerals=plant_data.reference_minerals
    )
    db.add(new_plant)
    db.commit()
    return new_plant


@app.post("/daily-plant-data", response_model=MeasurementCreate)
async def add_measurement(
    measurement_data: MeasurementCreate, db: Session = Depends(get_db)
):
    plant_name_lower = measurement_data.plant_name.lower()
    plant = db.query(PlantBenchmark).filter(PlantBenchmark.plant_name == plant_name_lower).first()
    if not plant:
        raise HTTPException(status_code=400, detail=f"Plant name '{measurement_data.plant_name}' not found in the database.")

    measurement_data_dict = measurement_data.model_dump()
    measurement_data_dict["plant_name"] = plant_name_lower
    db_measurement = PlantDailyMeasurements(**measurement_data_dict)
    db.add(db_measurement)
    db.commit()

    correction_data = {
        "plant_name": plant_name_lower,
        "date": measurement_data.date or date.today(),
        "soil_moisture_content": plant.reference_humidity - measurement_data.soil_moisture_content,
        "amount_of_mineral_substance": plant.reference_minerals - measurement_data.amount_of_mineral_substance,
        "temperature_conditions": plant.reference_temperature - measurement_data.temperature_conditions,
    }
    db_correction = PlantCorrections(**correction_data)
    db.add(db_correction)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Failed to add correction data: {e}")
        raise HTTPException(status_code=500, detail="Failed to add correction data.")

    return db_measurement


def serialize(data):
    return [item.__dict__ for item in data]

@app.get("/data/humidity")
async def get_humidity_data(db: Session = Depends(get_db)):
    daily_measurements = db.query(
        PlantDailyMeasurements.date,
        PlantDailyMeasurements.soil_moisture_content
    ).order_by(PlantDailyMeasurements.date).all()
    corrections = db.query(
        PlantCorrections.date,
        PlantCorrections.soil_moisture_content
    ).order_by(PlantCorrections.date).all()
    return {
        "daily_measurements": [m._asdict() for m in daily_measurements],
        "corrections": [c._asdict() for c in corrections]
    }

@app.get("/data/minerals")
async def get_minerals_data(db: Session = Depends(get_db)):
    daily_measurements = db.query(
        PlantDailyMeasurements.date,
        PlantDailyMeasurements.amount_of_mineral_substance
    ).order_by(PlantDailyMeasurements.date).all()
    corrections = db.query(
        PlantCorrections.date,
        PlantCorrections.amount_of_mineral_substance
    ).order_by(PlantCorrections.date).all()
    return {
        "daily_measurements": [m._asdict() for m in daily_measurements],
        "corrections": [c._asdict() for c in corrections]
    }

@app.get("/data/temperature")
async def get_temperature_data(db: Session = Depends(get_db)):
    daily_measurements = db.query(
        PlantDailyMeasurements.date,
        PlantDailyMeasurements.temperature_conditions
    ).order_by(PlantDailyMeasurements.date).all()
    corrections = db.query(
        PlantCorrections.date,
        PlantCorrections.temperature_conditions
    ).order_by(PlantCorrections.date).all()
    return {
        "daily_measurements": [m._asdict() for m in daily_measurements],
        "corrections": [c._asdict() for c in corrections]
    }

app.mount("/static/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/static/html", StaticFiles(directory="frontend/html"), name="html")
app.mount("/static/js", StaticFiles(directory="frontend/js"), name="js")
