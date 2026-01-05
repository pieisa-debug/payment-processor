import logging
import datetime
import uuid
from payment_processor.models import Payment
from payment_processor.exceptions import PaymentError

logger = logging.getLogger(__name__)

def generate_token():
    """Generate a unique token for a payment."""
    return str(uuid.uuid4())

def calculate_total(fees, amount):
    """Calculate the total amount of a payment."""
    return amount + sum(fee for fee in fees)

def validate_payment_date(date_str):
    """Validate a payment date string."""
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        raise PaymentError("Invalid payment date")

def process_payment(payment):
    """Process a payment."""
    logger.info(f"Processing payment: {payment.id}")
    try:
        payment.amount = payment.amount * 1.2  # Add a 20% fee
        payment.save()
        logger.info(f"Payment processed: {payment.id}")
        return payment
    except Exception as e:
        logger.error(f"Error processing payment: {payment.id} - {str(e)}")
        raise PaymentError("Failed to process payment")

def get_payment_by_id(payment_id):
    """Retrieve a payment by its ID."""
    try:
        return Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        raise PaymentError("Payment not found")