
# Plantilla Universal de Prompt para Xami-CX_V1

## Introducción y contexto
**Descripción:** Explica el propósito del manual y su ámbito de aplicación. Incluye objetivos clave, audiencia y beneficios de usar la plantilla.  

Este manual describe en detalle la primera versión de la Plantilla Universal de Prompt para Xami-CX, diseñada para facilitar la creación y estandarizar agentes conversacionales en contextos simples y multi-agente.  

**Objetivos:**
- Documentar cada bloque de la plantilla y su propósito.
- Establecer un proceso claro de uso, validación y mantenimiento.
- Asegurar consistencia, gobernanza y alineación con criterios de negocio y auditoría interna.

**Audiencia:**
- Desarrolladores e ingenieros de prompts.  
- Equipos de QA y gobernanza de IA.  
- Consultores y responsables de despliegue en Xami-CX.  

---

## Visión general de la plantilla
**Descripción:** Ofrece una visión de alto nivel de la estructura modular de la plantilla, resaltando sus componentes principales y su interacción.  

La plantilla aporta un esqueleto YAML/texto que define:
- Metadatos esenciales del agente.
- Identidad, personalidad y tono de marca.
- Configuración de la Base de Conocimiento (BdC), ya sea interna o referenciada.
- Definición de flujos conversacionales, guard-rails de seguridad y manejo de PII.
- Mecanismos de ruteo y colaboración en arquitecturas multi-agente.
- Ajustes de observabilidad, memoria de contexto, escalamiento y checklist de despliegue.

Este enfoque modular permite:
- Reutilizar bloques comunes (BdC, guard-rails, PII).
- Herencia y especialización rápida de sub-agentes colaboradores.
- Auditoría automatizada con el Agente Validador (modelo o3) para garantizar calidad.

La estructura completa puede consultarse en el **“Xami-CX Agent Prompt Template”**.

---

## Estructura detallada de la plantilla

### A · Arquitectura de agentes
**Descripción:** Este bloque define la topología y las relaciones entre agentes dentro de Xami-CX.  
Permite especificar si tu solución es un agente único, un supervisor que rutea mensajes a sub-agentes o un colaborador que hereda configuraciones de un supervisor.  

```yaml
agent_type : "single"                # Valores: single | supervisor | supervisor_router | collaborator
team_name  : "{{TODO: Equipo}}"      # Nombre del equipo o línea de negocio

# Si agent_type == supervisor_router → añade:
sub_agents  : [...]                  # Lista de IDs de sub-agentes gestionados

# Si agent_type == collaborator → añade:
supervisor_ref : "ID_Supervisor"     # Referencia al agente supervisor
inherit_blocks : [...]               # Bloques heredados del supervisor
```

---

### B · Rol & Alcance
**Descripción:** Define la responsabilidad y el nivel de autoridad de cada agente dentro de la solución.  

```yaml
role            : "Descripción clara del rol"
authority_level : "full|partial|none"
allowed_actions : [
  "leer_BdC",
  "invocar_subagent",
  "hand-off_humano"
]
```

---

### C · Protocolo de Colaboración
**Descripción:** Define cómo los agentes intercambian información y gestionan la continuidad en arquitecturas multi-agente.  

```yaml
handshake     : "sessionAttributes JSON"
routing_logic : "ruleset|manual|LLM-router"
timeout_ms    : 4000
fallback      : "Derivar a asesor humano"
```

---

### D · Routing Rules
**Descripción:** Reglas de enrutamiento para un supervisor-router.  

```yaml
routing_rules:
  - intent   : ^(Consulta_Estatus|Ubicación_Actual|Generar_Reporte)$
    route_to : "SkyBot-Status"
    priority : 1
  - intent   : ^(Incidencia|Escalar_Humano)$
    route_to : "SkyBot-Incident"
    priority : 2
```

---

### E · Herencia de bloques
**Descripción:** Indica qué secciones son heredadas automáticamente por sub-agentes (collaborators).  

```yaml
inherit_blocks: ["Base de Conocimiento","Guard-rails","Manejo de PII"]
```

