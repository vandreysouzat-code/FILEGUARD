
import unittest
import tempfile
import os
import json
import hashlib
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import fileguard


class TestFileGuard(unittest.TestCase):

    def test_calcular_hash(self):
        with tempfile.NamedTemporaryFile(delete=False) as arquivo:
            arquivo.write(b"FILEGUARD")
            caminho = arquivo.name

        try:
            resultado = fileguard.calcular_hash(caminho)
            esperado = hashlib.sha256(b"FILEGUARD").hexdigest()
            self.assertEqual(resultado, esperado)
        finally:
            os.remove(caminho)

    def test_analisar_diretorio(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = os.path.join(diretorio, "teste.txt")

            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write("Teste")

            resultado = fileguard.analisar_diretorio(diretorio)

            self.assertIn(caminho, resultado)

    def test_arquivo_integro(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = os.path.join(diretorio, "teste.txt")

            with tempfile.TemporaryDirectory() as pasta_banco:
                banco = os.path.join(pasta_banco, "database.json")

                with open(caminho, "w", encoding="utf-8") as arquivo:
                    arquivo.write("Original")

                hashes = fileguard.analisar_diretorio(diretorio)

                with open(banco, "w", encoding="utf-8") as arquivo:
                    json.dump(hashes, arquivo)

                with patch.object(fileguard, "DIRETORIO", diretorio):
                    with patch.object(fileguard, "BANCO", banco):
                        saida = StringIO()

                        with redirect_stdout(saida):
                            fileguard.verificar_integridade()

                self.assertIn(
                    "Todos os arquivos estão íntegros",
                    saida.getvalue()
                )

    def test_arquivo_modificado(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = os.path.join(diretorio, "teste.txt")

            with tempfile.TemporaryDirectory() as pasta_banco:
                banco = os.path.join(pasta_banco, "database.json")

                with open(caminho, "w", encoding="utf-8") as arquivo:
                    arquivo.write("Original")

                hashes = fileguard.analisar_diretorio(diretorio)

                with open(banco, "w", encoding="utf-8") as arquivo:
                    json.dump(hashes, arquivo)

                with open(caminho, "w", encoding="utf-8") as arquivo:
                    arquivo.write("Modificado")

                with patch.object(fileguard, "DIRETORIO", diretorio):
                    with patch.object(fileguard, "BANCO", banco):
                        saida = StringIO()

                        with redirect_stdout(saida):
                            fileguard.verificar_integridade()

                self.assertIn("ARQUIVO MODIFICADO", saida.getvalue())

    def test_json_corrompido(self):
        with tempfile.TemporaryDirectory() as diretorio:
            with tempfile.TemporaryDirectory() as pasta_banco:
                banco = os.path.join(pasta_banco, "database.json")

                with open(banco, "w", encoding="utf-8") as arquivo:
                    arquivo.write("JSON INVALIDO")

                with patch.object(fileguard, "DIRETORIO", diretorio):
                    with patch.object(fileguard, "BANCO", banco):
                        saida = StringIO()

                        with redirect_stdout(saida):
                            fileguard.verificar_integridade()

                self.assertIn("JSON está corrompido", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
