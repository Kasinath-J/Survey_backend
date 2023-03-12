from django.urls import path
from .views import LayoutList,LayoutCreate,LayoutSearch,LayoutResponse,LayoutAnalyse,LayoutTrain

urlpatterns = [

    # To retrieve Office Bearers
    path('list/', LayoutList.as_view()),
    path('train/', LayoutTrain.as_view()),
    path('create/', LayoutCreate.as_view()),
    path('search/', LayoutSearch.as_view()),
    path('response/', LayoutResponse.as_view()),
    path('analyse/', LayoutAnalyse.as_view()),

]
