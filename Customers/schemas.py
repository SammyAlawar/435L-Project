from flask_marshmallow import Marshmallow

ma = Marshmallow()
class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("id", "full_name", "username", "age", "address", "gender", "marital_status", "wallet")
