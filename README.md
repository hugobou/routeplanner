# Planificación de rutas con redes neuronales

Máster en ingeniería informática, UNED.

Trabajo de fin de máster.

Septiembre de 2021.

**Autor: Hugo Boullosa González**

**Tutora: Rocío Muñoz Mansilla**

**Co-tutor: Agustín Carlos Caminero Herráez**

## Resumen

La planificación de rutas es un problema de gran importancia en el sector del
transporte. En este trabajo desarrollamos un sistema de planificación de rutas en
redes viarias basado en redes neuronales. Se propone un algoritmo de planificación
de rutas con una serie de reglas y que utiliza una red neuronal para la predicción de
los nodos de que conforman la ruta. El sistema es aplicable al área geográfica de la
ciudad de Madrid y utiliza datos del tráfico en tiempo real proporcionados por el
Ayuntamiento de Madrid. El sistema es extensible, sencillo y utiliza tecnologías
estándar de modo que permita extensiones futuras. Se divide en una serie de
componentes que pueden ser reemplazados individualmente y se despliega en un
contenedor Docker. El algoritmo es capaz de generar rutas válidas en el 79,4% de las
rutas incluidas en conjunto de pruebas y el grueso de las rutas calculadas tienen una
longitud entre una y cuatro veces mayor que la longitud de la ruta óptima.