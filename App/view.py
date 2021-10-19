"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def initCatalog():
  """
  Inicializa el catalogo de libros
  """
  return controller.newCatalog()

def loadData(catalog):
  file = input('Ingresa 1 para cargar los archivos grande: (Por defecto se utilizan los archivos de artistas y obras pequeños): ')

  if file == '':
    artistas = 'Artists-utf8-small.csv'
    obras = 'Artworks-utf8-small.csv'
  elif file == '1':
    artistas = 'Artists-utf8-large.csv'
    obras = 'Artworks-utf8-large.csv'
  else:
    artistas = 'Artists-utf8-small.csv'
    obras = 'Artworks-utf8-small.csv'

  return controller.loadData(catalog, artistas, obras) 

# REQ. 1

def sortArtistsByYears(catalog):
  beginYear = input('Ingresa el año de incio: ')
  endYear = input('Ingresa el año final: ')

  artists = controller.getSortedArtistsBetweenYears(catalog, beginYear, endYear)

  firstThree = lt.subList(artists, 1, 3)
  lastThree = lt.subList(artists, lt.size(artists)-3, 3)

  print('\n-----------------------------------------------------------------')

  print('\n There are', lt.size(artists), 'artists born between', beginYear, 'and', endYear)
  print('\n The first and last 3 artists in range are...')

  print('\n-----------------------------------------------------------------')

  for year in lt.iterator(firstThree):
    print('\n  ConstituentID:', year['ConstituentID'])
    print('\n  DisplayName:', (year['DisplayName'] or 'Unknown'))
    print('\n  BeginDate:', year['BeginDate'])
    print('\n  Nationality:', (year['Nationality'] or 'Unknown'))
    print('\n  Gender:', (year['Gender'] or 'Unknown'))
    print('\n  ArtistBio:', (year['ArtistBio'] or 'Unknown'))
    print('\n  Wiki QID:', (year['Wiki QID'] or 'Unknown'))
    print('\n  ULAN:', (year['ULAN'] or 'Unknown'))
    print('\n-----------------------------------------------------------------')

  print('\n-----------------------------------------------------------------')
  for year in lt.iterator(lastThree):
    print('\n  ConstituentID:', year['ConstituentID'])
    print('\n  DisplayName:', (year['DisplayName'] or 'Unknown'))
    print('\n  BeginDate:', year['BeginDate'])
    print('\n  Nationality:', (year['Nationality'] or 'Unknown'))
    print('\n  Gender:', (year['Gender'] or 'Unknown'))
    print('\n  ArtistBio:', (year['ArtistBio'] or 'Unknown'))
    print('\n  Wiki QID:', (year['Wiki QID'] or 'Unknown'))
    print('\n  ULAN:', (year['ULAN'] or 'Unknown'))
    print('\n-----------------------------------------------------------------')

# REQ. 2

def sortArtworksByDates(catalog):
  beginYear = input('Ingresa la fecha de incio con un formato YYYY-mm-dd (Ej: 1920-06-8): ')
  endYear = input('Ingresa la fecha final con un formato YYYY-mm-dd (Ej: 1920-06-8): ')

  artworksInfo = controller.getSortedArtworksBetweenDates(catalog, beginYear, endYear)
  artworks = artworksInfo[0]

  firstThree = lt.subList(artworks, 1, 3)
  lastThree = lt.subList(artworks, lt.size(artworks)-3, 3)

  print('\n-----------------------------------------------------------------')

  print('\n There are', lt.size(artworks), 'artworks acquired between', beginYear, 'and', endYear)
  print('\n With', artworksInfo[2], 'different artists and purchased', artworksInfo[1], 'of them.')
  print('\n The first and last 3 artists in range are...')

  print('\n-----------------------------------------------------------------')

  for artwork in lt.iterator(firstThree):
    print('\n  ObjectID:', artwork['ObjectID'])
    print('\n  Title:', (artwork['Title'] or 'Unknown'))
    print('\n  ArtistsNames:')
    for artist in lt.iterator(artwork['ConstituentID']):
      print('\n \t * ', artist)
    print('\n  Medium:', (artwork['Medium'] or 'Unknown'))
    print('\n  Dimensions:', (artwork['Dimensions'] or 'Unknown'))
    print('\n  Date:', (artwork['Date'] or 'Unknown'))
    print('\n  DateAcquired:', (artwork['DateAcquired'] or 'Unknown'))
    print('\n  URL:', (artwork['URL'] or 'Unknown'))
    print('\n-----------------------------------------------------------------')

  print('\n-----------------------------------------------------------------')
  for artwork in lt.iterator(lastThree):
    print('\n  ObjectID:', artwork['ObjectID'])
    print('\n  Title:', (artwork['Title'] or 'Unknown'))
    print('\n  ArtistsNames:')
    for artist in lt.iterator(artwork['ConstituentID']):
      print('\n \t * ', artist)
    print('\n  Medium:', (artwork['Medium'] or 'Unknown'))
    print('\n  Dimensions:', (artwork['Dimensions'] or 'Unknown'))
    print('\n  Date:', (artwork['Date'] or 'Unknown'))
    print('\n  DateAcquired:', (artwork['DateAcquired'] or 'Unknown'))
    print('\n  URL:', (artwork['URL'] or 'Unknown'))
    print('\n-----------------------------------------------------------------')

