# expenseTracker/views.py
from django.http import JsonResponse

def server_status(request):
    return JsonResponse({"status": "Server is up and running"})
