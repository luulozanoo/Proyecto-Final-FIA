#PARTE 1 - Creación de tablero, entorno y búsqueda guiada y con agentes de búsqueda

import random
from collections import deque

#JUEGO GUIADO 

#---FUNCIONES AUXILIARES---

def creacion_tablero(dim:int)->list[list]:
    """
    Función para crear el tablero con sus elementos correspondientes
    
    :param dim (int): Dimensión del tablero
    :return: list[list] Tablero con todos los elementos añadidos
    """
    tablero_aux = []
    for _ in range(dim):
        fila = []
        for _ in range(dim):
            fila.append("*")
        tablero_aux.append(fila) #Tablero inicializado a *
    coronel_kurtz = 'CK'

    precipicios = 3
    tablero_precipicios = añadir_elementos(dim,'P',precipicios,tablero_aux) #Añadimos los elementos al tablero anterior para guardar el progreso
    tablero_soldado = añadir_elementos(dim,'S!',1,tablero_precipicios)
    tablero_salida = añadir_elementos(dim,'F',1,tablero_soldado) #Denotamos a la salida por F de Final
    tablero_final = añadir_elementos(dim,coronel_kurtz,1,tablero_salida) #Concluimos la creación del tablero
    return tablero_final #Devolvemos el tablero con todos los elementos añadidos

def añadir_elementos(dim:int,tipo_elemento:str,n_obs:int,tablero:list[list])->tuple[list[list],list]:
    """
    Esta función añade los elementos y obstáculos del palacio al tablero
    
    :param dim (int): Dimensión del palacio
    :param tipo_elemento (str): Tipo de elemento
    :param n_obs (int): Cantidad de dicho elemento
    :param tablero (list[list]): Tablero que representa el palacio
    :return: tuple[list[list], list]
    """
    for _ in range(n_obs): #Añadiremos tantos obstáculos de ese tipo como se haya indicado
        pos_fila = random.randint(0,dim-1) #Seleccionamos una posición aleatoria
        pos_columna = random.randint(0,dim-1)
        while (pos_fila == 0 and pos_columna == 0) or tablero[pos_fila][pos_columna] != "*": #Nos aseguramos que no sea la celda de inicio o que haya otro obstáculo en la celda
            pos_fila = random.randint(0,dim-1) #Si no volvemos a escoger la posición
            pos_columna = random.randint(0,dim-1)
        tablero[pos_fila][pos_columna] = tipo_elemento #Colocamos un obstáculo en la posición correspondiente
    return tablero #Devolvemos el tablero con el elemento añadido

def vecinos(fila:int,columna:int,dim:int)->list:
    """
    Esta función encuentra las celdas adyacentes a la que recibe como input
    
    :param fila (int): Fila de la celda
    :param columna (int): Columna de la celda
    :param dim (int): Dimensión del palacio
    :return list: Celdas adyacentes de la habitación
    """
    vecinos = [] #En esta lista guardaremos las adyacentes

    if fila > 0: #Veremos si no está en la fila superior
        vecinos.append((fila-1, columna))

    if fila < dim - 1: #Veremos si no está en la fila inferior
        vecinos.append((fila+1, columna))

    if columna > 0: #Si no está en la primera columna
        vecinos.append((fila, columna-1))

    if columna < dim - 1: #Y por último si no está en la última columna
        vecinos.append((fila, columna+1))
    
    return vecinos #Devolvemos las celdas adyacentes

def obtener_perceptos(tablero:list[list], fila:int, columna:int, grito:bool, dim:int)->list:
    """
    Obtiene los perceptos de la habitación correspondiente
    
    :param tablero (list[list]): Tablero que representa el palacio
    :param fila (int): FIla de la celda
    :param columna (int): Columna de la celda
    :param grito (bool): Indicador de la vida del soldado
    :param dim (int): Dimensión del palacio
    :return list: Lista con los perceptos
    """
    v = vecinos(fila, columna, dim) #Obtenemos los vecinos

    brisa = any(tablero[i][j] == "P" for i,j in v) #Analizamos si en algún vecino hay algún precipicio = True
    ronquido = not grito and any(tablero[i][j] == "S!" for i, j in v) #Vemos si hay grito o no si el soldado está en un vecino
    resplandor = tablero[fila][columna] == "F" or any(tablero[i][j] == "F" for i, j in v) #Vemos si la salida está en la propia celda o en algún vecino

    paredes = [fila == 0, fila == dim-1, columna == 0, columna == dim-1] #Comprobamos estado de las paredes

    return [brisa, ronquido, resplandor, paredes[0], paredes[1], paredes[2], paredes[3], grito] #Devolvemos lista de perceptos

