from PIL import Image, ImageDraw, ImageOps
import os

source = "assets/super.png"
base = "android/app/src/main/res"

tailles = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192
}

foreground = {
    "mipmap-mdpi": 108,
    "mipmap-hdpi": 162,
    "mipmap-xhdpi": 216,
    "mipmap-xxhdpi": 324,
    "mipmap-xxxhdpi": 432
}

original = Image.open(source).convert("RGBA")

def creer_image(taille, adaptative=False):
    image = ImageOps.fit(
        original,
        (taille, taille),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5)
    )
    if adaptative:
        fond = Image.new("RGBA", (taille, taille), (255, 255, 255, 0))
        logo = ImageOps.contain(
            original,
            (int(taille * 0.66), int(taille * 0.66)),
            method=Image.Resampling.LANCZOS
        )
        fond.alpha_composite(
            logo,
            ((taille - logo.width)//2, (taille - logo.height)//2)
        )
        return fond
    return image

for densite, taille in tailles.items():
    dossier = os.path.join(base, densite)
    os.makedirs(dossier, exist_ok=True)

    icone = creer_image(taille)
    icone.save(os.path.join(dossier, "ic_launcher.png"))

    masque = Image.new("L", (taille, taille), 0)
    ImageDraw.Draw(masque).ellipse(
        (0, 0, taille - 1, taille - 1), fill=255
    )
    ronde = icone.copy()
    ronde.putalpha(masque)
    ronde.save(os.path.join(dossier, "ic_launcher_round.png"))

    avant = creer_image(foreground[densite], True)
    avant.save(os.path.join(dossier, "ic_launcher_foreground.png"))

print("SUCCES : icones SADIOLA SUGU creees !")
