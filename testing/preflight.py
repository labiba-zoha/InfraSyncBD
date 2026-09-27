# InfraSync BD Selenium preflight checker
# Run this BEFORE the Selenium tests.
# It checks the frontend, backend, database connection and all 4 test logins.

import json
import sys
import urllib.error
import urllib.request

FRONTEND = "http://localhost:5173"
BACKEND = "http://localhost:5000"
PASSWORD = "admin123"

ACCOUNTS = [
    ("Super Admin", "admin@infrasync.gov.bd"),
    ("Department Officer", "salman@rhd.gov.bd"),
    ("Contractor", "tariq@builder.com"),
    ("Citizen", "rahim@citizen.com"),
]


def get(url, timeout=4):
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.status, res.read().decode("utf-8", errors="replace")


def post_json(url, payload, timeout=5):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return res.status, res.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")


def fail(message):
    print("[FAIL]", message)
    return False


print("=" * 70)
print("INFRASYNC BD - PRETEST DIAGNOSTIC")
print("=" * 70)

all_ok = True

# 1. Frontend
try:
    status, body = get(FRONTEND + "/login")
    if status == 200 and "root" in body:
        print("[OK] Frontend is running on http://localhost:5173")
    else:
        all_ok = fail(f"Frontend returned HTTP {status}.") and all_ok
except Exception as exc:
    all_ok = fail(
        "Frontend is NOT reachable on port 5173. Start it with: npm run dev\n"
        f"       Details: {type(exc).__name__}: {exc}"
    ) and all_ok

# 2. Backend + DB
try:
    status, body = get(BACKEND + "/api/health")
    parsed = json.loads(body)
    if status == 200 and parsed.get("database") == "connected":
        print("[OK] Backend is running on http://localhost:5000")
        print("[OK] MySQL database connection works")
    else:
        all_ok = fail(f"Backend health failed: HTTP {status}: {body}") and all_ok
except urllib.error.HTTPError as exc:
    body = exc.read().decode("utf-8", errors="replace")
    all_ok = fail(f"Backend health failed: HTTP {exc.code}: {body}") and all_ok
except Exception as exc:
    all_ok = fail(
        "Backend is NOT reachable on port 5000. Start it with: cd server && node server.js\n"
        f"       Details: {type(exc).__name__}: {exc}"
    ) and all_ok

# 3. Actual API logins
print("\nChecking the four seeded logins...")
for role, email in ACCOUNTS:
    try:
        status, body = post_json(
            BACKEND + "/api/auth/login",
            {"email": email, "password": PASSWORD},
        )
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {}

        if status == 200 and parsed.get("success") is True:
            actual_role = (parsed.get("user") or {}).get("role")
            print(f"[OK] {role}: {email} -> role={actual_role}")
        else:
            msg = parsed.get("message", body)
            all_ok = fail(
                f"{role} login failed for {email}: HTTP {status}: {msg}"
            ) and all_ok
    except Exception as exc:
        all_ok = fail(
            f"Could not test {role} login: {type(exc).__name__}: {exc}"
        ) and all_ok

print("\n" + "=" * 70)
if all_ok:
    print("PRECHECK PASSED. Now run test1, test2 and test3.")
    sys.exit(0)
else:
    print("PRECHECK FAILED. Fix the item(s) above BEFORE Selenium.")
    sys.exit(1)
