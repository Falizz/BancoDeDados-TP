import mysql.connector
import streamlit as st
import pandas as pd

# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="apresentadorSupermercado",
    password="1234",
    database="Supermercado"
)

cursor = mydb.cursor()

# Menu principal na barra lateral
st.sidebar.title("Menu de Navegação")
aba_selecionada = st.sidebar.radio(
    "Selecione a aba:",
    ["Fornecedor", "Produto", "Cliente", "Registros de Compras", "Funcionário", "Função", "Equipe"]
)

# Aba Fornecedor
def fornecedor_app(cursor, mydb):
    st.title("Gestão de Fornecedores")
    
    # Sub-abas para organizar
    aba = st.radio("Escolha uma ação", ["Visualizar", "Adicionar", "Editar", "Excluir"])

    # Visualizar fornecedores
    if aba == "Visualizar":
        st.subheader("Lista de Fornecedores")
        cursor.execute("SELECT * FROM Fornecedor")
        fornecedores = cursor.fetchall()
        df = pd.DataFrame(fornecedores, columns=["Código", "Nome", "Telefone", "Endereço"])
        st.dataframe(df)

    # Adicionar fornecedor
    elif aba == "Adicionar":
        st.subheader("Adicionar Fornecedor")
        with st.form("AdicionarFornecedor"):
            nome = st.text_input("Nome")
            telefone = st.text_input("Telefone")
            endereco = st.text_input("Endereço")
            submit = st.form_submit_button("Adicionar")
        
        if submit:
            try:
                cursor.execute(
                    "INSERT INTO Fornecedor (FornecedorNome, FornecedorTelefone, FornecedorEndereco) VALUES (%s, %s, %s)",
                    (nome, telefone, endereco),
                )
                mydb.commit()
                st.success("Fornecedor adicionado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao adicionar fornecedor: {e}")

    # Editar fornecedor
    elif aba == "Editar":
        st.subheader("Editar Fornecedor")
        cursor.execute("SELECT FornecedorCodigo, FornecedorNome FROM Fornecedor")
        fornecedores = cursor.fetchall()
        fornecedor_dict = {nome: codigo for codigo, nome in fornecedores}
        fornecedor_nome = st.selectbox("Selecione o fornecedor para editar", fornecedor_dict.keys())
        
        if fornecedor_nome:
            fornecedor_codigo = fornecedor_dict[fornecedor_nome]
            novo_nome = st.text_input("Novo Nome", fornecedor_nome)
            novo_telefone = st.text_input("Novo Telefone")
            novo_endereco = st.text_input("Novo Endereço")
            if st.button("Salvar Alterações"):
                try:
                    cursor.execute(
                        "UPDATE Fornecedor SET FornecedorNome=%s, FornecedorTelefone=%s, FornecedorEndereco=%s WHERE FornecedorCodigo=%s",
                        (novo_nome, novo_telefone, novo_endereco, fornecedor_codigo),
                    )
                    mydb.commit()
                    st.success("Fornecedor atualizado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao editar fornecedor: {e}")

    # Excluir fornecedor
    elif aba == "Excluir":
        st.subheader("Excluir Fornecedor")
        cursor.execute("SELECT FornecedorCodigo, FornecedorNome FROM Fornecedor")
        fornecedores = cursor.fetchall()
        fornecedor_dict = {nome: codigo for codigo, nome in fornecedores}
        fornecedor_nome = st.selectbox("Selecione o fornecedor para excluir", fornecedor_dict.keys())
        
        if fornecedor_nome:
            fornecedor_codigo = fornecedor_dict[fornecedor_nome]
            if st.button("Excluir"):
                try:
                    cursor.execute("DELETE FROM Fornecedor WHERE FornecedorCodigo = %s", (fornecedor_codigo,))
                    mydb.commit()
                    st.success("Fornecedor excluído com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao excluir fornecedor: {e}")

