# Guia de Implementação: Identificação de Contrato com Intervenção Humana

Este guia detalha os passos para implementar a funcionalidade de identificação de contrato, incluindo o fluxo de "human-in-the-loop" para casos com múltiplos contratos.

## 📋 Visão Geral

A nova funcionalidade adiciona um nó de identificação de contrato logo após o orquestrador, que:

- Busca contratos associados ao remetente do e-mail
- Se encontrar 1 contrato: prossegue automaticamente
- Se encontrar múltiplos contratos: envia um Adaptive Card para o usuário escolher
- Se não encontrar contratos: encerra o fluxo

---

## 🚀 Fase 1: Preparação do Estado e Ferramentas (Tools)

### 1.1 Atualizar o Estado do Agente

**📁 Arquivo:** `app/application/agents/state/email_analysis_state.py`

**🔧 Ação:** Adicione os novos campos ao estado:

```python
from typing import Optional, List, TypedDict

class EmailAnalysisState(TypedDict):
    # ... outros campos existentes

    # --- NOVOS CAMPOS ---
    # Guarda o ID do contrato final (escolhido ou único)
    contract_id: Optional[str]

    # Guarda a lista de contratos quando a intervenção é necessária
    contracts_for_choice: Optional[List[dict]]

    # Informações da empresa (se necessário)
    company_info: Optional[dict]
```

### 1.2 Criar a Tool da API de Contratos

**📁 Arquivo:** `app/application/agents/tools/contract_api_tool.py` (NOVO)

**🔧 Ação:** Implemente a tool que busca contratos:

```python
from langchain_core.tools import tool
from typing import List, Dict
import requests
import os

@tool
def get_contracts_by_email(email: str) -> List[Dict]:
    """
    Busca os contratos associados a um e-mail de remetente.

    Args:
        email: E-mail do remetente

    Returns:
        Lista de contratos encontrados
    """
    try:
        # Substitua pela URL da sua API real
        api_url = os.getenv("CONTRACTS_API_URL", "https://sua-api.com/contracts")

        headers = {
            "Content-Type": "application/json",
            # Adicione headers de autenticação se necessário
        }

        params = {"email": email}

        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()

        contracts = response.json()

        print(f"Encontrados {len(contracts)} contratos para {email}")
        return contracts

    except requests.RequestException as e:
        print(f"Erro ao buscar contratos para {email}: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado ao buscar contratos: {e}")
        return []
```

### 1.3 Criar/Atualizar a Tool do Adaptive Card

**📁 Arquivo:** `app/application/agents/tools/adaptive_card_tool.py`

**🔧 Ação:** Certifique-se de que a tool pode enviar cards para escolha de contrato:

```python
from langchain_core.tools import tool
from typing import List, Dict
import requests

@tool
def send_contract_choice_card(contracts: List[Dict], thread_id: str, recipient_email: str) -> Dict:
    """
    Envia um Adaptive Card para o usuário escolher entre múltiplos contratos.

    Args:
        contracts: Lista de contratos para escolha
        thread_id: ID da thread do grafo (para retorno)
        recipient_email: E-mail do destinatário

    Returns:
        Resposta da API do Microsoft Graph
    """
    try:
        # Construir o Adaptive Card JSON
        card_body = []

        # Título
        card_body.append({
            "type": "TextBlock",
            "text": "Múltiplos Contratos Encontrados",
            "weight": "bolder",
            "size": "medium"
        })

        # Descrição
        card_body.append({
            "type": "TextBlock",
            "text": "Encontrei múltiplos contratos associados ao seu e-mail. Por favor, selecione o contrato correto para esta tarefa:",
            "wrap": True
        })

        # Opções de contratos
        choices = []
        for contract in contracts:
            choices.append({
                "title": f"{contract.get('name', 'Contrato')} - {contract.get('company', 'Empresa')}",
                "value": contract.get('id')
            })

        card_body.append({
            "type": "Input.ChoiceSet",
            "id": "selectedContract",
            "choices": choices,
            "label": "Contrato",
            "placeholder": "selecione o contrato"
            "style": "compact"
        })

        # Botão de confirmação
        card_body.append({
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.Http",
                    "title": "Confirmar Contrato",
                    "method": "POST",
                    "url": "https://sua-api.com/api/v1/graph/handle-contract-choice",
                    "body": {
                        "thread_id": thread_id,
                        "chosen_contract_id": "{{selectedContract.value}}"
                    }
                }
            ]
        })

        adaptive_card = {
            "type": "AdaptiveCard",
            "version": "1.3",
            "body": card_body
        }

        # Enviar via Microsoft Graph API
        # Substitua pela implementação real da sua API
        graph_response = send_via_microsoft_graph(adaptive_card, recipient_email)

        return {"status": "success", "message": "Card enviado com sucesso"}

    except Exception as e:
        print(f"Erro ao enviar card de escolha de contrato: {e}")
        return {"status": "error", "message": str(e)}

def send_via_microsoft_graph(card: dict, recipient: str) -> dict:
    """Implementar conforme sua integração com Microsoft Graph"""
    # TODO: Implementar integração real
    print(f"Enviando card para {recipient}")
    return {"status": "sent"}
```

