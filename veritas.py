#!/usr/bin/env python3
"""
VERITAS - OSINT Reconnaissance & Intelligence Tool
Version: 1.1
"""

import requests
import json
import os
import sys
import webbrowser
from datetime import datetime
from colorama import init, Fore, Style, Back

# Initialize colorama
init(autoreset=True)

# === CONFIGURATION ===
VERSION = "1.1"
PASSWORD = "Illusivehacks"  # Premium password
CONFIG_FILE = "veritas_config.json"
ITEMS_PER_PAGE = 10  # Results per page

# Premium OSINT Tools - FULL DESCRIPTIONS
PREMIUM_REPOS = {
    "sherlock-project/sherlock": "Find usernames across 300+ social networks - The most popular OSINT username search tool",
    "megadose/holehe": "Check if an email is used on multiple websites and platforms - Email reconnaissance tool",
    "laramies/theHarvester": "Email, subdomain, and host harvesting tool for penetration testing and OSINT",
    "smicallef/spiderfoot": "Automated OSINT framework with 200+ modules for data collection and analysis",
    "michenriksen/aquatone": "Website screenshotting and discovery tool for visual reconnaissance",
    "soxoj/maigret": "Username search across 2000+ sites - Extensive social media username checker",
    "projectdiscovery/subfinder": "Fast subdomain discovery tool - Find subdomains for any domain",
    "lanmaster53/recon-ng": "Full-featured web reconnaissance framework with modular architecture",
    "digininja/CeWL": "Custom wordlist generator from websites - Spider and generate wordlists",
    "blacklanternsecurity/bbot": "Modular OSINT framework with automated data collection and correlation",
    "m8r0wn/m8r0wn": "OSINT framework for gathering intelligence on targets - Username and email enumeration",
    "targethacker/target-osint": "OSINT tools collection for target reconnaissance and intelligence gathering",
}

# Color scheme
COLORS = {
    'info': Fore.CYAN,
    'success': Fore.GREEN,
    'warning': Fore.YELLOW,
    'error': Fore.RED,
    'premium': Fore.MAGENTA,
    'reset': Style.RESET_ALL,
    'bold': Style.BRIGHT
}

# === BANNER ===
def print_banner():
    """Display the Veritas banner in blue"""
    banner = f"""
{Fore.BLUE}
 █▀▒   █▓ ▓ ▄▄██   ██ ███    ██▓ ▄▄▄█▄███▓  ▄▄▄          ▄▄██  
▓██░   █▒ ▓█   ▀  ▓██ ▒ ██▓ ▓▐█▒ ▓  ██▒ ▓▒ ▒▄▀ █▄     ▒ ▀   ▒  
 ▓▀▄  █▒░ ▒█ █    ▓██ ░▄█ ▒ ▒ █▒ ▒ ▓██░ ▒░ ▒██  ▀█▄   ░ ▓██▄   
  ▒██ █░░ ▒▓█  ▄  ▒▄█▀▀█▄   ░▐ ░ ░ ▓▄█▓ ░  ░▄█▄▄▄▄██    ▒   ▄█▓
   ▒▀█ ░  ░▒████▒ ░██▓ ▒██▒ ░▐█░   ▒██▒ ░   ▓█   ▓██▒ ▓███▄▄▀▒▒
   ░ ▐ ░  ░░ ▒░ ░ ░ ▒▓ ░▒▓░ ░▓     ▒ ░░     ▒▒   ▓▒█░ ▒ ▒▓▒ ▒ ░
   ░ ░░    ░ ░  ░   ░▒ ░ ▒░  ▒ ░     ░       ▒   ▒▒ ░ ░ ░▒  ░ ░
     ░░      ░      ░░   ░   ▒ ░   ░         ░   ▒    ░  ░  ░  
      ░      ░  ░    ░       ░                   ░  ░       ░  
     ░                                                         
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║  {Fore.YELLOW} OSINT Reconnaissance & Intelligence Tool {Fore.CYAN}           
║  {Fore.GREEN}  Version {VERSION} {Fore.CYAN}                   
║  {Fore.MAGENTA} Premium: {'ACTIVE' if check_premium_status() else 'LOCKED'}{Fore.CYAN}    
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

# === HELPER FUNCTIONS ===
def print_status(message, status_type="info"):
    """Print formatted status messages with [+] prefix"""
    colors = {
        'info': Fore.CYAN,
        'success': Fore.GREEN,
        'warning': Fore.YELLOW,
        'error': Fore.RED,
        'premium': Fore.MAGENTA,
        'search': Fore.BLUE,
        'nav': Fore.YELLOW
    }
    
    color = colors.get(status_type, Fore.WHITE)
    prefix = {
        'info': '[+]',
        'success': '[+]',
        'warning': '[!]',
        'error': '[-]',
        'premium': '[💎]',
        'search': '[🔍]',
        'nav': '[📄]'
    }.get(status_type, '[+]')
    
    print(f"{color}{prefix} {message}{Style.RESET_ALL}")

def check_premium_status():
    """Check if premium is unlocked"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                return data.get('premium', False)
        except:
            return False
    return False