def validacion_celda(fila:int, columna:int, dim:int, tablero:list[list], seguras:list,
                     posible_soldado:list, posible_precipicio:list, posible_salida:list,
                     movs_posibles:list, grito:bool, memoria:list) -> list:
    """
    Obtiene toda la información acerca de la celda
    
    :param fila (int): Fila de la celda
    :param columna (int): Columna de la celda
    :param dim (int): Dimensión del palacio
    :param tablero (list[list]): Tablero que representa el palacio
    :param seguras (list): Lista de celdas seguras
    :param posible_soldado (list): Lista de posiciones posibles para el soldado
    :param posible_precipicio (list): Lista de posiciones posibles para los precipicios
    :param posible_salida (list): Lista de posiciones posibles para la salida
    :param movs_posibles (list): Lista de movimientos posibles
    :param grito (bool): Indicador de vida del soldado
    :param granada (int): ¿Hay granada?
    :param memoria (list): Lista de celdas visitadas
    :return list: Datos necesarios para el movimiento
    """
    celda = (fila, columna)
    
    # OBTENER PERCEPTOS usando la función obtener_perceptos
    perceptos = obtener_perceptos(tablero, fila, columna, grito, dim)
    
    brisa,ronquido,resplandor,pared_arriba,pared_abajo,pared_izq,pared_der,grito = perceptos   
    vecino = vecinos(fila, columna, dim)
    
    #Evaluamos el conocimiento de la celda actual
    percepto_s = [brisa, ronquido, resplandor, pared_arriba,pared_abajo,pared_izq,pared_der,]
    opciones = ['Brisa', 'Ronquido', 'Resplandor', 'Pared arriba', 'Pared abajo', 'Pared izq', 'Pared der']
    
    #Deducciones lógicas del Capitán
    print(f"\nTenemos el siguiente conocimiento acerca de la celda {fila,columna}")
    for i in range(len(percepto_s)):
        print(f"{opciones[i]}: {percepto_s[i]}")

    if celda not in memoria:
        memoria.append(celda) #Si no la hemos visitado ya, la añadimos a visitadas, si no, no volveremos a analizar la misma información varias veces
        if celda not in seguras: #Si la celda no está en seguras (no la hemos analizado aún) la añadimos a la lista
            seguras.append(celda)

        # Lógica para precipicios
        if not brisa: #No recibimos estímulo
            if celda in posible_precipicio: #Si considerábamos la celda peligrosa, ya no lo es
                posible_precipicio.remove(celda)  

        if brisa: #Recibimos estímulo
            print(f'\nUy uy uy... Parece que cerca hay un precipicio... ¡Ojo con las celdas adyacentes!')
            for vec in vecino: #Si los vecinos no están en seguras ni en posible_precipicio los añadimos a la lista de posibles
                if vec not in seguras and vec not in posible_precipicio:
                    posible_precipicio.append(vec)

        # Lógica para soldado (solo si no hubo grito)
        if grito: #Si hubo grito, el soldado ha caído y ya no hay peligro
            print('\n¡El soldado ha caído! Ya no hay peligro de soldados.')
            posible_soldado.clear() #Ya no nos hace falta esta lista
        elif ronquido: #Si no hay grito y recibimos el estímulo
            print(f'\n Uy uy uy... Parece que cerca hay un soldado... ¡Ojo con las celdas adyacentes!')            
            for vec in vecino:#Si los vecinos no están en seguras ni en posible_soldado los añadimos a la lista de posibles
                if vec not in posible_soldado and vec not in seguras:
                    posible_soldado.append(vec)
        else: #Si no recibimos estímulo, si considerábamos la celda peligrosa, ya no lo es
            if celda in posible_soldado: 
                posible_soldado.remove(celda)

        # Lógica para salida
        if resplandor: #Recibimos el estímulo
            for vec in vecino:
                if vec not in seguras and vec not in posible_salida:
                    posible_salida.append(vec)
        if not brisa and not ronquido and not resplandor: #No recibimos ningún estímulo
            print('\n¡Estamos en una celda segura, ni soldados ni precipicios! ')

    #Analicemos los movimientos posibles
    if pared_arriba:
        movs_posibles.remove('W')
    if pared_izq:
        movs_posibles.remove('A')
    if pared_abajo:
        movs_posibles.remove('S')
    if pared_der:
        movs_posibles.remove('D')

    return movs_posibles, seguras, posible_soldado, posible_precipicio, posible_salida

