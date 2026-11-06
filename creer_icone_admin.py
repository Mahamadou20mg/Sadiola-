from PIL import Image, ImageOps, ImageDraw
from pathlib import Path

source = Image.open("assets/super.png").convert("RGBA")

tailles = {
    "mdpi": 1,
    "hdpi": 1.5,
    "xhdpi": 2,
    "xxhdpi": 3,
    "xxxhdpi": 4
}

for densite, facteur in tailles.items():
    dossier = Path(f"android/app/src/main/res/mipmap-{densite}")
    dossier.mkdir(parents=True, exist_ok=True)

    # Icône classique
    taille = int(48 * facteur)
    icone = ImageOps.fit(source, (taille, taille), method=Image.Resampling.LANCZOS)
    icone.save(dossier / "ic_launcher.png")

    # Icône ronde
    ronde = icone.copy()
    masque = Image.new("L", (taille, taille), 0)
    dessin = ImageDraw.Draw(masque)
    dessin.ellipse((0, 0, taille-1, taille-1), fill=255)
    ronde.putalpha(masque)
    ronde.save(dossier / "ic_launcher_round.png")

    # Image de premier plan pour icône adaptative
    taille_adaptative = int(108 * facteur)
    zone = int(72 * facteur)
    premier_plan = Image.new("RGBA", (taille_adaptative, taille_adaptative), (0, 0, 0, 0))
    logo = ImageOps.contain(source, (zone, zone), method=Image.Resampling.LANCZOS)
    x = (taille_adaptative - logo.width) // 2
    y = (taille_adaptative - logo.height) // 2
    premier_plan.alpha_composite(logo, (x, y))
    premier_plan.save(dossier / "ic_launcher_foreground.png")

print("SUCCÈS : icônes SUGU ADMIN créées dans toutes les tailles Android.")
