# ShadowGuardAI: Detecção e Pentest Autorizado de Software Gerado por IA

> Espelho em Markdown do `paper.tex` (trilha de Indústria e Inovação em SI, TII-SI, SBSI 2027),
> já com as correções do parecer de revisão de 23/11/2026. O PDF é gerado com
> `pdflatex paper; bibtex paper; pdflatex paper` (2×) **nesta pasta** (o `sbc-template.sty`
> precisa estar no diretório de trabalho).
>
> Pendência única: autores, filiação e e-mails (`[A PREENCHER]`).

---

## Abstract

AI coding assistants now write a growing share of production code, and studies report that a
large fraction of it is vulnerable. Off-the-shelf static analysis is reported to miss much of
that code, and compliance of AI-generated code against secure coding standards is rarely
evaluated. This pitch presents ShadowGuardAI, a service that combines local static analysis with
authorized assessment of the published application, maps every finding to CWE, OWASP Top 10 and
CWE Top 25, and refuses any active action without a signed rules of engagement. The prototype was
validated with 373 automated tests, 35 static rules over 38 scenarios and four authorized field
assessments that produced 51 findings, one critical and three high. Run on three of those
targets' published bundles, the same rules raised 20 alerts, none of them the four severe
authorization flaws. The monitoring and SSH stages were not exercised in the field.

## Resumo

Assistentes de código escrevem parcela crescente do software em produção, e estudos relatam que
parte relevante dele é vulnerável. A análise estática de autoria livre é relatada como capaz de
deixar passar boa parte desse código, e a conformidade do código gerado por IA frente a padrões
de código seguro é avaliada com raridade. Esta proposta apresenta o ShadowGuardAI, serviço que
combina análise estática local com avaliação autorizada da aplicação publicada, classifica cada
achado em CWE, OWASP Top 10 e CWE Top 25 e recusa executar ação ativa sem regras de operação
assinadas. O protótipo foi validado por 373 testes automatizados, 35 regras estáticas sobre 38
cenários e quatro avaliações de campo autorizadas, que produziram 51 achados, sendo um crítico e
três altos. Aplicadas aos bundles publicados de três desses alvos, as mesmas regras emitiram 20
alertas, nenhum deles correspondente aos quatro achados graves de autorização, e a maioria em
código de biblioteca de terceiros. Os estágios de monitoramento e de acesso por SSH não foram
exercitados em campo.

---

## 1. Contexto

Assistentes de código e agentes são utilizados de forma rotineira para produzir software, de modo
que o desenvolvedor que aprova uma solução porque ela passou nos testes funcionais pode deixar
vulnerabilidades no repositório sem perceber. A literatura que mede esse fenômeno não apresenta
um número único, pois os estudos contabilizam objetos e detectores diferentes.

O primeiro estudo desse tipo, sobre a prévia do GitHub Copilot em agosto de 2021, identificou que
aproximadamente 40% dos programas gerados eram vulneráveis (Pearce et al., 2021). Trabalhos
posteriores consideram só a saída funcionalmente correta: no BaxBench, os exploits têm
sucesso em torno da metade dos programas corretos de cada modelo (Vero et al., 2025), e em 186
tarefas de nível repositório 79,3% das soluções funcionais do SWE-Agent com Claude 4 Sonnet eram
inseguras (Zhao et al., 2026). A detecção é o problema prático: o Snyk Code deixou de apontar 64
programas vulneráveis que os exploits do BaxBench revelaram (Vero et al., 2025), e no
RealSec-Bench a precisão dos alertas do CodeQL revisados foi de 44,9% em 89 alertas (Wang et al.,
2026). Além disso, Blain e Noiseux relatam que seis ferramentas estáticas comerciais apontaram 19
dos 250 artefatos de seu corpus e 2 das 90 vulnerabilidades provadas por testemunhas de
satisfatibilidade do Z3, o que corresponde a 97,8% de omissão, caracterizada como lacuna
estrutural e não como problema de configuração (Blain & Noiseux, 2026).

Em um levantamento não sistemático de 20 fontes, nenhuma avalia a conformidade de código gerado
por IA contra padrões de código seguro como CWE e OWASP, que aparecem apenas como taxonomias para
escolher cenários e exploits. Diante dessa lacuna, este trabalho apresenta o ShadowGuardAI, um
serviço de análise estática e avaliação autorizada para equipes que adotam assistentes de código
e precisam de verificação barata a cada mudança, com rastreabilidade de auditoria e sem
transferência de código do cliente para fora da sua infraestrutura.

