import datetime

import pytest
from model_bakery import baker
from model_bakery.recipe import Recipe, seq

from configuracoes.leitor_configuracoes import LeitorConfiguracoes
from controle_colaboradores_api.apps.api_questionarios.models import \
    QuestionarioTipo, \
    QuestionarioObjeto, \
    Questionario, \
    ProtocoloResposta, \
    PerguntaPadronizada, \
    Pergunta, \
    PerguntaModulo, \
    PerguntaTipo, \
    Resposta, \
    Arquivo, \
    VerificacaoResposta


@pytest.fixture
def questionario_tipo(db):
    return baker.make(QuestionarioTipo)


@pytest.fixture
def questionario_objeto(db):
    return baker.make(QuestionarioObjeto)


@pytest.fixture
def questionario(db, questionario_tipo, questionario_objeto):
    return baker.make(Questionario,
                      tipo=questionario_tipo,
                      objeto=questionario_objeto)


@pytest.fixture
def pergunta_padronizada(db, questionario_tipo, questionario_objeto):
    return baker.make(PerguntaPadronizada,
                      questionario_tipo=questionario_tipo,
                      questionario_objeto=questionario_objeto,
                      ordem='001')


@pytest.fixture
def perguntas_padronizadas(db, questionario_tipo, questionario_objeto):
    perguntas = baker.make(PerguntaPadronizada,
                           questionario_tipo=questionario_tipo,
                           questionario_objeto=questionario_objeto,
                           ordem=seq('00'),
                           _quantity=3)
    for p in perguntas:
        p.save()
    return perguntas


@pytest.fixture
def modulo(db, questionario):
    return baker.make(PerguntaModulo, ordem=1, questionario=questionario)


@pytest.fixture
def modulos(db, questionario):
    modulos = baker.make(PerguntaModulo,
                         nome=seq('Módulo'),
                         questionario=questionario,
                         ordem=seq(0),
                         _quantity=3)

    for m in modulos:
        m.save()
    return modulos


@pytest.fixture
def pergunta(db, modulo):
    return baker.make(Pergunta,
                      ordem='001',
                      modulo=modulo)


@pytest.fixture
def perguntas(db, modulo):
    perguntas = baker.make(Pergunta,
                           ordem=seq('00'),
                           modulo=modulo,
                           _quantity=3)
    for p in perguntas:
        p.save()
    return perguntas


@pytest.fixture
def pergunta_dependente(db, modulo, pergunta):
    return baker.make(Pergunta,
                      ordem='001001',
                      exibicao_dependente_da_resposta_certa_da_pergunta=pergunta,
                      modulo=modulo)


@pytest.fixture
def perguntas_dependentes(db, modulo, pergunta):
    return baker.make(Pergunta,
                      ordem=seq('00100'),
                      exibicao_dependente_da_resposta_certa_da_pergunta=pergunta,
                      modulo=modulo,
                      _quantity=3)


@pytest.fixture
def pergunta_tipo(db):
    return baker.make(PerguntaTipo)


@pytest.fixture
def protocolo_resposta(db, questionario):
    return baker.make(ProtocoloResposta, questionario=questionario)


@pytest.fixture
def protocolos_respostas(db, questionario):
    protocolos = baker.make(ProtocoloResposta,
                            questionario=questionario,
                            finalizado=False,
                            _quantity=3)

    for p in protocolos:
        p.save()
    return protocolos


@pytest.fixture
def respostas(db, protocolo_resposta):
    respostas = baker.make(Resposta,
                           protocolo=protocolo_resposta,
                           pergunta__opcional=False,
                           pergunta__resposta_correta_tipo_sim_ou_nao=True,
                           pergunta__peso=1,
                           resposta_sim_nao_naosei=True,
                           verificacao__resposta_condiz_com_realidade=True,
                           _quantity=3)

    for r in respostas:
        r.save()
    return respostas


@pytest.fixture
def resposta(db, protocolo_resposta):
    return baker.make(Resposta,
                      protocolo=protocolo_resposta,
                      pergunta__opcional=False,
                      pergunta__resposta_correta_tipo_sim_ou_nao=True,
                      pergunta__peso=1,
                      resposta_sim_nao_naosei=True,
                      verificacao__resposta_condiz_com_realidade=True)


