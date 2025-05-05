from typing import List

import questionary

from netwhisper.cli.console import console
from netwhisper.utils import Device


def select_device(devices: List[Device]) -> Device:
    """Prompt the user to select a device from a list."""
    choices = [device.name for device in devices]

    selected_name = questionary.select(
        "Select a device to connect to:",
        choices=choices,
    ).ask()

    # Find the matching device object
    for device in devices:
        if device.name == selected_name:
            console.print(f"[bold cyan]Device selected:[/] {device.name}")
            return device

    raise ValueError(f"Selected device '{selected_name}' not found in inventory.")


def ask_question() -> str:
    """Prompt the user to ask a natural language question."""
    return questionary.text(
        "What do you want to do? (e.g., 'Configure a new VLAN', 'Shutdown an interface')"
    ).ask()


def choose_command(suggestions: List[str]) -> str:
    """Prompt the user to select one of the AI-generated command suggestions."""
    selected = questionary.select(
        "Select a configuration to apply:",
        choices=suggestions,
    ).ask()
    return selected
