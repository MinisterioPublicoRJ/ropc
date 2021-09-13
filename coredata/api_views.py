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
        # Mock
        mock_bairros_rio = [{"bairro": "Centro", "cod_mun": 1, "municipio": "Rio de Janeiro", "bairro_id": "1"}, {"bairro": "Santa Teresa", "cod_mun": 1, "municipio": "Rio de Janeiro", "bairro_id": "2"}]
        mock_bairros_nit = [{"bairro": "Centro", "cod_mun": 2, "municipio": "Niterói", "bairro_id": "3"}, {"bairro": "Icaraí", "cod_mun": 2, "municipio": "Niterói", "bairro_id": "4"}]
        return mock_bairros_rio if nm_mun == "Rio de Janeiro" else mock_bairros_nit
        #return Bairro.objects.get_ordered_for_municipio(nm_mun)


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
