import requests
import json
import time
import os
from datetime import datetime
import argparse

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Animation frames
FRAMES = [
    "🔍 Searching... ",
    "🔍 Scanning...  ",
    "🔍 Analyzing... ",
    "🔍 Processing.. "
]

def animate_search():
    """Display animated search effect"""
    for _ in range(2):
        for frame in FRAMES:
            print(f"\r{Colors.OKCYAN}{frame}{Colors.ENDC}", end="")
            time.sleep(0.2)
    print(f"\r{' '*20}\r", end="")

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Display colorful banner"""
    banner = f"""
{Colors.BOLD}{Colors.OKGREEN}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██████╗ ███████╗ █████╗ ██╗   ██╗███████╗██╗     ██████╗   ║
║   ██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝██║     ██╔══██╗  ║
║   ██████╔╝█████╗  ███████║██║   ██║█████╗  ██║     ██║  ██║  ║
║   ██╔══██╗██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝  ██║     ██║  ██║  ║
║   ██║  ██║███████╗██║  ██║ ╚████╔╝ ███████╗███████╗██████╔╝  ║
║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚══════╝╚═════╝   ║
║                                                              ║
║       T  O  X  I  C       M O B I L E   O S I N T                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
    print(banner)

def display_results(data, phone):
    """Display formatted results with colorful output"""
    clear_screen()
    display_banner()
    print(f"\n{Colors.BOLD}{Colors.OKGREEN}📱 Results for: {Colors.OKCYAN}{phone}{Colors.ENDC}\n")
    print(f"{Colors.BOLD}{Colors.WARNING}{'='*70}{Colors.ENDC}")

    results_found = False

    # --- UPDATED LOGIC TO PARSE THE NEW JSON STRUCTURE ---
    if 'List' in data and isinstance(data['List'], dict):
        # Iterate through each source inside "List" (e.g., "HiTeckGroop.in")
        for source_name, source_data in data['List'].items():
            if 'Data' in source_data and source_data['Data']:
                results_found = True
                print(f"\n{Colors.BOLD}{Colors.OKBLUE}🔍 RESULTS FROM: {source_name}{Colors.ENDC}")
                
                for idx, item in enumerate(source_data['Data'], 1):
                    print(f"\n{Colors.BOLD}{Colors.OKCYAN}Entry #{idx}:{Colors.ENDC}")
                    print(f"  {Colors.OKGREEN}Full Name     : {Colors.ENDC}{Colors.BOLD}{item.get('FullName', 'N/A')}")
                    print(f"  {Colors.OKGREEN}Father's Name : {Colors.ENDC}{item.get('FatherName', 'N/A')}")
                    print(f"  {Colors.OKGREEN}Address       : {Colors.ENDC}{item.get('Address', 'N/A')}")
                    print(f"  {Colors.OKGREEN}Region        : {Colors.ENDC}{item.get('Region', 'N/A')}")
                    
                    # Print all available phone numbers
                    if item.get('Phone'):
                        print(f"  {Colors.OKGREEN}Phone 1       : {Colors.ENDC}{item.get('Phone')}")
                    if item.get('Phone2'):
                        print(f"  {Colors.OKGREEN}Phone 2       : {Colors.ENDC}{item.get('Phone2')}")
                    if item.get('Phone3'):
                         print(f"  {Colors.OKGREEN}Phone 3       : {Colors.ENDC}{item.get('Phone3')}")
                    if item.get('Phone4'):
                         print(f"  {Colors.OKGREEN}Phone 4       : {Colors.ENDC}{item.get('Phone4')}")
                    if item.get('Phone5'):
                         print(f"  {Colors.OKGREEN}Phone 5       : {Colors.ENDC}{item.get('Phone5')}")

    if not results_found:
        print(f"\n{Colors.WARNING}⚠️ No detailed information found in the API response.{Colors.ENDC}")

    # --- SUMMARY SECTION ---
    print(f"\n{Colors.BOLD}{Colors.WARNING}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKGREEN}📊 SUMMARY:{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}Databases Searched : {Colors.ENDC}{data.get('NumOfDatabase', 'N/A')}")
    print(f"  {Colors.OKGREEN}Total Results      : {Colors.ENDC}{data.get('NumOfResults', 'N/A')}")
    print(f"  {Colors.OKGREEN}Search Time        : {Colors.ENDC}{data.get('search time', 'N/A')} seconds")
    print(f"  {Colors.OKGREEN}Search Date        : {Colors.ENDC}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\n{Colors.BOLD}{Colors.OKGREEN}✅ Search completed successfully!{Colors.ENDC}")

def fetch_data(phone):
    """Fetch data from API with animation"""
    api_url = f"https://osintpromax-5andkey-diejsskw.onrender.com/?query={phone}"
    try:
        animate_search()
        print(f"\n{Colors.OKCYAN}Connecting to API...{Colors.ENDC}")
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        print(f"\n{Colors.OKGREEN}✅ Data retrieved successfully!{Colors.ENDC}")
        time.sleep(0.5)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\n{Colors.FAIL}❌ Error fetching data: {e}{Colors.ENDC}")
        return None
    except json.JSONDecodeError:
        print(f"\n{Colors.FAIL}❌ Failed to parse API response (Invalid JSON).{Colors.ENDC}")
        return None

def main():
    """Main function to run the tool"""
    parser = argparse.ArgumentParser(description='Mobile OSINT Tool - Mobile Number Intelligence')
    parser.add_argument('phone', nargs='?', help='Mobile number to search (with country code)')
    args = parser.parse_args()
    clear_screen()
    display_banner()

    phone = args.phone or input(f"\n{Colors.BOLD}{Colors.OKCYAN}Enter mobile number (with country code): {Colors.ENDC}")
    if not phone:
        print(f"\n{Colors.FAIL}❌ No phone number provided. Exiting.{Colors.ENDC}")
        return

    print(f"\n{Colors.BOLD}{Colors.OKGREEN}🚀 Starting OSINT investigation for {phone}...{Colors.ENDC}")
    time.sleep(0.5)
    data = fetch_data(phone)
    if data:
        display_results(data, phone)
    else:
        print(f"\n{Colors.FAIL}❌ Failed to retrieve data. Please try again.{Colors.ENDC}")

if __name__ == "__main__":
    main()