## 2. Processo

O ShadowGuardAI foi construído como prova de conceito iterativa sobre o motor de agente local da
própria equipe, em ciclos fechados por testes automatizados, e a suíte atual conta com 373 testes.
O motor opera um modelo local por meio do Ollama (Ollama, 2026), de modo que o código do cliente
não sai da máquina, e o modelo não executa nada: em uma máquina de estados determinística, escolhe
um verbo de um catálogo tipado, com leitura, escrita confinada e ações destrutivas sujeitas a
confirmação humana. O runtime valida a escolha, abstém-se quando a base é insuficiente e registra
cada etapa em arquivo JSONL append-only, com redação de segredos.

### Um ciclo de quatro estágios

A Figura 1 (`figs/architecture.pdf`) organiza a solução entre três atores: o usuário que executa
software gerado por IA, a equipe de TI do cliente, que pode ser uma pessoa ou um sistema ITSM, e
o agente.

**S1, monitoramento passivo.** Um sensor somente-leitura no endpoint observa processos, portas e
scripts e alerta o usuário sobre falhas encontradas por 35 regras estáticas e por análise de
dependências por versão, com SBOM em CycloneDX (OWASP CycloneDX, 2026).

**S2, triagem e alerta.** Uma porta fora da linha de base, ou um processo iniciado de código
desconhecido, gera alerta para a TI com a evidência, e os alertas permanecem na rede do cliente.

**S3, avaliação autorizada.** A TI aprova assinando regras de operação (ROE, de *rules of
engagement*) para aquele alerta, com autorizador, host, software, janela e técnicas, e sem ROE
válido o motor recusa executar. A avaliação assume duas formas conforme a técnica autorizada: a
externa, sobre a superfície publicada, e a partir de uma sessão SSH no host do usuário, que é a
variante desenhada para o endpoint. Em ambas, força bruta, negação de serviço, persistência,
escrita destrutiva, exfiltração e movimento lateral são recusadas, os verbos que alteram o host
exigem confirmação humana, e limite de requisições e interruptor de emergência delimitam a
sessão. A variante SSH é ativa por executar comandos no alvo, ainda que o verificador próprio
emita apenas 18 operações de leitura.

**S4, relatório duplo.** Os achados são normalizados, com CWE, CVSS e evidência, e mapeados para o
OWASP Top 10 (OWASP Foundation, 2026) e o CWE Top 25 (MITRE, 2026); sem referência a arquivo e
linha, ou à requisição e resposta com hash, o achado é relatado como hipótese, e o que não foi
testado é declarado. O usuário recebe um relatório conciso, a TI recebe um relatório completo com
manifesto de evidência sha256, e o reteste fecha o ciclo.

### Modelo de ameaça

Seguindo a classificação STRIDE por componente (Shostack, 2014), consideram-se o modelo local
adulterado (A1), conteúdo hostil no software monitorado, como injeção de prompt (A2), aprovação
falsificada ou assinada sem leitura (A3), telemetria adulterada (A4), abuso do canal SSH (A5),
kit externo comprometido (A6) e vazamento de relatório (A7). O portão do ROE foi exercitado por
uma bateria determinística de ações hostis, com escrita destrutiva, exfiltração, técnica proibida
e execução fora da janela, todas recusadas nos testes automatizados; a resistência a um modelo
adversarial, por injeção de prompt, permanece não avaliada.

### Indicadores medidos

Cada engagement registra achados por severidade, CWE e categoria OWASP, o escopo exercitado e as
lacunas não testadas, as ações bloqueadas pelo portão e o tempo até o relatório, e o reteste
compara achados fechados, novos e persistentes, conforme a unidade de análise do engagement
(Runeson & Höst, 2009); o contato técnico da organização classifica cada achado como confirmado,
falso positivo ou incerto. Somente agregados são publicados, e todo teste ativo exige ROE
documentado e consentimento conforme a LGPD.

## 3. Solução

Em laboratório, 373 testes automatizados cobrem o portão do ROE, o redactor de log, o cofre de
credenciais e o registro de auditoria; 35 regras de análise estática foram calibradas por 38
cenários autorais, com recall de 100% e precisão de 100% e nenhum achado em arquivo seguro, e a
ablação sobre o código da própria ferramenta apontou uma única regra disparando, a de severidade
informativo para o uso de `console.log`.

