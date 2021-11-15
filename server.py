import dash
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
app = dash.Dash(__name__, external_stylesheets=[BS], title="疫情监控大屏")
app.config.suppress_callback_exceptions = True
