from django.db import models

# Create your models here.

class SocialMidiaUse(models.Model):
    class KDUseSocialMedia(models.IntegerChoices):
        kdMenosdeUmaHoraPorDia = 0, "Menos de Uma Hora por Dia"
        kdUmaATresHorasPorDia = 1, "Uma a Tres Horas por Dia"
        kdTresACincoHorasPorDia = 2, "Tres a Cinco Horas por Dia"
        kdMaisDeCincoHorasPorDia = 3, "Mais de Cinco Horas por Dia"

    class KDComparisonSocialMedia(models.IntegerChoices):
        kdSintoInspiradoFicoFelizPeloSucessoDosOutros = 0, "Sinto inspirado e fico feliz pelo sucesso dos outros"
        kdNormalmenteMeSintoIndiferenteEApenasObservo = 1, "Normalmente me sinto indiferente e apenas observo"
        kdAsVezesMeSintoIncomodadoMasTentoNaoMeComparar = 2, "As vezes me sinto incomodado, mas tento não me comparar"
        kdFrequentementeMeComparoMeSintoInferior = 3, "Frequentemente me comparo me sinto inferior"

    class KDSelfKnowledgeAboutSocialMediaUse(models.IntegerChoices):
        kdNãoSintoQuePassoTempoDemaisNasRedes = 0, "Não sinto que passo tempo demais nas redes"
        kdAsVezesMePreocupoComIsso = 1, "As vezes me preocupo com isso"
        kdFrequentementeMasTentoControlar = 2, "Frequentemente, mas tento controlar"
        kdSempreSintoQueEstouPassandoMuitoTempoOnline = 3, "Sempre sinto que estou passando muito tempo online"

    class KDCheckSocialNetworksWhenOffline(models.IntegerChoices):
        kdNãoSintoVontadeDeChecarAsRedesSociaisQuandoEstouOffiline = 0, "Não sinto vontade de checar as redes sociais quando estou offiline"
        kdRaramentePensoEmChecarQuandoEstouOffiline = 1, "Raramente penso em checar quando estou offiline"
        kdAsVezesSintoVontadeDeChecarMasConsigoMeControlar = 2, "As vezes me sinto vontade de checar, mas consigo me controlar"
        kdSimSintoUmaNecessidadeConstanteDeVerificar = 3, "Sim, sinto uma necessidade constante de verificar"

    class KDWouldPreferToUseLessSocialMedia(models.IntegerChoices):
        kdNãoEstouSatisfeitoComOTempoQuePassoNasRedes = 0, "Não, estou satisfeito com o tempo que passo nas redes"
        kdTalvezMasNãoSeiSeConseguiria = 1, "Talvez, mas não sei se conseguiria"
        kdSimMasAindaNãoTomeiNenhumaAção  = 2, "Sim, mas ainda não tomei nenhuma ação"
        kdSimDefinitivamenteMasTenhoDificuldadeEmReduzir = 3, "Sim, definitivamente, mas tenho dificuldade em reduzir"

    class KDResult(models.IntegerChoices):
        kdNãoUsaMuito = 0, "Usa muito pouco"
        kdUsoModerado = 1, "Uso moderado"
        kdUsaMuito  = 2, "Usa muito"
        kdPreocupante = 3, "Preocupante"

    id = models.AutoField(primary_key=True)
    use_of_social_midia = models.IntegerField(verbose_name="Tempo em Midias Sociais",
        choices=KDUseSocialMedia.choices,
        blank=False,
        null=False,)
    social_media_comparison = models.IntegerField(verbose_name="Comparação em Midias Sociais",
        choices=KDComparisonSocialMedia.choices,
        blank=False,
        null=False,)
    selfknowledge_about_social_media_use = models.IntegerField(verbose_name="Autoconhecimento sobre uso de social midia",
        choices=KDSelfKnowledgeAboutSocialMediaUse.choices,
        blank=False,
        null=False,)
    check_social_networks_when_offline = models.IntegerField(verbose_name="Checar redes sociais quando offline",
        choices=KDCheckSocialNetworksWhenOffline.choices,
        blank=False,
        null=False,)
    would_prefer_to_use_less_social_media = models.IntegerField(verbose_name="Preferiria usar menos midias sociais",
        choices=KDWouldPreferToUseLessSocialMedia.choices,
        blank=False,
        null=False,)
    result = models.IntegerField(verbose_name="Resultado",
        choices=KDResult.choices,
        blank=True,
        null=True,)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    
    def __str__(self):
        return f"{self.id} - {self.result}"

    class Meta:
        verbose_name = "Uso de Midias Sociais"
        verbose_name_plural = "Uso de Midias Sociais"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        result_value = self.use_of_social_midia + self.social_media_comparison + self.selfknowledge_about_social_media_use + self.check_social_networks_when_offline + self.would_prefer_to_use_less_social_media
        if result_value <= 5:
            self.result = 0
        if  result_value > 5 and result_value <= 8:
            self.result = 1
        if  result_value > 8 and result_value <= 10:
            self.result = 2
        if  result_value > 10:
            self.result = 3
        super(SocialMidiaUse, self).save(*args, **kwargs)