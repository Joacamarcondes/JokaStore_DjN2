from datetime import date
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from catalog.models import Genero, Plataforma, Jogo, Avaliacao

GAMES = [
    ("Cyberpunk 2077", 199.90, "RPG", date(2020,12,10), "Uma aventura futurista de mundo aberto na cidade de Night City."),
    ("Elden Ring", 249.90, "RPG", date(2022,2,25), "Explore um vasto mundo de fantasia, enfrente chefes e descubra segredos."),
    ("The Witcher 3", 129.90, "RPG", date(2015,5,19), "Acompanhe Geralt em uma jornada épica por um mundo repleto de escolhas."),
    ("Hollow Knight", 46.99, "Aventura", date(2017,2,24), "Explore um reino subterrâneo desenhado à mão e encare desafios precisos."),
    ("God of War", 199.90, "Ação", date(2018,4,20), "Kratos e Atreus embarcam em uma jornada pela mitologia nórdica."),
    ("Stardew Valley", 24.99, "Simulação", date(2016,2,26), "Construa sua fazenda, conheça moradores e descubra os segredos do vale."),
    ("EA Sports FC 25", 299.90, "Esportes", date(2024,9,27), "Monte seu time e dispute partidas de futebol."),
    ("Red Dead Redemption 2", 249.90, "Ação", date(2018,10,26), "Uma aventura de faroeste em um mundo aberto detalhado."),
    ("Minecraft", 99.00, "Sandbox", date(2011,11,18), "Construa, explore e sobreviva em mundos feitos de blocos."),
    ("Forza Horizon 5", 249.90, "Corrida", date(2021,11,9), "Corra por paisagens vibrantes inspiradas no México."),
]
PLATFORMS = ["PC", "PlayStation 5", "Xbox Series X|S", "Nintendo Switch"]
REVIEWS = [
    ("Ana", 5, "Muito divertido e com um mundo incrível."),
    ("Lucas", 4, "Ótimo jogo, recomendo bastante."),
    ("Marina", 5, "Vale muito a pena jogar."),
    ("Pedro", 4, "Boa experiência e ótima trilha sonora."),
    ("Rafa", 5, "Um dos meus favoritos!"),
]
COLORS = [(27,180,110),(111,73,180),(210,85,65),(36,135,165),(185,125,38),(91,150,75),(183,55,105),(160,95,50),(50,120,180),(40,155,140)]

class Command(BaseCommand):
    help = "Cria gêneros, plataformas, 10 jogos com capas ilustrativas e avaliações de exemplo."
    def handle(self, *args, **options):
        platform_objs = [Plataforma.objects.get_or_create(nome=p)[0] for p in PLATFORMS]
        genres = {}
        for _, _, genre, _, _ in GAMES:
            genres[genre] = Genero.objects.get_or_create(nome=genre)[0]
        for index, (name, price, genre, release, description) in enumerate(GAMES):
            jogo, created = Jogo.objects.get_or_create(
                nome=name,
                defaults={"preco": price, "data_lancamento": release, "destaque": index == 0,
                          "genero": genres[genre], "descricao": description}
            )
            if created or not jogo.capa:
                image = Image.new("RGB", (640, 360), COLORS[index])
                draw = ImageDraw.Draw(image)
                draw.rectangle((18,18,622,342), outline=(235,245,240), width=3)
                draw.text((40, 45), "JOKASTORE", fill=(235,245,240))
                # Text wrapping without depending on a particular installed font.
                words, lines, current = name.split(), [], ""
                for word in words:
                    candidate = (current + " " + word).strip()
                    if len(candidate) > 20:
                        lines.append(current); current = word
                    else:
                        current = candidate
                if current: lines.append(current)
                y = 135
                for line in lines:
                    draw.text((40, y), line, fill=(255,255,255), stroke_width=1)
                    y += 34
                draw.text((40, 300), f"{genre}  |  R$ {price:.2f}".replace(".", ","), fill=(220,255,230))
                output = BytesIO()
                image.save(output, format="PNG")
                jogo.capa.save(f"{index+1:02d}-{name.lower().replace(' ', '-')}.png", ContentFile(output.getvalue()), save=True)
            jogo.plataformas.set(platform_objs if index % 2 == 0 else platform_objs[:3])
            if index == 0 and not jogo.destaque:
                jogo.destaque = True
                jogo.save(update_fields=["destaque"])
        first_games = list(Jogo.objects.order_by("id")[:5])
        for index, (visitor, rating, comment) in enumerate(REVIEWS):
            Avaliacao.objects.get_or_create(jogo=first_games[index % len(first_games)], nome_visitante=visitor,
                                            nota=rating, comentario=comment)
        self.stdout.write(self.style.SUCCESS("Catálogo criado! Confira os jogos em / e o admin em /admin/."))
