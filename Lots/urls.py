from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register(r'lots', views.LotViewSet, basename='lots')

urlpatterns = router.urls

urlpatterns += [
    path('lots/update_rate/<int:pk>', views.UpdateRateView.as_view()),

]