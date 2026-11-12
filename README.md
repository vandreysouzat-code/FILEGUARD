# FILEGUARD



*Monitor de Integridade de Arquivos com Python*



O FILEGUARD é uma ferramenta desenvolvida em Python para monitorar a integridade de arquivos por meio de hashes SHA-256.



O projeto permite identificar alterações, arquivos novos e arquivos removidos em um diretório monitorado.



# Funcionalidades



\- Cálculo de hashes SHA-256.

\- Monitoramento de diretórios e subdiretórios.

\- Criação de referência de integridade em JSON.

\- Detecção de arquivos novos.

\- Detecção de arquivos modificados.

\- Detecção de arquivos removidos.

\- Tratamento de erros e JSON corrompido.

\- Testes automatizados com unittest.



\## Tecnologias



\- Python

\- hashlib

\- os

\- json

\- unittest



\## Como utilizar



Clone o repositório e entre na pasta do projeto.



\### Criar referência inicial



```bash

python fileguard.py baseline

```



\### Verificar integridade



```bash

python fileguard.py scan

```



O FILEGUARD compara os hashes atuais com a referência armazenada em `database.json`.



\## Testes automatizados



Execute:



```bash

python -m unittest -v

```



\## Estrutura do projeto



```text

FILEGUARD/

├── fileguard.py

├── test\_fileguard.py

├── .gitignore

├── README.md

├── database.json

└── monitorados/

```



\## Limitações de segurança



O FILEGUARD utiliza SHA-256 para identificar alterações no conteúdo dos arquivos.



A ferramenta não identifica o responsável pela alteração nem garante proteção contra um atacante que consiga modificar tanto os arquivos monitorados quanto o banco de referência.



O comando `baseline` atualiza a referência e deve ser utilizado somente quando o estado atual dos arquivos for considerado confiável.



\## Versão



1.0



\## Autor



Victor Andrey

