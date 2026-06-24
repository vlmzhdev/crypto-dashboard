# Crypto Gas & Fee Dashboard

A dashboard for tracking Bitcoin mempool fees and gas prices on Ethereum, BSC, and Polygon.  
Built as my first independent project to learn how background daemons, MySQL, REST APIs, and modern frontend fit together.

## Features
* Real-time fee data for BTC and three EVM networks updated asynchronously
* Auto-refreshing frontend that pulls data every 30s without reloading the page
* Background Python daemons fetch data every 60s via systemd
* PHP REST API serves the frontend from MySQL
* Credentials stored in .env, not hardcoded

## Stack

| Layer | Tech |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, Vanilla JS (Fetch API, Async/Await) |
| **Backend** | Python 3, PHP + PDO |
| **Database** | MySQL |
| **Server** | Nginx, PHP-FPM, systemd |

## Project Structure

```text
├── backend/
│   ├── evm_gas.py        # fetches EVM gas prices and writes to DB
│   ├── mempool_api.py    # scrapes Bitcoin mempool fees
│   └── .env.example
├── frontend/
│   ├── api.php           # BTC data endpoint
│   ├── evm_api.php       # EVM data endpoint
│   └── index.html        # Web interface with dynamic JS updates
└── .gitignore
