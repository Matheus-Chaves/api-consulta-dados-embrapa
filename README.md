# api-consulta-dados-embrapa

Projeto para entrega do Tech Challenge do primeiro módulo da Pós em Machine Learning Engineering - FIAP

## Arquitetura do Projeto

![arquiteturatechchallenge](https://github.com/bpcavalcante/api-consulta-dados-embrapa/assets/69259703/992b1cf2-8cac-407f-bad6-cd38ba7a764a)

## Como executar o projeto

1. Inicialize e ative o ambiente virtual:

    ```bash
    python3 -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux
    source venv/bin/activate
    ```

2. Instale as dependências do projeto:

    ```bash
    pip install -r requirements.txt
    ```

3. Rode o código para realizar o web scraping:

    ```bash
    python3 src/scraper.py
    ```

4. Inicialize a API

    ```bash
    uvicorn src.main:app --reload
    ```


# Planejamento do Deploy

## Etapa 1: Preparação do Ambiente
1. Configuração de Contas e Permissões:
- Configurar uma conta AWS e acesso apropriado aos serviços necessários (API Gateway, Load Balancer, Lambda, CloudWatch e X-Ray).
- Criar as policies necessárias e atribuídas às roles e usuários apropriados para garantir que cada serviço tenha as permissões corretas.

## Etapa 2: Implementação da Função AWS Lambda
1. Criação da Função Lambda:
- Escrever o código para a função Lambda que implementa a lógica da aplicação.
- Criar a função Lambda.
- Configurar as variáveis de ambiente e definir o runtime (Python).
- Atribuir uma role de execução que tenha permissões para qualquer serviço AWS que a função Lambda precisa acessar.

## Etapa 3: Configuração do Network Load Balancer
1. Criação do Network Load Balancer (NLB):
- Criar um novo Network Load Balancer.
- Configurar as definições básicas, como nome, esquema (interno ou internet-facing) e listeners.
- Adicionar a função Lambda como destino do Load Balancer. Para isso, será necessário configurar a integração Lambda com o NLB.

## Etapa 4: Configuração do API Gateway
1. Criação do API Gateway:
- Criar um novo API Gateway (REST ou HTTP API conforme necessário).
- Definir os endpoints e métodos HTTP que serão usados para acessar a aplicação.
- Configurar a integração do API Gateway com o Network Load Balancer criado na etapa anterior.
- Definir as permissões necessárias para permitir que o API Gateway invoque o Load Balancer.


## Etapa 5: Implementação de Monitoramento e Observabilidade
1. Configuração do Amazon CloudWatch:

- Configurar os logs do CloudWatch para a função Lambda e para o API Gateway.
- Criar dashboards personalizados e configurar alarmes para monitorar métricas importantes (tempo de execução da Lambda, taxa de erros, latência do API Gateway, etc.).

2. Configuração do AWS X-Ray:

- Ativar o tracing do AWS X-Ray para a função Lambda.
- Configurar o API Gateway para enviar traces para o X-Ray.
- Utilizar o console do X-Ray para visualizar e analisar as traces das solicitações, ajudando a identificar gargalos e problemas de desempenho.

## Etapa 6: Testes e Validação
1. Testes de Unidade e Integração:

- Executar testes de unidade e integração no código Lambda para garantir que ele funcione corretamente.
- Testar o fluxo completo de uma solicitação passando pelo API Gateway, Load Balancer e chegando à função Lambda.
2. Testes de Carga:

- Realizar testes de carga para verificar como a aplicação se comporta sob alta demanda.
- Utilizar ferramentas como AWS CloudWatch para monitorar o desempenho e ajustar configurações conforme necessário.


## Etapa 7: Implantação e Monitoramento Contínuo
1. Deploy:

- Realizar o deploy da função Lambda e das configurações do API Gateway e Load Balancer.
- Monitorar os logs e métricas iniciais para garantir que tudo esteja funcionando como esperado.

2. Monitoramento Contínuo e Manutenção:

- Continuar monitorando a aplicação usando Amazon CloudWatch e AWS X-Ray.
- Ajustar e otimizar conforme necessário, baseado nas métricas e logs coletados.


PS: Todos os recursos serão criados através de Infraestructure as Code, utilizando Terraform ou CloudFormation.

Seguindo essas etapas, será possível implantar a aplicação baseada na arquitetura apresentada, garantindo que todos os componentes estejam devidamente configurados e monitorados. Essa abordagem sistemática ajudará a minimizar problemas durante o deploy e a manter a aplicação estável e performática.
