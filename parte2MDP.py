#PARTE 2 - Cruzar el río: Incertidumbre (MDP)

import random

#---FUNCIONES AUXILIARES---

def creacion_entorno(filas:int,columnas:int,semilla:int)->dict:
    """
    Se encarga de crear el entorno del río
    
    :param filas (int): Número de filas
    :param columnas (int): Número de columnas
    :param semilla (int): Semilla
    :return dict: Diccionario de entorno
    """
    random.seed(semilla)
    #Designamos la posición del origen (0,0) y la del destino (aleatoria en la última col.)
    origen = (0, 0)
    destino = (random.randint(0,filas-1),columnas - 1)
    #Establecemos la posición de las islas
    pos_islas = []
    n_isla = 0
    while n_isla < 2:
        pos_fila = random.randint(1,filas-2)
        pos_col = random.randint(0,columnas-1)
        #Nos aseguramos que no halla ya otra isla ni que coincida con la posición de destino
        if (pos_fila,pos_col) not in pos_islas and (pos_fila,pos_col) != destino:
            pos_islas.append((pos_fila,pos_col))
            n_isla += 1

   
    return {'filas':filas,'columnas':columnas,'origen':origen,'destino':destino,'islas':pos_islas}


def visualizar_rio(entorno:dict,pos_agente:tuple)->None:
    """
    Permite visualizar el río. En cada movimiento visualizaremos el río.
    Permite ver las decisiones tomadas con el Proceso de Decisión de Markov
   
    :param entorno (dict): Diccionario con datos del entorno
    :param pos_agente (tuple): Posición del agente (origen)
    """
    filas = entorno['filas']
    columnas = entorno['columnas']
    destino = entorno['destino']
    islas = entorno['islas']


    for i in range(filas):
        ind_fila = ''
        for j in range(columnas):
            if (i,j) == pos_agente:
                celda = "|CWCK|"
            elif(i,j) == destino:
                celda = '| E  |'
            elif (i,j) in islas:
                celda = '| I  |'
            elif j == 0 or j == columnas - 1:
                celda = '|    |'
            else:
                celda = '| R  |'
            ind_fila += celda
        print(ind_fila)


def probabilidad_sig_estado(estado_actual:tuple,estado_obj:tuple,action:str,fuerzas:list,entorno:dict)->float:
    """
    Devuelve la probabilidad de llegar a la celda siguiente
    ejecutando una acción determinada
    
    :param estado_actual (tuple): Celda actual
    :param estado_obj (tuple): Celda a la que queremos llegar
    :param action (str): Acción que queremos ejecutar
    :param fuerzas (list): Lista de fuerza del río
    :param entorno (dict): Diccionario de entorno
    :return float: Probabilidad de llegar a la celda objetivo
    """
    #Inicializamos la probabilidad a 0 y obtenemos filas y cols. de la celda de origen y de destino
    prob = 0
    fila_act = estado_actual[0]
    col_act = estado_actual[1]

    fila_obj = estado_obj[0]
    col_obj = estado_obj[1]

    #Obtenemos la fuerza del río de esa columna
    fuerza =  fuerzas[col_act]

    #Calculamos adónde llegamos tomando la acción action
    if action == 'U':
        f_dest  = fila_act - 1
        c_dest = col_act
    elif action == 'D':
        f_dest = fila_act + 1
        c_dest = col_act
    elif action == 'L':
        c_dest = col_act - 1
        f_dest = fila_act
    elif action == 'R':
        c_dest = col_act + 1
        f_dest = fila_act
    elif action == 'S':
        f_dest = fila_act
        c_dest = col_act
    else:
        return 0.0

    #Si la celda está fuera de los límites del río, la celda objetivo es la celda actual
    if not (0 <= f_dest  and f_dest < entorno['filas'] and 0 <= c_dest and c_dest < entorno['columnas']) or (f_dest, c_dest) in entorno['islas']:
        f_dest, c_dest = fila_act, col_act

    prob = 0.0
    if action == 'D':
        if (fila_obj, col_obj) == (f_dest, c_dest):
            prob = 1.0
    else:
        # Probabilidad de éxito de la dirección: 1 - fuerza
        if (fila_obj, col_obj) == (f_dest, c_dest):
            prob += (1.0 - fuerza)

        f_corriente, c_corriente = fila_act + 1, col_act #El arrastre tira para abajo
        # Si el arrastre choca con borde o isla, se queda en la celda actual
        if f_corriente >= entorno['filas'] or (f_corriente, c_corriente) in entorno['islas']:
            f_corriente, c_corriente = fila_act, col_act

        #Si la celda objetivo coincide con la celda de arrastre (celda inferior) sumamos probabilidad  
        if (fila_obj, col_obj) == (f_corriente, c_corriente):
            prob += fuerza

    return prob


def fuerza_rio(columnas:int,semilla:int)->list:
    """
    Calcula la fuerza de arrastre en función de la columna
   
    :param columnas (int): Número de columnas
    :param semilla (int): Mapa del río
    :return (list): Lista de fuerzas del río
    """
    random.seed(semilla)
    fuerza =[]
    for c in range(columnas):
        #Si la columna es la primera o la última la fuerza es 0.0
        if c == 0 or c == columnas - 1:
            fuerza.append(0.0)
        else:
            #Si no, es un valor aleatorio siguiendo una distribución uniforme
            fuerza.append(round(random.uniform(0.06, 0.94), 1))
    return fuerza


