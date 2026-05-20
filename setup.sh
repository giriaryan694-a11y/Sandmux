#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# Sandmux Sandbox Tool - Setup Script
# Made By Aryan Giri | giriaryan694-a11y
# -----------------------------------------------------------------------------

set -e

# --- COLOR DEFINITIONS ---
RED='\e[1;31m'
GREEN='\e[1;32m'
YELLOW='\e[1;33m'
BLUE='\e[1;34m'
MAGENTA='\e[1;35m'
CYAN='\e[1;36m'
NC='\e[0m' # No Color

# --- CREDITS BANNER ---
clear
echo -e "${CYAN}=======================================================${NC}"
echo -e "${MAGENTA}                 SANDMUX SETUP SYSTEM                  ${NC}"
echo -e "${YELLOW}        Made By Aryan Giri | giriaryan694-a11y         ${NC}"
echo -e "${CYAN}=======================================================${NC}"
echo ""
echo -e "${BLUE}[*] Sandmux setup script is running...${NC}"
echo -e "${BLUE}[*] Preparing your isolated development environment.${NC}"
echo ""

# --- APT UPDATE & UPGRADE ---
echo -e "${CYAN}[1/3]${NC} ${YELLOW}Updating Termux package repositories...${NC}"
pkg update -y && pkg upgrade -y
echo -e "${GREEN}[+] System repositories are up to date!${NC}"
echo ""

# --- INSTALL CORE UTILITIES ---
echo -e "${CYAN}[2/3]${NC} ${YELLOW}Installing required packages (proot-distro & python)...${NC}"
pkg install -y proot-distro python
echo -e "${GREEN}[+] System packages successfully installed!${NC}"
echo ""

# --- INITIAL DISTRO PULL ---
if ! proot-distro list | grep -q "Installed: yes" | grep -q "ubuntu"; then
    echo -e "${CYAN}[3/3]${NC} ${YELLOW}Fetching clean Ubuntu core image via proot-distro...${NC}"
    proot-distro install ubuntu
    echo -e "${GREEN}[+] Ubuntu rootfs successfully pulled!${NC}"
else
    echo -e "${CYAN}[3/3]${NC} ${GREEN}[+] Ubuntu environment already present. Skipping download.${NC}"
fi
echo ""

# --- PYTHON DEPENDENCIES NOTICE ---
echo -e "${CYAN}=======================================================${NC}"
echo -e "${YELLOW}[!] NOTICE: Python Package Installation${NC}"
echo -e "${CYAN}=======================================================${NC}"
echo -e "Please install the required python packages using your preferred method"
echo -e "(e.g., global pip, virtual environment / venv, pipx, etc.)."
echo ""
if [ -f "requirements.txt" ]; then
    echo -e "You can use the included ${MAGENTA}requirements.txt${NC} file:"
    echo -e "👉 ${CYAN}pip install -r requirements.txt${NC}"
else
    echo -e "Required modules: ${MAGENTA}pyfiglet${NC}, ${MAGENTA}colorama${NC}"
fi
echo ""

# --- FINISH ---
echo -e "${CYAN}=======================================================${NC}"
echo -e "${GREEN}[+] Setup done !${NC}"
echo -e "${CYAN}=======================================================${NC}"
echo ""
echo -e "Once your Python dependencies are ready, execute:"
echo -e "👉 ${CYAN}python sandmux.py -h${NC}"
echo ""
