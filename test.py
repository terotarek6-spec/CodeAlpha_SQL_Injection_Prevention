import requests

url = "http://127.0.0.1:5000/add-secure-data"

print("=====================================================")
print("🛡️ TEST 1: Unauthorized Access Attempt (No Capability Code)")
print("=====================================================")
headers_invalid = {"X-Capability-Code": "HACKER-CODE-000"}
payload_1 = {"username": "hacker", "sensitive_info": "secret_pass"}

response_1 = requests.post(url, json=payload_1, headers=headers_invalid)
print("Status Code:", response_1.status_code)
print("Response:", response_1.json())
print("\n")


print("=====================================================")
print("🛡️ TEST 2: Authorized Access & SQL Injection Prevention")
print("=====================================================")
headers_valid = {"X-Capability-Code": "ALPHA-SECURE-2026"}
payload_sqli = {
    "username": "admin", 
    "sensitive_info": "' OR '1'='1'; DROP TABLE users; --" 
}

response_2 = requests.post(url, json=payload_sqli, headers=headers_valid)
print("Status Code:", response_2.status_code)
print("Response:", response_2.json())
print("=====================================================")