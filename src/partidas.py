from collections import defaultdict
import csv
from typing import Counter, NamedTuple
from datetime import datetime 

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

def lee_partidas(ruta:str) -> list[Partida]:
    '''
    Recibe una cadena de texto con la ruta de un fichero csv, y devuelve una 
    lista de tuplas Partida con la información contenida en el fichero. 
    '''
    res = []
    with open(ruta, encoding='utf-8') as f:
        lector = csv.reader(f, delimiter= ',')
        next(lector)
        for pj1, pj2, puntuacion, tiempo, fecha_hora, golpes_pj1, golpes_pj2, movimiento_final, combo_finish, ganador in lector:
            puntuacion = int(puntuacion)
            tiempo = float(tiempo)
            fecha_hora = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")
            golpes_pj1 = parsea_lista(golpes_pj1)
            golpes_pj2 = parsea_lista(golpes_pj2)
            combo_finish = combo_finish == "1"
            tupla = Partida(pj1, pj2, puntuacion, tiempo, fecha_hora, golpes_pj1, golpes_pj2, movimiento_final, combo_finish, ganador)
            res.append(tupla)
        return res
    
def parsea_lista(cadena:str)-> list[str]:
    sin_corchetes = cadena.replace('[', '').replace(']', '')
    res = []
    for trozo in sin_corchetes.split(","):
        res.append(trozo.split())
    return res
    
    
def victoria_mas_rapida(partidas:list[Partida])-> tuple[str, str, float]:
    '''
    Recibe una lista de tuplas de tipo Partida y devuelve una tupla compuesta por
    los dos personajes y el tiempo de aquella partida que haya sido la más rápida
    en acabar. Implemente este ejercicio usando solo bucles. No se puntuará el 
    ejercicio si se usan funciones de Python como min, max o sorted.(1 punto)
    '''
    menor_tiempo = None
    personaje1 = None
    personaje2 = None
    for p in partidas:
        if menor_tiempo == None or menor_tiempo > p.tiempo:
            menor_tiempo = p.tiempo
            personaje1 = p.pj1
            personaje2 = p.pj2
    return (personaje1, personaje2, menor_tiempo)            

def top_ratio_medio_personajes(partidas:list[Partida], n:int) -> list[str]:
    '''
    Recibe una lista de tuplas de tipo Partida y un número entero n, y devuelve 
    una lista con los n nombres de los personajes cuyas ratios de eficacia media
    sean las más bajas. La ratio de eficacia se calcula dividiendo la puntuación 
    entre el tiempo de aquellas partidas que haya ganado el personaje. 
    Es decir, si Ryu ha ganado 3 combates, su ratio media se calcula con los 
    cocientes puntuacion/tiempo de dichos combates. (1.5 puntos)
    '''
    personaje_ratios = defaultdict(list)
    for p in partidas:
        personaje_ratios[p.ganador].append(p.puntuacion/p.tiempo)

        # if p.pj1 == p.ganador:
        #     personaje_ratios[p.pj1].append(p.puntuacion/p.tiempo)
        # elif p.pj2 == p.ganador:
        #     personaje_ratios[p.pj1].append(p.puntuacion/p.tiempo)

    personaje_media_ratios = defaultdict(int)
    for personaje, ratio in personaje_ratios.items():
        personaje_media_ratios[personaje] = sum(ratio)/len(ratio)
        
    ordenado = sorted(personaje_media_ratios.items(), key = lambda t:t[1])[:n]
    
    return [tupla[0] for tupla in ordenado]

def enemigos_mas_debiles(partidas:list[Partida], personaje:str)-> tuple[list[str], int]:
    '''
    Recibe una lista de tuplas de tipo Partida y una cadena de texto personaje. 
    El objetivo de esta función es calcular los oponentes frente a los que el 
    personaje ha ganado más veces. Para ello, esta función devuelve una tupla 
    compuesta por una lista de nombres y el número de victorias, de aquellos 
    contrincantes contra los cuales el número de victorias haya sido el mayor. 
    Es decir, si introducimos como parámetro el valor Ken y este ha ganado 2 
    veces contra Blanka, 2 contra Ryu y 1 contra Bison, la función deberá 
    devolver (['Blanka', 'Ryu'], 2). (2 puntos)
    '''
    res = []
    for p in partidas: 
        if personaje == p.ganador and p.pj1 == p.ganador:
            res.append(p.pj2)
        elif personaje == p.ganador and p.pj2 == p.ganador:
            res.append(p.pj1)
    
    victorias_por_oponente = Counter(res)
    
    mayor_num_victorias = max(victorias_por_oponente.values())
    
    mas_frecuente = [oponente for oponente, num in victorias_por_oponente.items() if num == mayor_num_victorias]
    
    return (mas_frecuente, mayor_num_victorias)


def movimientos_comunes(partidas:list[Partida], personaje1:str, personaje2:str)-> list[str]:
    '''
    Recibe una lista de tuplas de tipo Partida y dos cadenas de texto personaje1 
    y personaje2, y devuelve una lista con los nombres de aquellos movimientos 
    que se repitan entre personaje1 y personaje2. Tenga solo en cuenta los 
    movimientos que aparecen listados en los campos golpes_pj1 y golpes_pj2. 
    (2 puntos)
    '''
    golpes_personaje1=set()
    golpes_personaje2=set()
    
    for p in partidas:
        if personaje1 == p.pj1:
            golpes_personaje1.union(set(p.golpes_pj1))
        elif personaje1 == p.pj2:
            golpes_personaje1.union(set(p.golpes_pj2))  

        if personaje2 == p.pj1:
            golpes_personaje2.union(set(p.golpes_pj1)) 
        elif personaje2 == p.pj2:
            golpes_personaje2.union(set(p.golpes_pj2))
    
    golpes_comunes = golpes_personaje1.intersection(golpes_personaje2)
    return golpes_comunes  
             

def dias_mas_combo_finish(partidas:list[Partida])-> str:
    '''
    Recibe una lista de tuplas de tipo Partida, y devuelve el día de la semana 
    en el que hayan acabado más partidas con un combo finish. Use el método 
    weekday() de datetime para obtener el día de la semana en formato numérico, 
    siendo 0 el lunes y 6 el domingo. Para hacer la traducción del número al 
    nombre, utilice una función auxiliar. (1.5 punto)
    '''
    dias_combo_finish = []
    for p in partidas:
        if p.combo_finish:
            dias_combo_finish.append(p.fecha_hora)
            
    dias_semana = [dia_semana(fecha)for fecha in dias_combo_finish]
    
    frecuencia= Counter(dias_semana)
    dia_mas_frecuente = frecuencia.most_common(1)[0][0]
    return dia_mas_frecuente

def dia_semana(fecha:datetime) -> str:
    num_dia = fecha.weekday()
    if num_dia == 0:
        return 'Lunes'
    if num_dia == 1:
        return 'Martes'
    if num_dia == 2:
        return 'Miércoles'
    if num_dia == 3:
        return 'Jueves'
    if num_dia == 4:
        return 'Viernes'
    if num_dia == 5:
        return 'Sábado'
    if num_dia == 6:
        return 'Domingo'
    
    