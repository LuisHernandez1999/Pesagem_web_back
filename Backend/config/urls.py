"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from apps.infra.auth.views.login_views import LoginApiView
from apps.infra.auth.views.refresh_token_view import RefreshTokenView
from apps.infra.auth.views.register_views import RegisterUserAPIView
from apps.infra.auth.views.generate_invite_view import GenerateInviteAPIView
from apps.infra.auth.views.register_views import RegisterByInviteAPIView
from apps.veiculo.views.veiculos_views import (VeiculoListApiView,
                                               VeiculoCreateApiView,
                                               VeiculoRankingPesagemApiView)
from apps.cooperativa.views.cooperativa_views import (CooperativaCreateAPIView,
                                                      EficienciaCooperativaRankingAPIView)
from apps.colaborador.views.colaborador_views import (ColaboradorCreateApiView,
                                                      ColaboradorListApiView)
from apps.pesagem.views.pesagem_views import (PesagemCreateApiView,
                                              PesagemTipoServicoView,
                                               PesagemListApiView
                                              ,ExibirPesagemPorMesAPIView
                                              ,PesagemGerarDocumentoAPIView)
from apps.os.views.os_views import (OrdemServicoCreateView,
                                    OrdemServicoVisualizacaoAPIView)
from apps.movimentacao.views.movimentacao_views import (MovimentacaoCreateAPIView,
                                                        MovimentacaoListAPIView)
from apps.insumos.views.insumos_views import (InsumoCreateAPIView,
                                              InsumoListAPIView)
from apps.celular.views.celular_views import (CelularCreateAPIView,CelularListAPIView,
                                              CelularDeleteAPIView,CelularUpdateAPIView,)
from apps.confirmacao.views.confirmacao_views import (ConfirmacaoServicoCreateView)
from apps.soltura.views.soltura_views import (RemocaoListView,SeletivaListView,
                                              DomiciliarListView,SolturaAnalyticsRemocaoView
                                              ,SolturaAnalyticsDomiciliarView,
                                              SolturaCreateView,
                                              SolturaAnalyticsSeletivaView)
from apps.soltura.views.rota_views import (RotaCreateView,RotaListView
                                           ,RotaDeleteView,RotaUpdateView)
from apps.soltura.views.excel.excel_views import (DomiciliarReportView,SeletivaReportView,
                                            RemocaoReportView,)
