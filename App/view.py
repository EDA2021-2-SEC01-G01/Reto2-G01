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
  file = input('Ingresa 1 para cargar los archivos grande: (Por defecto se utilizan los archivos de artistas y obras pequeños)')

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


def printMenu():
  print("Bienvenido")
  print("1- Cargar información en el catálogo")
  print("2- Listar cronológicamente los artistas")
  print("Otro- Salir")

catalog = initCatalog()

"""
Menu principal
"""
while True:
  printMenu()
  inputs = input('Seleccione una opción para continuar\n')
  if int(inputs[0]) == 1:
    print("Cargando información de los archivos ....")
    catalog = loadData(catalog)
  elif int(inputs[0]) == 2:
    sortArtistsByYears(catalog)
  else:
    sys.exit(0)
sys.exit(0)
