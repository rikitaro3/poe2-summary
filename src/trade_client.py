import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import time

class TradeClient:
    def __init__(self, league="Runes of Aldur", session_id=None, poe_token=None):
        self.league = league
        self.session_id = session_id or os.environ.get("POESESSID") or self._load_env_var("POESESSID")
        self.poe_token = poe_token or os.environ.get("POETOKEN") or self._load_env_var("POETOKEN")

    def _load_env_var(self, name):
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip() and not line.startswith("#"):
                            parts = line.strip().split("=", 1)
                            if len(parts) == 2 and parts[0].strip() == name:
                                return parts[1].strip().strip('"').strip("'")
            except Exception:
                pass
        return None

    def check_rate_limits(self, limit_hdr, state_hdr):
        try:
            limits = limit_hdr.split(",")
            states = state_hdr.split(",")
            for limit, state in zip(limits, states):
                l_parts = limit.split(":")
                s_parts = state.split(":")
                if len(l_parts) == 3 and len(s_parts) == 3:
                    max_req = int(l_parts[0])
                    time_window = int(l_parts[1])
                    cur_req = int(s_parts[0])
                    penalty = int(s_parts[2])
                    
                    if penalty > 0:
                        print(f"⚠️ Rate limit cooldown active: sleeping for {penalty} seconds.", file=sys.stderr)
                        time.sleep(penalty + 1)
                    elif cur_req >= max_req * 0.8:
                        sleep_time = max(1, int(time_window * 0.5))
                        print(f"⚠️ Rate limit warning ({cur_req}/{max_req} used for {time_window}s window). Safe-sleeping for {sleep_time} seconds...", file=sys.stderr)
                        time.sleep(sleep_time)
        except Exception:
            pass

    def send_request(self, query, max_retries=3):
        encoded_league = urllib.parse.quote(self.league)
        url = f"https://www.pathofexile.com/api/trade2/search/{encoded_league}"
        
        headers = {
            "User-Agent": "PoE2TradeHelper/1.0 (Contact: user-local-script)",
            "Content-Type": "application/json"
        }
        if self.session_id:
            headers["Cookie"] = f"POESESSID={self.session_id}"
        elif self.poe_token:
            headers["Authorization"] = f"Bearer {self.poe_token}"

        for attempt in range(max_retries):
            req = urllib.request.Request(
                url,
                data=json.dumps(query).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            try:
                with urllib.request.urlopen(req) as response:
                    limit_hdr = response.headers.get("X-Rate-Limit-Ip")
                    state_hdr = response.headers.get("X-Rate-Limit-Ip-State")
                    if limit_hdr and state_hdr:
                        self.check_rate_limits(limit_hdr, state_hdr)
                    
                    res_data = json.loads(response.read().decode("utf-8"))
                    search_id = res_data.get("id")
                    return f"https://www.pathofexile.com/trade2/search/{encoded_league}/{search_id}"
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    retry_after = e.headers.get("Retry-After")
                    wait_time = int(retry_after) if retry_after else 10
                    state_hdr = e.headers.get("X-Rate-Limit-Ip-State")
                    if state_hdr:
                        penalty_times = []
                        for state in state_hdr.split(","):
                            parts = state.split(":")
                            if len(parts) == 3:
                                penalty_times.append(int(parts[2]))
                        max_penalty = max(penalty_times) if penalty_times else 0
                        if max_penalty > 0:
                            wait_time = max(wait_time, max_penalty)
                    
                    print(f"⚠️ Rate limit hit (HTTP 429). Waiting for {wait_time} seconds before retry (Attempt {attempt+1}/{max_retries})...", file=sys.stderr)
                    time.sleep(wait_time + 1)
                    continue
                else:
                    raise e
        raise RuntimeError("Max retries exceeded due to rate limit (HTTP 429)")
