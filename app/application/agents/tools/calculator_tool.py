from langchain_core.tools import tool


@tool
def calculator_tool(x: int, y: int) -> int:
    """
    Multiplica dois números inteiros.
    Use esta ferramenta para calcular multiplicações.
    """
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ")

    result = x * y
    return result

@tool
def divide_tool(x: int, y: int) -> int:
    """
    Divide dois números inteiros.
    Use esta ferramenta para calcular divisões.
    """
    result = x / y
    return result