from fastapi import APIRouter, HTTPException
from api.services.scrapers_registry import scrapers_registry

router = APIRouter(
    prefix="/data", tags=["data"]
)  # getting from csv, but we need to ajust it


@router.get("/{category}", summary="Fetch viticulture data from Embrapa")
def get_data_by_category(category: str):
    """
    Generic route that returns cleaned JSON data for a given category:
    - production
    - processing
    - commercialization
    - importation
    - exportation
    """
    scraper_class = scrapers_registry.get(category.lower())

    if scraper_class is None:
        raise HTTPException(status_code=404, detail="Invalid data category")

    scraper = scraper_class()
    data = scraper.get_json()  # CHANGE IF NECESSARY
    # considering that each scraper will have a method called get_json().

    if not data:
        raise HTTPException(
            status_code=503, detail="No data available or Embrapa unreachable"
        )

    return data
