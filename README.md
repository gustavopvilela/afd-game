# Trabalho Prático 2 de _Fundamentos Teóricos da Computação_: Aplicação de AFDs na criação de jogos eletrônicos

![FTC](https://img.shields.io/badge/IFMG-Fundamentos%20Te%C3%B3ricos%20da%20Computa%C3%A7%C3%A3o-960c82)  [![Python](https://img.shields.io/badge/python-3.13.2-db70cb)](https://www.python.org/)

## Introdução
O código deste repositório representa o segundo trabalho prático da disciplina de Fundamentos Teóricos da Computação. Seu intuito é demonstrar a aplicação de autômatos finitos determinísticos na criação de jogos de computador, desenvolvendo movimentos simples de um personagem em tela.

Este trabalho foi desenvolvido pelos alunos Gustavo Henrique Pereira Vilela e Iasmim Garcia Castro.

Os sprites (imagens, frames) utilizados nestes códigos são do personagem Ori, protagonista dos jogos _[Ori and the Blind Forest](https://store.steampowered.com/app/387290/Ori_and_the_Blind_Forest_Definitive_Edition/?curator_clanid=37856651)_ e _[Ori and the Will of the Wisps](https://store.steampowered.com/app/1057090/Ori_and_the_Will_of_the_Wisps/?curator_clanid=37856651)_.

[![Ori and the Will of the Wisps](https://img.youtube.com/vi/2reK8k8nwBc/maxresdefault.jpg)](https://www.youtube.com/watch?v=2reK8k8nwBc)

Entretanto, as imagens de fato são da colaboração dos jogos anteriormente citados com o jogo _[Rivals of Aether](https://store.steampowered.com/app/383980/Rivals_of_Aether/)_, a _sprite sheet_ foi retirada do site _[DeviantArt](https://www.deviantart.com/1fishmob/art/Ori-Rivals-of-Aether-Sprite-Sheet-863060378)_, todos os créditos aos seus devidos criadores.

## Funções do programa

A seguir, serão apresentadas as funções principais dos algoritmos presentes neste trabalho.

### _Idle_ (ficar parado)

É a posição padrão do personagem. Ao não pressionar nenhuma tecla, ele ficará parado em sua posição atual.

### _Walk_ (andar)

Ao pressionar a tecla `A` ou `D`, o personagem fará um andado normal para a esquerda ou direita, respectivamente. Ao mantê-las pressionadas, Ori andará até chegar ao limite definido para a tela.

### _Jump_ (pular)

Ao clicar na tecla `W`, Ori dará um grande salto. Este salto pode ser modificado pelas teclas `A` ou `D`, que o fará movimentar no ar para a esquerda ou direita, respectivamente. Por estar pulando, este movimento é mais rápido que o andado comum.

### _Crouch_ (agachar)

Pressionando a tecla `S`, o personagem agachará. Esse movimento pode ser modificado pelas teclas `A` ou `D`, que o farão mover de forma agachada para a esqueda ou direita, respectivamente. Vale notar que este movimento é mais lento que o andado normal, justamente por ele estar agachado.

### _Dash_

Clicando na tecla `F`, o personagem dará uma corrida rápida para uma direção, percorrendo diversos pixels de uma só vez. Essa ação é influenciada pelo lado que Ori estiver olhando no momento: esquerda ou direita.

### _Hammer_ (Ataque de martelo)

O ataque feito por Ori é seu ataque de martelo presente em seu jogo _Ori and the Will of the Wisps_. Aqui, ele é realizado ao pressionar a tecla `Z`. A direção do ataque será a mesma que o personagem estiver olhando no momento: esquerda ou direita.

### _Super_ (combo)

O combo aqui é definido como uma sequência de teclas que devem ser apertadas em ordem e simultaneamente para que um ataque especial ocorra. Ao pressionar as teclas `O`, `R` e `I` – formando a palavra "_Ori_", será mostrado em tela uma animação especial como seu super.

---

_Feito com ❤️ para o professor Walace._