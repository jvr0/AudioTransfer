# AudioTransfer

Software para la extracción de información de la base de datos de Discogs.
Dados un máximo de 25 ids numéricos, separados por "," y sin espacios. 
Dado una referencia interna (normalmente de 6 caracteres).

Tras pasar las validaciones se activa el botón para el acceso a la API de Discogs. Se envian los id en una lista de strings, cada id del lanzamiento tiene la misma referencia asignada. Se recoge la info en Discogs de cada id, se guarda en una nueva row. Al finalizar el proceso se construye el excel y se habilita el botón de descarga. Para cada row se establece un tiempo de espera de 3 segundos para no sobrecargar la API.