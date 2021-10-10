import controle_colaboradores_api.apps.localidades_brasileiras.management.commands.cadastrar_localidades_brasileiras\
    as localidades_brasileiras

class TestCommand:

    def test_handle(self, db, mocker):
        spy_ufs = mocker.spy(localidades_brasileiras.Command, '_cadastrar_unidades_federativas')
        spy_municipios = mocker.spy(localidades_brasileiras.Command, '_cadastrar_municipios')
        spy_relacao = mocker.spy(localidades_brasileiras.Command, '_relacionar_capitais_com_ufs')

        assert localidades_brasileiras.Command().handle() == "Fim da execução bem sucedida."
        assert spy_ufs.call_count == 1
        assert spy_municipios.call_count == 1
        assert spy_relacao.call_count == 1

