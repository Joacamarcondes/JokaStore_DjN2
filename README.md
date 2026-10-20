# JokaStore — Catálogo de Jogos Digitais (Django)

Projeto escolar em Django com vitrine pública, página de detalhes, avaliações e dashboard protegido com CRUD.

## Requisitos
- Python 3.10 ou superior
- Pip

## 1. Criar e ativar ambiente virtual

Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
Se estiver usando o Prompt de Comando:
```bat
venv\Scripts\activate
```

## 2. Instalar dependências
```bash
pip install -r requirements.txt
```

## 3. Criar tabelas e administrador
```bash
python manage.py makemigrations catalog
python manage.py migrate
python manage.py createsuperuser
```
Escolha um usuário e senha para o funcionário/administrador.

## 4. Popular com 10 jogos e avaliações
```bash
python manage.py seed_catalog
```
O comando cria 10 jogos reais por nome, gêneros, plataformas, cinco avaliações e capas ilustrativas locais na pasta `media/capas/`. As capas são artes demonstrativas criadas pelo projeto, não capas oficiais dos jogos; se o professor exigir artes oficiais, substitua os PNGs pelas imagens correspondentes mantendo os mesmos nomes de arquivo.

## 5. Executar
```bash
python manage.py runserver
```
- Vitrine: http://127.0.0.1:8000/
- Detalhes: clique em uma capa
- Login/dashboard: http://127.0.0.1:8000/dashboard/
- Admin: http://127.0.0.1:8000/admin/

Use o superusuário criado no passo 3 para entrar no dashboard. O link “Dashboard / Login” também leva ao login.

## O que está implementado
- `Genero`, `Plataforma`, `Jogo`, `Avaliacao` com ForeignKey e ManyToMany.
- Um jogo com `destaque=True` no topo e os demais em grade.
- Detalhes do jogo com gênero, plataformas, descrição e avaliações via `{% for %}`.
- CRUD com ModelForm, protegido por `@login_required`.
- Upload de capas com `request.FILES` e `enctype="multipart/form-data"`.
- CSS responsivo inspirado na referência escura com verde neon.
- Configuração de `MEDIA_URL`/`MEDIA_ROOT`; mídia servida em desenvolvimento.

## Antes de entregar
1. Rode os comandos acima.
2. Confirme que o site abre e que as capas aparecem.
3. Faça login e teste adicionar, editar e apagar um jogo.
4. Confira `/admin/` e cadastre/ajuste os dados se necessário.
5. Entregue o projeto compactado incluindo `db.sqlite3` e `media/`, mas **não** inclua `venv/` nem `__pycache__/`.

> O banco `db.sqlite3` é gerado quando você executa `migrate`. O diretório `media/` é preenchido pelo comando `seed_catalog`.
