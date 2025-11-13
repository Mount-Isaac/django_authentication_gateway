from datetime import datetime

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