def save_premium_status(status):
    """Save premium status"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump({
            'premium': status,
            'date': str(datetime.now()),
            'version': VERSION
        }, f, indent=2)

# === PAGINATION CLASS ===
class Paginator:
    """Handle pagination for search results"""
    def __init__(self, items, items_per_page=10):
        self.items = items
        self.items_per_page = items_per_page
        self.total_items = len(items)
        self.total_pages = max(1, (self.total_items + items_per_page - 1) // items_per_page)
        self.current_page = 1
        self.current_results = []
        
    def get_page(self, page_num):
        """Get items for a specific page"""
        if page_num < 1 or page_num > self.total_pages:
            return []
        
        self.current_page = page_num
        start = (page_num - 1) * self.items_per_page
        end = min(start + self.items_per_page, self.total_items)
        self.current_results = self.items[start:end]
        return self.current_results
    
    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages:
            return self.get_page(self.current_page + 1)
        return self.current_results
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            return self.get_page(self.current_page - 1)
        return self.current_results
    
    def get_page_info(self):
        """Get current page information"""
        return {
            'current': self.current_page,
            'total': self.total_pages,
            'start': (self.current_page - 1) * self.items_per_page + 1,
            'end': min(self.current_page * self.items_per_page, self.total_items),
            'total_items': self.total_items
        }
    
    def print_navigation(self):
        """Display navigation controls"""
        info = self.get_page_info()
        print()
        print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW} Page {info['current']}/{info['total']} | Showing {info['start']}-{info['end']} of {info['total_items']} results{Style.RESET_ALL}")
        print(f"{Fore.CYAN}┌{'─' * 68}┐{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  [N] Next Page  [P] Previous Page  [O<num>] Open Result  [Q] Quit View{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└{'─' * 68}┘{Style.RESET_ALL}")
        print()

# === MAIN LOGIC ===
class Veritas:
    def __init__(self):
        self.premium = check_premium_status()
        self.results = []
        self.search_count = 0
        self.paginator = None
        self.in_pagination_mode = False
        
    def unlock_premium(self, password):
        """Unlock premium features"""
        if password == PASSWORD:
            self.premium = True
            save_premium_status(True)
            print_status("Premium UNLOCKED! All tools now available!", "success")
            return True
        else:
            print_status("Invalid password! Premium remains locked.", "error")
            return False
    
    def display_results_page(self, page_num=None):
        """Display a specific page of results"""
        if not self.paginator:
            print_status("No search results to display. Run a search first.", "warning")
            return
        
        # Get the page
        if page_num is not None:
            results = self.paginator.get_page(page_num)
        else:
            results = self.paginator.get_page(self.paginator.current_page)
        
        if not results:
            print_status("No results on this page.", "warning")
            return
        
        # Clear screen for cleaner view
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        print_status(f"Search Results: {self.paginator.total_items} tools found", "success")
        print()
        
        # Display results with global indices
        for idx, repo in enumerate(results, 1):
            # Calculate global index
            global_idx = (self.paginator.current_page - 1) * self.paginator.items_per_page + idx
            
            name = repo.get('full_name', 'Unknown')
            desc = repo.get('description', 'No description')
            stars = repo.get('stargazers_count', 0)
            url_link = repo.get('html_url', '')
            
            # Check if premium
            is_premium = name in PREMIUM_REPOS
            
            # Format output
            if is_premium and not self.premium:
                prefix = f"{Fore.RED}[{global_idx}] 🔒 PREMIUM"
            elif is_premium and self.premium:
                prefix = f"{Fore.GREEN}[{global_idx}] 🔓 UNLOCKED"
            else:
                prefix = f"{Fore.BLUE}[{global_idx}]  FREE"
            
            print(f"{prefix} {Fore.WHITE}{name} {Fore.YELLOW}⭐ {stars}")
            print(f"   {Fore.CYAN} {desc}")
            print(f"   {Fore.BLUE}🔗 {url_link}")
            
            if is_premium:
                print(f"   {Fore.MAGENTA} {PREMIUM_REPOS[name]}")
            
            print()
        
        # Show navigation
        self.paginator.print_navigation()
        
        # Handle pagination commands
        self.in_pagination_mode = True
        while self.in_pagination_mode:
            try:
                nav_input = input(f"{Fore.CYAN}veritas (page {self.paginator.current_page}/{self.paginator.total_pages})>{Style.RESET_ALL} ").strip().lower()
                
                if not nav_input:
                    continue
                
                if nav_input in ['n', 'next']:
                    if self.paginator.current_page < self.paginator.total_pages:
                        self.display_results_page(self.paginator.current_page + 1)
                        return
                    else:
                        print_status("Already on the last page!", "warning")
                
                elif nav_input in ['p', 'prev', 'previous']:
                    if self.paginator.current_page > 1:
                        self.display_results_page(self.paginator.current_page - 1)
                        return
                    else:
                        print_status("Already on the first page!", "warning")
                
                elif nav_input.startswith('o') or nav_input.startswith('open '):
                    # Extract number
                    try:
                        if nav_input.startswith('o'):
                            num = int(nav_input[1:].strip())
                        else:
                            num = int(nav_input.split()[1].strip())
                        
                        # Adjust for global index
                        actual_idx = num - 1
                        if 0 <= actual_idx < len(self.results):
                            self.open_repo(str(num))
                        else:
                            print_status(f"Invalid number. Use 1-{len(self.results)}", "error")
                    except ValueError:
                        print_status("Usage: O<number> or open <number>", "warning")
                
                elif nav_input in ['q', 'quit', 'exit']:
                    self.in_pagination_mode = False
                    print_status("Exited pagination view", "info")
                    break
                
                elif nav_input == 'help':
                    print(f"{Fore.CYAN}Navigation Commands:{Style.RESET_ALL}")
                    print(f"  {Fore.GREEN}N{Fore.WHITE}     - Next page")
                    print(f"  {Fore.GREEN}P{Fore.WHITE}     - Previous page")
                    print(f"  {Fore.GREEN}O<num>{Fore.WHITE} - Open result number <num>")
                    print(f"  {Fore.GREEN}Q{Fore.WHITE}     - Quit pagination view")
                
                else:
                    print_status(f"Unknown command. Use N, P, O<num>, or Q", "warning")
                    
            except KeyboardInterrupt:
                self.in_pagination_mode = False
                print()
                print_status("Exited pagination view", "info")
                break
    
    def search_github(self, query):
        """Search GitHub for OSINT tools"""
        print_status(f"Searching for '{query}' on GitHub...", "search")
        
        url = "https://api.github.com/search/repositories"
        params = {
            'q': query,
            'per_page': 50,  # Get more results for pagination
            'sort': 'stars',
            'order': 'desc'
        }
        headers = {'Accept': 'application/vnd.github.v3+json'}
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.results = data.get('items', [])
                self.search_count += 1
                
                total = data.get('total_count', 0)
                print_status(f"Found {total} results (showing first {len(self.results)})", "success")
                print()
                
                if not self.results:
                    print_status("No results found. Try a different query.", "warning")
                    return
                
                # Create paginator
                self.paginator = Paginator(self.results, ITEMS_PER_PAGE)
                
                # Display first page
                self.display_results_page(1)
                
            elif response.status_code == 403:
                print_status("GitHub API rate limit exceeded. Try again later.", "error")
            else:
                print_status(f"GitHub API error: {response.status_code}", "error")
                
        except requests.exceptions.Timeout:
            print_status("Request timed out. Check your internet connection.", "error")
        except requests.exceptions.ConnectionError:
            print_status("Network error. Please check your connection.", "error")
        except Exception as e:
            print_status(f"Unexpected error: {e}", "error")
    
    def show_premium_list(self):
        """Display all premium tools with pagination"""
        # Convert premium dict to list format for pagination
        premium_items = []
        for repo, desc in PREMIUM_REPOS.items():
            premium_items.append({
                'full_name': repo,
                'description': desc,
                'html_url': f"https://github.com/{repo}",
                'stargazers_count': 0,
                'is_premium': True
            })
        
        # Create paginator for premium list
        self.paginator = Paginator(premium_items, ITEMS_PER_PAGE)
        self.results = premium_items  # Store for open command
        
        # Display first page
        self.display_results_page(1)
    
    def open_repo(self, number):
        """Open a repository in browser"""
        try:
            idx = int(number) - 1
            if 0 <= idx < len(self.results):
                repo = self.results[idx]
                name = repo.get('full_name', '')
                url = repo.get('html_url', '')
                
                # Check premium lock
                if name in PREMIUM_REPOS and not self.premium:
                    print_status("This is a PREMIUM tool! Unlock with 'premium Illusivehacks'", "error")
                    return
                
                print_status(f"Opening {url} in browser...", "success")
                webbrowser.open_new_tab(url)
            else:
                print_status(f"Invalid number. Use 1-{len(self.results)}", "error")
        except ValueError:
            print_status("Please enter a valid number", "error")
    
    def show_help(self):
        """Display help menu"""
        help_text = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║  {Fore.YELLOW}  VERITAS - COMMAND REFERENCE{Fore.CYAN}                         
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}[+]{Fore.WHITE} search <query>        - Search GitHub for OSINT tools
{Fore.GREEN}[+]{Fore.WHITE} premium <password>    - Unlock premium tools (password: Illusivehacks)
{Fore.GREEN}[+]{Fore.WHITE} premium-list          - Show all premium tools with pagination
{Fore.GREEN}[+]{Fore.WHITE} open <number>         - Open repository by number
{Fore.GREEN}[+]{Fore.WHITE} clear                 - Clear the screen
{Fore.GREEN}[+]{Fore.WHITE} help / -h / --help    - Show this help menu
{Fore.GREEN}[+]{Fore.WHITE} info / about          - Show tool information
{Fore.GREEN}[+]{Fore.WHITE} exit / quit / q       - Exit Veritas

{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║  {Fore.YELLOW}📄 PAGINATION NAVIGATION{Fore.CYAN}                                 
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}[+]{Fore.WHITE} When viewing results, use these commands:
{Fore.GREEN}  N{Fore.WHITE}           - Next page
{Fore.GREEN}  P{Fore.WHITE}           - Previous page
{Fore.GREEN}  O<number>{Fore.WHITE}   - Open result by number
{Fore.GREEN}  Q{Fore.WHITE}           - Exit pagination view

{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║  {Fore.YELLOW}💡 QUICK START{Fore.CYAN}                                           
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}[+]{Fore.WHITE} 1. Search for tools: {Fore.CYAN}search email osint
{Fore.GREEN}[+]{Fore.WHITE} 2. Navigate pages: {Fore.CYAN}N (next) / P (previous)
{Fore.GREEN}[+]{Fore.WHITE} 3. Open a result: {Fore.CYAN}O1 (opens result #1)
{Fore.GREEN}[+]{Fore.WHITE} 4. Unlock premium: {Fore.CYAN}premium Illusivehacks
        """
        print(help_text)
    
    def show_info(self):
        """Display tool information"""
        info_text = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║  {Fore.YELLOW}ℹ️  VERITAS - INFORMATION{Fore.CYAN}                                
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}[+]{Fore.WHITE} Name:        Veritas
{Fore.GREEN}[+]{Fore.WHITE} Version:     {VERSION}
{Fore.GREEN}[+]{Fore.WHITE} Description: OSINT Reconnaissance & Intelligence Tool
{Fore.GREEN}[+]{Fore.WHITE} Purpose:     Search and discover OSINT tools on GitHub
{Fore.GREEN}[+]{Fore.WHITE} Premium:     {'ACTIVE' if self.premium else 'LOCKED'}
{Fore.GREEN}[+]{Fore.WHITE} Password:    Illusivehacks (for premium)
{Fore.GREEN}[+]{Fore.WHITE} Total Tools: {len(PREMIUM_REPOS)} premium tools
{Fore.GREEN}[+]{Fore.WHITE} Page Size:   {ITEMS_PER_PAGE} results per page
{Fore.GREEN}[+]{Fore.WHITE} Author:      Illusivehacks
{Fore.GREEN}[+]{Fore.WHITE} License:     MIT

