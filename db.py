import sqlite3
import pandas as pd

def conectar():
    """Conecta ao banco de dados SQLite e retorna a conexão e o cursor."""
    conn = sqlite3.connect("militares.db")
    cursor = conn.cursor()
    return conn, cursor

def criar_tabela():
    """Cria a tabela de militares se ela não existir."""
    conn, cursor = conectar()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS militares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            gradpost TEXT NOT NULL,
            nome TEXT NOT NULL,
            rg TEXT NOT NULL,
            cpf TEXT NOT NULL,
            banco TEXT NOT NULL,
            cc TEXT NOT NULL,
            agencia TEXT NOT NULL,
            type_vant TEXT NOT NULL CHECK (type_vant IN ('QQ', 'ADE')),
            vantagem INTEGER NOT NULL CHECK (vantagem BETWEEN 0 AND 50)
        )
    ''')
    conn.commit()
    conn.close()

def criar_militar(numero, gradpost, nome, rg, cpf, banco, cc, agencia, type_vant, vantagem):
    """Insere um novo militar no banco de dados."""
    conn, cursor = conectar()
    try:
        cursor.execute('''
            INSERT INTO militares (numero, gradpost, nome, rg, cpf, banco, cc, agencia, type_vant, vantagem)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (numero, gradpost, nome, rg, cpf, banco, cc, agencia, type_vant, vantagem))
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Erro ao inserir militar: {str(e)}")
    finally:
        conn.close()

def ler_militar(militar_id):
    """Lê as informações de um militar pelo ID."""
    conn, cursor = conectar()
    cursor.execute('''SELECT * FROM militares WHERE id = ?''', (militar_id,))
    militar = cursor.fetchone()
    conn.close()
    return militar

def ler_militares(filtro, valor):
    """Lê os militares que correspondem a um filtro específico."""
    conn, cursor = conectar()
    query = f'''SELECT * FROM militares WHERE {filtro} = ?'''
    cursor.execute(query, (valor,))
    militares = cursor.fetchall()
    conn.close()
    return militares

def todos_militares():
    """Retorna todos os militares cadastrados no banco de dados."""
    conn, cursor = conectar()
    cursor.execute('''SELECT * FROM militares''')
    militares = cursor.fetchall()
    conn.close()
    return militares

def atualizar_militar(militar_id, **dados):
    """Atualiza as informações de um militar pelo ID."""
    conn, cursor = conectar()
    campos = ", ".join([f"{campo} = ?" for campo in dados.keys()])
    valores = list(dados.values()) + [militar_id]
    query = f'''UPDATE militares SET {campos} WHERE id = ?'''
    cursor.execute(query, valores)
    conn.commit()
    conn.close()

def deletar_militar(militar_id):
    """Remove um militar do banco de dados pelo ID."""
    conn, cursor = conectar()
    cursor.execute('''DELETE FROM militares WHERE id = ?''', (militar_id,))
    conn.commit()
    conn.close()

def importar_militares_de_excel(caminho_excel):
    """Importa militares de um arquivo Excel para o banco de dados."""
    # Definir os cabeçalhos esperados
    cabecalhos_esperados = ["numero", "gradpost", "nome", "rg", "cpf", "banco", "cc", "agencia", "type_vant", "vantagem"]

    try:
        # Ler o arquivo Excel
        df = pd.read_excel(caminho_excel)

        # Verificar se os cabeçalhos são válidos
        if not all(col in df.columns for col in cabecalhos_esperados):
            return "Erro: O arquivo Excel não contém os cabeçalhos esperados."

        # Conectar ao banco de dados
        conn, cursor = conectar()

        # Ler linha por linha e inserir no banco de dados
        for index, row in df.iterrows():
            try:
                cursor.execute('''
                    INSERT INTO militares (numero, gradpost, nome, rg, cpf, banco, cc, agencia, type_vant, vantagem)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (row["numero"], row["gradpost"], row["nome"], row["rg"], row["cpf"], row["banco"], row["cc"], row["agencia"], row["type_vant"], row["vantagem"]))
            except Exception as e:
                conn.rollback()
                conn.close()
                return f"Erro ao processar a linha {index + 1}: {str(e)}"

        conn.commit()
        conn.close()
        return "Importação concluída com sucesso."

    except Exception as e:
        return f"Erro ao ler o arquivo Excel: {str(e)}"

# Criar a tabela ao importar o módulo
criar_tabela()