def mostrar_estado_juego(seguras:list, posible_salida:list, posible_soldado:list, posible_precipicio:list, 
                         salida_encontrada:bool, grito:bool,memoria:list,tablero:list[list]) -> None:
    """
    Muestra el estado actual del juego
    
    :param seguras (list): Lista de celdas seguras
    :param posible_soldado (list): Lista de posiciones posibles para el soldado
    :param posible_precipicio (list): Lista de posiciones posibles para los precipicios
    :param posible_salida (list): Lista de posiciones posibles para la salida
    :param salida_encontrada (bool): Indica si se ha encontrado la salida o no
    :param grito (bool): Indicador de la vida del soldado
    :param memoria (list): Lista de celdas visitadas
    :param tablero (list[list]): Tablero que representa el palacio
    :return None
    """
    
    print("\n-----ESTADO ACTUAL DEL JUEGO-----")
    print("\nCeldas visitadas")
    for celda in memoria:
        print(f"· {celda}")
    print(f"\nCeldas seguras ({len(seguras)}):")
    for celda in seguras:
        print(f"  ✓ {celda}")
    
    print(f"\nInformación sobre la salida:")
    if salida_encontrada:
        print("- Ya hemos encontrado la salida. La guardamos para cuando encontremos al Coronel")
    elif not posible_salida:
        print("- No tenemos información sobre la salida")
    else:
        print("- Posibles ubicaciones de la salida:")
        for celda in posible_salida:
            print(f"    · {celda}")
    
    print(f"\nInformación sobre el soldado:")
    if grito:
        print("- Soldado eliminado (grito escuchado)")
    elif not posible_soldado:
        print("- No tenemos información sobre el soldado")
    else:
        if len(posible_soldado) == 1:
            print(f"- INFERENCIA: El soldado está en {posible_soldado[0]}")
            tablero[posible_soldado[0][0]][posible_soldado[0][1]]
        else:
            print(f"- Posibles ubicaciones del soldado ({len(posible_soldado)}):")
            for celda in posible_soldado:
                print(f"    · {celda}")

    
    print(f"\nInformación sobre precipicios:")
    if not posible_precipicio:
        print(" - No tenemos información sobre precipicios")
    elif posible_precipicio:
        if len(posible_precipicio) == 1:
            print(f"- INFERENCIA: Hay un precipicio en {posible_precipicio[0]}")
        else:
            print(f"- Posibles ubicaciones de precipicios ({len(posible_precipicio)}):")
            for celda in posible_precipicio:
                print(f"    · {celda}")

    
def movimiento(pos_fila_actual:int, pos_columna_actual:int, tablero_final:list[list], dim:int, 
               seguras:list, posible_soldado:list, posible_precipicio:list, 
               posible_salida:list, granada:int, grito:bool,
               salida_encontrada:bool, kurtz_encontrado:bool,tablero:list[list],memoria:list)->list:
    """
    Se encarga de todo lo relacionado con los movimientos del Capitán
    por el tablero
    
    :param pos_fila_actual (int): Fila actual
    :param pos_columna_actual (int): Columna actual
    :param tablero_final (list[list]): Tablero que representa el palacio
    :param dim (int): Dimensión del palacio
    :param seguras (list): Lista de celdas seguras
    :param posible_soldado (list): Lista de posiciones posibles para el soldado
    :param posible_precipicio (list): Lista de posiciones posibles para los precipicios
    :param posible_salida (list): Lista de posiciones posibles para la salida
    :param granada (int): ¿Hay granada?
    :param grito (bool): Indicador de vida del soldado
    :param salida_encontrada (bool): Indica si se ha encontrado o no la salida
    :param kurtz_encontrado (bool): Indica si se ha encontrado o no a Kurtz
    :param tablero (list[list]): Tablero visible
    :param memoria (list): Lista de habitaciones visitadas
    :return list: Datos necesarios para el juego
    """
    
    mov_posibles = ['W','A','S','D']
    
    movs_posibles, seguras, posible_soldado, posible_precipicio, posible_salida = validacion_celda(
        pos_fila_actual, pos_columna_actual, dim, tablero_final,
        seguras, posible_soldado, posible_precipicio, posible_salida, 
        mov_posibles, grito,memoria
    )

    # Mostrar estado completo del juego
    mostrar_estado_juego(seguras, posible_salida, posible_soldado, posible_precipicio,
                         salida_encontrada, grito,memoria,tablero)
    
    if granada > 0 and not grito and 'G' not in movs_posibles:
        # Verificar si hay ronquido para activar la granada
        perceptos = obtener_perceptos(tablero_final, pos_fila_actual, pos_columna_actual, grito, dim)
        if perceptos[1]:
            movs_posibles.append('G')
            print("\n¡Granada disponible! (G)")
    
    #Pedimos movimiento por pantalla
    print(f"\nMovimientos disponibles en la celda {pos_fila_actual,pos_columna_actual}: {movs_posibles}")
    movimiento_valido = False
    while not movimiento_valido:
        movimiento_opcion = input('Escoge un movimiento (W/A/S/D/G): ').upper()
        while movimiento_opcion not in movs_posibles:
            print('¡Oh no! Movimiento no válido...Escoge de nuevo')
            movimiento_opcion = input('Escoge un movimiento (W/A/S/D/G): ').upper()

        # Guardar posición actual para limpiar después
        old_fila, old_col = pos_fila_actual, pos_columna_actual
        
        # Procesar movimiento
        if movimiento_opcion == 'W':
            pos_fila_actual -= 1
            movimiento_valido = True
        elif movimiento_opcion == 'S':
            pos_fila_actual += 1
            movimiento_valido = True
        elif movimiento_opcion == 'A':
            pos_columna_actual -= 1
            movimiento_valido = True
        elif movimiento_opcion == 'D':
            pos_columna_actual += 1
            movimiento_valido = True
        elif movimiento_opcion == 'G':
            if granada == 0:
                print("\nUps. Ya no te quedan granadas...")
                continue
            movimiento_valido = True

            #Mostramos celdas disponibles para la granada
            print('\n¡Te muestro las celdas disponibles para tirar la granada!')
            vecino = vecinos(old_fila, old_col, dim)
            for vec in vecino:
                print(f"· {vec}")
            
            #Pedimos ubicación al usuario
            soldado_caido = input("¿A qué celda deseas tirar la granada? Introduce sus coordenadas (fila,columna): ")
            while ',' not in soldado_caido:
                print('Coordenada no válida introduce una coordenada en formato fila,columna')
                soldado_caido = input("¿A qué celda deseas tirar la granada? Introduce sus coordenadas (fila,columna): ")
            idx = soldado_caido.index(",")
            fila_sol = int(soldado_caido[:idx])
            columna_sol = int(soldado_caido[idx+1:])
            
            # Validar coordenadas
            while (fila_sol, columna_sol) not in vecino or not (0 <= fila_sol < dim) or not (0 <= columna_sol < dim):
                print('¡Oh no! Celda no válida...Debe ser adyacente y dentro del tablero.')
                soldado_caido = input("¿A qué celda deseas tirar la granada? Introduce sus coordenadas: ")
                idx = soldado_caido.index(",")
                fila_sol = int(soldado_caido[:idx])
                columna_sol = int(soldado_caido[idx+1:])
            
            granada -= 1
            if tablero_final[fila_sol][columna_sol] == 'S!':
                print(f"¡Bien! Mataste al soldado, ya puedes acceder a esa casilla")
                tablero_final[fila_sol][columna_sol] = "*"
                tablero[fila_sol][columna_sol] = '*'
                grito = True
                posible_soldado.clear()
            else:
                print('¡Oh no! El soldado no estaba ahí... Ya no te quedan granadas')
            continue

    # Limpiar posición anterior
    tablero_final[old_fila][old_col] = "*"
    tablero[old_fila][old_col] = "X"
    
    # Verificar nueva posición
    obstaculo_letal = False
    celda_actual = tablero_final[pos_fila_actual][pos_columna_actual]
    
    if celda_actual == 'P' or (celda_actual == 'S!' and not grito):
        print('¡Oh no! Te has encontrado con un obstáculo letal y has muerto')
        obstaculo_letal = True
    
    return pos_fila_actual, pos_columna_actual, granada, grito, obstaculo_letal, posible_soldado, posible_precipicio, posible_salida

