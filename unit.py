import requests
import unittest
import os


class Classe_User:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.usuario = None
        self.perfil = None
        self.repositorios = None
        self.repositorios_urls = None
        self.seguidores = None
        self.seguindo = None
        self.buscar_dados()

    def buscar_dados(self):
        try:
            response = requests.get(self.repo_url)
            response.raise_for_status()  
            data = response.json()
            self.usuario = data.get('login')
            self.perfil = data.get('html_url')
            self.repositorios = data.get('public_repos')
            self.repositorios_urls = data.get('repos_url')
            self.seguidores = data.get('followers')
            self.seguindo = data.get('following')
        except requests.exceptions.RequestException as e:
            print(f"{e}")

    def get_repositorios(self):
        repos_dict = {}
        try:
            response = requests.get(self.repositorios_urls)
            response.raise_for_status()  
            repos = response.json()
            for repo in repos:
                repos_dict[repo['name']] = repo['html_url']
        except requests.exceptions.RequestException as e:
            print(f"{e}")
        return repos_dict

    def salva_txt(self):
        try:
            with open(f"{self.usuario}.txt", "w") as file:
                file.write(self.__repr__())
                file.write("\n\nRepositórios:\n")
                repos = self.get_repositorios()
                for name, url in repos.items():
                    file.write(f"{name}: {url}\n")
        except Exception as e:
            print(f"{e}")

    def __repr__(self):
        return (f"Usuário: {self.usuario}\n"
                f"Perfil: {self.perfil}\n"
                f"Repositórios: {self.repositorios}\n"
                f"URL_repositórios: {self.repositorios_urls}\n"
                f"Seguidores: {self.seguidores}\n"
                f"Seguindo: {self.seguindo}")    

usuario = input('Nome do usuário: ')
repo_url = f'https://api.github.com/users/{usuario}'
user = Classe_User(repo_url)
user.salva_txt()
    

class TestClasseUser(unittest.TestCase):

    def setUp(self):
        self.usuario = 'githubuser'
        self.repo_url = f'https://api.github.com/users/{self.usuario}'
        self.user = Classe_User(self.repo_url)

    def test_user_class_has_minimal_parameters(self):

        attributes = [
            'usuario', 'perfil', 'repositorios', 'repositorios_urls', 'seguidores', 'seguindo'
        ]
        for attr in attributes:
            self.assertTrue(hasattr(self.user, attr))

    def test_buscar_dados(self):
        self.assertEqual(self.user.usuario, 'githubuser')
        self.assertEqual(self.user.perfil, 'https://github.com/githubuser')
        self.assertEqual(self.user.repositorios, 4)
        self.assertEqual(self.user.repositorios_urls, 'https://api.github.com/users/githubuser/repos')
        self.assertEqual(self.user.seguidores, 12)
        self.assertEqual(self.user.seguindo, 0)

    def test_get_repositorios(self):
        repos = self.user.get_repositorios()
        expected_repos = {
            'empass': 'https://github.com/githubuser/empass',
            'grit': 'https://github.com/githubuser/grit',
            'mysuperproject': 'https://github.com/githubuser/mysuperproject',
            'simplegit': 'https://github.com/githubuser/simplegit'
        }
        breakpoint()
        self.assertEqual(repos, expected_repos)

    def test_salva_txt(self):
        self.user.salva_txt()
        filename = f"{self.user.usuario}.txt"
        self.assertTrue(os.path.isfile(filename))

        with open(filename, 'r') as file:
            content = file.read()

        self.assertIn(f"Usuário: {self.user.usuario}", content)
        self.assertIn(f"Perfil: {self.user.perfil}", content)
        self.assertIn(f"Repositórios: {self.user.repositorios}", content)
        self.assertIn(f"URL_repositórios: {self.user.repositorios_urls}", content)
        self.assertIn(f"Seguidores: {self.user.seguidores}", content)
        self.assertIn(f"Seguindo: {self.user.seguindo}", content)

        for name, url in self.user.get_repositorios().items():
            self.assertIn(f"{name}: {url}", content)

if __name__ == '__main__':
    unittest.main()