# Aba Produto
def produto_app(cursor, mydb):
    st.title("Gestão de Produtos")
    
    # Sub-abas para organizar
    aba = st.radio("Escolha uma ação", ["Visualizar", "Adicionar", "Editar", "Excluir"])

    # Visualizar produtos
    if aba == "Visualizar":
        st.subheader("Lista de Produtos")
        query = """
            SELECT Produto.CodigoBarras, Produto.ProdutoNome, Produto.PrecoCusto, Produto.PrecoVenda, Fornecedor.FornecedorNome
            FROM Produto
            INNER JOIN Fornecedor ON Produto.FornecedorCodigo = Fornecedor.FornecedorCodigo
        """
        cursor.execute(query)
        produtos = cursor.fetchall()
        df = pd.DataFrame(produtos, columns=["Código de Barras", "Nome", "Preço de Custo", "Preço de Venda", "Fornecedor"])
        st.dataframe(df)

    # Adicionar produto
    elif aba == "Adicionar":
        st.subheader("Adicionar Produto")
        # Carregar fornecedores
        cursor.execute("SELECT FornecedorCodigo, FornecedorNome FROM Fornecedor")
        fornecedores = cursor.fetchall()
        fornecedor_dict = {nome: codigo for codigo, nome in fornecedores}

        with st.form("AdicionarProduto"):
            nome = st.text_input("Nome do Produto")
            preco_custo = st.number_input("Preço de Custo", min_value=0.0, format="%.2f")
            preco_venda = st.number_input("Preço de Venda", min_value=0.0, format="%.2f")
            fornecedor_nome = st.selectbox("Fornecedor", fornecedor_dict.keys())
            submit = st.form_submit_button("Adicionar")
        
        if submit:
            fornecedor_codigo = fornecedor_dict[fornecedor_nome]
            try:
                cursor.execute(
                    "INSERT INTO Produto (FornecedorCodigo, ProdutoNome, PrecoCusto, PrecoVenda) VALUES (%s, %s, %s, %s)",
                    (fornecedor_codigo, nome, preco_custo, preco_venda),
                )
                mydb.commit()
                st.success("Produto adicionado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao adicionar produto: {e}")

    # Editar produto
    elif aba == "Editar":
        st.subheader("Editar Produto")
        cursor.execute("SELECT CodigoBarras, ProdutoNome FROM Produto")
        produtos = cursor.fetchall()
        produto_dict = {nome: codigo for codigo, nome in produtos}
        produto_nome = st.selectbox("Selecione o produto para editar", produto_dict.keys())
        
        if produto_nome:
            produto_codigo = produto_dict[produto_nome]
            novo_nome = st.text_input("Novo Nome", produto_nome)
            novo_preco_custo = st.number_input("Novo Preço de Custo", min_value=0.0, format="%.2f")
            novo_preco_venda = st.number_input("Novo Preço de Venda", min_value=0.0, format="%.2f")
            cursor.execute("SELECT FornecedorCodigo FROM Produto WHERE CodigoBarras = %s", (produto_codigo,))
            fornecedor_atual = cursor.fetchone()[0]
            
            # Carregar fornecedores
            cursor.execute("SELECT FornecedorCodigo, FornecedorNome FROM Fornecedor")
            fornecedores = cursor.fetchall()
            fornecedor_dict = {nome: codigo for codigo, nome in fornecedores}
            fornecedor_nome = st.selectbox("Fornecedor", fornecedor_dict.keys(), index=list(fornecedor_dict.values()).index(fornecedor_atual))
            
            if st.button("Salvar Alterações"):
                try:
                    fornecedor_codigo = fornecedor_dict[fornecedor_nome]
                    cursor.execute(
                        "UPDATE Produto SET ProdutoNome=%s, PrecoCusto=%s, PrecoVenda=%s, FornecedorCodigo=%s WHERE CodigoBarras=%s",
                        (novo_nome, novo_preco_custo, novo_preco_venda, fornecedor_codigo, produto_codigo),
                    )
                    mydb.commit()
                    st.success("Produto atualizado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao editar produto: {e}")

    # Excluir produto
    elif aba == "Excluir":
        st.subheader("Excluir Produto")
        cursor.execute("SELECT CodigoBarras, ProdutoNome FROM Produto")
        produtos = cursor.fetchall()
        produto_dict = {nome: codigo for codigo, nome in produtos}
        produto_nome = st.selectbox("Selecione o produto para excluir", produto_dict.keys())
        
        if produto_nome:
            produto_codigo = produto_dict[produto_nome]
            if st.button("Excluir"):
                try:
                    cursor.execute("DELETE FROM Produto WHERE CodigoBarras = %s", (produto_codigo,))
                    mydb.commit()
                    st.success("Produto excluído com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao excluir produto: {e}")


