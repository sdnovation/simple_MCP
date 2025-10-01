# 🛰️ Control Your Network with AI – Catalyst Center MCP Server

This repository contains an **MCP (Model Context Protocol) server** implementation that integrates **Cisco Catalyst Center (formerly DNA Center)** and **local LLMs** to query network devices and configurations.  

It provides two main tools through the [FastMCP](https://github.com/CognitiveNetworks/fastmcp) framework:
- `getDevices` – Retrieve detailed device information via Catalyst Center APIs  
- `getDeviceConfig` – SSH into devices and fetch their running configuration  

This project demonstrates how AI-driven agents can dynamically interact with your Cisco network infrastructure.  
For a detailed explanation, see my blog post:  
🔗 [Control Your Network with AI – Building Your First MCP Server with a Local LLM](https://krauss1990.wixsite.com/home/post/control-your-network-with-ai-building-your-first-mcp-server-with-a-local-llm)

---

## 🚀 Features
- Query all devices managed by Cisco Catalyst Center  
- Collect health metrics, OS versions, models, IP addresses, and locations  
- Retrieve full device running configurations via SSH (Netmiko)  
- Ready-to-use MCP server for integration with local AI agents  
- JSON-based output for easy parsing and automation  

---

## 📦 Requirements
- Python 3.9+  
- Cisco Catalyst Center (DNA Center) with API credentials  
- Devices reachable via SSH with configured credentials  

---

## 🔧 Installation

```bash
# Clone the repo
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt
