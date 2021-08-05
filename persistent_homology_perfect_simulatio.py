#!/usr/bin/env python3

from perfect_simulation import *
import gudhi
from matplotlib import pyplot as plt


intervalo = [-100,100]
diagrama_persistencia_dim0 = [ ]
for a in range(50):
    MinhaSimulacao = PerfectSimulation( janela = intervalo,\
                                        taxa_poisson= 0.9,\
                                        suporte_dist_pi = 5.0,\
                                        chamadas_simultaneas = 5.0 )

    MinhaSimulacao.Simulacao()

    nuvemDados = MinhaSimulacao.GermesProcessoPontualEmUmIntervalo( intervalo )

    filtracao = gudhi.AlphaComplex( nuvemDados )

    st = filtracao.create_simplex_tree()

    # Agora podemos calcular o diagrama de persistencia
    diagrama_persistencia = st.persistence( homology_coeff_field = 2 )

    #diagrama_persistencia_dim0 = diagrama_persistencia_dim0.append(  [ x[1][1] for x in diagrama_persistencia if x[1][1] != np.inf ] )
    diagrama_persistencia_dim0  += [ x[1][1] for x in diagrama_persistencia if x[1][1] != np.inf ]
#
# E gerar seu grafico
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

gudhi.plot_persistence_diagram( diagrama_persistencia, legend = True, axes=axes[0])

#estimativa_lambda = len( diagrama_persistencia_dim0 ) /  sum( diagrama_persistencia_dim0 )

#x1 = np.arange( 0, max( diagrama_persistencia_dim0 ), 0.1 )
#y1 = estimativa_lambda * np.exp( -estimativa_lambda * x1 )
#axes[1]= plt.plot(x1,y1, 'k')

axes[1] = plt.hist( diagrama_persistencia_dim0, density=True )
#title = "Parametro exponecial, lambda = {:.3f}".format( estimativa_lambda )
axes[1]  = plt.title( "Histograma do diagrama de persistencia de dim=0" )

#plt.show()
plt.savefig('diagrama_persistencia_hist.png')

#axes[1].show()
##plt.savefig('histograma_diagrama_persistencia')
#
