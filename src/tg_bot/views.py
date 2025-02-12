from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


@csrf_exempt
def me_view(request):
    username = request.GET.get("username")

    if not username:
        return JsonResponse({"error": "Укажите telegram_id в параметрах запроса"}, status=400)

    user = get_object_or_404(User, username=username)

    user_info = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "date_joined": user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return JsonResponse(user_info)
