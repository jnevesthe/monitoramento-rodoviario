from django.contrib import admin
from .models import Proprietario, Veiculo, Multa
#Josemar Neves

@admin.register(Proprietario)
class ProprietarioAdmin(admin.ModelAdmin):
    search_fields = ["nome_completo", "cidade"]  # o que será buscado no autocomplete

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    autocomplete_fields = ["proprietario"]  # campo proprietário terá rolagem + busca
    search_fields = ["marca", "modelo", "matricula"]

@admin.register(Multa)
class MultaAdmin(admin.ModelAdmin):
    #Josemar Neves
    autocomplete_fields = ["veiculo"]
    search_fields = ["localizacao"]






























#Josemar Neves
































#Josemar Neves
