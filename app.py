import falcon
from services.trade import Home

# Enable a simple CORS policy for all responses
app = falcon.App(cors_enable=True)


app.add_route('/home', Home())
