#!/usr/bin/env python3

import numpy as np
from operator import itemgetter

# --------------------------------------------------------------
###### A classe dos retangulos R = (x0, x1) \times (t0, t1)  ###
# --------------------------------------------------------------
class Retangulo:

    ###### Atributos
    ###### ---------
    def __init__(self, x0, x1, t0, t1):
        """ Atributos
        --------------
        Definindo os atributos do objeto
        instanciado
            R1 = Retangulo (x0, x1, t0, t1).
        Aqui, os atributos
            x0, x1, t0, t1
        definem a dimensao do retangulo R1, isto eh,
        matematematicamente dizendo,
        o retangulo R1 eh o produto cartesiano
            R1 = (x0, x1) \times (t0, t1)
        com
              x0 <= x1  e  t1 <= t0 <= 0.
        
          0-------x0-----------x1--------->
          |        |            |
          |        |            |
          |        |            |
          t0------ **************
          |        **************
          |        ******R1******
          |        **************
          |        **************
          |        **************
          t1-------**************
          |
          |
          V
        """ 
        self.x0 = x0
        self.x1 = x1
        self.t0 = t0
        self.t1 = t1


    ###### Metodos
    ###### ---------

    def Nascimento(self):
        # retornaremos t1 porque no algoritmo estamos olhando para
        # o tempo referente ao passado e 0 >= t0 >= t1.
        return self.t1


    def TempoDeVida(self):
        # retornaremos o intervalo [t1, t0] referente ao tempo de vida do
        # retangulo
        return [self.t1, self.t0]


    def Base(self):
        # retornaremos o intervalo representando o comprimento da ligacao,
        # isto eh, [x0, x1]
        return [self.x0, self. x1]


    def Area (self):
       """
       Calculando a area do retangulo
       """ 
       return (self.x1 - self.x0) * (self.t0 - self.t1)


    def ChecaInterseccao(self, r ):
        """
        Este metodo recebe como parametro um objeto da classe Retangulo
        e retorna o valor True se a interseccao
            self \cap r \neq \emptyset
        e retorna o valor False caso contrario
        """

        if ( self.x0 < r.x0 and r.x0 < self.x1 ) or ( self.x0 < r.x1 and r.x1 < self.x1 ):
            if ( self.t1 < r.t0 and r.t0 < self.t0 ) or ( self.t1 < r.t0 and r.t0 < self.t0 ):
                return True
            else:
                return False
        else:
            return False


    def SimulaProcessoPoisson (self, taxa_lambda):
        """
        Este metodo implementa a simulacao de um
        Processo de Poisson de taxa lambda em um objeto
        da classe Retangulo e retorna um numpy.array
        de pontos:
          numpy.array ( [ [x0, t0],
                            ...,
                          [xN, tN) ] )
        """

        N = np.random.poisson ( taxa_lambda * self.Area() )

        amostra_eixo_x = np.random.uniform (self.x0, self.x1, (N,1))
        amostra_eixo_y = np.random.uniform (self.t1, self.t0, (N,1))

        return np.concatenate ( (amostra_eixo_x, amostra_eixo_y), axis = 1 )


    def DiferencaEntreRetangulos (self, Retangulo_r):
        """
        Dado os objetos: Retangulo r1, r2.
        Chamando o metodo DiferencaEntreRetangulos como abaixo
            r1.DiferencaEntreRetangulos( r2 )
        ira calcular a diferenca
            r1 \ r2
        entre conjuntos e retornara uma lista
        de Retangulos disjuntos
           [ Rec1, Rec2, ..., RecN ]
        tal que
           r1 = r2 U Rec1 U Rec2 U ... U RecN,
        com U acima equivalendo a uniao de conjuntos.
        """
        if (Retangulo_r.Area() == 0) or ( self.ChecaInterseccao( Retangulo_r ) == False ):
            return []

        # Esta parte eh chatinha
        # Primeiro vejamos em quais parte do eixo x
        # do retangulo self o retangulo Retangulo_r intersepta
        # com seus vertices.
        # Por exemplo, desta analise teremos os possiveis
        # resultados
        # [ self.x0, self.x1 ]; sem interseccao no eixo x
        #       self.x0 [------------] self.x1
        #
        # [ self.x0, Retangulo_r.x0, self.x1 ]; uma interseccao  no eixo x
        #       self.x0 [----x--------] self.x1
        #
        # [ self.x0, Retangulo_r.x1, self.x1 ]; uma interseccao  no eixo x
        #       self.x0 [--------x----] self.x1
        # [ self.x0, Retangulo_r.x0, Retangulo_r.x1, self.x1 ]; duas interseccoes
        #                                   no eixo x
        #       self.x0 [---x-----x----] self.x1
        interseccao_eixo_x = [self.x0]
        if self.x0 < Retangulo_r.x0 and Retangulo_r.x0 < self.x1:
            interseccao_eixo_x.append (Retangulo_r.x0)
        if self.x0 < Retangulo_r.x1 and Retangulo_r.x1 < self.x1:
            interseccao_eixo_x.append (Retangulo_r.x1)

        interseccao_eixo_x.append (self.x1)

        # Agora o mesmo para o eixo t
        interseccao_eixo_t = [self.t0]
        if self.t1 < Retangulo_r.t0 and Retangulo_r.t0 < self.t0 :
            interseccao_eixo_t.append (Retangulo_r.t0)
        if self.t1 < Retangulo_r.t1 and Retangulo_r.t1 < self.t0 :
            interseccao_eixo_t.append (Retangulo_r.t1)

        interseccao_eixo_t.append (self.t1)

        # Com tudo isto temos os intervalos decompostos
        # como no exemplo abaixo, onde o retangulo
        # Retangulo_r esta complemtamente contido no retangulo
        # self.
        #
        #  [-----x----------x-------]
        #  |     |           |      |
        #  |     |           |      |
        #  |     |           |      |
        #  x-----|-----------|------|
        #  |     |           |      |
        #  |     |Retangulo_r|      |
        #  |     |           |      |
        #  x-----|-----------|------|
        #  |     |           |      |
        #  |     |           |      |
        #  |     |           |      |
        #  --------------------------
        #
        # Como exemplificado no exemplo acima,
        # vamos agora construir os retangulos
        # que decompoes o retangulo self excluindo
        # a interseccao com o retangulo Retangulo_r

        aux_eixo_x = []
        for i in range ( len(interseccao_eixo_x) - 1):
            aux_eixo_x.append( [interseccao_eixo_x[i], interseccao_eixo_x[i+1]] )

        aux_eixo_t = []
        for i in range ( len(interseccao_eixo_t) - 1):
            aux_eixo_t.append( [interseccao_eixo_t[i], interseccao_eixo_t[i+1]] )

        # Agora vamos criar todos retangulos possiveis
        # e checar se estes retangulos nao tem interseccao
        # com Retangulo_r
        retangulos_disjuntos = []
        for x in aux_eixo_x :
            for t in aux_eixo_t:
                # checando se o retangulo Retangulo(x[0], x[1], t[0], t[1])
                # nao tem interseccao com o Retangulo_r.
                # Para isto, basta analisar se o ponto medio deste rentangulo
                # pertence em Retangulo_r.
                ponto_medio = [ (x[0] + x[1])/2.0, (t[0] + t[1])/2.0 ]
                if not (Retangulo_r.x0 <= ponto_medio[0] and ponto_medio[0] <= Retangulo_r.x1 and Retangulo_r.t1 <= ponto_medio[1] and ponto_medio[1] <= Retangulo_r.t0):
                    retangulos_disjuntos.append( Retangulo(x[0], x[1], t[0], t[1]) )

        return retangulos_disjuntos


    def InterseccaoEntreRetangulos (self, Retangulo_r):
        """
        Este metodo retorna um objeto da classe Retangulo representando
        a interseccao entre o retangulo self e o Retangulo_r

        Note que a implementacao deste metodo eh nada mais que
        o metodo InterseccaoEntreRetangulos acima com apneas uma modificacao.
        Portanto, pelo codigo o codigo nao sera muito comentado
        """
        interseccao_eixo_x = [self.x0]
        if self.x0 < Retangulo_r.x0 and Retangulo_r.x0 < self.x1:
            interseccao_eixo_x.append (Retangulo_r.x0)
        if self.x0 < Retangulo_r.x1 and Retangulo_r.x1 < self.x1:
            interseccao_eixo_x.append (Retangulo_r.x1)

        interseccao_eixo_x.append (self.x1)

        interseccao_eixo_t = [self.t0]
        if self.t1 < Retangulo_r.t0 and Retangulo_r.t0 < self.t0 :
            interseccao_eixo_t.append (Retangulo_r.t0)
        if self.t1 < Retangulo_r.t1 and Retangulo_r.t1 < self.t0 :
            interseccao_eixo_t.append (Retangulo_r.t1)

        interseccao_eixo_t.append (self.t1)

        aux_eixo_x = []
        for i in range ( len(interseccao_eixo_x) - 1):
            aux_eixo_x.append( [interseccao_eixo_x[i], interseccao_eixo_x[i+1]] )

        aux_eixo_t = []
        for i in range ( len(interseccao_eixo_t) - 1):
            aux_eixo_t.append( [interseccao_eixo_t[i], interseccao_eixo_t[i+1]] )

        # Agora vamos criar todos retangulos possiveis
        # e checar QUAL retangulo TEM interseccao
        # com Retangulo_r
        # retangulos_disjuntos = []
        for x in aux_eixo_x :
            for t in aux_eixo_t:
                # checando se o retangulo Retangulo(x[0], x[1], t[0], t[1])
                # TEM interseccao com o Retangulo_r.
                # Para isto, basta analisar se o ponto medio deste rentangulo
                # pertence em Retangulo_r.
                ponto_medio = [ (x[0] + x[1])/2.0, (t[0] + t[1])/2.0 ]
                if (Retangulo_r.x0 <= ponto_medio[0] and ponto_medio[0] <= Retangulo_r.x1 and Retangulo_r.t1 <= ponto_medio[1] and ponto_medio[1] <= Retangulo_r.t0):
                    #retangulos_disjuntos.append( Retangulo(x[0], x[1], t[0], t[1]) )
                    return Retangulo(x[0], x[1], t[0], t[1])


    def Copia(self):
        """
        Retorna um retangulo cujos elementos sao uma copia do retangulo self
        """
        return Retangulo( self.x0, self.x1, self.t0, self.t1 )


    def __repr__(self):
        return '<{}: ( {}, {} ) x ( {}, {} )>\n'. format(self.__class__.__name__, self.x0, self.x1, self.t1, self.t0)


