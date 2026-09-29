"""Minimal Minecraft RCON client (Source RCON protocol), standard library only.
Thread-safe (one lock) with automatic reconnect on the next command after a failure."""
import socket
import struct
import threading

SERVERDATA_AUTH = 3
SERVERDATA_EXECCOMMAND = 2


class RconError(Exception):
    pass


class Rcon:
    def __init__(self, host, port, password, timeout=10):
        self.host, self.port, self.password, self.timeout = host, port, password, timeout
        self.sock = None
        self._id = 0
        self._lock = threading.RLock()

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        rid = self._send(SERVERDATA_AUTH, self.password)
        while True:
            resp_id, _type, _body = self._recv()
            if _type == 2:                       # auth response
                if resp_id == -1:
                    raise RconError("RCON authentication failed (wrong password?)")
                return

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            finally:
                self.sock = None

    def command(self, cmd):
        with self._lock:
            try:
                if self.sock is None:
                    self.connect()
                rid = self._send(SERVERDATA_EXECCOMMAND, cmd)
                while True:
                    resp_id, _type, body = self._recv()
                    if resp_id == rid:
                        return body
            except (OSError, RconError):
                self.close()          # reconnect on the next call
                raise

    # -- wire format: int32 length, int32 id, int32 type, body\0, \0
    def _send(self, ptype, body):
        self._id += 1
        payload = struct.pack("<ii", self._id, ptype) + body.encode("utf-8") + b"\x00\x00"
        self.sock.sendall(struct.pack("<i", len(payload)) + payload)
        return self._id

    def _recv_exact(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise RconError("connection closed by the server")
            buf += chunk
        return buf

    def _recv(self):
        (length,) = struct.unpack("<i", self._recv_exact(4))
        data = self._recv_exact(length)
        rid, ptype = struct.unpack("<ii", data[:8])
        return rid, ptype, data[8:-2].decode("utf-8", "replace")
