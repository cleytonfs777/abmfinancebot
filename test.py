import unittest
from db import (criar_militar, ler_militar, ler_militares, todos_militares, 
                atualizar_militar, deletar_militar, importar_militares_de_excel, conectar)

class TestBancoDeDadosMilitares(unittest.TestCase):

    def setUp(self):
        """Configuração inicial: cria um banco de dados em memória para testes."""
        self.conn, self.cursor = conectar()
        self.cursor.execute('''
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
        self.conn.commit()

    def tearDown(self):
        """Limpa o banco de dados após cada teste."""
        self.cursor.execute("DROP TABLE militares")
        self.conn.commit()
        self.conn.close()

    def test_criar_e_ler_militar(self):
        """Testa se um militar é criado e lido corretamente."""
        criar_militar("12345", "Capitão", "João Silva", "123456", "123.456.789-00", "Banco do Brasil", "12345-6", "1234", "QQ", 25)
        militar = ler_militar(1)
        self.assertIsNotNone(militar)
        self.assertEqual(militar[2], "Capitão")
        self.assertEqual(militar[9], "QQ")
        self.assertEqual(militar[10], 25)

    def test_validar_type_vant(self):
        """Testa se apenas valores válidos são aceitos no campo type_vant."""
        with self.assertRaises(Exception):
            criar_militar("12345", "Capitão", "João Silva", "123456", "123.456.789-00", "Banco do Brasil", "12345-6", "1234", "XYZ", 25)

    def test_validar_vantagem(self):
        """Testa se apenas valores válidos são aceitos no campo vantagem."""
        with self.assertRaises(Exception):
            criar_militar("12345", "Capitão", "João Silva", "123456", "123.456.789-00", "Banco do Brasil", "12345-6", "1234", "QQ", 55)

    def test_atualizar_militar(self):
        """Testa se os dados de um militar são atualizados corretamente."""
        criar_militar("12345", "Capitão", "João Silva", "123456", "123.456.789-00", "Banco do Brasil", "12345-6", "1234", "QQ", 25)
        atualizar_militar(1, nome="João Souza", type_vant="ADE", vantagem=30)
        militar = ler_militar(1)
        self.assertEqual(militar[3], "João Souza")
        self.assertEqual(militar[9], "ADE")
        self.assertEqual(militar[10], 30)

    def test_importar_militares_de_excel(self):
        """Testa se militares são importados corretamente de um arquivo Excel."""
        import pandas as pd
        dados = {
            "numero": ["12345", "54321"],
            "gradpost": ["Capitão", "Tenente"],
            "nome": ["João Silva", "Maria Oliveira"],
            "rg": ["123456", "654321"],
            "cpf": ["123.456.789-00", "987.654.321-00"],
            "banco": ["Banco do Brasil", "Caixa"],
            "cc": ["12345-6", "65432-1"],
            "agencia": ["1234", "4321"],
            "type_vant": ["QQ", "ADE"],
            "vantagem": [25, 10]
        }
        df = pd.DataFrame(dados)
        caminho_excel = "test_militares.xlsx"
        df.to_excel(caminho_excel, index=False)

        resultado = importar_militares_de_excel(caminho_excel)
        self.assertEqual(resultado, "Importação concluída com sucesso.")

        militares = todos_militares()
        self.assertEqual(len(militares), 2)

if __name__ == "__main__":
    unittest.main()
