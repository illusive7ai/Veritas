#!/bin/bash
# VERITAS - One-click setup script
# OSINT Reconnaissance & Intelligence Tool

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo " █▀▒   █▓ ▓ ▄▄██   ██ ███    ██▓ ▄▄▄█▄███▓  ▄▄▄          ▄▄██  "
echo "▓██░   █▒ ▓█   ▀  ▓██ ▒ ██▓ ▓▐█▒ ▓  ██▒ ▓▒ ▒▄▀ █▄     ▒ ▀   ▒  "
echo " ▓▀▄  █▒░ ▒█ █    ▓██ ░▄█ ▒ ▒ █▒ ▒ ▓██░ ▒░ ▒██  ▀█▄   ░ ▓██▄   "
echo "  ▒██ █░░ ▒▓█  ▄  ▒▄█▀▀█▄   ░▐ ░ ░ ▓▄█▓ ░  ░▄█▄▄▄▄██    ▒   ▄█▓"
echo "   ▒▀█ ░  ░▒████▒ ░██▓ ▒██▒ ░▐█░   ▒██▒ ░   ▓█   ▓██▒ ▓███▄▄▀▒▒"
echo "   ░ ▐ ░  ░░ ▒░ ░ ░ ▒▓ ░▒▓░ ░▓     ▒ ░░     ▒▒   ▓▒█░ ▒ ▒▓▒ ▒ ░"
echo "   ░ ░░    ░ ░  ░   ░▒ ░ ▒░  ▒ ░     ░       ▒   ▒▒ ░ ░ ░▒  ░ ░"
echo "     ░░      ░      ░░   ░   ▒ ░   ░         ░   ▒    ░  ░  ░  "
echo "      ░      ░  ░    ░       ░                   ░  ░       ░  "
echo "     ░                                                         "
echo -e "${CYAN}════════════════════════════════════════════════════════════"
echo -e "${YELLOW}  VERITAS - OSINT Reconnaissance & Intelligence Tool${CYAN}"
echo -e "  Version 1.1 - Terminal Efficiency${CYAN}"
echo -e "════════════════════════════════════════════════════════════${NC}"
echo ""

# Check Python
echo -e "${GREEN}[+] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[-] Python3 not found!${NC}"
    echo -e "${YELLOW}[!] Please install Python 3.6 or higher${NC}"
    echo -e "${YELLOW}[!] Ubuntu/Debian: sudo apt-get install python3 python3-pip${NC}"
    echo -e "${YELLOW}[!] MacOS: brew install python3${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}[+] Python version: $PYTHON_VERSION${NC}"

# Check pip
echo -e "${GREEN}[+] Checking pip installation...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}[!] pip3 not found. Installing...${NC}"
    python3 -m ensurepip --upgrade
fi

# Create virtual environment (optional)
echo -e "${GREEN}[+] Do you want to use a virtual environment?${NC}"
read -p "[y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}[+] Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}[+] Virtual environment activated!${NC}"
fi

# Install dependencies
echo -e "${GREEN}[+] Installing dependencies...${NC}"
echo -e "${CYAN}    - requests${NC}"
echo -e "${CYAN}    - colorama${NC}"
pip3 install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[+] Dependencies installed successfully!${NC}"
else
    echo -e "${RED}[-] Failed to install dependencies!${NC}"
    echo -e "${YELLOW}[!] Try manual install: pip install -r requirements.txt${NC}"
    exit 1
fi

# Make veritas.py executable
echo -e "${GREEN}[+] Making veritas.py executable...${NC}"
chmod +x veritas.py

# Check for config file
if [ ! -f "veritas_config.json" ]; then
    echo -e "${GREEN}[+] Creating initial config file...${NC}"
    echo '{"premium": false, "date": "2024-01-01", "version": "1.1"}' > veritas_config.json
fi

# Success message
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}[+] VERITAS SETUP COMPLETE! ✅${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN} Quick Start:${NC}"
echo -e "  ${YELLOW}1.${NC} Run Veritas: ${GREEN}python3 veritas.py${NC}"
echo -e "  ${YELLOW}2.${NC} Search tools: ${GREEN}search osint username${NC}"
echo -e "  ${YELLOW}3.${NC} Unlock premium: ${GREEN}premium Illusivehacks${NC}"
echo -e "  ${YELLOW}4.${NC} Get help: ${GREEN}help${NC}"
echo ""
echo -e "${CYAN}📄 Pagination Commands:${NC}"
echo -e "  ${GREEN}N${NC} - Next page    ${GREEN}P${NC} - Previous page"
echo -e "  ${GREEN}O<num>${NC} - Open result    ${GREEN}Q${NC} - Quit view"
echo ""
echo -e "${YELLOW}💡 Tip:${NC} Use 'premium-list' to see all premium tools!"
echo ""

# Ask to run
echo -e "${CYAN}Do you want to run Veritas now?${NC}"
read -p "[y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}[+] Starting Veritas...${NC}"
    echo ""
    python3 veritas.py
else
    echo -e "${GREEN}[+] Setup complete! Run Veritas anytime with: python3 veritas.py${NC}"
fi