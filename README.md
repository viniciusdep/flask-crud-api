# FLASK APIS
APIs Flask com metodo CRUD

Neste repo você encontrará 4 APIs (Clientes, Enderecos, Produtos e Inventário)
Cada uma com suas particularidades, inclusive a API de Inventário que relaciona as informações das demais. 

Cada arquivo contém: 
app.py - Arquivo padrão do flask para iniciar a API
auth.py - Configurações de basic authentication
nomedaapi.py - Instrumentação completa da API com metodos CRUD e conexão com o MySQL
config.py - Configurações do MySQL 
Dockerfile - Imagem personalizada da API 
requirements.txt - Todas as dependências da API

Além disso cada API conta com um arquivo .yaml onde é criado um deployment e um service para conteinerização caso necessário. 
