#!/usr/bin/env python3

"""
Copyright © 2022 MetaX Integrated Circuits (Shanghai) Co., Ltd. All Rights Reserved.

This software and associated documentation files (hereinafter collectively referred to as
"Software") is a proprietary commercial software developed by MetaX Integrated Circuits
(Shanghai) Co., Ltd. and/or its affiliates (hereinafter collectively referred to as “MetaX”).
The information presented in the Software belongs to MetaX. Without prior written permission
from MetaX, no entity or individual has the right to obtain a copy of the Software to deal in
the Software, including but not limited to use, copy, modify, merge, disclose, publish,
distribute, sublicense, and/or sell copies of the Software or substantial portions of the Software.

The Software is provided for reference only, without warranty of any kind, either express or
implied, including but not limited to the warranty of merchantability, fitness for any purpose
and/or noninfringement. In no case shall MetaX be liable for any claim, damage or other liability
arising from, out of or in connection with the Software.

If the Software need to be used in conjunction with any third-party software or open source
software, the rights to the third-party software or open source software still belong to the
copyright owners. For details, please refer to the respective notices or licenses. Please comply
with the provisions of the relevant notices or licenses. If the open source software licenses
additionally require the disposal of rights related to this Software, please contact MetaX
immediately and obtain MetaX 's written consent.

MetaX reserves the right, at its sole discretion, to change, modify, add or remove portions of the
Software, at any time. MetaX reserves all the right for the final explanation.
"""

from ctypes import *
import os

path_libmxsml = ""
path_libmxsml_array = [
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "libmxsml.so"
    ),
    "/opt/mxdriver/lib/libmxsml.so",
    "/opt/maca/lib/libmxsml.so",
    "/opt/mxn100/lib/libmxsml.so"
]
for file in path_libmxsml_array:
    if os.path.isfile(file):
        print("Using lib from %s" % file)
        path_libmxsml = file
        break

if not path_libmxsml:
    print("Unable to find mxsml library.")
    exit(1)

try:
    mxsml = cdll.LoadLibrary(path_libmxsml)
except OSError:
    print("Unable to load mxsml library.")
    exit(1)

DeviceId = c_uint
DieId = c_uint
SgpuId = c_uint

class MxSmlReturn(c_uint):
    MXSML_Success = 0
    MXSML_Failure = 1
    MXSML_NoDevice = 2
    MXSML_OperationNotSupport = 3
    MXSML_SysfsError = 4
    MXSML_SysfsWriteError = 5
    MXSML_InvalidDeviceId = 6
    MXSML_InvalidDieId = 7
    MXSML_PermissionDenied = 8
    MXSML_InvalidInput = 9
    MXSML_InsufficientSize = 10
    MXSML_Reserved3 = 11
    MXSML_IOControlFailure = 12
    MXSML_MmapFailure = 13
    MXSML_UnMmapFailure = 14
    MXSML_InvalidInputForMmap = 15
    MXSML_Reserved1 = 16
    MXSML_Reserved2 = 17
    MXSML_TargetVfNotFound = 18
    MXSML_InvalidFrequency = 19
    MXSML_FlrNotReady = 20
    MXSML_OpenDeviceFileFailure = 21
    MXSML_CloseDeviceFileFailure = 22
    MXSML_BusyDevice = 23
    MXSML_MmioNotEnough = 24
    MXSML_GetPciBridgeFailure = 25
    MXSML_LoadDllFailure = 26

class MxSmlDeviceBrand(c_uint):
    MXSML_Brand_Unknown = 0
    MXSML_Brand_N = 1
    MXSML_Brand_C = 2
    MXSML_Brand_G = 3
    MXSML_Brand_X = 4

class MxSmlDeviceVirtualizationMode(c_uint):
    MXSML_Virtualization_Mode_None = 0
    MXSML_Virtualization_Mode_Pf = 1
    MXSML_Virtualization_Mode_Vf = 2

class MxSmlRasIp(c_uint):
    MXSML_Ras_mc = 0
    MXSML_Ras_pcie = 1
    MXSML_Ras_fuse = 2
    MXSML_Ras_g2d = 3
    MXSML_Ras_int = 4
    MXSML_Ras_hag = 5
    MXSML_Ras_metalk = 6
    MXSML_Ras_smp0 = 7
    MXSML_Ras_smp1 = 8
    MXSML_Ras_ccx0 = 9
    MXSML_Ras_ccx1 = 10
    MXSML_Ras_ccx2 = 11
    MXSML_Ras_ccx3 = 12
    MXSML_Ras_dla0 = 13
    MXSML_Ras_dla1 = 14
    MXSML_Ras_vpue0 = 15
    MXSML_Ras_vpue1 = 16
    MXSML_Ras_vpud0 = 17
    MXSML_Ras_vpud1 = 18
    MXSML_Ras_vpud2 = 19
    MXSML_Ras_vpud3 = 20
    MXSML_Ras_vpud4 = 21
    MXSML_Ras_vpud5 = 22
    MXSML_Ras_vpud6 = 23
    MXSML_Ras_vpud7 = 24
    MXSML_Ras_dma0 = 25
    MXSML_Ras_dma1 = 26
    MXSML_Ras_dma2 = 27
    MXSML_Ras_dma3 = 28
    MXSML_Ras_dma4 = 29
    MXSML_Ras_mcctl0 = 30
    MXSML_Ras_mcctl1 = 31
    MXSML_Ras_mcctl2 = 32
    MXSML_Ras_mcctl3 = 33
    MXSML_Ras_dhub1 = 34
    MXSML_Ras_dhub2 = 35
    MXSML_Ras_dhub3 = 36
    MXSML_Ras_dhub4 = 37
    MXSML_Ras_dhub5 = 38
    MXSML_Ras_dhub6 = 39
    MXSML_Ras_dhub7 = 40
    MXSML_Ras_ath = 41
    MXSML_Ras_atul20 = 42
    MXSML_Ras_atul21 = 43
    MXSML_Ras_xsc = 44
    MXSML_Ras_ce = 45
    MXSML_Ras_eth = 46
    MXSML_Ras_ethsc = 47

class MxSmlVersionUnit(c_uint):
    MXSML_Version_Bios = 0
    MXSML_Version_Driver = 1
    MXSML_Version_Smp0 = 2
    MXSML_Version_Smp1 = 3
    MXSML_Version_Ccx0 = 4
    MXSML_Version_Ccx1 = 5
    MXSML_Version_Ccx2 = 6
    MXSML_Version_Ccx3 = 7        # only valid for N-class device

class MxSmlUsageIp(c_uint):
    MXSML_Usage_Dla = 0           # only valid for N-class device
    MXSML_Usage_Vpue = 1
    MXSML_Usage_Vpud = 2
    MXSML_Usage_G2d = 3           # only valid for N-class device
    MXSML_Usage_Xcore = 4         # only valid for C-class device
    MXSML_Usage_Mma = 5           # only valid for C-class device

class MxSmlLinkErrorCounterType(c_uint):
    MXSML_Link_Error_Replay = 0
    MXSML_Link_Error_Recovery = 1
    MXSML_Link_Error_Crc = 2
    MXSML_Link_Error_Max = 3

class MxSmlDeviceInfo(Structure):
    _fields_ = [
        ("deviceId", DeviceId),
        ("type", c_uint),         # deprecated, do not use
        ("bdfId", c_char*32),
        ("gpuId", c_uint),
        ("nodeId", c_uint),
        ("uuid", c_char*96),
        ("brand", c_uint),
        ("mode", c_uint),
        ("deviceName", c_char*32)
    ]

class MxSmlRasErrorRegister(Structure):
    _fields_ = [
        ("rasIp", MxSmlRasIp),
        ("registerIndex", c_uint),
        ("rasErrorUe", c_int),
        ("rasErrorCe", c_int)
    ]

class MxSmlRasErrorData(Structure):
    _fields_ = [
        ("rasErrorRegister", MxSmlRasErrorRegister*128),
        ("showRasErrorSize", c_int)
    ]

class MxSmlRasRegister(Structure):
    _fields_ = [
        ("rasIp", MxSmlRasIp),
        ("registerIndex", c_uint),
        ("registerData", c_int)
    ]

class MxSmlRasStatusData(Structure):
    _fields_ = [
        ("rasStatusRegister", MxSmlRasRegister*128),
        ("showRasStatusSize", c_int)
    ]

class MxSmlVirtualDeviceIds(Structure):
    _fields_ = [
        ("number", c_int),
        ("deviceId", c_int*128)
    ]

class MxSmlTemperatureSensors(c_uint):
    MXSML_Temperature_Hotspot = 0
    MXSML_Temperature_HotLimit = 1
    MXSML_Temperature_Soc = 2
    MXSML_Temperature_Core = 3
    MXSML_Temperature_Ccx_Dnoc = 4
    MXSML_Temperature_Csc_Fuse = 5
    MXSML_Temperature_Ccx_Dla_Vpue1_Ath = 6
    MXSML_Temperature_Vpue1 = 7
    MXSML_Temperature_Vpue0 = 8
    MXSML_Temperature_Atul2 = 9
    MXSML_Temperature_Dla1 = 10
    MXSML_Temperature_Dla0 = 11
    MXSML_Temperature_Emc0 = 12
    MXSML_Temperature_Emc1 = 13
    MXSML_Temperature_Sgm = 14
    MXSML_Temperature_Hbm = 15

class MxSmlHbmBandwidth(Structure):
    _fields_ = [
        ("hbmBandwidthReqTotal", c_int),
        ("hbmBandwidthRespTotal", c_int)
    ]

class MxSmlMemoryInfo(Structure):
    _fields_ = [
        ("visVramTotal", c_long),
        ("visVramUse", c_long),
        ("vramTotal", c_long),
        ("vramUse", c_long),
        ("xttTotal", c_long),
        ("xttUse", c_long)
    ]

