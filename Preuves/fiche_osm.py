import argparse
from md_to_html import convert
import requests
import math
from io import BytesIO
from PIL import Image, ImageDraw


def get_node(id:int)->dict:
    """Prend un id de noeud OSM en argument et télécharge les données sur ce noeud dans un dict"""
    api_url = "https://www.openstreetmap.org/api/0.6/node/" +str(id)+".json"
    response = requests.get(api_url)
    donnees = response.json()
    return donnees


def get_node_name(dict:dict)->str:
    """Cette fonction prend un identifiant de nœud OSM en argument et renvoit le nom de ce noeud"""
    try: 
        for c,v in dict['elements'][0]['tags'].items():
            if c == 'name':
                return v
    except:
        return "SANS NOM"

def print_node_attributes(dict:dict)->list:
    """Cette fonction prend un identifiant de nœud OSM en argument et renvoit les attributs de ce noeud (liste)"""
    res=[]
    for c,v in dict['elements'][0]['tags'].items():
        res.append(c + " : " + v )
    return res


def node_to_md(data: dict, filename: str) -> None:
    """Cette fonction prend un dictionnaire et un fichier en argument et reecrit ce dico dans ce fichier en md"""
    list=print_node_attributes(data)
    content=""
    content+= "# "+get_node_name(data)+ "\n\n" 
    for i in list:
        content+="* "+i+"\n"
    with open(filename, "w") as fichier:
        fichier.write(content)

def fiche_osm(id: int) -> None :
    """Prend un id de open street map et crer un .md et un .html de ce noeud"""
    try:
        node_to_md(get_node(id),"data.md")
        generate_map(id)

        with open("data.md","a")as fichier:
            fichier.write(f"\n![Image de la carte](photo_marqué.png)\n")
        convert("data.md","data.html")

    except :
        return "Erreur ID incorrect"


def get_node_coord_lat(num:int)->str:
    """Cette fonction prend un identifiant de nœud OSM en argument et renvoit les coordonnees de ce noeud"""
    donnees=get_node(num)
    for clef,valeur in donnees.items():
        if clef == 'elements':
            for i in valeur:
                for a,b in i.items():
                    if a == 'lat':
                        return b


def get_node_coord_lon(num:int)->str:
    """Cette fonction prend un identifiant de nœud OSM en argument et renvoit les coordonnees de ce noeud"""
    donnees=get_node(num)
    for clef,valeur in donnees.items():
        if clef == 'elements':
            for i in valeur:
                for a,b in i.items():
                    if a == 'lon':
                        return b




def latlon_to_tile_and_pixel(lat, lon, zoom, dimension=256)->list:
    """ Convertit une coordonnée GPS en indices de tuile Web Mercator et en position pixel dans la tuile"""
    res=[]

    # Convert the coordinate to the Web Mercator projection
    x_mercator = lon

    lat_rad = math.radians(lat)
    y_mercator = math.asinh(math.tan(lat_rad))

    # Transform the projected point onto the unit square
    x = 0.5 + x_mercator / 360.0
    y = 0.5 - y_mercator / (2 * math.pi)

    # Determine the zoom level and horizontal/vertical location of individual tiles
    n = 2 ** zoom

    xtile_float = n * x
    ytile_float = n * y

    xtile = int(xtile_float)
    ytile = int(ytile_float)

    # Transform the projected point into tile space
    xpixel = (xtile_float - xtile) * dimension
    ypixel = (ytile_float - ytile) * dimension

    res=[zoom,xtile,ytile,xpixel,ypixel]

    return res

def get_img_marque(list:list[str])->None:
    """ Prends liste zoom,xtile,ytile,xpixel,ypixel et telecharge la tuile correspondante marqué"""

    zoom=list[0]
    xtile=list[1]
    ytile=list[2]
    x=list[3]
    y=list[4]

    headers = {
        "User-Agent": "InstallTile"
    }

    response = requests.get("https://tile.openstreetmap.org/"+str(zoom)+"/"+str(xtile)+"/"+str(ytile)+".png", headers=headers, timeout=10)

    img = Image.open(BytesIO(response.content)).convert("RGBA")
    draw = ImageDraw.Draw(img)
    r = 6 

    draw.ellipse(
        (x - r, y - r, x + r, y + r), fill=(255, 0, 0) # Fait une ellipse avec 4 points et la remplie avec du rouge
    )

    return img.save("photo_marqué.png")

def generate_map(id)-> None:
    """ A partir d'un noeud renvoit une carte marqué de cette endroit"""
    get_img_marque(latlon_to_tile_and_pixel(get_node_coord_lat(id),get_node_coord_lon(id),18))


if __name__ == "__main__":
    """ Si exe dans terminal"""
    parser = argparse.ArgumentParser(
        description="Prend un noeud sur OpenStreetMap pour en faire un .md et un .html"
    )
    parser.add_argument(
        "id",
        type=int,
        help="ID du noeud OpenStreetMap"
        )

    args = parser.parse_args()
    fiche_osm(args.id)



