# Weather Webservice

Cet exercice est à destination d'élèves souhaitant s'entrainer à réaliser un web service.
Un exemple en python vous a été fourni mais toute technologie est acceptée.

## Sujet

Implémentez un web service qui retourne la météo prévisionnelle française à partir d'un code postal.
Ce code postal français doit être communiqué en passation de paramètre d'url.

Ainsi, votre service doit répondre à une route : <domain.tld>/weather?zipcode={zip}

Et retourner uniquement les informations suivantes :

- La température actuelle
- La température min et max de la journée
- La météo

A titre d'exemple, vous pouvez vous baser sur l'api de [openweathermap.org](https://home.openweathermap.org). Si vous préférez une autre API libre à vous !

Afin d'optimiser les requêtes, la réponse fournie par l'API doit être stockée au sein d'une base de données de votre choix.

Si la requête a déjà été réalisée dans un laps de temps court (par défaut: 15 minutes), le web service ne requêtera pas de nouveau l'api et retournera les informations issues depuis la base de données.

La réponse doit avoir un format en JSON. L'entête du content type doit être présent.

Afin d'avoir un travail vraiment abouti, le laps de temps de 15 minutes doit être paramétrable.

## Conseils

Il est d'usage pour toute API consommable d'utiliser des clés API.
Attention à ne pas stocker cette clé au sein du dépôt GIT. Assurez-vous donc de la stocker dans un fichier `.env` et de fournir un fichier `.env.sample` au correcteur afin qu'il n'ait pas besoin de deviner le nom des constantes ou les valeurs attendues.

Si vous avez utilisé une autre API que celle proposée et que vous voulez être sympa avec le formateur, merci de le prévenir et de lui indiquer comment procéder.