{Fore.CYAN}💡 "Veritas" - uncovering digital truth{Style.RESET_ALL}
        """
        print(info_text)
    
    def run(self):
        """Main interactive loop"""
        # Print banner on start
        print_banner()
        
        # Show premium status
        if self.premium:
            print_status("Premium Mode: ACTIVE - All tools unlocked!", "success")
        else:
            print_status("Premium Mode: LOCKED - Use 'premium Illusivehacks' to unlock", "warning")
        
        print()
        print_status("Type 'help' or '-h' for available commands", "info")
        print()
        
        while True:
            try:
                # Get user input
                cmd_input = input(f"{Fore.CYAN}veritas>{Style.RESET_ALL} ").strip()
                
                if not cmd_input:
                    continue
                
                # Parse command
                parts = cmd_input.split(maxsplit=1)
                command = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ''
                
                # Handle commands
                if command in ['exit', 'quit', 'q']:
                    print_status("Goodbye! Stay safe out there! 👋", "info")
                    break
                
                elif command in ['help', '-h', '--help']:
                    self.show_help()
                
                elif command == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_banner()
                
                elif command in ['info', 'about']:
                    self.show_info()
                
                elif command == 'search':
                    if arg:
                        self.search_github(arg)
                    else:
                        print_status("Usage: search <query>", "warning")
                        print_status("Example: search email osint", "info")
                
                elif command == 'premium':
                    if arg:
                        self.unlock_premium(arg)
                    else:
                        print_status("Usage: premium <password>", "warning")
                        print_status("Example: premium Illusivehacks", "info")
                
                elif command in ['premium-list', 'premiumlist', 'pl']:
                    self.show_premium_list()
                
                elif command == 'open':
                    if arg:
                        self.open_repo(arg)
                    else:
                        print_status("Usage: open <number>", "warning")
                        print_status("Example: open 1", "info")
                
                else:
                    print_status(f"Unknown command: '{command}'. Type 'help' for available commands.", "error")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Exiting Veritas...{Style.RESET_ALL}")
                break
            except Exception as e:
                print_status(f"Error: {e}", "error")

# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    # Check dependencies
    try:
        import requests
        from colorama import init, Fore, Style, Back
    except ImportError:
        print(f"{Fore.RED}[-] Missing required packages!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Install with: pip install -r requirements.txt{Style.RESET_ALL}")
        sys.exit(1)
    
    # Run Veritas
    tool = Veritas()
    tool.run()