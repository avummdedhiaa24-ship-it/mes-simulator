import random


def simulate_machine_failure():
    failure = random.choice([True, False, False])  # 33% chance

    if failure:
        return {
            "status": "FAILED",
            "reason": "Machine overheating"
        }
    else:
        return {
            "status": "RUNNING"
        }
