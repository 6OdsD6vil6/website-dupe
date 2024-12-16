from http.server import BaseHTTPRequestHandler, HTTPServer  
import logging

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Log the client's IP address  
        ip_address = self.client_address[0]
        print(f"Visitor IP: {ip_address}")

        # You can serve the cloned website here  
        try:
            with open('index.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, 'File Not Found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
