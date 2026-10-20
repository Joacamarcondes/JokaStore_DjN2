from django import forms
from .models import Jogo

class JogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        fields = ["nome", "preco", "data_lancamento", "capa", "destaque", "genero", "plataformas", "descricao"]
        widgets = {
            "data_lancamento": forms.DateInput(attrs={"type": "date"}),
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }
