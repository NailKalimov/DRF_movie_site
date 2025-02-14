from rest_framework import generics, viewsets
from .service import get_client_ip, MovieFilter
from .models import Movie, Actor
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import (MovieListSerializer,
                         MovieDetailSerializer,
                         ReviewCreateSerializer,
                         CreateRatingSerializer,
                         ActorsListSerializer,
                         ActorDetailSerializer)


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset = MovieFilter

    def get_queryset(self):
        movies = (Movie.objects.filter(draft=False)
        .annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        ))
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorsListSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer