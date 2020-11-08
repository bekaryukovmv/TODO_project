import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Item, TodoList


class ItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        allow_blank=False,
        error_messages={"blank": "You can't have blank item title"},
    )
    body = serializers.CharField(
        required=False,
        allow_blank=True,
        style={"base_template": "textarea.html"},
    )
    status = serializers.ChoiceField(
        choices=Item.STATUS_CHOICED, required=False
    )
    todo_list = serializers.PrimaryKeyRelatedField(
        queryset=TodoList.objects.all(), required=False
    )

    class Meta:
        model = Item
        exclude = ("created_at",)

        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=("todo_list", "title"),
                message="You've got this item in your list",
            )
        ]

    def validate_deadline(self, value):
        if value:
            if value < datetime.date.today():
                raise serializers.ValidationError(
                    "The deadline cannot be in the past!"
                )
        return value

    def to_internal_value(self, data):
        val = super().to_internal_value(data)

        if not val.get("body"):
            val["body"] = val["title"]

        if not val.get("todo_list"):
            val["todo_list"] = self.context.get("todo_list")

        return val


class TodoListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    personal_link = serializers.URLField(
        source="get_absolute_url", read_only=True
    )

    class Meta:
        model = TodoList
        fields = ("id", "name", "personal_link", "items")


class ChoicedListSerializer(serializers.Serializer):
    value = serializers.CharField()
    display_name = serializers.CharField()
