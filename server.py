import socket
import json
import os
import urllib.request
import urllib.error

HOST = "127.0.0.1"
PORT = 5000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR , exist_ok= True)

def get_cat_fact(): 
  """Fetch a random cat fact from the public API (no requests needed)."""
url = "http://catfact.ninja/fact"
try:
  with urllib.request.urlopen(url,timeout=5) as response: 
  dara = json.loads(response.read().decode("utf-8"))
  return data.get("fact", "no fact found") 
except (urllib.error.URLError , json.JSONDecodeError , TimeoutError) as e:
  return f"Error fetching cat fact : {e}"
except Exception as e: 
  return f"Error fetching cat face: {e}"
