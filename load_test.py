"""SmartParcel concurrent load test - Khalid 20200001899.
Run in AWS CloudShell after exporting API, KEY, and EMAIL environment variables.
"""
import os
import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = os.environ["API"] + "/parcels"
API_KEY = os.environ["KEY"]
EMAIL = os.environ.get("EMAIL", "20200001899@students.cud.ac.ae")

headers = {
    "x-api-key": API_KEY,
    "X-User-Role": "driver",
    "Content-Type": "application/json"
}


def create_parcel(i):
    data = {
        "sender": f"LoadSender{i}-{int(time.time())}",
        "receiver": f"LoadReceiver{i}",
        "address": "Dubai",
        "email": EMAIL
    }
    body = json.dumps(data).encode("utf-8")

    for attempt in range(1, 4):
        req = urllib.request.Request(API_URL, data=body, headers=headers, method="POST")
        start = time.time()
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                elapsed = time.time() - start
                text = response.read().decode("utf-8")
                return response.status, elapsed, text
        except urllib.error.HTTPError as e:
            elapsed = time.time() - start
            error_body = e.read().decode("utf-8")
            if attempt == 3:
                return e.code, elapsed, error_body
        except Exception as e:
            elapsed = time.time() - start
            if attempt == 3:
                return 0, elapsed, str(e)
        time.sleep(0.5)


start_all = time.time()
results = []

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(create_parcel, i) for i in range(1, 21)]
    for future in as_completed(futures):
        results.append(future.result())

total_time = time.time() - start_all
successes = sum(1 for status, _, _ in results if status == 201)
avg_response = sum(elapsed for _, elapsed, _ in results) / len(results)

print("SmartParcel Concurrent Load Test")
print("--------------------------------")
print("ThreadPoolExecutor max_workers: 20")
print(f"Total requests: {len(results)}")
print(f"Successes: {successes}/20")
print(f"Total time: {total_time:.2f} seconds")
print(f"Average response time: {avg_response:.2f} seconds")
print("Status codes:", [status for status, _, _ in results])

if successes != 20:
    print("
Failed responses:")
    for status, elapsed, text in results:
        if status != 201:
            print(f"Status={status}, Time={elapsed:.2f}, Error={text[:200]}")
