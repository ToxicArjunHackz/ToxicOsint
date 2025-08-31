import requests
import json
import time
import os
import sys
from datetime import datetime

# ----------------------------
# Colors for terminal output
# ----------------------------
class Colors:
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

# ----------------------------
# Animation frames
# ----------------------------
FRAMES = [
    "🔍 Searching... ",
    "🔍 Scanning...  ",
    "🔍 Analyzing... ",
    "🔍 Processing.. "
]

def animate_search(duration=3):
    """Animated search effect with rotating frames"""
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in FRAMES:
            print(f"\r{Colors.OKCYAN}{frame}{Colors.ENDC}", end="")
            time.sleep(0.2)
    print(f"\r{' '*30}\r", end="")

def progress_bar(task="Processing", length=30, duration=2):
    """Dynamic progress bar animation"""
    print(f"{Colors.OKBLUE}{task}:{Colors.ENDC} ", end="")
    for i in range(length+1):
        percent = int(i/length*100)
        bar = '█' * i + '-' * (length-i)
        print(f"\r{Colors.OKBLUE}{task}: |{bar}| {percent}%", end="")
        time.sleep(duration/length)
    print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    print(f"""
{Colors.BOLD}{Colors.OKGREEN}
===============================
     TOXIC MOBILE OSINT
===============================
{Colors.ENDC}
""")

# ----------------------------
# LeakOSint API configuration
# ----------------------------
LEAKOSINT_URL = "https://leakosintapi.com/"
API_TOKEN = "8354973020:38uTw7HW"

# ----------------------------
# Fetch data from LeakOSint API
# ----------------------------
def fetch_leakosint(phone, limit=1000, lang="ru"):
    payload = {
        "token": API_TOKEN,
        "request": phone,
        "limit": limit,
        "lang": lang
    }
    try:
        animate_search()
        print(f"{Colors.OKCYAN}Connecting to LeakOSint API...{Colors.ENDC}")
        response = requests.post(LEAKOSINT_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        if "Error code" in data:
            print(f"{Colors.FAIL}❌ API Error: {data['Error code']}{Colors.ENDC}")
            return None
        progress_bar("Fetching Data", length=40, duration=2)
        print(f"{Colors.OKGREEN}✅ Data retrieved successfully!{Colors.ENDC}")
        time.sleep(0.5)
        return data
    except requests.exceptions.RequestException as e:
        print(f"{Colors.FAIL}❌ Request failed: {e}{Colors.ENDC}")
        return None
    except json.JSONDecodeError:
        print(f"{Colors.FAIL}❌ Failed to parse API response (Invalid JSON).{Colors.ENDC}")
        return None

# ----------------------------
# Display results
# ----------------------------
def display_results(data, phone):
    clear_screen()
    display_banner()
    print(f"\n📌 Results for: {Colors.OKCYAN}{phone}{Colors.ENDC}\n")
    print(f"{Colors.BOLD}{Colors.WARNING}{'='*60}{Colors.ENDC}")

    results_found = False

    if 'List' in data and isinstance(data['List'], dict):
        for source_name, source_data in data['List'].items():
            if 'Data' in source_data and source_data['Data']:
                results_found = True
                print(f"\n{Colors.BOLD}{Colors.OKBLUE}🔹 RESULTS FROM: {source_name}{Colors.ENDC}")
                for idx, item in enumerate(source_data['Data'], 1):
                    print(f"\n{Colors.BOLD}{Colors.OKCYAN}Entry #{idx}:{Colors.ENDC}")
                    for key, value in item.items():
                        print(f"  {Colors.OKGREEN}{key:15}: {Colors.ENDC}{value}")

    if not results_found:
        print(f"\n{Colors.WARNING}⚠️ No detailed information found.{Colors.ENDC}")

    # Summary with animated dots
    print(f"\n{Colors.BOLD}{Colors.WARNING}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKGREEN}📊 SUMMARY:{Colors.ENDC}")
    for i in range(3):
        print(f"  {Colors.OKGREEN}Calculating results{'.'*i}{Colors.ENDC}", end="\r")
        time.sleep(0.5)
    print()
    print(f"  {Colors.OKGREEN}Databases Searched : {Colors.ENDC}{data.get('NumOfDatabase', 'N/A')}")
    print(f"  {Colors.OKGREEN}Total Results      : {Colors.ENDC}{data.get('NumOfResults', 'N/A')}")
    print(f"  {Colors.OKGREEN}Search Time        : {Colors.ENDC}{data.get('search time', 'N/A')} seconds")
    print(f"  {Colors.OKGREEN}Search Date        : {Colors.ENDC}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{Colors.BOLD}{Colors.OKGREEN}✅ Search completed successfully!{Colors.ENDC}")

# ----------------------------
# Main
# ----------------------------
def main():
    clear_screen()
    display_banner()
    phone = input(f"\n{Colors.BOLD}{Colors.OKCYAN}Enter mobile number (with country code): {Colors.ENDC}")
    if not phone:
        print(f"{Colors.FAIL}❌ No phone number provided. Exiting.{Colors.ENDC}")
        return

    print(f"\n{Colors.BOLD}{Colors.OKGREEN}🚀 Starting LeakOSint investigation for {phone}...{Colors.ENDC}")
    time.sleep(0.5)
    data = fetch_leakosint(phone)
    if data:
        display_results(data, phone)
    else:
        print(f"\n{Colors.FAIL}❌ Failed to retrieve data. Please try again.{Colors.ENDC}")

if __name__ == "__main__":
    main()
