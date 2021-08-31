# Plataforma FATEC

Sistema administrativo para FATEC Araras.

### Professores envolvidos

Prof. Me. Orlando Saraiva do Nascimento Júnior

Prof. Dr. Leonardo de Souza Lima

Profa. Me. Dhebora Souza Umbelino Silva


### Como desenvolver ?

1. Clone o repositório
2. Crie um virtualenv 
3. Ative a virtualenv
4. Instale as dependências
5. Execute os testes

```console
git clone https://github.com/orlandosaraivajr/FATEC_plataforma.git
cd FATEC_plataforma/
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt 
cd plataforma/
python manage.py migrate
python manage.py test
coverage run --source='.' manage.py test
coverage report
coverage html
python manage.py runserver
```
