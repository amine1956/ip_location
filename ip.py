from fastapi import FastAPI, Request
import requests
import uvicorn

app = FastAPI()

def get_client_ip(request: Request) -> str:
    # Attempt to retrieve the 'X-Envoy-External-Address' header
    client_ip = request.headers.get("X-Envoy-External-Address")

    # Fallback to 'client.host' if the header is absent or None
    if client_ip is None:
        client_ip = request.client.host

    return client_ip

def get_location(ip: str) -> dict:
    try:
        # Use ip-api.com to get location data for the IP address
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to retrieve location data"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/client-location")
async def client_location(request: Request):
    ip = get_client_ip(request)
    location_data = get_location(ip)
    return {"client_ip": ip, "location": location_data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
