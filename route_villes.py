import math as ma
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
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
    if ((lg1 < lg2) & (abs(ma.degrees(lg1)-ma.degrees(lg2)) < 180)) | \
        ((lg1 > lg2) & (abs(ma.degrees(lg1)-ma.degrees(lg2)) > 180)) :
        return x
    else:
        return 2*ma.pi - x


def calculerLongitudePrime(lg1,lt1, angle, l):
    
    return lg1 + l * Q * ma.sin(angle)/ ma.cos(lt1)


def calculerLatitudePrime(lt1, angle, l):
    
    return lt1 + ma.cos(angle) * l * Q

def tracerLoxodromie(lg1, lg2, lt1, lt2):
    
    if (abs(lg1-lg2) < 180):
        plt.plot([lg1, lg2], [lt1, lt2] , 'r-')
    else:
        if (lg1>lg2):
            plt.plot([lg1, lg2+360], [lt1, lt2] , 'r-')
            plt.plot([lg1-360, lg2], [lt1,lt2] , 'r-')
        else:
            plt.plot([lg1, lg2-360], [lt1, lt2] , 'r-')
            plt.plot([lg1+360, lg2], [lt1, lt2] , 'r-')

def donnerInformations(lg1, lg2):
    if(lg1 == lg2):
        print("\n\nOrthodromie et loxodromie se confondent dans la droite noire")
    else:
        print("\n\nL'orthodromie est la courbe verte")
        print("La loxodromie est la droite rouge")

fig = plt.figure(figsize=(8, 6), edgecolor='w')
m = Basemap(projection='cyl', resolution=None,
            llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, )


Q = ma.pi / (1.852*60*180)

longAdeg = demanderLongitude("A")
latAdeg  = demanderLatitude("A")
longBdeg = demanderLongitude("B")
latBdeg = demanderLatitude("B") 

longA = ma.radians(longAdeg)
longB = ma.radians(longBdeg)
latA  = ma.radians(latAdeg)
latB  = ma.radians(latBdeg)

distanceInitiale = calculerDistance(longA, longB, latA, latB)
print("\nLa distance entre les villes A et B est " + str(round(distanceInitiale * 6371)) + " kilomètres")

if (longAdeg == longBdeg):
    plt.plot([longAdeg, longBdeg], [latAdeg, latBdeg] , 'k-')
    
else:
    
    plt.plot(longAdeg, latAdeg , 'ok', markersize=5)
    plt.plot(longBdeg, latBdeg , 'ok', markersize=5)
    
    
    intervalle = 100
    
    
    capInitial = calculerCap(longA, longB, latA, latB, distanceInitiale)
    
    longPrime = calculerLongitudePrime(longA, latA, capInitial,intervalle)
    latPrime  = calculerLatitudePrime(latA, capInitial, intervalle)
    
    
    plt.plot([longAdeg, ma.degrees(longPrime)], [latAdeg, ma.degrees(latPrime)] , 'g-')
    
    distance = calculerDistance(longPrime, longB, latPrime, latB)
    
    
    while (distance*6371 >= intervalle):
    
        if(ma.degrees(longPrime)<(-180)):
            longPrime += ma.radians(360)
            
        if(ma.degrees(longPrime)>(180)):
            longPrime -= ma.radians(360) 
            
        longPrec = longPrime
        latPrec = latPrime
        cap = calculerCap(longPrime, longB, latPrime, latB, distance)
        
        longPrime = calculerLongitudePrime(longPrime, latPrime, cap, intervalle)
        latPrime  = calculerLatitudePrime(latPrime, cap, intervalle)
        
        plt.plot([ma.degrees(longPrec), ma.degrees(longPrime)], [ma.degrees(latPrec), ma.degrees(latPrime)] , 'g-')
        distance = calculerDistance(longPrime, longB, latPrime, latB)
    
    plt.plot([ma.degrees(longPrime), longBdeg], [ma.degrees(latPrime), latBdeg] , 'g-')   
    tracerLoxodromie(longAdeg, longBdeg, latAdeg, latBdeg)


donnerInformations(longAdeg, longBdeg)
dessiner_carte_mercator(m)
