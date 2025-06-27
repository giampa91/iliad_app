Order Management - Setup and Data Insertion Guide
Prerequisites

Docker and Docker Compose installed on your machine.
Python 3.8+ installed and requests package.

For running the application:

Step 1: Start the backend with Docker Compose
Run the following command to start the backend API and database containers:

    docker-compose up -d

This will launch your Django API on http://localhost:8000.

You can access the frontend at: http://localhost:3000

Step 2: Install Python and dependencies for the data insertion script

Make sure Python 3.8 or newer is installed, then install the required package requests:

    pip install requests

Step 3: Run the data insertion script

The script insert_orders.py will create 1000 random orders with products by calling the running API.
Run it with:

    python create_random_orders.py

Notes: Ensure the backend API is running before executing the script.

To stop and remove the Docker containers, run:

    docker-compose down

For production use should be use .env files.

Coverage report > 90%

    coverage report             
    Name                                                    Stmts   Miss  Cover
    ---------------------------------------------------------------------------
    __init__.py                                                 0      0   100%
    backend\__init__.py                                         0      0   100%
    backend\asgi.py                                             4      4     0%
    backend\manage.py                                          11     11     0%
    backend\settings.py                                        22      4    82%
    backend\urls.py                                             3      0   100%
    backend\wsgi.py                                             4      4     0%
    manage.py                                                  11      2    82%
    orders\__init__.py                                          0      0   100%
    orders\admin.py                                            12      0   100%
    orders\apps.py                                              4      0   100%
    orders\exceptions.py                                        2      2     0%
    orders\migrations\0001_initial.py                           7      0   100%
    orders\migrations\__init__.py                               0      0   100%
    orders\models\order.py                                      9      1    89%
    orders\models\product.py                                    7      1    86%
    orders\pagination.py                                       23      6    74%
    orders\serializers\order_create_serializer.py              10      0   100%
    orders\serializers\order_serializer.py                      9      0   100%
    orders\serializers\order_update_serializer.py              15      3    80%
    orders\serializers\product_serializer.py                    7      0   100%
    orders\serializers\simple_product_input_serializer.py       8      0   100%
    orders\services\order_service.py                           69      8    88%
    orders\services\product_service.py                         24      0   100%
    orders\tests\__init__.py                                    0      0   100%
    orders\tests\factories.py                                  14      0   100%
    orders\tests\models\__init__.py                             0      0   100%
    orders\tests\models\test_order_factory.py                   9      0   100%
    orders\tests\models\test_product_factory.py                 9      0   100%
    orders\tests\serializers\__init__.py                        0      0   100%
    orders\tests\serializers\test_order_serializers.py         45      0   100%
    orders\tests\serializers\test_product_serializers.py       24      0   100%
    orders\tests\services\__init__.py                           0      0   100%
    orders\tests\services\test_order_service.py                52      0   100%
    orders\tests\services\test_product_service.py              42      0   100%
    orders\tests\views\__init__.py                              0      0   100%
    orders\tests\views\test_order_view.py                      63      0   100%
    orders\tests\views\test_product_view.py                    27      0   100%
    orders\urls.py                                              8      0   100%
    orders\views\order_view.py                                 46      3    93%
    orders\views\product_view.py                               17      0   100%
    ---------------------------------------------------------------------------
    TOTAL                                                     617     49    92%