class MxSmlPmbusUnit(c_uint):
    MXSML_Pmbus_Soc = 0
    MXSML_Pmbus_Core = 1
    MXSML_Pmbus_Hbm = 2
    MXSML_Pmbus_Pcie = 3
    MXSML_Pmbus_Hbm2 = 4
    MXSML_Pmbus_Pcie2 = 5

class MxSmlPmbusInfo(Structure):
    _fields_ = [
        ("voltage", c_uint),
        ("current", c_uint),
        ("power", c_uint)
    ]

class MxSmlBoardWayElectricInfo(Structure):
    _fields_ = [
        ("voltage", c_uint),
        ("current", c_uint),
        ("power", c_uint)
    ]

class MxSmlClockIp(c_uint):
    MXSML_Clock_Csc = 0
    MXSML_Clock_Dla = 1
    MXSML_Clock_Mc = 2
    MXSML_Clock_Mc0 = 3
    MXSML_Clock_Mc1 = 4
    MXSML_Clock_Vpue = 5
    MXSML_Clock_Vpud = 6
    MXSML_Clock_Soc = 7
    MXSML_Clock_Dnoc = 8
    MXSML_Clock_G2D = 9
    MXSML_Clock_Ccx = 10
    MXSML_Clock_Xcore = 11

class MxSmlFwIp(c_uint):
    MXSML_Fw_IpName_SMP0 = 0
    MXSML_Fw_IpName_SMP1 = 1
    MXSML_Fw_IpName_CCX0 = 2
    MXSML_Fw_IpName_CCX1 = 3
    MXSML_Fw_IpName_CCX2 = 4
    MXSML_Fw_IpName_CCX3 = 5

class MxSmlLoglevel(c_uint):
    MXSML_Loglevel_NONE = 0
    MXSML_Loglevel_FATAL = 1
    MXSML_Loglevel_ERROR = 2
    MXSML_Loglevel_WARN = 3
    MXSML_Loglevel_INFO = 4
    MXSML_Loglevel_DEBUG = 5
    MXSML_Loglevel_VERBOSE = 6
    MXSML_Loglevel_UNKNOWN = 7

class MxSmlDpmIp(c_uint):
    MXSML_Dpm_Dla = 0
    MXSML_Dpm_Xcore = 1
    MXSML_Dpm_Mc = 2
    MXSML_Dpm_Soc = 3
    MXSML_Dpm_Dnoc = 4
    MXSML_Dpm_Vpue = 5
    MXSML_Dpm_Vpud = 6
    MXSML_Dpm_Hbm = 7
    MXSML_Dpm_G2d = 8
    MXSML_Dpm_Ravs = 9
    MXSML_Dpm_Tdc = 10
    MXSML_Dpm_Pcc = 11
    MXSML_Dpm_HbmPower = 12
    MXSML_Dpm_Ccx = 13
    MXSML_Dpm_Ip_Group = 14
    MXSML_Dpm_Dma = 15
    MXSML_Dpm_Csc = 16

class MxSmlMetaXLinkState(c_uint):
    MXSML_MetaXLink_State_Enabled = 0
    MXSML_MetaXLink_State_Smi_Disabled = 1
    MXSML_MetaXLink_State_Vf_Disabled = 2
    MXSML_MetaXLink_State_GpuNum_Disabled = 3
    MXSML_MetaXLink_State_Training_Disabled = 4

class MxSmlMxlkPortState(c_uint):
    MXSML_Mxlk_Port_State_NoTraining = 0
    MXSML_Mxlk_Port_State_Up = 1
    MXSML_Mxlk_Port_State_Down_Optical_InPlace = 2
    MXSML_Mxlk_Port_State_Down_Optical_OutPlace = 3
    MXSML_Mxlk_Port_State_Down_Optical_NoUse = 4
    MXSML_Mxlk_Port_State_NoUse = 5

class MxSmlClockThrottleType(c_uint):
    MXSML_CLK_THROTTLE_OVER_CURRENT = 0
    MXSML_CLK_THROTTLE_OVER_VOLTAGE = 1
    MXSML_CLK_THROTTLE_POWER_BRAKE = 2

class MxSmlPcieThroughput(Structure):
    _fields_ = [
        ("rx", c_int),
        ("tx", c_int)
    ]

class MxSmlDmaEngineBandwidth(Structure):
    _fields_ = [
        ("readReqBandwidth", c_int),
        ("readRespBandwidth", c_int),
        ("writeReqBandwidth", c_int),
        ("writeRespBandwidth", c_int)
    ]

class MxSmlProcessGpuInfo(Structure):
    _fields_ = [
        ("bdfId", c_char*32),
        ("gpuId", c_uint),
        ("gpuMemoryUsage", c_ulong)
    ]

class MxSmlProcessInfo(Structure):
    _fields_ = [
        ("processId", c_uint),
        ("processName", c_char*64),
        ("gpuNumber", c_uint),
        ("processGpuInfo", MxSmlProcessGpuInfo*64)
    ]

class MxSmlProcessGpuInfo_v2(Structure):
    _fields_ = [
        ("bdfId", c_char*32),
        ("gpuId", c_uint),
        ("gpuMemoryUsage", c_ulong),
        ("dieId", c_uint)
    ]

class MxSmlProcessInfo_v2(Structure):
    _fields_ = [
        ("processId", c_uint),
        ("processName", c_char*64),
        ("gpuNumber", c_uint),
        ("processGpuInfo", MxSmlProcessGpuInfo_v2*64)
    ]

class MxSmlProcessGpuInfo_v3(Structure):
    _fields_ = [
        ("bdfId", c_char*32),
        ("gpuId", c_uint),
        ("gpuMemoryUsage", c_ulong),
        ("dieId", c_uint),
        ("sgpuId", c_uint)
    ]

class MxSmlProcessInfo_v3(Structure):
    _fields_ = [
        ("processId", c_uint),
        ("processName", c_char*64),
        ("gpuNumber", c_uint),
        ("processGpuInfo", MxSmlProcessGpuInfo_v3*64)
    ]

class MxSmlMetaXLinkType(c_uint):
    MXSML_MetaXLink_Input = 0
    MXSML_MetaXLink_Target = 1

class MxSmlMetaXLinkBandwidth(Structure):
    _fields_ = [
        ("requestBandwidth", c_int),
        ("reponseBandwidth", c_int)
    ]

class MxSmlMetaXLinkTrafficStat(Structure):
    _fields_ = [
        ("requestTrafficStat", c_long),
        ("reponseTrafficStat", c_long)
    ]

class MxSmlMetaXLinkAer(Structure):
    _fields_ = [
        ("ceAer", c_int),
        ("ueAer", c_int)
    ]

METAX_LINK_NUM=7
class MxSmlMetaXLinkInfo(Structure):    # deprecated
    _fields_ = [
        ("speed", c_float * METAX_LINK_NUM),
        ("width", c_uint * METAX_LINK_NUM)
    ]

class MxSmlSingleMetaXLinkInfo(Structure):
    _fields_ = [
        ("speed", c_float),
        ("width", c_uint)
    ]

class MxSmlPcieInfo(Structure):
    _fields_ = [
        ("speed", c_float),
        ("width", c_uint)
    ]

class MxSmlOpticalModuleStatus(Structure):
    _fields_ = [
        ("temperature", c_int),
        ("voltage", c_uint),
        ("moduleState", c_uint),
        ("dataPathState", c_uint),
        ("rxState", c_uint*2),
        ("version", c_uint*2)
    ]

class MxSmlPciEventType(c_uint):
    MXSML_Pci_Event_AER_UE = 0
    MXSML_Pci_Event_AER_CE = 1
    MXSML_Pci_Event_SYNFLD = 2
    MXSML_Pci_Event_DBE = 3
    MXSML_Pci_Event_MMIO = 4

class MxSmlPciEventInfo(Structure):
    _fields_ = [
        ("bitNumber", c_int),
        ("count", c_uint),
        ("firstTime", c_char*20),
        ("name", c_char*64)
    ]

class MxSmlSgpuInfo(Structure):
    _fields_ = [
        ("parentDeviceId", c_uint),
        ("sgpuId", c_uint),
        ("vramQuota", c_uint),
        ("swQueuePriority", c_uint),
        ("computeQuota", c_uint),
        ("minor", c_uint),
        ("deviceQueuePriority", c_uint),
        ("uuid", c_char*94)
    ]

class MxSmlSgpuMemoryInfo(Structure):
    _fields_ = [
        ("total", c_long),
        ("used", c_long),
        ("free", c_long)
    ]

class MxSmlEccErrorCount(Structure):
    _fields_ = [
        ("sramCE", c_uint),
        ("sramUE", c_uint),
        ("dramCE", c_uint),
        ("dramUE", c_uint),
        ("retiredPage", c_uint)
    ]

class MxSmlMetaXLinkTopo(Structure):
    _fields_ = [
        ("topologyId", c_uint),
        ("socketId", c_uint),
        ("dieId", c_uint)
    ]

class MxSmlDeviceUnavailableReasonInfo(Structure):
    _fields_ = [
        ("unavailableCode", c_int),
        ("unavailableReason", c_char*64)
    ]

class MxSmlEthThroughput(Structure):
    _fields_ = [
        ("rx", c_int),
        ("tx", c_int),
    ]

class MxSmlLimitedDeviceIds(Structure):
    _fields_ = [
        ("number", c_int),
        ("deviceId", c_int*128),
    ]

mxSmlInit = mxsml.mxSmlInit
mxSmlInit.restype = c_uint

mxSmlInitWithFlags = mxsml.mxSmlInitWithFlags
mxSmlInitWithFlags.argtypes = [c_uint]
mxSmlInitWithFlags.restype = c_uint

