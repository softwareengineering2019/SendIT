import unittest
from flask import json
from api.endpoints.orders import OrdersApi
from api.endpoints.get_specific_user_orders import UserSpecificOrders
from run import app


class SendAPITests(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = app.test_client
        self.order = OrdersApi()
    
    # Test get all orders
    def test_get_all_orders(self):
        result = self.client().get('/api/v1/parcels')
        self.assertEqual(result.status_code, 200)
        
    # Tests for addng a new order #
    def test_if_data_posted_is_in_form_of_json(self):
        """
        Method to check if the data is in json form.
        """
        result = self.client().post(
            '/api/v1/parcels', content_type='application/json',
             data=json.dumps({
                "order_name": "phones",
                "order_status":"pending",
                "parcel_destination_address": "Mpigi",
                "parcel_pickup_address": "Kamwokya",
                "parcel_weight": 6,
                "receivers_contact": "070786543",
                "receivers_names": "mariat candance",
                "senders_contact": "0700978789",
                "senders_names": "Namyalo Agnes",
                "user_id": 4
            }))
        self.assertEqual(result.status_code, 201)
        # Json data
        order_data = json.loads(result.data)
        #testing  whether order was saved with the same attributes and values
        self.assertEqual(order_data["order_name"], "phones") 
        self.assertEqual(order_data["order_status"], "pending")
        self.assertEqual(order_data["parcel_destination_address"], "Mpigi") 
        self.assertEqual(order_data["parcel_pickup_address"], "Kamwokya") 
        self.assertEqual(order_data["parcel_weight"], 6) 
        self.assertEqual(order_data["receivers_contact"], "070786543") 
        self.assertEqual(order_data["receivers_names"], "mariat candance")
        self.assertEqual(order_data["senders_contact"], "0700978789")
        self.assertEqual(order_data["senders_names"], "Namyalo Agnes")
        self.assertEqual(order_data["user_id"], 4)

    # Tests for updating order status 
    def test_update_specific_order(self):
        """
        Method to update an order status.
        """
        result = self.client().put('/api/v1/parcels/1/cancel', content_type='application/json',
                            data=json.dumps(
                                {"order_status":"Delivered"}
                                ))
        self.assertEqual(result.status_code, 200)
        #fetch updated order to verify whether the order_status has changed to Delivered
        check_updated_order = self.client().get('/api/v1/parcels/1')
        self.assertEqual(check_updated_order.status_code, 200)
        json_data = json.loads(check_updated_order.data)
        #order_status value should now be Accepted
        assert json_data['order']['order_status'] == "Delivered"

    def test_get_specific_order(self):
        result = self.client().get('/api/v1/parcels/1')
        self.assertEqual(result.status_code, 200)

    def test_if_value_order_is_not_string(self):
        with self.assertRaises(ValueError):self.order.get("one")