import re

class LexicalError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"[LexicalError] Línea {line}, Columna {column}: {message}")
        self.line = line
        self.column = column

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, L:{self.line}, C:{self.column})"

class Lexer:
    KEYWORDS = {"level", "grid_size", "gravity", "spawn", "at"}

    TOKEN_SPECS = [
        ("COMMENT",    r"//[^\r\n]*"),
        ("NEWLINE",    r"\n"),
        ("SKIP",       r"[ \t\r]+"),
        ("FLOAT",      r"\d+\.\d+"),
        ("INTEGER",    r"\d+"),
        ("STRING",     r'"[^"\r\n]*"'),
        ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
        ("LBRACE",     r"\{"),
        ("RBRACE",     r"\}"),
        ("LPAREN",     r"\("),
        ("RPAREN",     r"\)"),
        ("COLON",      r":"),
        ("COMMA",      r","),
        ("MISMATCH",   r"."),  # Cualquier carácter no reconocido
    ]

    def __init__(self, source_code):
        self.source_code = source_code
        self.master_regex = re.compile(
            "|".join(f"(?P<{name}>{pattern})" for name, pattern in self.TOKEN_SPECS)
        )

    def tokenize(self):
        tokens = []
        line = 1
        line_start = 0

        for match in self.master_regex.finditer(self.source_code):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start + 1

            if kind == "NEWLINE":
                line += 1
                line_start = match.end()
            elif kind in ("SKIP", "COMMENT"):
                continue
            elif kind == "MISMATCH":
                raise LexicalError(f"Carácter ilegal '{value}'", line, column)
            else:
                if kind == "IDENTIFIER" and value in self.KEYWORDS:
                    kind = value.upper()
                elif kind == "STRING":
                    value = value[1:-1]  # Quitar comillas
                elif kind == "INTEGER":
                    value = int(value)
                elif kind == "FLOAT":
                    value = float(value)

                tokens.append(Token(kind, value, line, column))

        tokens.append(Token("EOF", None, line, 1))
        return tokens