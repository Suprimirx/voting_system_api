from django.urls import path, include
from rest_framework import routers
from voting import views

router = routers.DefaultRouter()
router.register(r'voters', views.VoterViewSet)
router.register(r'candidates', views.CandidateViewSet)
router.register(r'votes', views.VoteViewSet)  

urlpatterns = [
    # path('your_app/', include('your_app.urls')),
    path('api/', include(router.urls))
]