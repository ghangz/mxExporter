#!/usr/bin/env python3

"""
Copyright © 2026 MetaX Integrated Circuits (Shanghai) Co., Ltd. All Rights Reserved.

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

import re
from mx_exporter.mxsml_function import *
from mx_exporter.kubernetes import PodInfo


class ContainerInfoCollector:

    _PATTERNS = {
            "docker": re.compile(
                r"/(?:system\.slice/)?docker-([0-9a-f]{64})(?:\.(?:slice|scope))?|"
                r"/docker/([0-9a-f]{64})"
            ),
            "containerd": re.compile(
                r"/(?:system\.slice/)?containerd-([0-9a-f]{64})(?:\.(?:slice|scope))?|"
                r"/containerd/([0-9a-f]{64})"
            ),
            "crio": re.compile(
                r"/(?:system\.slice/)?crio-([0-9a-f]{64})(?:\.(?:slice|scope))?|"
                r"/crio/([0-9a-f]{64})"
            ),
        }

    def __init__(self, device_info_map, proc_path = '/proc'):
        self.device_info_map = device_info_map
        self.proc_path = proc_path

    def get_device_pid_info(self): # ret: { (device_id, die_id) : [pid1, pid2, ...] }
        device_pid_map = {}

        entrylist = []
        processNumber = c_uint(32)
        processInfo = (MxSmlProcessInfo_v2*32)(*entrylist)
        ret = mxSmlGetProcessInfo_v2(processNumber, processInfo)
        if ret != MxSmlReturn.MXSML_Success:
            return device_pid_map
        else:
            for idx, process in enumerate(processInfo):
                if idx == processNumber.value:
                    break
                for gpu_idx, gpu_info in enumerate(process.processGpuInfo):
                    if gpu_idx == process.gpuNumber:
                        break
                    key = (gpu_info.gpuId, gpu_info.dieId)
                    device_pid_map.setdefault(key, []).append(process.processId)

        return device_pid_map

    def read_cgroup_file(self, pid: int) -> str:
        cgroup_file = f"{self.proc_path}/{pid}/cgroup" # cgroup v1
        if os.path.exists(cgroup_file):
            try:
                with open(cgroup_file, 'r') as f:
                    value = f.read().strip()
                    parts = value.split("::")
                    return parts[-1].strip() if len(parts) >= 2 else ""
            except Exception as e:
                print("Read %s error %s" % (cgroup_file, e))

        return ""

    def parse_container_name(self, pid: int) -> str:
        cgroup_content = self.read_cgroup_file(pid)
        if cgroup_content:
            docker_match = self._PATTERNS["docker"].search(cgroup_content)
            if docker_match:
                return docker_match.group(1) or docker_match.group(2)

            containerd_match = self._PATTERNS["containerd"].search(cgroup_content)
            if containerd_match:
                return containerd_match.group(1) or containerd_match.group(2)

            crio_match = self._PATTERNS["crio"].search(cgroup_content)
            if crio_match:
                return crio_match.group(1) or crio_match.group(2)

        return ""

    def get_container_resource(self):
        device_pod_map = {}

        device_pid_map = self.get_device_pid_info()

        for (device_id, die_id), pid_list in device_pid_map.items():
            for pid in pid_list:
                container_name = self.parse_container_name(pid)
                if container_name:
                    if (device_id, die_id) in self.device_info_map:
                        uuid = self.device_info_map[(device_id, die_id)].uuid
                        device_pod_map[uuid] = PodInfo('', '', container_name, uuid)
                        break
                    else:
                        continue

        return device_pod_map
