"""
anlyse.py  —  Interpolation Polynomiale
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERSION 2 — Sections pédagogiques ajoutées :
  - _comprendre_fx_px()   : f(x) vs P(x) avec analogie température
  - _comprendre_x()       : qu'est-ce que x ? avec analogie voiture
  - _comprendre_courbe_unique() : pourquoi une seule courbe ?
  Ces sections s'insèrent AVANT _lagrange() et _newton()
  pour construire l'intuition progressive.

manim -p -qh anlyse.py IP
"""
from manim import *
from gtts import gTTS
import os, numpy as np, asyncio

def _gen_audio(path, txt):
    if os.path.exists(path): return
    try:
        import edge_tts
        async def _run():
            c = edge_tts.Communicate(txt, voice="fr-FR-HenriNeural", rate="+5%")
            await c.save(path)
        asyncio.run(_run())
        print(f"  ✓ {os.path.basename(path)} [Edge-TTS]")
    except Exception:
        gTTS(text=txt, lang="fr").save(path)
        print(f"  ✓ {os.path.basename(path)} [gTTS]")

DIR = "audio_ip"
os.makedirs(DIR, exist_ok=True)

TEXTS = {
# ── TEXTES EXISTANTS ────────────────────────────────────────────────────────
"i1":  "Bienvenue dans ce cours d'analyse numérique.",
"i2":  "Aujourd'hui on va comprendre l'interpolation polynomiale, une méthode pour reconstruire une courbe à partir de quelques points de mesure.",
"p1":  "Voici le problème de départ.",
"p2":  "On dispose de points mesurés sur le plan.",
"p3":  "On veut trouver un polynôme qui passe exactement par tous ces points.",
"p4":  "Ce polynôme jouera le rôle de la fonction inconnue entre les mesures.",
"u1":  "Ce polynôme est-il unique ? Bonne question.",
"u2":  "Avec un seul point, une infinité de courbes sont possibles.",
"u3":  "Avec deux points distincts, une seule droite les relie.",
"u4":  "Avec trois points, une seule parabole les traverse.",
"u5":  "En général, n plus un points distincts donnent un unique polynôme de degré au plus n.",
"u6":  "C'est le théorème fondamental de l'interpolation.",
"l1":  "Passons à la méthode de Lagrange.",
"l2":  "On construit des polynômes de base, appelés L i.",
"l3":  "Voici L zéro en orange : il vaut un en x zéro, et zéro partout ailleurs.",
"l4":  "Voici L un en bleu : il vaut un en x un, et zéro partout ailleurs.",
"l5":  "Voici L deux en violet : même principe, un en x deux, zéro ailleurs.",
"l6":  "Cette propriété s'appelle la propriété de Kronecker.",
"l7":  "Zoomons sur ce point : L zéro vaut exactement un ici.",
"l8":  "Le polynôme final est la combinaison linéaire de ces bases, pondérée par les y i.",
"l9":  "Voilà la formule de Lagrange. Retenez bien cette structure.",
"l10": "Et voici comment se calcule chaque polynôme de base L i explicitement.",
"l11": "Passons maintenant à la méthode de Newton.",
"n1":  "La méthode de Newton. Son avantage principal : si on ajoute un nouveau point, on ajoute simplement un nouveau terme au polynôme. Pas besoin de tout recalculer.",
"n4":  "Remplissons maintenant la table des différences divisées.",
"n5":  "On remplit la table colonne par colonne. Chaque valeur se calcule à partir de la colonne précédente.",
"n7":  "Cette flèche montre le calcul de bêta un, première différence divisée.",
"n8":  "Et cette flèche montre bêta deux, différence divisée de second ordre.",
"n9":  "Regardons de plus près ce coefficient bêta deux.",
"n10": "Passons maintenant à la formule du polynôme de Newton.",
"n11": "Voilà le polynôme de Newton. Chaque bêta k est la différence divisée d'ordre k.",
"n12": "Zoomons sur cette formule pour bien la retenir.",
"e1":  "Maintenant, parlons de l'erreur d'interpolation.",
"e2":  "Voici la vraie fonction f, en bleu.",
"e3":  "Et voici notre polynôme d'interpolation P n, en orange.",
"e4":  "On voit clairement l'écart entre les deux courbes. C'est l'erreur d'interpolation.",
"e6":  "Regardons sa valeur numérique ici.",
"e7":  "Effaçons le graphique et regardons maintenant la formule de majoration.",
"e8":  "On peut majorer l'erreur avec cette formule. M n plus un est le maximum de la dérivée.",
"e9":  "Zoomons sur cette formule importante.",
"e10": "Et voici la définition de M n plus un.",
"e11": "Attention au phénomène de Runge.",
"e12": "Trop de points mal placés créent de grandes oscillations du polynôme.",
"x1":  "Appliquons tout cela à un exemple concret.",
"x2":  "On prend f de x égal cosinus de pi sur quatre fois x.",
"x3":  "Premier point de mesure : M zéro en x égal zéro.",
"x4":  "Deuxième point M un, et troisième point M deux.",
"x5":  "Remplissons la table de Newton pour ces trois points.",
"x6":  "Voici les valeurs de y i dans la première colonne.",
"x7":  "Voici les premières différences divisées.",
"x8":  "Et voici bêta deux, différence divisée de second ordre.",
"x9":  "Zoomons sur ce coefficient bêta deux.",
"x10": "Passons maintenant au graphique.",
"x11": "Voici les axes et les trois points de mesure.",
"x12": "La courbe bleue est la vraie fonction cosinus.",
"x13": "La courbe orange est notre polynôme P deux.",
"x14": "Mesurons l'erreur en x égal un demi.",
"x15": "L'erreur est très petite, ce qui confirme la qualité de P deux.",
"x16": "Ajoutons maintenant le quatrième point M trois.",
"x17": "Le polynôme P trois, en vert, colle encore mieux à la courbe réelle.",
"c1":  "En résumé, retenons les trois points essentiels de ce cours.",
"c2":  "Lagrange : formule directe avec les polynômes de base L i.",
"c3":  "Newton : différences divisées, ajout facile de nouveaux points.",
"c4":  "Erreur : la formule de majoration garantit la qualité de l'approximation.",
"c5":  "Voilà la formule clé de Lagrange. Retenez-la bien.",
"c6":  "Bonne révision !",
"es1": "Regardons maintenant la somme, notée sigma. C'est très simple.",
"es2": "Imaginez vos factures de gaz : janvier cent euros, février cent vingt, mars quatre-vingt.",
"es3": "La somme totale fait cinq cent quarante euros. Vous venez de calculer un sigma !",
"es4": "En interpolation, sigma fait la même chose : il additionne la contribution de chaque point de mesure pour construire le polynôme.",
"eb1": "Maintenant, qu'est-ce que bêta ? Imaginez qu'on construit un bâtiment étage par étage.",
"eb2": "bêta zéro, c'est le rez-de-chaussée. La valeur au premier point. On commence de là.",
"eb3": "bêta un, c'est le premier étage. Il corrige la pente : est-ce que la courbe monte ou descend entre les deux premiers points ?",
"eb4": "bêta deux, c'est le deuxième étage. Il corrige la courbure : comment la courbe tourne-t-elle ?",
"eb5": "Chaque bêta qu'on ajoute améliore la précision. Plus d'étages, meilleure est l'approximation.",
"el1": "Qu'est-ce que L i ? Imaginez une salle de théâtre avec des spots lumineux.",
"el2": "Chaque spot éclaire une seule chaise. Le spot numéro un allume uniquement la chaise numéro un.",
"el3": "L i vaut exactement un en son propre point x i, et zéro en tous les autres points.",
"el4": "Grâce à cette propriété, chaque L i contrôle uniquement sa propre mesure. C'est ça la clé de Lagrange.",
"ed1": "Maintenant, les différences divisées. Prenons un exemple avec une voiture.",
"ed2": "À midi, la voiture est à cent kilomètres. À treize heures, elle est à cent soixante kilomètres.",
"ed3": "Cent soixante moins cent, divisé par une heure : soixante kilomètres par heure. C'est la vitesse moyenne !",
"ed4": "Voilà ! La différence divisée, c'est la variation entre deux valeurs divisée par la distance. Exactement comme une vitesse. C'est bêta un.",
"ec1": "Comment le polynôme passe-t-il exactement par chaque point ? Regardons cela ensemble.",
"ec2": "Voici nos points de mesure. La courbe se dessine et passe exactement par le premier point.",
"ec3": "Maintenant elle passe par tous les points. Chaque bêta a poussé la courbe vers le point suivant.",
"ec4": "Comme une couturière qui ajuste le tissu point par point, le polynôme s'adapte à chaque mesure. C'est la magie de l'interpolation.",
"tr_lag": "Maintenant que vous comprenez sigma et L i, voici la méthode de Lagrange complète.",
"tr_newt": "Maintenant que vous comprenez bêta et les différences divisées, voici la méthode de Newton.",
"tr_pass": "Voyons maintenant un exemple concret pour vérifier que le polynôme passe bien par tous les points.",
"cmp1": "Faisons une comparaison directe entre les deux méthodes.",
"cmp2": "Lagrange est explicite mais coûteux si on ajoute un point.",
"cmp3": "Newton est incrémental : ajouter un point coûte un seul terme.",
"cmp4": "Les deux méthodes donnent exactement le même polynôme final.",
"faq0": "Voici les questions les plus fréquentes sur l'interpolation.",
"faq1": "Question un : peut-on interpoler avec des points non distincts ?",
"faq1r": "Non. Deux points avec le même x rendent le polynôme indéfini. Les points doivent être tous distincts.",
"faq2": "Question deux : plus de points donne-t-il toujours un meilleur résultat ?",
"faq2r": "Pas forcément. Le phénomène de Runge montre que trop de points mal répartis créent des oscillations.",
"faq3": "Question trois : quelle méthode choisir en pratique ?",
"faq3r": "Newton si vous ajoutez des points progressivement. Lagrange pour une formule explicite directe.",

# ── NOUVEAUX TEXTES PÉDAGOGIQUES ─────────────────────────────────────────────
# Section : f(x) vs P(x)
"fp1": "Voici la question centrale : quelle est la différence entre f de x et P de x ?",
"fp2": "f de x, c'est la réalité. La nature la connaît, vous non. Vous n'avez que trois mesures.",
"fp3": "Voici vos trois mesures : à zéro heure, dix degrés. À douze heures, vingt-cinq degrés. À vingt-quatre heures, quinze degrés.",
"fp4": "P de x, c'est la courbe que vous construisez vous-même pour approcher f.",
"fp5": "P passe exactement par vos trois points. Entre ces points, P estime f. C'est là qu'apparaît l'erreur.",
"fp6": "Retenez bien : f est l'inconnu. P est votre approximation. L'interpolation, c'est construire P à partir de quelques valeurs de f.",

# Section : qu'est-ce que x ?
"qx1": "Maintenant, qu'est-ce que x ? C'est simplement un nombre que vous choisissez.",
"qx2": "Imaginez P de x comme une machine à calculer. Vous entrez un nombre, elle vous sort la température estimée.",
"qx3": "x zéro, x un, x deux sont les heures où vous avez mesuré. Ce sont des constantes connues.",
"qx4": "Quand on écrit x moins x zéro, on calcule simplement l'écart entre l'heure choisie et la première mesure.",
"qx5": "Par exemple, si x vaut six heures et x zéro vaut zéro, alors x moins x zéro vaut six. C'est la distance en heures depuis le premier point.",
"qx6": "Et x moins x zéro fois x moins x un, c'est cette distance multipliée par la distance au deuxième point. Ce produit vaut zéro dès qu'on est sur un point connu.",

# Section : pourquoi une seule courbe ?
"cu1": "Pourquoi choisit-on le polynôme de degré le plus bas ?",
"cu2": "Avec trois points, une infinité de courbes passent par eux. Chaque personne en tracerait une différente.",
"cu3": "Le polynôme de degré deux, la parabole, est le seul de ce type qui passe par exactement trois points donnés.",
"cu4": "C'est une propriété mathématique : trois points distincts déterminent une unique parabole. Pas deux, pas trois. Une seule.",
"cu5": "Voilà pourquoi tout le monde obtient la même réponse. La règle élimine l'ambiguité.",

# Section : intuition bêta avec voiture
"bv1": "Reprenons bêta avec un exemple très concret : une voiture sur la route.",
"bv2": "bêta zéro, c'est la position au départ. La voiture est au kilomètre vingt.",
"bv3": "bêta un, c'est la vitesse. Elle roule à soixante kilomètres par heure. Elle avance.",
"bv4": "bêta deux, c'est l'accélération. Elle appuie sur le frein ou l'accélérateur. La vitesse change.",
"bv5": "Chaque bêta ajoute une correction de plus. Sans bêta deux, on suppose que la voiture roule à vitesse constante. Avec bêta deux, on modélise le changement de vitesse.",
"bv6": "C'est exactement la même logique pour le polynôme de Newton. Chaque bêta affine l'approximation.",
}

