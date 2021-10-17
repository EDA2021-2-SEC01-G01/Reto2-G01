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
from datetime import datetime as dt
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
    'artists': None,
    'artworks': None,
    'artworks': None,
  }
  

  catalog['artists'] = mp.newMap(15500, maptype='CHAINING', loadfactor=1.5)

  catalog['artworks'] = mp.newMap(151000, maptype='CHAINING', loadfactor=2.0)

  catalog['artworksList'] = lt.newList('ARRAY_LIST')

  catalog['artistsByYear'] = mp.newMap(15500, maptype='CHAINING', loadfactor=1.5)

  catalog['artworksByDate'] = mp.newMap(151000, maptype='CHAINING', loadfactor=2.0)

  return catalog

# Añadir informacion al catalogo

def addArtist(catalog, artist):
  mp.put(catalog['artists'], artist['ConstituentID'], artist)

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
  lt.addLast(catalog['artworksList'], artwork)
  mp.put(catalog['artworks'], artwork['ObjectID'], artwork)

  if artwork['DateAcquired']:
    dateObject = dt.strptime(artwork['DateAcquired'], '%Y-%m-%d')
  else:
    dateObject = 'Unknown'

  dateStringCode = dateObject

  existingDate = mp.contains(catalog['artworksByDate'], dateStringCode)

  if existingDate:
    entry = mp.get(catalog['artworksByDate'], dateStringCode)
    date = me.getValue(entry)
    lt.addLast(date['artworks'], artwork)
  else:
    date = newDate(dateStringCode)
    lt.addLast(date['artworks'], artwork)
    mp.put(catalog['artworksByDate'], dateStringCode, date)

# Funciones para creacion de datos

def newYear(year):
  year = {
    'year': year,
    'artists': None
  }

  year['artists'] = lt.newList('ARRAY_LIST')

  return year


def newDate(date):
  date = {
    'date': date,
    'artworks': lt.newList('ARRAY_LIST')
  }

  return date

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


def artworksBeetweenDate(catalog, begin, end):
  artworks = lt.newList('ARRAY_LIST')
  purchased = 0
  nArtists = 0 

  artworksByDate = catalog['artworksByDate']

  keys = mp.keySet(artworksByDate)

  for key in lt.iterator(keys):
    if key != 'Unknown':
      if dt.strptime(begin, '%Y-%m-%d') <= key and key <= dt.strptime(end, '%Y-%m-%d'):
        entry = mp.get(artworksByDate, key)
        value = me.getValue(entry)['artworks']

        for atwork in lt.iterator(value):
          if 'purchase' in atwork['CreditLine'].lower():
            purchased += 1
          artistsIds = atwork['ConstituentID'][1:-1].replace(' ', '').split(',')
          atwork['ConstituentID'] = lt.newList('ARRAY_LIST')
          for id in artistsIds:
            if mp.contains(catalog['artists'], id):
              nArtists += 1
              lt.addLast(atwork['ConstituentID'], me.getValue(mp.get(catalog['artists'], id))['DisplayName'])

          lt.addLast(artworks, atwork)

  sa.sort(artworks, compareDates)
  return {'artworks': artworks, 'purchased': purchased, 'nArtists': nArtists}

# Funciones de ordenamiento

def compareDates(artwork1, artwork2):
  return dt.strptime(artwork1['DateAcquired'], '%Y-%m-%d') < dt.strptime(artwork2['DateAcquired'], '%Y-%m-%d')

def compareNames(artist1, artist2):
  return artist1['DisplayName'] < artist2['DisplayName']
