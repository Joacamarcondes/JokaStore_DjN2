from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import JogoForm
from .models import Jogo

def home(request):
    destaque = Jogo.objects.filter(destaque=True).order_by("id").first()
    jogos = Jogo.objects.all().prefetch_related("plataformas")
    if destaque:
        jogos = jogos.exclude(pk=destaque.pk)
    return render(request, "catalog/home.html", {"destaque": destaque, "jogos": jogos})

def detalhe_jogo(request, pk):
    jogo = get_object_or_404(Jogo.objects.select_related("genero").prefetch_related("plataformas", "avaliacoes"), pk=pk)
    return render(request, "catalog/detalhe.html", {"jogo": jogo})

@login_required
def dashboard(request):
    jogos = Jogo.objects.select_related("genero").all()
    return render(request, "catalog/dashboard.html", {"jogos": jogos})

@login_required
def adicionar_jogo(request):
    if request.method == "POST":
        form = JogoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Jogo adicionado com sucesso.")
            return redirect("dashboard")
    else:
        form = JogoForm()
    return render(request, "catalog/form_jogo.html", {"form": form, "titulo": "Adicionar jogo"})

@login_required
def editar_jogo(request, pk):
    jogo = get_object_or_404(Jogo, pk=pk)
    if request.method == "POST":
        form = JogoForm(request.POST, request.FILES, instance=jogo)
        if form.is_valid():
            form.save()
            messages.success(request, "Jogo atualizado com sucesso.")
            return redirect("dashboard")
    else:
        form = JogoForm(instance=jogo)
    return render(request, "catalog/form_jogo.html", {"form": form, "titulo": "Editar jogo"})

@login_required
def apagar_jogo(request, pk):
    jogo = get_object_or_404(Jogo, pk=pk)
    if request.method == "POST":
        jogo.delete()
        messages.success(request, "Jogo apagado.")
        return redirect("dashboard")
    return render(request, "catalog/confirmar_apagar.html", {"jogo": jogo})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    erro = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect(request.GET.get("next") or "dashboard")
        erro = "Usuário ou senha incorretos."
    return render(request, "registration/login.html", {"erro": erro})

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("home")
