![Groups](https://raw.githubusercontent.com/nunesfd/hostcontrol/refs/heads/main/assets/screenshots/list_groups.png)

# HostControl

[![English](https://img.shields.io/badge/lang-en-blue.svg)](./README.md)
[![Português](https://img.shields.io/badge/lang-pt--BR-green.svg)](./README.pt-BR.md)

HostControl é uma aplicação desktop baseada em terminal, desenvolvida com Python e a biblioteca [Textual](https://github.com/Textualize/textual). Esta ferramenta foi projetada especificamente para gerenciar o arquivo `/etc/hosts`, proporcionando uma interface intuitiva que permite adicionar, editar e remover grupos de hosts de maneira simples e eficiente.

![Hosts](https://raw.githubusercontent.com/nunesfd/hostcontrol/refs/heads/main/assets/screenshots/list_hosts.png)

## Funcionalidades

- Gerenciar grupos de hosts (adicionar, editar, remover)
- Visualizar o status de sincronização de cada grupo
- Interface amigável baseada em terminal
- Atalhos de teclado para ações rápidas

### IMPORTANTE - Antes da instalação

O arquivo `/etc/hosts` geralmente só pode ser modificado pelo superusuário (root), então é necessário conceder acesso ao app para que ele consiga gerenciar esse arquivo.

- **Executar como root:** Isso permite que o app tenha as permissões necessárias para alterar o arquivo.
- **Alterar as permissões do arquivo:** Modifique as permissões de `/etc/hosts` para que sua conta de usuário possa ler e escrever no arquivo.
- **Outras alternativas:** Também é possível usar grupos de usuários, configurar o arquivo `sudoers`, ou utilizar o **Polkit** para gerenciar as permissões de forma mais segura.

#### Solução rápida para Linux ou Mac:
```sh
sudo chown {MEU_USUARIO}:{MEU_USUARIO} /etc/hosts
```
> Essas são sugestões simples que podem resolver o problema. No entanto, você pode aplicar uma solução mais segura e personalizada, que se ajuste melhor ao seu ambiente, garantindo a integridade e a segurança do sistema.

## Instalar usando Docker

Para instalar e rodar a aplicação usando docker você pode usar o seguinte comando:

```bash
docker run --rm --name hostcontrol -it -v /etc/hosts:/opt/hosts -v /home/{your_user}/.host_control:/opt/host_control_db nunesfd/hostcontrol
```

Altere **your_user** pelo nome do **seu usuário**. 
Para mais detalhes sobre os parâmetros usados nesse comando, acesse:
<https://hub.docker.com/r/nunesfd/hostcontrol>

## Instalar usando python

### Pré-requisitos

Antes de instalar o HostControl, certifique-se de ter o seguinte instalado no seu sistema:

- Python 3.8 ou mais recente
- Pip (gerenciador de pacotes Python)

### 1. Clonar o repositório

Para instalar o HostControl, primeiro clone o repositório do GitHub:

```bash
git clone https://github.com/nunesfd/hostcontrol.git
cd hostcontrol
```

### 2. Criar e ativar um ambiente virtual (opcional, mas recomendado)

Criar um ambiente virtual irá isolar as dependências do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

Instale os pacotes Python necessários:

```bash
pip install -r requirements.txt
```
### 4. Executar a aplicação

Depois de instalar as dependências, você pode rodar o app usando:

```bash
python main.py
```

## Para usar em modo de desenvolvimento

### Rodar no modo de desenvolvimento
```bash
pip install textual-dev
make start-dev
```

### Rodar o console para debug
```bash
make start-console
```

## Contribuições

Se você deseja contribuir com o projeto, fique à vontade para fazer um fork do repositório e criar um pull request. Todas as contribuições são bem-vindas!

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
