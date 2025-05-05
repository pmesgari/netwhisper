import argparse

from netwhisper.cli.console import console
from netwhisper.cli.interaction import ask_question, choose_command, select_device
from netwhisper.device import DeviceConnection
from netwhisper.llm import get_command_suggestions
from netwhisper.utils import load_inventory

parser = argparse.ArgumentParser(description="NetWhisper CLI Tool")
parser.add_argument(
    "--inventory",
    type=str,
    default="inventory.yaml",
    help="Path to the inventory YAML file (default: inventory.yaml)",
)

args = parser.parse_args()


def app():
    devices = load_inventory(filepath=args.inventory)

    if not devices:
        console.print("[bold red]Error:[/] No devices found in inventory.")
        return

    selected_device = select_device(devices)
    console.print(
        f"Selected device: [bold green]{selected_device.name}[/] ({selected_device.hostname})"
    )

    device_conn = DeviceConnection(selected_device)

    if not device_conn.connect():
        return

    if not device_conn.gather_device_data():
        return

    question = ask_question()
    suggestions = get_command_suggestions(device_conn.facts, device_conn.running_config, question)

    if suggestions:
        selected_command = choose_command(suggestions)
        console.print("\n[bold green]Selected Configuration:[/]\n")
        console.print(selected_command)
    else:
        console.print("[bold red]No suggestions generated.[/]")

    device_conn.disconnect()


if __name__ == "__main__":
    app()