mxSmlGetMacaVersion = mxsml.mxSmlGetMacaVersion
mxSmlGetMacaVersion.argtypes = [POINTER(c_char), POINTER(c_uint)]
mxSmlGetMacaVersion.restype = c_uint

mxSmlGetDeviceCount = mxsml.mxSmlGetDeviceCount
mxSmlGetDeviceCount.restype = c_uint

mxSmlGetPfDeviceCount = mxsml.mxSmlGetPfDeviceCount
mxSmlGetPfDeviceCount.restype = c_uint

mxSmlGetDeviceDieCount = mxsml.mxSmlGetDeviceDieCount
mxSmlGetDeviceDieCount.argtypes = [DeviceId, POINTER(c_uint)]
mxSmlGetDeviceDieCount.restype = c_uint

mxSmlGetVirtualDevicesByPhysicalId = mxsml.mxSmlGetVirtualDevicesByPhysicalId
mxSmlGetVirtualDevicesByPhysicalId.argtypes = [DeviceId, POINTER(MxSmlVirtualDeviceIds)]
mxSmlGetVirtualDevicesByPhysicalId.restype = c_uint

mxSmlGetDeviceInfo = mxsml.mxSmlGetDeviceInfo
mxSmlGetDeviceInfo.argtypes = [DeviceId, POINTER(MxSmlDeviceInfo)]
mxSmlGetDeviceInfo.restype = c_uint

mxSmlGetAllLimitedDevices = mxsml.mxSmlGetAllLimitedDevices
mxSmlGetAllLimitedDevices.argtypes = [POINTER(MxSmlLimitedDeviceIds)]
mxSmlGetAllLimitedDevices.restype = c_uint

mxSmlGetLimitedDeviceInfo = mxsml.mxSmlGetLimitedDeviceInfo
mxSmlGetLimitedDeviceInfo.argtypes = [DeviceId, POINTER(MxSmlDeviceInfo)]
mxSmlGetLimitedDeviceInfo.restype = c_uint

mxSmlGetRasErrorData = mxsml.mxSmlGetRasErrorData
mxSmlGetRasErrorData.argtypes = [DeviceId, POINTER(MxSmlRasErrorData)]
mxSmlGetRasErrorData.restype = c_uint

mxSmlGetDieRasErrorData = mxsml.mxSmlGetDieRasErrorData
mxSmlGetDieRasErrorData.argtypes = [DeviceId, DieId, POINTER(MxSmlRasErrorData)]
mxSmlGetDieRasErrorData.restype = c_uint

mxSmlGetRasStatusData = mxsml.mxSmlGetRasStatusData
mxSmlGetRasStatusData.argtypes = [DeviceId, POINTER(MxSmlRasStatusData)]
mxSmlGetRasStatusData.restype = c_uint

mxSmlGetDieRasStatusData = mxsml.mxSmlGetDieRasStatusData
mxSmlGetDieRasStatusData.argtypes = [DeviceId, DieId, POINTER(MxSmlRasStatusData)]
mxSmlGetDieRasStatusData.restype = c_uint

mxSmlGetTemperatureInfo = mxsml.mxSmlGetTemperatureInfo
mxSmlGetTemperatureInfo.argtypes = [DeviceId, MxSmlTemperatureSensors, POINTER(c_int)]
mxSmlGetTemperatureInfo.restype = c_uint

mxSmlGetDieTemperatureInfo = mxsml.mxSmlGetDieTemperatureInfo
mxSmlGetDieTemperatureInfo.argtypes = [DeviceId, DieId, MxSmlTemperatureSensors, POINTER(c_int)]
mxSmlGetDieTemperatureInfo.restype = c_uint

mxSmlGetHbmBandWidth = mxsml.mxSmlGetHbmBandWidth
mxSmlGetHbmBandWidth.argtypes = [DeviceId, POINTER(MxSmlHbmBandwidth)]
mxSmlGetHbmBandWidth.restype = c_uint

mxSmlGetDieHbmBandWidth = mxsml.mxSmlGetDieHbmBandWidth
mxSmlGetDieHbmBandWidth.argtypes = [DeviceId, DieId, POINTER(MxSmlHbmBandwidth)]
mxSmlGetDieHbmBandWidth.restype = c_uint

mxSmlGetDieHbmBandwidthUtilization = mxsml.mxSmlGetDieHbmBandwidthUtilization
mxSmlGetDieHbmBandwidthUtilization.argtypes = [DeviceId, DieId, POINTER(c_uint)]
mxSmlGetDieHbmBandwidthUtilization.restype = c_uint

mxSmlGetMemoryInfo = mxsml.mxSmlGetMemoryInfo
mxSmlGetMemoryInfo.argtypes = [DeviceId, POINTER(MxSmlMemoryInfo)]
mxSmlGetMemoryInfo.restype = c_uint

mxSmlGetDieMemoryInfo = mxsml.mxSmlGetDieMemoryInfo
mxSmlGetDieMemoryInfo.argtypes = [DeviceId, DieId, POINTER(MxSmlMemoryInfo)]
mxSmlGetDieMemoryInfo.restype = c_uint

mxSmlGetPmbusInfo = mxsml.mxSmlGetPmbusInfo
mxSmlGetPmbusInfo.argtypes = [DeviceId, MxSmlPmbusUnit, POINTER(MxSmlPmbusInfo)]
mxSmlGetPmbusInfo.restype = c_uint

mxSmlGetDiePmbusInfo = mxsml.mxSmlGetDiePmbusInfo
mxSmlGetDiePmbusInfo.argtypes = [DeviceId, DieId, MxSmlPmbusUnit, POINTER(MxSmlPmbusInfo)]
mxSmlGetDiePmbusInfo.restype = c_uint

mxSmlGetBoardPowerInfo = mxsml.mxSmlGetBoardPowerInfo
BoardWaySize = c_uint
mxSmlGetBoardPowerInfo.argtypes = [DeviceId, POINTER(BoardWaySize), POINTER(MxSmlBoardWayElectricInfo)]
mxSmlGetBoardPowerInfo.restypes = c_uint

mxSmlGetClocks = mxsml.mxSmlGetClocks
clocksSize = c_uint
mxSmlGetClocks.argtypes = [DeviceId, MxSmlClockIp, POINTER(clocksSize), POINTER(c_uint)]
mxSmlGetClocks.restypes = c_uint

mxSmlGetDieClocks = mxsml.mxSmlGetDieClocks
clocksSize = c_uint
mxSmlGetDieClocks.argtypes = [DeviceId, DieId, MxSmlClockIp, POINTER(clocksSize), POINTER(c_uint)]
mxSmlGetDieClocks.restypes = c_uint

mxSmlGetPcieThroughput = mxsml.mxSmlGetPcieThroughput
mxSmlGetPcieThroughput.argtypes = [DeviceId, POINTER(MxSmlPcieThroughput)]
mxSmlGetPcieThroughput.restype = c_uint

mxSmlGetDmaBandwidth = mxsml.mxSmlGetDmaBandwidth
DmaBandwidthSize = c_uint
mxSmlGetDmaBandwidth.argtypes = [DeviceId, POINTER(MxSmlDmaEngineBandwidth), POINTER(DmaBandwidthSize)]
mxSmlGetDmaBandwidth.restype = c_uint

mxSmlGetNumberOfProcess = mxsml.mxSmlGetNumberOfProcess
mxSmlGetNumberOfProcess.argtypes = [POINTER(c_uint)]
mxSmlGetNumberOfProcess.restype = c_uint

mxSmlGetProcessInfo = mxsml.mxSmlGetProcessInfo
mxSmlGetProcessInfo.argtypes = [c_uint, POINTER(MxSmlProcessInfo)]
mxSmlGetProcessInfo.restype = c_uint

mxSmlGetProcessInfo_v2 = mxsml.mxSmlGetProcessInfo_v2
mxSmlGetProcessInfo_v2.argtypes = [c_uint, POINTER(MxSmlProcessInfo_v2)]
mxSmlGetProcessInfo_v2.restype = c_uint

mxSmlGetSingleGpuProcess = mxsml.mxSmlGetSingleGpuProcess
mxSmlGetSingleGpuProcess.argtypes = [c_uint, POINTER(c_uint), POINTER(MxSmlProcessInfo)]
mxSmlGetSingleGpuProcess.restype = c_uint

mxSmlGetSingleGpuProcess_v2 = mxsml.mxSmlGetSingleGpuProcess_v2
mxSmlGetSingleGpuProcess_v2.argtypes = [c_uint, POINTER(c_uint), POINTER(MxSmlProcessInfo_v2)]
mxSmlGetSingleGpuProcess_v2.restype = c_uint

mxSmlGetSingleGpuProcess_v3 = mxsml.mxSmlGetSingleGpuProcess_v3
mxSmlGetSingleGpuProcess_v3.argtypes = [c_uint, POINTER(c_uint), POINTER(MxSmlProcessInfo_v3)]
mxSmlGetSingleGpuProcess_v3.restype = c_uint

mxSmlGetMetaXLinkBandwidth = mxsml.mxSmlGetMetaXLinkBandwidth
linkSize = c_uint
mxSmlGetMetaXLinkBandwidth.argtypes = [DeviceId, MxSmlMetaXLinkType, POINTER(linkSize), POINTER(MxSmlMetaXLinkBandwidth)]
mxSmlGetMetaXLinkBandwidth.restype = c_uint

mxSmlGetMetaXLinkTrafficStat = mxsml.mxSmlGetMetaXLinkTrafficStat
linkSize = c_uint
mxSmlGetMetaXLinkTrafficStat.argtypes = [DeviceId, MxSmlMetaXLinkType, POINTER(linkSize), POINTER(MxSmlMetaXLinkTrafficStat)]
mxSmlGetMetaXLinkTrafficStat.restype = c_uint

