from rest_framework import serializers

from .models import Movie, Review


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'tagline')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class FilterListReviewSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


# class SubReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ('name', 'text', 'children')


class RecursiveFieldSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        serialised_data = ReviewSerializer(value, context=self.context).data
        return serialised_data


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveFieldSerializer(many=True)

    class Meta:
        list_serializer_class = FilterListReviewSerializer
        model = Review
        fields = ('name', 'text', 'children')


class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)
