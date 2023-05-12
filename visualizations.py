
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def plot_bollinger_bands(df, title="Bollinger Bands"):
    """
    Grafica las Bandas de Bollinger para un DataFrame dado.
    Df: DataFrame con columnas 'close', 'bb_bbh', 'bb_bbm', y 'bb_bbl'.
    title: Título para el gráfico (por defecto 'Bollinger Bands').
    """

    # Crear la figura y agregar los trazos.
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(y=df.close, mode='lines', name='close price', line=dict(color='#FF5733', width=2), connectgaps=True))
    fig.add_trace(go.Scatter(y=df.bb_bbh, mode='lines', name='high bollinger', line=dict(color='#1B68A1', width=2),
                             connectgaps=True))
    fig.add_trace(go.Scatter(y=df.bb_bbm, mode='lines', name='middle bollinger', line=dict(color='#8A8B94', width=2),
                             connectgaps=True))
    fig.add_trace(go.Scatter(y=df.bb_bbl, mode='lines', name='low bollinger', line=dict(color='#0190B6', width=2),
                             connectgaps=True, ))

    # Actualizar el diseño del gráfico.
    fig.update_layout(title=title, yaxis_title='Dollars', xaxis_title='Time')

    # Agregar una anotación.
    fig.add_annotation(text=("Figure. Evolución de las bandas de Bollinger"), showarrow=False, x=0, y=-0.15,
                       xref='paper', yref='paper', xanchor='left', yanchor='bottom', xshift=-1, yshift=-5,
                       font=dict(size=10, color="grey"), align="left")

    # Mostrar el gráfico.
    fig.show()

    # Devolver la figura.
    return


def plot_macd_indicator(df, title="MACD Indicator"):
    """
    Grafica el indicador MACD para un DataFrame dado.
    df: DataFrame con columnas 'macd', 'macd_signal', 'macd_hist', y 'close'.
    title: Título para el gráfico (por defecto 'MACD Indicator').
    """

    # Crear la figura y agregar los trazos.
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], shared_xaxes=True)
    fig.add_trace(
        go.Scatter(y=df.macd, mode='lines', name='MACD', line=dict(color='#FF5733', width=2), connectgaps=True), row=1,
        col=1, secondary_y=False)
    fig.add_trace(go.Scatter(y=df.macd_signal, mode='lines', name='Signal', line=dict(color='#1B68A1', width=2),
                             connectgaps=True), row=1, col=1, secondary_y=False)
    fig.add_trace(go.Bar(y=4 * df.macd_hist, name='Hist'), row=1, col=1, secondary_y=False)

    fig.add_trace(
        go.Scatter(y=df.close, mode='lines', name='Close price', line=dict(color='#FF5733', width=2), connectgaps=True),
        row=2, col=1, secondary_y=True)

    # Actualizar el diseño del gráfico.
    fig.update_layout(title=title, xaxis_title='Time')
    fig.update_yaxes(title_text='MACD', row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text='Dollars', row=2, col=1, secondary_y=True)

    # Agregar una anotación.
    fig.add_annotation(text=("Figure. Evolución del indicador MACD. Nota: el histograma fue amplificado."),
                       showarrow=False, x=0, y=-0.15,
                       xref='paper', yref='paper', xanchor='left', yanchor='bottom', xshift=-1, yshift=-5,
                       font=dict(size=10, color="grey"), align="left")

    # Mostrar el gráfico.
    fig.show()

    # Devolver la figura.
    return


def graph_oscillator(df, titulo):
    """
    Oscilator indicator Graph
    """

    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3])
    fig.add_trace(go.Scatter(y=df.stochastic, mode='lines', name='stochastic', line=dict(color='#8A8B94', width=2),
                             connectgaps=True), row=1, col=1)
    fig.add_trace(go.Scatter(y=[80] * len(df), mode='lines', name='Upper Bound', line=dict(color='#1B68A1', width=2),
                             connectgaps=True), row=1, col=1)
    fig.add_trace(go.Scatter(y=[20] * len(df), mode='lines', name='Lowe Bound', line=dict(color='#FFDF2D', width=2),
                             connectgaps=True), row=1, col=1)

    fig.add_trace(
        go.Scatter(y=df.close, mode='lines', name='close price', line=dict(color='#FF5733', width=2), connectgaps=True),
        row=2, col=1)
    fig.update_layout(title=titulo, xaxis_title='Time')

    fig.add_annotation(text=("Figure. Evolution of the stochastic oscillator"), showarrow=False, x=0, y=-0.15,
                       xref='paper', yref='paper', xanchor='left', yanchor='bottom', xshift=-1, yshift=-5,
                       font=dict(size=10, color="grey"), align="left", )
    fig.show()

    return

def graph_capital(train, test,titulo):

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=train, mode='lines',name='portafolio de entrenamiento',line=dict(color='#FF5733', width=2),connectgaps=True))
    fig.add_trace(go.Scatter(y=test, mode='lines',name='portafolio de testeo',line=dict(color='#1B68A1', width=2),connectgaps=True))
    fig.update_layout(title = titulo,yaxis_title='Dolars',xaxis_title='Time')
    fig.add_annotation(text = ("Figure. Evolución del capital"), showarrow=False, x = 0, y = -0.15,
           xref='paper', yref='paper' , xanchor='left', yanchor='bottom', xshift=-1, yshift=-5, font=dict(size=10, color="grey"), align="left",)
    fig.show()
    return