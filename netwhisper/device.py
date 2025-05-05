from contextlib import contextmanager
from typing import Generator, Optional

from jinja2 import Environment, FileSystemLoader
from napalm import get_network_driver

from netwhisper.logger import logger
from netwhisper.utils import Device, device_from_request

ENV = Environment(loader=FileSystemLoader("netwhisper/templates"))


class DeviceSession:
    def __init__(self, device: Device):
        self.device_info = device
        self.driver = None
        self.device = None

    def connect(self) -> bool:
        """Open connection to the device."""
        logger.info(
            f"[bold green]Connecting to {self.device_info.name} ({self.device_info.hostname})...[/]"
        )
        self.driver = get_network_driver(self.device_info.driver)
        self.device = self.driver(
            hostname=self.device_info.hostname,
            username=self.device_info.username,
            password=self.device_info.password,
            timeout=self.device_info.timeout,
            optional_args=self.device_info.optional_args,
        )
        self.device.open()
        logger.info("[bold green]Connection established![/]")

    def disconnect(self):
        """Close connection."""
        if self.device:
            self.device.close()
            logger.info("[bold green]Disconnected.[/]")


@contextmanager
def device_session(device_request) -> Generator[DeviceSession, None, None]:
    """
    Context manager to handle device connection and disconnection.
    """
    session = None
    try:
        device = device_from_request(device_request)
        session = DeviceSession(device)
        session.connect()
        yield session
    finally:
        logger.info("[bold green]Closing connection...[/]")
        if session:
            session.disconnect()


class DeviceServiceError(Exception):
    """Custom exception for device service errors."""

    pass


def safe_device_call(func):
    """
    Decorator to handle exceptions during device operations.
    """
    print("safe_device_call")

    def wrapper(session: DeviceSession, *args, **kwargs):
        try:
            return func(session, *args, **kwargs)
        except Exception as e:
            raise DeviceServiceError(f"{e}")

    return wrapper


class DeviceService:
    @staticmethod
    @safe_device_call
    def get_facts(session: DeviceSession) -> Optional[dict]:
        """Retrieve device facts."""
        return session.device.get_facts()

    @staticmethod
    @safe_device_call
    def get_config(session: DeviceSession) -> Optional[str]:
        """Retrieve running configuration."""
        return session.device.get_config()

    @staticmethod
    def get_route_to(
        session: DeviceSession, destination: str, protocol: str = ""
    ) -> Optional[dict]:
        """Get route to a destination."""
        return session.device.get_route_to(destination, protocol)

    @staticmethod
    def add_static_route(
        session: DeviceSession,
        destination: str,
        next_hop: str,
        show_diff: bool = False,
        commit: bool = False,
    ) -> Optional[dict]:
        """Add a static route to the device."""
        template = ENV.get_template("static_route.j2")
        rendered_config = template.render(destination=destination, next_hop=next_hop)
        ret = DeviceService.apply(session, rendered_config, show_diff=show_diff, commit=commit)
        logger.info(f"[bold green]Static route {destination} added successfully.[/]")
        return ret

    @staticmethod
    def apply(
        session: DeviceSession, config: str, show_diff: bool = False, commit: bool = False
    ) -> Optional[dict]:
        """Apply a configuration candidate."""
        session.device.load_merge_candidate(config=config)
        logger.info("[bold cyan]Configuration candidate loaded.[/]")
        diff = None
        if show_diff:
            diff = session.device.compare_config()
            if diff:
                logger.info("[bold yellow]Configuration differences:[/]")
                logger.info(diff)
            else:
                logger.info("[bold red]No differences found.[/]")
        if commit:
            session.device.commit_config()
            logger.info("[bold green]Configuration committed.[/]")

        return {"config": config, "diff": diff}
