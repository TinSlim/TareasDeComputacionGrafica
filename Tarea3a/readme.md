# Aquarium

- aquarium-solver.py
    
    1. Ejecución del programa: Escribir en la terminal:  python aquarium-solver.py problem-setup.json                            Donde problem-setup.json corresponde a los parámetros para la discretización y resolución de la EDP, asegurarse estar en el directorio correcto y haber creado un archivo .json que cumpla el formato del enunciado. 
    
    2. Consideraciones y Supuestos: Usar números naturales en el tamaño del acuario, hay que considerar que números grandes requerirán más tiempo para su resolución.  Si no hay archivo en la entrada, se usa uno de prueba.
    
    3. Uso: Ejecutar el código para generar la solución. 

- aquarium-view.py
    
    1. Ejecución del programa: Escribir en la terminal:  python aquarium-view.py view-setup.json                           Donde view-setup.json corresponde a los parámetros para el dibujo de los peces y nombre de la solución calculada en el otro programa, asegurarse estar en el directorio correcto y haber creado un archivo .json que cumpla el formato del enunciado.

    2. Consideraciones y Supuestos: Existe temperatura habitable para cada tipo de pez entre las temperaturas que se calculan en el otro programa. Si no hay archivo en la entrada, se usa uno de prueba.

    3. Uso: Ejecutar el código para observar distribución de los peces, usar flechas del teclado para rotar la cámara, usar teclas ‘O’ y ‘P’ para regular distancia del centro al observador, usar teclas ‘A’, ‘B’ y ‘C’ para mostrar voxeles de los volúmenes habitables por cada tipo de pez.