---

## 🔄 Fase 2: Implementação dos Nós do Grafo

### 2.1 Criar o Nó de Identificação de Contrato

**📁 Pasta:** `app/application/agents/node_functions/identify_contract_node/` (NOVA)

**📁 Arquivo:** `app/application/agents/node_functions/identify_contract_node/__init__.py`

```python
# Arquivo vazio para tornar o diretório um pacote Python
```

**📁 Arquivo:** `app/application/agents/node_functions/identify_contract_node/identify_contract_node.py`

```python
from app.application.agents.state.email_analysis_state import EmailAnalysisState
from app.application.agents.tools.contract_api_tool import get_contracts_by_email

def identify_contract(state: EmailAnalysisState) -> dict:
    """
    Identifica o contrato com base no remetente do e-mail e atualiza o estado.

    Args:
        state: Estado atual do agente

    Returns:
        Dicionário com atualizações para o estado
    """
    try:
        # Extrair e-mail do remetente do estado
        sender_email = state["email"].sender
        print(f"Buscando contratos para o remetente: {sender_email}")

        # Chamar a tool para buscar contratos
        contracts = get_contracts_by_email(email=sender_email)

        if len(contracts) == 1:
            # CASO 1: Contrato único encontrado
            contract = contracts[0]
            print(f"Contrato único encontrado: {contract.get('id', 'N/A')}")

            return {
                "contract_id": contract.get("id"),
                "company_info": {
                    "name": contract.get("company_name"),
                    "id": contract.get("company_id")
                }
            }

        elif len(contracts) > 1:
            # CASO 2: Múltiplos contratos - necessária intervenção humana
            print(f"Múltiplos contratos encontrados ({len(contracts)}). Necessária intervenção humana.")

            return {
                "contracts_for_choice": contracts
            }

        else:
            # CASO 3: Nenhum contrato encontrado
            print(f"Nenhum contrato encontrado para o remetente: {sender_email}")

            return {
                "contract_id": "NOT_FOUND"
            }

    except Exception as e:
        print(f"Erro ao identificar contrato: {e}")
        return {
            "contract_id": "ERROR",
            "error_message": str(e)
        }
```

### 2.2 Criar o Nó de Intervenção Humana para Contratos

**📁 Pasta:** `app/application/agents/node_functions/human_verification_node/` (se não existir)

**📁 Arquivo:** `app/application/agents/node_functions/human_verification_node/contract_choice_node.py`

```python
from app.application.agents.state.email_analysis_state import EmailAnalysisState
from app.application.agents.tools.adaptive_card_tool import send_contract_choice_card

def human_contract_choice(state: EmailAnalysisState) -> dict:
    """
    Envia um Adaptive Card para o usuário escolher entre múltiplos contratos.

    Args:
        state: Estado atual do agente

    Returns:
        Dicionário vazio (nó de pausa)
    """
    try:
        contracts = state.get("contracts_for_choice", [])

        if not contracts:
            print("Erro: Nenhum contrato para escolha encontrado no estado")
            return {}

        # Obter o thread_id da configuração atual
        # NOTA: A forma de obter o thread_id pode variar dependendo da implementação
        thread_id = state.get("thread_id", "unknown")

        # E-mail do remetente (assumindo que ele deve receber o card)
        recipient_email = state["email"].sender

        print(f"Enviando card de escolha de contrato para {recipient_email}")

        # Enviar o card
        result = send_contract_choice_card(
            contracts=contracts,
            thread_id=thread_id,
            recipient_email=recipient_email
        )

        if result.get("status") == "success":
            print("Card de escolha de contrato enviado com sucesso")
        else:
            print(f"Erro ao enviar card: {result.get('message', 'Erro desconhecido')}")

        # Este nó não retorna atualizações de estado
        # A execução será pausada aqui até a resposta do usuário
        return {}

    except Exception as e:
        print(f"Erro no nó de escolha de contrato: {e}")
        return {
            "error_message": str(e)
        }
```

