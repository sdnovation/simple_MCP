from catalystcentersdk import CatalystCenterAPI
from typing import Any
from fastmcp import FastMCP
import config
import asyncio
import json
from netmiko import ConnectHandler

mcp = FastMCP("CatCen MCP")


CatCen = CatalystCenterAPI(username = config.USERNAME,
                                  password = config.PASSWORD,
                                  base_url=config.URL,
                                  verify=False)

def _json_deobjectations(o: Any) -> Any:
    """
    take the mydict object and convert it to plain dict if it is a pydantic object with dict
    """
    if hasattr(o, "dict"):
      return o.dict()




@mcp.tool()
async def getDevices() -> list[dict[str, Any]]:
    """
    tool for accessing Cisco devices over the Catalyst Center (former DNA Center). You also get a lot of attributes per device
    using this you will get a list of all devices. within the list you can read the attribues like the device name, IP Address or Name
    example output:
    [{'airQualityHealth': {}, 'band': {}, 'clientCount': {}, 'cpuHealth': -1, 'deviceFamily': 'SWITCHES_AND_HUBS', 'deviceType': 'Cisco Catalyst 9000 UADP 8 Port Virtual Switch', 'freeMemoryBufferHealth': -1, 'freeTimerScore': -1, 'interDeviceLinkAvailFabric': -1, 'interDeviceLinkAvailHealth': 0, 'interfaceLinkErrHealth': -1, 'interferenceHealth': {}, 'ipAddress': '192.168.1.10', 'issueCount': 1, 'location': 'Global/Germany/Ingolstadt/Audi_AG/E1', 'macAddress': '52:54:00:32:88:B7', 'memoryUtilizationHealth': -1.0, 'model': 'Cisco Catalyst 9000 UADP 8 Port Virtual Switch', 'name': 'Border1', 'noiseHealth': {}, 'osVersion': '17.15.1', 'overallHealth': -2, 'packetPoolHealth': -1, 'reachabilityHealth': 'UNREACHABLE', 'utilizationHealth': {}, 'uuid': '97a78a52-0080-47e1-8168-066c810b5874', 'wanLinkUtilization': -1.0, 'wqePoolsHealth': -1}, {'airQualityHealth': {}, 'band': {}, 'clientCount': {}, 'cpuHealth': 10, 'cpuUlitilization': 53.25, 'cpuUtilization': 53.25, 'deviceFamily': 'SWITCHES_AND_HUBS', 'deviceType': 'Cisco Catalyst 9000 UADP 8 Port Virtual Switch', 'freeMemoryBufferHealth': -1, 'freeTimerScore': -1, 'interDeviceLinkAvailFabric': 10, 'interDeviceLinkAvailHealth': 100, 'interfaceLinkErrHealth': 10, 'interferenceHealth': {}, 'ipAddress': '192.168.30.10', 'issueCount': 1, 'location': 'Global/Germany/Ingolstadt/Audi_AG/E1', 'macAddress': '52:54:00:5B:04:83', 'memoryUtilization': 71, 'memoryUtilizationHealth': 10.0, 'model': 'Cisco Catalyst 9000 UADP 8 Port Virtual Switch', 'name': 'Edge1', 'noiseHealth': {}, 'osVersion': '17.15.1', 'overallHealth': 1, 'packetPoolHealth': -1, 'reachabilityHealth': 'REACHABLE', 'utilizationHealth': {}, 'uuid': 'a73da940-0d12-450c-b7dc-6f3622357d44', 'wanLinkUtilization': -1.0, 'wqePoolsHealth': -1}, {'airQualityHealth': {}, 'band': {}, 'clientCount': {}, 'cpuHealth': 10, 'cpuUlitilization': 53.25, 'cpuUtilization': 53.25, 'deviceFamily': 'SWITCHES_AND_HUBS', 'deviceType': 'Cisco Catalyst 9000 UADP 8 Port Virtual Switch', 'freeMemoryBufferHealth': -1, 'freeTimerScore': -1, 'interDeviceLinkAvailFabric': 10, 'interDeviceLinkAvailHealth': 100, 'interfaceLinkErrHealth': 10, 'interferenceHealth': {}, 'ipAddress': '192.168.30.5', 'issueCount': 2, 'location': 'Global/Germany/Ingolstadt/Audi_AG/E1', 'macAddress': '52:54:00:4D:51:AF', 'memoryUtilization': 71, 'memoryUtilizationHealth': 10.0, 'model': 'Cisco Catalyst 9000 UADP 8 Port Virtual Switch', 'name': 'Border2', 'noiseHealth': {}, 'osVersion': '17.15.1', 'overallHealth': 1, 'packetPoolHealth': -1, 'reachabilityHealth': 'REACHABLE', 'utilizationHealth': {}, 'uuid': 'b535614c-bcef-4ffe-98fd-ab8a304a676b', 'wanLinkUtilization': -1.0, 'wqePoolsHealth': -1}]
    """
    devices = await asyncio.to_thread(CatCen.devices.devices)
    #iterate trough the list and make a json string, if it is not possible, use _json_deobjectication
    #after that load the tring back to json
    return json.loads(json.dumps(devices.response, default=_json_deobjectations))






@mcp.tool()
async def getDeviceConfig(host: str, ) -> str:
   """
   use the IP Address of a device to ssh into it. Username and Password are already present in this tool.
   It will return the full running-configuration of the Cisco Device
   """
   device = {
    "device_type": "cisco_ios",      
    "host": host,
    "username": config.SSH_USERNAME,
    "password": config.SSH_PASSWORD
    }
   
   try:
    with ConnectHandler(**device) as conn:
        # If the device needs enable mode:
        # if device.get("secret"): conn.enable()

        running_cfg = conn.send_command("show running-config", use_textfsm=False)
        #return running_cfg
        return json.loads(json.dumps(running_cfg, default=_json_deobjectations))

   except Exception as e:
      return f"Connection failed. Reason: {e}"
   





if __name__ == "__main__":
   mcp.run(transport="http", port=8002, log_level="DEBUG")
   
   