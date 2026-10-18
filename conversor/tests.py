from django.test import TestCase
from django.urls import reverse

from .utils import analizar_cadena_utf8, convertir_numero


class ConversorTests(TestCase):
    def test_conversiones_validas_en_las_cuatro_bases(self):
        esperado = {"decimal": "42", "binario": "00101010", "octal": "52", "hexadecimal": "2A"}
        for base, valor in ((2, "101010"), (8, "52"), (10, "42"), (16, "2A")):
            with self.subTest(base=base):
                self.assertEqual(convertir_numero(valor, base), {**esperado, "bits_significativos": 6, "bytes_requeridos": 1})

    def test_validacion_de_digitos_base_y_valor_maximo(self):
        for valor, base in (("102", 2), ("8", 8), ("G", 16), ("65536", 10)):
            with self.subTest(valor=valor, base=base), self.assertRaises(ValueError):
                convertir_numero(valor, base)

    def test_validacion_de_vacios_y_negativos(self):
        for valor in ("", "-1"):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                convertir_numero(valor, 10)

    def test_texto_utf8_con_enye(self):
        resultado = analizar_cadena_utf8("ñ")
        self.assertEqual(resultado, [{"caracter": "ñ", "decimal": 241, "unicode": "U+00F1", "hexadecimal": "F1", "bytes_hex": "C3 B1", "num_bytes": 2}])

    def test_post_conversion_muestra_bits_y_bytes(self):
        respuesta = self.client.post(reverse("conversor:index"), {"accion": "convertir", "numero": "256", "base": "10"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "0000000100000000")
        self.assertContains(respuesta, "Bytes requeridos:")

    def test_formulario_texto_valida_vacio_y_limite(self):
        url = reverse("conversor:index")
        vacio = self.client.post(url, {"accion": "analizar", "texto": ""})
        largo = self.client.post(url, {"accion": "analizar", "texto": "a" * 21})
        self.assertContains(vacio, "Ingresa texto; el campo no puede estar vacío")
        self.assertContains(largo, "no puede superar los 20 caracteres")
