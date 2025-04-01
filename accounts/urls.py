from django.urls import path
from django.urls import path
from .views import dashboard, learn_page, grade_lessons, grade1, grade2, grade3, grade4, grade5, grade1_alphabets, grade1_numbers, grade1_shapes
from django.conf import settings
from django.conf.urls.static import static
from .views import blind_login, mute_login, regular_login, login_selection, face_login
from .views import grade1_alphabets, run_quiz, progress, parent, daily, ai, breakk, ron, basket

urlpatterns = [
    path('', login_selection, name='login_selection'),  # Main login selection page
    path('blind/', blind_login, name='blind_login'),  # Voice login
    path('mute_login/', mute_login, name='mute_login'),  # Secret code login
    path('regular/', regular_login, name='regular_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('learn/', learn_page, name='learn_page'),  # Route for Learn page
    path('learn/grade/<int:grade>/', grade_lessons, name='grade_lessons'),  # Standard login
    path('learn/grade1/', grade1, name='grade1'),
    path('learn/grade1/alphabets/', grade1_alphabets, name='grade1_alphabets'),
    path('learn/grade1/numbers/', grade1_numbers, name='grade1_numbers'),
    path('learn/grade1/shapes/', grade1_shapes, name='grade1_shapes'),
    path('learn/grade2/', grade2, name='grade2'),
    path('learn/grade3/', grade3, name='grade3'),
    path('learn/grade4/', grade4, name='grade4'),
    path('learn/grade5/', grade5, name='grade5'),
    path("grade1_alphabets/", grade1_alphabets, name="grade1_alphabets"),
    path("grade1_shapes/", grade1_shapes, name="grade1_shapes"),
    path("face_login",face_login,name="face_login"),
    path("grade1_numbers/", grade1_numbers, name="grade1_numbers"),
    #path('grade4/', grade4_quiz, name='grade4_quiz'),
    path('run_quiz/', run_quiz, name='run_quiz'),
    path('progress/', progress, name='progress'),
    path('parent/', parent, name='parent'),
    path('daily/', daily, name='daily'),
    path('ai/', ai, name='ai'),
    path('breakk/', breakk, name='breakk'),
    path('daily/basket/', basket, name='daily/basket/'),
    path('daily/ron/', ron, name='daily/ron/'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)