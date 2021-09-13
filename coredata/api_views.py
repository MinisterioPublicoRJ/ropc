from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from coredata.models import (
    Bairro,
    Batalhao,
    Delegacia,
    Municipio,
)
from coredata.serializers import (
    BairroSerializer,
    BatalhaoSerializer,
    DelegaciaSerializer,
    MunicipioSerializer
)


class MunicipiosView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Municipio.objects.all().order_by("nm_mun")
    serializer_class = MunicipioSerializer


class BairrosView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BairroSerializer
    lookup_url_kwarg = "nm_mun"

    def get_queryset(self):
        nm_mun = self.kwargs.get(self.lookup_url_kwarg)
        return Bairro.objects.get_ordered_for_municipio(nm_mun)


class BatalhaoView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BatalhaoSerializer
    lookup_url_kwarg = "nm_mun"

    def get_queryset(self):
        nm_mun = self.kwargs.get(self.lookup_url_kwarg)
        return Batalhao.objects.get_ordered_for_municipio(nm_mun)


class DelegaciaView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DelegaciaSerializer
    lookup_url_kwarg = "cod_mun"

    def get_queryset(self):
        cod_mun = self.kwargs.get(self.lookup_url_kwarg)
        return Delegacia.objects.filter(
            cod_mun__cod_6_dig=cod_mun
        ).order_by("nome").distinct("nome")
