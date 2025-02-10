from django.urls import path

from . import views


urlpatterns = [
    path("movie/", views.MovieListView.as_view()),
    #.../movie-list/?year_min=1997
    #../movie-list/?year_min=1997&year_max=2019
    #../movie-list/?year_min=1997&year_max=2019&genres=Боевик
    path("movie-list/", views.MovieList.as_view()),

    path("movie/<int:pk>/", views.MovieDetailView.as_view()),
    path("movie-detail/<int:pk>/", views.MovieDetail.as_view()),

    path("review/", views.ReviewCreateView.as_view()),
    path("review-create/", views.ReviewCreate.as_view()),

    path("rating/", views.AddStarRatingView.as_view()),
    path("rating-create", views.AddStarRating.as_view()),

    path("actors/", views.ActorsListView.as_view()),
    path("actors/<int:pk>/", views.ActorDetailView.as_view()),

]
