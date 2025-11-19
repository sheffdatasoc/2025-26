"""
Simple utilities for parsing MQTT messages.
"""
import json


def get_machine_name(topic):
    """Get machine name from topic (segment 3)"""
    parts = topic.split("/")
    return parts[3] if len(parts) > 3 else ""


def get_attribute_name(topic):
    """Get attribute name from topic (segment 6)"""
    parts = topic.split("/")
    return parts[6] if len(parts) > 6 else ""


def get_value(json_payload):
    """Extract 'value' field from JSON payload"""
    if not json_payload:
        return ""
    try:
        data = json.loads(json_payload)
        return str(data.get("value", ""))
    except:
        return ""
