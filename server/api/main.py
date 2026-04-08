from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Agent Protocol Server Running"}

@app.post("/message")
async def receive_message(req: Request):
    data = await req.json()
    print("Received:", data)
    return {"status": "received"}