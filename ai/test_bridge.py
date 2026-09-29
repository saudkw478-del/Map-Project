"""Self-test with a fake RCON server and a fake Claude API (no game / key needed)."""
import http.server, json, os, socket, struct, sys, tempfile, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

received = []
class FakeApi(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers["content-length"]); body = json.loads(self.rfile.read(n))
        assert self.headers["x-api-key"] == "test-key" and body["system"] and body["messages"][-1]["role"] == "user"
        received.append(body)
        out = json.dumps({"content": [{"type": "text", "text": "أيها المسافر، اتجه إلى الجدار قبل أن يحلّ الشتاء."}]}).encode()
        self.send_response(200); self.send_header("content-length", str(len(out))); self.end_headers(); self.wfile.write(out)
    def log_message(self, *a): pass
api = http.server.HTTPServer(("127.0.0.1", 0), FakeApi); threading.Thread(target=api.serve_forever, daemon=True).start()

commands = []
def rcon_server(sock):
    while True:
        c, _ = sock.accept()
        def serve(c=c):
            def rd(n):
                b = b""
                while len(b) < n:
                    x = c.recv(n - len(b))
                    if not x: raise EOFError
                    b += x
                return b
            def send(rid, t, body):
                p = struct.pack("<ii", rid, t) + body.encode() + b"\0\0"; c.sendall(struct.pack("<i", len(p)) + p)
            try:
                while True:
                    (ln,) = struct.unpack("<i", rd(4)); d = rd(ln); rid, t = struct.unpack("<ii", d[:8]); body = d[8:-2].decode()
                    if t == 3:
                        send(rid, 2, "") if body == "pw" else send(-1, 2, "")
                    else:
                        commands.append(body)
                        send(rid, 0, "#camp has 1" if "#camp" in body else ("x has 7" if "scoreboard" in body else ""))
            except Exception: pass
        threading.Thread(target=serve, daemon=True).start()
rs = socket.socket(); rs.bind(("127.0.0.1", 0)); rs.listen(5); threading.Thread(target=rcon_server, args=(rs,), daemon=True).start()

log = tempfile.NamedTemporaryFile("w", suffix=".log", delete=False, encoding="utf-8"); log.close()
os.environ.update(ANTHROPIC_API_KEY="test-key", RCON_PORT=str(rs.getsockname()[1]), RCON_PASSWORD="pw", LOG_PATH=log.name,
                  API_URL=f"http://127.0.0.1:{api.server_address[1]}/v1/messages", COOLDOWN_SEC="0")
import ai_bridge
b = ai_bridge.Bridge()
threading.Thread(target=b.run, daemon=True).start()
time.sleep(1.5)
with open(log.name, "a", encoding="utf-8") as f:
    f.write("[12:00:00] [Server thread/INFO]: <سعود> مرحبا بالجميع\n")            # ignored (no trigger)
    f.write("[12:00:01] [Server thread/INFO]: <سعود> !غراب وين أروح الحين؟\n"); f.flush()
time.sleep(2)
tell = [c for c in commands if c.startswith("tellraw")]
assert len(received) == 1, received
assert "سعود" in received[0]["messages"][-1]["content"], received[0]
assert tell and "\\u0627" in tell[0] and "dark_gray" in tell[0], tell
print("OK: 1 API call, tellraw sent:", tell[0][:120], "...")
print("state query issued:", [c for c in commands if c.startswith("scoreboard")][:2])
