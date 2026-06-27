import psutil
import time
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()

    def cpu(self):
        return psutil.cpu_percent(interval=1)

    def memory(self):
        mem = psutil.virtual_memory()
        return {"total": f"{mem.total/1024/1024/1024:.1f}GB", "used": f"{mem.used/1024/1024/1024:.1f}GB", "percent": mem.percent}

    def disk(self):
        disk = psutil.disk_usage("/")
        return {"total": f"{disk.total/1024/1024/1024:.0f}GB", "used": f"{disk.used/1024/1024/1024:.0f}GB", "percent": disk.percent}

    def stats(self):
        uptime = time.time() - self.start_time
        return {
            "cpu_percent": self.cpu(),
            "memory": self.memory(),
            "disk": self.disk(),
            "uptime_seconds": int(uptime),
            "timestamp": datetime.now().isoformat()
        }

    def print_stats(self):
        s = self.stats()
        print(f"📊 CPU: {s['cpu_percent']}% | RAM: {s['memory']['used']}/{s['memory']['total']} ({s['memory']['percent']}%) | Disk: {s['disk']['used']}/{s['disk']['total']}")

    def health_check(self, services=None):
        results = {}
        services = services or []
        for name, check_func in services.items():
            try:
                results[name] = "OK" if check_func() else "FAIL"
            except Exception as e:
                results[name] = f"ERROR: {e}"
        return results

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.print_stats()