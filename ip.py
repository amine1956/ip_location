from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Liste globale pour stocker les données des utilisateurs
user_data = []

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

# Route unique pour afficher la carte et la liste des utilisateurs
@app.get("/users", response_class=HTMLResponse)
async def client_location(request: Request):

    return templates.TemplateResponse("map.html", {"request": request,"users": user_data})
@app.get("/", response_class=HTMLResponse)
async def game(request: Request):
    ip = get_client_ip(request)
    location_data = get_location(ip)

    # Ajout des données de l'utilisateur à la liste globale
    user_info = {
        "ip": ip,
        "city": location_data.get("city", "Unknown"),
        "country": location_data.get("country", "Unknown"),
        "lat": location_data.get("lat", "Unknown"),
        "lon": location_data.get("lon", "Unknown"),
    }

    user_data.append(user_info)  # Ajouter les données à la liste globale
    print(user_data)
    return templates.TemplateResponse("index.html", {"request": request, "users": user_data})





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
