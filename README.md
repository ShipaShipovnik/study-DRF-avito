Данный проект представляет собой базу данных работающую с помощью апи с пользователем. Проект представляет собой базу данных сервиса по размещению объявлений по продаже.

# Описание используемых технологий
***Серилизаторы** преобразовывают данные в формат json.*
Серилизаторы находятся в файле serializers.py.

**Представления** были написаны с помощью generics классов. В django rest framework эти классы упрощают работу с методами CRUD (Create, Retrieve, Update, Delete). Они упрощают создание API, предоставляя готовые реализации для этих операций, чтобы не писать много повторяющегося кода.* Находятся в файле views.py

Права доступа находятся в файле permissions.py.
```python
from rest_framework import permissions

class IsOwnerReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
```

В основном используются данные разрешения:
- `IsAuthenticatedOrReadOnly`, что означает:
    - **Чтение**: Доступно всем пользователям.
    - **Запись**: Доступно только аутентифицированным пользователям.
- **`IsOwnerReadOnly`**: Пользователь может обновлять или удалять объект только в том случае, если он является владельцем поста.
# Пользователь. User.
views.py :
```python
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
```
serializers.py :
```python
  class UserSerializer(serializers.ModelSerializer):
      posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
      comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
      categories = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
  
      class Meta:
          model = User
          fields = ['id', 'username', 'posts', 'comments','categories']
```

# Объявление. Post
модель:
```python
class Post(models.Model):  
    created = models.DateTimeField(auto_now_add=True)  
    title = models.CharField(max_length=100, blank=True, default='')  
    price = models.FloatField(blank=False)  
    body = models.TextField(blank=True, default='')  
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)  
    categories = models.ManyToManyField('Category', related_name='post_set', blank=True)  
  
    class Meta:  
        ordering = ['created']  
        verbose_name = 'Объявление'  
        verbose_name_plural = 'Объявления'  
  
    def __str__(self):  
        return self.title
```
views.py :
```python
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
```
serializers.py :
```python
class PostSerializer(serializers.ModelSerializer):  
    owner = serializers.ReadOnlyField(source='owner.username')  
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  
  
    class Meta:  
        model = Post  
        fields = ['id', 'title', 'body', 'owner', 'comments','price', 'categories']
```
# Отзыв. Comment 
модель:
```python
class Comment(models.Model):  
    created = models.DateTimeField(auto_now_add=True)  
    body = models.TextField(blank=False)  
    stars = models.IntegerField(blank=False, validators=[MaxValueValidator(5)])  
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)  
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)  
  
    class Meta:  
        ordering = ['created']  
        verbose_name = 'Отзыв'  
        verbose_name_plural = 'Отзывы'  
  
    def __str__(self):  
        return self.body
```
views.py :
```python
class CommentList(generics.ListCreateAPIView):  
    queryset = Comment.objects.all()  
    serializer_class = serializers.CommentSerializer  
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  
  
    def perform_create(self, serializer):  
        serializer.save(owner=self.request.user)  
  
  
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):  
    queryset = Comment.objects.all()  
    serializer_class = serializers.CommentSerializer  
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
```
serializers.py :
```python
class CommentSerializer(serializers.ModelSerializer):  
    owner = serializers.ReadOnlyField(source='owner.username')  
  
    class Meta:  
        model = Comment  
        fields = ['id', 'body', 'stars','owner', 'post']
```
# Категория. Category.
views.py :
```python
class CategoryList(generics.ListCreateAPIView):  
    queryset = Category.objects.all()  
    serializer_class =  serializers.CategorySerializer  
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  
  
    def perform_create(self, serializer):  
        serializer.save(owner=self.request.user)  
  
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):  
    queryset = Category.objects.all()  
    serializer_class = serializers.CategorySerializer  
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
```
serializers.py :
```python
class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'owner', 'posts']
```
# РАБОТА С POSTMAN и ЗАПРОСАМИ
## POST
Добавление отзыва

![image](https://github.com/user-attachments/assets/bead9024-ea32-43d5-bab2-e28472bae15c)

## GET
Получение всех объявлнией

![image](https://github.com/user-attachments/assets/addc8289-fea5-415a-a9c5-26e91512ba16)

## PUT
Изменение цены в объявлении

![image](https://github.com/user-attachments/assets/c52ceae8-9ae6-444c-ae06-086c82f6c192)

## DELETE
Удаление категории

![image](https://github.com/user-attachments/assets/3cf46640-d979-4597-b13c-ee10482c7f24)
