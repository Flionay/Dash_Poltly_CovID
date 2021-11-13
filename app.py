import dash 
from views.china import layout_china
# 应用配置
from server import app

app.layout = layout_china
if __name__=='__main__':
    app.run_server(debug=True,port=9999)