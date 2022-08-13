from rest_framework import serializers

from accounts.models import Account as User
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username")

    class Meta:
        model = Review
        fields = ('id', "rating", "review", "username", "date")

    def get_username(self, review):
        user = User.objects.get(pk=review.user.pk)
        return f"{str(user.first_name).capitalize()} {str(user.last_name).capitalize()}"
