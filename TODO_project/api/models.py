import uuid as uuid_lib

from django.db import models
from django.urls import reverse


# use this base class because use UUID is best practice for Rest API
class BaseClass(models.Model):
    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class TodoList(BaseClass):
    @property
    def name(self):
        try:
            return self.items.first().title
        except AttributeError:
            return ""

    def get_absolute_url(self):
        return reverse("api:todo_list", kwargs={"pk": str(self.id)})

    def __str__(self):
        return str(self.id)


class Item(BaseClass):
    STATUS_CHOICED = [
        ("not_start", "Not Started"),
        ("progress", "In Progress"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    title = models.CharField(max_length=200)
    body = models.TextField(default="")
    status = models.CharField(max_length=10, blank=True, default="not_start")

    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    todo_list = models.ForeignKey(
        TodoList, on_delete=models.CASCADE, related_name="items"
    )

    class Meta:
        ordering = ("created_at",)
        unique_together = ("title", "todo_list")

    def __str__(self):
        return self.title
