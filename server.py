from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse


class myHTTPServer(BaseHTTPRequestHandler):

	# GET
	def do_GET(self):

		url = urlparse.urlparse(self.path)
	
		if url.path != '/':
			self.send_response(404)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write(bytes("404. Not found", "utf8"))
			return
	
		self.send_response(200)
		
		self.send_header('Content-type','text/html')
		self.end_headers()

		message = str(url) + '<br>\n' + str(urlparse.parse_qs(url.query))
		self.wfile.write(bytes(message, "utf8"))
		return


def run():
	print('starting server...')
	server_address = ('', 8080)
	httpd = HTTPServer(server_address, myHTTPServer)
	print('running server...')
	httpd.serve_forever()


run()
