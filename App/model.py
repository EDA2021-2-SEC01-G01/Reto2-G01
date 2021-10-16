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

def newCatalog():
  catalog = {
    'artists': None,
    'artistsIds': None,
    'artworks': None,
    'artworksIds': None,
  }
  
  catalog['artists'] = lt.newList('ARRAY_LIST')

  catalog['artistsIds'] = mp.newMap(15500, maptype='CHAINING', loadfactor=1.5)

  catalog['artworks'] = lt.newList('ARRAY_LIST')

  catalog['artworksIds'] = mp.newMap(151000, maptype='CHAINING', loadfactor=2.0)

  catalog['artistsByYear'] = mp.newMap(15500, maptype='CHAINING', loadfactor=1.5)

  return catalog

# Añadir informacion al catalogo

def addArtist(catalog, artist):
  lt.addLast(catalog['artists'], artist)
  mp.put(catalog['artistsIds'], artist['ConstituentID'], artist)

  existingYear = mp.contains(catalog['artistsByYear'], artist['BeginDate'])

  if existingYear:
    entry = mp.get(catalog['artistsByYear'], artist['BeginDate'])
    year = me.getValue(entry)
    lt.addLast(year['artists'], artist)
  else:
    year = newYear(artist['BeginDate'])
    lt.addLast(year['artists'], artist)
    mp.put(catalog['artistsByYear'], artist['BeginDate'], year)


def addArtwork(catalog, artwork):
  lt.addLast(catalog['artworks'], artwork)
  mp.put(catalog['artworksIds'], artwork['ObjectID'], artwork)

# Funciones para creacion de datos

def newYear(year):
  year = {
    'year': year,
    'artists': None
  }

  year['artists'] = lt.newList('ARRAY_LIST')

  return year

# Funciones de consulta

def artistsBeetweenYears(catalog, begin, end):
  artists = lt.newList('ARRAY_LIST')

  currentYear = int(begin)

  artistsByYear = catalog['artistsByYear']

  while currentYear <= int(end):
    entry = mp.get(artistsByYear, str(currentYear))

    if entry:
      value = me.getValue(entry)
      sa.sort(value['artists'], compareNames)
      for artist in lt.iterator(value['artists']):
        lt.addLast(artists, artist)
    
    currentYear += 1

  return artists

# Funciones utilizadas para comparar elementos dentro de una lista



# Funciones de ordenamiento

def compareNames(artist1, artist2):
  return artist1['DisplayName'] < artist2['DisplayName']
