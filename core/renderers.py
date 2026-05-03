import json
from rest_framework.renderers import JSONRenderer


class StandardRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None
        status_code = response.status_code if response else 200

        # Let exception handler own 4xx/5xx — don't double-wrap
        if status_code >= 400:
            return super().render(data, accepted_media_type, renderer_context)

        # 204 No Content — data is None
        if data is None:
            payload = {
                "ok": True,
                "data": None,
                "status": status_code,
            }
            return json.dumps(payload).encode()

        # Paginated response — DRF pagination injects 'results' key
        if isinstance(data, dict) and "results" in data:
            payload = {
                "ok": True,
                "data": data["results"],
                "pagination": {
                    "count": data.get("count"),
                    "next": data.get("next"),
                    "previous": data.get("previous"),
                },
                "status": status_code,
            }
        else:
            payload = {
                "ok": True,
                "data": data,
                "status": status_code,
            }

        return json.dumps(payload).encode()