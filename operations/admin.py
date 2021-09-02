from django.contrib import admin

from operations.models import Operacao


class CustomOperacaoAdmin(admin.ModelAdmin):
    exclude = ("secao_atual", "coordenadas_geo",)
    list_display = (
        "data",
        "hora_inicio",
        "hora_termino",
        #"municipio",
        #"bairro",
        #"localidade_operacao",
        "tipo_operacao",
        "criado_em",
    )
    ordering = ("-criado_em", "-data",)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Operacao, CustomOperacaoAdmin)
