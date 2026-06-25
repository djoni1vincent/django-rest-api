from rest_framework import serializers

from posts.models import Post, User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class PostSerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "author", "content", "created_at", "preview"]
        read_only_fields = ["id", "created_at", "author"]

    def get_preview(self, obj):
        return (obj.content[:100] + "...") if len(obj.content) > 100 else obj.content

    def validate_title(self, value):
        title = value.strip()
        if len(title) < 5:
            raise serializers.ValidationError("Title cannot be less then 5 symbols")
        return title

    def validate_content(self, value):
        content = value.strip()
        if not content:
            raise serializers.ValidationError("Content cannot be empty")
        return content
