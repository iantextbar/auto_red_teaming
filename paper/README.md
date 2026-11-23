# Paper SBSI 2027 — Trilha de Indústria e Inovação em SI (TII-SI)

Submissão de 4 páginas (2 a 4 permitidas, sem contar referências) sobre o ShadowGuardAI.
O prazo de submissão é **11/12/2026**, via JEMS-3.

## Arquivos

| Arquivo | Papel |
|---|---|
| `paper.tex` | fonte (português do Brasil, template SBC) |
| `paper.pdf` | PDF para submissão |
| `paper.md` | espelho em Markdown para revisão de texto |
| `references.bib` | 12 referências citadas |
| `sbc-template.sty`, `sbc.bst` | template oficial da SBC (não editar) |
| `figs/architecture.{tex,pdf}` | figura do ciclo de quatro estágios (TikZ) |

## Como compilar

O `sbc-template.sty` só é encontrado se o `paper.tex` estiver no **diretório de trabalho**.
Sem o BibTeX o PDF sai **sem referências** (parece caber em 4 páginas, mas não está pronto).

```powershell
cd docs/paper-sbsi-2027
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

A figura, se for editada, é recompilada dentro de `figs/`:

```powershell
pdflatex -interaction=nonstopmode figs/architecture.tex
```

## Checagens antes de submeter

1. **Corpo em 4 páginas e referências na página 5** — o texto tem ~2 linhas de folga; se
   acrescentar algo, recompile e confirme.
2. **Nenhum `[A PREENCHER]`** no PDF: hoje restam autores, filiação e e-mails.
3. **Zero citações pendentes**: `Select-String paper.log -Pattern "undefined"` não deve achar nada.
4. **Nenhum dado de cliente**: a seção 3 descreve os quatro casos por ramo e funcionalidades,
   sem nome, domínio, IP ou evidência. Os relatórios originais ficam em `private/`.
5. **Sigilo do repo**: `npm run secrecy` e `npm run lint:bom` verdes.

## Pendências

- [ ] Nomes, filiação e e-mails dos autores
- [x] Aval dos quatro avaliados para publicar os agregados anonimizados (confirmado)
- [ ] Revisão de texto pelos coautores
- [ ] Congelar os números na data da submissão (373 testes, 35 regras, 38 cenários, 51 achados,
      18 operações de leitura)
- [ ] Submissão no JEMS-3 (revisão simples, com nomes)

## Origem do texto

Rascunho inicial do Ian (12/11/2026) e seção de processo, figura e modelo de ameaça do PR #3 do
Etore (16/11/2026), no repositório `iantextbar/auto_red_teaming`. A versão em português, os
resultados de campo e o baseline estático foram escritos neste repositório.
