from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    # author = SlugRelatedField(read_only=True, slug_field='username')
    author = serializers.IntegerField(read_only=True, default=1)  # заменить на User
    # title = serializers.HiddenField()

    class Meta:
        exclude = ('title',)
        # fields = '__all__'
        model = Review

        validators = [
            UniqueTogetherValidator(queryset=Review.objects.all(),
                                    fields=('text', 'author'))
        ]

    def create(self, validated_data):
        title_id = self.context['title_id']
        print('title_id = ', title_id)
        validated_data['title'] = get_object_or_404(Title, pk=title_id)
        return super(ReviewSerializer, self).create(validated_data)

    # def get_title_object(self):
    #     title_id = self.context['title_id']
    #     return get_object_or_404(Title, pk=title_id)
