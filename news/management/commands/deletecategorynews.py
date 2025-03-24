from django.core.management.base import BaseCommand
from news.models import Category, Post, PostCategory

class Command(BaseCommand):
    help = "Удаляет все новости из указанной категории (с подтверждением)"

    def add_arguments(self, parser):
        parser.add_argument("category_id", type=int, help="ID категории для удаления новостей")

    def handle(self, *args, **kwargs):
        category_id = kwargs["category_id"]

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Категория с ID {category_id} не найдена."))
            return

        post_ids = list(PostCategory.objects.filter(category=category).values_list("post_id", flat=True))
        posts = Post.objects.filter(id__in=post_ids)

        if not posts.exists():
            self.stdout.write(self.style.WARNING(f"В категории '{category.name}' нет новостей."))
            return

        self.stdout.write(self.style.WARNING(f"Будет удалено {posts.count()} новостей из категории '{category.name}'."))
        confirm = input("Вы уверены? (yes/no): ")

        if confirm.lower() == "yes":
            posts.delete()

            PostCategory.objects.filter(post_id__in=post_ids).delete()

            self.stdout.write(self.style.SUCCESS(f"новости удалены"))
        else:
            self.stdout.write(self.style.ERROR("Операция отменена."))
