# -*- coding: utf-8 -*-
"""Per-city data for the Eje Cafetero landing pages.

Delivery tiers come from the coverage section of the main page, so they cannot
contradict it. Altitudes are the published municipal figures; the feeding notes
follow from altitude and climate, which is the one thing that genuinely differs
between these towns and actually matters for how much a dog eats.

Distances are approximate road distances from Armenia.

tier:
  free    - free delivery from 5kg, $4,000 on smaller orders (Armenia only)
  local   - delivery available, cost quoted on WhatsApp (rest of Quindío)
  request - shipped on request, 5kg minimum, cost quoted (Risaralda / Caldas)
"""

CITIES = [
 dict(slug='armenia', name='Armenia', dept='Quindío', tier='free', km=0, alt=1483,
      near=['calarca', 'circasia', 'la-tebaida', 'montenegro'],
      blurb='Armenia es nuestra base. Aquí pesamos, empacamos y salimos a repartir todos los días, '
            'así que es la ciudad donde más rápido llega el pedido.',
      local='Cubrimos toda la ciudad: el centro, Laureles, La Castellana, El Bosque, Las Colinas, '
            'Génova, La Adiela y los conjuntos de la avenida Bolívar y la vía Armenia–Pereira.',
      climate='A 1.483 metros sobre el nivel del mar, Armenia tiene un clima templado bastante estable '
              'durante todo el año. Es el punto medio del Quindío: los perros no gastan energía extra '
              'para calentarse como en Salento, ni pierden el apetito por calor como en La Tebaida. '
              'Las porciones de la tabla estándar funcionan bien acá sin ajustes.',
      logistics='Como salimos desde acá, en Armenia solemos entregar el mismo día si el pedido entra '
                'temprano. El domicilio es gratis desde 5kg, y los pedidos más pequeños tienen un costo '
                'de $4,000.'),
 dict(slug='calarca', name='Calarcá', dept='Quindío', tier='local', km=5, alt=1536,
      near=['armenia', 'la-tebaida', 'circasia'],
      blurb='Calarcá está prácticamente pegado a Armenia, subiendo hacia la cordillera por la vía a '
            'la Línea. Es de los municipios donde más pedidos repetidos tenemos.',
      local='Entregamos en el centro, en los barrios de la salida a la Línea, en La Bella y en las '
            'veredas cercanas a la vía principal.',
      climate='A 1.536 metros, Calarcá es apenas un poco más fresco que Armenia. Las noches bajan más '
              'que en el resto del valle, sobre todo subiendo hacia la cordillera, así que un perro que '
              'duerme afuera puede necesitar el extremo alto de su rango de porción.',
      logistics='Al estar a cinco kilómetros, los pedidos de Calarcá salen junto con la ruta de Armenia '
                'y suelen llegar el mismo día o al siguiente.'),
 dict(slug='circasia', name='Circasia', dept='Quindío', tier='local', km=10, alt=1750,
      near=['armenia', 'filandia', 'montenegro'],
      blurb='Circasia queda al norte de Armenia, camino a Filandia, en una de las zonas más verdes '
            'y de más fincas del Quindío.',
      local='Entregamos en el casco urbano y en las fincas y condominios de la vía Armenia–Circasia '
            'y del camino a Filandia.',
      climate='A 1.750 metros ya se siente el cambio: Circasia es notablemente más fresco que Armenia, '
              'con mañanas frías y mucha humedad. Un perro que vive a la intemperie quema más energía '
              'manteniendo su temperatura, y suele necesitar entre 5% y 10% más de alimento que el mismo '
              'perro en el valle.',
      logistics='Circasia entra en nuestra ruta del norte, la misma que cubre Filandia. El costo del '
                'envío se confirma por WhatsApp según la dirección, porque muchas entregas son a fincas.'),
 dict(slug='montenegro', name='Montenegro', dept='Quindío', tier='local', km=12, alt=1294,
      near=['armenia', 'quimbaya', 'la-tebaida'],
      blurb='Montenegro está al occidente de Armenia, en plena zona de fincas cafeteras y de turismo '
            'rural, cerca del Parque del Café.',
      local='Cubrimos el casco urbano y las fincas de la vía a Pueblo Tapao, al Parque del Café y al '
            'corregimiento de El Cuzco.',
      climate='A 1.294 metros, Montenegro es más cálido que Armenia. En clima cálido muchos perros '
              'comen algo menos al mediodía y recuperan el apetito en la tarde, así que conviene '
              'repartir la ración en dos comidas y dejar siempre agua fresca disponible.',
      logistics='Montenegro comparte ruta con Quimbaya. Confirmamos el costo del envío por WhatsApp, '
                'y muchas entregas van directamente a fincas de la zona.'),
 dict(slug='la-tebaida', name='La Tebaida', dept='Quindío', tier='local', km=15, alt=1183,
      near=['armenia', 'montenegro', 'calarca'],
      blurb='La Tebaida es el municipio más bajo y más cálido del Quindío, con la zona franca y el '
            'aeropuerto El Edén a un lado.',
      local='Entregamos en el casco urbano, en la zona franca, en Pisamos y en los condominios de la '
            'vía al aeropuerto y a Maravélez.',
      climate='A 1.183 metros es el punto más caliente del departamento, y eso se nota en el plato. '
              'Con calor los perros comen más despacio y a veces dejan comida al mediodía; no significa '
              'que estén enfermos. Alimenta temprano en la mañana y al caer la tarde, y no dejes el '
              'alimento al sol, porque en este clima pierde aroma más rápido.',
      logistics='La Tebaida entra en la ruta del sur junto con Montenegro. El costo del envío se '
                'confirma por WhatsApp según la dirección.'),
 dict(slug='quimbaya', name='Quimbaya', dept='Quindío', tier='local', km=25, alt=1339,
      near=['montenegro', 'filandia', 'armenia'],
      blurb='Quimbaya está al noroccidente del Quindío, cerca del límite con el Valle del Cauca y '
            'del Parque Panaca.',
      local='Llegamos al casco urbano y a las fincas de la vía a Panaca, a Puerto Alejandría y al '
            'corregimiento de Pueblo Tapao.',
      climate='A 1.339 metros el clima es cálido y húmedo. La humedad es el enemigo del alimento seco: '
              'un bulto abierto y mal tapado pierde aroma en pocos días y el perro empieza a comer con '
              'desgana. Un recipiente hermético cambia por completo la duración del producto acá.',
      logistics='Quimbaya está a unos 25 kilómetros y comparte ruta con Montenegro. Coordinamos la '
                'entrega por WhatsApp, normalmente con uno o dos días de anticipación.'),
 dict(slug='filandia', name='Filandia', dept='Quindío', tier='request', km=25, alt=1923,
      near=['circasia', 'quimbaya', 'salento'],
      blurb='Filandia es pueblo patrimonio, mirador del Quindío y zona de fincas, con muchos hogares '
            'que tienen perros de trabajo además de mascotas.',
      local='Coordinamos entregas al casco urbano, al mirador y a las fincas de la vía a Cruces y '
            'a Quimbaya.',
      climate='A 1.923 metros Filandia es frío y muy húmedo buena parte del año. Un perro que pasa el '
              'día afuera en este clima gasta bastante energía solo en mantener su temperatura, y suele '
              'necesitar el extremo alto de su rango. El pelaje también pide más grasa y proteína para '
              'mantenerse denso.',
      logistics='Filandia se despacha bajo pedido, con un mínimo de 5kg, y coordinamos el día por '
                'WhatsApp. Muchos clientes de acá piden para uno o dos meses de una vez.'),
 dict(slug='salento', name='Salento', dept='Quindío', tier='request', km=25, alt=1895,
      near=['filandia', 'circasia', 'armenia'],
      blurb='Salento y el Valle de Cocora son montaña, frío y caminata. Los perros de acá suelen ser '
            'mucho más activos que el promedio del departamento.',
      local='Coordinamos entregas al casco urbano y a las fincas, hospedajes y reservas de la vía a '
            'Cocora y a Boquía.',
      climate='A 1.895 metros el clima es frío y las jornadas al aire libre son largas. Frío más '
              'ejercicio es la combinación que más sube el consumo: un perro que camina a diario por '
              'Cocora puede necesitar entre 10% y 20% más de alimento que el mismo perro viviendo en un '
              'apartamento en Armenia.',
      logistics='Salento se despacha bajo pedido con mínimo de 5kg. Como la vía es de montaña, '
                'coordinamos el día con anticipación por WhatsApp.'),
 dict(slug='pereira', name='Pereira', dept='Risaralda', tier='request', km=45, alt=1411,
      near=['dosquebradas', 'santa-rosa-de-cabal', 'armenia'],
      blurb='Pereira es la ciudad más grande del Eje Cafetero y desde ahí nos escriben cada vez más '
            'dueños de perros de raza grande buscando precio por libra sin bajar la calidad.',
      local='Despachamos a toda la ciudad: Cuba, Álamos, Pinares, la Circunvalar, Los Alpes, Kennedy '
            'y la zona de Cerritos y la vía a Armenia.',
      climate='A 1.411 metros Pereira tiene un clima templado a cálido, muy parecido al de Armenia '
              'pero un poco más caliente en el día. Las porciones estándar funcionan bien, y en los '
              'meses más secos conviene revisar que el perro esté tomando suficiente agua.',
      logistics='Pereira se despacha bajo pedido con un mínimo de 5kg y el costo se cotiza por '
                'WhatsApp. Los envíos a Pereira y Dosquebradas salen juntos, así que si pides con un '
                'vecino se reparte el costo.'),
 dict(slug='dosquebradas', name='Dosquebradas', dept='Risaralda', tier='request', km=50, alt=1400,
      near=['pereira', 'santa-rosa-de-cabal'],
      blurb='Dosquebradas está pegado a Pereira, separado apenas por el viaducto, y funciona como una '
            'sola área urbana con ella.',
      local='Llegamos a La Badea, Los Naranjos, Santa Mónica, La Pradera, Frailes y el resto del '
            'área urbana.',
      climate='A 1.400 metros el clima es prácticamente el mismo de Pereira: templado, con días cálidos '
              'y noches frescas. No hace falta ajustar la porción por clima, solo por el peso y el nivel '
              'de actividad de tu perro.',
      logistics='Dosquebradas comparte despacho con Pereira, bajo pedido y con mínimo de 5kg. '
                'Cotizamos el envío por WhatsApp según la dirección.'),
 dict(slug='santa-rosa-de-cabal', name='Santa Rosa de Cabal', dept='Risaralda', tier='request', km=60, alt=1690,
      near=['pereira', 'dosquebradas', 'chinchina'],
      blurb='Santa Rosa de Cabal es zona fría y de fincas, famosa por sus termales y por el camino '
            'hacia el Nevado.',
      local='Coordinamos entregas al casco urbano y a las fincas de la vía a los termales, a Guacas '
            'y al camino hacia Chinchiná.',
      climate='A 1.690 metros el clima es fresco y llueve con frecuencia. En zonas húmedas el alimento '
              'seco se apelmaza si se guarda mal, así que acá insistimos más que en otros lados en '
              'usar un recipiente hermético y no dejar el bulto en el piso.',
      logistics='Santa Rosa se despacha bajo pedido con mínimo de 5kg, normalmente junto con la ruta '
                'de Pereira. Coordinamos el día por WhatsApp.'),
 dict(slug='chinchina', name='Chinchiná', dept='Caldas', tier='request', km=75, alt=1378,
      near=['manizales', 'santa-rosa-de-cabal'],
      blurb='Chinchiná está entre Manizales y Pereira, en el corazón cafetero de Caldas y sobre la '
            'vía que une a las dos ciudades.',
      local='Despachamos al casco urbano y a las fincas de la vía Manizales–Pereira y del sector de '
            'Alto de la Mina.',
      climate='A 1.378 metros Chinchiná es más cálido que Manizales, aunque estén a media hora. Si te '
              'mudaste de Manizales para acá, es normal que tu perro coma un poco menos al principio: '
              'el cambio de clima influye en el apetito más de lo que la gente cree.',
      logistics='Chinchiná se despacha bajo pedido con mínimo de 5kg, junto con la ruta de Manizales. '
                'El costo se cotiza por WhatsApp.'),
 dict(slug='manizales', name='Manizales', dept='Caldas', tier='request', km=90, alt=2150,
      near=['chinchina', 'santa-rosa-de-cabal', 'pereira'],
      blurb='Manizales es la capital de Caldas y la ciudad más alta y más fría del Eje Cafetero, '
            'con calles empinadas y mucha niebla.',
      local='Despachamos a toda la ciudad: Chipre, Palermo, La Enea, Milán, Villapilar, el centro y '
            'el sector de la Universidad.',
      climate='A 2.150 metros Manizales es la ciudad más fría de la región, y el frío sube el consumo '
              'de energía. Un perro que vive acá, sobre todo si duerme en patio o terraza, suele '
              'necesitar el extremo alto de su rango de porción. Las calles empinadas además hacen que '
              'un paseo normal en Manizales cueste más esfuerzo que el mismo paseo en Armenia.',
      logistics='Manizales es el punto más lejano que cubrimos, a unos 90 kilómetros. Se despacha bajo '
                'pedido con mínimo de 5kg y cotizamos el envío por WhatsApp. Muchos clientes de acá '
                'piden cantidades grandes para reducir el costo por libra y el número de envíos.'),
]

TIERS = {
 'free': dict(
    badge='Domicilio GRATIS',
    line='Domicilio <strong>gratis</strong> para pedidos de 5kg o más. Pedidos menores: $4,000.',
    faq='En Armenia el domicilio es gratis para pedidos de 5kg o más. Los pedidos menores tienen un '
        'costo de $4,000. Escríbenos por WhatsApp con tu dirección y coordinamos la entrega.'),
 'local': dict(
    badge='Envío disponible',
    line='Envío disponible. El costo se confirma por WhatsApp según tu dirección.',
    faq='Sí, entregamos en {city} con regularidad. El costo del envío se confirma por WhatsApp según tu '
        'dirección exacta, y en Armenia el domicilio es gratis desde 5kg.'),
 'request': dict(
    badge='Envío bajo pedido',
    line='Envío bajo pedido, con un <strong>mínimo de 5kg</strong>. El costo se cotiza por WhatsApp.',
    faq='Sí. Despachamos a {city} bajo pedido, con un mínimo de 5kg, y cotizamos el costo del envío por '
        'WhatsApp según tu dirección. Escríbenos al 312 673 7317 y te confirmamos el valor y el tiempo de entrega.'),
}
