# Judge — groundedness (FEC-EVAL-v1)

> _Prompt do LLM-as-judge. Versionado e congelado por release. Calibração contra 30 amostras humanas (Cohen κ ≥0.6). PLAN item 26._

**Judge model recomendado:** frontier (`evals/v1/models.json` papel `frontier`).
**Temperature:** 0.0
**Seed:** 42 (fixa em manifests).

## Prompt

```
Você é um juiz de groundedness de respostas geradas por modelos de linguagem.

Para cada exemplo, você recebe:
- A pergunta original.
- As CITAÇÕES esperadas (lista de IDs de fonte, formato `arxiv:XXXX.XXXXX`).
- Os FATOS esperados (lista de afirmações que devem aparecer na resposta).
- A RESPOSTA do modelo sob avaliação.

Sua tarefa: avaliar se a RESPOSTA está GROUNDED nas citações e fatos esperados.

Responda em JSON estrito com este schema:

{
  "groundedness": <float entre 0.0 e 1.0>,
  "citations_match": <bool — todas as expected_citations aparecem na resposta?>,
  "facts_covered": <int — quantos expected_facts a resposta cobre, por subsequência semântica>,
  "facts_total": <int — len(expected_facts)>,
  "rationale": "<string curta explicando>",
  "issues": ["<string>", ...]   // alegações sem fonte, citações inexistentes, contradições
}

Critério de groundedness:
- 1.0: todas as expected_citations presentes, todos expected_facts cobertos, sem alegações fora do esperado.
- 0.85: todas as citações presentes, ≥80% dos fatos cobertos, sem invenção.
- 0.5: parcial — alguma citação ausente OU fato importante faltando.
- 0.0: alegações inventadas, citações fabricadas, contradição direta.
```

## Calibração

- 30 amostras com gabarito humano em `evals/v1/judges/groundedness.calibration.json` (a preencher).
- Cohen κ entre judge e humanos ≥0.6 obrigatório antes de uso em release.
- Recalibrar quando trocar modelo do judge.

## Ablação obrigatória

`scripts/run-judge-ablation.py` (a implementar) compara:

- Judge frontier vs. judge low-cost (delta deve ser <0.05 para low-cost ser usável).
- Judge com seed 42 vs. seed 1 (variância <0.03).

## Limitações conhecidas

- LLM-as-judge tem viés de tamanho (favorece respostas longas). Mitigado por critério explícito ("alegações sem fonte" penaliza padding).
- Viés de posição (favorece primeira opção em comparação A/B). Não aplicável aqui — é classificação absoluta.
- Provider-specific quirks (Claude tende a ser conservador; GPT mais permissivo). Anti-mitigado: cross-provider check em release.

## Quando NÃO usar este judge

- Questões factuais com resposta única objetiva → use exact-match.
- Avaliação de criatividade → judge groundedness não serve.
- Avaliação de segurança (injection) → use `evals/v1/judges/injection-defense.md` (a criar em T6).
