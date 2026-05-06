from collections.abc import Mapping
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from core.logging_context import get_request_id


class EnvelopedJSONRenderer(JSONRenderer):

    _SUCCESS_MESSAGES = {
        status.HTTP_200_OK: "Request successful.",
        status.HTTP_201_CREATED: "Resource created successfully.",
        status.HTTP_202_ACCEPTED: "Request accepted.",
        status.HTTP_204_NO_CONTENT: "Request completed successfully.",
    }

    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        request = renderer_context.get("request")
        response = renderer_context.get("response")

        if self._should_skip_wrapping(request):
            return super().render(data, accepted_media_type, renderer_context)

        if self._is_already_enveloped(data):
            return super().render(data, accepted_media_type, renderer_context)

        status_code = getattr(response, "status_code", status.HTTP_200_OK)
        if status_code >= 400:
            return super().render(data, accepted_media_type, renderer_context)

        payload = {
            "success": True,
            "message": self._SUCCESS_MESSAGES.get(status_code, "Request successful."),
            "request_id": get_request_id(),
        }

        if self._is_paginated(data):
            payload["data"] = data.get("results", [])
            payload["count"] = data.get("count")
            payload["next"] = data.get("next")
            payload["previous"] = data.get("previous")
        elif data is not None:
            payload["data"] = data

        return super().render(payload, accepted_media_type, renderer_context)

    @staticmethod
    def _is_paginated(data) -> bool:
        return isinstance(data, Mapping) and {"count", "next", "previous", "results"}.issubset(data.keys())

    @staticmethod
    def _is_already_enveloped(data) -> bool:
        return isinstance(data, Mapping) and {"success", "message", "request_id"}.issubset(data.keys())

    @staticmethod
    def _should_skip_wrapping(request) -> bool:
        if request is None:
            return False

        path = request.path.rstrip("/")
        return path.endswith("/api/v1/schema")
