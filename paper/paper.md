# ShadowGuardAI: Detecção Contínua e Pentest Autorizado de Software Gerado por IA

> Espelho em Markdown do `paper.tex` (versão submetida à trilha de Indústria e Inovação em SI,
> TII-SI, SBSI 2027). O PDF é gerado com `pdflatex` + `bibtex` a partir do `.tex`; este arquivo
> serve para revisão de texto e para leitura no GitHub.
>
> Pendências marcadas como `[A PREENCHER]`: autores, filiação e e-mails.

**Autores:** [A PREENCHER]
**Filiação:** [A PREENCHER]
**E-mails:** [A PREENCHER]

---

## Abstract

AI coding assistants and agents now write a growing share of production code, and studies that
measure the result report that a large fraction of it is vulnerable. Off-the-shelf static
analysis is reported to miss much of that code, and compliance of AI-generated code against
secure coding standards is rarely evaluated. This pitch presents ShadowGuardAI, a continuous
monitoring and authorized assessment service for AI-generated software, which runs a local
model over a typed verb catalogue, maps every finding to CWE, OWASP Top 10 and CWE Top 25, and
refuses any active action without a signed rules of engagement. The prototype was validated
with 373 automated tests, 35 static analysis rules over 38 scenarios and four authorized field
assessments that produced 51 findings, one critical and three high, none detectable by
pattern-based static analysis alone.

## Resumo

Assistentes de código e agentes de inteligência artificial escrevem parcela crescente do
software em produção, e estudos que medem esse resultado relatam que parte relevante dele é
vulnerável. A análise estática de autoria livre é relatada como capaz de deixar passar boa
parte desse código, e a conformidade do código gerado por IA frente a padrões de código seguro
é avaliada com raridade. Esta proposta apresenta o ShadowGuardAI, serviço de monitoramento
contínuo e de avaliação autorizada de software gerado por IA, que opera um modelo local sobre
um catálogo de verbos tipados, classifica cada achado em CWE, OWASP Top 10 e CWE Top 25 e
recusa executar ação ativa sem regras de operação assinadas. O protótipo foi validado por 373
testes automatizados, 35 regras de análise estática sobre 38 cenários e quatro avaliações de
campo autorizadas, que produziram 51 achados, sendo um crítico e três altos, nenhum deles
detectável apenas por análise estática de padrões.

---

## 1. Contexto

Assistentes de código e agentes são utilizados de forma rotineira para produzir software, de
modo que o desenvolvedor que aprova uma solução porque ela passou nos testes funcionais pode
deixar vulnerabilidades no repositório sem perceber. A literatura que mede esse fenômeno não
apresenta um número único, pois os estudos contabilizam objetos e detectores diferentes.

O primeiro estudo desse tipo, sobre a prévia do GitHub Copilot em agosto de 2021, identificou
que aproximadamente 40% dos programas gerados eram vulneráveis (Pearce et al., 2021). Trabalhos
posteriores consideram apenas a saída funcionalmente correta: no BaxBench, que executa exploits
escritos por especialistas contra o código de onze modelos, os exploits têm sucesso em torno da
metade dos programas corretos de cada modelo (Vero et al., 2025), e em 186 tarefas de nível
repositório o SWE-Agent com Claude 4 Sonnet resolveu 57,0% das tarefas de forma funcional e
11,8% de forma também segura, o que corresponde a 79,3% das soluções funcionais inseguras
(Zhao et al., 2026). A detecção é onde se situa o problema prático: no BaxBench, o Snyk Code
deixou de apontar 64 programas vulneráveis que os exploits revelaram (Vero et al., 2025), e no
RealSec-Bench os alertas do CodeQL revisados pelos autores atingiram precisão de 44,9% em 89
alertas, elevada a 81,7% com adjudicação em dois estágios (Wang et al., 2026). Além disso,
Blain e Noiseux relatam que seis ferramentas de análise estática comerciais apontaram 19 dos
250 artefatos de seu corpus e 2 das 90 vulnerabilidades provadas por testemunhas de
satisfatibilidade do Z3, o que corresponde a 97,8% de omissão, caracterizada como lacuna
estrutural e não como problema de configuração (Blain & Noiseux, 2026).

Nas 20 fontes revisadas pela equipe, nenhuma avalia a conformidade de código gerado por IA
contra padrões de código seguro como CWE e OWASP, que aparecem apenas como taxonomias para
escolher cenários e exploits. Diante dessa lacuna, este trabalho apresenta o ShadowGuardAI, um
serviço de monitoramento contínuo e avaliação autorizada para equipes que adotam assistentes de
código e precisam de verificação barata a cada mudança, com rastreabilidade de auditoria e sem
transferência de código do cliente para fora da sua infraestrutura.

## 2. Processo

O ShadowGuardAI foi construído como prova de conceito iterativa sobre o motor de agente local da
própria equipe, em ciclos de construção, medição e correção fechados por testes automatizados; a
suíte atual conta com 373 testes. O motor opera um modelo local por meio do Ollama (Ollama,
2026), de modo que o código do cliente não sai da máquina, e o modelo não executa nada: em uma
máquina de estados determinística, escolhe um verbo de um catálogo tipado, com leitura, escrita
confinada e ações destrutivas sujeitas a confirmação humana. O runtime valida a escolha,
abstém-se quando a base é insuficiente e registra cada etapa em arquivo JSONL append-only, com
redação de segredos.