# REQ. 3

def getMediumsAndArtworks(catalog):
  name = input('Igrese el nombre del artista: ')

  id = controller.artistId(catalog, name)

  mediumsAndArtworks = controller.getArtworksFromArtist(catalog, name)

  firstMedium = lt.firstElement(mediumsAndArtworks['mediums'])

  artwoksToReturn = controller.getArtworksFromArtistByMediums(mediumsAndArtworks['artworks'], firstMedium['medium'])

  print(name, 'with MoMA ID', id, 'has', lt.size(mediumsAndArtworks['artworks']), 'pieces in his/her name at the museum.')
  print('There are', lt.size(mediumsAndArtworks['mediums']), 'different mediums/techniques in his/her work.')

  print('\nHer/His top 5 Medium/Technique are: ')

  for medium in lt.iterator(lt.subList(mediumsAndArtworks['mediums'], 1, 5)):
    print('\nMediumName:', medium['medium'])
    print('\nCount:', medium['count'])
    print('\n-------------------------')

  print('\n\nHis/Her most used Medium/Technique is:', firstMedium['medium'], 'with', firstMedium['count'], 'pieces.')
  print('A sample of 3', firstMedium['medium'], 'from the collection are:')
  print('\n--------------------------------------')

  for artwork in lt.iterator(lt.subList(artwoksToReturn, 1, 3)):
    print(' ObjectID:', artwork['ObjectID'])
    print(' Title:', artwork['Title'])
    print(' Medium:', artwork['Medium'])
    print(' Date:', (artwork['Date'] or 'Unknown'))
    print(' Dimensions:', artwork['Dimensions'])
    print(' DateAcquired:', artwork['DateAcquired'])
    print(' Department:', artwork['Department'])
    print(' Classification:', artwork['Classification'])
    print(' URL:', (artwork['URL'] or 'Unknown'))
    print('\n-----------------------------------')

# REQ. 4

def getNationsByArtworks(catalog):
  info = controller.getNationsByArtworks(catalog)

  print('Nationality | Count')
  for nation in lt.iterator(lt.subList(info['nations'], 1, 10)):
    print('\n', nation['nation'] + ':', nation['count'])
    print('\n---------------------------------')

  firstElement = lt.firstElement(info['nations'])
  print('The TOP nationality in the museum is:', firstElement['nation'], 'with', firstElement['count'], 'unique pieces.')
  print('The first and last 3 objects in', firstElement['nation'], 'artwork list are:')

  for artwork in lt.iterator(lt.subList(info['artworks']['artworks'], 1, 3)):
    print('\n')
    print('ObjectID:', artwork['ObjectID'])
    print('Title:', artwork['Title'])
    print('ArtistsNames:')
    for name in controller.getListOfNames(catalog, artwork):
      print('\t*', name)
    print('\nMedium:', artwork['Medium'])
    print('Date:', artwork['Date'])
    print('Dimensions:', artwork['Dimensions'])
    print('Department:', artwork['Department'])
    print('Classification:', artwork['Classification'])
    print('URL:', artwork['URL'])
    print('\n-------------------------')


  print('-------------------------')

  for artwork in lt.iterator(lt.subList(info['artworks']['artworks'], lt.size(info['artworks']['artworks']) - 3, 3)):
    print('\n')
    print('ObjectID:', artwork['ObjectID'])
    print('Title:', artwork['Title'])
    print('ArtistsNames:')
    for name in controller.getListOfNames(catalog, artwork):
      print('\t*', name)
    print('\nMedium:', artwork['Medium'])
    print('Date:', artwork['Date'])
    print('Dimensions:', artwork['Dimensions'])
    print('Department:', artwork['Department'])
    print('Classification:', artwork['Classification'])
    print('URL:', artwork['URL'])
    print('\n-------------------------')


def printMenu():
  print("Bienvenido")
  print("1- Cargar información en el catálogo")
  print("2- Listar cronológicamente los artistas")
  print("3- Listar cronológicamente las adquisiciones")
  print("4- Clasificar las obras de un artista por técnica")
  print("5- Clasificar las obras por nacionalidad de sus creadores")
  print("Otro- Salir")

catalog = None

"""
Menu principal
"""
while True:
  printMenu()
  inputs = input('Seleccione una opción para continuar\n')
  if int(inputs[0]) == 1:
    print("Cargando información de los archivos ....")
    catalog = initCatalog()
    catalog = loadData(catalog)
    print(catalog)
  elif int(inputs[0]) == 2:
    sortArtistsByYears(catalog)
  elif int(inputs[0]) == 3:
    sortArtworksByDates(catalog)
  elif int(inputs[0]) == 4:
    getMediumsAndArtworks(catalog)
  elif int(inputs[0]) == 5:
    getNationsByArtworks(catalog)
  else:
    sys.exit(0)
sys.exit(0)