def recompensas(estado_sig:tuple,entorno:dict)->int:
    """
    Calcula la recompensa actual de una celda

    :param estado_sig (tuple): Celda a evaluar
    :param entorno (dict): Diccionario de entorno
    :return int: Recompensa actual de la celda
    """
    if estado_sig == entorno['destino']:
        recompensa = 100
    elif estado_sig in entorno['islas']:
        recompensa = -100
    else:
        recompensa = -1
    return recompensa


def informacion_actual(estado_actual:tuple,actions:list,fuerza:list,entorno:dict)->None:
    """
    Muestra la información del estado actual

    :param estado_actual (tuple): Celda actual
    :param actions: Lista de acciones posibles
    :param fuerza (list): Lista de fuerzas del río
    :param entorno (dict): Diccionario de entorno
    :return None
    """
    fil,col = estado_actual
    fuerza_actual = fuerza[col]
    print(f'\n-----------INFORMACIÓN SOBRE {estado_actual}-----------')
    print(f"· Posición actual: {estado_actual}")
    print(f"· Acciones disponibles en este estado: {actions}")
    for a in actions:
        if a == 'U':
            f_dest = fil -1
            c_dest = col
        elif a == 'D':
            f_dest = fil + 1
            c_dest = col
        elif a == 'L':
            f_dest = fil
            c_dest = col - 1
        elif a == 'R':
            f_dest = fil
            c_dest = col + 1
        else:
            f_dest = fil
            c_dest = col

        p_choque = 0.0
        # Ajuste por bordes/islas (p_stay = 1) CHOQUE = 1.0
        if not (0 <= f_dest < entorno['filas'] and 0 <= c_dest < entorno['columnas']) or (f_dest, c_dest) in entorno['islas']:
            dest = f"{estado_actual} (Choque)"
            p_choque = 1.0

        else:
            dest = f"({f_dest}, {c_dest})"

        # Probabilidades de transición
        if a == 'D':
            p_exito = 1.0
            p_arrastre = 0.0
        else:
            p_exito = 1.0 - fuerza_actual
            p_arrastre = fuerza_actual

        print(f"· Destino tomando la acción {a}: {dest}")
        print(f"· Probabilidades de transición: {p_exito} de éxito, {p_arrastre} de arrastre, {p_choque} de choque")
    #Obtenemos la recompensa en dicho estado
    print(f"· Recompensa obtenida en este estado: {recompensas(estado_actual,entorno)}")


def mostrar_mapas(mapa:dict)->None:
    """
    Muestra los mapas

    :param mapa (dict): Diccionario de coordenadas
    """
    for clave in mapa:
        print(f" · {clave}: {mapa[clave]}")


def value_iteration(entorno:dict,fuerzas:list,gamma:float,epsilon:float)->list:
    """
    Lleva a cabo el algoritmo de Value Iteration, pieza clave en los procesos
    de decisión de Markov.

    :param entorno (dict): Diccionario de entorno
    :param fuerzas (list): Lista de fuerzas del río
    :param gamma (float): Factor de descuento
    :param epsilon (float): Condición de parada
    :return list: Devuelve el mapa de utilidad y la política óptima
    """
    mapa_utilidad = {}

    #Rellenamos el mapa de utilidad con todas las celdas del río inicializadas a 0
    for fila in range(entorno['filas']):
        for columna in range(entorno['columnas']):
            mapa_utilidad[(fila,columna)] = 0

    #Hacemos lo mismo para política óptima pero rellenando con la acción "S"
    politica_optima = {}
    for fila in range(entorno['filas']):
        for columna in range(entorno['columnas']):
            politica_optima[(fila,columna)] = 'S'

    acciones = ['U','D','L','R','S']
    parada = False
    while not parada:
        mapa_iteracion = mapa_utilidad.copy() #Hacemos copias de los mapas para evitar errores
        politica_copy = politica_optima.copy()
        cambios = 0
        for pos in mapa_utilidad:
            fil = pos[0] #Obtenemos la fila y columna de una posición del mapa
            col = pos[1]
            opciones = [(fil-1,col),(fil+1,col),(fil,col-1),(fil,col+1),(fil,col)] #Analizamos todos los destinos posibles
            if pos not in entorno['islas'] and pos != entorno['destino']: #Si la celda no coincide ni con el destino ni con una isla nos vale
                valor_acciones = []
                for action in acciones: #Verificaremos todas las acciones para todas las opciones de destino
                    valor_total = 0
                    for opc in opciones:
                        prob = probabilidad_sig_estado(pos,opc,action,fuerzas,entorno) #Calculamos la probabilidad
                        if prob > 0: #Si es mayor que 0 nos vale, si no es que algún dato o acción no son válidos
                            if opc in mapa_utilidad: #Siempre y cuando la celda esté entre las opciones y no fuera de los límite
                                estado_real = opc
                            else: #Si está fuera de los límites actualizamos a la posición
                                estado_real = pos

                            recompensa = recompensas(estado_real,entorno) #Obtenemos la recompensa en ese estado
                            #Aplicamos Ecuación de Bellman: ΣP(s'|s,a)*[R(s,a,s')+γV*(s')]
                            valor_total += prob*(recompensa + gamma*mapa_utilidad[estado_real])
                    #Añadimos el nuevo valor al valor de las acciones
                    valor_acciones.append(valor_total)
                val_mayor = max(valor_acciones) #Buscamos el que nos dará mayor puntuación (el máximo)
                ite_ant = mapa_iteracion[pos] #Obtenemos el valor máximo anterior

                dif = abs(val_mayor - ite_ant) #Calculamos la diferencia y obtenemos el máximo entre el cambio anterior y el actual
                cambios = max(cambios,dif)

                idx_opt = valor_acciones.index(val_mayor)
                acc_opt = acciones[idx_opt]

                mapa_iteracion[pos] = val_mayor #Actualizamos los mapas con los valores correspondientes
                politica_copy[pos] = acc_opt

        mapa_utilidad = mapa_iteracion.copy() #Actualizamos los mapas reales con copias de las copias
        politica_optima = politica_copy.copy()

        if cambios < epsilon: #Verificamos la condición de parada, si el cambio es menor que el epsilon establecido
            parada = True

    return mapa_utilidad, politica_optima


