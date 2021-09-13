from rest_framework import serializers

from coredata.models import (
    Bairro,
    Batalhao,
    Delegacia,
    Municipio,
)


class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = "__all__"


class BairroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bairro
        # Mock
        fields = ["municipio", "bairro"]
        # fields = "__all__"


class BatalhaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batalhao
        fields = "__all__"


class DelegaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delegacia
        fields = "__all__"
