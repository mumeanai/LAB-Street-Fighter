from collections import Counter, defaultdict
from datetime import datetime
from typing import NamedTuple
import csv
 
Partida = NamedTuple("Partida", [
    ("pj1", str),
    ("pj2", str),
    ("puntuacion", int),
    ("tiempo", float),
    ("fecha_hora", datetime),
    ("golpes_pj1", list[str]),
    ("golpes_pj2", list[str]),
    ("movimiento_final", str),
    ("combo_finish", bool),
    ("ganador", str),
    ])

#cadena.replace("lo que quiero quietar", "lo que quiero poner en su lugar")

def parsea_lista(cadena:str)-> list[str]:
    res = []
    for trozo in cadena.split(","):     #.split()   separa la cadena, como una lista de cadenas
        res.append(trozo.strip())       #.strip()   
    return res


def lee_partidas(ruta:str)-> list[Partida]:
    '''
    recibe una cadena de texto con la ruta de un fichero csv, 
    y devuelve una lista de tuplas Pelicula con la información 
    contenida en el fichero. Utilice 
    datetime.strptime(cadena, "%d/%m/%Y").date() para parsear 
    las fechas. (1 punto)
    '''
    res = []
    
    with open(ruta, encoding = 'utf-8') as f:
        lector = csv.reader(f, delimiter = ',')
        next(lector)
        for pj1, pj2, puntuacion, tiempo, fecha_hora, golpes_pj1, golpes_pj2, movimiento_final, combo_finish, ganador in lector:
            pj1 =  str(pj1)
            pj2 = str(pj2)
            puntuacion = int(puntuacion)
            tiempo = float(tiempo)
            fecha_hora = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")
            golpes_pj1 = parsea_lista(golpes_pj1)
            golpes_pj2 = parsea_lista(golpes_pj2)
            movimiento_final = str(movimiento_final)
            combo_finish = bool(combo_finish)
            ganador = str(ganador)
            
            tupla = Partida(pj1, pj2, puntuacion, tiempo, fecha_hora, golpes_pj1, golpes_pj2, movimiento_final, combo_finish, ganador)
            res.append(tupla)
            
        return res
    
    
def victoria_mas_rapida(partidas):
    '''
    recibe una lista de tuplas de tipo Partida y devuelve una tupla 
    compuesta por los dos personajes y el tiempo de aquella partida que 
    haya sido la más rápida en acabar. Implemente este ejercicio usando 
    solo bucles. No se puntuará el ejercicio si se usan funciones de Python 
    como min, max o sorted.(1 punto)
    '''
    partida_mas_rapida = None
    for p in partidas:
        if  partida_mas_rapida == None or p.tiempo < partida_mas_rapida.tiempo:
            partida_mas_rapida = p
    tupla = (partida_mas_rapida.pj1, partida_mas_rapida.pj2, partida_mas_rapida.tiempo)
    return tupla

def top_ratio_medio_personajes(partidas: list[Partida], n:int) -> list[str]:
    '''
    recibe una lista de tuplas de tipo Partida y un número entero n, y 
    devuelve una lista con los n nombres de los personajes cuyas ratios 
    de eficacia media sean las más bajas. La ratio de eficacia se calcula
    dividiendo la puntuación entre el tiempo de aquellas partidas que haya
    ganado el personaje. Es decir, si Ryu ha ganado 3 combates, su ratio 
    media se calcula con los cocientes puntuacion/tiempo de dichos combates.
    (1.5 puntos)
    '''
    
    ratio_por_personaje =  defaultdict()
    res  =[]
    for p in partidas:
        ratio = p.puntuacion/p.tiempo
        res.append(ratio)
        ratio_por_personaje[p.ganador] = res
        
    for ganador, ratio in ratio_por_personaje.items():
        ratio_por_personaje[ganador] = sum(ratio)/len(ratio)
        
    ordenado = sorted(ratio_por_personaje, key = lambda r:r[1])
    return ordenado[:n]

def enemigos_mas_debiles(partidas:list[Partida], personaje:str)-> tuple[list[str], int]:
    '''
    recibe una lista de tuplas de tipo Partida y una cadena de texto personaje.
    El objetivo de esta función es calcular los oponentes frente a los que el 
    personaje ha ganado más veces. Para ello, esta función devuelve una tupla
    compuesta por una lista de nombres y el número de victorias, de aquellos 
    contrincantes contra los cuales el número de victorias haya sido el mayor.
    Es decir, si introducimos como parámetro el valor Ken y este ha ganado 2 
    veces contra Blanka, 2 contra Ryu y 1 contra Bison, la función deberá 
    devolver (['Blanka', 'Ryu'], 2). (2 puntos)
    '''
    
    contrincantes = []
    for p in partidas:
        if p.ganador == personaje and p.ganador == p.pj1:
           contrincantes.append(p.pj2) 
        elif p.ganador == personaje and p.ganador == p.pj2:
            contrincantes.append(p.pj1)
    
    num_victorias = Counter (c for c in contrincantes)
    mayor_num_victorias = num_victorias.most_common(1)
    return (contrincantes, mayor_num_victorias)
      
            
