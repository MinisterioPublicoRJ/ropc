from django.contrib import admin


class CustomOperacaoAdmin(admin.ModelAdmin):
    exclude = ("secao_atual", "coordenadas_geo",)
    list_display = (
        "batalhao_responsavel",
        "data",
        "municipio",
        "bairro",
        "localidade",
        "tipo_operacao",
        "criado_em",
    )
    ordering = ("-criado_em", "-data",)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
