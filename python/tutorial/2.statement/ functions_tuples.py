# Returning Tuples for Unpacking
stock_prices = [('AAPL',200),('GOOG',300),('MSFT',400)]
for stock, price in stock_prices:
    print(f"Stock: {stock}, Price: {price}")


# functions often return tuples, to easily return multiple results for later use.
work_hours = [('Abby',100),('Billy',400),('Cassie',800)]
def employee_work_hours(work_hours):
    total_hours = 0
    for employee, hours in work_hours:
        total_hours += hours
    return total_hours, len(work_hours)

total, count = employee_work_hours(work_hours)
print(f"Total work hours: {total}, Number of employees: {count}")
