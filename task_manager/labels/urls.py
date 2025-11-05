from django.urls import path
from . import views

app_name = "labels"

urlpatterns = [
    path("", views.LabelsListView.as_view(), name="labels_list"),
    path("create/", views.LabelCreateView.as_view(), name="labels_create"),
    path('<int:pk>/', views.LabelDetailView.as_view(), name='labels_detail'),
    path("<int:pk>/update/", views.LabelUpdateView.as_view(), name="labels_update"),
    path("<int:pk>/delete/", views.LabelDeleteView.as_view(), name="labels_delete"),
]
