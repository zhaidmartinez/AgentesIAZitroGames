📘 Documentación de Índice de Base de Conocimiento (BdC) para Xami-CX

Este documento describe la sección Base de Conocimiento (BdC) de la plantilla universal de prompt, detallando su estructura, tipos de assets, esquemas, mantenimiento y consumo por parte de los agentes.

1. Introducción a la BdC
Objetivo

Definir qué es la BdC, su función en Xami-CX y cómo interactúan los agentes con ella.

Funciones principales

Centralizar todos los recursos: documentos, datos tabulares, diccionarios, APIs y datos de simulación.

Facilitar al agente la búsqueda correcta y precisa de información.

Capacidades del agente

El agente puede:

Aplicar búsqueda semántica (embeddings) sobre documentos no estructurados.

Leer datos tabulares (CSV, JSON, Excel).

Generar y ejecutar SQL dinámico usando el diccionario de datos.

Invocar endpoints REST o Lambdas para obtener datos en tiempo real.

Usar datos simulados cuando está habilitado simulation_mode.

Casos de uso

Búsqueda semántica sobre PDF/Word.

Lectura de catálogos en CSV/JSON.

Generación dinámica de consultas SQL.

Invocación de APIs externas.

Simulación controlada de datos.

2. Tipos de Assets en la BdC
Tipo	Bloque	Uso
Documentos no estructurados	UnstructuredAssets	Manuales, políticas, guías
Datos tabulares	StructuredAssets	CSV, JSON, YAML, Excel
Diccionario de datos	DataDictionary	Estructura de tablas y columnas
Endpoints en tiempo real	RealtimeEndpoints	APIs REST/Lambda
Datos de simulación	SimulationData	Datos mock para demo
3. Esquema detallado de cada asset

Cada asset incluye:

Campos obligatorios

Campos opcionales

Tipos de datos

Ejemplo YAML

3.1 UnstructuredAssets

Documentos no estructurados utilizados para búsquedas semánticas.

Campos

id

title

format — pdf, docx, md, txt

path_or_url

description

tags

updated_at

access — public, restricted

Ejemplo
UnstructuredAssets:
  - id: "doc_manual_onboarding"
    title: "Manual de Onboarding"
    format: pdf
    path_or_url: "http://dominio.com/public/manual_onboarding.pdf"
    description: "Proceso de inducción y políticas internas."
    tags: [onboarding, rrhh]
    updated_at: 2025-06-01
    access: restricted

3.2 StructuredAssets

Assets con datos tabulares.

Recomendaciones

Incluir row_count para optimizar paginación.

Definir primary_key.

Indicar formato (csv, json, yaml, excel).

Ejemplo
StructuredAssets:
  - id: "csv_ventas"
    name: "ventas_2024"
    format: csv
    columns:
      - { name: "id_venta", type: int }
      - { name: "fecha", type: date }
      - { name: "total", type: decimal(10,2) }
    row_count: 15000
    primary_key: id_venta
    updated_at: 2025-06-25

3.3 DataDictionary

Describe la estructura interna de tablas o vistas.

Beneficios

Permite generar SQL correctamente.

Valida columnas y tipos.

Documenta relaciones PK/FK.

Facilita consultas complejas.

Campos obligatorios

id

schema

columns

Opcionales

length

primary_key

foreign_keys

description

Ejemplo
DataDictionary:
  - id: "tabla_usuarios"
    schema: "public"
    description: "Información de usuarios registrados en la plataforma"
    columns:
      - { name: "user_id", type: "uuid", primary_key: true }
      - { name: "nombre", type: "varchar", length: 100 }
      - { name: "email", type: "varchar", length: 200 }
    foreign_keys:
      - { column: "role_id", references_table: "roles", references_column: "id" }

3.6 SimulationData

Datos ficticios que se usan cuando simulation_mode: true.

simulation_mode: true
SimulationData:
  estados_envio_demo:
    - "En tránsito"
    - "Entregado"
  ciudades_mx_demo:
    - { ciudad: "Querétaro", lat: 20.6, lon: -100.4 }

