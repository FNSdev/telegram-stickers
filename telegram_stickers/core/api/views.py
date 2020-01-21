from rest_framework import generics

from core.api.filters import StickerPackFilter
from core.api.serializers import StickerPackSerializer
from core.models import StickerPack


class StickerPackListView(generics.ListAPIView):
    queryset = StickerPack.objects.all()
    serializer_class = StickerPackSerializer
    filterset_class = StickerPackFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('order_by'):
            queryset = queryset.order_by(self.request.query_params['order_by'])

        return queryset


class StickerPackView(generics.RetrieveAPIView):
    queryset = StickerPack.objects.all()
    serializer_class = StickerPackSerializer
