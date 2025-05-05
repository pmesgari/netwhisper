# NetWhisper

**NetWhisper** is a FastAPI-based network automation platform that interacts with network devices using [NAPALM](https://github.com/napalm-automation/napalm). It enables retrieving and applying configurations through a clean, extensible REST API.

---

## 🚀 Features

- Fetch running configurations
- Apply configuration changes
- Simple, modular design with testable service layer
- Typed API with Pydantic models

---

## 📦 Installation

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (used instead of pip/poetry)
- Docker (optional, for running Arista cEOS or test devices)

### Getting Started

```bash
# Clone the repo
git clone https://github.com/pmesgari/netwhisper.git
cd netwhisper

# Set up the virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv sync

# To sync with an active virtualenv
uv sync --active

# Run the development server
uvicorn netwhisper.api.main:app --reload --log-config logging_config.json
```

## 🧪 Example Usage

### Get Device Facts

``` bash
curl -X POST http://localhost:8000/device/get_facts \
  -H "Content-Type: application/json" \
  -d '{
        "device": {
          "name": "sw01",
          "hostname": "192.168.0.1",
          "username": "admin",
          "password": "admin",
          "driver": "eos",
          "optional_args": { "port": 8081 }
        }
      }'
```

### Add Static Route

```bash
curl -X POST http://localhost:8000/device/add_static_route \
  -H "Content-Type: application/json" \
  -d '{
        "device": {
          "name": "sw01",
          "hostname": "192.168.0.1",
          "username": "admin",
          "password": "admin",
          "driver": "eos",
          "optional_args": { "port": 8081 }
        },
        "destination": "10.1.1.0/24",
        "next_hop": "192.168.0.254",
        "show_diff": true,
        "commit": false
      }'
```