# --------------------------------------------------------------
###### A classe que realizara a simulacao perfeita em uma janela
###### \Lambda = [a,b] \subseteq R
# --------------------------------------------------------------
class PerfectSimulation:

    ###### Atributos
    ###### ---------

    def __init__(self, janela, taxa_poisson, suporte_dist_pi, chamadas_simultaneas ):
        """
        Os atributos desta classe sao:
         - janela                 := uma lista [a,b] representando o intervalo o
                                     qual a simulacao perfeita sera realizada.
                                     Aqui, a lista [a,b] representa exatamente este
                                     intervalo.

        - taxa_poisson            := a taxa do processo pontual de Poisson.

        - distribuicao_pi         := distribuicao da variavel aleatoria pi. Por padrao
                                     pi = uniforme. Se quiser muda-la, deve-se implememtar a
                                     a amostragem da nova distribuicao no metodo AmostraDistribuicaoPi(self, size)

        - suporte_dist_pi         := inf { x in R; pi( (0,x) ) = 1 }, onde pi
                                     eh a distribuicao \pi do paper da Nevena Maric.

        - chamadas_simultaneas    := numero de chamadas simultaneas
                                     que o sistema aguenta.

        - cla_ancestrais          := lista cujos elementos sao os retangulos representando
                                     todos os possiveis ancestrais do processo. Isto eh, esta lista
                                     representa a primeira parte do algoritmo (Backward)

        - cla_ancestrais_limpo    := lista cujos elementos sao os retangulos representando
                                     a filtracao do cla dos ancestrais. Isto eh, esta lista
                                     representa a ultima parte do algoritmo (Forward)

        - processo_pontual_inicial:= lista [ [x_0, u0], ..., [xN, uN] ] contendo os pontos da
                                     simulacao inicial do processo pontual "loss network" em
                                              janela \subseteq R.
                                     Aqui os pontos x0, x1, ..., xN vem do PPP( taxa_poisson ) e
                                     u0, u1, ..., uN vem da distribuicao pi.

        - processo_pontual_final  := lista [ [x_0, u0], ..., [xM, uM] ], com M <= N ( N acima), referente
                                     a filtracao do processo_pontual_inicial considerando o
                                     cla de ancestrais final do algoritmo.

        """
        self.janela                   = janela
        self.taxa_poisson             = taxa_poisson
        self.distribuicao_pi          = "uniforme"
        self.suporte_dist_pi          = suporte_dist_pi
        self.chamadas_simultaneas     = chamadas_simultaneas
        self.cla_ancestrais           = []
        self.cla_ancestrais_limpo     = []
        self.processo_pontual_inicial = []
        self.processo_pontual_final   = []



    ###### Metodos
    ###### ---------

    def AmostraDistribuicaoPi(self, size):
        """
        Este metodo retorna um array numpy de tamanho (size,1)
        cujos elementos vem da distribuicao self.distribuicao_pi.
        """
        if self.distribuicao_pi == "uniforme":
            return np.random.uniform (0, self.suporte_dist_pi, (size, 1))
        else:
            return []


    def ConstrucaoClaAncestrais (self):
        """
        Esta rotina eh a implementacao do algoritmo da seccao 4.1
        o qual ao seu final atribui ao atributo self.cla_ancestrais a
        lista de retangulos dos possiveis ancestrais.
        """

        ###### etapa C1.
        ###### ----------
        sL = [ self.janela[0], 0]
        sR = [ self.janela[1], 0]

        N = np.random.poisson ( self.taxa_poisson * (self.janela[1] - self.janela[0] + self.suporte_dist_pi ) )

        amostra_poisson = np.random.uniform ( self.janela[0] - self.suporte_dist_pi, self.janela[1], (N, 1) )

        ###### etapa C2.
        ###### ----------
        amostra_pi = self.AmostraDistribuicaoPi( N )

        for i in range( N ):
            if ( self.janela[0] <= amostra_poisson[i,0] and amostra_poisson[i,0] <= self.janela[1] ) or \
               ( self.janela[0] <= amostra_poisson[i,0] + amostra_pi[i,0] and amostra_poisson[i,0] + amostra_pi[i,0] <= self.janela[1] ):
                (self.processo_pontual_inicial).append( [amostra_poisson[i,0], amostra_poisson[i,0] + amostra_pi[i,0]] )


        ###### etapa C3 e C4.
        ###### --------------

        Delta = []

        for x in self.processo_pontual_inicial:
            amostra_exponencial = (-1) * np.random.exponential(1.0)

            (self.cla_ancestrais).append ( Retangulo ( x[0], x[1], 0.0, amostra_exponencial ) )
            Delta.append ( Retangulo ( x[0] - self.suporte_dist_pi, x[1], 0.0, amostra_exponencial ) )


        ###### etapa C5.
        ###### ----------
        continua_o_loop = True

        if ( self.processo_pontual_inicial == [] ):
            continua_o_loop = False
        else:
            cla_ancestrais_k = (self.cla_ancestrais).copy() # cla de ancestrais de cada iteracao


        while continua_o_loop:
            amostra_processo_poisson = []

            sL[1]  = min ( sL[0], min( [a.x0 - self.suporte_dist_pi for a in cla_ancestrais_k] ) )
            sR[1]  = max ( sR[0], max( [a.x1 for a in cla_ancestrais_k] ) )

            ###### etapa C6.
            ###### ----------

            # tomando a amostra do PPP
            for Retangulo_r in Delta:
                amostra_processo_poisson.append ( Retangulo_r.SimulaProcessoPoisson( self.taxa_poisson ) )

            if sL[0] - sL[1] > 0.0:
                amostra_processo_poisson_aux_sL_tamanho = np.random.poisson ( self.taxa_poisson * ( sL[0] - sL[1] ) )
                amostra_processo_poisson_aux_sL         = np.random.uniform ( sL[1], sL[0], (amostra_processo_poisson_aux_sL_tamanho, 2) )
                amostra_processo_poisson_aux_sL[:,1]    = 0
                amostra_processo_poisson.append ( amostra_processo_poisson_aux_sL )

            if sR[1] - sR[0] > 0.0:
                amostra_processo_poisson_aux_sR_tamanho = np.random.poisson ( self.taxa_poisson * ( sR[1] - sR[0] ) )
                amostra_processo_poisson_aux_sR         = np.random.uniform ( sR[0], sR[1], (amostra_processo_poisson_aux_sR_tamanho, 2) )
                amostra_processo_poisson_aux_sR[:,1]    = 0
                amostra_processo_poisson.append ( amostra_processo_poisson_aux_sR )

            # esta lista amostra_processo_poisson contem o processo de poisson (x_i, t_i)
            # agora vamos criar os retangulos

            ###### etapa C7.
            ###### ----------
            nk = 0
            cla_ancestrais_k = []
            for simulacoes in amostra_processo_poisson:
                nk += simulacoes.shape[0]
                #print(nk)

                if simulacoes.shape[0] != 0:
                    amostra_exponencial = (-1) * np.random.exponential(1.0, (simulacoes.shape[0],1) )
                    amostra_pi          = self.AmostraDistribuicaoPi (simulacoes.shape[0])

                    for i in range( simulacoes.shape[0] ):
                        cla_ancestrais_k.append ( Retangulo( simulacoes[i,0], simulacoes[i, 0] + amostra_pi[i,0],\
                                                             simulacoes[i,1], simulacoes[i,1] + amostra_exponencial[i,0]  ) )

            Delta_k = []
            for Retangulo_r in cla_ancestrais_k:
                Delta_k.append ( Retangulo ( Retangulo_r.x0 - self.suporte_dist_pi, Retangulo_r.x1, 0, Retangulo_r.t1 ) )


            for Retangulo_r in cla_ancestrais_k:
                (self.cla_ancestrais).append ( Retangulo_r )

            if nk == 0:
                continua_o_loop = False
            else:
                Delta_aux = []
                for Retangulo_r in Delta:
                    for Retangulo_rr in Delta_k:
                        Delta_aux = Delta_aux + Retangulo_r.DiferencaEntreRetangulos( Retangulo_rr )
                Delta = Delta_aux
                sL[0] = sL[1]
                sR[0] = sR[1]


    def LimpezaClaAncestrais(self):
        """
        Parte final do algoritmo que ira realizar a limpeza do cla de ancestrais
        gerado pelo metodo acima. gerando cla_ancestrais_limpo. (Forward)
        """

        ##### Variaveis
        cla_ancestrais_indexada_pelo_nascimento = [] # vamos criar a lista de cla de ancestrais
                                                     # [ [t1, r1], ..., [t1, rN] ] onde
                                                     #
                                                     # t1 eh o tempo de nascimento do retangulo r1.
                                                     # O mesmo para os outros retangulos.

        continua_loop = True                         # variavel auxiliar para continuar o loop

        ###############

        if self.cla_ancestrais == []:
            self.cla_ancestrais_limpo = []
            # e nada mais a fazer
        else:
            # devemos ordenar o cla de ancestrais pelo tempo de nascimento
            cla_ancestrais_indexada_pelo_nascimento = [ [r.Nascimento(), r] for r in self.cla_ancestrais ]

            #ordenando
            cla_ancestrais_indexada_pelo_nascimento = sorted( cla_ancestrais_indexada_pelo_nascimento, key = itemgetter(0) )

            while cla_ancestrais_indexada_pelo_nascimento != []:
                Retangulo_r1 = (cla_ancestrais_indexada_pelo_nascimento.pop(0)).pop(1) # ignora o tempo de nascimento

                # adiciona o Retangulo_r1 no cla_ancestrais_limpo
                (self.cla_ancestrais_limpo).append( Retangulo_r1 )

                if self.chamadas_simultaneas == 1:
                    i = 0
                    while i < len( cla_ancestrais_indexada_pelo_nascimento ) :
                    #for i in range ( len( cla_ancestrais_indexada_pelo_nascimento ) ):
                        Retangulo_r2  =  cla_ancestrais_indexada_pelo_nascimento[i][1]

                        if Retangulo_r1.ChecaInterseccao( Retangulo_r2 ):
                            cla_ancestrais_indexada_pelo_nascimento.pop(i)
                            continue

                        i += 1
                else:

                    i = 0
                    while i < len( cla_ancestrais_indexada_pelo_nascimento ) + 1 - self.chamadas_simultaneas :
                    #for i in range ( len( cla_ancestrais_indexada_pelo_nascimento ) + 1 - self.chamadas_simultaneas ):

                        #Retangulo_interseccao_com_r1 = []
                        #numero_interseccao_com_r1    = 1

                        Retangulo_r2  =  cla_ancestrais_indexada_pelo_nascimento[i][1]

                        if Retangulo_r1.ChecaInterseccao( Retangulo_r2 ):

                            numero_interseccao_com_r1    = 2
                            Retangulo_interseccao_com_r1 = Retangulo_r1.InterseccaoEntreRetangulos( Retangulo_r2 )

                            cla_ancestrais_indexada_pelo_nascimento.pop(i)
                            i -= 1 # porque a lista perdeu o elemento i

                            (self.cla_ancestrais_limpo).append( Retangulo_r2 )

                            j = 0
                            while j < len ( cla_ancestrais_indexada_pelo_nascimento ):
                            #for j in range ( len ( cla_ancestrais_indexada_pelo_nascimento ) ):
                                Retangulo_r3 = cla_ancestrais_indexada_pelo_nascimento[j][1]

                                if Retangulo_r3.ChecaInterseccao( Retangulo_interseccao_com_r1 ):
                                    numero_interseccao_com_r1 += 1
                                    if numero_interseccao_com_r1 > self.chamadas_simultaneas:
                                        cla_ancestrais_indexada_pelo_nascimento.pop(j)
                                        j -= 1 # porque a lista perdeu o elemento j

                                j += 1

                        i += 1


    def ConstruindoProcessoPontualFinal(self):
        """
        Finalmente este metodo constroi o processo pontual resultante de uma
        medida invariante resultante da simulacao perfeita.
        """
        for ponto in self.processo_pontual_inicial:
            for Retangulo_r in self.cla_ancestrais_limpo:
                if ponto == Retangulo_r.Base():
                    (self.processo_pontual_final).append( ponto )


    def Simulacao(self):
        """
        Este metodo realiza a simulacao perfeita completa com a construcao
        dos clas ancestrais e com sua limpeza. No final o objeto
        tera em seus atributos todos os valores importantes, tal qual
        seu processo pontual resultante de uma medida invariante,
        armazenado na lista self.processo_pontual_final.
        """
        self.ConstrucaoClaAncestrais()
        self.LimpezaClaAncestrais()
        self.ConstruindoProcessoPontualFinal()


    def GermesProcessoPontualEmUmIntervalo(self, intervalo):
        """
        Para rodar este metodo eh necessario ja ter rodado o metodo Simulacao.
        Apos rodar a simulacao, dado um intervalo representado por uma lista
        [a,b] este metodo ira retornar uma lista de pontos da reta real.
        Tais pontos nada mais sao que o extremo inferior de cada elemento
        da lista self.processo_pontual_final.

        Por exemplo.
        seja Intervalo = [0,5]
        e processo_pontual_final = [ [1,2], [6,7], [4,8] ]
        Entao rodando o metodo GermesProcessoPontualEmUmIntervalo receberemos
        a lista
             return [ [1], [4] ]
        """

        lista = []
        for elemento in self.processo_pontual_final:
            if intervalo[0] <= elemento[0] and elemento[0] <= intervalo[1]:
                lista.append( [elemento[0] ] )

        return lista