mxSmlGetMetaXLinkAer = mxsml.mxSmlGetMetaXLinkAer
linkSize = c_uint
mxSmlGetMetaXLinkAer.argtypes = [DeviceId, POINTER(linkSize), POINTER(MxSmlMetaXLinkAer)]
mxSmlGetMetaXLinkAer.restype = c_uint

# deprecated
mxSmlGetMetaXLinkInfo = mxsml.mxSmlGetMetaXLinkInfo
mxSmlGetMetaXLinkInfo.argtypes = [DeviceId, POINTER(MxSmlMetaXLinkInfo)]
mxSmlGetMetaXLinkInfo.restype = c_uint

mxSmlGetMetaXLinkInfo_v2 = mxsml.mxSmlGetMetaXLinkInfo_v2
linkSize = c_uint
mxSmlGetMetaXLinkInfo_v2.argtypes = [DeviceId, POINTER(linkSize), POINTER(MxSmlSingleMetaXLinkInfo)]
mxSmlGetMetaXLinkInfo_v2.restype = c_uint

mxSmlGetDpmIpClockInfo = mxsml.mxSmlGetDpmIpClockInfo
mxSmlGetDpmIpClockInfo.argtypes = [DeviceId, MxSmlDpmIp, POINTER(c_uint), POINTER(c_uint)]
mxSmlGetDpmIpClockInfo.restype = c_uint

mxSmlGetDpmIpVddInfo = mxsml.mxSmlGetDpmIpVddInfo
mxSmlGetDpmIpVddInfo.argtypes = [DeviceId, MxSmlDpmIp, POINTER(c_uint), POINTER(c_uint)]
mxSmlGetDpmIpVddInfo.restype = c_uint

mxSmlGetCurrentDpmIpPerfLevel = mxsml.mxSmlGetCurrentDpmIpPerfLevel
mxSmlGetCurrentDpmIpPerfLevel.argtypes = [DeviceId, MxSmlDpmIp, POINTER(c_uint)]
mxSmlGetCurrentDpmIpPerfLevel.restype = c_uint

mxSmlGetCurrentDieDpmIpPerfLevel = mxsml.mxSmlGetCurrentDieDpmIpPerfLevel
mxSmlGetCurrentDieDpmIpPerfLevel.argtypes = [DeviceId, DieId, MxSmlDpmIp, POINTER(c_uint)]
mxSmlGetCurrentDieDpmIpPerfLevel.restype = c_uint

mxSmlGetDeviceVersion = mxsml.mxSmlGetDeviceVersion
mxSmlGetDeviceVersion.argtypes = [DeviceId, c_uint, POINTER(c_char), POINTER(c_uint)]
mxSmlGetDeviceVersion.restype = c_uint

mxSmlGetDeviceDieVersion = mxsml.mxSmlGetDeviceDieVersion
mxSmlGetDeviceDieVersion.argtypes = [DeviceId, DieId, c_uint, POINTER(c_char), POINTER(c_uint)]
mxSmlGetDeviceDieVersion.restype = c_uint

mxSmlGetDeviceIpUsage = mxsml.mxSmlGetDeviceIpUsage
mxSmlGetDeviceIpUsage.argtypes = [DeviceId, c_uint, POINTER(c_int)]
mxSmlGetDeviceIpUsage.restype = c_uint

mxSmlGetDieIpUsage = mxsml.mxSmlGetDieIpUsage
mxSmlGetDieIpUsage.argtypes = [DeviceId, DieId, c_uint, POINTER(c_int)]
mxSmlGetDieIpUsage.restype = c_uint

mxSmlGetFwIpLoglevel = mxsml.mxSmlGetFwIpLoglevel
mxSmlGetFwIpLoglevel.argtypes = [DeviceId, c_uint, POINTER(c_uint)]
mxSmlGetFwIpLoglevel.restype = c_uint

mxSmlGetErrorString = mxsml.mxSmlGetErrorString
mxSmlGetErrorString.argtypes = [c_uint]
mxSmlGetErrorString.restype = c_char_p

mxSmlGetPcieInfo = mxsml.mxSmlGetPcieInfo
mxSmlGetPcieInfo.argtypes = [DeviceId, POINTER(MxSmlPcieInfo)]
mxSmlGetPcieInfo.restype = c_uint

mxSmlGetPcieMaxLinkInfo = mxsml.mxSmlGetPcieMaxLinkInfo
mxSmlGetPcieMaxLinkInfo.argtypes = [DeviceId, POINTER(MxSmlPcieInfo)]
mxSmlGetPcieMaxLinkInfo.restype = c_uint

mxSmlGetDeviceState = mxsml.mxSmlGetDeviceState
mxSmlGetDeviceState.argtypes = [DeviceId, POINTER(c_int)]
mxSmlGetDeviceState.restype = c_uint

mxSmlGetLocalAndRemoteUuid = mxsml.mxSmlGetLocalAndRemoteUuid
mxSmlGetLocalAndRemoteUuid.argtypes = [POINTER(c_char), POINTER(c_char), POINTER(c_uint)]
mxSmlGetLocalAndRemoteUuid.restype = c_uint

mxSmlGetLocalAndMultipleRemoteUuid = mxsml.mxSmlGetLocalAndMultipleRemoteUuid
mxSmlGetLocalAndMultipleRemoteUuid.argtypes = [POINTER(c_char), POINTER(POINTER(c_char)), POINTER(c_uint), POINTER(c_uint)]
mxSmlGetLocalAndMultipleRemoteUuid.restype = c_uint

mxSmlGetOpticalModuleStatus = mxsml.mxSmlGetOpticalModuleStatus
mxSmlGetOpticalModuleStatus.argtypes = [DeviceId, POINTER(MxSmlOpticalModuleStatus), POINTER(c_uint)]
mxSmlGetOpticalModuleStatus.restype = c_uint

mxSmlGetCurrentClocksThrottleReason = mxsml.mxSmlGetCurrentClocksThrottleReason
mxSmlGetCurrentClocksThrottleReason.argtypes = [DeviceId, POINTER(c_ulonglong)]
mxSmlGetCurrentClocksThrottleReason.restype = c_uint

mxSmlGetDieCurrentClocksThrottleReason = mxsml.mxSmlGetDieCurrentClocksThrottleReason
mxSmlGetDieCurrentClocksThrottleReason.argtypes = [DeviceId, DieId, POINTER(c_ulonglong)]
mxSmlGetDieCurrentClocksThrottleReason.restype = c_uint

mxSmlGetBoardPowerLimit = mxsml.mxSmlGetBoardPowerLimit
mxSmlGetBoardPowerLimit.argtypes = [DeviceId, POINTER(c_uint)]
mxSmlGetBoardPowerLimit.restype = c_uint

mxSmlGetBoardPowerLimitConstraints = mxsml.mxSmlGetBoardPowerLimitConstraints
mxSmlGetBoardPowerLimitConstraints.argtypes = [DeviceId, POINTER(c_uint), POINTER(c_uint)]
mxSmlGetBoardPowerLimitConstraints.restype = c_uint

mxSmlGetMetaXLinkState = mxsml.mxSmlGetMetaXLinkState
mxSmlGetMetaXLinkState.argTypes = [DeviceId, POINTER(MxSmlMetaXLinkState), POINTER(c_char), POINTER(c_uint)]
mxSmlGetMetaXLinkState.restype = c_uint

mxSmlGetMetaXLinkPortState = mxsml.mxSmlGetMetaXLinkPortState
mxSmlGetMetaXLinkPortState.argTypes = [DeviceId, POINTER(MxSmlMxlkPortState), POINTER(c_uint)]
mxSmlGetMetaXLinkPortState.restype = c_uint

mxSmlGetPciMmioState = mxsml.mxSmlGetPciMmioState
mxSmlGetPciMmioState.argTypes = [DeviceId, POINTER(c_uint)]
mxSmlGetPciMmioState.restype = c_uint

mxSmlGetPciEventInfo = mxsml.mxSmlGetPciEventInfo
mxSmlGetPciEventInfo.argTypes = [DeviceId, MxSmlPciEventType, POINTER(MxSmlPciEventInfo), POINTER(c_uint)]
mxSmlGetPciEventInfo.restype = c_uint

mxSmlGetBoardSerial = mxsml.mxSmlGetBoardSerial
mxSmlGetBoardSerial.argtypes = [DeviceId, POINTER(c_char), POINTER(c_uint)]
mxSmlGetBoardSerial.restype = c_uint

mxSmlGetDeviceIsaVersion = mxsml.mxSmlGetDeviceIsaVersion
mxSmlGetDeviceIsaVersion.argTypes = [DeviceId, POINTER(c_int)]
mxSmlGetDeviceIsaVersion.restype = c_uint

mxSmlGetSgpuCount = mxsml.mxSmlGetSgpuCount
mxSmlGetSgpuCount.argtypes = [DeviceId]
mxSmlGetSgpuCount.restype = c_uint

mxSmlGetSgpuInfo = mxsml.mxSmlGetSgpuInfo
mxSmlGetSgpuInfo.argtypes = [DeviceId, SgpuId, POINTER(MxSmlSgpuInfo)]
mxSmlGetSgpuInfo.restype = c_uint

mxSmlGetSgpuAlias = mxsml.mxSmlGetSgpuAlias
mxSmlGetSgpuAlias.argtypes = [DeviceId, SgpuId, POINTER(c_char), POINTER(c_uint)]
mxSmlGetSgpuAlias.restype = c_uint

mxSmlGetSgpuMemory = mxsml.mxSmlGetSgpuMemory
mxSmlGetSgpuMemory.argtypes = [DeviceId, SgpuId, POINTER(MxSmlSgpuMemoryInfo)]
mxSmlGetSgpuMemory.restype = c_uint