#---FUNCIÓN PRINCIPAL---

def juego_guiado(dim:int)->None:
    """
    Función principal que lleva a cabo toda 
    la ejecución de esta opción
    
    :param dim (int): Dimensión del palacio
    :return None
    """

    print("¡Hola! Soy el Capitán Willard. Acompáñame en esta aventura para encontrar al Coronel Kurtz evitando los obstáculos letales.")
    print("Partimos de la celda (0,0)...\n")

    #Creamos los dos tableros
    tablero_final = creacion_tablero(dim)
    tablero = []
    for _ in range(dim):
        fila = []
        for _ in range(dim):
            fila.append("*")
        tablero.append(fila)
    
    #Inicialamos  y definimos todas las variables y listas
    capitan_willard = 'CW'
    capitan_coronel = capitan_willard

    seguras = [(0,0)]
    posible_soldado = []
    posible_precipicio = []
    posible_salida = []
    memoria = []
    granada = 1

    obstaculo_letal = False
    grito = False
    salida_encontrada = False
    salida_pos = None
    kurtz_encontrado = False

    #Colocamos al Capitán Willard en su posición inicial
    pos_fila_actual = 0
    pos_columna_actual = 0
    tablero_final[pos_fila_actual][pos_columna_actual] = capitan_willard
    tablero[pos_fila_actual][pos_columna_actual] = capitan_willard

    # FASE 1: BUSCAR A KURTZ
    while not obstaculo_letal and not kurtz_encontrado:
        #Imprimimos el tablero visible para mayor visibilidad
        for fila in tablero:
            print(fila)

        resultado = movimiento(pos_fila_actual, pos_columna_actual, tablero_final, dim, seguras,
                              posible_soldado, posible_precipicio, posible_salida,
                              granada, grito, salida_encontrada, kurtz_encontrado,tablero,memoria)
        
        pos_fila_actual, pos_columna_actual, granada, grito, obstaculo_letal, posible_soldado, posible_precipicio, posible_salida = resultado
        
        if obstaculo_letal:
            break
            
        # Verificar qué hay en la nueva posición
        celda_actual = tablero_final[pos_fila_actual][pos_columna_actual]
        
        #Comprobamos si hemos encontrado la salida a kurtz o las dos
        if celda_actual == 'F' and not salida_encontrada:
            print("¡Muy bien! Has encontrado la casilla de salida. Guardamos la posición para cuando encontremos al Coronel")
            salida_encontrada = True
            salida_pos = (pos_fila_actual, pos_columna_actual)
            tablero[pos_fila_actual][pos_columna_actual] = 'F'
        
        elif celda_actual == 'CK' and not kurtz_encontrado:
            print(f"¡Hemos encontrado al Coronel Kurtz! Se hallaba escondido en la celda {pos_fila_actual, pos_columna_actual}")
            kurtz_encontrado = True
            capitan_coronel = 'CWCK'
        
        # Marcar posición actual
        tablero_final[pos_fila_actual][pos_columna_actual] = capitan_coronel
        tablero[pos_fila_actual][pos_columna_actual] = capitan_coronel
        print(f"Bien, estamos en la celda {pos_fila_actual, pos_columna_actual}")

    # FASE 2: BUSCAR SALIDA (si encontramos a Kurtz)
    if not obstaculo_letal and kurtz_encontrado: 
        if salida_encontrada:
            print(f"¡Perfecto! Ya sabemos que la salida está en {salida_pos}")
            print("Ahora debemos dirigirnos allí para escapar.")
        else:
            print("Todavía no sabemos dónde está la salida. Debemos buscarla.")
        
        # Buscar salida si no la hemos encontrado
        while not obstaculo_letal and not salida_encontrada:
            #Imprimimos el tablero visible para mayor visibilidad
            for fila in tablero:
                print(fila)

            resultado = movimiento(pos_fila_actual, pos_columna_actual, tablero_final, dim, seguras,
                              posible_soldado, posible_precipicio, posible_salida,
                              granada, grito, salida_encontrada, kurtz_encontrado,tablero,memoria)
            
            pos_fila_actual, pos_columna_actual, granada, grito, obstaculo_letal, posible_soldado, posible_precipicio, posible_salida = resultado
            
            if obstaculo_letal:
                break
                
            # Verificar si encontramos la salida en esta celda
            celda_actual = tablero_final[pos_fila_actual][pos_columna_actual]
            
            if celda_actual == 'F' and not salida_encontrada:
                salida_encontrada = True
                salida_pos = (pos_fila_actual, pos_columna_actual)
                print(f"¡Encontramos la salida! Está en {salida_pos}")
                break
            
            tablero_final[pos_fila_actual][pos_columna_actual] = capitan_coronel
        
        # FASE 3: IR A LA SALIDA (si la conocemos)
        if not obstaculo_letal and salida_encontrada:
            print(f"\n¡VAMOS A LA SALIDA EN {salida_pos}!")
            if (pos_fila_actual,pos_columna_actual) == salida_pos:
                salir = True
            else:
                salir = False
                while not salir:
                    resultado = movimiento(pos_fila_actual, pos_columna_actual, tablero_final, dim, seguras,
                                    posible_soldado, posible_precipicio, posible_salida,
                                    granada, grito, salida_encontrada, kurtz_encontrado,tablero,memoria)
                
                    pos_fila_actual, pos_columna_actual, granada, grito, obstaculo_letal, posible_soldado, posible_precipicio, posible_salida = resultado
                    
                    if obstaculo_letal:
                        break
                        
                    # Verificar si encontramos la salida en esta celda
                    celda_actual = tablero_final[pos_fila_actual][pos_columna_actual]
                    if (pos_fila_actual,pos_columna_actual) == salida_pos:
                        salir = True
                        break

            print("¡Lo lograste! Conseguimos escapar y convencer al Coronel Kurtz. ¡Muchas gracias por la ayuda!")