for key, txt in TEXTS.items():
    _gen_audio(os.path.join(DIR, key + ".mp3"), txt)

def AP(k): return os.path.join(DIR, k + ".mp3")

DURATIONS = {
"i1":2.7,  "i2":8.0,
"p1":2.3,  "p2":3.5,  "p3":5.0,  "p4":5.0,
"u1":3.0,  "u2":4.2,  "u3":3.8,  "u4":3.5,  "u5":6.8,  "u6":2.7,
"l1":2.7,  "l2":3.8,  "l3":6.8,  "l4":6.8,  "l5":6.0,
"l6":3.0,  "l7":4.7,  "l8":6.3,  "l9":3.8,  "l10":5.0, "l11":3.0,
"n1":11.0, "n4":3.0,  "n5":7.0,
"n7":4.7,  "n8":4.7,  "n9":3.5,  "n10":3.8, "n11":6.0, "n12":3.5,
"e1":2.3,  "e2":3.0,  "e3":3.8,  "e4":4.7,
"e6":2.3,  "e7":4.2,  "e8":7.0,  "e9":2.3,  "e10":3.8,
"e11":2.3, "e12":4.7,
"x1":3.0,  "x2":5.5,  "x3":4.7,  "x4":3.8,  "x5":3.8,  "x6":4.2,
"x7":2.7,  "x8":3.8,  "x9":2.7,  "x10":1.8,
"x11":3.8, "x12":3.5, "x13":3.5, "x14":3.0, "x15":5.0, "x16":3.0, "x17":5.5,
"c1":4.2,  "c2":4.7,  "c3":3.8,  "c4":4.7,  "c5":3.5,  "c6":1.4,
"cmp1":3.5,"cmp2":4.2,"cmp3":4.7,"cmp4":3.8,
"tr_lag":6.0,"tr_newt":6.0,"tr_pass":6.8,
"faq0":3.5,"faq1":4.7,"faq1r":7.0,"faq2":5.0,"faq2r":6.8,"faq3":3.8,"faq3r":5.5,
"es1":3.8,"es2":6.0,"es3":6.3,"es4":8.8,
"eb1":5.5,"eb2":6.0,"eb3":10.0,"eb4":6.8,"eb5":5.8,
"el1":6.0,"el2":6.8,"el3":7.5,"el4":7.5,
"ed1":4.2,"ed2":7.0,"ed3":7.5,"ed4":9.2,
"ec1":5.0,"ec2":6.8,"ec3":7.0,"ec4":8.8,
# Nouvelles durées
"fp1":4.5,"fp2":5.5,"fp3":7.0,"fp4":4.5,"fp5":6.5,"fp6":7.5,
"qx1":4.0,"qx2":5.5,"qx3":5.5,"qx4":5.5,"qx5":7.0,"qx6":8.0,
"cu1":3.5,"cu2":5.5,"cu3":6.0,"cu4":7.5,"cu5":5.0,
"bv1":4.5,"bv2":4.5,"bv3":4.5,"bv4":4.5,"bv5":8.0,"bv6":5.5,
}

def DUR(k): return DURATIONS.get(k, 3.0)

# PALETTE
BG="#0D1117"; C_WHT="#FFFDE7"; C_YEL="#FFD54F"; C_BLU="#64B5F6"
C_GRN="#81C784"; C_RED="#EF9A9A"; C_PUR="#CE93D8"; C_TEA="#80CBC4"
C_ORG="#FFAB76"; C_GRY="#546E7A"; C_DIM="#1E2A3A"

def pulse_formula(scene, mob, col=C_YEL, n=2):
    box  = SurroundingRectangle(mob, color=col, stroke_width=2.5, buff=0.18, corner_radius=0.10)
    glow = SurroundingRectangle(mob, color=col, stroke_width=7.0, buff=0.23, corner_radius=0.14, stroke_opacity=0.0)
    scene.add(box, glow)
    for _ in range(n):
        scene.play(glow.animate(run_time=0.22).set_stroke(opacity=0.50, width=9),
                   box.animate(run_time=0.22).set_stroke(width=4.5))
        scene.play(glow.animate(run_time=0.22).set_stroke(opacity=0.0, width=7),
                   box.animate(run_time=0.22).set_stroke(width=2.5))
    scene.remove(box, glow)

class Alien(VGroup):
    S=0.48
    def __init__(self,**kw):
        super().__init__(**kw); S=self.S
        body=RoundedRectangle(width=1.3*S,height=1.4*S,corner_radius=0.3*S,fill_color="#00c853",fill_opacity=1,stroke_color="#00e676",stroke_width=1.8)
        head=RoundedRectangle(width=1.5*S,height=1.3*S,corner_radius=0.28*S,fill_color="#69f0ae",fill_opacity=1,stroke_color="#00e676",stroke_width=1.8)
        head.next_to(body,UP,buff=0.04*S)
        al=Line(head.get_top()+LEFT*0.28*S,head.get_top()+LEFT*0.42*S+UP*0.38*S,stroke_color="#b2ff59",stroke_width=2.5*S)
        ar=Line(head.get_top()+RIGHT*0.28*S,head.get_top()+RIGHT*0.42*S+UP*0.38*S,stroke_color="#b2ff59",stroke_width=2.5*S)
        bl=Dot(al.get_end(),radius=0.07*S,color="#ffeb3b"); br=Dot(ar.get_end(),radius=0.07*S,color="#ffeb3b")
        ewl=Circle(radius=0.21*S,fill_color=WHITE,fill_opacity=1,stroke_width=0)
        ewr=Circle(radius=0.21*S,fill_color=WHITE,fill_opacity=1,stroke_width=0)
        ewl.move_to(head.get_center()+np.array([-0.27*S,0.10*S,0]))
        ewr.move_to(head.get_center()+np.array([0.27*S,0.10*S,0]))
        pul=Circle(radius=0.10*S,fill_color="#1a237e",fill_opacity=1,stroke_width=0)
        pur=Circle(radius=0.10*S,fill_color="#1a237e",fill_opacity=1,stroke_width=0)
        pul.move_to(ewl.get_center()+np.array([0.03*S,-0.02*S,0]))
        pur.move_to(ewr.get_center()+np.array([0.03*S,-0.02*S,0]))
        shl=Dot(pul.get_center()+np.array([0.03*S,0.03*S,0]),radius=0.03*S,color=WHITE)
        shr=Dot(pur.get_center()+np.array([0.03*S,0.03*S,0]),radius=0.03*S,color=WHITE)
        bwl=Line(head.get_center()+np.array([-0.42*S,0.32*S,0]),head.get_center()+np.array([-0.12*S,0.37*S,0]),stroke_color="#1b5e20",stroke_width=2.5*S)
        bwr=Line(head.get_center()+np.array([0.12*S,0.37*S,0]),head.get_center()+np.array([0.42*S,0.32*S,0]),stroke_color="#1b5e20",stroke_width=2.5*S)
        mc=head.get_center()+np.array([0,-0.18*S,0])
        mouth=ArcBetweenPoints(mc+LEFT*0.20*S,mc+RIGHT*0.20*S,angle=PI*0.5,stroke_color="#1b5e20",stroke_width=3*S)
        aml=Line(body.get_left()+UP*0.28*S,body.get_left()+np.array([-0.45*S,-0.08*S,0]),stroke_color="#00a040",stroke_width=5*S)
        amr=Line(body.get_right()+UP*0.28*S,body.get_right()+np.array([0.45*S,-0.08*S,0]),stroke_color="#00a040",stroke_width=5*S)
        ll=Line(body.get_bottom()+LEFT*0.20*S,body.get_bottom()+np.array([-0.20*S,-0.50*S,0]),stroke_color="#1b5e20",stroke_width=6*S)
        lr=Line(body.get_bottom()+RIGHT*0.20*S,body.get_bottom()+np.array([0.20*S,-0.50*S,0]),stroke_color="#1b5e20",stroke_width=6*S)
        fl=Ellipse(width=0.32*S,height=0.16*S,fill_color="#1b5e20",fill_opacity=1,stroke_width=0)
        fr=Ellipse(width=0.32*S,height=0.16*S,fill_color="#1b5e20",fill_opacity=1,stroke_width=0)
        fl.next_to(ll.get_end(),DOWN,buff=0.01); fr.next_to(lr.get_end(),DOWN,buff=0.01)
        self.add(fl,fr,ll,lr,aml,amr,body,head,al,ar,bl,br,ewl,ewr,pul,pur,shl,shr,bwl,bwr,mouth)

def title_line(txt,col=C_YEL):
    t=Text(txt,font_size=36,color=col,weight=BOLD)
    ul=Line(t.get_left(),t.get_right(),stroke_width=1.5,color=col,stroke_opacity=0.5)
    ul.next_to(t,DOWN,buff=0.07); return VGroup(t,ul)

def hand_axes(xr,yr,xl=8.0,yl=4.8):
    return Axes(x_range=xr,y_range=yr,x_length=xl,y_length=yl,
        axis_config={"color":C_GRY,"stroke_width":1.8,"include_tip":True,"tip_length":0.18})

def hdot(ax,x,y,col=C_ORG):
    return VGroup(Dot(ax.c2p(x,y),radius=0.16,color=col,fill_opacity=0.20).set_z_index(3),
                  Dot(ax.c2p(x,y),radius=0.08,color=col).set_z_index(4))

def lag_fn(pts):
    xs,ys=[p[0] for p in pts],[p[1] for p in pts]
    def P(x):
        v=0.
        for i in range(len(xs)):
            L=1.
            for j in range(len(xs)):
                if j!=i: L*=(x-xs[j])/(xs[i]-xs[j])
            v+=ys[i]*L
        return v
    return P

def hbox(mob,col=C_YEL):
    return VGroup(
        SurroundingRectangle(mob,color=col,stroke_width=3,buff=0.22,corner_radius=0.12,stroke_opacity=0.25),
        SurroundingRectangle(mob,color=col,stroke_width=1.5,buff=0.22,corner_radius=0.12))

def mkrow(*pairs):
    return VGroup(*[MathTex(t,font_size=21,color=c) if t else VMobject()
                    for t,c in pairs]).arrange(RIGHT,buff=0.85)