mxSmlGetSgpuUsage = mxsml.mxSmlGetSgpuUsage
mxSmlGetSgpuUsage.argtypes = [DeviceId, SgpuId, POINTER(c_int)]
mxSmlGetSgpuUsage.restype = c_uint

mxSmlGetSgpuAnnotationsId = mxsml.mxSmlGetSgpuAnnotationsId
mxSmlGetSgpuAnnotationsId.argtypes = [DeviceId, SgpuId, POINTER(c_char), POINTER(c_uint)]
mxSmlGetSgpuAnnotationsId.restype = c_uint

mxSmlGetDeviceTimeslice = mxsml.mxSmlGetDeviceTimeslice
mxSmlGetDeviceTimeslice.argtypes = [DeviceId, POINTER(c_uint)]
mxSmlGetDeviceTimeslice.restype = c_uint

mxSmlSetDeviceTimeslice = mxsml.mxSmlSetDeviceTimeslice
mxSmlSetDeviceTimeslice.argtypes = [DeviceId, c_uint]
mxSmlSetDeviceTimeslice.restype = c_uint

mxSmlGetTotalEccErrors = mxsml.mxSmlGetTotalEccErrors
mxSmlGetTotalEccErrors.argtypes = [DeviceId, POINTER(MxSmlEccErrorCount)]
mxSmlGetTotalEccErrors.restype = c_uint

mxSmlGetDieTotalEccErrors = mxsml.mxSmlGetDieTotalEccErrors
mxSmlGetDieTotalEccErrors.argtypes = [DeviceId, DieId, POINTER(MxSmlEccErrorCount)]
mxSmlGetDieTotalEccErrors.restype = c_uint

mxSmlGetMetaXLinkTopo = mxsml.mxSmlGetMetaXLinkTopo
mxSmlGetMetaXLinkTopo.argtypes = [DeviceId, POINTER(MxSmlMetaXLinkTopo)]
mxSmlGetMetaXLinkTopo.restype = c_uint

mxSmlGetDieUnavailableReason = mxsml.mxSmlGetDieUnavailableReason
mxSmlGetDieUnavailableReason.argtypes = [DeviceId, DieId, POINTER(MxSmlDeviceUnavailableReasonInfo)]
mxSmlGetDieUnavailableReason.restype = c_uint

mxSmlGetEthThroughput = mxsml.mxSmlGetEthThroughput
mxSmlGetEthThroughput.argtypes = [DeviceId, POINTER(MxSmlEthThroughput)]
mxSmlGetEthThroughput.restype = c_uint

mxSmlGetDieDriverReservedMemory = mxsml.mxSmlGetDieDriverReservedMemory
mxSmlGetDieDriverReservedMemory.argtypes = [DeviceId, DieId, POINTER(c_uint)]
mxSmlGetDieDriverReservedMemory.restype = c_uint

mxSmlGetPcieErrorCounter = mxsml.mxSmlGetPcieErrorCounter
mxSmlGetPcieErrorCounter.argtypes = [DeviceId, MxSmlLinkErrorCounterType, POINTER(c_ulonglong)]
mxSmlGetPcieErrorCounter.restype = c_uint

mxSmlGetMetaXLinkErrorCounter = mxsml.mxSmlGetMetaXLinkErrorCounter
mxSmlGetMetaXLinkErrorCounter.argtypes = [DeviceId, MxSmlLinkErrorCounterType, POINTER(c_uint), POINTER(c_ulonglong)]
mxSmlGetMetaXLinkErrorCounter.restype = c_uint

mxSmlGetMmaUsageToggle = mxsml.mxSmlGetMmaUsageToggle
mxSmlGetMmaUsageToggle.argtypes = [DeviceId, POINTER(c_uint)]
mxSmlGetMmaUsageToggle.restype = c_uint

mxSmlGetDieMmaUsageToggle = mxsml.mxSmlGetDieMmaUsageToggle
mxSmlGetDieMmaUsageToggle.argtypes = [DeviceId, DieId, POINTER(c_uint)]
mxSmlGetDieMmaUsageToggle.restype = c_uint

mxSmlSetMmaUsageToggle = mxsml.mxSmlSetMmaUsageToggle
mxSmlSetMmaUsageToggle.argtypes = [DeviceId, c_int]
mxSmlSetMmaUsageToggle.restype = c_uint

mxSmlSetDieMmaUsageToggle = mxsml.mxSmlSetDieMmaUsageToggle
mxSmlSetDieMmaUsageToggle.argtypes = [DeviceId, c_int]
mxSmlSetDieMmaUsageToggle.restype = c_uint

mxSmlGetDieClocksThrottleDuration = mxsml.mxSmlGetDieClocksThrottleDuration
mxSmlGetDieClocksThrottleDuration.argtypes = [DeviceId, DieId, MxSmlClockThrottleType, POINTER(c_ulong)]
mxSmlGetDieClocksThrottleDuration.restype = c_uint

