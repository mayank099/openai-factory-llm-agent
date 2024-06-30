tools = [
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "This function is used for cancelling any order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The unique identifier of the order to be cancelled"
                    },
                    "reason": {
                        "type": "string",
                        "description": "The reason for order cancellation (optional)"
                    }
                },
                "required": ["order_id"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_cart",
            "description": "Add items to the shopping cart",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "The unique identifier of the item to add to the cart"
                    },
                    "quantity": {
                        "type": "number",
                        "description": "The quantity of the item to add (default is 1)"
                    }
                },
                "required": ["item_id"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search for products based on keywords or filters",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query or keywords"
                    },
                    "filters": {
                        "type": "object",
                        "description": "Additional filters such as price range, brand, or category (optional)"
                    }
                },
                "required": ["query"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "view_product_details",
            "description": "Get detailed information about a specific product",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The unique identifier of the product"
                    }
                },
                "required": ["product_id"]
            },
        }
    },
]
