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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo


def newCatalog():
  return model.newCatalog()


# Funciones para la carga de datos

def loadData(catalog, artistsFile, artworksFile):
  artistsFileF = cf.data_dir + artistsFile
  artworksFileF = cf.data_dir + artworksFile

  inputArtist = csv.DictReader(open(artistsFileF, encoding='utf-8'))
  inputArtworks = csv.DictReader(open(artworksFileF, encoding='utf-8'))

  for artist in inputArtist:
    model.addArtist(catalog, artist)

  for artwork in inputArtworks:
    model.addArtwork(catalog, artwork)

  return catalog

# Funciones de ordenamiento

def sortMediums(artworks):
  return model.topMediumsByArtworks(artworks)

# Funciones de consulta sobre el catálogo

def calculatePrice(catalog, department):
  return model.calculatePrice(catalog, department)


def getSortedArtistsBetweenYears(catalog, beginDate, endDate):
  artistList = model.artistsBeetweenYears(catalog, beginDate, endDate)
  return artistList


def getSortedArtworksBetweenDates(catalog, beginDate, endDate):
  artworksInfo = model.artworksBeetweenDate(catalog, beginDate, endDate)
  return (artworksInfo['artworks'], artworksInfo['purchased'], artworksInfo['nArtists'])


def getArtworksFromArtist(catalog, name):
  id = model.artistIdByName(catalog, name)

  artworks = model.artworksByArtist(catalog, id)

  sortedMediums = sortMediums(artworks)

  return {'artworks': artworks, 'mediums': sortedMediums}


def artistId(catalog, name):
  return model.artistIdByName(catalog, name)


def getListOfNames(catalog, artwork):
  listFromStr = artwork['ConstituentID'][1:-1].replace(' ', '').split(',')

  namesList = []

  for id in listFromStr:
    namesList.append(model.getNameFromId(catalog, id))

  return namesList


def getArtworksFromArtistByMediums(artworks, medium):
  return model.getArtworksByMedium(artworks, medium)


def getNationsByArtworks(catalog):
  return model.getSortedNationsByArtworks(catalog)
  