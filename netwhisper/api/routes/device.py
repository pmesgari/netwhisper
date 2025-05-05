from fastapi import APIRouter

from netwhisper.api.models import (
    AddStaticRouteRequest,
    AddStaticRouteResponse,
    DeviceFacts,
    GetConfigRequest,
    GetConfigResponse,
    GetFactsRequest,
    GetFactsResponse,
    GetRouteToRequest,
    GetRouteToResponse,
)
from netwhisper.device import DeviceService, device_session

router = APIRouter()


@router.post("/get_facts", response_model=GetFactsResponse)
def get_facts(request: GetFactsRequest):
    """
    Retrieve device facts.
    
    Example:
        curl -X POST "http://localhost:8000/device/get_facts" \
            -H "accept: application/json" \
            -H "Content-Type: application/json" \
            -d '{
                "device": {
                    "name": "sw01",
                    "hostname": "134.149.24.155",
                    "username": "admin",
                    "password": "admin",
                    "driver": "eos",
                    "optional_args": {
                        "port": 8081
                    }
                }
            }'
    """
    with device_session(request.device) as session:
        facts = DeviceService.get_facts(session)
        return GetFactsResponse(
            success=True,
            message="Facts retrieved",
            data=DeviceFacts(**facts),
        )


@router.post("/get_config", response_model=GetConfigResponse)
def get_config(request: GetConfigRequest):
    """
    Retrieve the running configuration from the device.
    
    Example:
        curl -X POST "http://localhost:8000/device/get_config" \
            -H "accept: application/json" \
            -H "Content-Type: application/json" \
            -d '{
                "device": {
                    "name": "sw01",
                    "hostname": "134.149.24.155",
                    "username": "admin",
                    "password": "admin",
                    "driver": "eos",
                    "optional_args": {
                        "port": 8081
                    }
                }
            }'
    """
    with device_session(request.device) as session:
        config = DeviceService.get_config(session)
        return GetConfigResponse(
            success=True,
            message="Config retrieved successfully",
            data=config,
        )


@router.post("/get_route_to", response_model=GetRouteToResponse)
def get_route_to(request: GetRouteToRequest):
    """
    Return all available routes to a destination.

    Example:
        curl -X POST "http://localhost:8000/device/get_route_to" \
            -H "accept: application/json" \
            -H "Content-Type: application/json" \
            -d '{
                "device": {
                    "name": "sw01",
                    "hostname": "134.149.24.155",
                    "username": "admin",
                    "password": "admin",
                    "driver": "eos",
                    "optional_args": {
                        "port": 8081
                    }
                },
                "destination": "1.1.1.0/24"
            }'
    """
    with device_session(request.device) as session:
        routes = DeviceService.get_route_to(session, request.destination, request.protocol)
        return GetRouteToResponse(
            success=True,
            message="Routes retrieved successfully",
            data=routes,
        )


@router.post("/add_static_route", response_model=AddStaticRouteResponse)
def add_static_route(request: AddStaticRouteRequest):
    """
    Add a static route to the device.

    Example:
        curl -X POST "http://localhost:8000/device/add_static_route" \
            -H "accept: application/json" \
            -H "Content-Type: application/json" \
            -d '{
                "device": {
                    "name": "sw01",
                    "hostname": "134.149.24.155",
                    "username": "admin",
                    "password": "admin",
                    "driver": "eos",
                    "optional_args": {
                        "port": 8081
                    }
                },
                "destination": "1.1.1.0/24",
                "next_hop": "10.0.0.2",
                "show_diff": true,
                "commit": false
            }'
    """
    with device_session(request.device) as session:
        ret = DeviceService.add_static_route(
            session,
            request.destination,
            request.next_hop,
            request.show_diff,
            request.commit,
        )
        return AddStaticRouteResponse(
            success=True,
            message=f"Static route {request.destination} via {request.next_hop} added",
            data=ret,
        )