# Aba Cliente
def cliente_app(cursor, mydb):
    st.title("Gestão de Clientes")

    # Sub-abas para organizar
    aba = st.radio("Escolha uma ação", ["Visualizar", "Adicionar", "Editar", "Excluir"])

    # Visualizar clientes
    if aba == "Visualizar":
        st.subheader("Lista de Clientes")
        query = "SELECT ClienteCadastro, ClienteNome, ClienteCPF, ClienteEndereco, ClienteTelefone FROM Cliente"
        cursor.execute(query)
        clientes = cursor.fetchall()
        df = pd.DataFrame(clientes, columns=["Cadastro", "Nome", "CPF", "Endereço", "Telefone"])
        st.dataframe(df)

    # Adicionar cliente
    elif aba == "Adicionar":
        st.subheader("Adicionar Cliente")
        with st.form("AdicionarCliente"):
            nome = st.text_input("Nome do Cliente")
            cpf = st.text_input("CPF")
            endereco = st.text_input("Endereço")
            telefone = st.text_input("Telefone")
            submit = st.form_submit_button("Adicionar")
        
        if submit:
            try:
                cursor.execute(
                    "INSERT INTO Cliente (ClienteNome, ClienteCPF, ClienteEndereco, ClienteTelefone) VALUES (%s, %s, %s, %s)",
                    (nome, cpf, endereco, telefone),
                )
                mydb.commit()
                st.success("Cliente adicionado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao adicionar cliente: {e}")

    # Editar cliente
    elif aba == "Editar":
        st.subheader("Editar Cliente")
        cursor.execute("SELECT ClienteCadastro, ClienteNome FROM Cliente")
        clientes = cursor.fetchall()
        cliente_dict = {nome: cadastro for cadastro, nome in clientes}
        cliente_nome = st.selectbox("Selecione o cliente para editar", cliente_dict.keys())
        
        if cliente_nome:
            cliente_cadastro = cliente_dict[cliente_nome]
            novo_nome = st.text_input("Novo Nome", cliente_nome)
            cursor.execute("SELECT ClienteCPF, ClienteEndereco, ClienteTelefone FROM Cliente WHERE ClienteCadastro = %s", (cliente_cadastro,))
            cliente_atual = cursor.fetchone()
            novo_cpf = st.text_input("Novo CPF", cliente_atual[0])
            novo_endereco = st.text_input("Novo Endereço", cliente_atual[1])
            novo_telefone = st.text_input("Novo Telefone", cliente_atual[2])
            
            if st.button("Salvar Alterações"):
                try:
                    cursor.execute(
                        "UPDATE Cliente SET ClienteNome=%s, ClienteCPF=%s, ClienteEndereco=%s, ClienteTelefone=%s WHERE ClienteCadastro=%s",
                        (novo_nome, novo_cpf, novo_endereco, novo_telefone, cliente_cadastro),
                    )
                    mydb.commit()
                    st.success("Cliente atualizado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao editar cliente: {e}")

    # Excluir cliente
    elif aba == "Excluir":
        st.subheader("Excluir Cliente")
        cursor.execute("SELECT ClienteCadastro, ClienteNome FROM Cliente")
        clientes = cursor.fetchall()
        cliente_dict = {nome: cadastro for cadastro, nome in clientes}
        cliente_nome = st.selectbox("Selecione o cliente para excluir", cliente_dict.keys())
        
        if cliente_nome:
            cliente_cadastro = cliente_dict[cliente_nome]
            if st.button("Excluir"):
                try:
                    cursor.execute("DELETE FROM Cliente WHERE ClienteCadastro = %s", (cliente_cadastro,))
                    mydb.commit()
                    st.success("Cliente excluído com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao excluir cliente: {e}")

