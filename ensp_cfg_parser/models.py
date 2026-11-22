from pydantic import BaseModel, Field
from typing import List, Optional


class Interface(BaseModel):
    name: str
    ip: Optional[str] = None
    mask: Optional[str] = None
    vlan: Optional[str] = None
    description: Optional[str] = None


class StaticRoute(BaseModel):
    destination: str
    mask: str
    next_hop: str


class Device(BaseModel):
    hostname: str
    device_type: Optional[str] = None
    version: Optional[str] = None
    interfaces: List[Interface] = Field(default_factory=list)
    static_routes: List[StaticRoute] = Field(default_factory=list)
