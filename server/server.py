from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import socketserver


PORT = 8080
handler = SimpleHTTPRequestHandler


class CustomServer(BaseHTTPRequestHandler):

    SUPPORTED_EXTENSIONS = (".css", ".html")

    def do_GET(self):

        # Find file type being requested
        file_type = self.get_file_type()
        if file_type not in self.SUPPORTED_EXTENSIONS:
            self.send_response(404, "Not Found")
            return
        

    def get_file_type(self):
        pass


if __name__ == "__main__":
    webServer = HTTPServer(("", PORT), CustomServer)
    print("server started")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()
        print("Server stopped.")
