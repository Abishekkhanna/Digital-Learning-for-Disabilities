from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser
import speech_recognition as sr
import os
import sys




import subprocess

from django.shortcuts import render


def dashboard(request):
    return render(request, "accounts/dashboard.html")  # Make sure this template exists


def login_selection(request):
    return render(request, 'accounts/login_selection.html')  # Make sure this template exists

# Blind Student Login (Voice-Based)
import speech_recognition as sr
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.urls import reverse

def blind_login(request):
    if request.method == "POST":
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Adjusting for background noise... Speak now.")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for noise

            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # Increased timeout
                print("Processing speech...")

                spoken_password = recognizer.recognize_google(audio).strip()
                print("Recognized:", spoken_password)

                if spoken_password == "123":
                    user = authenticate(username="blind_user", password="123")
                    if user:
                        login(request, user)
                        return redirect(reverse("dashboard"))
                    return JsonResponse({"message": "Authentication failed"}, status=401)
                else:
                    return JsonResponse({"message": "Incorrect password"}, status=400)

            except sr.WaitTimeoutError:
                print("No speech detected. Try speaking again.")
                return JsonResponse({"message": "No speech detected. Please try again."}, status=400)
            except sr.UnknownValueError:
                print("Speech not understood. Speak more clearly.")
                return JsonResponse({"message": "Could not understand. Try again."}, status=400)
            except sr.RequestError:
                print("Speech recognition service unavailable.")
                return JsonResponse({"message": "Speech recognition service unavailable."}, status=500)

    return render(request, "accounts/blind_login.html")

from django.contrib import messages

# Mute Student Login (Secret Code)
def mute_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        secret_code = request.POST.get("password")

        if username == "admin" and secret_code == "123":
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid username or secret code.")
            return redirect("mute_login")  # Redirect back to login page

    return render(request, "accounts/login_selection.html")
# Deaf & Physically Disabled Student Login (Regular Login)
def regular_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user and user.user_type == "regular":
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            return render(request, "regular_login.html", {"error": "Invalid credentials"})

    return render(request, "regular_login.html")


from django.shortcuts import render

def learn_page(request):
    return render(request, 'accounts/learn.html')

def grade_lessons(request, grade):
    return render(request, 'accounts/grade_lessons.html', {'grade': grade})

def learn_page(request):
    return render(request, 'accounts/learn.html')

def grade1(request):
    return render(request, 'accounts/grade1.html')

def grade1_alphabets(request):
    return render(request, 'accounts/grade1_alphabets.html')

def grade1_numbers(request):
    return render(request, 'accounts/grade1_numbers.html')

def grade1_shapes(request):
    return render(request, 'accounts/grade1_shapes.html')

def grade2(request):
    return render(request, 'accounts/grade2.html')

def grade3(request):
    return render(request, 'accounts/grade3.html')

def grade4(request):
    subprocess.Popen(["python","accounts/templates/accounts/quiz.py"])
    return render(request, 'accounts/grade4.html')

import subprocess

def grade5(request):
    subprocess.Popen(["python","accounts/templates/accounts/hand_control.py"])
    return render(request, 'accounts/grade5.html')



def grade1_alphabets(request):
    script_path = os.path.abspath("C:/Abishek Khanna/Django Project/Django Project/learning_platform/practice.py")  # ✅ Use absolute path 

    try:
        # ✅ Run script and capture errors
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        print("STDOUT:", result.stdout)  # ✅ Check output
        print("STDERR:", result.stderr)  # ✅ Check errors

    except Exception as e:
        print("Error running script:", str(e))

    return render(request, "accounts/grade1_alphabets.html")


def grade1_shapes(request):
    script_path = os.path.abspath("C:/Abishek Khanna/Django Project/Django Project/learning_platform/assesment.py")  # ✅ Use absolute path 

    try:
        # ✅ Run script and capture errors
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        print("STDOUT:", result.stdout)  # ✅ Check output
        print("STDERR:", result.stderr)  # ✅ Check errors

    except Exception as e:
        print("Error running script:", str(e))

    return render(request, "accounts/grade1_shapes.html")

def grade1_numbers(request):
    script_path = os.path.abspath("C:/Abishek Khanna/Django Project/Django Project/learning_platform/33Numbers.py")  # ✅ Use absolute path 

    try:
        # ✅ Run script and capture errors
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        print("STDOUT:", result.stdout)  # ✅ Check output
        print("STDERR:", result.stderr)  # ✅ Check errors

    except Exception as e:
        print("Error running script:", str(e))

    return render(request, "accounts/grade1_numbers.html")


def face_login(request):
    pass


import subprocess
import os
from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
import subprocess

def grade4(request):
    return render(request, 'accounts/grade4.html')

def run_quiz(request):
    try:
        # Run the Python script
        result = subprocess.run(['python', 'quiz.py'], capture_output=True, text=True)
        return HttpResponse(f"Quiz Started: {result.stdout}")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

def progress(request):
    return render(request, 'accounts/progress.html')

def parent(request):
    return render(request, 'accounts/parents.html')

def ai(request):
    return render(request, 'accounts/ai.html')

def daily(request):
    return render(request, 'accounts/daily.html')

def breakk(request):
    return render(request, 'accounts/break.html')

def ron(request):
    return render(request, 'accounts/ron.html')

def basket(request):
    return render(request, 'accounts/basket.html')