@pytest.fixture
def verificacao_resposta(db):
    resposta_verificada = baker.make(Resposta,
                                     verificacao=None)
    return baker.make(VerificacaoResposta,
                      resposta_verificada=resposta_verificada)


@pytest.fixture
def arquivo(db, resposta):
    return baker.make(Arquivo,
                      resposta=resposta)


@pytest.fixture
def arquivos(db, resposta):
    arqs = baker.make(Arquivo,
                      resposta=resposta,
                      _quantity=3)

    for a in arqs:
        a.save()
    return arqs


class TestQuestionarioQuerySet:

    def test_proxima_versao_pelo_tipo_objeto_quando_uma_versao_existente(self,
                                                                         questionario,
                                                                         questionario_tipo,
                                                                         questionario_objeto):
        proxima_versao = Questionario.objects.proxima_versao_pelo_tipo_objeto(questionario_tipo, questionario_objeto)
        expected_proxima_versao = questionario.versao + 1
        assert proxima_versao == expected_proxima_versao

    def test_proxima_versao_pelo_tipo_objeto_quando_nenhuma_versao_existente(self,
                                                                             questionario_tipo,
                                                                             questionario_objeto):
        proxima_versao = Questionario.objects.proxima_versao_pelo_tipo_objeto(questionario_tipo, questionario_objeto)
        expected_proxima_versao = 1
        assert proxima_versao == expected_proxima_versao


class TestQuestionario:

    def test_str(self, questionario):
        questionario.tipo.nome = "Tipo A"
        questionario.objeto.nome = "Objeto A"
        str_questionario = str(questionario)
        assert str_questionario == "Tipo A - Objeto A"

    def test_save(self, mocker, questionario):
        questionario.versao = 4
        questionario.save()
        expected_questionario = Questionario.objects.get(pk=questionario.id)
        assert questionario == expected_questionario
        assert questionario.versao == expected_questionario.versao

    def test_delete(self, questionario):
        questionario.delete()

    def test_delete_com_protocolo_resposta_para_falhar(self, questionario, protocolo_resposta):
        with pytest.raises(Exception):
            questionario.delete()

    def test_finalizar(self, questionario):
        questionario.finalizado = False
        questionario.save()

        questionario.finalizar()
        questionario_da_database = Questionario.objects.get(pk=questionario.id)
        assert questionario_da_database.finalizado is True

    def test_desativar(self, questionario):
        questionario.ativo = True
        questionario.save()

        questionario.desativar()
        questionario_da_database = Questionario.objects.get(pk=questionario.id)
        assert questionario_da_database.ativo is False

    def test_ativar(self, questionario):
        questionario.ativo = False
        questionario.save()

        questionario.ativar()
        questionario_da_database = Questionario.objects.get(pk=questionario.id)
        assert questionario_da_database.ativo is True

    def test_criar_modulo_com_perguntas_padronizadas_do_tipo(self,
                                                             questionario,
                                                             perguntas_padronizadas):
        questionario._criar_modulo_com_perguntas_padronizadas_do_tipo()

        modulo = questionario.modulos.get(ordem=1)
        assert modulo.nome == f"Perguntas gerais - {questionario.tipo}"

    def test_criar_modulo_perguntas_padronizadas_do_objeto(self,
                                                           questionario,
                                                           perguntas_padronizadas):
        questionario._criar_modulo_perguntas_padronizadas_do_objeto()

        modulo = questionario.modulos.get(ordem=1)
        assert modulo.nome == f"Perguntas gerais - {questionario.objeto}"

    def test_copiar_perguntas_para_modulo(self, questionario, perguntas):
        perguntas_mocks_lista_ids = [p.id for p in perguntas]

        perguntas_queryset = Pergunta.objects.filter(pk__in=perguntas_mocks_lista_ids)
        novo_modulo = baker.make(PerguntaModulo, questionario=questionario)
        Questionario._copiar_perguntas_para_modulo(perguntas_queryset, novo_modulo)

        perguntas_copiadas = novo_modulo.perguntas.all()

        colunas_a_comparar = ['modulo', 'ordem', 'enunciado', 'observacoes', 'fundamentacao',
                              'tipo', 'reposta_correta_tipo_sim_ou_nao', 'opcional',
                              'visivel_para_destinatario', 'resultado_destacado', 'peso']

        for i in range(3):
            perguntas_com_colunas_filtradas = {k: v for k, v in perguntas[i].__dict__.items()
                                               if k in colunas_a_comparar}
            perguntas_copiadas_com_colunas_filtradas = {k: v for k, v in perguntas_copiadas[i].__dict__.items()
                                                        if k in colunas_a_comparar}
            print(perguntas_com_colunas_filtradas)
            print(perguntas_copiadas_com_colunas_filtradas)
            assert perguntas_com_colunas_filtradas == perguntas_copiadas_com_colunas_filtradas


