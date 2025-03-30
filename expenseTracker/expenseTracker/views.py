# expenseTracker/views.py
from django.http import JsonResponse

def server_status(request):
    """Server up status view"""
    return JsonResponse({"status": "Server is up and running"})