#---FUNCIONES PRINCIPALES---

def proceso_completo(filas:int,columnas:int,semilla:int,gamma:float,epsilon:float)->None:
    """
    Función que lleva a cabo toda la ejecución de esta parte

    :param filas (int): Número de filas
    :param columnas (int): Número de columnas
    :param semilla (int): Mapa del río
    :param gamma (float): Factor de descuento
    :param epsilon (float): Condición de parada de Value Iteration
    :return None
    """
    entorno = creacion_entorno(filas,columnas,semilla)
    fuerzas =  fuerza_rio(entorno['columnas'],semilla)

    mapa_utilidad,politica_optima = value_iteration(entorno,fuerzas,gamma,epsilon)

    print('----------------MAPA DE UTILIDAD----------------')
    mostrar_mapas(mapa_utilidad)
    print('------------------------------------------------')

    print('----------------MAPA DE POLÍTICA ÓPTIMA----------------')
    mostrar_mapas(politica_optima)
    print('-------------------------------------------------------')

    estado_actual = entorno['origen']
    mision_en_curso = True
    actions = ['U','D','L','R','S']
    steps = 0
    max_steps = 50
    recompensa_acumulada = 0

    print("VISUALIZACIÓN INICIAL DEL RÍO")
    visualizar_rio(entorno,estado_actual)

    while mision_en_curso and steps < max_steps:
        steps += 1
        accion_opt =  politica_optima[estado_actual]
        #Seleccionamos la fuerza de la columna para ver si Willard será arrastrado por el río o no
        fuerza_col = fuerzas[estado_actual[1]]

        informacion_actual(estado_actual,actions,fuerzas,entorno)

        #fuerza_col, será como la p_umbral en parte2.py nos servirá para ver si es arrastrado o no
        if accion_opt != 'D' and random.random() < fuerza_col:
            accion_final = 'D'
            print('¡Willard ha sido arrastrado por la corriente...!')
        else:
            accion_final = accion_opt
            print("¡Hemos conseguido mantener el rumbo!")

    
        fil, col = estado_actual
        if accion_final == 'U':
            fil -= 1
        elif accion_final == 'D':
            fil += 1
        elif accion_final == 'L':
            col -= 1
        elif accion_final == 'R':
            col += 1

        dest = (fil, col)

        if (0 <= fil < entorno['filas'] and 0 <= col < entorno['columnas'] and dest not in entorno['islas']):
            estado_actual = dest
        else:
            print(f"¡CHOQUE! Willard rebota y permanece en {estado_actual}")

    
        print('ACTUALIZACIÓN VISUALIZACIÓN')
        visualizar_rio(entorno,estado_actual)
        recompensa_acumulada += recompensas(estado_actual, entorno)

        if estado_actual == entorno['destino']:
            print(f'¡Misión cumplida! Pasos: {steps}')
            print(f'Recompensa total acumulada: {recompensa_acumulada}')
            mision_en_curso = False


def simulacion(): #POLÍTICA PERFECTA
    print("\n\n>>> ESCENARIO A: WILLARD IMPULSIVO (Gamma=0.1)") #BUCLE
    proceso_completo(filas=7, columnas=5, semilla=42, gamma=0.1, epsilon=0.01)

    print("\n\n>>> ESCENARIO B: WILLARD PRUDENTE (Gamma=0.99)") #ASEGURA MÁX PTCION
    proceso_completo(filas=5, columnas=6, semilla=42, gamma=0.99, epsilon=0.01)

    print("\n\n>>> ESCENARIO C: RÍO DESCONOCIDO (Semilla=123)") #DIST. RÍO
    proceso_completo(filas=4, columnas=5, semilla=123, gamma=0.9, epsilon=0.01)