class TestQuestionarioTipo:

    def test_str(self, questionario_tipo):
        questionario_tipo.nome = "Tipo A"
        assert str(questionario_tipo) == "Tipo A"


class TestQuestionarioObjeto:

    def test_str(self, questionario_objeto):
        questionario_objeto.nome = "Objeto A"
        assert str(questionario_objeto) == "Objeto A"


class TestPerguntaTipo:

    def test_str(self, pergunta_tipo):
        pergunta_tipo.nome = "Tipo A"
        assert str(pergunta_tipo) == "Tipo A"

    def test_delete(self, pergunta_tipo):
        with pytest.raises(Exception):
            pergunta_tipo.delete()


class TestPerguntaModuloQuerySet:

    def test_proxima_ordem_no_questionario_com_um_modulo(self, modulo):
        prox_ordem = PerguntaModulo.objects.proxima_ordem_no_questionario(modulo.questionario)
        assert prox_ordem == 2

    def test_proxima_ordem_no_questionario_sem_modulos(self, questionario):
        prox_ordem = PerguntaModulo.objects.proxima_ordem_no_questionario(questionario)
        assert prox_ordem == 1

    def test_proxima_ordem_no_questionario_com_tres_modulos(self, modulos):
        prox_ordem = PerguntaModulo.objects.proxima_ordem_no_questionario(modulos[0].questionario)
        assert prox_ordem == 4

    def test_reordenar_para_aumento_de_ordem(self, modulos):
        modulo1, modulo2, modulo3 = modulos
        assert modulo1.ordem == 1
        assert modulo2.ordem == 2
        assert modulo3.ordem == 3

        nova_ordem = 3
        PerguntaModulo.objects.reordenar_para_aumento_de_ordem(modulo1, nova_ordem)

        modulo1.ordem = nova_ordem
        modulo1.save()

        modulo1_reordenado = PerguntaModulo.objects.get(pk=modulo1.id)
        modulo2_reordenado = PerguntaModulo.objects.get(pk=modulo2.id)
        modulo3_reordenado = PerguntaModulo.objects.get(pk=modulo3.id)
        assert modulo2_reordenado.ordem == 1
        assert modulo3_reordenado.ordem == 2
        assert modulo1_reordenado.ordem == 3

    def test_reordenar_para_reducao_de_ordem(self, modulos):
        modulo1, modulo2, modulo3 = modulos
        assert modulo1.ordem == 1
        assert modulo2.ordem == 2
        assert modulo3.ordem == 3

        nova_ordem = 1
        PerguntaModulo.objects.reordenar_para_reducao_de_ordem(modulo3, nova_ordem)

        modulo3.ordem = nova_ordem
        modulo3.save()

        modulo1_reordenado = PerguntaModulo.objects.get(pk=modulo1.id)
        modulo2_reordenado = PerguntaModulo.objects.get(pk=modulo2.id)
        modulo3_reordenado = PerguntaModulo.objects.get(pk=modulo3.id)
        assert modulo3_reordenado.ordem == 1
        assert modulo1_reordenado.ordem == 2
        assert modulo2_reordenado.ordem == 3


class TestPerguntaModulo:

    def test_str(self, modulo):
        modulo.ordem = 1
        modulo.nome = "Módulo A"
        assert str(modulo) == "1 Módulo A"

    def test_mudar_ordem(self, modulo):
        modulo.ordem = 1
        modulo.save()

        modulo.mudar_ordem(3)
        m = PerguntaModulo.objects.get(pk=modulo.id)
        assert m.ordem == 3

        modulo.mudar_ordem(1)
        m = PerguntaModulo.objects.get(pk=modulo.id)
        assert m.ordem == 1

    def test_aumentar_ordem(self, modulo):
        modulo.ordem = 1
        modulo.save()

        modulo._aumentar_ordem(5)
        m = PerguntaModulo.objects.get(pk=modulo.id)
        assert m.ordem == 5

    def test_diminuir_ordem(self, modulo):
        modulo.ordem = 5
        modulo.save()

        modulo._diminuir_ordem(1)
        m = PerguntaModulo.objects.get(pk=modulo.id)
        assert m.ordem == 1


