from fastapi import FastAPI

app = FastAPI()
app.title = "Mi primera api con FastAPI"
app.version = "0.0.1"

@app.get("/",tags=["Home"])
def message():
  return "Hola mundo"