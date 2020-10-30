import math as ma
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain

def dessiner_carte_mercator(m, scale=0.2):
    # draw a shaded-relief image
    m.shadedrelief(scale=scale)
    
    # latitudes et longitudes retournes dans un dictionnaire
    latitudes = m.drawparallels(np.linspace(-90, 90, 13))
    longitudes = m.drawmeridians(np.linspace(-180, 180, 13))

    # keys contain the plt.Line2D instances
    paralleles = chain(*(tup[1][0] for tup in latitudes.items()))
    meridiens = chain(*(tup[1][0] for tup in longitudes.items()))
    all_lines = chain(paralleles, meridiens)
    
    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')

def demanderLatitude(p):
    return float(input("Veuillez entre la Latitude de votre point "+p+" : "))

def demanderLongitude(p):
    return float(input("Veuillez entre la Longitude de votre point "+p+" : "))

def calculerDistance(lg1, lg2, lt1, lt2):
    
    return ma.acos(ma.sin(lt1)*ma.sin(lt2) + ma.cos(lt1)*ma.cos(lt2)*ma.cos(lg1-lg2))

def calculerCap (lg1, lg2, lt1, lt2, d):
    
    v = (ma.sin(lt2) - ma.sin(lt1) * ma.cos(d))/(ma.cos(lt1) * ma.sin(d))
    x = ma.acos(v)
    if (lg1 < lg2):
        return x
    else:
        return 2*ma.pi - x

def calculerLongitudePrime(lg1,lt1, angle, l):
    
    return lg1 + l * Q * ma.sin(angle)/ ma.cos(lt1)

def calculerLatitudePrime(lt1, angle, l):
    
    return lt1 + ma.cos(angle) * l * Q




Q = ma.pi / (1.852*60*180)

longAdeg = 2.33333333333
longBdeg = -73.968565
latAdeg  = 48.86666666666666
latBdeg = 40.779897

longA = ma.radians(longAdeg)
longB = ma.radians(longBdeg)
latA  = ma.radians(latAdeg)
latB  = ma.radians(latBdeg)


distanceInitiale = calculerDistance(longA, longB, latA, latB)
print("La distance entre les villes A et B est " + str(distanceInitiale * 6371) + " kilomètres")

intervalle = 100

capInitial = calculerCap(longA, longB, latA, latB, distanceInitiale)

longPrime = calculerLongitudePrime(longA, latA, capInitial,intervalle)
latPrime  = calculerLatitudePrime(latA, capInitial, intervalle)

distance = calculerDistance(longPrime, longB, latPrime, latB)

while (distance*6371 >= intervalle):
    cap = calculerCap(longPrime, longB, latPrime, latB, distance)
    longPrime = calculerLongitudePrime(longPrime, latPrime, cap, intervalle)
    latPrime  = calculerLatitudePrime(latPrime, cap, intervalle)
    plt.plot(ma.degrees(longPrime), ma.degrees(latPrime) , 'ok', markersize=1)
    distance = calculerDistance(longPrime, longB, latPrime, latB)

