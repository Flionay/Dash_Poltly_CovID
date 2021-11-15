import dash 
from views.china import layout_china
# 应用配置
from server import app
app.layout = layout_china
server = app.server
if __name__=='__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8983)