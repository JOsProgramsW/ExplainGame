from lexer import Lexer, LexicalError
from parser_sprint1 import Sprint1Parser, SyntaxErrorDSL

def run_test(title, code):
    print("=" * 60)
    print(f"PRUEBA: {title}")
    print("-" * 60)
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"1. [TECH-01 Lexer] OK -> {len(tokens)} tokens generados.")
        print(f"   Muestra de tokens: {tokens[:4]} ...")

        parser = Sprint1Parser(tokens)
        result = parser.parse()
        print("2. [US-01 & US-02 Parser] OK -> Nivel estructurado en memoria:")
        print(f"   Nombre: {result['level_name']}")
        print(f"   Grid: {result['grid_size']} | Gravedad: {result['gravity']}")
        print(f"   Entidades ({len(result['entities'])}): {result['entities']}")
    except (LexicalError, SyntaxErrorDSL) as e:
        print(f"ERROR CAPTURADO CORRECTAMENTE:\n   {e}")
    print()

if __name__ == "__main__":
    # Prueba 1: Archivo válido (nivel_valido.egame)
    with open("nivel_valido.egame", "r", encoding="utf-8") as f:
        valid_code = f.read()
    run_test("Nivel Válido (US-01 y US-02 Éxito)", valid_code)

    # Prueba 2: TECH-01 Escenario 2 (Carácter ilegal '@')
    bad_char_code = 'level "Test" {\n    grid_size: (10, 10)\n    @error\n}'
    run_test("TECH-01 Escenario 2: Carácter ilegal '@'", bad_char_code)

    # Prueba 3: US-01 Escenario 2 (Tipo inválido en gravity)
    bad_gravity_code = 'level "Test" {\n    gravity: "alta"\n}'
    run_test("US-01 Escenario 2: Tipo inválido en gravity", bad_gravity_code)

    # Prueba 4: US-02 Escenario 2 (Coordenada incompleta)
    bad_spawn_code = 'level "Test" {\n    spawn Enemy at (10)\n}'
    run_test("US-02 Escenario 2: Coordenada incompleta en spawn", bad_spawn_code)