class TestPerguntaQuerySet:

    def test_proxima_ordem_no_modulo_sem_perguntas(self, modulo):
        prox_ordem = Pergunta.objects.proxima_ordem_no_modulo(modulo)
        assert prox_ordem == '001'

    def test_proxima_ordem_no_modulo_com_uma_pergunta(self, pergunta):
        prox_ordem = Pergunta.objects.proxima_ordem_no_modulo(pergunta.modulo)
        assert prox_ordem == '002'

    def test_proxima_ordem_no_modulo_com_tres_perguntas(self, modulo, perguntas):
        prox_ordem = Pergunta.objects.proxima_ordem_no_modulo(perguntas[0].modulo)
        assert prox_ordem == '004'

    def test_proxima_ordem_dependente_da_pergunta_que_nao_possui_dependentes(self, pergunta):
        prox_ordem_dependente = Pergunta.objects.proxima_ordem_dependente_da_pergunta(pergunta)
        assert prox_ordem_dependente == '001001'

    def test_proxima_ordem_dependente_da_pergunta_que_possui_um_dependente(self, pergunta_dependente):
        prox_ordem_dependente = Pergunta.objects.proxima_ordem_dependente_da_pergunta(
            pergunta_dependente.exibicao_dependente_da_resposta_certa_da_pergunta)
        assert prox_ordem_dependente == '001002'

    def test_proxima_ordem_dependente_da_pergunta_que_possui_tres_dependentes(self, perguntas_dependentes):
        prox_ordem_dependente = Pergunta.objects.proxima_ordem_dependente_da_pergunta(
            perguntas_dependentes[0].exibicao_dependente_da_resposta_certa_da_pergunta)
        assert prox_ordem_dependente == '001004'

    def test_reordenar_para_criacao_de_pergunta_nao_dependente(self, perguntas):
        pergunta1, pergunta2, pergunta3 = perguntas
        assert pergunta1.ordem == "001"
        assert pergunta2.ordem == "002"
        assert pergunta3.ordem == "003"

        pergunta_nova = baker.prepare(Pergunta,
                                      ordem='001',
                                      modulo=pergunta1.modulo,
                                      tipo=pergunta1.tipo)
        Pergunta.objects.reordenar_para_criacao_de_pergunta_nao_dependente(pergunta_nova)

        pergunta1_reordenada = Pergunta.objects.get(pk=pergunta1.id)
        pergunta2_reordenada = Pergunta.objects.get(pk=pergunta2.id)
        pergunta3_reordenada = Pergunta.objects.get(pk=pergunta3.id)
        assert pergunta_nova.ordem == "001"
        assert pergunta1_reordenada.ordem == "002"
        assert pergunta2_reordenada.ordem == "003"
        assert pergunta3_reordenada.ordem == "004"

    def test_reordenar_para_exclusao_de_pergunta_nao_dependente(self, perguntas):
        pergunta1, pergunta2, pergunta3 = perguntas
        assert pergunta1.ordem == "001"
        assert pergunta2.ordem == "002"
        assert pergunta3.ordem == "003"

        pergunta1.delete()
        Pergunta.objects.reordenar_para_exclusao_de_pergunta_nao_dependente(pergunta1)

        pergunta2_reordenada = Pergunta.objects.get(pk=pergunta2.id)
        pergunta3_reordenada = Pergunta.objects.get(pk=pergunta3.id)
        assert pergunta2_reordenada.ordem == "001"
        assert pergunta3_reordenada.ordem == "002"


class TestPergunta:

    def test_str(self, pergunta):
        pergunta.modulo.nome = "Módulo A"
        pergunta.enunciado = "Pergunta A"
        pergunta.ordem = "001"
        assert str(pergunta) == "(Módulo A) 001 Pergunta A"

    def test_checar_se_perguntas_dependente_e_determinante_pertencem_mesmo_modulo(self,
                                                                                  modulos,
                                                                                  pergunta,
                                                                                  pergunta_dependente):
        pergunta.modulo = modulos[0]
        pergunta_dependente.modulo = modulos[1]
        pergunta_dependente.exibicao_dependente_da_resposta_certa_da_pergunta = pergunta
        with pytest.raises(Exception):
            pergunta_dependente._checar_se_perguntas_dependente_e_determinante_pertencem_mesmo_modulo()


