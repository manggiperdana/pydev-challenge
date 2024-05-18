# PythonDevTrial

## Scope & Requirements

In this project you will build a REST API for an information system and let's say you will work only for 2 modules:

- Order
- Inventory

The main plugin we use to build the API is FastAPI, you are required to build under this platform. For the database you can use any database (SQLite, MySQL, Postgre, etc).

### Order

In order, you will have properties for example:

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
- Status [**Pending** | **Sent** | **Closed**]
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
- But after all the items are sent, we can edit only for some properties like description of the order.
- Order status are automatically change to **Sent** when all of the order items are sent (QtySent = Qty), vice versa, it automatically back to **Pending** if the user update the sent items (QtySent < Qty)

#### API End Points

| METHOD | END POINTS       | Params                                                                                                                    |
| :----- | :--------------- | :------------------------------------------------------------------------------------------------------------------------ |
| GET    | /order           | $q = search string in customer name, description, document no; $limit; $page, $orderBy = column name; $order = ASC / DESC |
| POST   | /order           | $OrderObject                                                                                                              |
| PUT    | /order/{orderId} | $OrderObject                                                                                                              |
| DELETE | /order/{orderId} |                                                                                                                           |

### Inventory

In inventory, you will have properties like:

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
