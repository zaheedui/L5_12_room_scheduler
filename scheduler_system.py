
"""Room scheduling system with reservation and equipment tracking."""

import json
from collections import Counter
from datetime import datetime
from itertools import count


reservations = {}
equipment_pool = {"projector": 2, "microphone": 4, "webcam": 1}
conflicts = []
_reservation_ids = count(1)


def schedule_room(room_id, time_slot, equipment_list=None):
    """Schedule a room, record conflicts, and reserve available equipment."""
    if equipment_list is None:
        equipment_list = []

    if not isinstance(room_id, str) or not room_id.strip():
        raise ValueError("room_id must be a non-empty string.")

    if not isinstance(time_slot, str):
        raise TypeError("time_slot must be a string such as '09-11'.")

    try:
        start, end = time_slot.split("-")
        start_hour = int(start)
        end_hour = int(end)
    except ValueError as exc:
        raise ValueError(
            "time_slot must use the format '09-11'."
        ) from exc

    if not 0 <= start_hour < end_hour <= 24:
        raise ValueError("time_slot must have valid, increasing hours.")

    if not isinstance(equipment_list, (list, tuple)):
        raise TypeError("equipment_list must be a list or tuple.")

    requested_equipment = Counter(equipment_list)

    for equipment, quantity in requested_equipment.items():
        if equipment not in equipment_pool:
            raise ValueError(f"Unknown equipment: {equipment}")
        if quantity > equipment_pool[equipment]:
            raise ValueError(f"Not enough {equipment} available.")

    for reservation in reservations.values():
        if (
            reservation["room"] == room_id
            and reservation["slot"] == time_slot
        ):
            conflicts.append(
                f"{room_id} double-booked at {time_slot}"
            )

    for equipment, quantity in requested_equipment.items():
        equipment_pool[equipment] -= quantity

    reservation_id = next(_reservation_ids)
    reservations[reservation_id] = {
        "room": room_id,
        "slot": time_slot,
        "equipment": list(equipment_list),
    }

    return reservation_id


def cancel_reservation(reservation_id):
    """Cancel an existing reservation and return its equipment."""
    if reservation_id not in reservations:
        return

    reservation = reservations.pop(reservation_id)

    for equipment in reservation["equipment"]:
        equipment_pool[equipment] += 1


def slot_hours(time_slot):
    """Return the duration of a valid time slot in hours."""
    if not isinstance(time_slot, str):
        raise TypeError("time_slot must be a string such as '09-11'.")

    try:
        start, end = time_slot.split("-")
        start_hour = int(start)
        end_hour = int(end)
    except ValueError as exc:
        raise ValueError(
            "time_slot must use the format '09-11'."
        ) from exc

    if not 0 <= start_hour < end_hour <= 24:
        raise ValueError("time_slot must have valid, increasing hours.")

    return end_hour - start_hour


def export_schedule(file="schedule.json"):
    """Export reservations to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(reservations, output_file, indent=4)


def logConflicts(file="conflicts.log"):  # pylint: disable=invalid-name
    """Append scheduling conflicts to a log and display its contents."""
    with open(file, "a", encoding="utf-8") as output_file:
        for conflict in conflicts:
            output_file.write(f"{datetime.now()} {conflict}\n")

    with open(file, "r", encoding="utf-8") as log_file:
        print(log_file.read())


def main():
    """Demonstrate room scheduling and reservation management."""
    schedule_room("Board-1", "09-11")
    schedule_room("Board-1", "09-11")

    reservation_id = schedule_room("Huddle-3", "14-16")
    print(
        "Slot length for b:",
        slot_hours(reservations[reservation_id]["slot"]),
    )

    cancel_reservation(77)

    slot = (
        input("Slot for Board-2, like 10-12 (Enter for 10-12): ")
        or "10-12"
    )
    schedule_room("Board-2", slot, ["projector", "webcam"])

    export_schedule()
    logConflicts()

    print("Equipment left:", equipment_pool)
    print("Reservations:", reservations)


if __name__ == "__main__":
    main()