Em campo, quatro aplicações publicadas foram avaliadas em regime não destrutivo, sem criação de
conta e sem alteração de dados, com autorização do responsável em cada caso; duas tiveram regras
de engajamento documentadas e uma é produto próprio da equipe. Segundo os responsáveis, o desenvolvimento contou com os
assistentes Claude e Codex, mas a ferramenta não foi registrada por caso, de modo que a
atribuição dos achados a código gerado por IA permanece indiciária; o intake do produto passou a
registrar esse contexto. A Tabela 1 resume o escopo exercitado e os 51 achados.

**Tabela 1.** *Engagements de campo (out.–nov. 2026): escopo exercitado e achados por severidade
(C, A, M, B, I) — total 1, 3, 10, 18 e 19.*

| Aplicação | Funcionalidades e escopo exercitado | Achados |
|---|---|---|
| Delivery de restaurante | cardápio, pedido e pagamento; painel de gestão; 5 hosts; Auth, Firestore e Storage | 0/0/3/8/7 |
| Gestão patrimonial e de contratações públicas | transferência de bens, painel operacional, convites; 43 tabelas, 35 RPCs e 5 edge functions | 0/3/4/2/3 |
| Portal por assinatura de estratégias | biblioteca, comparativo com backtest, minicurso; páginas protegidas e respostas RSC | 1/0/1/4/4 |
| Aplicativo de fitness (produto próprio) | treinos, sincronização e histórico; 138 transações e sessão de teste fornecida | 0/0/2/4/5 |

*Nota.* Nenhum dado de cliente é identificado; os relatórios originais permanecem em `private/`
no repositório do motor. Fonte: elaboração própria.

Para testar a afirmação sobre análise estática, as 35 regras foram aplicadas aos bundles
publicados de três dos quatro alvos, os disponíveis localmente. As regras emitiram 20 alertas, a
maioria sobre código de biblioteca empacotado, e nenhum correspondia às quatro falhas mais graves;
o único alerta de severidade alta no backend, a chave publicável embutida no bundle, é pública por
desenho e foi reclassificada na revisão manual. A medição é pequena e sobre código minificado, mas
mostra, no mesmo corpus, o que a regra aponta e o que a falha explora.

A leitura conjunta revela um padrão que sustenta a proposta. Em três das quatro aplicações, a
camada de dados estava endurecida: autorização por linha em todas as tabelas testadas,
armazenamento negando listagem anônima e controle de acesso de objetos recusando leitura sem
sessão, além de autenticação, proteção contra CSRF e limite de requisições funcionando. As falhas
concentraram-se na borda de autorização, e não na persistência: funções de API executáveis sem
autenticação, uma que bloqueia contas alheias e outra que aprova a transferência de patrimônio;
dados proprietários serializados antes do redirecionamento e devolvidos no corpo da resposta;
cadastro aberto somado a painel administrativo sem defesa em profundidade; e documento servido
pela CDN sem cabeçalhos, ainda que a API os enviasse.

Esse resultado é consistente com a lacuna estrutural relatada pela literatura (Blain & Noiseux,
2026): o achado crítico e os três altos são falhas de autorização e de desenho, classificadas como
CWE-862, CWE-285 e CWE-200, e nenhum corresponde a um padrão coberto pelas 35 regras. A detecção
útil veio da superfície publicada, do bundle e da prova de conceito controlada, e não do
verificador de padrões. Os quatro relatórios saíram por um único operador, três no mesmo dia e um
no dia seguinte.

### Limitações

O conjunto de evidências tem limites declarados. Os casos são quatro, auto-selecionados, de ramos
distintos e com escalas de severidade heterogêneas (apenas um aplicou CVSS); um é produto próprio e a origem de geração foi apenas declarada, sem registro por caso; dois não tiveram sessão autenticada, de modo
que falhas internas ao app logado permanecem não testadas; e a cobertura é reportada em lugar do
recall de campo. Os cenários do bench são autorais, e falhas de desenho (A04 do OWASP Top 10) não
são detectáveis por análise estática. Próximos passos: monitoramento e SSH em host próprio, teste do portão com modelo adversarial e
medição das regras com CWEval (Peng et al., 2025).

---

## Referências

As entradas completas, com DOI/arXiv, estão em `references.bib`.

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
  Benchmarking Vulnerability of Agent-Generated Code in Real-World Tasks*. arXiv:2512.03262.
