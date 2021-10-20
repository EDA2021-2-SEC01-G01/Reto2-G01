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

from math import cos
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
  catalog = {}

  catalog['artists'] = mp.newMap(15500, maptype='CHAINING', loadfactor=1.5)

  catalog['artistsIdsByName'] = mp.newMap(15500, maptype='PROBING', loadfactor=0.5)

  catalog['artworks'] = mp.newMap(151000, maptype='CHAINING', loadfactor=2.0)

  catalog['artworksList'] = lt.newList('ARRAY_LIST')

  catalog['artistsByYear'] = mp.newMap(15500, maptype='CHAINING', loadfactor=1.5)

  catalog['artworksByDate'] = mp.newMap(151000, maptype='CHAINING', loadfactor=2.0)

  catalog['artworksByArtist'] = mp.newMap(151000, maptype='CHAINING', loadfactor=2.0)

  catalog['artworksByNationality'] = mp.newMap(151000, maptype='CHAINING', loadfactor=2.0)

  catalog['artworksByDepartment'] = mp.newMap(151000, maptype='CHAINING', loadfactor=2.0)

  catalog['pricesOfArtworks'] = mp.newMap(151000, maptype='CHAINING', loadfactor=2.0)

  return catalog

# Añadir informacion al catalogo

def addArtist(catalog, artist):
  mp.put(catalog['artists'], artist['ConstituentID'], artist)
  mp.put(catalog['artistsIdsByName'], artist['DisplayName'], artist['ConstituentID'])

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

  # Artworks by date

  if artwork['DateAcquired']:
    dateObject = numberFromDate(artwork['DateAcquired'])
  else:
    dateObject = 0

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

  # Artworks by artist

  artistsList = artwork['ConstituentID'][1:-1].replace(' ', '').split(',')

  for artist in artistsList:
    existingArtist = mp.contains(catalog['artworksByArtist'], artist)

    if existingArtist:
      entry = mp.get(catalog['artworksByArtist'], artist)
      artistValue = me.getValue(entry)
      lt.addLast(artistValue['artworks'], artwork)
    else:
      artistValue = newArtist(artist)
      lt.addLast(artistValue['artworks'], artwork)
      mp.put(catalog['artworksByArtist'], artist, artistValue)

  # Artorks by nationality

  for id in artistsList:
    artistEntry = mp.get(catalog['artists'], id)
    artist = me.getValue(artistEntry)
    existingNation = mp.contains(catalog['artworksByNationality'], artist['Nationality'] or 'Nationality unknown')

    if existingNation:
      entry = mp.get(catalog['artworksByNationality'], artist['Nationality'] or 'Nationality unknown')
      value = me.getValue(entry)
      lt.addLast(value['artworks'], artwork)
    else:
      nationValue = newNation(artist['Nationality'] or 'Nationality unknown')
      lt.addLast(nationValue['artworks'], artwork)
      mp.put(catalog['artworksByNationality'], artist['Nationality'] or 'Nationality unknown', nationValue)
  
  #Artworks by department
  
  if artwork["Department"] == "":
    artwork["Department"] = "Unknown"

  existDepartment = mp.contains(catalog["artworksByDepartment"], artwork["Department"])

  if existDepartment:
    entry = mp.get(catalog["artworksByDepartment"], artwork["Department"])
    artworks = me.getValue(entry)
    lt.addLast(artworks["artworks"], artwork)
  else:
    entry = newDepartment(artwork["Department"])
    lt.addLast(entry["artworks"], artwork)
    mp.put(catalog["artworksByDepartment"], artwork["Department"], entry)


# Funciones para creacion de datos

def newDepartment(department):
  department = {
    "department": department,
    "artworks": lt.newList("ARRAY_LIST")
  }

  return department


def numberFromDate(date):
  return int(date.replace('-', ''))


def newNation(nation):
  nation = {
    'nation': nation,
    'artworks': lt.newList('ARRAY_LIST')
  }

  return nation


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

def newArtist(artist):
  artist = {
    'artist': artist,
    'artworks': lt.newList('ARRAY_LIST'),
  }

  return artist

# Funciones de consulta

def calculatePrice(catalog,department):
  artworks = mp.get(catalog["artworksByDepartment"], department)
  artworks = me.getValue(artworks)
  info = {}
  aproximateWeight = 0
  aproximateCost = 0
  size = lt.size(artworks["artworks"])

  for artwork in lt.iterator(artworks["artworks"]):
    if artwork["Weight (kg)"] != "":
      aproximateWeight += float(artwork["Weight (kg)"].replace(" ", ""))
    price = getPrices(artwork)
    price = round(price,3)
    artwork["TransCost (USD)"] = price
    aproximateCost += price
  
  info["totalCost"] = aproximateCost
  info["totalWeight"] = aproximateWeight
  info["size"] = size
  info["5MostExpensive"] = mostExpensive(artworks["artworks"])
  info["5Older"] = oldest(artworks["artworks"])

  return info


