from django.shortcuts import render, redirect
from django.db import connection
from django.utils import timezone
from django.http import HttpResponse


def execute_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
        return None


def view_users(request):
    users = execute_query("SELECT id, username, email FROM users")
    return render(request, 'view_users.html', {'users': users})


def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  
        execute_query(
            "INSERT INTO users (username, email, password, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
            [username, email, password, timezone.now(), timezone.now()]
        )
        return redirect('view_users')
    return render(request, 'add_user.html')


def update_user(request, user_id):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password') 
        execute_query(
            "UPDATE users SET username=%s, email=%s, password=%s, updated_at=%s WHERE id=%s",
            [username, email, password, timezone.now(), user_id]
        )
        return redirect('view_users')
    

    user = execute_query("SELECT id, username, email FROM users WHERE id=%s", [user_id])
    if user:
        return render(request, 'update_user.html', {'user': user[0]})
    return HttpResponse("User not found", status=404)


def delete_user(request, user_id):
    execute_query("DELETE FROM users WHERE id=%s", [user_id])
    return redirect('view_users')
