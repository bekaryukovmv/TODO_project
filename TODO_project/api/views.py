from rest_framework import generics, response, status
from rest_framework.generics import get_object_or_404

from .models import Item, TodoList
from .serializers import (
    ChoicedListSerializer,
    ItemSerializer,
    TodoListSerializer,
)


class TodoListCreateAPIView(generics.ListCreateAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer


class TodoListRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer


class ItemsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.todo_list = get_object_or_404(TodoList, pk=self.kwargs.get("pk"))

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(todo_list=self.todo_list)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"todo_list": self.todo_list}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ItemsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemStatusListAPIView(generics.ListAPIView):
    queryset = [
        {"value": key, "display_name": val}
        for (key, val) in Item.STATUS_CHOICED
    ]
    serializer_class = ChoicedListSerializer
