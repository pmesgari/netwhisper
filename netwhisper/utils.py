from dataclasses import dataclass
from typing import List

import yaml

from netwhisper.api.models import DeviceInput


@dataclass
class Device:
    name: str
    hostname: str
    username: str
    password: str
    driver: str
    timeout: int
    optional_args: dict


def device_from_request(request: DeviceInput) -> Device:
    return Device(
        name=request.name,
        hostname=request.hostname,
        username=request.username,
        password=request.password,
        driver=request.driver,
        timeout=request.timeout,
        optional_args=request.optional_args,
    )


def load_inventory(filepath: str = "inventory.yaml") -> List[Device]:
    """Load devices from an inventory YAML file."""
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)

    devices = []
    for item in data.get("devices", []):
        device = Device(
            name=item["name"],
            hostname=item["hostname"],
            username=item["username"],
            password=item["password"],
            driver=item["driver"],
            optional_args=item.get("optional_args", {}),
        )
        devices.append(device)

    return devices
