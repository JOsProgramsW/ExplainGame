class SyntaxErrorDSL(Exception):
    def __init__(self, message, token):
        super().__init__(
            f"[SyntaxError] Línea {token.line}, Columna {token.column}: {message} (se encontró '{token.value}')"
        )

class Sprint1Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    @property
    def current(self):
        return self.tokens[self.pos]

    def consume(self, expected_type, error_msg=None):
        if self.current.type == expected_type:
            tok = self.current
            self.pos += 1
            return tok
        msg = error_msg or f"Se esperaba el token '{expected_type}'"
        raise SyntaxErrorDSL(msg, self.current)

    def parse(self):
        # US-01: Encabezado level "Nombre" { ... }
        self.consume("LEVEL", "El archivo debe iniciar con la palabra clave 'level'")
        level_name = self.consume("STRING", "Se esperaba el nombre del nivel entre comillas").value
        self.consume("LBRACE", "Se esperaba '{' después del nombre del nivel")

        level_data = {
            "level_name": level_name,
            "grid_size": None,
            "gravity": None,
            "entities": []
        }

        while self.current.type != "RBRACE" and self.current.type != "EOF":
            if self.current.type == "GRID_SIZE":
                level_data["grid_size"] = self._parse_grid_size()
            elif self.current.type == "GRAVITY":
                level_data["gravity"] = self._parse_gravity()
            elif self.current.type == "SPAWN":
                level_data["entities"].append(self._parse_spawn())
            else:
                raise SyntaxErrorDSL(
                    "Instrucción no válida dentro de 'level'. Se esperaba 'grid_size', 'gravity' o 'spawn'",
                    self.current
                )

        self.consume("RBRACE", "Falta cerrar el bloque 'level' con '}'")
        self.consume("EOF", "Contenido inesperado después de cerrar el bloque 'level'")
        return level_data

    def _parse_grid_size(self):
        self.consume("GRID_SIZE")
        self.consume("COLON", "Se esperaba ':' después de 'grid_size'")
        self.consume("LPAREN", "Se esperaba '(' para definir las dimensiones")
        width = self.consume("INTEGER", "El ancho de 'grid_size' debe ser un número entero").value
        self.consume("COMMA", "Se esperaba ',' separando ancho y alto en 'grid_size'")
        height = self.consume("INTEGER", "El alto de 'grid_size' debe ser un número entero").value
        self.consume("RPAREN", "Se esperaba ')' al finalizar 'grid_size'")
        return (width, height)

    def _parse_gravity(self):
        self.consume("GRAVITY")
        self.consume("COLON", "Se esperaba ':' después de 'gravity'")
        if self.current.type in ("INTEGER", "FLOAT"):
            val = self.current.value
            self.pos += 1
            return float(val)
        raise SyntaxErrorDSL("El valor de 'gravity' debe ser numérico (entero o decimal)", self.current)

    def _parse_spawn(self):
        # US-02: spawn Entidad at (x, y)
        self.consume("SPAWN")
        entity_type = self.consume("IDENTIFIER", "Se esperaba el tipo de entidad después de 'spawn'").value
        self.consume("AT", "Se esperaba la palabra clave 'at' después del tipo de entidad")
        self.consume("LPAREN", "Se esperaba '(' antes de las coordenadas")
        x = self.consume("INTEGER", "La coordenada X debe ser un entero").value
        self.consume("COMMA", "Se esperaba ',' entre las coordenadas X y Y")
        y = self.consume("INTEGER", "La coordenada Y debe ser un entero").value
        self.consume("RPAREN", "Se esperaba ')' después de la coordenada Y")
        return {"type": entity_type, "x": x, "y": y}