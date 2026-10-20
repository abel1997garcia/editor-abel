# Mapa de la biblioteca

Todos los textos están en `C:\Users\Clap\.claude\skills\consultor-verdad-interna\libros\` (un `.txt` por libro, extraído de los PDF originales de `C:\Users\Clap\Desktop\SANACION TRAUMAS\`). Busca con Grep (`-i`, `-C 15` o más) y lee el fragmento con Read (`offset`/`limit`) cuando necesites el contexto completo.

## Cómo buscar bien

- **Usa raíces, no palabras completas**: `rodill`, `migra[ñn]`, `estreñ`, `tiroid`, `lumbar|lumbago`, `ansiedad|angustia`. Los textos tienen tildes irregulares: prueba con y sin tilde (`est[oó]mago`).
- **Diccionario de Biodescodificación**: cada entrada empieza con el NOMBRE EN MAYÚSCULAS en su propia línea. Busca `^\s*RODILLA` (con `-i` desactivado si hay mucho ruido) y lee unas 60–120 líneas desde ahí. Una dolencia puede tener varias entradas (p. ej. `RODILLA`, `RODILLA, ARTROSIS`, `ESTREÑIMIENTO (LH-2)`): léelas todas. Cada entrada suele traer: etapa biológica, conflicto, "resentir" (la frase interna), y las versiones de Louise Hay, Jacques Martel y Lise Bourbeau.
- **Eybl (causas anímicas según Hamer)**: organizado por órgano/tejido. Busca el órgano (`rodilla`, `menisco`, `colon`, `tiroides`) y lee la sección: capa germinal, conflicto, fase activa vs. fase de curación, crisis.
- **Corbera – Visión cuántica del transgeneracional**: casos numerados ("Mujer, treinta y ocho años"). Busca el síntoma o el patrón y lee el caso entero: muestra cómo se encadenan síntoma, clan y resentir.
- **Wolynn – Este dolor no es mío**: busca "lenguaje core", "sentencia core", "frase" para el método de rastreo de miedos heredados, y el síntoma concreto si aparece.
- Si una búsqueda devuelve demasiado, añade otra palabra del contexto (`rodill.*(madre|padre|someti)`), o limita con `head_limit`.

## Qué hay en cada libro y cuándo consultarlo

### Diccionarios y mapas síntoma → conflicto (consúltalos SIEMPRE que haya un síntoma físico)
| Archivo | Qué aporta |
|---|---|
| `DICCIONARIO BIODESCODIFICACION.txt` | Joan Marc Vilanova. ~700 páginas. Recopila Corbera, Sellam, Flèche, tablas de Hamer, Louise Hay, Jacques Martel, Lise Bourbeau, Laura Armas, cromoterapia. Índice de enfermedades, protocolos, técnicas de PNL y anatomía. **La fuente principal para cualquier síntoma.** |
| `LAS CAUSAS animicas de las enfermedades 5 Björn Eybl segun las LEYES DE HAMER.txt` | Björn Eybl. Órgano por órgano según las 5 leyes de Hamer: tipo de conflicto, capa germinal, qué pasa en la fase activa y en la de curación. Sirve para distinguir si el síntoma indica conflicto activo o en reparación. |
| `NO ES POSIBLE CURARSE SIN APRENDER A VIVIR.txt` | Fernando Callejón y Guillermo Hernández Plata. Medicina psicobiológica: capítulos por sistemas, con conflictos y sentido biológico. Segunda opinión frente al diccionario. |
| `Descodificación biológica de los problemas digestivos.txt` | (Obtenido por OCR; puede tener errores de lectura.) Aparato digestivo de boca a ano, conflictos de "bocado". |
| `Sobrepeso-1.txt` | (Obtenido por OCR.) Sobrepeso, retención de líquidos, protección, carencia. |

### Transgeneracional, clan y lealtades (cuando algo se repite, hay fechas o edades que coinciden, o la persona "no se reconoce" en lo que vive)
| Archivo | Qué aporta |
|---|---|
| `¡AY MIS ANCESTROS!.txt` | Anne Ancelin Schützenberger. Síndrome de aniversario, lealtades invisibles, cripta y fantasma (secretos), hijos de sustitución, genosociograma. |
| `LEALTADES INVISIBLES.txt` | Boszormenyi-Nagy y Spark. El "libro mayor" familiar: deudas, méritos, lealtad, parentalización, justicia en el clan. |
| `ESTE DOLOR NO ES MIO.txt` | Mark Wolynn. Miedos y síntomas heredados; método del **lenguaje core** (queja core, descriptores core, frase core, trauma core). Las 4 dinámicas inconscientes: fusión con un padre, rechazo a un padre, ruptura del vínculo temprano con la madre, identificación con un miembro excluido. Ejercicios de frases sanadoras. |
| `VISION CUANTICA DEL TRANSGENERACIONAL-1.txt` | Enric Corbera y Rosa Rubio. Libro de casos de bioneuroemoción: síntoma + clan + resentir + resolución. Muy útil para ver ejemplos parecidos al de la persona. |
| `Bert Hellinger - Ordenes del Amor-1.txt` | Bert Hellinger. Constelaciones familiares: órdenes del amor (pertenencia, jerarquía, equilibrio entre dar y tomar), excluidos, implicaciones, frases de solución, pareja, hijos, culpa e inocencia. |
| `C4 Lectura 1 Transgeneracional.asd.txt` | Apuntes del curso: bases del transgeneracional. |
| `Lectura Mat 5 Mod. 2 C.txt` | Los **dobles** en el árbol (mismo nombre, fechas, número de hijo, parecido físico). |
| `Mat 5 Mod. 4 LecturaC3.txt` | Genograma y genosociograma: cómo construir el árbol y qué buscar. |
| `Lectura 3 Síndrome de aniversario.txt` | Síndrome de aniversario y ciclo biológico memorizado (Fréchet). |
| `PS Mod 1 Lectura 2 Lealtades familiares invisibles (2)C.txt`, `Resumen de Lealtades Familiares.txt` | Resúmenes de lealtades. |
| `gematria.txt` | Significado simbólico de los números (para fechas y edades que se repiten). Úsalo con prudencia y solo si la persona trae números o fechas. |
| `La Tora Completa.txt` | Texto de la Torá. Solo para referencias simbólicas o arquetípicas si la persona las busca. No es fuente diagnóstica. |

### Proyecto sentido (concepción, embarazo, parto y los primeros 3 años)
| Archivo | Qué aporta |
|---|---|
| `PS Mod 1 Lectura 1 Historia del Proyecto Sentido CC.txt` | Fréchet y el origen del concepto. |
| `PS Mod 2 Lectura Tipos de Proyecto Sentido Lectura 1 C.txt` | 6 tipos de proyecto sentido (Salomon Sellam). |
| `PS Mod 3 Lectura Tipos de hijos en PS C.txt` | Tipos de hijo (basurero, esponja, síntoma, yacente, reemplazo, bastón de la vejez, salvador, parentalizado, accidente, no deseado…) y **tipos de parto** (rápido, lento, tardío, cesárea, fórceps, inducido). |
| `PS Mod 4 Lectura 1 C2.txt`, `Tabla de trabajos en reparación.txt` | Profesiones como reparación del clan. |
| `Funciones de los roles paternos Mat 1 Mod 2.txt` | Funciones paternas (proteger, proveer, impulsar) y maternas (alimentar, dar amor, contener). |

### Leyes biológicas (Hamer) y conceptos base
| Archivo | Qué aporta |
|---|---|
| `Conceptos Básicos.txt` | DHS, conflicto programante y desencadenante, pistas o raíles, masa conflictual, simpaticotonía y vagotonía. |
| `Lectura 1a Ley Hamer.txt` … `Lectura 4a y 5a Ley Hamer.txt` | Las 5 leyes, lateralidad, capas germinales, recidivas, curación pendiente, alergias como pistas. |
| `Lectura Biología.txt` | Epigenética (Waddington) y bases biológicas. |
| `Simbolismos Inconscientes Mod. 2.txt` | Simbolismo padre/madre (arriba/abajo, aire/agua, alimentos, partes del cuerpo, lados). |
| `Nota de apoyo para el caso Mat4 Mod 1.asd.txt`, `Nota de apoyo para el caso Mat4 Mod 3.txt` | (OCR) Notas de casos del curso. |

### Mente, inconsciente, creencias y emociones
| Archivo | Qué aporta |
|---|---|
| `La Biología de la Creencia -1.txt` | Bruce Lipton. Epigenética, la membrana celular como "cerebro", el subconsciente programado de 0 a 7 años, crecimiento frente a protección, placebo y nocebo, paternidad consciente. |
| `El impacto de las emociones en el ADN-1.txt` | Nathalie Zammatteo. Emociones de embarazo, nacimiento y primer año en el ADN; reescribir la propia historia. |
| `Dejar ir. El camino a la liberación.txt` | David R. Hawkins. Mecanismo de rendición: soltar el sentimiento sin resistirlo ni contarse historias. **El mapa de la conciencia está en l.1224–1345**: cada nivel, de vergüenza 20 a paz 600, descrito por Hawkins, y la calibración de los chakras (l.1338). Mecanismos de supresión, expresión y escape. |
| `2. Lectura de Apoyo Emociones C.txt`, `Proceso para vivir las emociones.txt` | Emociones primarias (miedo, asco, ira, alegría, tristeza) y secundarias, y su función; proceso para sentirlas. |
| `Lectura El inconsciente C.txt`, `Módulo 1 Lectura Psicología C5.txt` | Inconsciente (Jung, Freud), mecanismos de defensa. |
| `Lectura 1…7 libro de texto Leyes Universales*.txt` | Los 7 principios del Kybalión: mentalismo, correspondencia, vibración, polaridad, ritmo, causa y efecto, género. |

### Hamer: material oficial de LearningGNM (carpeta `Hamer-LearningGNM/`, en español, de Caroline Markolin)
Es la fuente más fiel a Hamer. Para cualquier órgano, **consúltala junto a Eybl**.
| Archivo | Qué aporta |
|---|---|
| `Five_Biological_Laws_SP.txt` | Las cinco leyes completas, con ilustraciones descritas. |
| `Overview_SBS_SP.txt`, `SBS_Introduction_Sp.txt`, `Embryology_SP.txt`, `Brain_SP.txt` | Visión general de los programas, capas germinales y relés cerebrales. |
| Un archivo por órgano: `Bones_Joints_SP`, `Skeletal_Muscles_SP`, `Intestines_Rectum_SP`, `Stomach_Duodenum_SP`, `Liver_SP`, `Pancreas_SP`, `Kidneys_Bladder_SP`, `Heart_SP`, `Blood_Vessels_SP`, `Lungs_SP`, `Larynx_SP`, `Nose_Sinuses_SP`, `Mouth_Pharynx_SP`, `Pharyngeal_Ducts_SP`, `Esophagus_SP`, `Thyroid_SP`, `Eyes_SP`, `Ears_SP`, `Skin_SP`, `Connective_Tissue_SP`, `Fat_Tissue_SP`, `Periosteum_SP`, `Teeth_SP`, `Lymphatic_System_SP`, `Female_Breast_SP`, `Female_Sexual_Organs_SP`, `Male_Sexual_Organs_SP` | Para cada tejido: conflicto biológico exacto, fase activa, fase de curación, crisis épica y lateralidad. |
| `Schizophrenic_Constellations_SP.txt` | "Constelaciones": varios conflictos activos a la vez que explican estados psíquicos (depresión, manía, ansiedad, obsesiones, ataques de pánico, adicciones…). **Muy útil para patrones emocionales.** |
| `Allergies_Sp`, `Torn_from_my_Skin_Sp`, `Osteoporosis_Sp`, `What_are_Diseases_Sp`, `Reading_the_Brain_Sp`, `Madrid_2005_Sp`, `Explore_Article_Sp`, `GNM_Therapy_Sp` | Artículos: alergias y pistas, piel, osteoporosis, qué es la enfermedad, terapia GNM. |
| `Metastasis_Sp`, `Carcinogens_Sp`, `Toxins_Theory_Sp`, `Diet_Theory_Sp`, `Cancer_as_a_Fungus_Sp`, `Lanka_Bardens_Trial_Sp`, `Nature_of_Tumors_Sp`, `Understanding_Breast_Cancer_Sp`, `Understanding_Genetic_Diseases_Sp` | Críticas de Hamer a la medicina. No sirven para la lectura emocional y no se usan para opinar sobre tratamientos. |

### Bioneuroemoción (Corbera)
| Archivo | Qué aporta |
|---|---|
| `Corbera - Bioneuroemocion un metodo para el bienestar emocional.txt` | El PDF de la editorial El Grano de Mostaza (probablemente un extracto): el método, la coherencia emocional, el observador y la percepción. |
| `VISION CUANTICA DEL TRANSGENERACIONAL-1.txt` | (ya listado arriba) Casos. |

### Lipton: material oficial (carpeta `Lipton-web/`, en inglés)
Entrevistas, preguntas y respuestas, sinopsis de *The Biology of Belief* y el dossier de *The Honeymoon Effect* (el amor, la pareja y el subconsciente). Complementa al libro completo en español.

### Neville Goddard: manifestación e imaginación (carpeta `Neville-Goddard/`, en inglés, obras de 1939 a 1966)
| Archivo | Qué aporta |
|---|---|
| `1944_feeling_is_the_secret.txt` | La ley: el sentimiento es el secreto. El subconsciente acepta como real lo que se siente como real. Dormirse en la sensación del deseo cumplido. |
| `1952_the_power_of_awareness.txt` | "Yo soy": la conciencia como única realidad. Suponer el estado deseado, vivir en el final, revisión. |
| `1941_your_faith_is_your_fortune.txt`, `1939_at_your_command.txt` | El "yo soy" como Dios dentro, la Biblia como psicología, la fe como suposición. |
| `1945_prayer_the_art_of_believing.txt` | La oración como estado sentido, relajación y sugestión. |
| `1949_out_of_this_world.txt` | Pensar en cuatro dimensiones, suposiciones que se convierten en hechos. |
| `1952_the_creative_use_of_imagination.txt`, `1954_awakened_imagination_text.txt` | Imaginación despierta y técnica de **revisión** (reescribir el día o un recuerdo como debería haber sido). |
| `1956_seedtime_and_harvest.txt` | Siembra y cosecha: los estados interiores dan su fruto. |
| `1961_the_law_and_the_promise.txt` | Decenas de casos reales de la ley de la suposición. |
| `1966_freedom_for_all.txt` | Visión práctica de la ley de la suposición y la Biblia como psicología. |

### Napoleon Hill: éxito, propósito y acción (carpeta `Napoleon-Hill/`, en inglés, ediciones originales de dominio público)
| Archivo | Qué aporta |
|---|---|
| `1937_think_and_grow_rich.txt` | *Piense y hágase rico*: 13 pasos, los 6 pasos del deseo, autosugestión, **transmutación sexual** (busca `transmut`), mente maestra, sexto sentido, los **seis miedos** (busca `SIX BASIC FEARS`). |
| `1928_the_law_of_success.txt` | *La ley del éxito*: las 16 lecciones completas. Es texto de OCR y tiene algún error. Busca en inglés (`definite chief aim`, `self-confidence`, `master mind`, `failure`). |

### Apuntes propios
| Archivo | Qué aporta |
|---|---|
| `Apuntes - Dispenza y Hawkins (mapa de la conciencia).txt` | Resumen de las enseñanzas de Dispenza (sacado de su blog oficial y del conocimiento general de sus libros, porque **no hay libros suyos en la carpeta**) y una tabla del **mapa de la conciencia de Hawkins** (emoción, proceso y visión de la vida por nivel). El texto original del mapa está en `Dejar ir`, l.1224–1345: úsalo primero. Cuando uses Dispenza, di que viene de estos apuntes y no de un libro.
| `Apuntes - Medicina china (5 elementos) y chakras.txt` | **MTC**: cada elemento con sus órganos, emoción, virtud, aspecto del espíritu, tejidos, estación y **reloj horario de los órganos** (síntomas que se repiten a la misma hora); ciclos de generación y control. **Chakras**: los 7, cada uno con su tema, derecho, emoción que lo bloquea, señales, cuerpo y calibración de Hawkins. Todo con puentes a la biblioteca. |
| `Apuntes - Reiki y energía sexual.txt` | Reiki (Usui, los 5 principios, uso como autorregulación). **Energía sexual**: Hill (transmutación), el taoísmo (Jing, órbita microcósmica), el tantra, el efecto en la energía de la persona y su relación con **el inconsciente y los secretos sexuales del clan**, con preguntas para la consulta. |
| `Apuntes - Regulación del sistema nervioso (polivagal y trauma).txt` | Porges (ventral, simpático, dorsal; neurocepción, co-regulación), ventana de tolerancia, Levine (titulación, pendulación, descarga), van der Kolk. **Cómo detectar en qué estado está la persona**, herramientas de regulación paso a paso y **protocolo para trabajar el trauma sin desbordar**. |
| `Apuntes - Las 5 heridas (Bourbeau) y El Trabajo (Byron Katie).txt` | Las 5 heridas: rechazo, abandono, humillación, traición e injusticia, cada una con su máscara, edad, progenitor, cuerpo, vocabulario, miedo y señal de curación, y el proceso para sanarla. **Byron Katie**: las 4 preguntas, las inversiones y la hoja "Juzga a tu prójimo", aplicadas al resentir. |
| `Apuntes - Psicomagia y metagenealogía (Jodorowsky).txt` | Los principios para diseñar un acto psicomágico, la metagenealogía (qué buscar en el árbol, las 4 dimensiones) y **7 plantillas de actos simbólicos** construidas con esos principios. |
| `Apuntes - Prácticas validadas para sanar y liberar emociones.txt` | **Unas 30 prácticas**, cada una con su nivel de evidencia [A]–[D] y sus estudios, si es autoaplicable o necesita un profesional, los pasos, la dosis y qué esperar. Regulación, dejar ir, escritura expresiva, EFT, silla vacía, autocompasión, Byron Katie, TCC, EMDR, Experiencia Somática, IFS, hipnosis, constelaciones (con el ensayo de Heidelberg), Wolynn, rituales, WOOP, ensayo mental (y el estudio de Dispenza), la revisión de Neville, hábitos de 66 días, Tony Robbins, gratitud, ejercicio, yoga, mindfulness y reiki. **La sección 8 indica qué práctica usar en cada caso.** |
| `Apuntes - Seguimiento, plazos y efecto placebo.txt` | Por qué hay que medir; escalas SUDS, VOC, WHO-5 (completa), PHQ-9 y GAD-7, diario del síntoma y escala de objetivos; **plazos esperables** (de inmediato a 12 meses); **criterios de "funciona o hay que cambiar de camino"**; el **efecto placebo** (opioides, dopamina, condicionamiento, placebo abierto, nocebo, antidepresivos); y la **plantilla del plan de práctica**. |
| `Apuntes - Ejercicios para casa (niño interior, carta, espejo, priming, frío).txt` | **Ejercicios con guion para la llamada y tarea para casa**: el método de 3 pasos de **Federica Zani** (sentir al niño interior en el cuerpo, hablarle y la carta de liberación quemada), la carta a los padres, las preguntas de la ley del espejo y los ejercicios para la herida de humillación; 4 **meditaciones del niño interior** (incluida la reparación de una escena); frases diarias según la herida; **priming de Tony Robbins**; visualización con emoción elevada (Dispenza y Neville, con WOOP); 4 formas de **gratitud**; **ducha fría** progresiva (con la evidencia de 2025 y precauciones); espejo (Louise Hay), ho'oponopono, exploración corporal, movimiento de descarga, páginas matutinas; y un **ejemplo de plan semanal**. |
| `Apuntes - Neuroquímica, microbiota, alimentación y ayuno.txt` | **Dopamina** (equilibrio placer-dolor de Lembke, ayuno de dopamina), **serotonina** (el 90–95% intestinal no llega al cerebro), oxitocina, endorfinas, cortisol, GABA, BDNF y una **tabla de "qué química necesito"**; el **eje intestino-cerebro** (SMILES, fermentados de Stanford, 30 plantas); **Tim Spector**: los 5 principios y el **orden en el plato** (verdura, proteína, carbohidrato), el paseo después de comer, la glucosa y la energía; **ayuno**: evidencia honesta sobre la claridad mental, un protocolo progresivo y contraindicaciones; y un **plan de 4 semanas "cuerpo y ánimo"**. |
| `Apuntes - Rabia constructiva, ley del espejo y lateralidad.txt` | El protocolo **"rabia con propósito"** (reconocer, expresar con control, bajar, usar); **la ley del espejo y el equilibrio del inconsciente en el abuso** (lo que dicen Garza, Hellinger, Corbera y la investigación sobre revictimización, y cómo usarlo en orden y sin culpa); **lateralidad, energía masculina o femenina y estado hormonal**. |
| `Apuntes - Energía espiritual (vibración, prana, energía sexual, pecados capitales).txt` | Vibración y frecuencia emocional; **el prana de los alimentos** (sáttvico, rajásico y tamásico, y su coincidencia con la ciencia); **energía sexual y retención** (la tradición, la evidencia y una práctica de 30 a 90 días); **los 7 pecados capitales** como energía mal dirigida y su virtud, con una práctica semanal; prácticas espirituales de base. |
| `Apuntes - Rutina de energía y autoestima.txt` | **Rutina diaria completa**: mañana, alimentación, ayuno, movimiento y fuerza, energía sexual, espíritu y noche; los 5 hábitos de autoestima; un plan para empezar en 4 semanas. |

### Fuera de la biblioteca
- Cualquier otra fuente externa: dila como tal.