#JUEGO CON AGENTES

#---FUNCIONES AUXILIARES---

def bfs_camino(fila:int, columna:int, memoria:list, seguras:list, dim:int, tablero_final:list[list], grito:bool):
    """
    Se encargará de encontrar 
    
    :param fila (int): Fila de la celda
    :param columna (int): Columna de la celda
    :param memoria (list): Lista de celdas visitadas
    :param seguras (list): Lista de celdas seguras
    :param dim (int): Dimensión del palacio
    :param tablero_final (list[list]): Tablero que representa el palacio
    :param grito (bool): Indicador de vida del soldado
    :return list: Camino
    :return None
    """
    cola = deque() #Creamos la estructura de cola
    cola.append(((fila, columna), [])) #Añadimos la celda
    estados_explorados = {(fila, columna)} #Creamos un set de estados explorados

    while cola:
        (fil, col), camino = cola.popleft()

        # OBJETIVO: Una celda segura que NO hayamos visitado nunca
        if (fil, col) in seguras and (fil, col) not in memoria:
            return camino 

        for vec in vecinos(fil, col, dim):
            transitable = False
            if vec in seguras:
                transitable = True
            if transitable:
                if tablero_final[vec[0]][vec[1]] == 'P': 
                    transitable = False
                if not grito and tablero_final[vec[0]][vec[1]] == 'S!': 
                    transitable = False
            
            if transitable and vec not in estados_explorados:
                estados_explorados.add(vec)
                cola.append((vec, camino + [vec]))
    return None

