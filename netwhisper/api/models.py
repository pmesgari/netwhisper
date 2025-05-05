from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class ApiResponse(GenericModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None


class ConfigurableMixin(BaseModel):
    show_diff: bool = False
    commit: bool = True


class ConfigApplyResult(BaseModel):
    config: str
    diff: Optional[str] = None
    commit: Optional[bool] = False


class DeviceInput(BaseModel):
    name: str
    hostname: str
    username: str
    password: str
    driver: str
    timeout: int = 10
    optional_args: dict = {}


class DeviceRequest(BaseModel):
    device: DeviceInput


class GetFactsRequest(DeviceRequest):
    pass


class GetConfigRequest(DeviceRequest):
    pass


class GetRouteToRequest(DeviceRequest):
    destination: str
    protocol: str = ""


class AddStaticRouteRequest(DeviceRequest, ConfigurableMixin):
    destination: str
    next_hop: str


class DeviceFacts(BaseModel):
    hostname: str
    fqdn: str
    vendor: str
    model: str
    serial_number: str
    os_version: str
    uptime: Union[int, float]
    interface_list: List[str]


class MyResponse(BaseModel):
    running: str
    candidate: str
    startup: str


GetFactsResponse = ApiResponse[DeviceFacts]
GetConfigResponse = ApiResponse[MyResponse]
GetRouteToResponse = ApiResponse[Dict[str, Any]]
AddStaticRouteResponse = ApiResponse[ConfigApplyResult]
