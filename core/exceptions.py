from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Unhandled exception (e.g. bare Python exceptions, 500s)
    # DRF returns None for these — we catch and format them
    if response is None:
        return Response(
            {
                "ok": False,
                "message": "A server error occurred.",
                "errors": {},
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    raw = response.data
    errors = {}
    message = ""

    if isinstance(raw, dict):
        for field, value in raw.items():

            # 'detail' = single string errors (auth, permission, 404, throttle)
            if field == "detail":
                message = str(value)
                continue

            # non_field_errors = cross-field / object-level validation errors
            if field == "non_field_errors":
                msgs = value if isinstance(value, list) else [value]
                message = message or str(msgs[0])
                errors["non_field_errors"] = [str(m) for m in msgs]
                continue

            # Field-level errors
            if isinstance(value, list):
                errors[field] = [str(m) for m in value]
            elif isinstance(value, dict):
                # Nested serializer errors — recurse one level
                errors[field] = _normalize_nested(value)
            else:
                errors[field] = [str(value)]

    elif isinstance(raw, list):
        # Top-level list errors (rare)
        message = str(raw[0]) if raw else "An error occurred."
        errors = {"detail": [str(e) for e in raw]}

    else:
        message = str(raw)

    response.data = {
        "ok": False,
        "message": message,
        "errors": errors,
        "status": response.status_code,
    }

    return response


def _normalize_nested(error_dict):
    """
    Recursively normalize nested serializer errors into
    consistent {field: [str, ...]} format.
    """
    result = {}
    for field, value in error_dict.items():
        if isinstance(value, list):
            result[field] = [str(m) for m in value]
        elif isinstance(value, dict):
            result[field] = _normalize_nested(value)
        else:
            result[field] = [str(value)]
    return result