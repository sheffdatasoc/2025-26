"""
Utility functions for parsing MQTT messages.
"""
import json
import logging

logger = logging.getLogger(__name__)


def get_machine_name(topic):
    """
    Extract machine name from MQTT topic.
    
    Args:
        topic: MQTT topic string
        
    Returns:
        Machine name from segment 3 of the topic
    """
    return _get_segment(topic, 3)


def get_attribute_name(topic):
    """
    Extract attribute name from MQTT topic.
    
    Args:
        topic: MQTT topic string
        
    Returns:
        Attribute name from segment 6 of the topic
    """
    return _get_segment(topic, 6)


def get_value(json_payload):
    """
    Extract value from JSON payload.
    
    Args:
        json_payload: JSON string containing the value
        
    Returns:
        Extracted value as string, or empty string if not found
    """
    if not json_payload:
        return ""
    
    try:
        data = json.loads(json_payload)
        value = data.get("value")
        return "" if value is None else str(value)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse JSON payload: {e}")
        return ""
    except Exception as e:
        logger.error(f"Unexpected error parsing payload: {e}")
        return ""


def _get_segment(topic, index):
    """
    Extract a segment from a topic string by index.
    
    Args:
        topic: Topic string with segments separated by '/'
        index: Zero-based index of the segment to extract
        
    Returns:
        Segment at the specified index, or empty string if not found
    """
    if not topic:
        return ""
    
    parts = topic.split("/")
    return parts[index] if len(parts) > index else ""
