from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Directory for HTML templates

def get_client_ip(request: Request) -> str:
    client_ip = request.headers.get("X-Envoy-External-Address")
    if client_ip is None:
        client_ip = request.client.host
    return client_ip

def get_location(ip: str) -> dict:
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to retrieve location data"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
async def client_location(request: Request):
    ip = get_client_ip(request)
    location_data = get_location(ip)
    print(location_data)  # Affiche les données pour débogage
    return templates.TemplateResponse("map.html", {"request": request, "location": location_data})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
