# Security Design | ambiente local

## Ativos e fronteiras

Contas, hash de senha, sessão, titularidade de eventos, ingressos/códigos, chave de parceiro e integridade financeira. Dados fictícios apenas. Web usa cookie de sessão e CSRF; API autentica chave por header e não aceita cookie como alternativa. Banco/worker restritos à rede Compose. Não usar cartão real.

| Ameaça | Controle | Evidência |
|---|---|---|
| IDOR por URL/POST | Query de dono + guarda server-side antes de mostrar dados; 404 para outro dono | A07/X03/X11/A28 |
| Escalação por role no cadastro | Ignorar/rejeitar role do cliente e fixar participant | A06 |
| Vazamento de ingressos | Filtrar participant_id; não usar buyer_email como identidade | A20/X16 |
| CSRF | Middleware Django e token nos POST web; logout POST; API só key e CSRF exemption localizada | testes de CSRF real |
| Injeção | ORM parametrizado; sem SQL string formatada; escape de templates | testes input e revisão |
| Chave ausente/inválida | Compare_digest e autenticação antes do parsing, não registrar chave | A23 |
| PAN e senha em log | Não persistir PAN nem raw body; redaction e hash framework | A17/A06 |
| Corrida e replay | Lock comum, estados terminais, check-in idempotente quanto ao efeito | A14–A16/A25–A26 |
| Credenciais demo expostas | Apenas loopback; defaults explicitamente locais, sem segredos reais; .gitignore .env | A04 |

Sessão padrão server-side, cookie HttpOnly/SameSite=Lax, secure somente sob HTTPS (local HTTP deve funcionar), expiração planejada 8h, rotação no login e invalidação logout. Não usar open redirect: next só caminho local validado. Login com mensagens genéricas, validadores de senha do Django; seed usa hasher, não texto puro. Escapar nomes de evento e usuários no HTML. Limite de payload JSON de 16 KiB, campos de formulário com limites, preço/capacidade dentro do tipo persistente. Não incluir stack trace em erro HTTP padrão; DEBUG desativado no modo avaliador. Rate limiting de produção fora do escopo, nunca comprometer teste 30 concorrentes. TLS público e gestão real de segredo fora de escopo; não publicar serviço de demonstração.
