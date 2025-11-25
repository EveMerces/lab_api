import unittest
from app import app
import werkzeug
import json

# Patch temporário para adicionar o atributo '__version__' em werkzeug
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = "mock-version"

class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Criação do cliente de teste
        cls.client = app.test_client()
        cls.client.testing = True

    def test_home(self):
        """Teste 1: Verificar se a API está rodando e retorna mensagem correta"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "API is running"})
        print("✓ Teste 1 passou: Endpoint home funcionando corretamente")

    def test_get_items_returns_list(self):
        """Teste 2: Verificar se /items retorna uma lista válida de itens"""
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.json)
        self.assertIsInstance(response.json['items'], list)
        self.assertEqual(len(response.json['items']), 3)
        self.assertEqual(response.json['items'], ["item1", "item2", "item3"])
        print("✓ Teste 2 passou: Lista de itens retornada corretamente")

    def test_login_generates_valid_token(self):
        """Teste 3: Verificar se o login gera um token JWT válido"""
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)
        
        # Verificar se o token não está vazio
        token = response.json['access_token']
        self.assertIsNotNone(token)
        self.assertGreater(len(token), 0)
        print(f"✓ Teste 3 passou: Token JWT gerado com sucesso (tamanho: {len(token)} caracteres)")

    def test_protected_route_without_token(self):
        """Teste 4: Verificar se rota protegida bloqueia acesso sem token"""
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)
        print("✓ Teste 4 passou: Rota protegida bloqueou acesso sem token")

    def test_protected_route_with_valid_token(self):
        """Teste 5: Verificar se rota protegida permite acesso com token válido"""
        # Primeiro, obter o token
        login_response = self.client.post('/login')
        token = login_response.json['access_token']
        
        # Tentar acessar rota protegida com o token
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/protected', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Protected route"})
        print("✓ Teste 5 passou: Rota protegida permitiu acesso com token válido")

    def test_invalid_endpoint_returns_404(self):
        """Teste 6: Verificar se endpoint inexistente retorna 404"""
        response = self.client.get('/endpoint-que-nao-existe')
        self.assertEqual(response.status_code, 404)
        print("✓ Teste 6 passou: Endpoint inexistente retornou 404 corretamente")

if __name__ == '__main__':
    unittest.main(verbosity=2)
