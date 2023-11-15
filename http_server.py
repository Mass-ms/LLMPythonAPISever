import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
import function_calling

#HTTP Sever Address
ADDRESS = "127.0.0.1"
PORT = 8080

class MyHandler(BaseHTTPRequestHandler):
    
    def process_text(self,text):
        print("get text successfully")
        print(f"Processing:{text}")
        ptext = function_calling.run_conversation(text)
        print(f"Processed:{ptext}")
        return ptext
    
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")
        try:
            data = json.loads(body)
            text = data.get("text", None)
            if text is not None:
                result = self.process_text(text)
                response = {"status":"success", "message":"result"}
            else:
                response = {"status":"error", "message":"No text provided"}
        except json.JSONDecodeError:
            result = {"status":"error","error":"Invalid JSON"}
        
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(result.encode("utf-8"))
        
if __name__=="__main__":
    httpd = ThreadingHTTPServer(("localhost",8000),MyHandler)
    httpd.serve_forever()