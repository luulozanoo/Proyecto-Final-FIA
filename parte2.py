#PARTE 2 - Creación de tablero, entorno y búsqueda guiada y con agentes bayesianos con probabilidades

import random
import heapq
import matplotlib.pyplot as plt
import seaborn as sns

#JUEGO GUIADO

#---FUNCIONES AUXILIARES---

def creacion_tablero(dim:int)->list[list]:
    """
    Se encarga de crear el tablero con sus trampas
    
    :param dim (int): Dimensión del templo
    :return list[list]: Tablero con elementos
    """
    tablero_aux = []
    for _ in range(dim):
        fila = []
        for _ in range(dim):
            fila.append([])
        tablero_aux.append(fila)

    coronel_kurtz = 'CK'
    tab_fuego = añadir_trampas(dim,'F',tablero_aux)
    tab_pinchos = añadir_trampas(dim,'P',tab_fuego)
    tab_dardos = añadir_trampas(dim,'D',tab_pinchos)

    tab_soldado = añadir_resto_elementos(dim,'M',tab_dardos)
    tab_salida = añadir_resto_elementos(dim,'S',tab_soldado)
    tab_final = añadir_resto_elementos(dim,coronel_kurtz,tab_salida)

    return tab_final

def añadir_trampas(dim:int,tipo_elemento:str,tablero:list[list])->list[list]:
    """
    Se encarga de colocar las trampas
    
    :param dim (int): Dimensión del templo
    :param tipo_elemento (str): Tipo de trampa a colocar
    :param tablero (list[list]): Tablero anterior (guardar progreso)
    :return list[list]: Tablero con nueva trampa
    """
    pos_fila = random.randint(0,dim-1)
    pos_columna = random.randint(0,dim-1)
    while (pos_fila == 0 and pos_columna == 0): #Nos aseguramos que no sea la celda de inicio
        pos_fila = random.randint(0,dim-1)
        pos_columna = random.randint(0,dim-1)
    tablero[pos_fila][pos_columna].append(tipo_elemento) #Colocamos un obstáculo en la posición correspondiente
    return tablero

def añadir_resto_elementos(dim:int,tipo_elemento:str,tablero:list[list])->list[list]:
    """
    Se encarga de añadir el resto de elementos al tablero
    
    :param dim (int): Dimensión del templo
    :param tipo_elemento (str): Tipo de elemento a colocar
    :param tablero (list[list]): Tablero anterior (guardar progreso)
    :return list[list]: Tablero con elemento colocado
    """
    pos_fila = random.randint(0,dim-1)
    pos_columna = random.randint(0,dim-1)
    while (pos_fila == 0 and pos_columna == 0) or any(trampa in tablero[pos_fila][pos_columna] for trampa in ['F', 'P', 'D']): #Nos aseguramos que no sea la celda de inicio o que haya otro obstáculo en la celda
        pos_fila = random.randint(0,dim-1)
        pos_columna = random.randint(0,dim-1)  
    tablero[pos_fila][pos_columna].append(tipo_elemento) #Colocamos un obstáculo en la posición correspondiente
    return tablero

