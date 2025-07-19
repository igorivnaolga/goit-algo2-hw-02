from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)

    # Sort by priority (1 is highest), then by print_time descending for greedy grouping
    jobs.sort(key=lambda x: (x.priority, -x.print_time))

    print_order = []
    total_time = 0

    i = 0
    n = len(jobs)

    while i < n:
        group = []
        group_volume = 0

        j = i
        while j < n:
            job = jobs[j]
            if (
                len(group) < printer.max_items
                and group_volume + job.volume <= printer.max_volume
            ):
                group.append(job)
                group_volume += job.volume
                jobs.pop(j)
                n -= 1
            else:
                j += 1

        if group:
            print_order.extend([job.id for job in group])
            max_time = max(job.print_time for job in group)
            total_time += max_time
        else:
            # If no grouping was possible, forcibly schedule the next job alone
            job = jobs.pop(0)
            print_order.append(job.id)
            total_time += job.print_time
            n -= 1

    return {"print_order": print_order, "total_time": total_time}


# Testing


def test_printing_optimization():
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]

    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150},
    ]

    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {"max_volume": 300, "max_items": 2}

    print("Test 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nTest 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nTest 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
