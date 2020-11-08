from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models import Item, TodoList


class ItemModelTest(TestCase):
    def test_default_body(self):
        item = Item()
        self.assertEqual(item.body, "")

    def test_related_item_to_list(self):
        list_ = TodoList.objects.create()
        item = Item(title="test")
        item.todo_list = list_
        item.save()
        self.assertIn(item, list_.items.all())

    def test_cannot_save_empty_title_items(self):
        list_ = TodoList.objects.create()
        item = Item(todo_list=list_, title="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_invalid_duplicates(self):
        list_ = TodoList.objects.create()
        Item.objects.create(todo_list=list_, title="something")
        with self.assertRaises(ValidationError):
            item = Item(todo_list=list_, title="something")
            item.full_clean()

    def test_can_create_same_item_from_different_lists(self):
        list1 = TodoList.objects.create()
        list2 = TodoList.objects.create()
        Item.objects.create(
            todo_list=list1, title="test title", body=" some body :-)"
        )
        item = Item(todo_list=list2, title="test title", body=" some body :-)")
        item.full_clean()

    def test_list_ordering(self):
        list1 = TodoList.objects.create()
        item1 = Item.objects.create(todo_list=list1, title="i1")
        item2 = Item.objects.create(todo_list=list1, title="item 2")
        item3 = Item.objects.create(todo_list=list1, title="3")
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_string_repr(self):
        item = Item(title="some text")
        self.assertEqual(str(item), "some text")


class ListModelTest(TestCase):
    def test_get_list_absolute_url(self):
        list_ = TodoList.objects.create()
        self.assertEqual(
            list_.get_absolute_url(), f"/api/v1/lists/{list_.id}/"
        )

    def test_list_name_is_first_item_title(self):
        list_ = TodoList.objects.create()
        Item.objects.create(todo_list=list_, title="first item")
        Item.objects.create(todo_list=list_, title="second item")
        self.assertEqual(list_.name, "first item")
