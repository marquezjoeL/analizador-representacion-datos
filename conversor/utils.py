"""Conversiones numéricas y análisis de texto UTF-8."""

BASES = (2, 8, 10, 16)
MAXIMO = 65_535


def convertir_numero(valor, base=10):
    """Valida un número escrito en ``base`` y devuelve sus representaciones."""
    if base not in BASES:
        raise ValueError("Selecciona una base válida: 2, 8, 10 o 16.")
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError("Ingresa un número; el campo no puede estar vacío.")
    valor = valor.strip()
    if valor.startswith("-"):
        raise ValueError("No se permiten números negativos.")
    if valor.startswith("+"):
        valor = valor[1:]
    try:
        numero = int(valor, base)
    except ValueError:
        raise ValueError(f"El número contiene dígitos inválidos para la base {base}.") from None
    if numero > MAXIMO:
        raise ValueError("El valor no puede ser superior a 65,535.")
    binario = format(numero, "b")
    bits_significativos = len(binario)
    bits_alineados = ((bits_significativos + 7) // 8) * 8
    binario_completo = binario.zfill(bits_alineados)
    return {
        "decimal": str(numero), "binario": binario_completo,
        "octal": format(numero, "o"), "hexadecimal": format(numero, "X"),
        "bits_significativos": bits_significativos,
        "bytes_requeridos": bits_alineados // 8,
    }


def analizar_cadena_utf8(texto):
    """Describe cada carácter Unicode y su secuencia de bytes UTF-8."""
    if not isinstance(texto, str):
        raise TypeError("El valor debe ser texto.")
    if not texto:
        raise ValueError("Ingresa texto; el campo no puede estar vacío.")
    if len(texto) > 20:
        raise ValueError("El texto no puede superar los 20 caracteres.")
    resultado = []
    for caracter in texto:
        bytes_utf8 = caracter.encode("utf-8")
        resultado.append({
            "caracter": caracter, "decimal": ord(caracter),
            "unicode": f"U+{ord(caracter):04X}",
            "hexadecimal": f"{ord(caracter):X}",
            "bytes_hex": " ".join(f"{byte:02X}" for byte in bytes_utf8),
            "num_bytes": len(bytes_utf8),
        })
    return resultado