if __name__ == "__main__":
    head_len = 40

    def PrintStructure(s):
        for field in s._fields_:
            print (field[0], getattr(s, field[0]))

    def demo_get_maca_version():
        size = c_uint(64)
        entrylist = []
        macaVersion = (c_char * 64)(*entrylist)
        ret = mxSmlGetMacaVersion(macaVersion, size)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetMacaVersion failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetMacaVersion", head_len, macaVersion.value.decode('ASCII')))

    def demo_get_server_info():
        entrylist = []
        localUuid = (c_char * 64)(*entrylist)
        remoteUuid1 = (c_char * 64)(*entrylist)
        remoteUuid2 = (c_char * 64)(*entrylist)
        remotes = (POINTER(c_char)*2)(*[remoteUuid1, remoteUuid2])
        remotesSize = c_uint(2)
        uuidSize = c_uint(64)
        ret = mxSmlGetLocalAndMultipleRemoteUuid(localUuid, remotes, byref(remotesSize), byref(uuidSize))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetLocalAndMultipleRemoteUuid failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print(
                "{:{}}: local_uuid({}), remotesSize({}), remoteUuid1({}), remoteUuid2({})".format(
                    "mxSmlGetLocalAndMultipleRemoteUuid",
                    head_len,
                    localUuid.value.decode('ASCII'),
                    remotesSize.value,
                    remoteUuid1.value.decode('ASCII'),
                    remoteUuid2.value.decode('ASCII')
                )
            )

    def demo_get_device_info(device_id):
        device_info = MxSmlDeviceInfo()
        ret = mxSmlGetDeviceInfo(device_id, byref(device_info))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDeviceInfo failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print(
                "{:{}}: {}  {} (UUID: {})".format(
                    "mxSmlGetDeviceInfo",
                    head_len,
                    device_info.deviceName.decode('ASCII'),
                    device_info.bdfId.decode('ASCII'),
                    device_info.uuid.decode('ASCII'),
                )
            )

    def demo_get_device_state(device_id):
        deviceState = c_int(0)
        ret = mxSmlGetDeviceState(device_id, deviceState)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDeviceState failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetDeviceState", head_len, deviceState.value))

    def demo_get_board_serial(device_id):
        size = c_uint(32)
        entrylist = []
        boardSerial = (c_char * 32)(*entrylist)
        ret = mxSmlGetBoardSerial(device_id, boardSerial, byref(size))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetBoardSerial failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetBoardSerial", head_len, boardSerial.value.decode('ASCII')))

    def demo_get_device_isa_version(device_id):
        isaVersion = c_int(0)
        ret = mxSmlGetDeviceIsaVersion(device_id, byref(isaVersion))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDeviceIsaVersion failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetDeviceIsaVersion", head_len, isaVersion.value))

    def demo_get_temperature_info(device_id):
        temperature = c_int(0)
        tempType = MxSmlTemperatureSensors.MXSML_Temperature_Soc
        ret = mxSmlGetTemperatureInfo(device_id, tempType, temperature)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetTemperatureInfo failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: soc({:.2f} C)".format("mxSmlGetTemperatureInfo", head_len, temperature.value/100))

    def demo_get_board_power_info(device_id):
        entryBoardInfo = []
        boardPower = (MxSmlBoardWayElectricInfo* 3)(*entryBoardInfo)
        BoardWaySize = c_uint(3)
        ret = mxSmlGetBoardPowerInfo(device_id, BoardWaySize, boardPower)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetBoardPowerInfo failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            i = 0
            power_total = sum([boardPower[i].power for i in range(BoardWaySize.value)])
            print("{:{}}: total({:.3f} W)".format("mxSmlGetBoardPowerInfo", head_len, power_total/1000))

    def demo_get_board_power_limit(device_id):
        powerLimit = c_uint(0)
        ret = mxSmlGetBoardPowerLimit(device_id, byref(powerLimit))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetBoardPowerLimit failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {} W".format("mxSmlGetBoardPowerLimit", head_len, powerLimit.value/1000))

    def demo_get_board_power_limit_constraints(device_id):
        minPowerLimit = c_uint(0)
        maxPowerLimit = c_uint(0)
        ret = mxSmlGetBoardPowerLimitConstraints(device_id, byref(minPowerLimit), byref(maxPowerLimit))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetBoardPowerLimitConstraints failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {} W - {} W".format(
                "mxSmlGetBoardPowerLimitConstraints", head_len, minPowerLimit.value/1000, maxPowerLimit.value/1000))

    def demo_get_pcie_throughput(device_id):
        pcieThroughput = MxSmlPcieThroughput()
        ret = mxSmlGetPcieThroughput(device_id, byref(pcieThroughput))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetPcieThroughput failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: TX({} MB/s), RX({} MB/s)".format("mxSmlGetPcieThroughput", head_len, pcieThroughput.tx, pcieThroughput.rx))

    def demo_get_pcie_info(device_id):
        pcieInfo = MxSmlPcieInfo()
        ret = mxSmlGetPcieInfo(device_id, byref(pcieInfo))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetPcieInfo failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: speed({} GT/s), width(x{})".format("mxSmlGetPcieInfo", head_len, pcieInfo.speed, pcieInfo.width))

    def demo_get_pcie_bridge_info(device_id):
        pcieInfo = MxSmlPcieInfo()
        ret = mxSmlGetPcieMaxLinkInfo(device_id, byref(pcieInfo))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetPcieMaxLinkInfo failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: speed({} GT/s), width(x{})".format("mxSmlGetPcieMaxLinkInfo", head_len, pcieInfo.speed, pcieInfo.width))

    def demo_get_pci_event(ip_name, ip_unit, device_id):
        entrylist = []
        eventInfo = (MxSmlPciEventInfo*2)(*entrylist)
        size = c_uint(2)
        ret = mxSmlGetPciEventInfo(device_id, ip_unit, eventInfo, byref(size))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetPciEventInfo {} failed: {}".format(ip_name, mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: ip({}), size({})".format("mxSmlGetPciEventInfo", head_len, ip_name, size.value))
            for i in range(size.value):
                print("  bitNumber({}), count({}), firstTime({}), name({})".format(
                    eventInfo[i].bitNumber, eventInfo[i].count,
                    eventInfo[i].firstTime.decode('ASCII'), eventInfo[i].name.decode('ASCII')))

    def demo_get_pci_link_error_counter(counter_name, counter_type, device_id):
        counter_value = c_ulonglong(0)
        ret = mxSmlGetPcieErrorCounter(device_id, counter_type, byref(counter_value))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetPcieErrorCounter {} failed: {}".format(counter_name, mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: type({}), counter({})".format("mxSmlGetPcieErrorCounter", head_len, counter_name, counter_value.value))

    def demo_get_dpm_clock_info(ip_name, ip_unit, device_id):
        entrylist = []
        clockInfo = (c_uint * 12)(*entrylist)
        size = c_uint(12)
        ret = mxSmlGetDpmIpClockInfo(device_id, ip_unit, clockInfo, size)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDpmIpClockInfo {} failed: {}".format(ip_name, mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetDpmIpClockInfo", head_len,
                                     ", ".join(["{}[{}]({} MHz)".format(ip_name, i, clockInfo[i]) for i in range(size.value)])))

    def demo_get_dpm_voltage_info(ip_name, ip_unit, device_id):
        entrylist = []
        voltageInfo = (c_uint * 12)(*entrylist)
        size = c_uint(12)
        ret = mxSmlGetDpmIpVddInfo(device_id, ip_unit, voltageInfo, size)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDpmIpVddInfo {} failed: {}".format(ip_name, mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetDpmIpVddInfo", head_len,
                                     ", ".join(["{}[{}]({} V)".format(ip_name, i, voltageInfo[i]) for i in range(size.value)])))

    def demo_get_topology_info(device_id):
        topoInfo = MxSmlMetaXLinkTopo()
        ret = mxSmlGetMetaXLinkTopo(device_id, byref(topoInfo))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetMetaXLinkTopo failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: topology_id({}), socket_id({}), die_id({})".format(
                "mxSmlGetMetaXLinkTopo", head_len, topoInfo.topologyId, topoInfo.socketId, topoInfo.dieId))

    def demo_get_fw_log_level(ip_name, ip_unit, device_id):
        loglevel = c_uint(0)
        ret = mxSmlGetFwIpLoglevel(device_id, ip_unit, loglevel)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetFwIpLoglevel for {} failed: {}".format(ip_name, mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}({})".format("mxSmlGetFwIpLoglevel", head_len, ip_name, loglevel.value))

    def demo_get_pci_mmio_state(device_id):
        state = c_uint()
        ret = mxSmlGetPciMmioState(device_id, byref(state))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetPciMmioState failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetPciMmioState", head_len, state.value))

    def demo_get_om_temperature_info(device_id):
        size = c_uint(3)
        entrylist = []
        opticalModuleStatus = (MxSmlOpticalModuleStatus*3)(*entrylist)
        ret = mxSmlGetOpticalModuleStatus(device_id, opticalModuleStatus, byref(size))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetOpticalModuleStatus failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("mxSmlGetOpticalModuleStatus:")
            i = 0
            while i < size.value:
                PrintStructure(opticalModuleStatus[i])
                i += 1

    def demo_get_mxlk_state(device_id):
        mxlkStateCode = MxSmlMetaXLinkState(MxSmlMetaXLinkState.MXSML_MetaXLink_State_Enabled)
        entrylist = []
        mxlkState = (c_char * 128)(*entrylist)
        size = c_uint(128)
        ret = mxSmlGetMetaXLinkState(device_id, byref(mxlkStateCode), mxlkState, byref(size))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetMetaXLinkState failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: mxlkStateCode({}), mxlkState({})".format(
                "mxSmlGetMetaXLinkState", head_len, mxlkStateCode, mxlkState.value.decode('ASCII')))

    def demo_get_mxlk_port_state(device_id):
        entrylist = []
        mxlkPortState = (MxSmlMxlkPortState * 7)(*entrylist)
        size = c_uint(7)
        ret = mxSmlGetMetaXLinkPortState(device_id, mxlkPortState, byref(size))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetMetaXLinkPortState failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format(
                "mxSmlGetMetaXLinkPortState", head_len,
                ", ".join(["PORT#{}({})".format(i + 1, mxlkPortState[i].value) for i in range(size.value)])))

    def demo_get_mxlk_info(device_id):
        entryLinklist = []
        mxlkInfo = (MxSmlSingleMetaXLinkInfo* 7)(*entryLinklist)
        linkSize = c_uint(7)
        ret = mxSmlGetMetaXLinkInfo_v2(device_id, linkSize, mxlkInfo)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetMetaXLinkInfo_v2 failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("mxSmlGetMetaXLinkInfo_v2:")
            for i in range(linkSize.value):
                print("  PORT#{}:  speed({} GT/s), width(x{})".format(i + 1, mxlkInfo[i].speed, mxlkInfo[i].width))

    def demo_get_mxlk_bandwidth(device_id):
        state = True
        entryLinklist = []
        mxlkRxBw = (MxSmlMetaXLinkBandwidth* 7)(*entryLinklist)
        linkSize = c_uint(7)
        ret = mxSmlGetMetaXLinkBandwidth(device_id, MxSmlMetaXLinkType.MXSML_MetaXLink_Input, linkSize, mxlkRxBw)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetMetaXLinkBandwidth input failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
            state = False

        mxlkTxBw = (MxSmlMetaXLinkBandwidth* 7)(*entryLinklist)
        linkSize = c_uint(7)
        ret = mxSmlGetMetaXLinkBandwidth(device_id, MxSmlMetaXLinkType.MXSML_MetaXLink_Target, linkSize, mxlkTxBw)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetMetaXLinkBandwidth target failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
            state = False

        if state:
            print("mxSmlGetMetaXLinkBandwidth:")
            for i in range(linkSize.value):
                print("  PORT#{}:  RX({} MB/s), TX({} MB/s)".format(i + 1, mxlkRxBw[i].requestBandwidth, mxlkTxBw[i].requestBandwidth))

    def demo_get_mxlk_traffic_stat(device_id):
        state = True
        entryLinklist = []
        mxlkRxTrafficStat = (MxSmlMetaXLinkTrafficStat* 7)(*entryLinklist)
        linkSize = c_uint(7)
        ret = mxSmlGetMetaXLinkTrafficStat(device_id, MxSmlMetaXLinkType.MXSML_MetaXLink_Input, linkSize, mxlkRxTrafficStat)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetMetaXLinkTrafficStat failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
            state = False

        mxlkTxTrafficStat = (MxSmlMetaXLinkTrafficStat* 7)(*entryLinklist)
        linkSize = c_uint(7)
        ret = mxSmlGetMetaXLinkTrafficStat(device_id, MxSmlMetaXLinkType.MXSML_MetaXLink_Target, linkSize, mxlkTxTrafficStat)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetMetaXLinkTrafficStat failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
            state = False

        if state:
            print("mxSmlGetMetaXLinkTrafficStat:")
            for i in range(linkSize.value):
                print("  PORT#{}:  RX({} Bytes), TX({} Bytes)".format(
                    i + 1, mxlkRxTrafficStat[i].requestTrafficStat, mxlkTxTrafficStat[i].requestTrafficStat))

    def demo_get_mxlk_aer(device_id):
        entryLinklist = []
        metaxLinkAer = (MxSmlMetaXLinkAer* 7)(*entryLinklist)
        linkSize = c_uint(7)
        ret = mxSmlGetMetaXLinkAer(device_id, linkSize, metaxLinkAer)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetMetaXLinkAer failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("mxSmlGetMetaXLinkAer:")
            for i in range(linkSize.value):
                print("  PORT#{}:  CE({}), UE({})".format(i + 1, metaxLinkAer[i].ceAer, metaxLinkAer[i].ueAer))

    def demo_get_mxlk_error_counter(counter_name, counter_type, device_id):
        entryLinklist = []
        counter_value = (c_ulonglong * METAX_LINK_NUM)(*entryLinklist)
        linkSize = c_uint(METAX_LINK_NUM)
        ret = mxSmlGetMetaXLinkErrorCounter(device_id, counter_type, byref(linkSize), counter_value)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetMetaXLinkErrorCounter {} failed: {}".format(counter_name, mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("mxSmlGetMetaXLinkErrorCounter({}):".format(counter_name))
            for i in range(linkSize.value):
                print("  PORT#{}:  {}".format(i + 1, counter_value[i]))

    def demo_get_eth_throughput(device_id):
        ethThroughput = MxSmlEthThroughput()
        ret = mxSmlGetEthThroughput(device_id, byref(ethThroughput))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetEthThroughput failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: TX({} MB/s), RX({} MB/s)".format("mxSmlGetEthThroughput", head_len, ethThroughput.tx, ethThroughput.rx))

    def demo_get_die_version(ip_name, ip_unit, device_id, die_id):
        size = c_uint(64)
        entrylist = []
        version = (c_char * 64)(*entrylist)
        ret = mxSmlGetDeviceDieVersion(device_id, die_id, ip_unit, version, size)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDeviceVersion {} failed: {}".format(ip_name, mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}({})".format("mxSmlGetDeviceVersion", head_len, ip_name, version.value.decode('ASCII')))

    def demo_get_die_unavailable_reason(device_id, die_id):
        unavailable_reason = MxSmlDeviceUnavailableReasonInfo()
        ret = mxSmlGetDieUnavailableReason(device_id, die_id, byref(unavailable_reason))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieUnavailableReason failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: code({}), reason({})".format(
                "mxSmlGetDieUnavailableReason", head_len,
                unavailable_reason.unavailableCode, unavailable_reason.unavailableReason.decode('ASCII')))

    def demo_get_die_temperature_info(ip_name, ip_unit, device_id, die_id):
        temperature = c_int(0)
        ret = mxSmlGetDieTemperatureInfo(device_id, die_id, ip_unit, temperature)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieTemperatureInfo {} failed: {}".format(ip_name, mxSmlGetErrorString(ret).decode('ASCII')))
            state = False
        else:
            print("{:{}}: {}({:.2f} C)".format("mxSmlGetDieTemperatureInfo", head_len, ip_name, temperature.value/100))

    def demo_get_die_usage_info(ip_name, ip_unit, device_id, die_id):
        usage = c_int(0)
        ret = mxSmlGetDieIpUsage(device_id, die_id, ip_unit, usage)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieIpUsage {} failed: {}".format(ip_name, mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}({} %)".format("mxSmlGetDieIpUsage", head_len, ip_name, usage.value))

    def demo_get_die_memory_info(device_id, die_id):
        memory = MxSmlMemoryInfo()
        ret = mxSmlGetDieMemoryInfo(device_id, die_id, byref(memory))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieMemoryInfo failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: vram(used({} KB), total({} KB)), xtt(used({} KB), total({} KB))".format(
                "mxSmlGetDieMemoryInfo", head_len, memory.vramUse, memory.vramTotal, memory.xttUse, memory.xttTotal))

    def demo_get_die_pmbus_info(ip_name, ip_unit, device_id, die_id):
        pmbusInfo = MxSmlPmbusInfo()
        ret = mxSmlGetDiePmbusInfo(device_id, die_id, ip_unit, byref(pmbusInfo))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDiePmbusInfo {} failed: {}".format(ip_name, mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}({:.3f} W)".format("mxSmlGetDiePmbusInfo", head_len, ip_name, pmbusInfo.power/1000))

    def demo_get_die_clock_info(ip_name, ip_unit, device_id, die_id):
        clocksSize = c_uint(8)
        clocksMhz = (c_uint * 2)()
        ret = mxSmlGetDieClocks(device_id, die_id, ip_unit, clocksSize, clocksMhz)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetClocks {} failed: {}".format(ip_name, mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}(size({}), clock({} MHz))".format("mxSmlGetClocks", head_len, ip_name, clocksSize.value, clocksMhz[0]))

    def demo_get_die_hbm_bandwidth(device_id, die_id):
        hbmBw = MxSmlHbmBandwidth()
        ret = mxSmlGetDieHbmBandWidth(device_id, die_id, byref(hbmBw))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetHbmBandWidth failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {} MB/s".format("mxSmlGetHbmBandWidth", head_len, hbmBw.hbmBandwidthRespTotal))

    def demo_get_die_hbm_bandwidth_utilization(device_id, die_id):
        utilization = c_uint(0)
        ret = mxSmlGetDieHbmBandwidthUtilization(device_id, die_id, utilization)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieHbmBandwidthUtilization failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {} %".format("mxSmlGetDieHbmBandwidthUtilization", head_len, utilization.value))

    def demo_get_die_dpm_level(device_id, die_id):
        dpmIp = MxSmlDpmIp.MXSML_Dpm_Xcore
        dpmIpPerfLevel = c_uint(0)
        ret = mxSmlGetCurrentDieDpmIpPerfLevel(device_id, die_id, dpmIp, dpmIpPerfLevel)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetCurrentDpmIpPerfLevel xcore failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: xcore({})".format("mxSmlGetCurrentDpmIpPerfLevel", head_len, dpmIpPerfLevel.value))

    def demo_get_die_process_info(device_id, die_id):
        entrylist = []
        processNumber = c_uint(32)
        processInfo = (MxSmlProcessInfo_v2*32)(*entrylist)
        ret = mxSmlGetSingleGpuProcess_v2(device_id, processNumber, processInfo)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetSingleGpuProcess_v2 failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            number = 0
            for idx, process in enumerate(processInfo):
                if idx == processNumber.value:
                    break
                for gpu_idx, gpu_info in enumerate(process.processGpuInfo):
                    if gpu_idx == process.gpuNumber:
                        break
                    if gpu_info.gpuId == device_id and gpu_info.dieId == die_id:
                        number += 1
                        break
            print("{:{}}: process_number({})".format("mxSmlGetSingleGpuProcess_v2", head_len, number))

    def demo_get_die_clk_tr(device_id, die_id):
        clocksThrottleReason = c_ulonglong(0)
        ret = mxSmlGetDieCurrentClocksThrottleReason(device_id, die_id, byref(clocksThrottleReason))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieCurrentClocksThrottleReason failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetDieCurrentClocksThrottleReason", head_len, clocksThrottleReason.value))

    def demo_get_die_ecc_count(device_id, die_id):
        ecc = MxSmlEccErrorCount()
        ret = mxSmlGetDieTotalEccErrors(device_id, die_id, byref(ecc))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieTotalEccErrors failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: sramCE({}), sramUE({}), dramCE({}), dramUE({}), retiredPage({})".format(
                "mxSmlGetDieTotalEccErrors", head_len, ecc.sramCE, ecc.sramUE, ecc.dramCE, ecc.dramUE, ecc.retiredPage))

    def demo_get_die_ras_count(device_id, die_id):
        device_RasErrorData = MxSmlRasErrorData()
        ret = mxSmlGetDieRasErrorData(device_id, die_id, byref(device_RasErrorData))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieRasErrorData failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: size({})".format("mxSmlGetDieRasErrorData", head_len, device_RasErrorData.showRasErrorSize))

    def demo_get_die_ras_status(device_id, die_id):
        device_RasStatusData = MxSmlRasStatusData()
        ret = mxSmlGetDieRasStatusData(device_id, die_id, byref(device_RasStatusData))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieRasStatusData failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: size({})".format("mxSmlGetDieRasStatusData", head_len, device_RasStatusData.showRasStatusSize))

    def demo_get_die_driver_reserved_memory(device_id, die_id):
        reserved_memory = c_uint(0)
        ret = mxSmlGetDieDriverReservedMemory(device_id, die_id, byref(reserved_memory))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieDriverReservedMemory failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetDieDriverReservedMemory", head_len, reserved_memory.value))

    def demo_get_die_mma_usage_toggle(device_id, die_id):
        toggle = c_uint(0)
        ret = mxSmlGetDieMmaUsageToggle(device_id, die_id, byref(toggle))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieMmaUsageToggle failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetDieMmaUsageToggle", head_len, toggle.value))

    def demo_get_die_clock_throttle_duration(ip_name, ip_unit, device_id, die_id):
        duration = c_ulong()
        ret = mxSmlGetDieClocksThrottleDuration(device_id, die_id, ip_unit, byref(duration))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDieClocksThrottleDuration {} failed: {}".format(ip_name, mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}({} us)".format("mxSmlGetDieClocksThrottleDuration", head_len, ip_name, duration.value))

    def demo_get_sgpu_timeslice(device_id):
        timeslice = c_uint(0)
        ret = mxSmlGetDeviceTimeslice(device_id, byref(timeslice))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDeviceTimeslice failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetDeviceTimeslice", head_len, timeslice.value))

    def demo_get_sgpu_info(device_id, sgpu_id):
        sgpuInfo = MxSmlSgpuInfo()
        ret = mxSmlGetSgpuInfo(device_id, sgpu_id, byref(sgpuInfo))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetSgpuInfo failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {} %  {}gb (UUID: {})".format(
                "mxSmlGetSgpuInfo", head_len, sgpuInfo.computeQuota, sgpuInfo.vramQuota / 1024, sgpuInfo.uuid.decode('ASCII')))

    def demo_get_sgpu_usage(device_id, sgpu_id):
        usage = c_int(0)
        ret = mxSmlGetSgpuUsage(device_id, sgpu_id, byref(usage))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetSgpuUsage failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetSgpuUsage", head_len, usage.value))

    def demo_get_sgpu_memory_info(device_id, sgpu_id):
        memory = MxSmlSgpuMemoryInfo()
        ret = mxSmlGetSgpuMemory(device_id, sgpu_id, byref(memory))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetSgpuMemory failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: total({} bytes), used({} bytes), free({} bytes))".format(
                "mxSmlGetSgpuMemory", head_len, memory.total, memory.used, memory.free))

    def demo_get_sgpu_alias(device_id, sgpu_id):
        size = c_uint(32)
        entrylist = []
        alias = (c_char * 32)(*entrylist)
        ret = mxSmlGetSgpuAlias(device_id, sgpu_id, alias, byref(size))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetSgpuAlias failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetSgpuAlias", head_len, alias.value.decode('ASCII')))

    def demo_get_sgpu_annotations_id(device_id, sgpu_id):
        size = c_uint(96)
        entrylist = []
        annotations_id = (c_char * 96)(*entrylist)
        ret = mxSmlGetSgpuAnnotationsId(device_id, sgpu_id, annotations_id, byref(size))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetSgpuAnnotationsId failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("{:{}}: {}".format("mxSmlGetSgpuAnnotationsId", head_len, annotations_id.value.decode('ASCII')))

    def demo_get_limited_devices_info(device_id):
        limited_device_info = MxSmlDeviceInfo()
        ret = mxSmlGetLimitedDeviceInfo(device_id, byref(limited_device_info))
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetLimitedDeviceInfo failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print(
                "{:{}}: {}  {}".format(
                    "mxSmlGetLimitedDeviceInfo",
                    head_len,
                    limited_device_info.deviceName.decode('ASCII'),
                    limited_device_info.bdfId.decode('ASCII')
                )
            )

    ret = mxSmlInit()
    # limited devices
    limited_device_ids = MxSmlLimitedDeviceIds()
    ret = mxSmlGetAllLimitedDevices(byref(limited_device_ids))
    if ret != MxSmlReturn.MXSML_Success:
        print("mxSmlGetAllLimitedDevices failed: %s" % mxSmlGetErrorString(ret).decode('ASCII'))
    else:
        print("limited devices count: %d" % limited_device_ids.number)
        for i in range(limited_device_ids.number):
            device_id = limited_device_ids.deviceId[i]
            print("limited device id: %d" % device_id)
            demo_get_limited_devices_info(device_id)

    if ret != MxSmlReturn.MXSML_Success:
        print("mxsml init failed: %s" % mxSmlGetErrorString(ret).decode('ASCII'))
        exit(1)

    ret = mxSmlInitWithFlags(0)
    if ret != MxSmlReturn.MXSML_Success:
        print("mxSmlInitWithFlags failed: %s" % mxSmlGetErrorString(ret).decode('ASCII'))
        exit(1)

    demo_get_maca_version()
    demo_get_server_info()

    device_count = mxSmlGetDeviceCount()
    print("mxSmlGetDeviceCount: " + str(device_count))

    for device_id in range(device_count):
        print("{} GPU#{} {}".format("=" * head_len, device_id, "=" * head_len))
        demo_get_device_info(device_id)
        demo_get_device_state(device_id)
        demo_get_board_serial(device_id)
        demo_get_device_isa_version(device_id)
        demo_get_temperature_info(device_id)
        demo_get_board_power_info(device_id)
        demo_get_board_power_limit(device_id)
        demo_get_board_power_limit_constraints(device_id)
        demo_get_pcie_throughput(device_id)
        demo_get_pcie_info(device_id)
        demo_get_pcie_bridge_info(device_id)
        demo_get_topology_info(device_id)
        demo_get_fw_log_level("smp0", MxSmlFwIp.MXSML_Fw_IpName_SMP0, device_id)
        demo_get_pci_event("aer_ue", MxSmlPciEventType.MXSML_Pci_Event_AER_UE, device_id)
        demo_get_pci_event("aer_ce", MxSmlPciEventType.MXSML_Pci_Event_AER_CE, device_id)
        demo_get_pci_event("synfld", MxSmlPciEventType.MXSML_Pci_Event_SYNFLD, device_id)
        demo_get_pci_event("dbe", MxSmlPciEventType.MXSML_Pci_Event_DBE, device_id)
        demo_get_pci_event("mmio", MxSmlPciEventType.MXSML_Pci_Event_MMIO, device_id)
        demo_get_pci_link_error_counter("CRC", MxSmlLinkErrorCounterType.MXSML_Link_Error_Crc, device_id)
        demo_get_pci_link_error_counter("REPLAY", MxSmlLinkErrorCounterType.MXSML_Link_Error_Replay, device_id)
        demo_get_pci_link_error_counter("RECOVERY", MxSmlLinkErrorCounterType.MXSML_Link_Error_Recovery, device_id)
        demo_get_dpm_clock_info("mc", MxSmlDpmIp.MXSML_Dpm_Mc, device_id)
        demo_get_dpm_voltage_info("mc", MxSmlDpmIp.MXSML_Dpm_Mc, device_id)
        demo_get_pci_mmio_state(device_id)
        demo_get_om_temperature_info(device_id)
        demo_get_mxlk_state(device_id)
        demo_get_mxlk_port_state(device_id)
        demo_get_mxlk_info(device_id)
        demo_get_mxlk_bandwidth(device_id)
        demo_get_mxlk_traffic_stat(device_id)
        demo_get_mxlk_aer(device_id)
        demo_get_mxlk_error_counter("CRC", MxSmlLinkErrorCounterType.MXSML_Link_Error_Crc, device_id)
        demo_get_mxlk_error_counter("REPLAY", MxSmlLinkErrorCounterType.MXSML_Link_Error_Replay, device_id)
        demo_get_mxlk_error_counter("RECOVERY", MxSmlLinkErrorCounterType.MXSML_Link_Error_Recovery, device_id)
        demo_get_eth_throughput(device_id)

        # die
        die_count = c_uint(1)
        ret = mxSmlGetDeviceDieCount(device_id, die_count)
        if ret != MxSmlReturn.MXSML_Success:
            print("mxSmlGetDeviceCount failed: {}".format(mxSmlGetErrorString(ret).decode('ASCII')))
        else:
            print("mxSmlGetDeviceCount: {}".format(die_count.value))

        for die_id in range(die_count.value):
            print("{} GPU#{} DIE#{} {}".format("-" * head_len, device_id, die_id, "-" * head_len))
            demo_get_die_version("bios", MxSmlVersionUnit.MXSML_Version_Bios, device_id, die_id)
            demo_get_die_version("driver", MxSmlVersionUnit.MXSML_Version_Driver, device_id, die_id)
            demo_get_die_unavailable_reason(device_id, die_id)
            demo_get_die_temperature_info("hotspot", MxSmlTemperatureSensors.MXSML_Temperature_Hotspot, device_id, die_id)
            demo_get_die_temperature_info("core", MxSmlTemperatureSensors.MXSML_Temperature_Core, device_id, die_id)
            demo_get_die_usage_info("vpue", MxSmlUsageIp.MXSML_Usage_Vpue, device_id, die_id)
            demo_get_die_usage_info("vpud", MxSmlUsageIp.MXSML_Usage_Vpud, device_id, die_id)
            demo_get_die_usage_info("xcore", MxSmlUsageIp.MXSML_Usage_Xcore, device_id, die_id)
            demo_get_die_usage_info("mma", MxSmlUsageIp.MXSML_Usage_Mma, device_id, die_id)
            demo_get_die_memory_info(device_id, die_id)
            demo_get_die_pmbus_info("soc", MxSmlPmbusUnit.MXSML_Pmbus_Soc, device_id, die_id)
            demo_get_die_pmbus_info("core", MxSmlPmbusUnit.MXSML_Pmbus_Core, device_id, die_id)
            demo_get_die_pmbus_info("hbm", MxSmlPmbusUnit.MXSML_Pmbus_Hbm, device_id, die_id)
            demo_get_die_pmbus_info("pcie", MxSmlPmbusUnit.MXSML_Pmbus_Pcie, device_id, die_id)
            demo_get_die_clock_info("vpue", MxSmlClockIp.MXSML_Clock_Vpue, device_id, die_id)
            demo_get_die_clock_info("vpud", MxSmlClockIp.MXSML_Clock_Vpud, device_id, die_id)
            demo_get_die_clock_info("mem", MxSmlClockIp.MXSML_Clock_Mc0, device_id, die_id)
            demo_get_die_clock_info("xcore", MxSmlClockIp.MXSML_Clock_Xcore, device_id, die_id)
            demo_get_die_hbm_bandwidth(device_id, die_id)
            demo_get_die_hbm_bandwidth_utilization(device_id, die_id)
            demo_get_die_dpm_level(device_id, die_id)
            demo_get_die_process_info(device_id, die_id)
            demo_get_die_clk_tr(device_id, die_id)
            demo_get_die_ecc_count(device_id, die_id)
            demo_get_die_ras_count(device_id, die_id)
            demo_get_die_ras_status(device_id, die_id)
            demo_get_die_driver_reserved_memory(device_id, die_id)
            demo_get_die_mma_usage_toggle(device_id, die_id)
            demo_get_die_clock_throttle_duration("over current", MxSmlClockThrottleType.MXSML_CLK_THROTTLE_OVER_CURRENT, device_id, die_id)
            demo_get_die_clock_throttle_duration("over voltage", MxSmlClockThrottleType.MXSML_CLK_THROTTLE_OVER_VOLTAGE, device_id, die_id)
            demo_get_die_clock_throttle_duration("power brake", MxSmlClockThrottleType.MXSML_CLK_THROTTLE_POWER_BRAKE, device_id, die_id)

        # sgpu
        sgpuNum = mxSmlGetSgpuCount(device_id)
        print("mxSmlGetSgpuCount: {}".format(sgpuNum))
        demo_get_sgpu_timeslice(device_id)

        for sgpu_id in range(sgpuNum):
            print("{} GPU#{} SGPU#{} {}".format("-" * head_len, device_id, sgpu_id, "-" * head_len))
            demo_get_sgpu_info(device_id, sgpu_id)
            demo_get_sgpu_usage(device_id, sgpu_id)
            demo_get_sgpu_memory_info(device_id, sgpu_id)
            demo_get_sgpu_alias(device_id, sgpu_id)
            demo_get_sgpu_annotations_id(device_id, sgpu_id)

        print()
