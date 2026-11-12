
import os
import sys
import hashlib
import json

VERSAO = "1.0"
DIRETORIO = "monitorados"
BANCO = "database.json"


def calcular_hash(caminho):
    sha256 = hashlib.sha256()

    with open(caminho, "rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(4096), b""):
            sha256.update(bloco)

    return sha256.hexdigest()


def analisar_diretorio(diretorio):
    hashes = {}

    for raiz, pastas, arquivos in os.walk(diretorio):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            hashes[caminho] = calcular_hash(caminho)

    return hashes


def salvar_referencia(hashes):
    try:
        with open(BANCO, "w", encoding="utf-8") as arquivo:
            json.dump(hashes, arquivo, indent=4)

        print("Referência atualizada com sucesso.")

    except OSError as erro:
        print(f"ERRO ao salvar referência: {erro}")


def verificar_integridade():
    if not os.path.exists(BANCO):
        print("ERRO: Referência não encontrada. Execute baseline.")
        return

    try:
        hashes_atuais = analisar_diretorio(DIRETORIO)

        with open(BANCO, "r", encoding="utf-8") as arquivo:
            hashes_originais = json.load(arquivo)

    except json.JSONDecodeError:
        print("ERRO: O banco de dados JSON está corrompido.")
        return

    except OSError as erro:
        print(f"ERRO ao acessar arquivos: {erro}")
        return

    if not isinstance(hashes_originais, dict) or not all(
        isinstance(caminho, str) and isinstance(hash_arquivo, str)
        for caminho, hash_arquivo in hashes_originais.items()
    ):
        print("ERRO: Estrutura do banco de dados inválida.")
        return

    novos = hashes_atuais.keys() - hashes_originais.keys()
    removidos = hashes_originais.keys() - hashes_atuais.keys()

    modificados = [
        caminho for caminho in hashes_atuais
        if caminho in hashes_originais
        and hashes_atuais[caminho] != hashes_originais[caminho]
    ]

    for caminho in sorted(novos):
        print(f"NOVO ARQUIVO: {caminho}")

    for caminho in sorted(modificados):
        print(f"ARQUIVO MODIFICADO: {caminho}")

    for caminho in sorted(removidos):
        print(f"ARQUIVO REMOVIDO: {caminho}")

    if not novos and not modificados and not removidos:
        print("STATUS: Todos os arquivos estão íntegros.")


def main():
    print(f"FILEGUARD - Monitor de Integridade | v{VERSAO}")

    if not os.path.isdir(DIRETORIO):
        print("ERRO: Diretório monitorados não encontrado.")
        return

    if len(sys.argv) != 2:
        print("Uso: python fileguard.py [scan|baseline]")
        return

    comando = sys.argv[1].lower()

    if comando == "baseline":
        try:
            hashes = analisar_diretorio(DIRETORIO)
            salvar_referencia(hashes)

        except OSError as erro:
            print(f"ERRO ao analisar diretório: {erro}")

    elif comando == "scan":
        verificar_integridade()

    else:
        print("Comando inválido. Use scan ou baseline.")


if __name__ == "__main__":
    main()
