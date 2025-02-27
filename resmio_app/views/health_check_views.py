from django.db import connections
from django.http import JsonResponse
from django.views import View

class HealthCheckView(View):
    """
    A health check that verifies the database connection.
    """
    def get(self, _):
        try:
            connection = connections["default"]
            connection.cursor()
        except Exception as e:
            return JsonResponse({"status": "unhealthy", "error": str(e)}, status=500)

        return JsonResponse({"status": "healthy"}, status=200)
