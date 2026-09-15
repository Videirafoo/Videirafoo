# Segurança

Este repositório é educacional e público. Mesmo assim, falhas de segurança devem ser tratadas com cuidado.

## Não publique segredos

Nunca envie em issues, pull requests, screenshots, commits ou exemplos:

- senhas;
- tokens do GitHub;
- chaves de API;
- cookies de sessão;
- credenciais de banco de dados;
- arquivos `.env` reais;
- dados pessoais sensíveis.

## Como relatar um problema

Se o problema for uma falha comum sem exposição de segredo, abra uma issue descrevendo:

1. onde o problema ocorre;
2. como reproduzir;
3. qual impacto foi observado;
4. qual comportamento era esperado.

Se o relato exigir compartilhar uma credencial, token, dado privado ou informação que aumente o risco de exploração, **não publique esse material no repositório**. Revogue ou troque o segredo primeiro e use um canal privado apropriado da plataforma.

## Escopo atual

O GitHub Student Dashboard analisa apenas informações públicas do GitHub. A aplicação não precisa de credenciais do usuário para o fluxo público padrão.

Variáveis opcionais como `GITHUB_TOKEN` e `OPENAI_API_KEY` devem existir somente no ambiente de execução e nunca no código versionado.

## Princípios

- menor privilégio;
- evidência antes de conclusão;
- conteúdo externo tratado como não confiável;
- nenhuma chave embutida no código;
- falhas externas não devem alterar checks determinísticos;
- dependências e CI devem permanecer revisáveis.
