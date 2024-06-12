Automation QA - Release notes
----
**Version 9.5.0**                            

<em>11/06/2024</em>
- <font color='red'>__[Novo]__</font> - Geração do instalador.

**Version 9.4.0**                            

<em>11/06/2024</em>
- Geração da evidência.
- Implementação da abertura do browser em tempo de execução.
- Remoção dos drivers dos navegadores.

**Version 9.3.0**                            

<em>07/06/2024</em>
- Adaptação das funções e aumento da performance.
- Correção do log.

**Version 9.2.0**

<em>07/06/2024</em>
- Leitura dos passos do GitLab.
- Leitura dos parâmetros de cada passo.

**Version 9.1.0**
                                           
<em>03/06/2024</em>
- Remoção dos itens de interface.
- Conectando com o GitLab da T-Systems.

**Version 9.0.0**                            
                                           
<em>28/05/2024</em>
- Adaptação para o ambiente da T-Systems / GitLab.

**Version 8.6.0**                            
                                           
<em>18/03/2022</em>
- Atualização do arquivo de comparação para o BeyondCompare;
- Atualização de algumas bibliotecas do Python;
- O Edge Chromium com execução InPrivate;
- Merge com a versão do AutoUpdate (parcial).

**Version 8.5.1**                            
                                           
<em>08/03/2022</em>
- Correção da geração de evidência quando possui um passo com bug. Não apresentava o passo com falha.

**Version 8.5**                            
                                           
<em>07/03/2022</em>
- Atualização do arquivo de tradução para o inglês;
- Atualização da biblioteca de tradução do Google;
- Correção do Hash na comparação dos arquivos para tradução;
- Atualização do versão do Edge com o driver 99.0.1150.30 (Compilação oficial) (64 bits);
- Redução do texto do ReadMe, pois excede o tamanho do componente do Kivy.

**Version 8.4.1**                            
                                           
<em>11/02/2022</em>
- Correção do tratamento de Alert no Firefox com prompt.
 
**Version 8.4**                            
                                           
<em>10/02/2022</em>
- Exclusão da pasta build e dist após geração do pacote;
- Inclusão do botão "Gerar evidência" na tela de log; 
- Correção do tratamento de Alert no Firefox. 

**Version 8.3**                            
                                           
<em>09/02/2022</em>
- Atualização do Firefox versão 96.0.3 (64-bits);
- Correção na geração das evidências em branco.

**Version 8.2.1**                            
                                           
<em>04/02/2022</em>
- Atualização da versão 98.0.4758.82 do Google Chrome.

**Version 8.2**                            
                                           
<em>04/02/2022</em>  

- Tradução dos arquivos de configuração;
- Correção da validação do nome do caso de teste. Incluído o . (ponto);
- Correção da mensagem de caracter inválido para o nome do caso de teste;
- Correção no tratamento do teste com caracter inválido;
- Inclusão do tratamento caso um navegador não esteja instalado na máquina (Edge Legacy).
- Retirada do campo de test plan para geração das evidências;
- Atualização do arquivo "Notepad_Theme_Log_Automation.xml";
- Alteração do caminho do TestEnvironment para que fosse possível realizar o debug.

**Version 8.1**                            
                                           
<em>20/01/2022</em>  

- Corrigido erros na funcionalidade Validar;
- Inclusão do botão do rodar a automação na tela de console;
- Atualização das bibliotecas com as versões mais recentes;
- Atualização do requirements.txt;
- Correção de um erro no validate, quando informava "Passed" em um teste "Failed".

**Version 8.0**                            
                                           
<em>13/01/2022</em>  

- Inclusão do arquivo de configuração do log no pacote;
- Atualização do driver do Edge Chromium para o 97.0.1072.55 (64 bits);
- Inclusão das páginas .html para teste no TestEnvironment;
- Corrigido bug a executar print script em um teste de Desktop;
- Atualização do driver do IE 11;
- Aguardar o retorno da conexão com o Azure eternamente;  
- Adicionada a opção "Ctrl + <qualquer tecla>" e "Alt + <qualquer tecla>".

**Version 7.9**                            
                                           
<em>07/01/2022</em>                        
                                            
- Adicionado alerta de token expirado, quando executado por linha de comando;
- Corrigido adição errada do comentário na Run, mesmo com teste Passed;
- Utilização do Python 3.9 (Melhoria de performance).

**Version 7.8**                            
                                           
<em>03/01/2022</em>
                                            
- Correção na deleção dos arquivos. 