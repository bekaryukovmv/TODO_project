from django.urls import path

from . import views

app_name = "api"


urlpatterns = [
    path("lists/", views.TodoListCreateAPIView.as_view(), name="todo_lists"),
    path(
        "lists/<uuid:pk>/",
        views.TodoListRetrieveDestroyAPIView.as_view(),
        name="todo_list",
    ),
    path(
        "lists/<uuid:pk>/items/",
        views.ItemsListCreateAPIView.as_view(),
        name="todo_list_items",
    ),
    path(
        "lists/<uuid:list_pk>/items/<uuid:pk>/",
        views.ItemsRetrieveUpdateDestroyAPIView.as_view(),
        name="todo_list_single_item",
    ),
    path(
        "item-status-choices/",
        views.ItemStatusListAPIView.as_view(),
        name="item_status_choices",
    ),
]
