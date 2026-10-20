from django.contrib import admin
from .models import Genero, Plataforma, Jogo, Avaliacao

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    search_fields = ["nome"]

@admin.register(Plataforma)
class PlataformaAdmin(admin.ModelAdmin):
    search_fields = ["nome"]

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ["nome", "preco", "genero", "destaque", "data_lancamento"]
    list_filter = ["destaque", "genero", "plataformas"]
    search_fields = ["nome"]
    filter_horizontal = ["plataformas"]

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ["nome_visitante", "jogo", "nota", "criada_em"]
    list_filter = ["nota"]
