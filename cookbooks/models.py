# D:\PythonProject\WebParsing\cookbooks\models.py


import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models



# Пользователь (заглушка, если есть кастомная модель — используйте её)
from django.contrib.auth import get_user_model
User = get_user_model()


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Email is required')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)
#
# class User(AbstractBaseUser, PermissionsMixin):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Полное имя')
#     email = models.EmailField(unique=True, blank=True, null=True)
#     provider_email = models.BooleanField(default=False, help_text="Регистрация по Email (true - запрет на изменение данных)")
#     phone_country = models.CharField(max_length=10, blank=True, null=True, verbose_name='Телефонный код страны')
#     phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
#     question_phone = models.CharField(max_length=255, blank=True, null=True, verbose_name='Контрольный вопрос')
#     answer = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ответ на контрольный вопрос')
#     provider_phone = models.BooleanField(default=False, help_text="Регистрация по телефону (true - запрет на изменение данных)")
#     social_provider = models.CharField(max_length=50, blank=True, null=True, verbose_name='Провайдер соц. сети')
#     avatar_url = models.URLField(blank=True, null=True, verbose_name='Фото пользователя')
#     avatar_blur_hash_url = models.URLField(blank=True, null=True, verbose_name='Blur hash фото')
#     birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
#     gender = models.CharField(max_length=50, blank=True, null=True, verbose_name='Гендерная идентичность')
#
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     objects = CustomUserManager()
#
#     def __str__(self):
#         return self.full_name or self.email or str(self.id)


# Категории
class Category(models.Model):
    """
    Категории рецептов (завтрак, обед и т.д.)
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название категории"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Краткое описание"
    )
    type = models.CharField(
        max_length=50,
        choices=[
            ('image', 'Изображение'),
            ('youtube', 'YouTube')
        ],
        default='image',
        verbose_name="Тип медиа"
    )
    url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на фото/видео"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['title']

    def __str__(self):
        return self.title


# модель Ингредиенты
class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)


# модель Теги
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)


# модель Рецепты
class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='recipes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recipes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(
        max_length=20,
        choices=[('image', 'Image'), ('youtube', 'YouTube')],
        default='image'
    )
    url = models.URLField(max_length=500, blank=True)
    time_to_cook = models.PositiveIntegerField(null=True, blank=True, help_text="Время приготовления в минутах")
    servings = models.PositiveIntegerField(null=True, blank=True, help_text="Количество порций")
    is_public = models.BooleanField(default=True)
    created_updated_in = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, through='RecipeTag', related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')

    def __str__(self):
        return self.title

'''
В Django связи "многие ко многим" (ManyToManyField) обычно не требуют явного создания модели связи при использовании. 
Django автоматически создает скрытую модель связи для отслеживания связей "многие ко многим" в базе данных. 
По умолчанию, эта модель связи получает имя, составленное из имен моделей, объединенных подчеркиванием.
??? - не решенный вопрос: В таблице 'Связь рецептов и ингредиентов', первоначально планировалось так-же 
хранить информацио о количестве ингридиентов, потому таблицы связей будем создавать явно
'''
# Связь рецептов и ингредиентов
class RecipeIngredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amt = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=50)


# Связь рецептов и тегов
class RecipeTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

