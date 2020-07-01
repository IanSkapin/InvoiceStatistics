
# InvoiceStats
Invoices are agreements to transfer money between companies. We need a python class to aggregate and
gather basic stats on the invoices we process. Your task is to write this class.
Write a python class, "InvoiceStats", along with suitable tests, which supports the following methods:
- add_invoices - add a list of invoices, in dollars and cents
- add_invoice - add a single invoice, in dollars and cents.
- clear - remove all stored invoice data.
- get_median - find the median value of the added invoices, to
the nearest cent. Half a cent should round down
- get_mean - find the mean value of the invoices, to the nearest cent. Half a cent should round down.

Constraints:
- Valid invoice values v are 0 < v < $200,000,000.00 and must be a whole number of dollars and cents.
- Adding non valid invoice value(s) should raise an exception.
- You may decide what data type(s) to use to best represent the invoice amounts.
- Maximum number of invoices is 20,000,000
- Assume the machine the code is running on will not crash, so no need to persist data.
- You may use (non standard) third party libraries. If so, please include details of them, including why you used
them.
- Your code will be judged on scalability, clarity, readability, accuracy, test coverage, performance and
robustness.


## Implementation
My understanding of the intended normal usage for the InvoiceStats class is that of it running in the background and 
accumulating invoices over time as they happen in the system without human interaction. The get_median and get_mean on 
the other hand I imagine would be called as direct consequence of human interaction. Maybe someone is generating a 
report. From these scenario I formed the following assumptions.   

Assumptions:
 - get_median and get_mean should execute in constant time
 - as invoices are added over time the add_invoices and add_invoice may carry compute cost
 
Possible further optimizations:
 - the check_input method is relatively time consuming, if the invoice input could be changed to (dollars: int, cents: 
 int) the performance could be improved by up to ~ 1/3, it would also allow for decimal object to be used and scale_up 
 to be removed 
 - the FastMedian.insert_list method could possibly be improved for large additions by using heapify and heap merge 
 
Requirements:
 - implemented in python 3.8.1
 - please see the requirements.txt for the list of libraries versions in the virtual environment used
 
Unittests:

    cd InvoiceStatistics
    python -m pytest .

Example:

    cd InvoiceStatistics
    python performance.py 