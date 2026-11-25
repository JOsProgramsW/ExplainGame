# Explain Game (`.egame`) — Metalenguaje para Niveles de Videojuegos

Lenguaje de Dominio Específico (DSL) declarativo desarrollado bajo metodología **Scrum** para describir, validar y estructurar escenarios de videojuegos.

## Equipo Scrum
- **Product Owner:** Victor Manuel Aldana Cazares
- **Scrum Master:** David Arturo Marquez Castro
- **Development Team (Lexer/Parser):** Miguel Alexander Camacho Lopez
- **Development Team (AST/Runtime):** Jose Carlos Hernandez Alvarez

## Estructura del Proyecto (Sprint 1)
- `lexer.py`: Analizador léxico con rastreo de línea y columna (`TECH-01`).
- `parser_sprint1.py`: Analizador sintáctico base para bloques `level` y `spawn` (`US-01`, `US-02`).
- `nivel_valido.egame`: Script de ejemplo escrito en Explain Game.
- `main.py`: Suite de pruebas y validación de escenarios.

## Ejecución
```bash
python main.py