def bfs_salida(fila:int,columna:int, salida_pos:tuple, seguras:list, dim:int, tablero_final: list[list], grito: bool):
    """
    Se encarga de encontrar un camino a la salida y ver 
    si es posible llegar hasta la misma sin encontrarse
    con obstáculos
    
    :param fila (int): Fila de la celda
    :param columna (int): Columna de la celda
    :param salida_pos (tuple): Objetivo
    :param seguras (list): Lista de celdas seguras
    :param dim (int): Dimensión del palacio
    :param tablero_final (list[list]): Tablero que representa el palacio
    :param grito (bool): Indicador de vida del soldado
    :return camino Si encontramos la salida
    :return None 
    """
    cola = deque() #Mismo proceso que bfs_camino
    cola.append(((fila,columna), []))
    estados_explorados = set([(fila,columna)])

    while cola:
        (fil, col), camino = cola.popleft()

        if (fil, col) == salida_pos: #Nos interesa ver si llegamos a la salida
            return camino
        
        for vec in vecinos(fil, col, dim):
            # Verificar si el vecino es transitable
            transitable = True
            
            # Verificar si está en seguras o si es la salida misma
            if vec != salida_pos and vec not in seguras:
                transitable = False
            
            # Verificar obstáculos letales
            if transitable:
                if tablero_final[vec[0]][vec[1]] == 'P':
                    transitable = False
                if not grito and tablero_final[vec[0]][vec[1]] == 'S!':
                    transitable = False
            
            if transitable and vec not in estados_explorados:
                estados_explorados.add(vec)
                cola.append((vec, camino + [vec]))

    return None

def razonamiento_agente(fila: int, col: int, dim: int, seguras: list, 
                        posible_soldado: list, posible_precipicio: list, posible_salida: list, 
                        grito: bool, tablero:list[list]):
    """
    Docstring for razonamiento_agente
    
    :param fila (int): Fila de la celda
    :param col (int): Fila de la columna
    :param dim (int): Dimensión del palacio
    :param seguras (list): Lista de celdas seguras
    :param posible_soldado (list): Lista de posiciones posibles para el soldado
    :param posible_precipicio (list): Lista de posiciones posibles para los precipicios
    :param posible_salida (list): Lista de posiciones posibles para la salida
    :param grito (bool): Indicador de vida del soldado
    :param tablero (list[list]): Tablero que representa el palacio
    :return list Datos necesarios para la ejecución del juego
    """
    celda = (fila, col)
    
    # Obtener perceptos
    vecino = vecinos(fila, col, dim)
    perceptos = obtener_perceptos(tablero, fila, col, grito, dim)
    brisa,ronquido,resplandor,pared_arriba,pared_abajo,pared_izq,pared_der,grito = perceptos 
    
    # Lógica simple para actualizar seguras
    if not brisa and not ronquido:
        for vec in vecino:
            if vec not in seguras:
                seguras.append(vec)
        if celda not in seguras:
            seguras.append(celda)
    
    # Lógica para precipicios
    if brisa:
        for vec in vecino:
            if vec not in seguras and vec not in posible_precipicio:
                posible_precipicio.append(vec)
    
    # Lógica para soldado
    if not grito:
        if not ronquido:
            # Eliminar vecinos de posibles soldados
            if celda in posible_soldado: 
                posible_soldado.remove(celda)
        elif ronquido:
            # Añadir vecinos como posibles soldados
            for vec in vecino:
                if vec not in seguras and vec not in posible_soldado:
                    posible_soldado.append(vec)
    
    # Lógica para salida
    if resplandor:
        for vec in vecino:
            if vec not in seguras and vec not in posible_salida:
                posible_salida.append(vec)
    
    return seguras, posible_soldado, posible_precipicio, posible_salida, [brisa, ronquido, resplandor]

