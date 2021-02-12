from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from operations.models import (
    InformacaoGeralOperacao,
    InformacaoOperacionalOperacao,
    Operacao,
)
from operations.serializers import (
    InformacaoGeralOperacaoSerializer,
    InformacaoOperacionalOperacaoSerializer,
)


class CreateGeneralInfo(APIView):
    permission_classes = [IsAuthenticated]

    def create_object(self, user, id_):
        obj, _ = Operacao.objects.get_or_create(identificador=id_, usuario=user)
        return obj

    def post(self, request, *args, **kwargs):
        form_uuid = kwargs.get("form_uuid")
        operacao = self.create_object(self.request.user, form_uuid)
        ser = InformacaoGeralOperacaoSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(operacao=operacao)
        return Response()

    def get(self, request, *args, **kwargs):
        form_uuid = kwargs.get("form_uuid")
        info_op = get_object_or_404(
            InformacaoGeralOperacao,
            operacao__identificador=form_uuid
        )
        ser = InformacaoGeralOperacaoSerializer(info_op)
        return Response(data=ser.data)


class CreateOperationalInfo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        form_uuid = kwargs.get("form_uuid")
        operacao = Operacao.objects.get(identificador=form_uuid)
        ser = InformacaoOperacionalOperacaoSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(operacao=operacao)
        return Response()

    def get(self, request, *args, **kwargs):
        form_uuid = kwargs.get("form_uuid")
        info_op = get_object_or_404(
            InformacaoOperacionalOperacao,
            operacao__identificador=form_uuid
        )
        ser = InformacaoOperacionalOperacaoSerializer(info_op)
        return Response(data=ser.data)
