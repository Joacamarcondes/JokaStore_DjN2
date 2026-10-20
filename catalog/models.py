from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Genero(models.Model):
    nome = models.CharField(max_length=60, unique=True)
    def __str__(self):
        return self.nome
    class Meta:
        ordering = ["nome"]
        verbose_name = "Gênero"
        verbose_name_plural = "Gêneros"

class Plataforma(models.Model):
    nome = models.CharField(max_length=60, unique=True)
    def __str__(self):
        return self.nome
    class Meta:
        ordering = ["nome"]
        verbose_name = "Plataforma"
        verbose_name_plural = "Plataformas"

class Jogo(models.Model):
    nome = models.CharField(max_length=120)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    data_lancamento = models.DateField()
    capa = models.ImageField(upload_to="capas/")
    destaque = models.BooleanField(default=False)
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT, related_name="jogos")
    plataformas = models.ManyToManyField(Plataforma, related_name="jogos")
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nome
    class Meta:
        ordering = ["nome"]
        verbose_name = "Jogo"
        verbose_name_plural = "Jogos"

class Avaliacao(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, related_name="avaliacoes")
    nome_visitante = models.CharField(max_length=100)
    nota = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField()
    criada_em = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.nome_visitante} — {self.jogo.nome} ({self.nota}/5)"
    class Meta:
        ordering = ["-criada_em"]
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
