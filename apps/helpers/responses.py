from datetime import datetime
from json import (
    dumps,
    loads, 
    JSONDecodeError
)
from rest_framework.response import Response
from termcolor import colored

def format_response(
    success: bool,
    message: str,
    request_id: str,
    data=None,
    error=None,
    status_code: int | None = None
) -> dict:
    """
    Formats API responses into a consistent structure for both success and error cases.

    Success:
    {
        "success": true,
        "message": "Action completed successfully",
        "data": {...},
        "meta": {
            "request_id": "...",
            "timestamp": "2025-11-12T19:20:30Z"
        }
    }

    Error:
    {
        "success": false,
        "message": "Order not found",
        "error": {
            "type": "NotFoundError",
            "details": "Order with ID 9876 not found"
        },
        "meta": {
            "request_id": "...",
            "timestamp": "2025-11-12T19:20:30Z"
        }
    }
    """

    response = {
        "success": success,
        "message": message,
        "meta": {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat() + "Z"
        }
    }

    # add data for successful responses
    if success and data is not None:
        response["data"] = data

    # add error details for failed responses
    if not success and error is not None:
        response["errors"] = error

    return response


def flatten_errors(errors):
    messages = []
    for field, detail in errors.items():
        # Handle nested dicts (e.g., serializer inside serializer)
        if isinstance(detail, dict):
            nested = flatten_errors(detail)
            messages.extend([f"{field} → {msg}" for msg in nested])
        # Handle list of messages
        elif isinstance(detail, list):
            messages.extend([f"{field}: {msg}" for msg in detail])
        # Handle single string
        else:
            messages.append(f"{field}: {detail}")
    return messages


def format_request_body(bytes_data):
    try:
        # parse valid JSON
        return loads(bytes_data)
    except JSONDecodeError:
        try:
            # decode bytes → string
            text = bytes_data.decode() if isinstance(bytes_data, (bytes, bytearray)) else str(bytes_data)
            # format to JSON
            return pretty_fallback_format(text)
        except Exception:
            return str(bytes_data)

def pretty_fallback_format(text):
    """
    Attempt to make malformed JSON readable with indentation.
    Adds indentation and newlines similar to JSON formatting.
    """
    lines = []
    indent = 0
    for char in text:
        if char == '{':
            lines.append('{')
            indent += 4
            lines.append('' + ' ' * indent)
        elif char == '}':
            indent -= 4
            lines.append('' + ' ' * indent + '}')
        elif char == ',':
            lines.append(',' + ' ' * indent)
        else:
            lines.append(char)
    return ''.join(lines)


def log_request_response(request_id, request_body_bytes, response):
    request_body = format_request_body(request_body_bytes) if request_body_bytes else {}
    response_data = response.data if isinstance(response, Response) else {}
    print(
        f"\n{'=' * 60}\n"
        f"{' '*24}{colored('Request Log', 'cyan', attrs=['bold'])}\n"
        f"{'=' * 60}\n"
        f"{colored('request_id:', 'yellow')} {request_id}\n"
        f"{colored('request_data:', 'yellow')} "
        f"{dumps(request_body, indent=4, ensure_ascii=False) if isinstance(request_body, dict) else request_body}\n"
        f"{colored('response:', 'yellow')} {dumps(response_data, indent=4, ensure_ascii=False)}\n"
    )

