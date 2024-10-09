from fastapi import FastAPI

app = FastAPI(title='Склад')


@app.get("/")
async def root():
    return {"message": "Hello World"}