def movimiento_agente(pos_fila_actual: int, pos_columna_actual: int, tablero_final: list[list], 
                      dim: int, seguras: list, posible_soldado: list, posible_precipicio: list, 
                      posible_salida: list, granada: int, grito: bool, memoria: list, tablero: list[list]):
    """
    Se encarga del movimiento del agente
    
    :param pos_fila_actual (int): Fila de la celda
    :param pos_columna_actual (int): Columna de la celda
    :param tablero_final (list[list]): Tablero que representa el palacio
    :param dim (int): Dimensión del palacio
    :param seguras (list): Lista de celdas seguras
    :param posible_soldado (list): Lista de posiciones posibles para el soldado
    :param posible_precipicio (list): Lista de posiciones posibles para los precipicios
    :param posible_salida (list): Lista de posiciones posibles para la salida
    :param granada (int): Indica si hay o no granada
    :param grito (bool): Indicador de vida del soldado
    :param memoria (list): Lista de celdas visitadas
    :param tablero (list[list]): Tablero visible
    :return Datos necesarios para completar la ejecución del juego
    """
    celda = (pos_fila_actual, pos_columna_actual)

    #¿Hemos visitado ya esta celda?
    if celda not in memoria:
        memoria.append(celda)

    seguras, posible_soldado, posible_precipicio, posible_salida, perceptos = razonamiento_agente(
        pos_fila_actual, pos_columna_actual,dim, seguras, 
        posible_soldado, posible_precipicio, posible_salida, grito, tablero_final, 
    )

    #Comprobamos si la posición actual coincide con la salida
    if tablero_final[pos_fila_actual][pos_columna_actual] == 'F':
        #Actualizamos el tablero_visible
        tablero[pos_fila_actual][pos_columna_actual] = "F"
        # Marcamos que ya sabemos dónde está, pero NO hacemos return si no tenemos a Kurtz

    #Comprobamos si la posición actual coincide con el Coronel
    if tablero_final[pos_fila_actual][pos_columna_actual] == 'CK':
        return pos_fila_actual, pos_columna_actual, granada, grito, False, True, seguras, posible_soldado, posible_precipicio, posible_salida
        
    seguras_temporal = [s for s in seguras if s != (pos_fila_actual, pos_columna_actual) or s not in memoria]

    #Buscamos el camino 
    camino = bfs_camino(pos_fila_actual, pos_columna_actual, memoria, seguras_temporal, dim, tablero_final, grito)
    #Si hay camino, avanzamos
    if camino:
        siguiente = camino[0]  # Primer paso del camino
        print(f"Moviendo de {celda} a {siguiente}")
        #Actualizamos valores
        tablero[pos_fila_actual][pos_columna_actual] = "X"
        pos_fila_actual, pos_columna_actual = siguiente

        #Comprobación estado de la celda
        celda_actual = tablero_final[pos_fila_actual][pos_columna_actual]
        if celda_actual == 'P' or (celda_actual == 'S!' and not grito):
            print(f'¡Oh no! Te has encontrado con un obstáculo letal en {pos_fila_actual,pos_columna_actual} y has muerto')
            return pos_fila_actual, pos_columna_actual, granada, grito, True, False, seguras, posible_soldado, posible_precipicio, posible_salida

        #Si es segura, actualizamos el movimiento
        tablero[pos_fila_actual][pos_columna_actual] = "CW"
        return pos_fila_actual, pos_columna_actual, granada, grito, False, False, seguras, posible_soldado, posible_precipicio, posible_salida

    #Si no, exploramos
    else:
        print("No hay más celdas seguras para explorar")
        #Intentamos explorar una celda no segura
        for vec_fil, vec_col in vecinos(pos_fila_actual, pos_columna_actual, dim):
            vec = (vec_fil, vec_col)
            if vec not in memoria:
                print(f"\nIntentando explorar celda no segura: {vec}")
                # Limpiar posición anterior
                tablero[pos_fila_actual][pos_columna_actual] = "X"
                # Mover
                pos_fila_actual, pos_columna_actual = vec_fil, vec_col
                # Actualizar tablero visible
                tablero[pos_fila_actual][pos_columna_actual] = "CW"
                #Comprobación de que hay en la celda nueva
                celda_actual = tablero_final[pos_fila_actual][pos_columna_actual]
                if celda_actual == 'P' or (celda_actual == 'S!' and not grito):
                    print(f'¡Oh no! Te has encontrado con un obstáculo letal en {pos_fila_actual,pos_columna_actual} y has muerto')
                    return pos_fila_actual, pos_columna_actual, granada, grito, True, False, seguras, posible_soldado, posible_precipicio, posible_salida
                
                return pos_fila_actual, pos_columna_actual, granada, grito, False, False, seguras, posible_soldado, posible_precipicio, posible_salida
        
        print("Completamente atascado. Fin del juego.")
        return pos_fila_actual, pos_columna_actual, granada, grito, True, False, seguras, posible_soldado, posible_precipicio, posible_salida

def obtener_ruta_optima(inicio: tuple, fin: tuple, seguras: list, dim: int, tablero_final: list[list], grito: bool):
    """
    Obtiene la ruta óptima para llegar hasta Kurzt desde el origen
    Se emplea una vez hemos encontrado a Kurtz

    :param inicio (tuple): Posición de partida
    :param fin (tuple): Posición de Kurtz
    :param seguras (list): Lista de celdas seguras
    :param dim (int): Dimensión del palacio
    :param tablero_final (list[list]): Tablero que representa el palacio
    :param grito (bool): Indicador de vida del soldado
    """
    cola = deque() #Misma manera que en bfs_camino o bfs_salida
    cola.append((inicio, [inicio]))
    estados_explorados = {inicio}

    while cola:
        (fil, col), camino = cola.popleft() # Estructura FIFO

        if (fil, col) == fin:
            return camino # Retorna el camino hasta Kurtz

        for vec in vecinos(fil, col, dim):
            # Verificamos que sea una celda que Willard ya determinó como segura
            if vec in seguras:
                #Verificación extra
                if not (tablero_final[vec[0]][vec[1]] == 'P' or (tablero_final[vec[0]][vec[1]] == 'S!' and not grito)) and vec not in estados_explorados:
                    estados_explorados.add(vec)
                    cola.append((vec, camino + [vec]))
    return None

#---FUNCIÓN PRINCIPAL---

