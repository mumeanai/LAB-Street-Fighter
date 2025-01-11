from partidas import *

def test_lee_partidas(datos):
    print('1. Test de lee_peliculas:')
    print(f'Total registros leídos: {len(datos)}')
    print('Mostrando los tres primeros registros:', *datos[:3], sep ="\n\t" )
    print('########'*10)
    
def test_victoria_mas_rapida(datos):
    print('2. Test victora_mas_rapida')
    print(f'La partida más rápida fue una entre {victoria_mas_rapida(datos)[0]} y {victoria_mas_rapida(datos)[1]} que duró {victoria_mas_rapida(datos)[2]} segundos.')
    print('########'*10)

def test_top_ratio_medio_personajes(datos):
    print('3. Test de top_ratio_medio_personajes')
    print('El top 3 de ratios medios es:', top_ratio_medio_personajes(datos, 3))
    print('########'*10)

def test_enemigo_mas_debil(datos):
    print('4. Test de enemigo_mas_debil')
    print(f'Los enemigos más débiles de Ken son {enemigos_mas_debiles(datos, 'Ken')}')
    print('########'*10)

def test_movimientos_comunes(datos):
    print('5. Test de movimientos_comunes')
    print('Los movimientos repetidos entre Ryu y Ken son:', movimientos_comunes(datos, 'Ryu', 'Ken'))
    print('########'*10)

def test_dia_mas_combo_finish(datos):
    print('6. Test de dia_mas_combo_finish')
    print('El día que más Ultra Combo Finish ha habido es el', dias_mas_combo_finish(datos))

if __name__ == "__main__":
    datos = lee_partidas("data\games.csv")
    test_lee_partidas(datos)
    test_victoria_mas_rapida(datos)
    test_top_ratio_medio_personajes(datos)
    test_enemigo_mas_debil(datos)
    test_movimientos_comunes(datos)
    test_dia_mas_combo_finish(datos)