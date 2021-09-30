"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def initCatalog():
    catalog = {
        "artists": None,
        "artworks": None,
        "mediums": None}

    catalog["mediums"] = mp.newMap(100,111,"PROBING",loadfactor=0.5)
    return catalog

# Funciones para agregar informacion al catalogo
def loadArtists(catalog, filename):
    catalog["artists"] = lt.newList('ARRAY_LIST', filename=filename)
    return catalog

def loadArtworks(catalog, filename):
    catalog["artworks"] = lt.newList('ARRAY_LIST', filename=filename)
    return catalog

# Funciones para creacion de datos
def addArtist(catalog, artist):
    lt.addLast(catalog["artists"], artist)

def addArtwork(catalog, artwork):
    lt.addLast(catalog["artworks"], artwork)
    mp.put(catalog["mediums"], artwork["Medium"], artwork)

# Funciones de consulta

def olderArtworksbyMedium(catalog,medium,x):
    olderones = lt.newList("ARRAY_LIST")
    for artwork in lt.iterator(catalog["artworks"]):
        if artwork["Medium"] == medium:
            lt.addLast(olderones,artwork)

    sa.sort(olderones,compareYears)
    older = lt.subList(catalog["artists"],-x,x)
    return older

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def compareYears(year1, year2):
    return (year1 < year2)