### Um ciclo contínuo de quatro estágios

A Figura 1 (`figs/architecture.pdf`) organiza a solução como um ciclo entre três atores: o
usuário que executa software gerado por IA, a equipe de TI do cliente, que pode ser uma pessoa
ou um sistema ITSM, e o agente.

**S1, monitoramento passivo.** Um sensor somente-leitura no endpoint observa processos, portas em
escuta e scripts, e alerta o usuário sobre falhas básicas encontradas por 35 regras estáticas
sobre padrões típicos de código gerado por IA, como segredos embutidos, e por análise de
dependências por versão contra uma base de avisos mantida offline, com SBOM em CycloneDX (OWASP
CycloneDX, 2026).

**S2, triagem e alerta.** Uma porta fora da linha de base do endpoint, ou um processo iniciado a
partir de código desconhecido, gera alerta para a TI com a evidência correspondente, e os
alertas permanecem na rede do cliente.

**S3, pentest autorizado.** A TI aprova assinando regras de operação (ROE, de *rules of
engagement*) para aquele alerta, com autorizador, host, software, janela e técnicas, e sem ROE
válido o motor recusa executar. O agente abre então uma sessão SSH para a máquina do usuário e
conduz um pentest ativo do software e do host notificados: dentro das técnicas listadas no ROE,
executa comandos, avalia configuração e fronteiras de privilégio e, quando o software expõe
interface de rede, sonda a interface dentro do escopo aprovado. Força bruta, negação de serviço,
persistência, escrita destrutiva, exfiltração e movimento lateral são recusadas em qualquer
perfil, os verbos que alteram o host exigem confirmação humana, e limite de requisições e
interruptor de emergência delimitam a sessão. O pentest é ativo por executar comandos no alvo,
ainda que o verificador próprio emita apenas 19 operações de leitura; um kit externo de pentest,
opcional, pode ser acionado para sondas complementares, com saída tratada como não confiável.

**S4, relatório duplo.** Os achados são normalizados, com CWE, CVSS e evidência, e mapeados para o
OWASP Top 10 (OWASP Foundation, 2026) e o CWE Top 25 (MITRE, 2026); sem referência a arquivo e
linha, ou a requisição e resposta com hash, o achado é relatado como hipótese, e o que não foi
testado é declarado. O usuário recebe um relatório conciso, a TI recebe um relatório completo
com manifesto de evidência sha256, e o reteste fecha o ciclo.

### Modelo de ameaça

Seguindo a classificação STRIDE por componente (Shostack, 2014), consideram-se o modelo local
adulterado (A1), conteúdo hostil no software monitorado, como injeção de prompt (A2), aprovação
falsificada ou assinada sem leitura (A3), telemetria adulterada (A4), abuso do canal SSH (A5),
kit externo comprometido (A6) e vazamento de relatório (A7). O que vem do modelo, do endpoint ou
das ferramentas é tratado como não confiável e jamais decide a autorização: o ROE é verificado a
cada etapa, e a sessão SSH é vinculada ao host, à janela e às técnicas aprovadas.

### Indicadores medidos

Cada engagement registra achados por severidade, CWE e categoria OWASP, a cobertura declarada e
as lacunas não testadas, as ações bloqueadas pelo portão do ROE e as horas de operador, e o
reteste compara achados fechados, novos e persistentes, conforme a unidade de análise do
engagement (Runeson & Höst, 2009); o contato técnico da organização classifica cada achado como
confirmado, falso positivo ou incerto. Somente agregados são publicados, e todo teste ativo exige
ROE assinado e consentimento conforme a LGPD.

## 3. Solução

O protótipo foi validado em duas frentes: laboratório e campo. Em laboratório, 373 testes
automatizados cobrem o portão do ROE, o redactor de log, o cofre de credenciais e o registro de
auditoria; 35 regras de análise estática foram calibradas por 38 cenários autorais, com recall de
100% e precisão de 100% e nenhum achado em arquivo seguro, e a ablação sobre o código da própria
ferramenta apontou uma única regra disparando, a de severidade informativo para o uso de
`console.log`. O portão do ROE falha de forma fechada e bloqueia, por exemplo, perfil ativo sem
ROE válido, execução fora da janela e requisição mutante em perfil passivo.

### Resultados de campo

Em campo, quatro aplicações publicadas foram avaliadas com autorização do responsável, em regime
não destrutivo, sem criação de conta de teste e sem alteração de dados, dois deles sob ROE
assinado. No total foram 51 achados, sendo um crítico, três altos, dez médios, 18 baixos e 19
informativos.

**Tabela 1.** *Engagements de campo: ramo, funcionalidades avaliadas e achados por severidade
(C, A, M, B, I).*

