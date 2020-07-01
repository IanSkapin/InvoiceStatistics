from median import FastMedian


class InvoiceStats(FastMedian):
    """Internally stored invoices multiplied by 100 and stored as integers."""
    def __init__(self):
        self.mean = 0
        self.mean_weight = 0
        super().__init__()

    @staticmethod
    def check_input(values: list):
        """Check invoice validity

        Args:
            values(list): list of float invoice values to be validated

        Raises: ValueError in case invoice is out of bounds 0 < invoice < 20M and if the invoice uses fraction of a cent

        """
        for idx in range(len(values)):
            if values[idx] != round(values[idx], ndigits=2):
                raise ValueError("Invalid invoice value. 1 cent is the smallest acceptable unit.")
            if not 0 < values[idx] < 200_000_000.00:
                raise ValueError(
                    "Invalid invoice value. Please make sure the value is positive and smaller than 20,000,000.00")

    @staticmethod
    def scale_up(value: (float, int)):
        """Convert valid float of dollars and cents to integer where the hundreds represent dollars and the rest
        represent cents.

        Args:
            value(flat,int): validated invoice

        Returns(int): integer of the scaled up input

        """
        return int(round(100 * value))

    def _update_mean(self, values_sum, values_count: int):
        """Not to be called externally. Update the current stored mean info with the mean from the input data.

        Args:
            values(iterable): iterable of integers
            values_count(int): count of integers in values

        """
        new_weight = self.mean_weight + values_count
        self.mean = (self.mean * self.mean_weight + values_sum) / new_weight
        self.mean_weight = new_weight

    def add_invoice(self, value: (int, float)):
        """Add an invoice to the statistical data.

        Args:
            value(float, int): invoice in dollars and cents

        """
        self.check_input([value])
        value = self.scale_up(value)
        self.insert(value)
        self._update_mean(value, 1)

    def add_invoices(self, values: list):
        """Add multiple invoices to the statistical data

        Args:
            values(list): list of floats or integers

        """
        self.check_input(values)
        values_count = len(values)
        values = map(self.scale_up, values)
        values_sum = self.insert_list(values)
        self._update_mean(values_sum, values_count)

    def clear(self):
        """Clear the statistical data, resetting the mean and median"""
        self.mean = 0
        self.mean_weight = 0
        super().clear()

    def get_median(self):
        """Returns the statistical median for the added data. Returns None if no data was added."""
        if self.max_pq:
            return round(self.median() / 100, ndigits=2)

    def get_mean(self):
        """Returns the statistical mean for the added data. Returns None if no data was added."""
        if self.mean:
            return round(self.mean / 100, ndigits=2)