---

## Bloques principales (0–16)

| Bloque | Campos clave | Propósito |
|--------|--------------|-----------|
| 0. Metadatos | agent_name, version, language, author, last_updated, contact_owner, description, notes | Centralizar información de identificación, control de versiones y responsables. |
| 1. Identidad & Personalidad | tone, values, catch_phrases | Definir voz, estilo y elementos de marca. |
| 2. Objetivo de Negocio & Público | goal, audiences, key_kpis | Especificar propósito comercial, segmentos de usuario e indicadores clave. |
| 3. Base de Conocimiento | bdc_ref, bdc_version, bdc_note | Indicar fuente de datos y versión. |
| 4. Guard-rails & Política | Lista de políticas de seguridad | Definir restricciones y mecanismos de seguridad. |
| 5. Variables & Placeholders | {{variable}}, valores por defecto | Declarar parámetros dinámicos. |
| 6. Flujos Conversacionales | flows → id, trigger_keywords, steps, exit_condition | Describir lógica de diálogo. |
| 7. Formato de Respuesta | max_words, markdown, allowed_emojis | Establecer límites de longitud y formato. |
| 8. Manejo de PII | consent_phrase, email_regex, phone_regex, pii_destination | Configurar validación y destino seguro de datos personales. |
| 9. Herramientas / Power-Ups | tools → name, description, inputs, outputs, auth | Detallar integraciones con servicios externos. |
| 10. Ejemplos de Interacción | Casos de uso y adversariales | Validar flujos y defensa ante inyecciones. |
| 11. Errores & Fallback | default_error, no_intent, db_timeout | Definir mensajes de error y rutas alternativas. |
| 12. Checklist de Despliegue | Lista de ítems | Validar configuración antes de lanzamiento. |
| 13. Observabilidad & KPIs | log_events, metrics_targets | Especificar métricas y monitoreo. |
| 14. Memoria & Contexto | turn_window, store_session_vars, expiration_minutes | Configurar gestión de contexto. |
| 15. Política de Actualización de BdC | owner, refresh_cycle, process | Mantener actualizada la base de conocimiento. |
| 16. Criterios de Escalación Humana | handoff_conditions, handoff_channel, handoff_payload | Definir escenarios de derivación a humano. |

---

## Guía paso a paso de uso
1. Define tu objetivo funcional.  
2. Prepara tu meta-prompt con la instrucción base.  
3. Incluye toda la plantilla.  
4. Ajusta valores concretos.  
5. Solicita la generación del YAML completo.  
6. Revisa la salida.  
7. Valida con el Agente Validador (modelo o3).  
8. Aplica correcciones.  
9. Guarda el prompt como configuración de sistema.  
10. Despliega y prueba.  

---

## Ejemplos de Meta-Prompt

### Ejemplo 1: Agente simple
```yaml
Usa la Plantilla Universal Xami-CX para crear el prompt de sistema de un agente.
Objetivo funcional: "Precalificar créditos personales según ingreso y edad del solicitante."

agent_name: "CrediBot MX"
version: "v1.0"
language: "es"

Genera el prompt de sistema completo en formato YAML.
```

### Ejemplo 2: Supervisor con routing
```yaml
Usa la Plantilla Universal Xami-CX para crear el prompt de sistema de un supervisor-router.
Objetivo funcional: "Orquestar rutas de consulta de estado e incidencias para SkyBot-Suite."

agent_type: "supervisor_router"
team_name: "SkyBot-Suite"
sub_agents:
  - "SkyBot-Status"
  - "SkyBot-Incident"
version: "v1.0"
language: "es"

Genera el prompt de sistema completo en formato YAML.
```

---

## Buenas prácticas y patrones
- Usar **snake_case** para identificadores.  
- Nunca dejar valores como “X días” sin placeholder.  
- Compartir BdC, guard-rails y PII entre colaboradores.  
- Prompts deterministas (temp 0–0.2).  
- Tag de Git y version en metadatos.  
- Testing adversarial obligatorio.  
