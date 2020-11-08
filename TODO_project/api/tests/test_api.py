import json

from django.test import TestCase
from django.urls import reverse

from api.models import Item, TodoList


class ListAPITest(TestCase):
    base_url = "/api/v1/lists/{}/"

    def test_get_returns_json_200(self):
        list_ = TodoList.objects.create()
        response = self.client.get(self.base_url.format(list_.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

    def test_get_returns_items_for_correct_list(self):
        other_list = TodoList.objects.create()
        Item.objects.create(
            todo_list=other_list, title="test 1", body="test 1"
        )
        our_list = TodoList.objects.create()
        item1 = Item.objects.create(
            todo_list=our_list, title="item 1", body="body 1"
        )
        item2 = Item.objects.create(
            todo_list=our_list, title="item 2", body="body 2"
        )
        response = self.client.get(self.base_url.format(our_list.id))
        self.assertEqual(
            json.loads(response.content.decode("utf8")),
            {
                "id": str(our_list.id),
                "name": our_list.name,
                "personal_link": str(our_list.get_absolute_url()),
                "items": [
                    {
                        "id": str(item1.id),
                        "title": item1.title,
                        "body": item1.body,
                        "status": item1.status,
                        "todo_list": str(our_list.id),
                        "deadline": item1.deadline,
                    },
                    {
                        "id": str(item2.id),
                        "title": item2.title,
                        "body": item2.body,
                        "status": item2.status,
                        "todo_list": str(our_list.id),
                        "deadline": item2.deadline,
                    },
                ],
            },
        )


class ItemsAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TodoList.objects.create()

    def setUp(self):
        self.list_ = TodoList.objects.first()
        self.base_url = reverse(
            "api:todo_list_items", kwargs={"pk": str(self.list_.id)}
        )

    def test_POSTing_a_new_item(self):
        list_ = TodoList.objects.create()
        response = self.client.post(
            self.base_url,
            {
                "todo_list": list_.id,
                "title": "new item",
                "body": "test body",
                "status": "progress",
            },
        )
        self.assertEqual(response.status_code, 201)
        new_item = list_.items.get()
        self.assertEqual(new_item.title, "new item")
        self.assertEqual(new_item.body, "test body")
        self.assertEqual(new_item.status, "progress")
        self.assertEqual(new_item.deadline, None)

    def post_empty_input(self):
        return self.client.post(
            self.base_url, data={"todo_list": self.list_.id, "title": ""},
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_empty_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_returns_error_code(self):
        response = self.post_empty_input()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content.decode("utf8")),
            {"title": ["You can't have blank item title"]},
        )

    def test_duplicate_items_error(self):
        self.client.post(
            self.base_url.format(self.list_.id),
            data={"todo_list": self.list_.id, "title": "duplicate"},
        )
        response = self.client.post(
            self.base_url.format(self.list_.id),
            data={"todo_list": self.list_.id, "title": "duplicate"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content.decode("utf8")),
            {"non_field_errors": ["You've got this item in your list"]},
        )
