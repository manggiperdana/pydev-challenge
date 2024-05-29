# PythonDevTrial

## Spesification
- Python version : Python 3.12.3
- Pip version : pip 24.0
- use virtualenv
- Database Using SQLite

## Architecture
 - api (for router with endpoint versioning)
 - core (for config and utility)
 - db (for database session)
 - models (for table orm)
 - repositories (for logical processes)
 - schemas (for schematic request and response data transfer object)
 - services (for business based processes)

## Usage
Linux / MacOs command
1. Make sure you have .env file for generated test.db you can copy from .env.sample, it's have database url config, api endpoint versioning, and debug status.

```
cp .env.sample .env
```
2. Run requirement.txt to download package need for this project

```
pip install -r requirements.txt
```
3. Run the locally project with

```
uvicorn app.main:app --reload
```

4. View documentation utl page at to check endpoint:
```
http://localhost:8000/docs
```
## Brief & Requirements

In this project you will build a REST API for an information system and you will work only for 2 modules:

- Order
- Inventory

The main plugin we use to build the API is FastAPI, you are required to build with this platform. For the database you can use any database (SQLite, MySQL, Postgre, etc) preferably MySQL / SQLite.

## Scope

### Order

#### Properties

- DocumentNo
- Customer
- Order details

  - Product
  - Qty
  - Qty Sent
  - Price
  - Subtotal
  - DiscountPerItem
  - AfterDiscount
  - Tax
  - AfterTax

- Description
- Status [**Pending** | **Sent** | **Paid** | **Closed**]
- Subtotal
- Discount
- AfterDiscount
- Tax
- AfterTax
- LastModifiedAt
- SentAt
- CreateAt
- DeleteAt

#### Business Logic

- When the order is still pending, we can change everything.
- But after order is paid, we can edit only for some properties like description of the order.
- Order status are automatically change to **Sent** when all of the order items are sent (QtySent = Qty), vice versa, it automatically back to **Pending** if the user update the sent items (QtySent < Qty)

#### API End Points

| METHOD | END POINTS                    | Params / Brief                                                                                                               |
| :----- | :---------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| GET    | /order                        | $q = search string in customer name, description, document no; $limit; $page, $orderBy = column name; $order = ASC / DESC    |
| GET    | /order/details                | $productId = filter by product; $customerId = filter by customer; $limit; $page, $orderBy = column name; $order = ASC / DESC |
| POST   | /order                        | $OrderObject                                                                                                                 |
| POST   | /order/{orderId}/mark-as-paid | Will mark this order as paid                                                                                                 |
| PUT    | /order/{orderId}              | $OrderObject                                                                                                                 |
| DELETE | /order/{orderId}              |

### Inventory

#### Properties

- OrderDetail (relation to order detail)
- Order (relation to order)
- QtyOut
- AmountOut

#### Business Logic

- Inventory will subscribe to order's events. Everytime order changed or deleted the inventory will modifed with the same events. So you will not have any API calls for create or update inventory.
- Inventory added when the order is sent (partiall or full), updated when the order sent is updated, and removed when the order detail is removed

#### End Points

| METHOD | END POINTS             | Params                                                                                                               |
| :----- | :--------------------- | :------------------------------------------------------------------------------------------------------------------- |
| GET    | /inventory             | $limit; $page, $orderBy = column name; $order = ASC / DESC, $orderId = filter by order, $customerId = filter by cust |
| GET    | /inventory/{productId} | $limit; $page, $orderBy = column name; $order = ASC / DESC, $orderId = filter by order, $customerId = filter by cust |
