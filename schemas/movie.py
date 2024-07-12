from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None # De esta manera se puede hacer un modo opcional para este parametro
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=150)
    year: int = Field(le=2022)
    rating: float = Field(le=10.0,ge=0)
    category: str = Field(min_length=5,max_length=15)
# Con este diccionario model_config se puede establecer el ejemplo de la informacion que debe llevar el body
    model_config = {
        "json_schema_extra": {
            "examples":[
                {
                "id":1,
                "title":"Mi pelicula",
                "overview":"Descripcion de la pelicula",
                "year":2022,
                "rating":9.8,
                "category":"Accion"}
            ]
        }
    }