import time
import psutil
import os

def measure_performance(func, *args, **kwargs):
    """Măsoară timpul și memoria pentru o funcție"""
    process = psutil.Process(os.getpid())
    
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    start_time = time.time()
    
    result = func(*args, **kwargs)
    
    end_time = time.time()
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    
    return {
        'result': result,
        'time': round(end_time - start_time, 4),
        'memory': round(mem_after - mem_before, 2)
    }
