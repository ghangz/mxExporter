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

import time
import threading
from datetime import datetime
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from mx_exporter.mxsml_function import *


old_print = print
def timestamp_print(*args, **kwargs):
    old_print(datetime.now(), "SgpuMonitor", *args, **kwargs)
print = timestamp_print


class SgpuMonitor:
    def __init__(self):
        self.init_members()


    def initialize(self):
        while True:
            ret = mxsml_init()
            if ret != MxSmlReturn.MXSML_Success:
                print("sgpu mxSmlInit failed: %s" % (mxsml_get_error_string(ret)))
                time.sleep(5)
            else:
                break


    def monitor(self, sgpu_metrics_required, parent_device_ids):
        workers = len(parent_device_ids) # for sgpu metrics
        if workers == 0:
            return

        self.sgpu_metrics_required = sgpu_metrics_required
        futures = []
        self.clear_sgpu()
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for id in parent_device_ids:
                futures.append(executor.submit(self.monitor_sgpu_devices, id))

        for future in as_completed(futures):
            future.result()

        for metric_id in self.sgpu_metrics_required:
            self.sgpu_metric_map[metric_id](metric_id)
        self.update_front_index()


    def get_sgpu_data(self):
        with self.lock:
            data = deepcopy(self.sgpu_data[self.front_index])
        return data


    def update_sgpu_data(self, device_id, sgpu_id, metric_id, data):
        if (device_id, sgpu_id) not in self.sgpu_data[self.back_index]:
            self.sgpu_data[self.back_index][(device_id, sgpu_id)] = ({metric_id : data})
        else:
            self.sgpu_data[self.back_index][(device_id, sgpu_id)].update({metric_id : data})


    def get_sgpu_info_dict(self):
        with self.lock:
            all_sgpu_info = deepcopy(self.all_sgpu_info[self.front_index])
            sgpu_pod_uuid_map = deepcopy(self.sgpu_pod_uuid_map[self.front_index])
        return all_sgpu_info, sgpu_pod_uuid_map


    def clear_all_sgpu_info(self):
        with self.lock:
            self.sgpu_data = [{}, {}]
            self.all_sgpu_info = [{}, {}]
            self.sgpu_pod_uuid_map = [{}, {}]
            self.sgpu_memory_info = [{}, {}]


    def clear_sgpu(self): # sgpu is dynamic
        with self.lock:
            self.sgpu_data[self.back_index].clear()
            self.all_sgpu_info[self.back_index].clear()
            self.sgpu_pod_uuid_map[self.back_index].clear()
            self.sgpu_memory_info[self.back_index].clear()


    def update_front_index(self):
        with self.lock:
            self.front_index = 1 - self.front_index
            self.back_index = 1 - self.back_index


    def monitor_sgpu_devices(self, device_id):
        if len(self.sgpu_metrics_required) != 0:
            sgpu_count = mxsml_get_sgpu_count(device_id)
            if sgpu_count == -1 or sgpu_count == 0:
                # Skip if the version of mxsmlBindings.py and libmxsml.so is too low for sgpu mode
                return

            sgpu_memory_toggle = 0
            if any(map(lambda metric: metric in self.sgpu_metrics_required,
                ['sgpu_memory_total', 'sgpu_memory_used', 'sgpu_memory_free'])):
                sgpu_memory_toggle = 1

            self.safe_print("Get sgpu data GPU#%d(sgpu count:%d)" %(device_id, sgpu_count))
            self.get_sgpu_info(device_id, sgpu_count, sgpu_memory_toggle)


    def init_members(self):
        # buffer[0], buffer[1]
        self.front_index = 0
        self.back_index = 1 - self.front_index
        self.sgpu_data = [{}, {}] # (device id, sgpu id) : {metric id : value}

        self.all_sgpu_info = [{}, {}] # { (device_id, sgpu_id) : MxSmlSgpuInfo() }
        self.sgpu_pod_uuid_map = [{}, {}] # { (device_id, sgpu_id) : pod_register_uuid }
        self.sgpu_memory_info = [{}, {}] # { (device_id, sgpu_id) : MxSmlSgpuMemoryInfo() }

        self.lock = threading.Lock()
        self.print_lock = threading.Lock()

        self.sgpu_metrics_required = []  # user required sgpu metrics

        self.sgpu_metric_map = {
            "sgpu_compute_quota": self.get_sgpu_compute_quota,
            "sgpu_usage"        : self.get_sgpu_usage,
            "sgpu_memory_total" : self.get_sgpu_memory_total,
            "sgpu_memory_used"  : self.get_sgpu_memory_used,
            "sgpu_memory_free"  : self.get_sgpu_memory_free
        }

    def safe_print(self, *args, **kwargs):
        with self.print_lock:
            print(*args, **kwargs)


    def get_sgpu_info(self, device_id, sgpu_count, sgpu_memory_toggle):
        count = 0
        for sgpu_id in range(0, 16): # max sgpu count = 16
            if count >= sgpu_count:
                break

            ret, sgpu_info = mxsml_get_sgpu_info(device_id, sgpu_id)
            if ret == MxSmlReturn.MXSML_Success:
                count = count + 1
                pod_register_uuid = mxsml_get_sgpu_annotations_id(device_id, sgpu_id)
                if sgpu_memory_toggle:
                    self.get_sgpu_memory_info(device_id, sgpu_id)
                with self.lock:
                    self.all_sgpu_info[self.back_index][(device_id, sgpu_id)] = sgpu_info
                    self.sgpu_pod_uuid_map[self.back_index][(device_id, sgpu_id)] = pod_register_uuid
            elif ret != MxSmlReturn.MXSML_OperationNotSupport:
                print("mxSmlGetSgpuInfo failed: %s" % (mxsml_get_error_string(ret)))
                self.need_init = True
                break


    def get_sgpu_usage(self, metric_id):
        with self.lock:
            for (device_id, sgpu_id) in self.all_sgpu_info[self.back_index]:
                usage = c_int(0)
                ret = mxSmlGetSgpuUsage(device_id, sgpu_id, byref(usage))
                if ret != MxSmlReturn.MXSML_Success and ret != MxSmlReturn.MXSML_OperationNotSupport:
                    print(f"Device {device_id} Sgpu {sgpu_id} mxSmlGetSgpuUsage failed: "
                            + mxSmlGetErrorString(ret).decode('ASCII'))
                else:
                    self.update_sgpu_data(device_id, sgpu_id, metric_id, usage.value/100)


    def get_sgpu_memory_info(self, device_id, sgpu_id):
        memory = MxSmlSgpuMemoryInfo()
        ret = mxSmlGetSgpuMemory(device_id, sgpu_id, byref(memory))
        if ret != MxSmlReturn.MXSML_Success and ret != MxSmlReturn.MXSML_OperationNotSupport:
            print(f"Device {device_id} Sgpu {sgpu_id} mxSmlGetSgpuMemory failed: "
                    + mxSmlGetErrorString(ret).decode('ASCII'))
            self.need_init = True
            return
        with self.lock:
            self.sgpu_memory_info[self.back_index][(device_id, sgpu_id)] = memory


    def get_sgpu_memory_total(self, metric_id):
        with self.lock:
            for (device_id, sgpu_id) in self.sgpu_memory_info[self.back_index]:
                memory = self.sgpu_memory_info[self.back_index][(device_id, sgpu_id)]
                self.update_sgpu_data(device_id, sgpu_id, metric_id, memory.total/1024)


    def get_sgpu_memory_used(self, metric_id):
        with self.lock:
            for (device_id, sgpu_id) in self.sgpu_memory_info[self.back_index]:
                memory = self.sgpu_memory_info[self.back_index][(device_id, sgpu_id)]
                self.update_sgpu_data(device_id, sgpu_id, metric_id, memory.used/1024)


    def get_sgpu_memory_free(self, metric_id):
        with self.lock:
            for (device_id, sgpu_id) in self.sgpu_memory_info[self.back_index]:
                memory = self.sgpu_memory_info[self.back_index][(device_id, sgpu_id)]
                self.update_sgpu_data(device_id, sgpu_id, metric_id, memory.free/1024)


    def get_sgpu_compute_quota(self, metric_id):
        with self.lock:
            for (device_id, sgpu_id) in self.all_sgpu_info[self.back_index]:
                sgpuInfo = self.all_sgpu_info[self.back_index][(device_id, sgpu_id)]
                self.update_sgpu_data(device_id, sgpu_id, metric_id, sgpuInfo.computeQuota)


if __name__ == "__main__":
    metrics_required_sgpu = [
        "sgpu_compute_quota", "sgpu_usage", "sgpu_memory_total",
        "sgpu_memory_used", "sgpu_memory_free"
    ]

    monitor = SgpuMonitor()
    monitor.initialize()

    while True:
        monitor.monitor(metrics_required_sgpu, [0, 1, 2])
        print(monitor.get_sgpu_data())
        time.sleep(10)

