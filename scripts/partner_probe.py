#!/usr/bin/env python3
"""Black-box partner contract + two concurrent bursts; only for fresh local test events."""
import argparse
import concurrent.futures
import json
import threading
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Web/API origin, no /api/partner suffix")
    parser.add_argument("--key", required=True)
    parser.add_argument("--events", nargs=2, required=True, metavar=("E4", "E5"))
    args = parser.parse_args()
    require(args.events[0] != args.events[1], "use two distinct events")
    base = args.base.rstrip("/") + "/api/partner"
    default = object()
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    opener = urllib.request.build_opener(NoRedirect())
    def call(path, method="GET", payload=None, key=default):
        headers = {"Accept": "application/json"}
        if key is default:
            key = args.key
        if key is not None:
            headers["X-Api-Key"] = key
        body = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            body = json.dumps(payload).encode()
        req = urllib.request.Request(base + path, data=body, headers=headers, method=method)
        try:
            with opener.open(req, timeout=15) as resp:
                status, raw = resp.status, resp.read()
        except urllib.error.HTTPError as exc:
            status, raw = exc.code, exc.read()
        try:
            return status, json.loads(raw)
        except (ValueError, UnicodeError):
            raise AssertionError(f"{method} {path}: non-JSON HTTP {status}") from None
    valid = {"buyerEmail":"probe@example.test","cardNumber":"4000000000000001"}
    bad = {"buyerEmail":"bad","cardNumber":"123"}
    missing = "00000000-0000-4000-8000-000000000000"
    for key in (None, args.key + "-invalid"):
        for path, method, payload in (("/events","GET",None),(f"/events/{missing}/purchases","POST",bad),(f"/tickets/{missing}","GET",None)):
            require(call(path, method, payload, key) == (401,{"error":"unauthorized"}), f"auth precedence {path}")
    require(call(f"/events/{missing}/purchases","POST",bad) == (422,{"error":"invalid_request"}), "invalid_request precedence")
    require(call(f"/events/{missing}/purchases","POST",valid) == (404,{"error":"event_not_available"}), "missing event")
    require(call(f"/tickets/{missing}") == (404,{"error":"ticket_not_found"}), "missing ticket")
    def events():
        status, body = call("/events")
        require(status == 200 and isinstance(body,list), "events must be 200 array")
        for row in body:
            require(set(row) == {"id","name","startsAt","priceCents","availableSeats"}, "event fields")
            require(isinstance(row["id"],str) and isinstance(row["name"],str), "event strings")
            dt = datetime.fromisoformat(row["startsAt"].replace("Z","+00:00"))
            require(dt.tzinfo is not None, "startsAt timezone")
            require(type(row["priceCents"]) is int and row["priceCents"] > 0, "priceCents")
            require(type(row["availableSeats"]) is int and row["availableSeats"] >= 0, "availableSeats")
        return {row["id"]:row for row in body}
    for event_id in args.events:
        e = events().get(event_id)
        require(e is not None and e["availableSeats"] == 5, f"{event_id}: needs five available seats")
        barrier = threading.Barrier(30, timeout=15)
        def buy(i):
            barrier.wait()
            start = time.monotonic()
            response = call(f"/events/{event_id}/purchases","POST",{**valid,"buyerEmail":f"load-{i}@example.test"})
            return start, response
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as pool:
            results = list(pool.map(buy, range(30)))
        counts = Counter(status for _,(status,_) in results)
        print(f"{event_id}: {dict(sorted(counts.items()))}")
        require(counts == Counter({202:5,409:25}), f"incorrect concurrency histogram: {counts}")
        tickets = {}
        codes = set()
        for started,(status,body) in results:
            if status == 409:
                require(body == {"error":"sold_out"}, "sold_out payload")
            else:
                require(set(body) == {"ticketId","code","status"} and body["status"] == "pending", "purchase shape/pending")
                require(isinstance(body["ticketId"],str) and isinstance(body["code"],str) and body["code"], "ticket ID/code")
                require(body["ticketId"] not in tickets and body["code"] not in codes, "duplicate code or ticket ID")
                tickets[body["ticketId"]] = (started,body["code"])
                codes.add(body["code"])
        require(events()[event_id]["availableSeats"] == 0, "capacity not exhausted")
        require(call(f"/events/{event_id}/purchases","POST",bad) == (422,{"error":"invalid_request"}), "payload before sold out")
        pending = set(tickets)
        deadline = min(start for start,_ in tickets.values()) + 10.0
        while pending and time.monotonic() <= deadline:
            for tid in list(pending):
                status, body = call(f"/tickets/{tid}")
                require(status == 200 and set(body) == {"ticketId","code","eventId","status","checkedIn"}, "ticket shape")
                require(body["ticketId"] == tid and body["eventId"] == event_id and body["code"] == tickets[tid][1] and body["checkedIn"] is False, "ticket data mismatch")
                require(body["status"] in ("pending","confirmed"), "unexpected state for approved card")
                if body["status"] == "confirmed":
                    pending.remove(tid)
            if pending:
                time.sleep(0.1)
        require(not pending and time.monotonic() <= deadline, f"confirmation deadline exceeded: {pending}")
        print(f"PASS {event_id}: 5 confirmed, 0 available, 25 sold_out")
    print("PASS probe; UI, precise gateway windows and full integrated flow remain separate gates.")

if __name__ == "__main__":
    main()
