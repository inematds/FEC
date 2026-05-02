# REVIEW-RUBRIC — Rubrica de peer review externo

> _Preencha um arquivo `reviews/<trilha>-revisor<N>.md` com este template para cada trilha que você revisa._

## Identificação

```
Revisor: <nome>
Afiliação: <empresa/instituição>
Trilha revisada: T<n> — <nome>
Versão revisada: rc tag (ex.: v1.0.0-rc.2) + commit SHA
Data: YYYY-MM-DD
Conflito de interesse: <declaração>
```

## Critérios

Para cada critério, marque **✅ Aprovado**, **⚠️ Aprovado com ressalvas** (descreva), ou **❌ Reprovado** (descreva).

### 1. Correção técnica

A trilha apresenta padrões corretos? Alegações têm evidência (paper datado OU run no harness `evals/v1/runs/<id>`)?

```
[ ] ✅  [ ] ⚠️  [ ] ❌
```

Comentários:

### 2. Profundidade adequada

Conteúdo é denso o suficiente para o público (eng. de software/ML em produção)? Não é "curso de marketing"?

```
[ ] ✅  [ ] ⚠️  [ ] ❌
```

Comentários:

### 3. Clareza pedagógica

Explicações são claras? Subseções INEMA ("O que é / Por que aprender / Conceitos-chave") cumprem o papel? Aluno consegue seguir sem ficar travado?

```
[ ] ✅  [ ] ⚠️  [ ] ❌
```

Comentários:

### 4. Exercícios reproduzíveis

Os exercícios têm teste automatizado? Você rodou e passou? Ambíguos? Tempo estimado bate?

```
[ ] ✅  [ ] ⚠️  [ ] ❌
```

Comentários:

### 5. "Quando NÃO usar"

Cada padrão técnico tem a seção? Os trade-offs estão honestos?

```
[ ] ✅  [ ] ⚠️  [ ] ❌
```

Comentários:

### 6. Bibliografia

≥10 referências com data, autor, link válido? Mistura saudável de papers e posts? Sem cherry-pick?

```
[ ] ✅  [ ] ⚠️  [ ] ❌
```

Comentários:

### 7. Provider-neutral

Padrões neutros vêm primeiro? Capacidades específicas estão em `CAPACIDADES.md`? `fec_sdk` é canônico nos exemplos?

```
[ ] ✅  [ ] ⚠️  [ ] ❌
```

Comentários:

### 8. Acessibilidade e ilustrações

≥3 ilustrações de tipos diferentes? Light mode funciona? `<title>`/`aria-label` em diagramas? axe-core verde no PR?

```
[ ] ✅  [ ] ⚠️  [ ] ❌
```

Comentários:

### 9. Eval-thinking embutida

T1.1 introduz, módulos seguintes aplicam? "Toda mudança de prompt entra com mini-eval" é demonstrado?

```
[ ] ✅  [ ] ⚠️  [ ] ❌
```

Comentários:

## Recomendação final

```
[ ] APROVADO — pode publicar como GA.
[ ] APROVADO COM RESSALVAS — pode publicar com fixes listados.
[ ] REPROVADO — fixes substanciais necessários antes de re-revisar. Recomendo `beta` enquanto isso.
```

## Comentários abertos

Espaço para qualquer feedback que não cabe nos critérios acima.

## Assinatura

```
Revisor: <nome>
Data: YYYY-MM-DD
Tempo investido: <h>
```

## Compensação

[ ] Voucher INEMA recebido em YYYY-MM-DD.
[ ] Crédito em `REVISORES.md` confirmado.
