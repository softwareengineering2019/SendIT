"""
This module defines api end point to enable an admin to update the order status

"""
from flask import jsonify
from flask import request
from flask.views import MethodView
from api.model.orders import Orders
from api.token.token_required import token_required

class UserSpecificOrders(MethodView):
    """Class to define an endpoint to get a specific user order"""
    # orders_object = OrdersApi()
    # orders_list = orders_object.orders
    @token_required
    def get(self, current_user):
        """function to get a single order for a user"""
        user_type = current_user[0][7]
        specific_user_id = current_user[0][0]
        if user_type == 'user':
            try:
                user_id = int(specific_user_id)
            except:
                return jsonify({'message':'Invalid User Id'}), 400
            return Orders.get_specific_user_orders(self,user_id)
        return jsonify({'message':'Cannot Perform That Function!'}), 404

    @token_required
    def put(self,current_user, parcel_id):
        """function to enable a user to change the destination address of a specific order"""
        user_type = current_user[0][7]
        user_id = current_user[0][0]
        #check if user is admin
        if user_type == 'user':
            try:
                parcel_id = int(parcel_id)
            except:
                return jsonify({'message':'Invalid Parcel Id'}), 400
            return Orders.update_order_destination(self, parcel_id, 
            request.json['parcel_destination_address'], user_id)
        return jsonify({'message':'Cannot Perform That Function!'}), 404

    
