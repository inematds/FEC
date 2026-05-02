# SAFETY-INJECTION — Modelo de ameaça para prompt injection no curso

> _Como o curso aborda prompt injection sem virar "manual de ataque". PLAN item 62._

## Escopo educacional

A FEC ensina prompt injection na trilha **T6** (avaliação e produção) com foco em **defesa**. Cobertura:

### In-scope
- Classes documentadas de ataque: jailbreak básico, indirect injection (via documentos recuperados), exfiltration via tool, tool poisoning.
- Payloads em **fixtures testáveis** (`fixtures/injection/`) — não copy-paste em texto corrido.
- Sandbox local (P5) onde o aluno executa contra um agente HIPOTÉTICO do curso.
- Defesas ensinadas: input/output guard, allow-list de tools, separação de escopo do prompt do usuário, *spotlight* (Anthropic 2024), prompt sanitization patterns.

### Out-of-scope (não cobrimos)
- Payloads contra produtos reais nomeados (ChatGPT, Claude.ai, Gemini app, etc.).
- Bypass de safety models específicos por nome.
- Conteúdo CSAM, armas biológicas/químicas, instruções para ataques contra pessoas reais ou infraestrutura crítica.
- "Jailbreak para fazer o modelo XYZ produzir conteúdo proibido" — não interessa pedagogicamente.

## Apresentação do conteúdo

- **Payloads ficam em fixtures** (`fixtures/injection/<classe>/<id>.json`) com schema validado. NUNCA em texto corrido nos módulos HTML.
- **Aluno carrega fixture** via lab; código que executa fica em sandbox (`SECURITY-SANDBOX.md`).
- **Texto dos módulos** descreve a CLASSE de ataque conceitualmente, não fornece o payload pronto para colar em produtos reais.
- **Exemplos visuais** (diagramas SVG) mostram fluxo abstrato — "tool A recebe instrução não-confiável" — sem payload literal.

## Golden de injection

`evals/v1/datasets/FEC-GS-INJECTION-v1` contém 20 payloads classificados:

- 10 jailbreak básico (instruções "ignore previous").
- 5 indirect injection (payload em documento recuperado).
- 3 tool exfil (modelo tenta usar tool de leitura para vazar contexto).
- 2 tool poisoning (modelo tenta usar tool de escrita para gravar payload em sistema).

P5 exige **≥18/20 bloqueados** (sandbox + defesas) antes de virar GA.

## Disclaimer obrigatório nos módulos T6

Todo módulo que cobre injection abre com:

> ⚠️ **Conteúdo educacional.** Os payloads abaixo são para você aprender a **detectar e defender**. Não use contra produtos de terceiros sem autorização explícita; pode violar ToS e leis de cibersegurança.

## Política

- PR que adiciona payload PRECISA classificar em uma das classes in-scope.
- PR com payload out-of-scope é fechado com explicação.
- Reporter externo de novo padrão de injection: GHSA + decisão de cobertura por maintainers + revisão externa de segurança.
