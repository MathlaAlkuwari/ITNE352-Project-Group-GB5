import socket
import json
import os
from fetcher import get_cat_fact
HOST = "127.0.0.1"
PORT = 5000
# we will start by creating folder for json result if it doesnt exist
if not os.path.exist("results"):
  os.makedirs("result")
  server= socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
  server.bind((HOST, PORT))
  server.listen(1)
  print(f"server is running on {HOST}:{PORT}")
  while True :
    conn , addr = server.accept()
    print("client connected: ", addr)
    msg = conn.rcv(1024).decode()
    print("client says: ", msg)
    if msg == 1 
    # clients want cat fact
    fact= get_cat_fact()
    # save to json file
data = {"fact" : fact}
with open(" result/cat_fact.json" ,"w") as f :
  json.dump(data , f , indent=4)
  conn.send(fact.encode())
elif msg == "2" : 
# client wants to exist 
conn.send("goodbye!".encode())
else:
conn.send("invalid option.".encode())
conn.close()

  