# Aba Registros de Compras
def nota_fiscal_app(cursor, mydb):
    st.title("Gestão de Registros de Compras")

    # Sub-abas para organizar
    aba = st.radio("Escolha uma ação", ["Visualizar", "Adicionar"])

    # Visualizar notas fiscais
    if aba == "Visualizar":
        st.subheader("Registros de Compras")

        # Campo para CPF do cliente
        cpf_cliente = st.text_input("Filtrar por CPF do Cliente (deixe em branco para ver todos):")

        if cpf_cliente:  # Caso um CPF seja informado
            query = """
            SELECT nf.CodigoNota, p.ProdutoNome, c.ClienteNome, nf.NotaValor, nf.NotaPagamento, nf.NotaData
            FROM NotaFiscal nf
            INNER JOIN Produto p ON nf.CodigoBarras = p.CodigoBarras
            INNER JOIN Cliente c ON nf.ClienteCadastro = c.ClienteCadastro
            WHERE c.ClienteCPF = %s
            """
            cursor.execute(query, (cpf_cliente,))
        else:  # Exibir todos os registros se o CPF não for informado
            query = """
            SELECT nf.CodigoNota, p.ProdutoNome, c.ClienteNome, nf.NotaValor, nf.NotaPagamento, nf.NotaData
            FROM NotaFiscal nf
            INNER JOIN Produto p ON nf.CodigoBarras = p.CodigoBarras
            INNER JOIN Cliente c ON nf.ClienteCadastro = c.ClienteCadastro
            """
            cursor.execute(query)

        notas = cursor.fetchall()
        if notas:
            df = pd.DataFrame(notas, columns=["Código Nota", "Produto", "Cliente", "Valor", "Pagamento", "Data"])
            st.dataframe(df)
        else:
            st.info("Nenhum registro encontrado para o CPF informado.")

    # Adicionar Registros de Compras
    elif aba == "Adicionar":
        st.subheader("Adicionar ao Registros de Compras")
        
        # Selecionar Produto
        cursor.execute("SELECT CodigoBarras, ProdutoNome FROM Produto")
        produtos = cursor.fetchall()
        produto_dict = {nome: codigo for codigo, nome in produtos}
        produto_nome = st.selectbox("Selecione o Produto", produto_dict.keys())
        
        # Selecionar Cliente
        cursor.execute("SELECT ClienteCadastro, ClienteNome FROM Cliente")
        clientes = cursor.fetchall()
        cliente_dict = {nome: cadastro for cadastro, nome in clientes}
        cliente_nome = st.selectbox("Selecione o Cliente", cliente_dict.keys())
        
        nota_valor = st.number_input("Valor da Nota", min_value=0.0, step=0.01)
        nota_pagamento = st.text_input("Forma de Pagamento")
        nota_data = st.date_input("Data da Nota")

        if st.button("Adicionar"):
            try:
                cursor.execute(
                    """
                    INSERT INTO NotaFiscal (CodigoBarras, ClienteCadastro, NotaValor, NotaPagamento, NotaData)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (produto_dict[produto_nome], cliente_dict[cliente_nome], nota_valor, nota_pagamento, nota_data),
                )
                mydb.commit()
                st.success("Registros de Compras adicionada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao adicionar Registros de Compras: {e}")

def funcionario_app(cursor, mydb):
    st.subheader("Gestão de Funcionários")
    
    # Seleção de funcionalidade
    opcao = st.radio("Escolha uma opção:", ["Visualizar Funcionários", "Adicionar Funcionário", "Atualizar Funcionário", "Excluir Funcionário"])
    
    if opcao == "Visualizar Funcionários":
        st.write("### Funcionários Cadastrados")
        query = "SELECT * FROM Funcionario"
        cursor.execute(query)
        resultados = cursor.fetchall()
        if resultados:
            df = pd.DataFrame(resultados, columns=["CodFuncionario", "FuncionarioNome", "Salario"])
            st.dataframe(df)
        else:
            st.info("Nenhum funcionário encontrado.")
    
    elif opcao == "Adicionar Funcionário":
        with st.form("form_add_funcionario"):
            nome = st.text_input("Nome do Funcionário:")
            salario = st.number_input("Salário:", min_value=0.0, format="%.2f")
            submit = st.form_submit_button("Adicionar")
        
        if submit:
            if nome and salario:
                try:
                    query = "INSERT INTO Funcionario (FuncionarioNome, Salario) VALUES (%s, %s)"
                    cursor.execute(query, (nome, salario))
                    mydb.commit()
                    st.success("Funcionário adicionado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao adicionar funcionário: {e}")
            else:
                st.warning("Preencha todos os campos.")
    
    elif opcao == "Atualizar Funcionário":
        st.write("### Atualizar Dados de um Funcionário")
        query = "SELECT CodFuncionario, FuncionarioNome FROM Funcionario"
        cursor.execute(query)
        funcionarios = cursor.fetchall()
        
        if funcionarios:
            funcionario_selecionado = st.selectbox("Selecione o Funcionário:", funcionarios, format_func=lambda x: f"{x[1]} (ID: {x[0]})")
            novo_nome = st.text_input("Novo Nome:", funcionario_selecionado[1])
            novo_salario = st.number_input("Novo Salário:", min_value=0.0, format="%.2f")
            
            if st.button("Atualizar"):
                try:
                    query = "UPDATE Funcionario SET FuncionarioNome = %s, Salario = %s WHERE CodFuncionario = %s"
                    cursor.execute(query, (novo_nome, novo_salario, funcionario_selecionado[0]))
                    mydb.commit()
                    st.success("Funcionário atualizado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar funcionário: {e}")
        else:
            st.info("Nenhum funcionário disponível para atualizar.")
    
    elif opcao == "Excluir Funcionário":
        st.write("### Excluir um Funcionário")
        query = "SELECT CodFuncionario, FuncionarioNome FROM Funcionario"
        cursor.execute(query)
        funcionarios = cursor.fetchall()
        
        if funcionarios:
            funcionario_selecionado = st.selectbox("Selecione o Funcionário:", funcionarios, format_func=lambda x: f"{x[1]} (ID: {x[0]})")
            
            if st.button("Excluir"):
                try:
                    query = "DELETE FROM Funcionario WHERE CodFuncionario = %s"
                    cursor.execute(query, (funcionario_selecionado[0],))
                    mydb.commit()
                    st.success("Funcionário excluído com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao excluir funcionário: {e}")
        else:
            st.info("Nenhum funcionário disponível para excluir.")

def funcao_app(cursor, mydb):
    st.subheader("Gestão de Funções")
    
    # Seleção de funcionalidade
    opcao = st.radio("Escolha uma opção:", ["Visualizar Funções", "Adicionar Função", "Atualizar Função", "Excluir Função"])
    
    if opcao == "Visualizar Funções":
        st.write("### Funções Cadastradas")
        query = "SELECT * FROM Funcao"
        cursor.execute(query)
        resultados = cursor.fetchall()
        if resultados:
            df = pd.DataFrame(resultados, columns=["CodFuncao", "FuncaoNome"])
            st.dataframe(df)
        else:
            st.info("Nenhuma função encontrada.")
    
    elif opcao == "Adicionar Função":
        with st.form("form_add_funcao"):
            nome_funcao = st.text_input("Nome da Função:")
            submit = st.form_submit_button("Adicionar")
        
        if submit:
            if nome_funcao:
                try:
                    query = "INSERT INTO Funcao (FuncaoNome) VALUES (%s)"
                    cursor.execute(query, (nome_funcao,))
                    mydb.commit()
                    st.success("Função adicionada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao adicionar função: {e}")
            else:
                st.warning("Preencha o campo nome da função.")
    
    elif opcao == "Atualizar Função":
        st.write("### Atualizar Dados de uma Função")
        query = "SELECT CodFuncao, FuncaoNome FROM Funcao"
        cursor.execute(query)
        funcoes = cursor.fetchall()
        
        if funcoes:
            funcao_selecionada = st.selectbox("Selecione a Função:", funcoes, format_func=lambda x: f"{x[1]} (ID: {x[0]})")
            novo_nome_funcao = st.text_input("Novo Nome da Função:", funcao_selecionada[1])
            
            if st.button("Atualizar"):
                try:
                    query = "UPDATE Funcao SET FuncaoNome = %s WHERE CodFuncao = %s"
                    cursor.execute(query, (novo_nome_funcao, funcao_selecionada[0]))
                    mydb.commit()
                    st.success("Função atualizada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar função: {e}")
        else:
            st.info("Nenhuma função disponível para atualizar.")
    
    elif opcao == "Excluir Função":
        st.write("### Excluir uma Função")
        query = "SELECT CodFuncao, FuncaoNome FROM Funcao"
        cursor.execute(query)
        funcoes = cursor.fetchall()
        
        if funcoes:
            funcao_selecionada = st.selectbox("Selecione a Função:", funcoes, format_func=lambda x: f"{x[1]} (ID: {x[0]})")
            
            if st.button("Excluir"):
                try:
                    query = "DELETE FROM Funcao WHERE CodFuncao = %s"
                    cursor.execute(query, (funcao_selecionada[0],))
                    mydb.commit()
                    st.success("Função excluída com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao excluir função: {e}")
        else:
            st.info("Nenhuma função disponível para excluir.")

def equipe_app(cursor, mydb):
    st.subheader("Gestão de Equipes")
    
    # Seleção de funcionalidade
    opcao = st.radio("Escolha uma opção:", ["Visualizar Equipes", "Adicionar Equipe", "Atualizar Equipe", "Excluir Equipe"])
    
    if opcao == "Visualizar Equipes":
        st.write("### Equipes Cadastradas")
        query = """
            SELECT E.CodEquipe, F.FuncaoNome, Fu.FuncionarioNome 
            FROM Equipe E
            JOIN Funcao F ON E.CodFuncao = F.CodFuncao
            JOIN Funcionario Fu ON E.CodFuncionario = Fu.CodFuncionario
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        if resultados:
            df = pd.DataFrame(resultados, columns=["CodEquipe", "Função", "Funcionário"])
            st.dataframe(df)
        else:
            st.info("Nenhuma equipe encontrada.")
    
    elif opcao == "Adicionar Equipe":
        st.write("### Adicionar Equipe")
        query_funcao = "SELECT CodFuncao, FuncaoNome FROM Funcao"
        query_funcionario = "SELECT CodFuncionario, FuncionarioNome FROM Funcionario"
        
        cursor.execute(query_funcao)
        funcoes = cursor.fetchall()
        
        cursor.execute(query_funcionario)
        funcionarios = cursor.fetchall()
        
        with st.form("form_add_equipe"):
            funcao_selecionada = st.selectbox("Selecione a Função:", funcoes, format_func=lambda x: x[1])
            funcionario_selecionado = st.selectbox("Selecione o Funcionário:", funcionarios, format_func=lambda x: x[1])
            submit = st.form_submit_button("Adicionar")
        
        if submit:
            try:
                query = "INSERT INTO Equipe (CodFuncao, CodFuncionario) VALUES (%s, %s)"
                cursor.execute(query, (funcao_selecionada[0], funcionario_selecionado[0]))
                mydb.commit()
                st.success("Equipe adicionada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao adicionar equipe: {e}")
    
    elif opcao == "Atualizar Equipe":
        st.write("### Atualizar Equipe")
        query = """
            SELECT E.CodEquipe, F.FuncaoNome, Fu.FuncionarioNome 
            FROM Equipe E
            JOIN Funcao F ON E.CodFuncao = F.CodFuncao
            JOIN Funcionario Fu ON E.CodFuncionario = Fu.CodFuncionario
        """
        cursor.execute(query)
        equipes = cursor.fetchall()
        
        if equipes:
            equipe_selecionada = st.selectbox("Selecione a Equipe:", equipes, format_func=lambda x: f"Equipe {x[0]} - {x[1]} / {x[2]}")
            
            query_funcao = "SELECT CodFuncao, FuncaoNome FROM Funcao"
            query_funcionario = "SELECT CodFuncionario, FuncionarioNome FROM Funcionario"
            
            cursor.execute(query_funcao)
            funcoes = cursor.fetchall()
            
            cursor.execute(query_funcionario)
            funcionarios = cursor.fetchall()
            
            novo_funcao = st.selectbox("Nova Função:", funcoes, format_func=lambda x: x[1])
            novo_funcionario = st.selectbox("Novo Funcionário:", funcionarios, format_func=lambda x: x[1])
            
            if st.button("Atualizar"):
                try:
                    query_update = """
                        UPDATE Equipe 
                        SET CodFuncao = %s, CodFuncionario = %s 
                        WHERE CodEquipe = %s
                    """
                    cursor.execute(query_update, (novo_funcao[0], novo_funcionario[0], equipe_selecionada[0]))
                    mydb.commit()
                    st.success("Equipe atualizada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar equipe: {e}")
        else:
            st.info("Nenhuma equipe disponível para atualizar.")
    
    elif opcao == "Excluir Equipe":
        st.write("### Excluir Equipe")
        query = """
            SELECT E.CodEquipe, F.FuncaoNome, Fu.FuncionarioNome 
            FROM Equipe E
            JOIN Funcao F ON E.CodFuncao = F.CodFuncao
            JOIN Funcionario Fu ON E.CodFuncionario = Fu.CodFuncionario
        """
        cursor.execute(query)
        equipes = cursor.fetchall()
        
        if equipes:
            equipe_selecionada = st.selectbox("Selecione a Equipe:", equipes, format_func=lambda x: f"Equipe {x[0]} - {x[1]} / {x[2]}")
            
            if st.button("Excluir"):
                try:
                    query_delete = "DELETE FROM Equipe WHERE CodEquipe = %s"
                    cursor.execute(query_delete, (equipe_selecionada[0],))
                    mydb.commit()
                    st.success("Equipe excluída com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao excluir equipe: {e}")
        else:
            st.info("Nenhuma equipe disponível para excluir.")

# Direcionar para a aba selecionada
if aba_selecionada == "Fornecedor":
    fornecedor_app(cursor, mydb)
elif aba_selecionada == "Produto":
    produto_app(cursor, mydb)
elif aba_selecionada == "Cliente":
    cliente_app(cursor, mydb)
elif aba_selecionada == "Registros de Compras":
    nota_fiscal_app(cursor, mydb)
elif aba_selecionada == "Funcionário":
    funcionario_app(cursor, mydb)
elif aba_selecionada == "Função":
    funcao_app(cursor, mydb) 
elif aba_selecionada == "Equipe":
    equipe_app(cursor, mydb)  