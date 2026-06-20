import numpy as np


def estimate_distance(box_area, frame_area):
    ratio = box_area / frame_area

    if ratio > 0.25:
        return "very close"
    elif ratio > 0.10:
        return "nearby"
    elif ratio > 0.03:
        return "ahead"
    else:
        return "far"


def get_direction(box_center_x, frame_width):
    left_boundary = frame_width * 0.35
    right_boundary = frame_width * 0.65

    if box_center_x < left_boundary:
        return "on your left"
    elif box_center_x > right_boundary:
        return "on your right"
    else:
        return "ahead"


def get_box_area(box):
    x1, y1, x2, y2 = box
    width = x2 - x1
    height = y2 - y1
    return width * height


def build_announcement(detections, frame_width, frame_height):
    if not detections:
        return None

    frame_area = frame_width * frame_height
    messages = []
    sorted_dets = sorted(detections, key=lambda d: get_box_area(d['box']), reverse=True)
    top = sorted_dets[:3]

    for det in top:
        box = det['box']
        label = det['label']
        x1, y1, x2, y2 = box

        center_x = (x1 + x2) / 2
        box_area = get_box_area(box)

        dist = estimate_distance(box_area, frame_area)
        direction = get_direction(center_x, frame_width)

        msg = f"{label}, {dist}, {direction}"
        messages.append(msg)

    full_message = ". ".join(messages)
    return full_message


PRIORITY_OBJECTS = {
    'person': 10,
    'car': 9,
    'truck': 9,
    'bus': 9,
    'motorcycle': 8,
    'bicycle': 8,
    'dog': 7,
    'chair': 5,
    'dining table': 5,
    'bottle': 3,
    'cup': 3,
}

def get_priority(label):
    return PRIORITY_OBJECTS.get(label.lower(), 2)