---

## 🛣️ Fase 3: Montagem e Roteamento do Grafo

### 3.1 Criar o Roteador para Identificação de Contrato

**📁 Arquivo:** `app/application/agents/agent_builder/routers.py`

**🔧 Ação:** Adicione a função de roteamento:

```python
from app.application.agents.state.email_analysis_state import EmailAnalysisState

def route_after_contract_identification(state: EmailAnalysisState) -> str:
    """
    Decide o próximo passo após a tentativa de identificação do contrato.

    Args:
        state: Estado atual do agente

    Returns:
        Nome do próximo nó ou "END"
    """
    # Verificar se há contratos para escolha (múltiplos contratos)
    if state.get("contracts_for_choice"):
        print("Roteando para intervenção humana - múltiplos contratos")
        return "HUMAN_CONTRACT_CHOICE"

    # Verificar se há um contrato válido identificado
    contract_id = state.get("contract_id")
    if contract_id and contract_id not in ["NOT_FOUND", "ERROR"]:
        print(f"Roteando para classificação - contrato identificado: {contract_id}")
        return "CLASSIFY_NODE"

    # Casos de erro ou contrato não encontrado
    if contract_id == "NOT_FOUND":
        print("Roteando para fim - nenhum contrato encontrado")
    elif contract_id == "ERROR":
        print("Roteando para fim - erro na identificação do contrato")
    else:
        print("Roteando para fim - estado indefinido")

    return "END"

# Roteador adicional após escolha do usuário (se necessário)
def route_after_contract_choice(state: EmailAnalysisState) -> str:
    """
    Roteador usado após o usuário fazer a escolha do contrato.
    """
    contract_id = state.get("contract_id")

    if contract_id and contract_id not in ["NOT_FOUND", "ERROR"]:
        print(f"Usuário escolheu contrato: {contract_id}. Prosseguindo para classificação.")
        return "CLASSIFY_NODE"
    else:
        print("Erro após escolha do usuário. Encerrando fluxo.")
        return "END"
```

### 3.2 Atualizar o Agent Builder

**📁 Arquivo:** `app/application/agents/agent_builder/email_analyzer_agent_builder.py`

**🔧 Ação:** Modifique a estrutura do grafo:

```python
from langgraph.graph import StateGraph, END

# Importar os novos componentes
from app.application.agents.node_functions.identify_contract_node.identify_contract_node import identify_contract
from app.application.agents.node_functions.human_verification_node.contract_choice_node import human_contract_choice
from app.application.agents.agent_builder.routers import route_after_contract_identification

# ... outros imports existentes

class EmailAnalyzerAgentBuilder:
    def build(self):
        """Constrói o grafo do agente com a nova funcionalidade de identificação de contrato."""

        workflow = StateGraph(EmailAnalysisState)

        # ===========================================
        # DEFINIÇÃO DOS NÓS
        # ===========================================

        # Nós existentes
        workflow.add_node("orchestrator", orchestrator)
        workflow.add_node("classify_node", classify_email)
        workflow.add_node("task_extraction_node", task_extraction)
        workflow.add_node("format_template_node", format_template)
        workflow.add_node("tool_node", tool_execution)
        # ... outros nós existentes

        # --- NOVOS NÓS ---
        workflow.add_node("identify_contract", identify_contract)
        workflow.add_node("human_contract_choice", human_contract_choice)

        # ===========================================
        # DEFINIÇÃO DAS ARESTAS
        # ===========================================

        # Ponto de entrada (não muda)
        workflow.set_entry_point("orchestrator")

        # --- ALTERAÇÃO PRINCIPAL: Nova primeira aresta ---
        # ANTES: workflow.add_edge("orchestrator", "classify_node")
        # AGORA:
        workflow.add_edge("orchestrator", "identify_contract")

        # --- NOVA ARESTA CONDICIONAL: Após identificação do contrato ---
        workflow.add_conditional_edges(
            "identify_contract",
            route_after_contract_identification,
            {
                "CLASSIFY_NODE": "classify_node",
                "HUMAN_CONTRACT_CHOICE": "human_contract_choice",
                "END": END
            }
        )

        # --- ARESTA APÓS ESCOLHA HUMANA ---
        # O nó human_contract_choice pausa a execução
        # Quando retomar, o próximo roteador será executado
        workflow.add_conditional_edges(
            "human_contract_choice",
            route_after_contract_choice,
            {
                "CLASSIFY_NODE": "classify_node",
                "END": END
            }
        )

        # ===========================================
        # ARESTAS EXISTENTES (mantém como estavam)
        # ===========================================

        # Exemplo das arestas que já existiam:
        workflow.add_conditional_edges(
            "classify_node",
            route_after_classification,  # Função existente
            {
                "TASK": "task_extraction_node",
                "NO_TASK": END,
                "UNSURE": "human_in_the_loop"  # Se você já tem este fluxo
            }
        )

        # ... resto das arestas existentes

        # Compilar o grafo
        app = workflow.compile(checkpointer=self.checkpointer)
        return app
```