def vecinos(fila:int,columna:int,dim:int)->list:
    """
    Esta función encuentra las celdas adyacentes a la que recibe como input
    
    :param fila (int): Fila de la celda
    :param columna (int): Columna de la celda
    :param dim (int): Dimensión del templo
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

def obtener_perceptos(tablero:list[list], fila:int, columna:int, grito:bool, dim:int):
    """
    Obtiene los perceptos de la habitación correspondiente
    
    :param tablero (list[list]): Tablero que representa el templo
    :param fila (int): FIla de la celda
    :param columna (int): Columna de la celda
    :param grito (bool): Indicador de la vida del soldado
    :param dim (int): Dimensión del templo
    :return list: Lista con los perceptos
    """
    v = vecinos(fila, columna, dim) + [(fila, columna)]

    eF = any("F" in tablero[i][j] for i,j in v)
    eP = any("P" in tablero[i][j] for i, j in v)
    eD = any("D" in tablero[i][j] for i, j in v)
    
    # El soldado solo se oye si está vivo (not grito)
    eM = not grito and any("M" in tablero[i][j] for i, j in v)
    
    # La salida se siente si está en los vecinos o en la propia celda
    eS = any("S" in tablero[i][j] for i, j in v)

    # Lectura de paredes
    pared_arriba = (fila == 0) 
    pared_abajo = (fila == dim-1)
    pared_izq = (columna == 0) 
    pared_der = (columna == dim-1)

    return [eF,eP,eD,eM,eS, pared_arriba, pared_abajo, pared_izq, pared_der, grito]

def probabilidades_priori(dim:int)->dict:
    """
    Construye matrices con probabilidades iniciales prior
    
    :param dim (int): Dimensión del palacio
    :return dict: Matrices de estímulos
    """
    N = dim*dim
    prior = 1/(N-1)

    print("Partimos pensando que todas las celdas menos la inicial tienen la misma probabilidad de tener una trampa")
    tablero_priori = []
    for _ in range(dim): #Inicializamos el tablero con el valor del prior
        fila = []
        for _ in range(dim):
            fila.append(prior)
        tablero_priori.append(fila)
    tablero_priori[0][0] = 0.0 #Menos la primera posición
    priors_estimulos = {'F':[fila[:] for fila in tablero_priori],'P':[fila[:] for fila in tablero_priori],'D':[fila[:] for fila in tablero_priori],
                        'M':[fila[:] for fila in tablero_priori],'S':[fila[:] for fila in tablero_priori],'CK':[fila[:] for fila in tablero_priori]}
    return priors_estimulos #Devolvemos un diccionario con clave el estímulo y valor su matriz correspondiente

def probabilidades_likelihood(dim:int,fil:int,col:int,percibido:bool)->list[list]:
    """
    Crea la matriz de verosimilitud de un estímulo concreto
    
    :param dim (int): Dimensión del palacio
    :param fil (int): Fila de la celda
    :param col (int): Columna de la celda
    :param percibido (bool): Booleano de perceptión de estímulo
    :return list[list]: Matriz de verosimilitud
    """
    matriz_inicial = []
    for _ in range(dim):
        fila = []
        for _ in range(dim):
            fila.append(0.0) #Inicializamos la matriz a 0
        matriz_inicial.append(fila)
    
    #Buscamos celdas para evaluar en función de si recibimos o no el estímulo
    celdas_relevantes = vecinos(fil,col,dim) + [(fil,col)]
    if percibido: #Si lo recibimos la probabilidad se concentrará en esas celdas
        for i in range(dim):  #Escogemos este tipo de estructura aunque se repita el for porque es más visual para entender el proceso
            for j in range(dim): 
                if (i,j) in celdas_relevantes:
                    matriz_inicial[i][j] = 1.0
    else: #Si no lo recibimos, se reparte entre las demás celdas
        for i in range(dim):
            for j in range(dim):
                if (i,j) not in celdas_relevantes:
                    matriz_inicial[i][j] = 1.0
    return matriz_inicial #Devolvemos la matriz de verosimilitud

def probabilidades_posterior(matriz_prior:list[list],fil:int,col:int,dim:int,percibido:bool)->list[list]:
    """
    Crea la matriz del posterior para el estímulo percibido
    
    :param matriz_prior (list[list]): Matriz del prior del elemento
    :param fil (int): Fila de la celda
    :param col (int): Columna de la celda
    :param dim (int): Dimensión del templo
    :param percibido (bool): Estímulo percibido o no
    :return list[list]: Matriz del posterior
    """
    matriz_likelihood = probabilidades_likelihood(dim,fil,col,percibido)
    matriz_posterior_no_norm = [] #Creamos una matriz de posterior inicializada a 0.0
    norma = 0
    for _ in range(dim):
        fila = []
        for _ in range(dim):
            fila.append(0.0)
        matriz_posterior_no_norm.append(fila)
    
    #Aplicamos Regla Posterior: Prior x Likelihood
    for i in range(dim):
        for j in range(dim):
            if i == fil and j == col:
                matriz_posterior_no_norm[i][j] = 0.0
            else:
                matriz_posterior_no_norm[i][j] = matriz_prior[i][j]*matriz_likelihood[i][j]
            norma += matriz_prior[i][j]*matriz_likelihood[i][j]
    
    #Comprobamos si está normalizada y si no, normalizamos para que sume 1 (dividimos por la norma)
    if norma > 0:
        for i in range(dim):
            for j in range(dim):
                matriz_posterior_no_norm[i][j] /= norma

    return matriz_posterior_no_norm

def mapas_de_calor_probabilidades(priors_estimulos:dict,dim:int,fil:int,col:int)->None:
    """
    Muestra los mapas de calor de las trampas, soldado y salida
    
    :param priors_estimulos (dict): Diccionario con estímulos y matrices priors
    :param dim (int): Dimensión del templo
    :param fil (int): Fila de la celda
    :param col (col): Columna de la celda
    :return None
    """
    matriz_F = priors_estimulos['F']
    matriz_P = priors_estimulos['P']
    matriz_D = priors_estimulos['D']
    matriz_M = priors_estimulos['M']
    matriz_S = priors_estimulos['S']
    
    #Inicializamos la matriz a 0.0
    matriz_trampas = []
    for _ in range(dim):
        fila = []
        for _ in range(dim):
            fila.append(0.0)
        matriz_trampas.append(fila)

    #Calculamos el riesgo de encontrar alguna trampa
    for i in range(dim):
        for j in range(dim):
            if i == fil and j == col:
                matriz_trampas[i][j] = 0.0
            else:
                matriz_trampas[i][j] = matriz_F[i][j] + matriz_P[i][j] + matriz_D[i][j]

    mapas = [
            (matriz_trampas, '---MAPA DE CALOR TRAMPAS---', 'Reds'),
            (matriz_M, '---MAPA DE CALOR SOLDADO---', 'Blues'),
            (matriz_S, '---MAPA DE CALOR SALIDA---', 'Greens')
        ]

    for matriz, titulo, color in mapas: #Representamos cada mapa
        plt.figure(figsize=(6, 5)) # Creamos una figura nueva para cada mapa
        sns.heatmap(matriz, annot=True, fmt='.3f', cmap=color) 
        plt.title(titulo)
        plt.show()

def movimientos_seguros(priors_estimulos: dict, fil:int,col:int, p_umbral: float, dim: int)->list:
    """
    Se encarga de determinar si una celda es segura basándose en las probabilidades
    y de devolver una lista de objetivos para tirar la granada 
    si se detecta el estímulo del soldado.
    
    :param priors_estimulos (dict): Diccionario con estímulos y matrices priors
    :param fil (int): Fila de la celda
    :param col (col): Columna de la celda
    :param p_umbral (float): Probabilidad para determinar si una celda es segura o no
    :param dim (int): Dimensión del templo
    :return list: Lista de celdas seguras y objetivos de la granada
    """
    #Comenzamos obteniendo las matrices prior de los estímulos
    matriz_F = priors_estimulos['F']
    matriz_P = priors_estimulos['P']
    matriz_D = priors_estimulos['D']
    matriz_M = priors_estimulos['M']

    #Obtenemos los vecinos y partimos de una max_prob_militar = -1 que se irá actualizando
    vecino = vecinos(fil,col,dim)
    celdas_seguras = []
    obj_granada = []
    max_prob_militar = -1

    for fila,columna in vecino:
        riesgo_trampas = matriz_F[fila][columna] + matriz_P[fila][columna] + matriz_D[fila][columna]
        riesgo_soldado = matriz_M[fila][columna]

        #Tenemos en cuenta todo el riesgo posible y un riesgo mínimo para el soldado
        if riesgo_soldado >= max_prob_militar and riesgo_soldado > 0.1:
            max_prob_militar = riesgo_soldado
            obj_granada.append((fila,columna))

        #Verificamos si una celda es segura con la probabilidad umbral
        if (riesgo_trampas+riesgo_soldado) < p_umbral:
            celdas_seguras.append((fila,columna))
    
    return celdas_seguras,obj_granada

def realidad(fila:int,columna:int,tablero:list[list],kurtz:bool,grito:bool,salida:tuple,pos_kurtz:tuple)->list:
    """
    Representa el estado actual del juego en una determinada celda
    
    :param fila (int): Fila de la celda
    :param columna (int): Columna de la celda
    :param tablero (list[list]): Tablero que representa el templo
    :param kurtz (bool): Indica si Kurtz está o no en la celda
    :param grito (bool): Indicador de vida del soldado
    :param salida (tuple): Coordenadas de salida (si las hay)
    :param pos_kurtz (tuple): Coordenadas de Kurtz (si las hay)
    :return list: Datos necesarios para continuar la ejecución del proceso
    """
    trampas = ['F','D','P']
    #Verificamos si encontramos alguna trampa en la celda o un soldado vivo
    if any(tramp in tablero[fila][columna] for tramp in trampas) or (not grito and 'M' in tablero[fila][columna]):
        print('¡Oh no! Te has encontrado con un obstáculo letal y has muerto')
        return 'MUERTE',kurtz,None,None
    
    #Si encontramos a Kurtz y no hay soldado en su celda y no lo habíamos encontrado aún
    if 'CK' in tablero[fila][columna] and 'M' not in tablero[fila][columna] and not kurtz:
        print(f"¡Hemos encontrado al Coronel Kurtz! Se hallaba escondido en la celda {fila, columna}")
        kurtz = True #Encontrado
        pos_kurtz = (fila,columna) #Almacenamos su posición

    #Comprobamos si la salida se encuentra en la celda
    if 'S' in tablero[fila][columna]: 
        salida = (fila,columna) #Si es así almancenamos su posición
        if kurtz: #Si además está Kurtz, hemos terminado
            print(f"¡Encontramos la salida!")
            return 'VICTORIA',kurtz,salida,pos_kurtz
        else: #Si no simplemente Willard sigue vivo pero con la salida encontrada
            print(f"¡Muy bien! Has encontrado la casilla de salida en {fila,columna}. Guardamos la posición para cuando encontremos al Coronel")
    
    return 'VIVO',kurtz,salida,pos_kurtz

def movimientos_posibles(perceptos:list,granada:int)->list:
    """
    Devuelve los movimientos posibles en una celda
    
    :param perceptos (list): Lista de perceptos
    :param granada (int): Estado de la granada
    :return list: Lista de movimientos posibles
    """
    #Partimos con todos los movimientos posibles
    movs_posibles = ['W','A','S','D']

    #Obtenemos el estímulo del soldado y los de las paredes
    eM = perceptos[3]
    pared_arriba, pared_abajo, pared_izq, pared_der = perceptos[5:9]

    #Validamos movimientos en función de los estímulos recibidos
    if pared_arriba:
        movs_posibles.remove('W')
    if pared_izq:
        movs_posibles.remove('A')
    if pared_abajo:
        movs_posibles.remove('S')
    if pared_der:
        movs_posibles.remove('D')
    if eM and granada > 0:
        print('¡Granada disponible!')
        movs_posibles.append('G')
    
    return movs_posibles #Devolvemos la lista de movimientos posibles

def validar_ejecutar_movimiento(pos_fila_actual:int,pos_columna_actual:int,granada:int,grito:bool,eM:bool,perceptos:list,blanco_granada:list,tablero_final:list[list],dim:int)->list:
    """
    Se encarga de validar y ejecutar el movimiento que desee
    hacer el usuario
    
    :param pos_fila_actual (int): Fila de la celda
    :param pos_columna_actual (int): Columna de la celda
    :param granada (int): Estado de la granada
    :param grito (bool): Indicador de vida del soldado
    :param eM (bool): Indicador de estímulo del soldado
    :param perceptos (list): Lista de perceptos
    :param blanco_granada (list): Posiciones para tirar la granada si se recibe estímulo de soldado
    :param tablero_final (list[list]): Tablero que representa el templo
    :param dim (int): Dimensión del templo
    :return list: Datos necesarios para ejecutar el proceso
    """
    movimiento_valido = False
    while not movimiento_valido:#Si quiere tirar una granada y no hay granadas
        #Vemos movimientos posibles
        movs_posibles = movimientos_posibles(perceptos,granada) 
        print(f'\nMovimientos posibles en la celda {pos_fila_actual,pos_columna_actual}: {movs_posibles}')
        #Validamos el movimiento seleccionado
        movimiento = input(f"Escoge un movimiento (W/A/S/D/G): ").upper()
        while movimiento not in movs_posibles:
            print('¡Oh no! Movimiento no válido...Escoge de nuevo')
            movimiento= input('Escoge un movimiento (W/A/S/D/G): ').upper()
        #Ejecutamos el movimiento
        if movimiento == 'W':
            pos_fila_actual -= 1
            movimiento_valido = True
        elif movimiento == 'S':
            pos_fila_actual += 1
            movimiento_valido = True
        elif movimiento == 'A':
            pos_columna_actual -= 1
            movimiento_valido = True
        elif movimiento == 'D':
            pos_columna_actual += 1
            movimiento_valido = True
        elif movimiento== 'G' :
            if granada == 0:
                print("\nUps. Ya no te quedan granadas...")
                continue
            else:
                movimiento_valido = True
                if not eM:
                    print("\nNo hay ruidos de soldado cerca. No lanzamos la granada.")
                elif blanco_granada:
                    granada -= 1
                    if len(blanco_granada) == 1:
                        f_obj,c_obj = blanco_granada[0]
                        print(f"¡LANZAMOS GRANADA A LA CELDA {f_obj,c_obj}!")
                    else:
                        print('\n¡Te muestro las celdas disponibles para tirar la granada!')
                        for gra in blanco_granada:
                            print(f"· {gra}")
                        soldado_caido = input("¿A qué celda deseas tirar la granada? Introduce sus coordenadas fila,columna: ")
                        idx = soldado_caido.index(",")
                        f_obj = int(soldado_caido[:idx])
                        c_obj = int(soldado_caido[idx+1:])
                        
                        # Validar coordenadas
                        while (f_obj, c_obj) not in blanco_granada or not (0 <= f_obj < dim) or not (0 <= c_obj< dim):
                            print('¡Oh no! Celda no válida...Debe ser adyacente y dentro del tablero.')
                            soldado_caido = input("¿A qué celda deseas tirar la granada? Introduce sus coordenadas: ")
                            idx = soldado_caido.index(",")
                            f_obj = int(soldado_caido[:idx])
                            c_obj = int(soldado_caido[idx+1:])
                    if 'M' in tablero_final[f_obj][c_obj]:
                        print(f"¡Bien! Mataste al soldado")
                        tablero_final[f_obj][c_obj].remove('M')
                        grito = True
                    else:
                        print('¡Oh no! El soldado no estaba ahí... Ya no te quedan granadas')
                continue
        #Actualizamos las posiciones
        if movimiento != 'G':
            print(f'¡Rumbo a la celda {pos_fila_actual,pos_columna_actual}!')
    return pos_fila_actual,pos_columna_actual,granada,grito

#---FUNCIÓN PRINCIPAL---

def juego_guiado(dim:int)->None:
    """
    Función principal que lleva a cabo toda la ejecución
    
    :param dim (int): Dimensión del templo
    :return None
    """
    #Creación de tableros
    tablero = []
    tablero_final = creacion_tablero(dim)
    for _ in range(dim):
        fila = []
        for _ in range(dim):
            fila.append("*")
        tablero.append(fila)

    #Inicializamos las variables
    capitan_willard = 'CW'
    p_umbral = 0.25 #Valor como referencia
    salida = None
    pos_kurtz = None
    pos_fila_actual = 0
    pos_columna_actual = 0
    grito = False
    kurtz_encontrado = False
    granada = 1
    obstaculo_letal = False
    mision_cumplida = False

    #Obtenemos los priors
    priors = probabilidades_priori(dim)

    print("¡Hola! Soy el Capitán Willard. Acompáñame en esta aventura para encontrar al Coronel Kurtz evitando los obstáculos letales.")
    print("Partimos de la celda (0,0)...")

    #FASE 1: BUSCAR A KURTZ
    while not obstaculo_letal and not kurtz_encontrado:
        tablero[pos_fila_actual][pos_columna_actual] = capitan_willard
        #Imprimimos el tablero visible para facilitar la visualización
        for fila in tablero:
            print(fila)

        #Obtenemos los perceptos de la celda
        perceptos = obtener_perceptos(tablero_final, pos_fila_actual, pos_columna_actual, grito, dim)
        eM = perceptos[3]

        #Obtenemos cada matriz del prior por separado
        claves = ['F', 'P', 'D', 'M', 'S']
        for i in range(5):
            priors[claves[i]] = probabilidades_posterior(priors[claves[i]], pos_fila_actual, pos_columna_actual, dim, perceptos[i])

        #Buscamos los movimientos seguros y las posibles celdas para tirar la granada
        seguras, blanco_granada = movimientos_seguros(priors, pos_fila_actual, pos_columna_actual, p_umbral, dim)

        #Mostramos los mapas de calor
        mapas_de_calor_probabilidades(priors, dim, pos_fila_actual, pos_columna_actual)
        
        #Actualizamos el tablero visible
        tablero[pos_fila_actual][pos_columna_actual] = 'X'
        #Mostramos una recomendación con las celdas seguras
        print(f"\nRecomendación: Celdas seguras {seguras}")
        #Si percibimos el estímulo, indicamos las posibles celdas de posición del soldado 
        if eM: 
            print(f"\nEl soldado podría estar en {blanco_granada}")

        #Ejecutamos el movimiento 
        pos_fila_actual, pos_columna_actual, granada, grito = validar_ejecutar_movimiento(
            pos_fila_actual, pos_columna_actual, granada, grito, 
            eM, perceptos, blanco_granada, tablero_final, dim
        )

        #Validamos el resultado de ese movimiento
        resultado, kurtz_encontrado,salida,pos_kurtz = realidad(pos_fila_actual, pos_columna_actual, tablero_final, kurtz_encontrado, grito,salida,pos_kurtz)
        
        #Concluimos
        if resultado == 'MUERTE':
            obstaculo_letal = True
        elif resultado == 'VICTORIA':
            print("¡Misión cumplida con éxito!")
            break

    #FASE 2: ENCONTRAR LA SALIDA
    #Igual que para buscar a kurtz pero ahora evaluamos el estímulo de la salida en vez del de soldado
    if kurtz_encontrado and not mision_cumplida and not obstaculo_letal:
        if salida is not None:
            print(f"\n¡VAMOS A LA SALIDA EN POSICIÓN {salida}! Misión cumplida")
        else:
            print('------------------------------------------------------------')
            print('¡Busquemos ahora la salida para completar la misión!')
            pos_fila_actual,pos_columna_actual = pos_kurtz
            while not obstaculo_letal and not mision_cumplida:
                tablero[pos_fila_actual][pos_columna_actual] = 'CWCK'
                for fila in tablero:
                    print(fila)
                perceptos = obtener_perceptos(tablero_final, pos_fila_actual, pos_columna_actual, grito, dim)
                eS = perceptos[4]

                claves = ['F', 'P', 'D', 'M', 'S']
                for i in range(5):
                    priors[claves[i]] = probabilidades_posterior(priors[claves[i]], pos_fila_actual, pos_columna_actual, dim, perceptos[i])

                seguras, blanco_granada = movimientos_seguros(priors, pos_fila_actual, pos_columna_actual, p_umbral, dim)

                mapas_de_calor_probabilidades(priors, dim, pos_fila_actual, pos_columna_actual)
                tablero[pos_fila_actual][pos_columna_actual] = 'X'
                print(f"Recomendación: Celdas seguras {seguras}")
                if eS: 
                    print(f"¡La salida está cerca...Lo presiento!")
                
                pos_fila_actual, pos_columna_actual, granada, grito = validar_ejecutar_movimiento(
                    pos_fila_actual, pos_columna_actual, granada, grito, 
                    eM, perceptos, blanco_granada, tablero_final, dim
                )

                resultado, kurtz_encontrado,salida,pos_kurtz = realidad(pos_fila_actual, pos_columna_actual, tablero_final, kurtz_encontrado, grito,salida,pos_kurtz)
                
                if resultado == 'MUERTE':
                    obstaculo_letal = True
                elif resultado == 'VICTORIA':
                    mision_cumplida = True
                    print("¡Misión cumplida con éxito!")

#JUEGO CON AGENTES

#---FUNCIONES AUXILIARES---

def heuristica(f1:int,c1:int,f2:int,c2:int)->int:
    """
    Devuelve la heurística entre dos celdas (distancia Manhattan)
    
    :param f1 (int): Fila celda 1
    :param c1 (int): Columna celda 1
    :param f2 (int): Fila celda 2
    :param c2 (int): Columna celda 2
    :return int: Distancia, coste heurístico
    """
    return abs(f1 - f2) + abs(c1 - c2) #Distancia Manhattan

def funcion_coste_acumulado(fil:int,col:int,priors:dict)->float:
    """
    Calcula el coste acumulado en dicha celda
    
    :param fil (int): Fila de la celda
    :param col (int): Columna de la celda
    :param priors (dict): Diccionario de estímulos con sus matrices de priors
    :return float: Coste acumulado de la celda
    """
    #Calculamos riesgo total y verificamos
    riesgo_trampas_soldado = priors['F'][fil][col] + priors['P'][fil][col] + priors['D'][fil][col] + priors['M'][fil][col]

    if riesgo_trampas_soldado >= 0.95:
        return float('inf')
    
    #El coste por movimiento es 1 (1 paso para llegar a esa celda adyacente) + el coste de riesgo*penalización suave
    return 1 + riesgo_trampas_soldado*5

def a_estrella_algoritmo(inicio:tuple,objetivo:tuple,priors:dict,dim:int):
    """
    Lleva a cabo la implementación del algoritmo A*
    
    :param inicio (tuple): Celda de partida
    :param objetivo (tuple): Celda objetivo
    :param priors (dict): Diccionario de priors con sus matrices correspondientes
    :param dim (int): Dimensión del templo
    """
    #Crearemos una lista que será la frontera
    frontera = []
    #Será una cola de prioridad que guardará todos los nodos a explorar
    heapq.heappush(frontera,(0,inicio))

    #Creamos el diccionario de padres y costes
    origen = {}
    g_real = {}
    for f in range(dim):
        for c in range(dim):
            g_real[(f, c)] = float('inf')
    g_real[inicio] = 0

    #Inicializamos el set de exploración
    cerrados = set()
    max_iter = dim*dim*10
    iteraciones = 0

    #Siempre que haya frontera y las iteraciones sean menora que max_iter
    while frontera and iteraciones < max_iter:
        iteraciones += 1
        _,nodo_actual = heapq.heappop(frontera)

        #Si ya hemos evaluado el nodo, pasamos
        if nodo_actual in cerrados:
            continue

        #Si no, lo añadimos al set de exploración
        cerrados.add(nodo_actual)

        #Si el nodo es el objetivo que buscamos, retornamos el camino hasta él
        if nodo_actual == objetivo:
            return camino(origen,nodo_actual)
        
        #Evaluaremos los vecinos del nodo
        vecino = vecinos(nodo_actual[0],nodo_actual[1],dim)
        for vec in vecino:
            #Si ya los hemos evaluado, pasamos
            if vec in cerrados:
                continue

            #Si no, calculamos su coste del vecino, pasando si el coste es infinito
            coste_actual = funcion_coste_acumulado(vec[0],vec[1],priors)
            if coste_actual == float('inf'): #Si es trampa o no es celda segura, no nos vale
                continue

            #Calculamos el coste acumulado sumándole el coste del nodo actual al coste real del vecino
            coste_acumulado = g_real[nodo_actual] + coste_actual

            #Si el coste es menor al que tenía el vecino en el diccionario de costes (es mejor), actualizamos
            if coste_acumulado < g_real[vec]: 
                origen[vec] = nodo_actual
                g_real[vec] = coste_acumulado

                #Calculamos función de evaluación con heurística y coste_acumulado
                f_evaluacion = heuristica(vec[0],vec[1],objetivo[0],objetivo[1]) + coste_acumulado
                #Actualizamos cola de prioridad
                heapq.heappush(frontera,(f_evaluacion,vec))
    return None

def camino(origen:dict,nodo_actual:tuple)->list:
    """
    Devuelve el camino del origen al objetivo, pero hasta que
    llega al objetivo va añadiendo nodos al camino
    
    :param origen (dict): Diccionario de padres e hijos
    :param nodo_actual (tuple): Nodo a evaluar
    :return list: Camino
    """
    way = [nodo_actual]
    while nodo_actual in origen: #Vamos actualizando yendo de objetivo a inicio
        nodo_actual = origen[nodo_actual]
        way.append(nodo_actual)
    return way[::-1] #Invertimos la lista para que vaya de inicio a fin

def obtener_coronel_aprox(priors:dict,visitadas:dict,dim:int)->tuple:
    """
    Devuelve la posición de lo que se cree que es el objetivo
    (posición de Kurtz)
    
    :param priors (dict): Diccionario de priors con matrices
    :param visitadas (dict): Diccionario de celdas visitadas
    :param dim (int): Dimensión del templo
    :return tuple: Celda objetivo
    """
    #Inicializamos el obj y mejor_valor a None y a infinito respect.
    obj = None
    mejor_valor = float('inf')

    for fila in range(dim):
        for columna in range(dim):
            #Si ya hemos estado en la celda, la penalizamos con coste mayor
            if (fila,columna) in visitadas:
                penalizacion = visitadas[(fila,columna)]*0.2
            else:
                penalizacion = 0

            #Calculamos el riesgo total de trampas y soldado y calculamos la probabilidad de que esté Kurtz en dicha celda
            riesgo_trampas_soldado = priors['F'][fila][columna] + priors['P'][fila][columna] + priors['D'][fila][columna] + priors['M'][fila][columna]
            prob_ck = priors['CK'][fila][columna]

            #Si esta probabilidad es mayor que 0.6 retornamos la celda
            if prob_ck > 0.6:
                return (fila, columna)
            
            #Obtenemos el valor con la penalización incluida, multiplicando a prob_ck * 3 para aumentar la posibilidad de ir a dicha celda
            valor = riesgo_trampas_soldado - prob_ck*3 + penalizacion

            #Si el riesgo es menor que el que consideramos mejor valor, actualizamos
            if valor < mejor_valor:
                mejor_valor = valor
                obj = (fila,columna)

    return obj #Devolvemos el que creemos que es el objetivo

def obtener_salida_aprox(priors:dict, visitadas:dict, dim:int)->tuple:
    """
    Devuelve la posición de lo que se cree que es el objetivo
    (posición de la salida)
    
    :param priors (dict): Diccionario de priors con matrices
    :param visitadas (dict): Diccionario de celdas visitadas
    :param dim (int): Dimensión del templo
    :return tuple: Celda objetivo
    """
    obj = None
    mejor_valor = float('inf')

    for fila in range(dim):
        for columna in range(dim):
            # Mantenemos la misma lógica de penalización para que no de vueltas
            if (fila,columna) in visitadas:
                penalizacion = visitadas[(fila,columna)]*0.2
            else:
                penalizacion = 0

            #Calculamos el riesgo total de trampas y soldado y calculamos la probabilidad de que esté la salida en dicha celda
            riesgo = (priors['F'][fila][columna] + priors['P'][fila][columna] + 
                      priors['D'][fila][columna] + priors['M'][fila][columna])
            prob_s = priors['S'][fila][columna]

            #Obtenemos el valor con la penalización incluida, multiplicando a prob_s * 3 para aumentar la posibilidad de ir a dicha celda
            valor = riesgo - (prob_s * 3) + penalizacion

            #Si el riesgo es menor que el que consideramos mejor valor, actualizamos
            if valor < mejor_valor:
                mejor_valor = valor
                obj = (fila, columna)

    return obj #Devolvemos el que creemos que es el objetivo

#---FUNCIÓN PRINCIPAL---

def juego_con_agente_A_estrella(dim:int)->None:
    """
    Función principal que lleva a cabo toda la ejecución
    de este proceso
    
    :param dim (int): Dimensión del templo
    :return None
    """
    #Creación de tableros
    tablero = []
    tablero_final = creacion_tablero(dim)
    for _ in range(dim):
        fila = []
        for _ in range(dim):
            fila.append("*")
        tablero.append(fila)

    #Inicialización de variables
    capitan_willard = 'CW'
    p_umbral = 0.25 #Determinado como referencia
    salida = None
    pos_kurtz = None
    pos_fila_actual = 0
    pos_columna_actual = 0
    grito = False
    kurtz_encontrado = False
    granada = 1
    obstaculo_letal = False
    mision_cumplida = False

    #Creación de diccionarios y obtención de priors
    visitadas = {}
    priors = probabilidades_priori(dim)

    print("¡Hola! Soy el Capitán Willard. Acompáñame en esta aventura para encontrar al Coronel Kurtz evitando los obstáculos letales.")
    print("Partimos de la celda (0,0)...\n")

    #FASE 1: BUSCAR A KURTZ
    while not obstaculo_letal and not kurtz_encontrado:
        #Validamos si ya hemos estado o no en la celda
        posicion = (pos_fila_actual, pos_columna_actual)

        if posicion in visitadas:
            cuenta_actualizada = visitadas[posicion] + 1
        else:
            cuenta_actualizada = 1
        visitadas[posicion] = cuenta_actualizada
        tablero[pos_fila_actual][pos_columna_actual] = capitan_willard
        for fila in tablero: 
            print(fila)

        #Obtenemos los perceptos, sobre todo el del soldado
        perceptos = obtener_perceptos(tablero_final, pos_fila_actual, pos_columna_actual, grito, dim)
        eM = perceptos[3]

        #Matrices de priors por separado
        claves = ['F', 'P', 'D', 'M', 'S']
        for i in range(len(claves)):
            priors[claves[i]] = probabilidades_posterior(priors[claves[i]], pos_fila_actual, pos_columna_actual, dim, perceptos[i])

        #Mostramos mapas de calor
        mapas_de_calor_probabilidades(priors, dim, pos_fila_actual, pos_columna_actual)
        #Mismo proceso que en juego_guiado pero en este caso haya
        #muchas posiciones o una en blanco_granada nos quedamos siempre con la primera
        if eM and granada > 0:
            _,blanco_granada = movimientos_seguros(priors, pos_fila_actual, pos_columna_actual, p_umbral, dim)
            if blanco_granada:
                fila, columna = blanco_granada[0] 
                print(f"¡LANZAMOS GRANADA A LA CELDA {fila,columna}!")
                granada -= 1
                if 'M' in tablero_final[fila][columna]:
                    print(f"¡Bien! Mataste al soldado")
                    tablero_final[fila][columna].remove('M')
                    grito = True
                    for i in range(dim):
                        for j in range(dim):
                            priors['M'][i][j] = 0.0
                else:
                    print('¡Oh no! El soldado no estaba ahí... Ya no te quedan granadas')
        
        #Obtenemos la posición aprox del coronel
        objetivo_ck = obtener_coronel_aprox(priors,visitadas,dim)
        if objetivo_ck is None:
            print("No hay un objetivo claro para Kurtz.")
            break

        #Calculamos la ruta a la posición aprox
        ruta = a_estrella_algoritmo((pos_fila_actual,pos_columna_actual),objetivo_ck,priors,dim)

        #Si existe camino, evaluamos
        if ruta and len(ruta) > 1:
            tablero[pos_fila_actual][pos_columna_actual] = 'X'
            pos_fila_actual, pos_columna_actual = ruta[1]
            print(f'\n¡Rumbo a la celda {pos_fila_actual,pos_columna_actual}!\n')
        else:
            print('No hemos encontrado una ruta segura al objetivo...¡Nos arriesgamos un poco...!')
            #Aumentamos la probabilidad umbral para conseguir una ruta
            ruta = a_estrella_algoritmo((pos_fila_actual, pos_columna_actual), objetivo_ck, priors, p_umbral + 0.25, dim,visitadas)
            if ruta and len(ruta) > 1:
                tablero[pos_fila_actual][pos_columna_actual] = 'X'
                pos_fila_actual, pos_columna_actual = ruta[1]
            else:
                print("Atrapado definitivamente.")
                break
        
        #Concluimos
        resultado, kurtz_encontrado, salida, pos_kurtz = realidad(pos_fila_actual, pos_columna_actual, tablero_final, kurtz_encontrado, grito, salida, pos_kurtz)
        if resultado == 'MUERTE':
            obstaculo_letal = True
    
    #FASE 2: ENCONTRAR LA SALIDA
    if kurtz_encontrado and not mision_cumplida and not obstaculo_letal:
        if salida is not None: #Si ya encontramos la salida terminamos
            print(f"Ya tenemos la salida: posición {salida}. ¡Vamos hacia ahí! Misión cumplida")
        else:
            print('Tenemos al coronel, pero debemos buscar la salida...')
            pos_fila_actual, pos_columna_actual = pos_kurtz

        #Buscamos la salida comenzando en la posición donde estaba Kurtz
        while not obstaculo_letal and not mision_cumplida:
            #Validamos si ya hemos estado o no en la celda
            posicion = (pos_fila_actual, pos_columna_actual)

            if posicion in visitadas:
                cuenta_actualizada = visitadas[posicion] + 1
            else:
                cuenta_actualizada = 1

            visitadas[posicion] = cuenta_actualizada
            tablero[pos_fila_actual][pos_columna_actual] = 'CWCK'
            
            for fila in tablero: 
                print(fila)

            #Obtenemos los perceptos
            perceptos = obtener_perceptos(tablero_final, pos_fila_actual, pos_columna_actual, grito, dim)

            #Matrices prior por separado
            claves = ['F', 'P', 'D', 'M', 'S']
            for i in range(5):
                priors[claves[i]] = probabilidades_posterior(priors[claves[i]], pos_fila_actual, pos_columna_actual, dim, perceptos[i])

            #Si no encontramos la salida, usamos la función obtener_salida_aprox
            if salida is not None:
                objetivo_escape = salida  
            else:
                objetivo_escape = obtener_salida_aprox(priors,visitadas, dim)

            #Calculamos la ruta desde la posición actual a la salida
            ruta = a_estrella_algoritmo((pos_fila_actual, pos_columna_actual), objetivo_escape, priors, dim)

            if ruta and len(ruta) > 1: #Si hay camino, lo recorremos
                tablero[pos_fila_actual][pos_columna_actual] = 'X'
                pos_fila_actual, pos_columna_actual = ruta[1]
                print(f"\nVamos hacia {objetivo_escape} -> Nos movemos a {pos_fila_actual, pos_columna_actual}\n")
            else: #Si no, no encontramos ruta segura
                print("No hay camino seguro a la salida.")
                break

            #Concluimos
            resultado, kurtz_encontrado, salida, pos_kurtz = realidad(
                pos_fila_actual, pos_columna_actual, tablero_final, 
                kurtz_encontrado, grito, salida, pos_kurtz
            )
            
            if resultado == 'MUERTE':
                obstaculo_letal = True
                print("Muerte en la huida.Fallamos...")
            elif resultado == 'VICTORIA':
                mision_cumplida = True 
                print("¡MISIÓN CUMPLIDA! Hemos conseguido escapar.")