# ═══════════════════════════════════════════════════
#  SCÈNE
# ═══════════════════════════════════════════════════
class IP(MovingCameraScene):

    def _init_char(self):
        self._ch=Alien(); self._ch.move_to(np.array([5.1,-3.1,0])); self.add(self._ch)

    def _init_progress(self):
        labels=["Intro","Problème","f vs P","x ?","Unicité","Lagrange","Newton","Erreur","Exemple","Résumé"]
        colors=[C_BLU,C_ORG,C_GRN,C_TEA,C_YEL,C_TEA,C_PUR,C_RED,C_ORG,C_YEL]
        w=13.0; sw=w/len(labels)
        self._pb_segs=VGroup()
        self._pb_colors=colors
        self._pb_labels=labels
        for i in range(len(labels)):
            seg=Rectangle(width=sw-0.05,height=0.16,
                          fill_color=C_GRY,fill_opacity=0.25,stroke_width=0)
            seg.move_to(np.array([-w/2+sw*(i+0.5),-3.88,0]))
            self._pb_segs.add(seg)
        self._pb_lbl=Text("",font_size=11,color=C_GRY)
        self._pb_lbl.move_to(np.array([0,-4.08,0]))
        self.add(self._pb_segs,self._pb_lbl)
        self._pb_idx=-1

    def _set_progress(self, idx):
        self._pb_idx=idx
        col=self._pb_colors[idx]
        for i,seg in enumerate(self._pb_segs):
            if i<idx:    seg.set_fill(color=self._pb_colors[i],opacity=0.45)
            elif i==idx: seg.set_fill(color=col,opacity=1.0)
            else:        seg.set_fill(color=C_GRY,opacity=0.20)
        nl=Text(f"◀ {self._pb_labels[idx]} ▶",font_size=11,color=col)
        nl.move_to(np.array([0,-4.08,0])); self._pb_lbl.become(nl)

    def _section_banner(self, txt, col):
        box=RoundedRectangle(width=7.5,height=0.85,corner_radius=0.18,
                             fill_color=col,fill_opacity=0.13,
                             stroke_color=col,stroke_width=2.0)
        lbl=Text(txt,font_size=30,color=col,weight=BOLD); lbl.move_to(box.get_center())
        b=VGroup(box,lbl); b.move_to(ORIGIN)
        self.play(FadeIn(b,shift=DOWN*0.2,run_time=0.20))
        self.play(FadeOut(b,shift=UP*0.2,run_time=0.20))

    def _zt(self,t,scale=2.5,dur=0.4):
        c=t if isinstance(t,np.ndarray) else t.get_center()
        self.play(self.camera.frame.animate.scale(1/scale).move_to(c),run_time=dur)

    def _zo(self,dur=0.35):
        self.play(self.camera.frame.animate.set(width=14.2).move_to(ORIGIN),run_time=dur)

    def _clr(self):
        self.play(self.camera.frame.animate.set(width=14.2).move_to(ORIGIN),run_time=0.2)
        rm=[m for m in self.mobjects
            if m is not self._ch
            and m is not self._pb_segs
            and m is not self._pb_lbl]
        if rm: self.play(FadeOut(Group(*rm),run_time=0.2))

    def say(self, key, fn=None, anim_dur=0.0):
        """
        Synchronisation garantie sans chevauchement :
        1. add_sound()  → son démarre au temps T
        2. fn()         → animations (durée réelle = anim_dur)
        3. wait(gap)    → on attend le MAXIMUM de (son, animations)
                          + buffer fixe de 0.08s entre chaque say()
        Ainsi le son suivant ne peut JAMAIS commencer avant la fin
        du son courant ET de l'animation courante.
        """
        BUFFER = 0.08  # gap minimal garanti entre deux sons
        self.add_sound(AP(key))
        if fn: fn()
        # On attend jusqu'à ce que LES DEUX soient terminés
        total = max(DUR(key), anim_dur)
        gap   = total - anim_dur + BUFFER
        if gap > 0.0: self.wait(gap)

    def construct(self):
        self.camera.background_color=BG
        self._init_char()
        self._init_progress()
        self._intro()
        self._probleme()
        # ── NOUVELLES SECTIONS PÉDAGOGIQUES ──────────────────────────────
        self._comprendre_fx_px()        # f(x) vs P(x)
        self._comprendre_x()            # qu'est-ce que x ?
        self._comprendre_courbe_unique() # pourquoi une seule courbe ?
        # ── SECTIONS EXISTANTES ──────────────────────────────────────────
        self._unicite()
        self._explication_sigma()
        self._explication_Li()
        self.say("tr_lag", lambda: self.play(Flash(self._ch, color=C_YEL, run_time=0.5)), anim_dur=0.5)
        self._lagrange()
        self._explication_beta()
        self._comprendre_beta_voiture()  # intuition bêta avec voiture
        self._explication_diff_div()
        self.say("tr_newt", lambda: self.play(Flash(self._ch, color=C_PUR, run_time=0.5)), anim_dur=0.5)
        self._newton()
        self._explication_passage()
        self.say("tr_pass", lambda: self.play(Flash(self._ch, color=C_GRN, run_time=0.5)), anim_dur=0.5)
        self._comparaison()
        self._erreur()
        self._exemple()
        self._faq()
        self._conclusion()

    # ═══════════════════════════════════════════════════════════════════════
    #  NOUVELLES SECTIONS PÉDAGOGIQUES
    # ═══════════════════════════════════════════════════════════════════════

    # ─── f(x) vs P(x) ───────────────────────────────────────────────────────
    def _comprendre_fx_px(self):
        self._set_progress(2)
        tl=title_line("f(x) vs P(x) — la différence essentielle", C_GRN)
        tl.to_edge(UP, buff=0.3)

        # Axes et courbes
        ax=hand_axes((0,25,4),(-1,30,5),xl=8.5,yl=4.2); ax.shift(DOWN*0.5)
        pts=[(0,10),(12,25),(24,15)]

        # f(x) — courbe inconnue (on simule la vraie avec un sinus)
        f_r=lambda x: 10+15*np.sin(x*np.pi/24)+2*np.sin(x*np.pi/8)
        # P(x) — notre parabole calculée
        P_=lag_fn(pts)

        curve_f=ax.plot(f_r, x_range=[0,24], color=C_GRY, stroke_width=1.8, stroke_opacity=0.5)
        curve_P=ax.plot(P_,  x_range=[0,24], color=C_BLU, stroke_width=3.0)

        dots=VGroup(*[hdot(ax,x,y,C_RED) for x,y in pts])
        lbl_f=Text("f(x) — réalité inconnue", font_size=16, color=C_GRY)
        lbl_f.to_edge(RIGHT,buff=0.2).shift(UP*1.2)
        lbl_P=Text("P(x) — votre approximation", font_size=16, color=C_BLU)
        lbl_P.next_to(lbl_f,DOWN,buff=0.22)

        # Boîtes d'explication côte à côte
        box_f=VGroup(
            Text("f(x)", font_size=28, color=C_GRY, weight=BOLD),
            Text("La réalité", font_size=18, color=C_GRY),
            Text("Connue seulement", font_size=15, color=C_GRY),
            Text("en 3 points", font_size=15, color=C_GRY),
        ).arrange(DOWN,buff=0.12)
        rect_f=SurroundingRectangle(box_f,color=C_GRY,stroke_width=1.5,buff=0.22,corner_radius=0.12)
        gf=VGroup(rect_f,box_f)

        box_P=VGroup(
            Text("P(x)", font_size=28, color=C_BLU, weight=BOLD),
            Text("Votre construction", font_size=18, color=C_BLU),
            Text("Passe exactement", font_size=15, color=C_BLU),
            Text("par les 3 points", font_size=15, color=C_BLU),
        ).arrange(DOWN,buff=0.12)
        rect_P=SurroundingRectangle(box_P,color=C_BLU,stroke_width=1.5,buff=0.22,corner_radius=0.12)
        gP=VGroup(rect_P,box_P)

        compare=VGroup(gf,gP).arrange(RIGHT,buff=1.0)

        # Flèche erreur à x=18
        xg=18; yP=P_(xg); yF=f_r(xg)
        seg_err=DashedLine(ax.c2p(xg,yP),ax.c2p(xg,yF),color=C_RED,stroke_width=2.5)
        lbl_err=Text("erreur = f − P", font_size=16, color=C_RED)
        lbl_err.next_to(ax.c2p(xg,(yP+yF)/2),RIGHT,buff=0.15)

        def fn_fp1():
            self._section_banner("f(x) vs P(x)", C_GRN)
            self.play(Write(tl[0],run_time=0.7), Create(tl[1],run_time=0.3))
        self.say("fp1", fn_fp1, anim_dur=0.4+0.7+0.3)

        def fn_fp2():
            self.play(Create(ax,run_time=0.6))
            self.play(Create(curve_f,run_time=1.0))
            self.play(FadeIn(lbl_f,run_time=0.5))
        self.say("fp2", fn_fp2, anim_dur=2.1)

        def fn_fp3():
            self.play(LaggedStartMap(GrowFromCenter,dots,lag_ratio=0.3,run_time=0.8))
        self.say("fp3", fn_fp3, anim_dur=0.8)

        def fn_fp4():
            self.play(Create(curve_P,run_time=1.2))
            self.play(FadeIn(lbl_P,run_time=0.5))
        self.say("fp4", fn_fp4, anim_dur=1.7)

        def fn_fp5():
            self.play(Create(seg_err,run_time=0.8))
            self.play(FadeIn(lbl_err,run_time=0.5))
        self.say("fp5", fn_fp5, anim_dur=1.3)

        def fn_fp6():
            self.play(FadeOut(VGroup(ax,curve_f,curve_P,dots,lbl_f,lbl_P,seg_err,lbl_err),run_time=0.3))
            compare.move_to(ORIGIN)
            self.play(FadeIn(gf,shift=RIGHT*0.3,run_time=0.8))
            self.play(FadeIn(gP,shift=LEFT*0.3,run_time=0.8))
            pulse_formula(self,gP,C_BLU,n=2)
        self.say("fp6", fn_fp6, anim_dur=0.3+0.8+0.8+0.88)
        self._clr()

    # ─── QU'EST-CE QUE x ? ──────────────────────────────────────────────────
    def _comprendre_x(self):
        self._set_progress(3)
        tl=title_line("Qu'est-ce que x ?", C_TEA)
        tl.to_edge(UP, buff=0.3)

        # Machine à calculer
        machine=RoundedRectangle(width=3.5,height=2.0,corner_radius=0.3,
                                  fill_color=C_DIM,fill_opacity=1,
                                  stroke_color=C_TEA,stroke_width=2.5)
        machine.move_to(ORIGIN)
        m_lbl=Text("P(x)", font_size=36, color=C_TEA, weight=BOLD)
        m_lbl.move_to(machine.get_center())
        m_sub=Text("machine à calculer", font_size=14, color=C_GRY)
        m_sub.next_to(machine,DOWN,buff=0.15)

        # Entrée / sortie
        arr_in=Arrow(LEFT*4.5,LEFT*1.8,color=C_ORG,stroke_width=2.5,max_tip_length_to_length_ratio=0.2)
        arr_out=Arrow(RIGHT*1.8,RIGHT*4.5,color=C_GRN,stroke_width=2.5,max_tip_length_to_length_ratio=0.2)
        lbl_in=Text("x = 6h", font_size=22, color=C_ORG, weight=BOLD)
        lbl_in.next_to(arr_in,UP,buff=0.15)
        lbl_out=Text("P(6) = 20.4°", font_size=22, color=C_GRN, weight=BOLD)
        lbl_out.next_to(arr_out,UP,buff=0.15)

        # Ligne de points connus
        pts_line=VGroup(
            VGroup(Text("x₀ = 0h",  font_size=18,color=C_RED), Text("connu",font_size=13,color=C_GRY)).arrange(DOWN,buff=0.05),
            VGroup(Text("x₁ = 12h", font_size=18,color=C_RED), Text("connu",font_size=13,color=C_GRY)).arrange(DOWN,buff=0.05),
            VGroup(Text("x₂ = 24h", font_size=18,color=C_RED), Text("connu",font_size=13,color=C_GRY)).arrange(DOWN,buff=0.05),
        ).arrange(RIGHT,buff=0.8)
        pts_line.next_to(machine,UP,buff=0.8)

        sep_line=Line(pts_line.get_left()+LEFT*0.3, pts_line.get_right()+RIGHT*0.3,
                      stroke_width=0.8, color=C_GRY)
        sep_line.next_to(pts_line,DOWN,buff=0.1)

        # Explication x - x0
        eq_box=VGroup(
            MathTex(r"x - x_0 = 6 - 0 = 6", font_size=28, color=C_YEL),
            Text("← distance depuis le premier point mesuré", font_size=16, color=C_GRY),
        ).arrange(DOWN,buff=0.2)
        eq_box.to_edge(DOWN,buff=0.6)
        hb_eq=hbox(eq_box[0],C_YEL)

        def fn_qx1():
            self._section_banner("Qu'est-ce que x ?", C_TEA)
            self.play(Write(tl[0],run_time=0.7), Create(tl[1],run_time=0.3))
        self.say("qx1", fn_qx1, anim_dur=0.4+0.7+0.3)

        def fn_qx2():
            self.play(Create(machine,run_time=0.6))
            self.play(Write(m_lbl,run_time=0.5), FadeIn(m_sub,run_time=0.4))
        self.say("qx2", fn_qx2, anim_dur=1.5)

        def fn_qx3():
            self.play(FadeIn(pts_line,run_time=0.7))
            self.play(Create(sep_line,run_time=0.3))
        self.say("qx3", fn_qx3, anim_dur=1.0)

        def fn_qx4():
            self.play(GrowArrow(arr_in,run_time=0.6))
            self.play(FadeIn(lbl_in,run_time=0.5))
        self.say("qx4", fn_qx4, anim_dur=1.1)

        def fn_qx5():
            self.play(GrowArrow(arr_out,run_time=0.6))
            self.play(FadeIn(lbl_out,run_time=0.5))
        self.say("qx5", fn_qx5, anim_dur=1.1)

        def fn_qx6():
            self.play(Write(eq_box[0],run_time=0.8),
                      Create(hb_eq[1],run_time=0.5),Create(hb_eq[0],run_time=0.5))
            self.play(FadeIn(eq_box[1],run_time=0.6))
            pulse_formula(self,eq_box[0],C_YEL,n=2)
        self.say("qx6", fn_qx6, anim_dur=0.8+0.6+0.88)
        self._clr()

    # ─── POURQUOI UNE SEULE COURBE ? ────────────────────────────────────────
    def _comprendre_courbe_unique(self):
        self._set_progress(4)
        tl=title_line("Pourquoi une seule courbe ?", C_YEL)
        tl.to_edge(UP, buff=0.3)

        ax=hand_axes((0,25,4),(0,35,5),xl=8.0,yl=4.2); ax.shift(DOWN*0.5)
        pts=[(0,10),(12,25),(24,15)]
        P_=lag_fn(pts)
        dots=VGroup(*[hdot(ax,x,y,C_RED) for x,y in pts])

        # 4 courbes quelconques passant par les 3 points
        def perturb(c):
            def f(x):
                base=P_(x)
                return base + c*x*(x-12)*(x-24)/300
            return f

        colors_other=[C_GRY,C_TEA,C_PUR,C_ORG]
        other_curves=VGroup(*[
            ax.plot(perturb(c),x_range=[0,24],color=col,stroke_width=1.5,stroke_opacity=0.4)
            for c,col in zip([-2,-1,1,2],colors_other)
        ])
        lbl_other=Text("∞ courbes possibles — chacune donne un résultat différent à 6h",
                       font_size=16,color=C_GRY)
        lbl_other.to_edge(DOWN,buff=0.9)

        # La vraie courbe — P de degré 2
        curve_P=ax.plot(P_,x_range=[0,24],color=C_YEL,stroke_width=3.5)
        lbl_P=Text("P(x) de degré 2 — unique !", font_size=20, color=C_YEL, weight=BOLD)
        lbl_P.to_edge(DOWN,buff=0.6)

        # Théorème encadré
        thm=VGroup(
            Text("3 points  →  3 inconnues  →  1 seul polynôme de degré 2",
                 font_size=22,color=C_YEL),
        )
        hb_thm=hbox(thm,C_YEL)

        def fn_cu1():
            self._section_banner("Une seule courbe ?", C_YEL)
            self.play(Write(tl[0],run_time=0.7), Create(tl[1],run_time=0.3))
            self.play(Create(ax,run_time=0.6))
        self.say("cu1", fn_cu1, anim_dur=0.4+0.7+0.3+0.6)

        def fn_cu2():
            self.play(LaggedStartMap(GrowFromCenter,dots,lag_ratio=0.3,run_time=0.7))
            self.play(LaggedStartMap(Create,other_curves,lag_ratio=0.15,run_time=1.2))
            self.play(FadeIn(lbl_other,run_time=0.5))
        self.say("cu2", fn_cu2, anim_dur=2.4)

        def fn_cu3():
            self.play(FadeOut(VGroup(other_curves,lbl_other),run_time=0.3))
            self.play(Create(curve_P,run_time=1.2))
            self.play(FadeIn(lbl_P,run_time=0.5))
        self.say("cu3", fn_cu3, anim_dur=2.0)

        def fn_cu4():
            self.play(FadeOut(VGroup(ax,curve_P,dots,lbl_P),run_time=0.3))
            thm.move_to(ORIGIN)
            self.play(Write(thm[0],run_time=1.0),
                      Create(hb_thm[1],run_time=0.6),Create(hb_thm[0],run_time=0.6))
            pulse_formula(self,thm,C_YEL,n=2)
        self.say("cu4", fn_cu4, anim_dur=0.3+1.0+0.88)

        def fn_cu5():
            self._zt(thm,scale=1.4)
            self._zo()
        self.say("cu5", fn_cu5, anim_dur=0.4+0.35)
        self._clr()

    # ─── INTUITION BÊTA AVEC LA VOITURE ─────────────────────────────────────
    def _comprendre_beta_voiture(self):
        self._set_progress(6)
        tl=title_line("Intuition de bêta — la voiture", C_ORG)
        tl.to_edge(UP, buff=0.3)

        # Étages beta comme pour voiture
        floor_data=[
            (C_ORG, "β₀ = 20 km",          "Position initiale : km 20"),
            (C_TEA, "β₁·(x−x₀) = 60(x−0)", "Vitesse : +60 km/h"),
            (C_PUR, "β₂·(x−x₀)(x−x₁)",     "Accélération : freinage ou accél."),
        ]
        floors=VGroup(); flabels=VGroup()
        for i,(c,mtxt,etxt) in enumerate(floor_data):
            rect=Rectangle(width=5.5,height=0.65,fill_color=c,fill_opacity=0.25,
                           stroke_color=c,stroke_width=1.5)
            rect.move_to(np.array([0.8,-1.0+i*0.82,0]))
            el=Text(etxt,font_size=14,color=c); el.next_to(rect,LEFT,buff=0.2)
            ml=Text(mtxt,font_size=14,color=C_WHT); ml.move_to(rect.get_center())
            floors.add(rect); flabels.add(VGroup(el,ml))

        # Graphe position vs temps
        ax=hand_axes((0,3,0.5),(0,100,20),xl=7.5,yl=3.0); ax.move_to(np.array([0,0.5,0]))
        pts_v=[(0,20),(1,80),(2,50)]
        curve_v=ax.plot(lag_fn(pts_v),x_range=[0,2],color=C_ORG,stroke_width=2.8)
        dots_v=VGroup(*[hdot(ax,x,y,C_RED) for x,y in pts_v])
        ax_lbl_x=Text("temps (h)", font_size=14, color=C_GRY).next_to(ax,RIGHT,buff=0.1)
        ax_lbl_y=Text("km", font_size=14, color=C_GRY).next_to(ax,UP,buff=0.1)

        formula_v=MathTex(
            r"P(x)=\beta_0 + \beta_1(x-x_0) + \beta_2(x-x_0)(x-x_1)",
            font_size=22, color=C_PUR)
        formula_v.to_edge(DOWN,buff=0.5)
        hb_v=hbox(formula_v,C_PUR)

        def fn_bv1():
            self._section_banner("Bêta avec la voiture", C_ORG)
            self.play(Write(tl[0],run_time=0.7), Create(tl[1],run_time=0.3))
        self.say("bv1", fn_bv1, anim_dur=0.4+0.7+0.3)

        def fn_bv2():
            self.play(GrowFromEdge(floors[0],edge=DOWN,run_time=0.6))
            self.play(FadeIn(flabels[0],run_time=0.5))
        self.say("bv2", fn_bv2, anim_dur=1.1)

        def fn_bv3():
            self.play(GrowFromEdge(floors[1],edge=DOWN,run_time=0.6))
            self.play(FadeIn(flabels[1],run_time=0.5))
        self.say("bv3", fn_bv3, anim_dur=1.1)

        def fn_bv4():
            self.play(GrowFromEdge(floors[2],edge=DOWN,run_time=0.6))
            self.play(FadeIn(flabels[2],run_time=0.5))
        self.say("bv4", fn_bv4, anim_dur=1.1)

        def fn_bv5():
            self.play(FadeOut(VGroup(floors,flabels),run_time=0.3))
            self.play(Create(ax,run_time=0.6))
            self.play(FadeIn(ax_lbl_x,run_time=0.3),FadeIn(ax_lbl_y,run_time=0.3))
            self.play(LaggedStartMap(GrowFromCenter,dots_v,lag_ratio=0.3,run_time=0.7))
            self.play(Create(curve_v,run_time=1.0))
        self.say("bv5", fn_bv5, anim_dur=0.3+0.6+0.3+0.7+1.0)

        def fn_bv6():
            self.play(Write(formula_v,run_time=1.0),
                      Create(hb_v[1],run_time=0.6),Create(hb_v[0],run_time=0.6))
            pulse_formula(self,formula_v,C_PUR,n=2)
        self.say("bv6", fn_bv6, anim_dur=1.0+0.88)
        self._clr()

    # ═══════════════════════════════════════════════════════════════════════
    #  SECTIONS EXISTANTES (inchangées)
    # ═══════════════════════════════════════════════════════════════════════

    def _intro(self):
        self._set_progress(0)
        titre=Text("Interpolation Polynomiale",font_size=48,color=C_YEL,weight=BOLD)
        sous=Text("Analyse Numérique · 3ème année",font_size=22,color=C_GRY)
        sous.next_to(titre,DOWN,buff=0.35)
        self.say("i1", lambda: self.play(Write(titre,run_time=1.2)), anim_dur=1.2)
        self.say("i2", lambda: self.play(FadeIn(sous,shift=UP*0.2,run_time=1.0)), anim_dur=1.0)
        self._clr()

    def _probleme(self):
        self._set_progress(1)
        tl=title_line("Le problème",C_BLU); tl.to_edge(UP,buff=0.3)
        ax=hand_axes((0,7,1),(-1,5,1),xl=8.0,yl=4.6); ax.shift(DOWN*0.4)
        f_r=lambda x:2+np.sin(x)*np.cos(x*0.5)*1.5
        spts=[(x,f_r(x)) for x in [1.0,2.3,3.6,5.0,6.2]]
        dots=VGroup(*[hdot(ax,x,y,C_ORG) for x,y in spts])
        c_p=ax.plot(lag_fn(spts),x_range=[0.4,6.6],color=C_GRN,stroke_width=2.8)
        lpt=Text("points mesurés",font_size=17,color=C_ORG); lpt.next_to(dots[2],UP,buff=0.35)
        apt=Arrow(lpt.get_bottom(),dots[2].get_top(),color=C_ORG,stroke_width=1.5,buff=0.05,max_tip_length_to_length_ratio=0.25)
        lcp=Text("polynôme d'interpolation",font_size=17,color=C_GRN)
        lcp.to_edge(RIGHT,buff=0.25).shift(DOWN*0.5)
        acp=Arrow(lcp.get_left(),c_p.point_from_proportion(0.65),color=C_GRN,stroke_width=1.5,buff=0.05,max_tip_length_to_length_ratio=0.25)

        def fn_p1():
            self._section_banner("Le Problème",C_BLU)
            self.play(Write(tl[0],run_time=0.6)); self.play(Create(tl[1],run_time=0.25))
        self.say("p1", fn_p1, anim_dur=0.4+0.6+0.25)

        def fn_p2():
            self.play(Create(ax,run_time=0.8))
            self.play(LaggedStartMap(GrowFromCenter,dots,lag_ratio=0.2,run_time=0.6))
        self.say("p2", fn_p2, anim_dur=1.4)

        def fn_p3():
            self.play(FadeIn(lpt,run_time=0.4)); self.play(GrowArrow(apt,run_time=0.4))
        self.say("p3", fn_p3, anim_dur=0.8)

        def fn_p4():
            self.play(Create(c_p,run_time=1.0))
            self.play(FadeIn(lcp,run_time=0.25),GrowArrow(acp,run_time=0.25))
        self.say("p4", fn_p4, anim_dur=1.5)
        self._clr()

    def _unicite(self):
        self._set_progress(4)
        tl=title_line("Existence et unicité",C_YEL); tl.to_edge(UP,buff=0.3)
        ax=hand_axes((-0.5,5,1),(-1.5,4,1),xl=7.8,yl=4.6); ax.shift(DOWN*0.4)
        p1=hdot(ax,2.5,2.0,C_ORG); p2=hdot(ax,4.0,1.2,C_ORG); p3=hdot(ax,1.0,0.5,C_ORG)
        many=VGroup(*[ax.plot(lambda x,a=a:a*(x-2.5)**2+2,x_range=[0.2,4.8],color=C_BLU,stroke_width=1.4,stroke_opacity=0.20) for a in [-0.9,-0.45,0,0.45,0.9,1.2]])
        l2=ax.plot(lag_fn([(2.5,2),(4,1.2)]),x_range=[0.2,4.8],color=C_BLU,stroke_width=2.5)
        l3=ax.plot(lag_fn([(1,0.5),(2.5,2),(4,1.2)]),x_range=[0.2,4.8],color=C_TEA,stroke_width=2.5)
        lb1=Text("∞ courbes",font_size=20,color=C_BLU).to_edge(DOWN,buff=0.4)
        lb2=Text("1 seule droite",font_size=20,color=C_BLU).to_edge(DOWN,buff=0.4)
        lb3=Text("1 seule parabole",font_size=20,color=C_TEA).to_edge(DOWN,buff=0.4)
        thm=VGroup(MathTex(r"n+1\;\text{points distincts}",font_size=32,color=C_YEL),
                   MathTex(r"\Downarrow",font_size=36,color=C_GRY),
                   MathTex(r"\exists!\;P_n\;\text{tel que}\;P_n(x_i)=y_i",font_size=30,color=C_GRN)
                   ).arrange(DOWN,buff=0.40)
        hb=hbox(thm,C_YEL)

        def fn_u1():
            self._section_banner("Existence et Unicité",C_YEL)
            self.play(Write(tl[0],run_time=0.7),Create(tl[1],run_time=0.3))
            self.play(Create(ax,run_time=0.5))
        self.say("u1", fn_u1, anim_dur=0.4+1.0+0.5)
        def fn_u2():
            self.play(GrowFromCenter(p1,run_time=0.25))
            self.play(LaggedStartMap(Create,many,lag_ratio=0.08,run_time=0.8))
            self.play(Write(lb1,run_time=0.5))
        self.say("u2", fn_u2, anim_dur=1.6)
        def fn_u3():
            self.play(FadeOut(VGroup(many,lb1),run_time=0.2))
            self.play(GrowFromCenter(p2,run_time=0.25))
            self.play(Create(l2,run_time=0.7)); self.play(Write(lb2,run_time=0.5))
        self.say("u3", fn_u3, anim_dur=1.65)
        def fn_u4():
            self.play(FadeOut(VGroup(l2,lb2),run_time=0.2))
            self.play(GrowFromCenter(p3,run_time=0.25))
            self.play(Create(l3,run_time=0.7)); self.play(Write(lb3,run_time=0.5))
        self.say("u4", fn_u4, anim_dur=1.65)
        def fn_u5():
            self.play(FadeOut(VGroup(l3,lb3,ax,p1,p2,p3),run_time=0.25))
            self.play(Write(thm[0],run_time=0.7)); self.play(FadeIn(thm[1],run_time=0.3))
            self.play(Write(thm[2],run_time=0.8),Create(hb[1],run_time=0.5),Create(hb[0],run_time=0.5))
        self.say("u5", fn_u5, anim_dur=2.55)
        def fn_u6():
            self._zt(thm,scale=1.4); pulse_formula(self,thm,C_YEL,n=2); self._zo()
        self.say("u6", fn_u6, anim_dur=0.4+0.88+0.35)
        self._clr()

    def _explication_sigma(self):
        self._set_progress(5)
        tl=title_line("Sigma — C'est quoi une somme ?",C_YEL); tl.to_edge(UP,buff=0.3)
        mois=["Jan","Fev","Mar","Avr","Mai"]; vals=[100,120,80,150,90]
        cols_b=[C_BLU,C_GRN,C_ORG,C_PUR,C_TEA]
        barres=VGroup(); labels=VGroup(); max_h=2.5
        for i,(m,v,c) in enumerate(zip(mois,vals,cols_b)):
            h=v/150*max_h
            bar=Rectangle(width=0.9,height=h,fill_color=c,fill_opacity=0.85,stroke_width=0)
            bar.move_to(np.array([-3.5+i*1.6,-1.5+h/2,0]))
            lm=Text(m,font_size=16,color=c); lm.next_to(bar,DOWN,buff=0.08)
            lv=Text(f"{v}E",font_size=15,color=C_WHT); lv.next_to(bar,UP,buff=0.06)
            barres.add(bar); labels.add(VGroup(lm,lv))
        total_box=RoundedRectangle(width=5.5,height=0.75,corner_radius=0.15,fill_color=C_YEL,fill_opacity=0.15,stroke_color=C_YEL,stroke_width=2.0)
        total_box.move_to(np.array([0,-2.4,0]))
        total_txt=MathTex(r"\Sigma = 100+120+80+150+90 = \mathbf{540}",font_size=26,color=C_YEL); total_txt.move_to(total_box)
        ax_s=hand_axes((0,5,1),(0,5,1),xl=8.0,yl=3.5); ax_s.move_to(np.array([0,0.2,0]))
        pts_s=[(1,1),(2,4),(3,2),(4,4)]
        curve_s=ax_s.plot(lag_fn(pts_s),x_range=[0.5,4.5],color=C_GRN,stroke_width=2.8)
        sig_dots=VGroup(*[hdot(ax_s,x,y,C_YEL) for x,y in pts_s])
        sig_lbl=VGroup(*[MathTex(f"y_{i}",font_size=18,color=C_YEL).next_to(ax_s.c2p(x,y),UR,buff=0.1) for i,(x,y) in enumerate(pts_s)])
        sigma_form=MathTex(r"P_n(x)=\sum_{i=0}^{n}y_i\,L_i(x)",font_size=30,color=C_YEL)
        sigma_form.to_edge(DOWN,buff=0.5); hbf=hbox(sigma_form,C_YEL)
        sigma_ann=Text("<-- sigma : additionne chaque y_i fois L_i",font_size=15,color=C_GRY)
        sigma_ann.next_to(sigma_form,UP,buff=0.15)
        def fn_es1():
            self._section_banner("Comprendre Sigma",C_YEL)
            self.play(Write(tl[0],run_time=0.8)); self.play(Create(tl[1],run_time=0.3))
        self.say("es1", fn_es1, anim_dur=0.4+1.1)
        def fn_es2():
            self.play(LaggedStartMap(GrowFromEdge,barres,edge=DOWN,lag_ratio=0.2,run_time=1.4))
            self.play(LaggedStartMap(FadeIn,labels,lag_ratio=0.2,run_time=0.6))
        self.say("es2", fn_es2, anim_dur=2.0)
        def fn_es3():
            self.play(FadeIn(total_box,run_time=0.25)); self.play(Write(total_txt,run_time=0.8))
        self.say("es3", fn_es3, anim_dur=1.05)
        def fn_es4():
            self.play(FadeOut(VGroup(barres,labels,total_box,total_txt),run_time=0.25))
            self.play(Create(ax_s,run_time=0.5))
            self.play(Create(curve_s,run_time=0.8),LaggedStartMap(GrowFromCenter,sig_dots,lag_ratio=0.2,run_time=0.6))
            self.play(FadeIn(sig_lbl,run_time=0.5))
            self.play(Write(sigma_form,run_time=0.8),Create(hbf[1],run_time=0.5),Create(hbf[0],run_time=0.5))
            self.play(FadeIn(sigma_ann,run_time=0.5))
            pulse_formula(self,sigma_form,C_YEL,n=2)
        self.say("es4", fn_es4, anim_dur=0.25+0.5+0.8+0.5+0.8+0.5+0.88)
        self._clr()

    def _explication_Li(self):
        self._set_progress(5)
        tl=title_line("L_i — Le spot qui éclaire une seule chaise",C_TEA); tl.to_edge(UP,buff=0.3)
        chairs_pos=[-3.0,-1.0,1.0,3.0]; chairs_col=[C_ORG,C_TEA,C_PUR,C_RED]
        chairs=VGroup(*[Circle(radius=0.28,fill_color=c,fill_opacity=0.15,stroke_color=c,stroke_width=2.0).move_to(np.array([x,-0.5,0])) for x,c in zip(chairs_pos,chairs_col)])
        chair_lbl=VGroup(*[Text(f"x{i}",font_size=16,color=c).next_to(chairs[i],DOWN,buff=0.1) for i,c in enumerate(chairs_col)])
        spot=Circle(radius=0.28,fill_color=C_TEA,fill_opacity=0.9,stroke_color=C_TEA,stroke_width=3); spot.move_to(chairs[1].get_center())
        glow=Circle(radius=0.45,color=C_TEA,stroke_opacity=0.3,stroke_width=8,fill_opacity=0); glow.move_to(spot.get_center())
        val1=Text("L1(x1) = 1",font_size=22,color=C_TEA,weight=BOLD); val1.next_to(spot,UP,buff=0.35)
        cross_labels=VGroup(*[Text("L1(xi) = 0",font_size=16,color=C_GRY).next_to(chairs[i],UP,buff=0.25) for i in [0,2,3]])
        kron=MathTex(r"L_i(x_j)=\begin{cases}1 & i=j\\0 & i\neq j\end{cases}",font_size=28,color=C_TEA)
        kron.to_edge(DOWN,buff=0.55); hbk=hbox(kron,C_TEA)
        def fn_el1():
            self._section_banner("Comprendre L_i Lagrange",C_TEA)
            self.play(Write(tl[0],run_time=0.8)); self.play(Create(tl[1],run_time=0.3))
            self.play(LaggedStartMap(GrowFromCenter,chairs,lag_ratio=0.2,run_time=0.6))
            self.play(FadeIn(chair_lbl,run_time=0.35))
        self.say("el1", fn_el1, anim_dur=0.4+0.8+0.3+0.6+0.35)
        def fn_el2():
            self.play(Transform(chairs[1],spot,run_time=0.5))
            self.play(FadeIn(glow,run_time=0.25)); self.play(Write(val1,run_time=0.5))
        self.say("el2", fn_el2, anim_dur=1.25)
        self.say("el3", lambda: self.play(FadeIn(cross_labels,run_time=0.6)), anim_dur=0.6)
        def fn_el4():
            self.play(Write(kron,run_time=0.8),Create(hbk[1],run_time=0.5),Create(hbk[0],run_time=0.5))
            pulse_formula(self,kron,C_TEA,n=2)
        self.say("el4", fn_el4, anim_dur=0.8+0.88)
        self._clr()

    def _lagrange(self):
        self._set_progress(5)
        tl=title_line("Méthode de Lagrange",C_TEA); tl.to_edge(UP,buff=0.3)
        xs3=[0.8,2.5,4.2]
        ax=hand_axes((0,5,1),(-0.5,1.8,0.5),xl=7.2,yl=3.8); ax.shift(DOWN*0.5).shift(LEFT*0.5)
        BCOLS=[C_ORG,C_TEA,C_PUR]
        def Li(i,xs):
            def f(x):
                v=1.
                for j,xj in enumerate(xs):
                    if j!=i: v*=(x-xj)/(xs[i]-xj)
                return v
            return f
        curves=VGroup(*[ax.plot(Li(i,xs3),x_range=[0.1,4.9],color=col,stroke_width=2.5) for i,col in enumerate(BCOLS)])
        lbl_b=VGroup(MathTex(r"L_0(x)",font_size=22,color=C_ORG),MathTex(r"L_1(x)",font_size=22,color=C_TEA),MathTex(r"L_2(x)",font_size=22,color=C_PUR)).arrange(DOWN,buff=0.4).to_edge(RIGHT,buff=0.4)
        kron=MathTex(r"L_i(x_j)=\begin{cases}1&i=j\\0&i\neq j\end{cases}",font_size=26,color=C_TEA); kron.to_edge(RIGHT,buff=0.35).shift(UP*0.6)
        ann1=MathTex(r"L_0(x_0)=1",font_size=28,color=C_ORG)
        arr1=Arrow(ann1.get_bottom(),ax.c2p(xs3[0],1.0),color=C_ORG,stroke_width=1.5,buff=0.1,max_tip_length_to_length_ratio=0.25)
        f_lag=VGroup(MathTex(r"P_n(x)=\sum_{i=0}^{n}y_i\,L_i(x)",font_size=40,color=C_YEL),MathTex(r"L_i(x)=\prod_{j\neq i}\frac{x-x_j}{x_i-x_j}",font_size=32,color=C_TEA)).arrange(DOWN,buff=0.5)
        hb2=hbox(f_lag,C_YEL)
        def fn_l1():
            self._section_banner("Méthode de Lagrange",C_TEA)
            self.play(Write(tl[0],run_time=0.8),Create(tl[1],run_time=0.35))
        self.say("l1", fn_l1, anim_dur=0.4+0.8)
        self.say("l2", lambda: self.play(Create(ax,run_time=1.1)), anim_dur=1.1)
        def fn_l3():
            self.play(Create(curves[0],run_time=1.3)); self.play(FadeIn(lbl_b[0],run_time=0.5))
        self.say("l3", fn_l3, anim_dur=1.8)
        def fn_l4():
            self.play(Create(curves[1],run_time=1.3)); self.play(FadeIn(lbl_b[1],run_time=0.5))
        self.say("l4", fn_l4, anim_dur=1.8)
        def fn_l5():
            self.play(Create(curves[2],run_time=1.3)); self.play(FadeIn(lbl_b[2],run_time=0.5))
        self.say("l5", fn_l5, anim_dur=1.8)
        self.say("l6", lambda: self.play(Write(kron,run_time=1.1)), anim_dur=1.1)
        def fn_l7():
            self._zt(ax.c2p(xs3[0],1.0),scale=3.2)
            ann1.move_to(self.camera.frame.get_center()+UP*0.5)
            self.play(Write(ann1,run_time=0.6),GrowArrow(arr1,run_time=0.6))
            self.play(FadeOut(VGroup(ann1,arr1),run_time=0.25)); self._zo()
        self.say("l7", fn_l7, anim_dur=0.4+0.6+0.25+0.35)
        self.say("l11", lambda: self.play(FadeOut(VGroup(ax,curves,lbl_b,kron),run_time=0.8)), anim_dur=0.8)
        def fn_l8():
            self.play(Write(f_lag[0],run_time=1.3),Create(hb2[1],run_time=0.6),Create(hb2[0],run_time=0.6))
        self.say("l8", fn_l8, anim_dur=1.3)
        def fn_l9():
            self._zt(f_lag[0],scale=1.5); pulse_formula(self,f_lag[0],C_YEL,n=2); self._zo()
        self.say("l9", fn_l9, anim_dur=0.4+0.88+0.35)
        self.say("l10", lambda: self.play(FadeIn(f_lag[1],shift=UP*0.2,run_time=1.1)), anim_dur=1.1)
        self._clr()

    def _explication_beta(self):
        self._set_progress(6)
        tl=title_line("Beta — Étage par étage vers la courbe",C_PUR); tl.to_edge(UP,buff=0.3)
        floor_data=[(C_ORG,"b0 = valeur de depart","Rez-de-chaussee : point initial"),(C_TEA,"b1(x-x0) = pente","1er etage : monte ou descend"),(C_PUR,"b2(x-x0)(x-x1) = courbure","2eme etage : tourne a gauche ou droite")]
        floors=VGroup(); flabels=VGroup()
        for i,(c,mtxt,etxt) in enumerate(floor_data):
            rect=Rectangle(width=5.5,height=0.65,fill_color=c,fill_opacity=0.25,stroke_color=c,stroke_width=1.5)
            rect.move_to(np.array([0.8,-1.0+i*0.82,0]))
            el=Text(etxt,font_size=14,color=c); el.next_to(rect,LEFT,buff=0.2)
            ml=Text(mtxt,font_size=14,color=C_WHT); ml.move_to(rect.get_center())
            floors.add(rect); flabels.add(VGroup(el,ml))
        ax_b=hand_axes((0,3,1),(0,5,1),xl=7.5,yl=3.2); ax_b.move_to(np.array([0,0.5,0]))
        pts_b=[(0.5,1.0),(1.5,4.0),(2.5,2.5)]
        curve_b=ax_b.plot(lag_fn(pts_b),x_range=[0.3,2.7],color=C_YEL,stroke_width=2.8)
        dots_b=VGroup(*[hdot(ax_b,x,y,C_PUR) for x,y in pts_b])
        ann_b0=MathTex(r"\beta_0",font_size=22,color=C_ORG); ann_b0.next_to(ax_b.c2p(pts_b[0][0],pts_b[0][1]),LEFT,buff=0.15)
        arr_b0=Arrow(ann_b0.get_right(),ax_b.c2p(pts_b[0][0],pts_b[0][1]),color=C_ORG,stroke_width=1.5,buff=0.05,max_tip_length_to_length_ratio=0.3)
        ann_b1=MathTex(r"\beta_1",font_size=22,color=C_TEA); ann_b1.next_to(ax_b.c2p(1.0,2.5),UP,buff=0.1)
        ann_b2=MathTex(r"\beta_2",font_size=22,color=C_PUR); ann_b2.next_to(ax_b.c2p(pts_b[2][0],pts_b[2][1]),RIGHT,buff=0.15)
        formula=MathTex(r"P(x)=\beta_0+\beta_1(x-x_0)+\beta_2(x-x_0)(x-x_1)",font_size=22,color=C_PUR)
        formula.to_edge(DOWN,buff=0.5); hbp=hbox(formula,C_PUR)
        def fn_eb1():
            self._section_banner("Comprendre Beta",C_PUR)
            self.play(Write(tl[0],run_time=0.8)); self.play(Create(tl[1],run_time=0.3))
        self.say("eb1", fn_eb1, anim_dur=0.4+1.1)
        def fn_eb2():
            self.play(GrowFromEdge(floors[0],edge=DOWN,run_time=0.6)); self.play(FadeIn(flabels[0],run_time=0.5))
        self.say("eb2", fn_eb2, anim_dur=1.1)
        def fn_eb3():
            self.play(GrowFromEdge(floors[1],edge=DOWN,run_time=0.6)); self.play(FadeIn(flabels[1],run_time=0.5))
        self.say("eb3", fn_eb3, anim_dur=1.1)
        def fn_eb4():
            self.play(GrowFromEdge(floors[2],edge=DOWN,run_time=0.6)); self.play(FadeIn(flabels[2],run_time=0.5))
        self.say("eb4", fn_eb4, anim_dur=1.1)
        def fn_eb5():
            self.play(FadeOut(VGroup(floors,flabels),run_time=0.25))
            self.play(Create(ax_b,run_time=0.5))
            self.play(Create(curve_b,run_time=0.8),LaggedStartMap(GrowFromCenter,dots_b,lag_ratio=0.3,run_time=0.6))
            self.play(FadeIn(ann_b0,run_time=0.25),GrowArrow(arr_b0,run_time=0.25))
            self.play(FadeIn(ann_b1,run_time=0.25)); self.play(FadeIn(ann_b2,run_time=0.25))
            self.play(Write(formula,run_time=0.8),Create(hbp[1],run_time=0.5),Create(hbp[0],run_time=0.5))
            pulse_formula(self,formula,C_PUR,n=2)
        self.say("eb5", fn_eb5, anim_dur=0.25+0.5+0.8+0.5+0.88)
        self._clr()

    def _explication_diff_div(self):
        self._set_progress(6)
        tl=title_line("beta = vitesse entre deux points",C_ORG); tl.to_edge(UP,buff=0.3)
        ax=hand_axes((0,2,0.5),(0,200,50),xl=7.5,yl=3.5); ax.move_to(np.array([0,0.0,0]))
        pt_a=hdot(ax,0.5,100,C_BLU); pt_b=hdot(ax,1.5,160,C_GRN)
        la=Text("12h00 : 100 km",font_size=16,color=C_BLU); la.next_to(ax.c2p(0.5,100),LEFT,buff=0.15)
        lb=Text("13h00 : 160 km",font_size=16,color=C_GRN); lb.next_to(ax.c2p(1.5,160),RIGHT,buff=0.15)
        seg=DashedLine(ax.c2p(0.5,100),ax.c2p(1.5,160),color=C_ORG,stroke_width=2.8)
        calc1=Text("Difference : 160 - 100 = 60 km",font_size=20,color=C_ORG); calc1.to_edge(DOWN,buff=1.0)
        calc2=Text("Distance en temps : 1.5 - 0.5 = 1 heure",font_size=20,color=C_ORG); calc2.to_edge(DOWN,buff=1.0)
        spd=MathTex(r"\beta_1 = \frac{60\text{ km}}{1\text{ h}} = 60\text{ km/h}",font_size=28,color=C_ORG)
        spd.to_edge(DOWN,buff=0.7); hbs=hbox(spd,C_ORG)
        annot=Text("La difference divisee = variation / ecart = bêta !",font_size=17,color=C_YEL,weight=BOLD)
        annot.next_to(spd,UP,buff=0.2)
        def fn_ed1():
            self._section_banner("Comprendre les Differences Divisees",C_ORG)
            self.play(Write(tl[0],run_time=0.8)); self.play(Create(tl[1],run_time=0.3))
            self.play(Create(ax,run_time=0.5))
        self.say("ed1", fn_ed1, anim_dur=0.4+0.8+0.3+0.5)
        def fn_ed2():
            self.play(GrowFromCenter(pt_a,run_time=0.35)); self.play(FadeIn(la,run_time=0.35))
            self.play(GrowFromCenter(pt_b,run_time=0.35)); self.play(FadeIn(lb,run_time=0.35))
        self.say("ed2", fn_ed2, anim_dur=1.4)
        def fn_ed3():
            self.play(Create(seg,run_time=0.8)); self.play(Write(calc1,run_time=0.6))
        self.say("ed3", fn_ed3, anim_dur=1.4)
        def fn_ed4():
            self.play(Transform(calc1,calc2,run_time=0.5))
            self.play(Write(spd,run_time=0.8),Create(hbs[1],run_time=0.5),Create(hbs[0],run_time=0.5))
            self.play(FadeIn(annot,run_time=0.5)); pulse_formula(self,spd,C_ORG,n=2)
        self.say("ed4", fn_ed4, anim_dur=0.5+0.8+0.5+0.88)
        self._clr()

    def _newton(self):
        self._set_progress(6)
        tl=title_line("Méthode de Newton",C_PUR); tl.to_edge(UP,buff=0.3)
        tbl_t=Text("Table des différences divisées :",font_size=20,color=C_PUR,weight=BOLD); tbl_t.next_to(tl,DOWN,buff=0.55)
        hrow=mkrow(("x_i",C_GRY),("y_i",C_GRY),(r"f[\cdot,\cdot]",C_GRY),(r"f[\cdot,\cdot,\cdot]",C_GRY))
        r1=mkrow((r"x_0",C_ORG),(r"y_0",C_ORG),(r"\beta_1",C_TEA),(r"\beta_2",C_PUR))
        r2=mkrow((r"x_1",C_ORG),(r"y_1",C_ORG),(r"f[x_1,x_2]",C_TEA),("",C_GRY))
        r3=mkrow((r"x_2",C_ORG),(r"y_2",C_ORG),("",C_GRY),("",C_GRY))
        tbl=VGroup(hrow,r1,r2,r3).arrange(DOWN,buff=0.32,aligned_edge=LEFT)
        sep=Line(hrow.get_left(),hrow.get_right(),stroke_width=0.7,color=C_GRY).next_to(hrow,DOWN,buff=0.07)
        a1=Arrow(r1[1].get_right(),r1[2].get_left(),buff=0.07,color=C_TEA,stroke_width=1.5,max_tip_length_to_length_ratio=0.22)
        a2=Arrow(r2[1].get_right(),r2[2].get_left(),buff=0.07,color=C_TEA,stroke_width=1.5,max_tip_length_to_length_ratio=0.22)
        a3=Arrow(r1[2].get_right(),r1[3].get_left(),buff=0.07,color=C_PUR,stroke_width=1.5,max_tip_length_to_length_ratio=0.22)
        f_new=VGroup(MathTex(r"P_n(x)=\beta_0+\beta_1(x-x_0)+\beta_2(x-x_0)(x-x_1)+\cdots",font_size=25,color=C_PUR),MathTex(r"\beta_k=f[x_0,x_1,\ldots,x_k]",font_size=23,color=C_YEL)).arrange(DOWN,buff=0.35)
        hb3=hbox(f_new[0],C_PUR)
        def fn_n1():
            self._section_banner("Méthode de Newton",C_PUR)
            self.play(Write(tl[0],run_time=0.7)); self.play(Create(tl[1],run_time=0.3))
        self.say("n1", fn_n1, anim_dur=0.4+0.7+0.3)
        def fn_n4():
            self.play(FadeIn(tbl_t,run_time=0.6)); self.play(FadeIn(hrow,run_time=0.5),Create(sep,run_time=0.3))
        self.say("n4", fn_n4, anim_dur=1.4)
        def fn_n5():
            self.play(FadeIn(r1,run_time=0.6)); self.play(FadeIn(r2,run_time=0.6)); self.play(FadeIn(r3,run_time=0.6))
        self.say("n5", fn_n5, anim_dur=1.8)
        self.say("n7", lambda: self.play(GrowArrow(a1,run_time=1.4)), anim_dur=1.4)
        self.say("n8", lambda: self.play(GrowArrow(a2,run_time=1.4)), anim_dur=1.4)
        def fn_n9():
            self.play(GrowArrow(a3,run_time=0.7)); self._zt(a3,scale=2.5); self._zo()
        self.say("n9", fn_n9, anim_dur=0.7+0.4+0.35)
        self.say("n10", lambda: self.play(FadeOut(VGroup(tbl_t,tbl,sep,a1,a2,a3),run_time=1.0)), anim_dur=1.0)
        def fn_n11():
            self.play(Write(f_new[0],run_time=1.1),Create(hb3[1],run_time=0.6),Create(hb3[0],run_time=0.6))
            self.play(FadeIn(f_new[1],shift=UP*0.2,run_time=0.6))
        self.say("n11", fn_n11, anim_dur=1.7)
        def fn_n12():
            self._zt(f_new[0],scale=1.5); pulse_formula(self,f_new[0],C_PUR,n=2); self._zo()
        self.say("n12", fn_n12, anim_dur=0.4+0.88+0.35)
        self._clr()

    def _explication_passage(self):
        self._set_progress(7)
        tl=title_line("Le polynôme touche chaque point exactement",C_GRN); tl.to_edge(UP,buff=0.3)
        ax=hand_axes((0,4,1),(0,5,1),xl=8.0,yl=3.8); ax.move_to(np.array([0,-0.1,0]))
        pts=[(0.5,1.0),(1.5,4.0),(2.5,2.5),(3.5,4.5)]; cols_p=[C_RED,C_BLU,C_GRN,C_PUR]
        dots=VGroup(*[hdot(ax,x,y,c) for (x,y),c in zip(pts,cols_p)])
        curve=ax.plot(lag_fn(pts),x_range=[0.3,3.7],color=C_YEL,stroke_width=3.0)
        pt_labels=VGroup(*[Text(f"M{i}",font_size=16,color=c).next_to(ax.c2p(x,y),UP,buff=0.15) for i,((x,y),c) in enumerate(zip(pts,cols_p))])
        vlines=VGroup(*[DashedLine(ax.c2p(x,0),ax.c2p(x,y),stroke_width=1.2,color=c,stroke_opacity=0.5) for (x,y),c in zip(pts,cols_p)])
        checks=VGroup(*[Text("OK",font_size=14,color=C_GRN,weight=BOLD).next_to(ax.c2p(x,y),UR,buff=0.08) for x,y in pts])
        concl=Text("Chaque bêta ajuste la courbe vers le point suivant.",font_size=18,color=C_YEL,weight=BOLD); concl.to_edge(DOWN,buff=0.55)
        concl2=Text("Comme une couturière qui ajuste tissu par tissu !",font_size=16,color=C_GRY); concl2.next_to(concl,DOWN,buff=0.1)
        def fn_ec1():
            self._section_banner("Comment la courbe passe par les points ?",C_GRN)
            self.play(Write(tl[0],run_time=0.8)); self.play(Create(tl[1],run_time=0.3))
            self.play(Create(ax,run_time=0.5))
        self.say("ec1", fn_ec1, anim_dur=0.4+0.8+0.3+0.5)
        def fn_ec2():
            self.play(GrowFromCenter(dots[0],run_time=0.25)); self.play(FadeIn(pt_labels[0],run_time=0.25))
            self.play(Create(curve,run_time=1.4))
        self.say("ec2", fn_ec2, anim_dur=1.9)
        def fn_ec3():
            self.play(LaggedStartMap(GrowFromCenter,dots[1:],lag_ratio=0.2,run_time=0.8))
            self.play(LaggedStartMap(FadeIn,pt_labels[1:],lag_ratio=0.2,run_time=0.6))
            self.play(LaggedStartMap(Create,vlines,lag_ratio=0.2,run_time=0.8))
            self.play(LaggedStartMap(FadeIn,checks,lag_ratio=0.2,run_time=0.6))
        self.say("ec3", fn_ec3, anim_dur=2.8)
        def fn_ec4():
            self.play(Write(concl,run_time=0.8)); self.play(FadeIn(concl2,run_time=0.6))
        self.say("ec4", fn_ec4, anim_dur=1.4)
        self._clr()

    def _comparaison(self):
        self._set_progress(7)
        tl=title_line("Lagrange  vs  Newton",C_GRN); tl.to_edge(UP,buff=0.3)
        def cell(txt,col,bg=None,fs=17):
            t=Text(txt,font_size=fs,color=col)
            if bg:
                b=RoundedRectangle(width=max(t.width+0.5,2.8),height=t.height+0.28,corner_radius=0.07,fill_color=bg,fill_opacity=0.25,stroke_color=col,stroke_width=0.8)
                b.move_to(t.get_center()); return VGroup(b,t)
            return t
        rows=[("Critère",C_WHT,"Lagrange",C_TEA,"Newton",C_PUR),("Formule",C_GRY,"Somme explicite",C_TEA,"Table itérative",C_PUR),("Ajout 1 point",C_GRY,"Tout recalculer",C_RED,"1 seul terme",C_GRN),("Complexité",C_GRY,"O(n²)",C_ORG,"O(n)",C_GRN),("Résultat",C_GRY,"Pₙ(x) identique",C_YEL,"Pₙ(x) identique",C_YEL)]
        tbl=VGroup()
        for ct,cc,lt,lc,nt,nc in rows:
            tbl.add(VGroup(cell(ct,cc,fs=17),cell(lt,lc,C_DIM,17),cell(nt,nc,C_DIM,17)).arrange(RIGHT,buff=0.6))
        tbl.arrange(DOWN,buff=0.28,aligned_edge=LEFT).next_to(tl,DOWN,buff=0.4)
        sep=Line(tbl[0].get_left()+LEFT*0.1,tbl[0].get_right()+RIGHT*0.1,stroke_width=0.8,color=C_GRY).next_to(tbl[0],DOWN,buff=0.08)
        note=Text("Les deux donnent exactement le même Pₙ(x) !",font_size=20,color=C_YEL); note.next_to(tbl,DOWN,buff=0.35); hbn=hbox(note,C_YEL)
        def fn_cmp1():
            self._section_banner("Lagrange vs Newton",C_GRN)
            self.play(Write(tl[0],run_time=0.8)); self.play(Create(tl[1],run_time=0.3))
        self.say("cmp1", fn_cmp1, anim_dur=0.4+0.8+0.3)
        def fn_cmp2():
            self.play(FadeIn(tbl[0],run_time=0.5)); self.play(Create(sep,run_time=0.25))
            self.play(FadeIn(tbl[1],shift=RIGHT*0.15,run_time=0.6))
        self.say("cmp2", fn_cmp2, anim_dur=1.35)
        def fn_cmp3():
            self.play(FadeIn(tbl[2],shift=RIGHT*0.15,run_time=0.6))
            self.play(FadeIn(tbl[3],shift=RIGHT*0.15,run_time=0.6))
        self.say("cmp3", fn_cmp3, anim_dur=1.2)
        def fn_cmp4():
            self.play(FadeIn(tbl[4],shift=RIGHT*0.15,run_time=0.6))
            self.play(FadeIn(note,run_time=0.5),Create(hbn[1],run_time=0.35),Create(hbn[0],run_time=0.35))
            pulse_formula(self,note,C_YEL,n=2)
        self.say("cmp4", fn_cmp4, anim_dur=0.6+0.5+0.88)
        self._clr()

    def _erreur(self):
        self._set_progress(7)
        tl=title_line("Erreur d'interpolation",C_RED); tl.to_edge(UP,buff=0.3)
        ax=hand_axes((0,5,1),(-0.5,3,0.5),xl=7.2,yl=4.0); ax.shift(DOWN*0.4).shift(LEFT*0.3)
        gf=lambda x:0.5*np.sin(x)+1+0.3*x
        spts=[(1,gf(1)),(2.5,gf(2.5)),(4,gf(4))]
        cR=ax.plot(gf,x_range=[0.3,4.8],color=C_BLU,stroke_width=2.2)
        cI=ax.plot(lag_fn(spts),x_range=[0.3,4.8],color=C_ORG,stroke_width=2.2)
        xg=3.3; yI=lag_fn(spts)(xg); yF=gf(xg)
        seg=DashedLine(ax.c2p(xg,yI),ax.c2p(xg,yF),color=C_RED,stroke_width=2.5)
        lf=MathTex(r"f(x)",font_size=18,color=C_BLU); lf.next_to(ax.c2p(4.5,gf(4.5)),UR,buff=0.1)
        lp=MathTex(r"P_n(x)",font_size=18,color=C_ORG); lp.next_to(ax.c2p(4.5,lag_fn(spts)(4.5)),DR,buff=0.1)
        le=MathTex(r"|E_n|",font_size=20,color=C_RED); le.next_to(ax.c2p(xg,(yI+yF)/2),RIGHT,buff=0.15)
        val=MathTex(rf"|E|\approx{abs(yF-yI):.3f}",font_size=28,color=C_RED)
        arv=Arrow(val.get_left(),ax.c2p(xg,(yI+yF)/2),color=C_RED,stroke_width=1.5,buff=0.08,max_tip_length_to_length_ratio=0.25)
        ef=VGroup(MathTex(r"|E_n(x)|\leq\frac{M_{n+1}}{(n+1)!}\prod_{i=0}^{n}|x-x_i|",font_size=28,color=C_RED),MathTex(r"M_{n+1}=\max_{[a,b]}|f^{(n+1)}(t)|",font_size=22,color=C_GRY)).arrange(DOWN,buff=0.3)
        hb4=hbox(ef[0],C_RED)
        runge=VGroup(Text("⚠  Phénomène de Runge :",font_size=20,color=C_YEL,weight=BOLD),Text("trop de points mal placés → grandes oscillations",font_size=19,color=C_YEL)).arrange(DOWN,buff=0.10).next_to(ef,DOWN,buff=0.45)
        def fn_e1():
            self._section_banner("Erreur d'Interpolation",C_RED)
            self.play(Write(tl[0],run_time=0.7),Create(tl[1],run_time=0.3))
            self.play(Create(ax,run_time=0.5))
        self.say("e1", fn_e1, anim_dur=0.4+0.7+0.5)
        def fn_e2():
            self.play(Create(cR,run_time=0.8)); self.play(FadeIn(lf,run_time=0.35))
        self.say("e2", fn_e2, anim_dur=1.15)
        def fn_e3():
            self.play(Create(cI,run_time=0.8)); self.play(FadeIn(lp,run_time=0.35))
        self.say("e3", fn_e3, anim_dur=1.15)
        def fn_e4():
            self.play(Create(seg,run_time=0.7)); self.play(FadeIn(le,run_time=0.5))
        self.say("e4", fn_e4, anim_dur=1.2)
        def fn_e6():
            self._zt(ax.c2p(xg,(yI+yF)/2),scale=3.2)
            val.move_to(self.camera.frame.get_center()+RIGHT*0.7)
            self.play(Write(val,run_time=0.6),GrowArrow(arv,run_time=0.6))
            self.play(FadeOut(VGroup(val,arv),run_time=0.25)); self._zo()
        self.say("e6", fn_e6, anim_dur=0.4+0.6+0.25+0.35)
        self.say("e7", lambda: self.play(FadeOut(VGroup(ax,cR,cI,seg,lf,lp,le),run_time=1.0)), anim_dur=1.0)
        def fn_e8():
            self.play(Write(ef[0],run_time=1.3),Create(hb4[1],run_time=0.6),Create(hb4[0],run_time=0.6))
        self.say("e8", fn_e8, anim_dur=1.3)
        def fn_e9():
            self._zt(ef[0],scale=1.5); pulse_formula(self,ef[0],C_RED,n=2); self._zo()
        self.say("e9", fn_e9, anim_dur=0.4+0.88+0.35)
        self.say("e10", lambda: self.play(FadeIn(ef[1],run_time=1.0)), anim_dur=1.0)
        self.say("e11", lambda: self.play(Write(runge[0],run_time=1.0)), anim_dur=1.0)
        self.say("e12", lambda: self.play(Write(runge[1],run_time=1.3)), anim_dur=1.3)
        self._clr()

    def _exemple(self):
        self._set_progress(8)
        tl=title_line("Exemple : f(x) = cos(πx/4)",C_ORG); tl.to_edge(UP,buff=0.3)
        b0=1.0; b1=np.sqrt(2)/2-1.0; f12_=-(np.sqrt(2)/2); b2=(f12_-b1)/2.0
        rw=VGroup(MathTex(r"M_0(0,1)",font_size=23,color=C_ORG),MathTex(r"M_1\!\left(1,\tfrac{\sqrt2}{2}\right)",font_size=23,color=C_ORG),MathTex(r"M_2(2,0)",font_size=23,color=C_ORG)).arrange(RIGHT,buff=0.7).next_to(tl,DOWN,buff=0.5)
        tbl_t=Text("Table de Newton :",font_size=18,color=C_PUR,weight=BOLD); tbl_t.next_to(rw,DOWN,buff=0.38)
        tbl=VGroup(mkrow(("x_i",C_GRY),("y_i",C_GRY),(r"f[\cdot,\cdot]",C_GRY),(r"\beta_k",C_GRY)),mkrow((r"0",C_ORG),(r"1",C_ORG),(rf"{b1:.3f}",C_TEA),(rf"{b2:.3f}",C_PUR)),mkrow((r"1",C_ORG),(r"\tfrac{\sqrt2}{2}",C_ORG),(rf"{f12_:.3f}",C_TEA),("",C_GRY)),mkrow((r"2",C_ORG),(r"0",C_ORG),("",C_GRY),("",C_GRY))).arrange(DOWN,buff=0.28,aligned_edge=LEFT).next_to(tbl_t,DOWN,buff=0.28)
        sep=Line(tbl[0].get_left(),tbl[0].get_right(),stroke_width=0.7,color=C_GRY).next_to(tbl[0],DOWN,buff=0.07)
        ta1=Arrow(tbl[1][1].get_right(),tbl[1][2].get_left(),buff=0.07,color=C_TEA,stroke_width=1.4,max_tip_length_to_length_ratio=0.22)
        ta2=Arrow(tbl[2][1].get_right(),tbl[2][2].get_left(),buff=0.07,color=C_TEA,stroke_width=1.4,max_tip_length_to_length_ratio=0.22)
        ta3=Arrow(tbl[1][2].get_right(),tbl[1][3].get_left(),buff=0.07,color=C_PUR,stroke_width=1.4,max_tip_length_to_length_ratio=0.22)
        def fn_x1():
            self._section_banner("Exemple Numérique",C_ORG)
            self.play(Write(tl[0],run_time=0.8)); self.play(Create(tl[1],run_time=0.3))
        self.say("x1", fn_x1, anim_dur=0.4+0.8+0.3)
        self.say("x2", lambda: self.play(FadeIn(rw[0],shift=UP*0.12,run_time=1.3)), anim_dur=1.3)
        self.say("x3", lambda: self.play(FadeIn(rw[1],shift=UP*0.12,run_time=1.3)), anim_dur=1.3)
        self.say("x4", lambda: self.play(FadeIn(rw[2],shift=UP*0.12,run_time=1.3)), anim_dur=1.3)
        def fn_x5():
            self.play(FadeIn(tbl_t,run_time=0.6)); self.play(FadeIn(tbl[0],run_time=0.5),Create(sep,run_time=0.3))
        self.say("x5", fn_x5, anim_dur=1.4)
        def fn_x6():
            self.play(FadeIn(tbl[1],run_time=0.6)); self.play(FadeIn(tbl[2],run_time=0.6)); self.play(FadeIn(tbl[3],run_time=0.6))
        self.say("x6", fn_x6, anim_dur=1.8)
        self.say("x7", lambda: self.play(GrowArrow(ta1,run_time=1.0),GrowArrow(ta2,run_time=1.0)), anim_dur=1.0)
        self.say("x8", lambda: self.play(GrowArrow(ta3,run_time=1.3)), anim_dur=1.3)
        def fn_x9():
            self._zt(ta3,scale=2.5); self._zo()
        self.say("x9", fn_x9, anim_dur=0.4+0.35)
        self.say("x10", lambda: self.play(FadeOut(VGroup(rw,tbl_t,tbl,sep,ta1,ta2,ta3),run_time=1.0)), anim_dur=1.0)
        f4=lambda x:np.cos(np.pi/4*x); P2_=lambda x:b0+b1*x+b2*x*(x-1)
        f3v=f4(3); b3=((f3v-f12_)/2-b2)/3; P3_=lambda x:P2_(x)+b3*x*(x-1)*(x-2)
        pts3=[(0,1.0),(1,np.sqrt(2)/2),(2,0.0)]
        ax=hand_axes((-.2,3.5,.5),(-.9,1.4,.4),xl=8.0,yl=4.8); ax.shift(DOWN*0.3)
        ce=ax.plot(f4,x_range=[0,3.4],color=C_BLU,stroke_width=2.5,stroke_opacity=0.7)
        c2=ax.plot(P2_,x_range=[0,2.95],color=C_ORG,stroke_width=2.8)
        c3=ax.plot(P3_,x_range=[0,3.4],color=C_GRN,stroke_width=2.8)
        dts=VGroup(*[hdot(ax,x,y,C_ORG) for x,y in pts3])
        pt3=hdot(ax,3,f3v,C_GRN)
        lf2=MathTex(r"f(x)",font_size=17,color=C_BLU).to_edge(RIGHT,buff=0.3).shift(UP*1.6)
        lp2=MathTex(r"P_2(x)",font_size=17,color=C_ORG).next_to(lf2,DOWN,buff=0.22)
        lp3=MathTex(r"P_3(x)",font_size=17,color=C_GRN).next_to(lp2,DOWN,buff=0.22)
        xv=0.5; yp=P2_(xv); yf2=f4(xv)
        eseg=DashedLine(ax.c2p(xv,yp),ax.c2p(xv,yf2),color=C_RED,stroke_width=2.5)
        ne=MathTex(rf"|E|\approx{abs(yp-yf2):.4f}",font_size=28,color=C_RED)
        ae=Arrow(ne.get_left(),ax.c2p(xv,(yp+yf2)/2),color=C_RED,stroke_width=1.5,buff=0.08,max_tip_length_to_length_ratio=0.25)
        arrm=Arrow(ax.c2p(3,f3v)+UP*0.7,ax.c2p(3,f3v),color=C_GRN,stroke_width=2,max_tip_length_to_length_ratio=0.28)
        lm3=MathTex(r"M_3",font_size=18,color=C_GRN).next_to(ax.c2p(3,f3v)+UP*0.7,UP,buff=0.08)
        def fn_x11():
            self.play(Create(ax,run_time=0.7)); self.play(LaggedStartMap(GrowFromCenter,dts,lag_ratio=0.2,run_time=0.7))
        self.say("x11", fn_x11, anim_dur=1.4)
        def fn_x12():
            self.play(Create(ce,run_time=1.0)); self.play(FadeIn(lf2,run_time=0.5))
        self.say("x12", fn_x12, anim_dur=1.5)
        def fn_x13():
            self.play(Create(c2,run_time=1.0)); self.play(FadeIn(lp2,run_time=0.5))
        self.say("x13", fn_x13, anim_dur=1.5)
        self.say("x14", lambda: self.play(Create(eseg,run_time=1.3)), anim_dur=1.3)
        def fn_x15():
            self._zt(ax.c2p(xv,(yp+yf2)/2),scale=3.5)
            ne.move_to(self.camera.frame.get_center()+RIGHT*0.6)
            self.play(Write(ne,run_time=0.6),GrowArrow(ae,run_time=0.6))
            self.play(FadeOut(VGroup(ne,ae,eseg),run_time=0.25)); self._zo()
        self.say("x15", fn_x15, anim_dur=0.4+0.6+0.25+0.35)
        def fn_x16():
            self.play(GrowFromCenter(pt3,run_time=0.6)); self.play(GrowArrow(arrm,run_time=0.6))
            self.play(FadeIn(lm3,run_time=0.5))
        self.say("x16", fn_x16, anim_dur=1.7)
        def fn_x17():
            self.play(Create(c3,run_time=1.3)); self.play(FadeIn(lp3,run_time=0.5))
            self.play(FadeOut(VGroup(arrm,lm3),run_time=0.25))
        self.say("x17", fn_x17, anim_dur=2.05)
        self._clr()

    def _faq(self):
        self._set_progress(9)
        tl=title_line("Questions Fréquentes",C_BLU); tl.to_edge(UP,buff=0.3)
        def faq_card(q,a,qcol,y):
            qi=Text("?",font_size=24,color=qcol,weight=BOLD); ql=Text(q,font_size=17,color=C_WHT)
            qr=VGroup(qi,ql).arrange(RIGHT,buff=0.22)
            qb=RoundedRectangle(width=11.2,height=0.52,corner_radius=0.10,fill_color=qcol,fill_opacity=0.10,stroke_color=qcol,stroke_width=1.5)
            qr.move_to(qb.get_center()); qcard=VGroup(qb,qr)
            ai=Text("→",font_size=19,color=C_GRN); al=Text(a,font_size=15,color=C_GRY)
            ar=VGroup(ai,al).arrange(RIGHT,buff=0.22)
            ar.next_to(qcard,DOWN,buff=0.09,aligned_edge=LEFT).shift(RIGHT*0.3)
            card=VGroup(qcard,ar); card.move_to(np.array([0,y,0])); return card
        c1=faq_card("Peut-on interpoler avec des points non distincts ?","Non. Deux points avec le même x rendent le polynôme indéfini.",C_RED,1.4)
        c2=faq_card("Plus de points donne-t-il toujours un meilleur résultat ?","Non. Le phénomène de Runge crée des oscillations avec trop de points.",C_YEL,0.0)
        c3=faq_card("Quelle méthode choisir en pratique ?","Newton si ajout progressif. Lagrange pour une formule explicite directe.",C_GRN,-1.4)
        def fn_faq0():
            self._section_banner("Questions Fréquentes",C_BLU)
            self.play(Write(tl[0],run_time=0.8)); self.play(Create(tl[1],run_time=0.3))
        self.say("faq0", fn_faq0, anim_dur=0.4+0.8+0.3)
        self.say("faq1",  lambda: self.play(FadeIn(c1[0],shift=RIGHT*0.2,run_time=1.6)), anim_dur=1.6)
        self.say("faq1r", lambda: self.play(FadeIn(c1[1],shift=RIGHT*0.15,run_time=1.6)), anim_dur=1.6)
        self.say("faq2",  lambda: self.play(FadeIn(c2[0],shift=RIGHT*0.2,run_time=1.6)), anim_dur=1.6)
        self.say("faq2r", lambda: self.play(FadeIn(c2[1],shift=RIGHT*0.15,run_time=1.6)), anim_dur=1.6)
        self.say("faq3",  lambda: self.play(FadeIn(c3[0],shift=RIGHT*0.2,run_time=1.6)), anim_dur=1.6)
        self.say("faq3r", lambda: self.play(FadeIn(c3[1],shift=RIGHT*0.15,run_time=1.6)), anim_dur=1.6)
        self._clr()

    def _conclusion(self):
        self._set_progress(9)
        tl=title_line("En résumé",C_YEL); tl.to_edge(UP,buff=0.3)
        bd=[(C_TEA,Text("Lagrange :",font_size=22,color=C_TEA,weight=BOLD),MathTex(r"P_n(x)=\sum_{i=0}^{n}y_i\,L_i(x)",font_size=22,color=C_WHT)),
            (C_PUR,Text("Newton :",font_size=22,color=C_PUR,weight=BOLD),Text("différences divisées, ajout facile",font_size=21,color=C_WHT)),
            (C_RED,Text("Erreur :",font_size=22,color=C_RED,weight=BOLD),MathTex(r"|E_n|\leq\frac{M_{n+1}}{(n+1)!}\prod_{i}|x-x_i|",font_size=20,color=C_WHT))]
        items=VGroup()
        for col,lbl,cnt in bd:
            items.add(VGroup(Dot(radius=0.09,color=col),lbl,cnt).arrange(RIGHT,buff=0.22))
        items.arrange(DOWN,buff=0.5,aligned_edge=LEFT).next_to(tl,DOWN,buff=0.55)
        final=MathTex(r"P_n(x)=\sum_{i=0}^{n}y_i\,L_i(x)",font_size=36,color=C_YEL); final.to_edge(DOWN,buff=0.8)
        hbf=hbox(final,C_YEL)
        closing=Text("Bonne révision !",font_size=30,color=C_GRN,weight=BOLD); closing.next_to(final,DOWN,buff=0.42)
        def fn_c1():
            self._section_banner("En Résumé",C_YEL)
            self.play(Write(tl[0],run_time=0.8),Create(tl[1],run_time=0.5))
        self.say("c1", fn_c1, anim_dur=0.4+0.8)
        self.say("c2", lambda: self.play(FadeIn(items[0],shift=RIGHT*0.2,run_time=1.1)), anim_dur=1.1)
        self.say("c3", lambda: self.play(FadeIn(items[1],shift=RIGHT*0.2,run_time=1.1)), anim_dur=1.1)
        self.say("c4", lambda: self.play(FadeIn(items[2],shift=RIGHT*0.2,run_time=1.1)), anim_dur=1.1)
        def fn_c5():
            self.play(Write(final,run_time=1.1),Create(hbf[1],run_time=0.6),Create(hbf[0],run_time=0.6))
        self.say("c5", fn_c5, anim_dur=1.1)
        def fn_c6():
            self._zt(final,scale=1.5); pulse_formula(self,final,C_YEL,n=2); self._zo()
            self.play(Write(closing,run_time=0.7))
        self.say("c6", fn_c6, anim_dur=0.4+0.88+0.35+0.7)
        self.wait(0.5)