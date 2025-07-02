from typing import List
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
        api_url = "https://607e3ed502a23c0017e8b00c.mockapi.io/contracts"

        headers = {
            "Content-Type": "application/json",
            # Adicione headers de autenticação se necessário
        }

        params = {"email": email}

        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()

        contracts = response.json()

        contracts_by_email = [contract for contract in contracts if contract["responsible_email"] == email]

        print(f"Encontrados {len(contracts)} contratos para {email}")
        return contracts_by_email

    except requests.RequestException as e:
        print(f"Erro ao buscar contratos para {email}: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado ao buscar contratos: {e}")
        return []
