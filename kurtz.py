import parte1 as p1
import parte2 as p2
import parte2MDP as p2MDP

menu1 = """
----- 🏰👽 BIENVENIDO AL PALACIO PELIGROSO 👽🏰 -----

A continuación deberás escoger UNA de las modalidades de juego
    · Guiado (G) → TÚ guiarás al Capitán Willard
    · Agentes (A) → El capitán decidirá por sí mismo las acciones 
      siguiendo uno de los agentes que selecciones

"""
menu2 = """
----- 👻🏦 BIENVENIDO AL TEMPLO TENEBROSO 🏦👻 -----

Te enfrentas a la SEGUNDA parte de esta aventura
A continuación deberás escoger UNA de las modalidades de juego
    · Guiado (G) → TÚ guiarás al Capitán Willard
    · Agentes (A) → El capitán decidirá por sí mismo las acciones 
      siguiendo uno de los agentes que selecciones

"""
menuMDP = """
----- ⛵🌫️  BIENVENIDO AL RÍO NEBULOSO  🌫️⛵ -----

Finalmente, nos enfrentamos a la ÚLTIMA parte de esta aventura
Deberemos cruzar el río y llegar a la orilla opuesta sanos y salvos
Según el manual de instrucciones, podemos encontrar una solución
usando MDP... ¿Nos ayudas?

**Indicaciones para el usuario: se han implementado 3 escenarios distintos
cambiando algunos de los datos para mostrar cómo varía la obtención del camino
y políticas óptimos
"""
if __name__ == "__main__":
    print("¡¡BIENVENIDO A CAMBOYA!!")
    print('A continuación se te presentan los 3 desafíos a los que se enfrentó el Capitán en su aventura.')
    print('Pulsando "Z" podrás pasar a la siguiente opción')
    print('\n---PARTE 1: PALACIO PELIGROSO---')
    print(menu1)
    opcion = input('\nElige una modalidad de juego (G/A) o pulsa "Z" para saltar a la PARTE 2: ').upper()
    while opcion != 'G' and opcion != 'A' and opcion != 'Z': #Escoger la modalidad de juego
        print('¡Oh no! Opción no válida...Escoge de nuevo')
        opcion = input('Elige una modalidad de juego (G/A) o pulsa "Z" para saltar a la PARTE 2: ').upper()
    while opcion != 'Z':
        if opcion == 'G':
            print('Has escogido la opción guiada...¡Buena suerte!🍀')
            p1.juego_guiado(6)
        elif opcion == 'A':
            print('Has escogido la opción por agentes. Emplearemos el agente BFS. ¡Buena suerte!🍀')
            p1.juego_con_agente_bfs(6)
        opcion = input('Elige una modalidad de juego (G/A) o pulsa "Z" para saltar a la PARTE 2: ').upper()
    
    print('\n---PARTE 2: TEMPLO TENEBROSO---')
    print(menu2)
    opcion = input('\nElige una modalidad de juego (G/A) o pulsa "Z" para saltar a la PARTE 3: ').upper()
    while opcion != 'G' and opcion != 'A' and opcion != "Z": #Escoger la modalidad de juego
        print('¡Oh no! Opción no válida...Escoge de nuevo')
        opcion = input('Elige una modalidad de juego (G/A) o pulsa "Z" para saltar a la PARTE 3: ').upper()
    while opcion != "Z":
        if opcion == 'G':
            print('Has escogido la opción guiada...¡Buena suerte!🍀')
            p2.juego_guiado(6)
        elif opcion == "A":
            print('Has escogido la opción por agentes. Emplearemos el agente A*')
            p2.juego_con_agente_A_estrella(6)
        opcion = input('Elige una modalidad de juego (G/A) o pulsa "Z" para saltar a la PARTE 3: ').upper()

    print('\n---PARTE 3: RÍO NEBULOSO---')
    print(menuMDP)
    opcion = input('\nElige "J" para jugar o pulsa "Z" para acabar la aventura: ').upper()
    while opcion != "J" and opcion != "Z":
        print('¡Oh no! Opción no válida...Escoge de nuevo')
        opcion = input('\nElige "J" para jugar o pulsa "Z" para acabar la aventura: ').upper()
    while opcion != "Z":
        p2MDP.simulacion()
        opcion = input('\nElige "J" para jugar o pulsa "Z" para acabar la aventura: ').upper()
    print("Esta aventura ha terminado, ¡lo hicimos! ¡Hasta la próxima!")
    