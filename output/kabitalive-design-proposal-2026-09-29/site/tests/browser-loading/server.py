from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import ssl,json,os
os.chdir('/private/tmp/kbl-loading080')
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if self.path.endswith('runtime-config.json'):
   data=json.dumps({'firebase':{'enabled':True,'projectId':'kabita-live','apiKey':'synthetic-key','authDomain':'demo.example.invalid','appId':'synthetic-app','allowedHosts':['127.0.0.1']},'engagement':{'likes':'likes.html' in self.headers.get('Referer',''),'publicComments':True}}).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
  else:super().do_GET()
s=ThreadingHTTPServer(('127.0.0.1',8940),Handler);ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);ctx.load_cert_chain('/private/tmp/kbl-cert080.pem','/private/tmp/kbl-key080.pem');s.socket=ctx.wrap_socket(s.socket,server_side=True);s.serve_forever()
