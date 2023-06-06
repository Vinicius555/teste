import conexao
import re
from unidecode import unidecode

nome_padrao = r"^[a-zA-Z]+( [a-zA-Z]+)*$"


class Livros:
    def __init__(self, nomeLivro, nomeAutor, anoLivro, categoria):
        self.nome = nomeLivro
        self.autor = nomeAutor
        self.ano = anoLivro
        self.categoria = categoria


class CrudLivros:
    @staticmethod
    def criar_livros():
        try:
            while True:
                nome = input("NOME:")
                nomes = nome.split()

                if len(nomes) >= 1:
                    nome_completo = " ".join(nomes)
                    nome_sem_acentos = unidecode(nome_completo)
                    if re.match(nome_padrao, nome_sem_acentos):
                        break
                else:
                    print(
                        "ERROR!Digite os nomes cotendo apenas letras e um unico espaço entre eles."
                    )
            while True:
                autor = input("AUTOR:")
                nomes = autor.split()

                if len(nomes) >= 1:
                    nome_completo = " ".join(nomes)
                    nome_sem_acentos = unidecode(nome_completo)
                    if re.match(nome_padrao, nome_sem_acentos):
                        break
                else:
                    print(
                        "ERROR!Digite os nomes cotendo apenas letras e um unico espaço entre eles."
                    )
            while True:
                ano = input("ANO DE LANÇAMENTO:")
                if not ano.isdigit():
                    print("ERROR!Digite apenas Números.")
                elif len(ano) != 4:
                    print("ERROR!Esse ano não existe. Digite no formato xxxx.")
                else:
                    break
            while True:
                categoria = input("CATEGORIA DO LIVRO:")
                if not categoria.isalpha():
                    print("ERROR!Digite apenas Letras.")
                else:
                    break
        except conexao.error as ex:
            print(ex)
        else:
            conexao.cursor.execute(
                f"INSERT INTO livros VALUES (NULL,'{nome}','{autor}',{ano},'{categoria}')"
            )
            conexao.banco.commit()
            print("Livro adicionado com sucesso!")

    @staticmethod
    def ler_livros():
        try:
            conexao.cursor.execute("SELECT * FROM livros")
            livros = conexao.cursor.fetchall()

            for livro in livros:
                print("======================")
                print("ID:", livro[0])
                print("NOME DO LIVRO:", livro[1])
                print("AUTOR:", livro[2])
                print("ANO DE LANÇAMENTO:", livro[3])
                print("CATEGORIA:", livro[4])
                print("======================")

        except conexao.error as ex:
            print(ex)

    @staticmethod
    def ler_livro():
        try:
            while True:
                nome = input("Informe o nome do livro que deseja procurar:")
                conexao.cursor.execute(f"SELECT * FROM livros WHERE NomeLivro='{nome}'")
                livro = conexao.cursor.fetchall()
                if livro:
                    for livro in livro:
                        print("======================")
                        print("ID:", livro[0])
                        print("NOME DO LIVRO:", livro[1])
                        print("AUTOR:", livro[2])
                        print("ANO DE LANÇAMENTO:", livro[3])
                        print("CATEGORIA:", livro[4])
                        print("======================")
                        break
                else:
                    print("Livro não encontrado!")
                    print("1. Procurar de novo:")
                    print("2. lista livros")
                    print("3. sair")
                    perg = input("Oque deseja fazer:")
                    if perg == "1":
                        pass
                    elif perg == "2":
                        CrudLivros.ler_livros()
                    elif perg == "3":
                        break
                    else:
                        print("opção invalida!")

        except conexao.error as ex:
            print(ex)

    @staticmethod
    def atualizar_livro():
        try:
            id = int(input("Informe o ID:"))
            livro = conexao.cursor.execute(f"SELECT * FROM livros WHERE id={id}")

            if livro:
                for livro in livro:
                    print("======================")
                    print("ID:", livro[0])
                    print("NOME DO LIVRO:", livro[1])
                    print("AUTOR:", livro[2])
                    print("ANO DE LANÇAMENTO:", livro[3])
                    print("CATEGORIA:", livro[4])
                    print("======================")
                    break

                while True:
                    print(
                        "Digite os novos DADOS de cliente (ou deixe em branco para manter o valor atual):"
                    )
                    novo_nome = input(f"Novo Nome ({livro[1]})")
                    novo_autor = input(f"Novo CPF ({livro[2]})")
                    novo_ano = input(f"Novo Telefone ({livro[3]})")
                    novo_categoria = input(f"Nova Categoria ({livro[4]})")

                    novo_nome = novo_nome if novo_nome else livro[1]
                    novo_autor = novo_autor if novo_autor else livro[2]
                    novo_ano = novo_ano if novo_ano else livro[3]
                    novo_categoria = novo_categoria if novo_categoria else livro[4]

                    if not novo_nome.isalpha():
                        print("ERROR!O Nome do Livro deve conter apenas letras.")
                    elif not novo_autor.isalpha():
                        print("ERROR!O Nome do Autor deve conter apenas letras.")
                    elif novo_ano != 4:
                        print("ERROR! Ano Inválido. Digite no formato xxxx.")
                    elif not novo_ano.isdigit():
                        print("ERROR! O Ano deve conter apenas númereos.")
                    elif novo_categoria.isalpha():
                        print("ERROR! A categoria deve conter apenas letras.")
                    else:
                        conexao.cursor.execute(
                            f"UPDDATE livros SET NomeLivro='{novo_nome}' , NomeAutor={novo_autor},AnoLivro={novo_ano},Categoria={novo_categoria} WHERE id={id}"
                        )
                        conexao.banco.commit()
                        print("Livro Atualizado com sucesso!")
                        break
        except conexao.error as ex:
            print(ex)
        except ValueError:
            print("Erro: ID Inválido.")

    def deleta_livro(self, id):
        try:
            id = int(input("Informe o ID:"))
            livro = self.ler_livro(id)

            if livro and len(livro) > 0:
                print("======================")
                print("ID:", livro[0])
                print("NOME DO LIVRO:", livro[1])
                print("AUTOR:", livro[2])
                print("ANO DE LANÇAMENTO:", livro[3])
                print("CATEGORIA:", livro[4])
                print("======================")
            else:
                print("Livro não encontrado")
            perg = str(input(f"Deseja Deletar o cadastro do cliente (S/N):")).lower()
            if perg == "s":
                conexao.cursor.execute(f"DELETE FROM livros WHERE id={id}")
                conexao.banco.commit()
                print("Livro Deletado com Sucesso.")
            else:
                pass

        except ValueError:
            print("Erro: ID inválido.")