from apps.soltura.views.excel.excel_status_views import ReportStatusView
from apps.soltura.views.excel.excel_download_views import ReportDownloadView
from apps.averiguacao.views.averiguacao_views import (AveriguacaoEstatisticasSemanaApiView,
                                                      AveriguacaoCreateApiView,
                                                      AveriguacaoListApiView,
                                                      AveriguacaoDetailApiView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginApiView.as_view(), name="login"),
    path("auth/refresh/",RefreshTokenView.as_view(),name="RefreshToken"),
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("api/invite/", GenerateInviteAPIView.as_view(),name="Invite"),
    path("api/register-by-invite/", RegisterByInviteAPIView.as_view(),name="InviteRegister"),
    path("api/veiculos-list/",VeiculoListApiView.as_view(),name="VeiculosList"),
    path("api/veiculo-create/",VeiculoCreateApiView.as_view(),name="VeiculoCreate"),
    path("api/create-colaborador/",ColaboradorCreateApiView.as_view(),name="ColaboradorCreate"),
    path("api/colaborador-list/",ColaboradorListApiView.as_view(),name="ColaboradorList"),
    path("api/veiculos-ranking/",VeiculoRankingPesagemApiView.as_view(),name=" VeiculoListRanking"),
    path("api/create-cooperativa/",CooperativaCreateAPIView.as_view(),name="CooperativaCreate"),
    path("api/cooperativa-ranking/", EficienciaCooperativaRankingAPIView.as_view(), name="CooperativaRanking"),
    path("api/create-pesagem/",PesagemCreateApiView.as_view(),name="CreatePesagem"),
    path("api/pesagem-list/",PesagemListApiView.as_view(),name="PesagemList"),
    path("api/pesagem-list-por-mes/",ExibirPesagemPorMesAPIView.as_view(),name="PesagemListPorMes"),
    path("api/pesagem-tipo_servico/",PesagemTipoServicoView.as_view(),name="PesagemList"),
    path("api/pesagem-excel/",PesagemGerarDocumentoAPIView.as_view(),name="PesagemExcel"),
    path("api/os-create/",OrdemServicoCreateView.as_view(),name="OrdemServicoCreate"),
    path("api/os-list/",OrdemServicoVisualizacaoAPIView.as_view(),name="list-Os"),
    path("api/movimentacao-create/",MovimentacaoCreateAPIView.as_view(),name="MovimentacaoCreate"),
    path("api/movimentacao-list/",MovimentacaoListAPIView.as_view(),name='MovimentacaoList'),
    path("api/insumos-create/",InsumoCreateAPIView.as_view(),name="InsumosCreate"),
    path("api/insumos-list/",InsumoListAPIView.as_view(),name="InsumosList"),
    path("api/create-celular/",CelularCreateAPIView.as_view(),name="CelularCreate"),
    path("api/list-celular/",CelularListAPIView.as_view(),name="ListCelular"),
    path("api/celular/<int:id_celular>/delete/",  CelularDeleteAPIView.as_view(),name="CelularDelete"),
    path("api/celular/<int:id_celular>/update/",  CelularUpdateAPIView.as_view(),name="CelularUpdate"),
    path("api/create-confirmacao/",ConfirmacaoServicoCreateView.as_view(),name="CreateConfirmacao"),
    path("api/solturas/create/", SolturaCreateView.as_view(),name="CreateService"),
    path("api/solturas/remocao/", RemocaoListView.as_view(),name="RemocaoList"),
    path("api/solturas/seletiva/", SeletivaListView.as_view(),name="SeletivaList"),
    path("api/solturas/domiciliar/", DomiciliarListView.as_view(),name="DomiciliarList"),
    path("api/solturas-charts/remocao/",SolturaAnalyticsRemocaoView.as_view(),name="analytics-soltura-remocao",),
    path("api/solturas-charts/seletiva/",SolturaAnalyticsSeletivaView.as_view(),name="analytics-soltura-seletiva",),
    path("api/solturas-charts/domiciliar/",SolturaAnalyticsDomiciliarView.as_view(),name="analytics-soltura-domiciliar",),
    path('api/excel/remocao/', RemocaoReportView.as_view(), name='ExcelRemocao'),
    path('api/excel/domiciliar/', DomiciliarReportView.as_view(), name='ExcelDomiciliar'),
    path('api/excel/seletiva/', SeletivaReportView.as_view(), name='ExcelSeletiva'),
    path("reports/status/<uuid:task_id>/",ReportStatusView.as_view(),name="relatorio-status"),
    path("reports/download/<str:nome_arquivo>/",ReportDownloadView.as_view(),name="relatorio-download"),
    path("api/rota/", RotaCreateView.as_view()),
    path("api/rota/list/", RotaListView.as_view()),
    path("api/rota/<int:id_rota>/", RotaUpdateView.as_view()),
    path("api/rota/<int:id_rota>/delete/", RotaDeleteView.as_view()),
    path("api/averiguacao-semanal/",AveriguacaoEstatisticasSemanaApiView.as_view(),name='AveriguacaoLIstSemanal'),
    path("api/averiguacao-list/",AveriguacaoListApiView.as_view(),name='AveriguacaoList'),
    path('api/averiguacao/<int:id>/', AveriguacaoDetailApiView.as_view(), name='averiguacao-detail'),
    path("api/create-averiguacao/",AveriguacaoCreateApiView.as_view(),name="CreateAveriguacao")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)