| Aplicação | Funcionalidades exercitadas | Achados |
|---|---|---|
| Delivery de restaurante | cardápio, carrinho, pedido e pagamento; painel de gestão; autenticação; borda de CDN | 0/0/3/8/7 |
| Gestão patrimonial e de contratações públicas | aprovação de transferência de bens, painel operacional, convites de processo, cadastro | 0/3/4/2/3 |
| Portal por assinatura de estratégias de investimento | biblioteca de estratégias, comparativo com backtest, minicurso, planos pagos | 1/0/1/4/4 |
| Aplicativo de fitness com gamificação | treinos, sincronização e histórico, acesso por código de uso único, administração | 0/0/2/4/5 |

*Nota.* Nenhum dado de cliente é identificado; os relatórios originais permanecem em `private/`
no repositório do motor. Fonte: elaboração própria.

A leitura conjunta dos casos revela um padrão que sustenta a proposta. Em três das quatro
aplicações, a camada de dados estava endurecida: autorização por linha habilitada em todas as
tabelas testadas, armazenamento negando listagem anônima e controle de acesso de objetos
recusando leitura sem sessão, além de autenticação, proteção contra CSRF e limite de requisições
funcionando. As falhas concentraram-se na borda de autorização, e não na persistência: funções de
API executáveis sem autenticação, incluindo uma que permite bloquear contas alheias e outra que
aprova a transferência de patrimônio; dados proprietários serializados antes do redirecionamento
e devolvidos no corpo da resposta; cadastro aberto somado a painel administrativo sem defesa em
profundidade; e documento e ativos servidos pela CDN sem cabeçalhos de segurança, ainda que a API
os enviasse.

Esse resultado tem consequência direta para a tese do trabalho. O achado crítico e os três altos
são falhas de autorização e de desenho, classificadas como CWE-862, CWE-285 e CWE-200, e nenhum
corresponde a um padrão que uma regra de análise estática detecte, o que confirma de forma
empírica a lacuna estrutural relatada pela literatura (Blain & Noiseux, 2026). A detecção útil
veio da superfície publicada, do bundle e da prova de conceito controlada, e não do verificador
de padrões.

### Limitações

O conjunto de evidências tem limites declarados. Os casos são quatro, de organizações
auto-selecionadas e de ramos distintos, o que limita a generalização; dois deles não tiveram
sessão autenticada, de modo que falhas internas ao app logado permanecem não testadas; e a
cobertura é reportada em lugar do recall de campo, que é desconhecível. Os cenários do bench são
autorais e medem cobertura e regressão. Falhas de desenho, como as da categoria A04 do OWASP Top
10, não são detectáveis por análise estática.

### Trabalho futuro

Como passos seguintes, os autores pretendem ampliar a série com os demais parceiros beta, manter
os retestes e importar datasets públicos de referência, como CWEval (Peng et al., 2025) e BaxBench
(Vero et al., 2025), com licença verificada.

---

## Referências

As entradas completas, com DOI/arXiv e nota de verificação, estão em `references.bib`.

- Blain, D., & Noiseux, M. (2026). *Broken by Default: A Formal Verification Study of Security
  Vulnerabilities in AI-Generated Code*. arXiv:2604.05292.
- MITRE. (2026). *CWE Top 25 Most Dangerous Software Weaknesses*. https://cwe.mitre.org/top25/
- Ollama. (2026). *Ollama*. https://ollama.com/
- OWASP CycloneDX. (2026). *CycloneDX Specification Overview*. https://cyclonedx.org/specification/overview/
- OWASP Foundation. (2026). *OWASP Top 10*. https://owasp.org/Top10/
- Pearce, H., Ahmad, B., Tan, B., Dolan-Gavitt, B., & Karri, R. (2021). *Asleep at the Keyboard?
  Assessing the Security of GitHub Copilot's Code Contributions*. arXiv:2108.09293.
- Peng, J., Cui, L., Huang, K., Yang, J., & Ray, B. (2025). *CWEval: Outcome-driven Evaluation on
  Functionality and Security of LLM Code Generation*. arXiv:2501.08200.
- Runeson, P., & Höst, M. (2009). Guidelines for Conducting and Reporting Case Study Research in
  Software Engineering. *Empirical Software Engineering*, 14(2), 131-164.
- Shostack, A. (2014). *Threat Modeling: Designing for Security*. Wiley.
- Vero, M., Mündler, N., Chibotaru, V., Raychev, V., Baader, M., Jovanović, N., He, J., & Vechev,
  M. (2025). *BaxBench: Can LLMs Generate Correct and Secure Backends?* ICML 2025, PMLR 267.
- Wang, Y., Zhang, Z., Wang, C., Xu, X., Liu, M., Wang, Y., Chen, J., & Zheng, Z. (2026).
  *RealSec-bench: A Benchmark for Evaluating Secure Code Generation in Real-World Repositories*.
  arXiv:2601.22706.
- Zhao, S., Wang, D., Zhang, K., Luo, J., Li, Z., & Li, L. (2026). *Is Vibe Coding Safe?
  Benchmarking Vulnerability of Agent-Generated Code in Real-World Tasks*. ICML 2026, PMLR 306.