---

## 🌐 Fase 4: Implementação do Endpoint de Callback

### 4.1 Criar a Rota da API

**📁 Arquivo:** `app/presentation/graphMicrosoft/routers.py`

**🔧 Ação:** Adicione o endpoint para receber a escolha do contrato:

```python
from fastapi import APIRouter, Request, HTTPException, Depends
import json
from typing import Dict, Any

# Assumindo que você tem alguma forma de obter a instância do agente
# Ajuste conforme sua arquitetura de injeção de dependência
from app.application.agents.agent_builder.email_analyzer_agent_builder import EmailAnalyzerAgentBuilder

router = APIRouter()

@router.post("/handle-contract-choice")
async def handle_contract_choice(request: Request) -> Dict[str, Any]:
    """
    Endpoint para receber a escolha do usuário sobre qual contrato usar.

    Este endpoint é chamado quando o usuário clica em uma opção no Adaptive Card.
    """
    try:
        # Extrair payload da requisição
        payload = await request.json()

        thread_id = payload.get("thread_id")
        chosen_contract_id = payload.get("chosen_contract_id")

        # Validar dados obrigatórios
        if not thread_id:
            raise HTTPException(status_code=400, detail="thread_id é obrigatório")

        if not chosen_contract_id:
            raise HTTPException(status_code=400, detail="chosen_contract_id é obrigatório")

        print(f"Recebida escolha de contrato: {chosen_contract_id} para thread: {thread_id}")

        # ===========================================
        # OBTER INSTÂNCIA DO AGENTE
        # ===========================================
        # ATENÇÃO: Esta parte precisa ser ajustada conforme sua arquitetura
        # Você precisa obter a instância do agente que está gerenciando os checkpoints

        # Opção 1: Se você tem um singleton/registry
        # agent_app = AgentRegistry.get_instance()

        # Opção 2: Se você reconstrói o agente
        builder = EmailAnalyzerAgentBuilder()
        agent_app = builder.build()

        # Opção 3: Se você injeta via dependency
        # agent_app = get_agent_instance()  # Implementar conforme sua DI

        # ===========================================
        # ATUALIZAR ESTADO E RETOMAR EXECUÇÃO
        # ===========================================

        config = {"configurable": {"thread_id": thread_id}}

        # Buscar informações do contrato escolhido (se necessário)
        # Aqui você pode fazer uma chamada adicional à sua API de contratos
        # para obter detalhes completos do contrato escolhido

        # Atualizar o estado com a escolha do usuário
        state_update = {
            "contract_id": chosen_contract_id,
            "contracts_for_choice": None,  # Limpar a lista de escolhas
            # Adicionar informações da empresa se necessário
            # "company_info": contract_details.get("company_info")
        }

        # Aplicar a atualização do estado
        agent_app.update_state(config, state_update)

        # Retomar a execução do grafo
        # O grafo continuará do ponto onde parou (após human_contract_choice)
        result = agent_app.invoke(None, config)

        print(f"Fluxo retomado com sucesso para thread: {thread_id}")

        return {
            "status": "success",
            "message": "Escolha de contrato processada e fluxo retomado",
            "thread_id": thread_id,
            "contract_id": chosen_contract_id
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"Erro ao processar escolha de contrato: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar escolha de contrato: {str(e)}"
        )

@router.get("/contracts/{thread_id}/status")
async def get_contract_status(thread_id: str) -> Dict[str, Any]:
    """
    Endpoint opcional para verificar o status de uma thread específica.
    Útil para debugging e monitoramento.
    """
    try:
        # Obter instância do agente (mesmo padrão do endpoint anterior)
        builder = EmailAnalyzerAgentBuilder()
        agent_app = builder.build()

        config = {"configurable": {"thread_id": thread_id}}

        # Obter estado atual
        current_state = agent_app.get_state(config)

        return {
            "thread_id": thread_id,
            "current_state": current_state.values if current_state else None,
            "next_steps": current_state.next if current_state else None
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter status: {str(e)}"
        )
```