def juego_con_agente_bfs(dim:int):
    """
    Función principal que lleva a cabo toda 
    la ejecución de esta opción
    
    :param dim (int): Dimensión del palacio
    :return None
    """

    print("¡Hola! Soy el Capitán Willard. Acompáñame en esta aventura para encontrar al Coronel Kurtz evitando los obstáculos letales.")
    print("Partimos de la celda (0,0)...\n")

    #Creación de los dos tableros
    tablero_final = creacion_tablero(dim)
    tablero = []
    for _ in range(dim):
        fila = []
        for _ in range(dim):
            fila.append("*")
        tablero.append(fila)
    
    #Inicializamos y definimos todas las variables y listas
    capitan_willard = 'CW'
    capitan_coronel = capitan_willard

    seguras = [(0,0)]
    posible_soldado = []
    posible_precipicio = []
    posible_salida = []
    memoria = []
    granada = 1


    obstaculo_letal = False
    grito = False
    salida_encontrada = False
    salida_pos = None
    kurtz_encontrado = False
    mision_completada = False
    pos_kurtz = None


    #Colocamos al Capitán Willard en su posición inicial
    pos_fila_actual = 0
    pos_columna_actual = 0
    tablero_final[pos_fila_actual][pos_columna_actual] = capitan_willard
    tablero[pos_fila_actual][pos_columna_actual] = capitan_willard
    memoria.append((pos_fila_actual, pos_columna_actual))

    #FASE 1: BUSCAR A KURTZ
    while not obstaculo_letal and not kurtz_encontrado and not mision_completada:
        #Imprimimos el tablero visible para mayor visibilidad
        for fila in tablero:
            print(fila)

        resultado = movimiento_agente(pos_fila_actual, pos_columna_actual, tablero_final, 
                      dim, seguras, posible_soldado, posible_precipicio, 
                      posible_salida, granada, grito, memoria, tablero)
        
        pos_fila_actual, pos_columna_actual, granada, grito, obstaculo_letal, objetivo_alcanzado, seguras, posible_soldado, posible_precipicio, posible_salida = resultado

        if obstaculo_letal:
            break

        #Verificar si hemos encontrado a Kurtz
        if objetivo_alcanzado:
            if tablero_final[pos_fila_actual][pos_columna_actual] == 'CK':
                print(f"¡Hemos encontrado al Coronel Kurtz en {pos_fila_actual, pos_columna_actual}!")
                kurtz_encontrado = True
                capitan_coronel = 'CWCK'
                tablero_final[pos_fila_actual][pos_columna_actual] = capitan_coronel
                tablero[pos_fila_actual][pos_columna_actual] = capitan_coronel

                #Guardamos la posición de Kurtz para encontrar el camino óptimo
                pos_kurtz = (pos_fila_actual, pos_columna_actual) 
            
                ruta_total = obtener_ruta_optima((0,0), pos_kurtz, seguras, dim, tablero_final, grito)
                print('------------------------------------------------------------------')
                print(f"Ruta óptima para encontrar al Coronel desde la posición (0,0):")
                print(ruta_total) 
                print('------------------------------------------------------------------')
                break
            
            #Si encontramos la salida, la almacenamos en salida_pos y actualizamos el tablero_visible
            elif tablero_final[pos_fila_actual][pos_columna_actual] == 'F':
                print(f"Hemos encontrado la salida en {pos_fila_actual, pos_columna_actual}, pero primero debemos encontrar al Coronel")
                salida_encontrada = True
                salida_pos = (pos_fila_actual, pos_columna_actual)
                tablero[pos_fila_actual][pos_columna_actual] = "F"
                #Añadimos la posición a la memoria si no está para no volver a visitar la celda
                if (pos_fila_actual, pos_columna_actual) not in memoria:
                    memoria.append((pos_fila_actual, pos_columna_actual))
                continue 
                    
    #FASE 2: BUSCAR LA SALIDA (si encontramos a Kurtz)
    if not obstaculo_letal and kurtz_encontrado:
        if salida_encontrada:
            print(f"\n¡VAMOS A LA SALIDA EN {salida_pos}!")
        else:
            print("Ya tenemos al Coronel, ahora debemos buscar la salida...")

        #Buscar la salida si no la hemos encontrado
        while not obstaculo_letal and not salida_encontrada and not mision_completada:
        #Imprimimos el tablero visible para mayor visibilidad
            for fila in tablero:
                print(fila)

            resultado = movimiento_agente(pos_fila_actual, pos_columna_actual, tablero_final, 
                        dim, seguras, posible_soldado, posible_precipicio, 
                        posible_salida, granada, grito, memoria, tablero)
                
            pos_fila_actual, pos_columna_actual, granada, grito, obstaculo_letal, objetivo_alcanzado, seguras, posible_soldado, posible_precipicio, posible_salida = resultado

            #Verificar si encontramos la salida en esta celda
            if tablero_final[pos_fila_actual][pos_columna_actual] == 'F':
                print(f"¡Hemos encontrado la salida en {pos_fila_actual,pos_columna_actual}!")
                salida_encontrada = True
                salida_pos = (pos_fila_actual,pos_columna_actual)
                break

        #FASE 3: IR A LA SALIDA (si la conocemos)
        if not obstaculo_letal and salida_encontrada:
            print(f"\n¡VAMOS A LA SALIDA EN {salida_pos}!")
            ruta_total = obtener_ruta_optima(pos_kurtz,salida_pos, seguras, dim, tablero_final, grito)
            print('------------------------------------------------------------------')
            print(f"Ruta óptima para encontrar la salida desde la posición {pos_kurtz}:")
            print(ruta_total) 
            print('------------------------------------------------------------------')
            mision_completada = True
            
    if mision_completada:
        print("¡Lo lograste! Conseguimos escapar y convencer al Coronel Kurtz. ¡Muchas gracias por la ayuda!") 