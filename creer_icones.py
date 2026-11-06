from PIL import Image, ImageDraw
import os

source = Image.open("assets/sugu.jpeg").convert("RGB")

tailles = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192
}

foreground = {
    "mdpi": 108,
    "hdpi": 162,
    "xhdpi": 216,
    "xxhdpi": 324,
    "xxxhdpi": 432
}

def creer_image(taille, transparent=False):
    fond = Image.new(
        "RGBA",
        (taille, taille),
        (0, 0, 0, 0) if transparent else (247, 246, 243, 255)
    )

    largeur = int(taille * 0.90)
    hauteur = int(largeur * source.height / source.width)

    logo = source.resize((largeur, hauteur), Image.Resampling.LANCZOS)
    x = (taille - largeur) // 2
    y = (taille - hauteur) // 2

    fond.alpha_composite(logo.convert("RGBA"), (x, y))
    return fond

base = "android/app/src/main/res"

for densite, taille in tailles.items():
    dossier = f"{base}/mipmap-{densite}"
    os.makedirs(dossier, exist_ok=True)

    icone = creer_image(taille)

    icone.convert("RGB").save(
        f"{dossier}/ic_launcher.png"
    )

    masque = Image.new("L", (taille, taille), 0)
    ImageDraw.Draw(masque).ellipse(
        (0, 0, taille - 1, taille - 1), fill=255
    )

    ronde = icone.copy()
    ronde.putalpha(masque)
    ronde.save(f"{dossier}/ic_launcher_round.png")

    taille_fg = foreground[densite]
    avant = creer_image(taille_fg, True)
    avant.save(f"{dossier}/ic_launcher_foreground.png")

print("SUCCES : toutes les icones ont ete creees !")
