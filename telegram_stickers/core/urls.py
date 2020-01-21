from django.urls import path
from core.api.views import StickerPackListView, StickerPackView

app_name = 'core'

urlpatterns = [
    path('sticker-packs/', StickerPackListView.as_view(), name='sticker-pack-list'),
    path('sticker-packs/<int:pk>/', StickerPackView.as_view(), name='sticker-pack-detail'),
]