### 4.2 Registrar as Novas Rotas

**📁 Arquivo:** `main.py` (ou onde você registra as rotas)

**🔧 Ação:** Certifique-se de que as novas rotas estão registradas:

```python
from app.presentation.graphMicrosoft.routers import router as graph_router

# ... código existente

app.include_router(graph_router, prefix="/api/v1/graph", tags=["Graph"])
```

---

## ✅ Checklist de Implementação

### Fase 1: Estado e Tools

- [x] Atualizar `EmailAnalysisState` com novos campos
- [ ] Criar `contract_api_tool.py` com função de busca
- [ ] Atualizar/criar `adaptive_card_tool.py` para contratos

### Fase 2: Nós do Grafo

- [ ] Criar pasta `identify_contract_node/`
- [ ] Implementar `identify_contract_node.py`
- [ ] Criar `contract_choice_node.py` para intervenção humana

### Fase 3: Grafo e Roteamento

- [ ] Adicionar `route_after_contract_identification` em `routers.py`
- [ ] Atualizar `email_analyzer_agent_builder.py`
- [ ] Modificar a primeira aresta do orquestrador
- [ ] Adicionar arestas condicionais para o novo fluxo

### Fase 4: API e Callback

- [ ] Implementar endpoint `/handle-contract-choice`
- [ ] Implementar endpoint de status (opcional)
- [ ] Registrar rotas no aplicativo principal
- [ ] Configurar URLs no Adaptive Card

### Testes e Validação

- [ ] Testar fluxo com 1 contrato (deve prosseguir automaticamente)
- [ ] Testar fluxo com múltiplos contratos (deve enviar card)
- [ ] Testar fluxo sem contratos (deve encerrar)
- [ ] Testar retorno do usuário (deve retomar corretamente)
- [ ] Validar logs e tratamento de erros

---

## 🐛 Pontos de Atenção

### 1. Gerenciamento de Instância do Agente

O ponto mais crítico é garantir que o endpoint de callback use a mesma instância (ou configuração) do agente que gerencia os checkpoints. Considere:

- Usar um padrão Singleton
- Implementar injeção de dependência
- Garantir que o `checkpointer` seja persistente

### 2. Thread ID no Adaptive Card

Certifique-se de que o `thread_id` é corretamente passado no payload do Adaptive Card e retornado na ação do usuário.

### 3. Tratamento de Erros

Implemente tratamento robusto de erros em todos os pontos:

- Falha na API de contratos
- Erro no envio do Adaptive Card
- Problemas na retomada do grafo

### 4. Configuração de URLs

As URLs nos Adaptive Cards devem apontar para endpoints acessíveis publicamente. Em desenvolvimento, considere usar ferramentas como ngrok.

### 5. Segurança

Considere implementar:

- Autenticação nos endpoints de callback
- Validação de origem das requisições
- Rate limiting

---

## 🎯 Próximos Passos

Após a implementação básica, considere estas melhorias:

1. **Cache de Contratos**: Implementar cache para evitar chamadas desnecessárias à API
2. **Métricas**: Adicionar logging e métricas para monitorar o uso
3. **Interface de Admin**: Criar interface para visualizar threads pausadas
4. **Timeout**: Implementar timeout para threads que ficam pausadas por muito tempo
5. **Notificações**: Adicionar notificações quando o fluxo é retomado

---

Este guia fornece uma base sólida para implementar a funcionalidade completa de identificação de contrato com intervenção humana no seu sistema.