class TestPerguntaPadronizadaQuerySet:

    def test_padronizadas_pelo_tipo(self, questionario_tipo, perguntas_padronizadas):
        perguntas_encontradas = PerguntaPadronizada.objects.padronizadas_pelo_tipo(questionario_tipo)
        for i, p in enumerate(perguntas_padronizadas):
            assert p.id == perguntas_encontradas[i].id

    def test_padronizadas_pelo_objeto(self, questionario_objeto, perguntas_padronizadas):
        perguntas_encontradas = PerguntaPadronizada.objects.padronizadas_pelo_objeto(questionario_objeto)
        for i, p in enumerate(perguntas_padronizadas):
            assert p.id == perguntas_encontradas[i].id


class TestPerguntaPadronizada:

    def test_str(self, pergunta_padronizada):
        pergunta_padronizada.questionario_tipo.nome = "Tipo A"
        pergunta_padronizada.questionario_objeto.nome = "Objeto A"
        pergunta_padronizada.ordem = "001"
        pergunta_padronizada.enunciado = "Pergunta A"
        assert str(pergunta_padronizada) == "(Tipo: Tipo A) 001 Pergunta A"

        pergunta_padronizada.questionario_tipo = None
        assert str(pergunta_padronizada) == "(Objeto: Objeto A) 001 Pergunta A"


class TestProtocoloRespostaQuerySet:

    def test_nao_finalizados(self, protocolos_respostas):
        protocolos_encontrados = ProtocoloResposta.objects.nao_finalizados()
        for i, p in enumerate(protocolos_respostas):
            assert p.id == protocolos_encontrados[i].id

    def test_nao_finalizados_do_questionario(self, protocolos_respostas):
        protocolos_encontrados = ProtocoloResposta.objects.nao_finalizados_do_questionario(
            protocolos_respostas[0].questionario)
        for i, p in enumerate(protocolos_respostas):
            assert p.id == protocolos_encontrados[i].id

    def test_finalizados_do_questionario(self, protocolos_respostas):
        for p in protocolos_respostas:
            p.finalizado = True
            p.save()

        protocolos_encontrados = ProtocoloResposta.objects.finalizados_do_questionario(
            protocolos_respostas[0].questionario)
        for i, p in enumerate(protocolos_respostas):
            assert p.id == protocolos_encontrados[i].id


class TestProtocoloResposta:

    def test_str(self, protocolo_resposta):
        protocolo_resposta.questionario.tipo.nome = "Tipo A"
        protocolo_resposta.questionario.objeto.nome = "Objeto A"
        protocolo_resposta.finalizado = True
        agora = datetime.datetime.now()
        protocolo_resposta.modificacao = agora
        assert str(
            protocolo_resposta) == f'Questionario: Tipo A - Objeto A | Usuário: {protocolo_resposta.usuario} | Finalizado: True ' \
                                   f'| Modificação: {agora}'

    def test_pontos_para_calculo_percentual_de_acerto(self, protocolo_resposta, respostas):
        assert protocolo_resposta.percentual_de_acerto == 100

        respostas[0].resposta_sim_nao_naosei = False
        respostas[0].save()
        assert protocolo_resposta.percentual_de_acerto == 66.67

        respostas[1].resposta_sim_nao_naosei = False
        respostas[1].pergunta.peso = 2
        respostas[1].pergunta.save()
        respostas[1].save()
        assert protocolo_resposta.percentual_de_acerto == 25

        respostas[2].pergunta.peso = 4
        respostas[2].pergunta.save()
        respostas[2].resposta_sim_nao_naosei = True
        respostas[2].save()
        assert protocolo_resposta.percentual_de_acerto == 57.14


class TestRespostaQuerySet:

    def test_respostas_do_protocolo_resposta(self, protocolo_resposta, respostas):
        respostas_encontradas = Resposta.objects.respostas_do_protocolo_resposta(protocolo_resposta)
        for i, r in enumerate(respostas):
            assert r.id == respostas_encontradas[i].id