4. Versionado y mantenimiento de la BdC
bdc_version: "v1.0"
last_full_refresh: 2025-06-25
contact_owner: "dataops@empresa.com"

Proceso de actualización

Actualizar assets/YAML.

Incrementar versión.

Registrar last_full_refresh.

Notificar al equipo y re-entrenar agentes.

5. Cómo consume el agente la BdC

Búsqueda semántica → UnstructuredAssets

Lectura directa de datos → StructuredAssets

Generación de SQL → DataDictionary

Simulación → SimulationData

Fallbacks

Si un asset no existe → informar error + proponer human-handoff.

6. Ejemplo completo: kb_skyangel.yaml
bdc_version: "v1.0"
last_full_refresh: 2025-06-25
contact_owner: "dataops@skyangel.mx"
total_assets: 7

UnstructuredAssets:
  - id: "doc_prod_manual"
    title: "Manual de Servicio SkyAngel 2025"
    format: pdf
    path_or_url: "https://dominio.com/skyangel-docs/manual_servicio_2025.pdf"
    description: "Descripción de productos, SLA y protocolos de rastreo."
    tags: [manual, sla, protocolos]
    updated_at: 2025-05-12
    access: public

  - id: "doc_politicas_inc"
    title: "Política de Incidencias y Recuperación de Activos"
    format: pdf
    path_or_url: "https://dominio.com/skyangel-docs/politicas_incidencias.pdf"
    description: "Pasos formales ante robos, extravío o siniestros."
    tags: [incidencias, seguridad]
    updated_at: 2025-04-30
    access: restricted

StructuredAssets:
  - id: "csv_estados_envio"
    name: "catalogo_estados_envio"
    format: csv
    columns:
      - { name: "estado_logistico", type: varchar }
      - { name: "descripcion", type: varchar }
    row_count: 4
    primary_key: estado_logistico
    updated_at: 2025-06-25

  - id: "csv_ciudades_mx"
    name: "catalogo_ciudades_mx"
    format: csv
    columns:
      - { name: "ciudad", type: varchar }
      - { name: "lat", type: decimal(8,5) }
      - { name: "lon", type: decimal(8,5) }
    row_count: 32
    primary_key: ciudad
    updated_at: 2025-06-22

DataDictionary:
  - id: "tabla_usuarios"
    schema: "public"
    description: "Información de usuarios registrados en la plataforma"
    columns:
      - { name: "user_id", type: uuid, primary_key: true, description: "ID único" }
      - { name: "nombre", type: varchar, length: 100, description: "Nombre completo" }
      - { name: "email", type: varchar, length: 200, description: "Correo electrónico" }
    foreign_keys:
      - { column: "role_id", references_table: "roles", references_column: "id" }

  - id: "roles"
    schema: "public"
    description: "Catálogo de roles de usuario"
    columns:
      - { name: "id", type: uuid, primary_key: true, description: "ID de rol" }
      - { name: "rol", type: varchar, length: 50, description: "Nombre del rol" }

  - id: "permisos"
    schema: "public"
    description: "Permisos asociados a roles"
    columns:
      - { name: "perm_id", type: uuid, primary_key: true, description: "ID de permiso" }
      - { name: "role_id", type: uuid, description: "Referencia a roles.id" }
      - { name: "perm_name", type: varchar, length: 100, description: "Nombre del permiso" }
    foreign_keys:
      - { column: "role_id", references_table: "roles", references_column: "id" }

SimulationData:
  simulation_mode: false
  estados_envio_demo:
    - "En tránsito"
    - "Entregado"
    - "Demorado por clima"
  ciudades_mx_demo:
    - { ciudad: "Querétaro", lat: 20.5939, lon: -100.392 }
    - { ciudad: "San Luis Potosí", lat: 22.1511, lon: -100.981 }
    - { ciudad: "Monterrey", lat: 25.6866, lon: -100.316 }