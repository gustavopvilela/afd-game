from typing import Iterable, Dict, Tuple, Optional


class AFD:
    # Uma vez que estamos fazendo uma máquina de Moore, todas as ações relativas
    # ao personagem em tela são feitas a partir do estado em que se está, e não
    # a partir das transições, dessa forma, faremos as transições do AFD de estado
    # para estado, e não de um estado para uma ação.
    def __init__(self,
                 estados: Iterable[str],
                 alfabeto: Iterable[str],
                 transicoes: Dict[Tuple[str, str | None], str],
                 estado_inicial: str,
                 estados_finais: Optional[Iterable[str]] = None):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.transicoes = dict(transicoes)
        self.estado_inicial = estado_inicial

        if estados_finais is None: self.estados_finais = set()
        else: self.estados_finais = set(estados_finais)

        # Para processar o AFD, colocaremos a variável de "estado atual" na classe.
        self.estado_atual = estado_inicial

    """
        Processamos a próxima transição do AFD para recuperarmos o estado
        atual dele, assim, podendo controlar as animações de cada estado.
    """
    def processar (self, simbolo):
        key = (self.estado_atual, simbolo)
        if key in self.transicoes:
            self.estado_atual = self.transicoes[key]
        else:
            default_key = (self.estado_atual, None)
            if default_key in self.transicoes:
                self.estado_atual = self.transicoes[default_key]

        return self.estado_atual