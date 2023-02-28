from django.urls import path
from .import views

urlpatterns = [
    path('', views.MuseumView.as_view(), name='gallery'),
    path('<int:piece_id>/detailed_piece/', views.PieceDetailed.as_view(), name='detailed_piece'),
    path('<int:exh_id>/detail_exhibition/', views.ExhibitionDetailed.as_view(), name='detail_exhibition'),
    # path('<int:news_id>/detailed/', views.NewsDetailed.as_view(), name='detailed'),
    path('add_exhibition/', views.AddExhibition.as_view(), name='add_exhibition'),
    path('add_museum_piece/', views.AddMuseumPiece.as_view(), name='add_museum_piece'),
    path('add_author/', views.AddAuthor.as_view(), name='add_author'),
    path('add_hall/', views.AddHall.as_view(), name='add_hall'),
    path('<int:id>/update_exhibition/', views.ChangeExhibitons.as_view(), name='change_exhibitions'),
    path('<int:id>/update_museum_piece/', views.ChangeMuseumPiece.as_view(), name='change_museum_piece'),
    path("filter/", views.FilterPiecesView.as_view(), name='filter')
    #path('login/', views.Login.as_view(), name='login'),
    #path('logout/', views.Logout.as_view(), name='logout')
]