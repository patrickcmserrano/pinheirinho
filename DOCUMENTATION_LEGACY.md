# Comparativo Técnico: Pinheirinho (Nova Arquitetura) vs. Legacy (BDL V3)

Este documento detalha as diferenças técnicas fundamentais encontradas durante a migração e correção do sistema `Pinheirinho` em relação à implementação original de referência (`bdl_race_control_final_v3`), e explica as decisões de design adotadas para garantir modernidade sem perder a compatibilidade "espiritual".

## 1. Controle de Iluminação (Sinaleira)

A maior diferença técnica encontrada foi na forma como o sistema interage com o Assetto Corsa para acender as luzes da sinaleira (Christmas Tree).

### Abordagem Legacy (V3)
**Método:** Reescrita de Arquivo de Configuração (`ext_config.ini`).
*   **Como funcionava:** O script legacy abria o arquivo físico `ext_config.ini` da pista, procurava pela seção `[MATERIAL_...]` e reescrevia os valores de `VALUE_0` (Emissive) diretamente no disco.
*   **Vantagens:** Funciona em qualquer versão do CSP (Custom Shaders Patch), pois força o motor a recarregar o parâmetro do arquivo.
*   **Desvantagens:**
    *   **Alta Latência:** Operações de disco (I/O) são lentas. Em um drag race onde milissegundos contam, escrever no disco para acender uma luz é ineficiente.
    *   **Risco de Corrupção:** Se o jogo ou o script travar durante a escrita, o arquivo da pista pode ser corrompido.
    *   **Conflitos:** Não suporta múltiplas instâncias ou pistas complexas dinamicamente sem alterar arquivos do usuário.

### Abordagem Nova (Pinheirinho)
**Método:** Chamadas de API em Memória (`ac_ext` / `ac`).
*   **Como funciona:** Utilizamos as APIs modernas do CSP (`ac_ext.vaomaterial_emissive`) para alterar as propriedades do material diretamente na memória da GPU/Engine.
*   **Vantagens:**
    *   **Zero Latência:** A mudança é instantânea (próximo frame).
    *   **Segurança:** Não toca nos arquivos originais da pista no disco.
*   **Problema Encontrado:** A implementação inicial estava vazia (`pass`), causando a falha visual.

### Nossa Solução (Híbrida)
Para garantir que o sistema funcione sem obrigar o usuário a ter a versão "Bleeding Edge" do CSP, implementamos uma estratégia resiliente em `lighting.py`:
1.  **Tentativa Primária:** Usa `ac_ext.vaomaterial_emissive` (Padrão moderno).
2.  **Fallback:** "Degrada" graciosamente. Se a API não existir, o código captura o erro e segue, evitando travar a simulação (embora sem luzes visuais caso a API falhe totalmente, evitamos a reescrita de arquivo perigosa do Legacy).

---

## 2. Arquitetura de Software

### Abordagem Legacy (V3)
**Estilo:** Monolítico Imperativo.
*   Código fonte único de ~2500 linhas.
*   Lógica de estado (variáveis globais como `button1_state`, `pin_on`), UI e I/O misturados.
*   Difícil de testar ou modificar sem quebrar outras partes (efeitos colaterais globais).

### Abordagem Nova (Pinheirinho)
**Estilo:** Functional Core, Imperative Shell ("Redux-like").
*   **Core Puro:** A lógica da corrida (regras, estados, tempos) está isolada em funções puras (`reducers.py`) que não sabem que o Assetto Corsa existe. Isso permite testes unitários fora do jogo.
*   **Estado Imutável:** O estado da corrida é um objeto imutável. Nunca "alteramos" uma variável, criamos um novo estado a cada frame. Isso elimina bugs de condição de corrida.
*   **Shell (Pinheirinho.py):** Apenas esta camada "suja" conversa com o Assetto Corsa (Input/Output).

---

## 3. Logging e Debug

### Abordagem Legacy (V3)
*   Logs eram feitos através de uma fila (`queue`) e gravados ou mostrados no chat.
*   Dependia muito do Chat do jogo para feedback.

### Abordagem Nova (Pinheirinho)
*   Criamos um utilitário `Logger` (`logger.py`) unificado.
*   **Dual Output:** Cada mensagem de log é enviada simultaneamente para:
    1.  `ac.log`: Arquivo `log.txt` oficial (para análise pós-jogo).
    2.  `ac.console`: Console Python dentro do jogo (para debug em tempo real desenvolvimento).
*   **UI de Debug:** O "Minimenu" foi enriquecido para mostrar o estado interno dos sensores (L: PRE=True/False), permitindo diagnosticar problemas de alinhamento na pista sem precisar olhar logs.

---

## Resumo
Mantivemos a "alma" da integração (ler sensores, controlar luzes), mas modernizamos a implementação para ser:
1.  **Mais Rápida** (Memória vs Disco).
2.  **Mais Segura** (Sem corrupção de arquivos).
3.  **Mais Auditável** (Arquitetura de estado previsível).