class TestResposta:

    def test_tipo_da_pergunta(self, resposta, pergunta_tipo):
        resposta.pergunta.tipo = pergunta_tipo
        assert resposta.tipo_da_pergunta == pergunta_tipo

    def test_entra_para_calculo_percentual_de_acerto(self, resposta):
        resposta.pergunta.opcional = False
        resposta.pergunta.resposta_correta_tipo_sim_ou_nao = True
        resposta.pergunta.save()
        assert resposta.entra_para_calculo_percentual_de_acerto == True

        resposta.pergunta.opcional = True
        resposta.pergunta.save()
        assert resposta.entra_para_calculo_percentual_de_acerto == False

    def test_pontos_para_calculo_percentual_de_acerto(self, resposta):
        # Resposta entra para o cálculo
        resposta.pergunta.resposta_correta_tipo_sim_ou_nao = True
        resposta.pergunta.opcional = False
        resposta.pergunta.save()

        # Resposta correta
        resposta.resposta_sim_nao_naosei = True
        resposta.pergunta.peso = 2
        resposta.pergunta.save()
        resposta.save()
        assert resposta.pontos_para_calculo_percentual_de_acerto == 2

        # Resposta correta com verificação que corrige a resposta para incorreta
        resposta.verificacao.resposta_condiz_com_realidade = False
        resposta.verificacao.save()
        assert resposta.pontos_para_calculo_percentual_de_acerto == 0

        # Resposta incorreta
        resposta.resposta_sim_nao_naosei = False
        resposta.verificacao.resposta_condiz_com_realidade = True
        resposta.verificacao.save()
        resposta.pergunta.save()
        resposta.save()
        assert resposta.pontos_para_calculo_percentual_de_acerto == 0

        # Resposta incorreta com verificação que corrige a resposta para correta
        resposta.verificacao.resposta_condiz_com_realidade = False
        resposta.verificacao.save()
        assert resposta.pontos_para_calculo_percentual_de_acerto == 2

        # Resposta não entra para o cálculo
        resposta.pergunta.opcional = True
        resposta.pergunta.save()
        assert resposta.pontos_para_calculo_percentual_de_acerto == 0

    def test_peso_para_calculo_percentual_de_acerto(self, resposta):
        # Resposta entra para o cálculo
        resposta.pergunta.resposta_correta_tipo_sim_ou_nao = True
        resposta.pergunta.opcional = False
        resposta.pergunta.peso = 2
        resposta.pergunta.save()
        assert resposta.peso_para_calculo_percentual_de_acerto == 2

        # Resposta não entra para o cálculo
        resposta.pergunta.opcional = True
        resposta.pergunta.save()
        assert resposta.peso_para_calculo_percentual_de_acerto == 0

    def test_str(self, resposta):
        assert str(resposta) == f'Protocolo: {resposta.protocolo} | Pergunta: {resposta.pergunta}'


class TestArquivoQuerySet:

    def test_arquivos_da_resposta(self, resposta):
        arquivos_encontrados = Arquivo.objects.arquivos_da_resposta(resposta)
        for i, a in enumerate(resposta.arquivos.all()):
            assert a.id == arquivos_encontrados[i].id


class TestArquivo:

    def test_link_publico(self, arquivo):
        link_bucket = LeitorConfiguracoes.obter_configuracao_especifica("armazenamento")["link_bucket_dos_arquivos"]
        arquivo.acesso_publico = True
        arquivo.nome = "Arquivo1"
        arquivo.caminho_relativo = "pasta/subpasta"
        arquivo.save()
        assert arquivo.link_publico == f'{link_bucket}/pasta/subpasta/Arquivo1'

        arquivo.acesso_publico = False
        assert arquivo.link_publico == "Não há link público. O acesso ao arquivo é restrito."

    def test_str(self, arquivo):
        arquivo.nome = "Arquivo1"
        assert str(arquivo) == "Arquivo1"


class TestVerificacaoResposta:

    def test_str(self, verificacao_resposta):
        agora = datetime.datetime.now()
        verificacao_resposta.modificacao = agora
        assert str(verificacao_resposta) == \
               f'Resposta verificada: {verificacao_resposta.resposta_verificada} ' \
               f'| Usuário da verificação: {verificacao_resposta.usuario_modificacao} ' \
               f'| Modificação: {agora}'