def getPrices(artwork):
  weight = artwork['Weight (kg)'].replace(' ', '')
  height = artwork['Height (cm)'].replace(' ', '')
  width = artwork['Width (cm)'].replace(' ', '')
  length = artwork['Length (cm)'].replace(' ', '')

  valueKgM2M3 = 0

  if (weight != ''):
    weight = float(weight)
    if weight * 72 > valueKgM2M3:
      valueKgM2M3 = weight * 72

  if height != '' and width != '' and length != '':
    m3 = (float(height) * float(width) * float(length))/10000
    if m3 * 72 > valueKgM2M3:
      valueKgM2M3 = m3 * 72
  
  elif height != '' and width != '':
    m2 = (float(height) * float(width)) / 10000
    if m2 * 72 > valueKgM2M3:
      valueKgM2M3 = m2 * 72
  
  elif height != '' and length != '':
    m2 = (float(height) * float(length)) / 10000
    if m2 * 72 > valueKgM2M3:
      valueKgM2M3 = m2 * 72
  
  elif width != '' and length != '':
    m2 = (float(width) * float(length)) / 10000
    if m2 * 72 > valueKgM2M3:
      valueKgM2M3 = m2 * 72
  
  if valueKgM2M3 == 0:
    valueKgM2M3 = 48

  return valueKgM2M3
    
def mostExpensive(artworks):
  sa.sort(artworks,comparePrice)
  return lt.subList(artworks,1,5)
  

def oldest(artwoks):
  sa.sort(artwoks,compareDates2)
  return lt.subList(artwoks,1,5)

def getNameFromId(catalog, id):
  return me.getValue(mp.get(catalog['artists'], id))['DisplayName']


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

  interationDate = numberFromDate(begin)

  while numberFromDate(begin) <= interationDate and interationDate <= numberFromDate(end):
    if mp.contains(artworksByDate, interationDate):
      entry = mp.get(artworksByDate, interationDate)
      value = me.getValue(entry)['artworks']

      for artwork in lt.iterator(value):
        if 'purchase' in artwork['CreditLine'].lower():
          purchased += 1
        artistsIds = artwork['ConstituentID'][1:-1].replace(' ', '').split(',')
        artwork['ConstituentID'] = lt.newList('ARRAY_LIST')
        for id in artistsIds:
          nArtists += 1
          lt.addLast(artwork['ConstituentID'], me.getValue(mp.get(catalog['artists'], id))['DisplayName'])

        lt.addLast(artworks, artwork)

    interationDate += 1

  sa.sort(artworks, compareDates)
  return {'artworks': artworks, 'purchased': purchased, 'nArtists': nArtists}


def artistIdByName(catalog, name):
  entry = mp.get(catalog['artistsIdsByName'], name)
  if not entry:
    return None
  value = me.getValue(entry)
  return value 


def artworksByArtist(catalog, artistId):
  entry = mp.get(catalog['artworksByArtist'], artistId)
  return me.getValue(entry)['artworks']


def topMediumsByArtworks(artworks):
  mediums = {}
  mediumsList = lt.newList('ARRAY_LIST')

  for artwork in lt.iterator(artworks):
    exists = mediums.get(artwork['Medium'], False)
    if exists:
      medium = mediums.get(artwork['Medium'])
      medium['count'] += 1
    else:
      medium = {
        'medium': artwork['Medium'],
        'count': 1,
      }
      mediums[artwork['Medium']] = medium

  for key in mediums:
    lt.addLast(mediumsList, mediums[key])

  sa.sort(mediumsList, compareCount)
  return mediumsList


def getArtworksByMedium(artworks, medium):
  final = lt.newList('ARRAY_LIST')

  for artwork in lt.iterator(artworks):
    if artwork['Medium'] == medium:
      lt.addLast(final, artwork)

  return final


def getSortedNationsByArtworks(catalog):
  keys = mp.keySet(catalog['artworksByNationality'])
  nations = lt.newList()

  for key in lt.iterator(keys):
    entry = mp.get(catalog['artworksByNationality'], key)
    value = me.getValue(entry)['artworks']
    lt.addLast(nations, {'nation': key, 'count': lt.size(value)})

  sa.sort(nations, compareCount)

  return {'nations': nations, 'artworks': me.getValue(mp.get(catalog['artworksByNationality'], lt.firstElement(nations)['nation']))}

# Funciones de ordenamiento

def compareDates(artwork1, artwork2):
  return numberFromDate(artwork1['DateAcquired']) < numberFromDate(artwork2['DateAcquired'])

def compareNames(artist1, artist2):
  return artist1['DisplayName'] < artist2['DisplayName']

def compareCount(elem1, elem2):
  return elem1['count'] > elem2['count']

def comparePrice(artwork1, artwork2):
  return artwork1["TransCost (USD)"] > artwork2["TransCost (USD)"]

def compareDates2(artwork1,artwork2):
  if artwork1["Date"] == "":
      artwork1["Date"] = "2020"
  if artwork2["Date"] == "":
      artwork2["Date"] = "2020"
  return artwork1["Date"] < artwork2["Date"]