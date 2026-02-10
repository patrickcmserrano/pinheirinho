# Manual de Configuração - Pinheirinho

Este manual explica como configurar o mod **Pinheirinho** para funcionar em diferentes pistas de Drag (Arrancada) no Assetto Corsa, ajustando a posição dos sensores virtuais.

## 📁 Localização do Arquivo de Configuração

Todas as configurações de pistas e coordenadas de sensores estão armazenadas no arquivo:

`apps/python/pinheirinho/config/tracks.json`

## 📝 Estrutura do Arquivo (JSON)

O arquivo utiliza o formato JSON. Cada entrada principal representa uma pista.

```json
{
    "ID_DA_PISTA": {
        "name": "Nome Legível da Pista",
        "left_lane": { ... configurações da pista esquerda ... },
        "right_lane": { ... configurações da pista direita ... }
    }
}
```

### Definição dos Sensores (Lanes)

Cada pista (lane) possui 3 sensores críticos:
1.  **pre_stage**: O primeiro feixe de luz (Pre-Stage).
2.  **stage**: O segundo feixe, linha de largada oficial (Stage).
3.  **finish**: A linha de chegada.

Cada sensor possui a seguinte estrutura:
```json
"pre_stage": {
    "center": [X, Y, Z], 
    "width": 4.0
}
```
*   **center**: Uma lista com 3 números `[X, Y, Z]` representando a coordenada exata do centro do sensor no mundo 3D.
*   **width**: A largura da pista naquele ponto (Atualmente reservado para uso futuro, a detecção usa um raio fixo de 0.5m a partir do centro).

## 📍 Como Obter as Coordenadas (X, Y, Z)

Para configurar uma nova pista, você precisa descobrir as coordenadas exatas onde os carros vão alinhar.

1.  **Entre no Assetto Corsa** com o carro que deseja usar para testar.
2.  **Posicione o carro** exatamente onde deseja que o sensor seja ativado (ex: pneu dianteiro na linha de Pre-Stage).
    *   *Dica: As coordenadas no Assetto Corsa são: X (Esquerda/Direita), Y (Altura), Z (Frente/Trás).*
3.  **Utilize um App de Desenvolvedor** ou o console Python para ler a posição atual.
    *   Se você tiver acesso ao console Python do AC ou apps de telemetria, procure pelos valores de `World Position` do carro.
4.  **Anote os valores de X, Y, Z**.
5.  Repita o processo para:
    *   Pre-Stage Esquerdo / Direito
    *   Stage Esquerdo / Direito
    *   Chegada (Finish) Esquerda / Direita

## ⚙️ Modificando o Código para Nova Pista

**Atenção:** Na versão atual, o sistema pode estar configurado para carregar uma pista padrão (ex: `drag_strip_kunos`).

Se você estiver configurando uma pista diferente (ex: Interlagos Retão), você precisa:
1.  Criar a entrada no `tracks.json` com um ID novo (ex: `"interlagos_drag"`).
2.  Verificar no arquivo `src/infrastructure/sensor.py` qual ID está sendo carregado.
    *   *Versões futuras detectarão o nome da pista automaticamente.*

## 📋 Exemplo Prático

Se você quiser ajustar o **Pre-Stage da Pista Esquerda** na pista Kunos:

1.  Abra `apps/python/pinheirinho/config/tracks.json`.
2.  Localize `"drag_strip_kunos"` -> `"left_lane"` -> `"pre_stage"`.
3.  Altere o valor de `"center"`.

De:
```json
"center": [-12.5, 0.0, 10.0]
```
Para (exemplo hipotético 1 metro à frente):
```json
"center": [-12.5, 0.0, 11.0]
```
4.  Salve o arquivo e reinicie a sessão no Assetto Corsa.
