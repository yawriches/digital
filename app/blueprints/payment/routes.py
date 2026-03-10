import hashlib
import hmac
import json
import requests
from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app.blueprints.payment import payment_bp
from app.extensions import db, csrf
from app.models import Order, CartItem


@payment_bp.route('/initialize/<int:order_id>')
@login_required
def initialize(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()

    if order.payment_status == 'paid':
        flash('This order has already been paid.', 'info')
        return redirect(url_for('main.order_confirmation', order_number=order.order_number))

    paystack_secret = current_app.config.get('PAYSTACK_SECRET_KEY', '')
    paystack_public = current_app.config.get('PAYSTACK_PUBLIC_KEY', '')

    if not paystack_secret or not paystack_public:
        order.payment_status = 'paid'
        order.status = 'processing'
        order.payment_reference = 'DEMO-NO-PAYSTACK'
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('Payment successful (demo mode).', 'success')
        return redirect(url_for('main.order_confirmation', order_number=order.order_number))

    amount_kobo = int(order.total_amount * 100)

    headers = {
        'Authorization': f'Bearer {paystack_secret}',
        'Content-Type': 'application/json'
    }
    data = {
        'email': current_user.email,
        'amount': amount_kobo,
        'currency': 'GHS',
        'reference': order.order_number,
        'callback_url': url_for('payment.verify', order_id=order.id, _external=True),
        'metadata': {
            'order_id': order.id,
            'order_number': order.order_number
        }
    }

    try:
        resp = requests.post('https://api.paystack.co/transaction/initialize',
                             headers=headers, json=data, timeout=30)
        result = resp.json()
        
        # Debug logging
        print(f"Paystack Response Status: {resp.status_code}")
        print(f"Paystack Response: {result}")
        
        if result.get('status'):
            return redirect(result['data']['authorization_url'])
        else:
            error_msg = result.get('message', 'Payment initialization failed')
            flash(f'Payment failed: {error_msg}', 'danger')
            return redirect(url_for('main.checkout'))
    except Exception as e:
        print(f"Paystack Exception: {str(e)}")
        flash('Payment service unavailable. Please try again later.', 'danger')
        return redirect(url_for('main.checkout'))


@payment_bp.route('/verify/<int:order_id>')
@login_required
def verify(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    reference = request.args.get('reference', order.order_number)

    paystack_secret = current_app.config.get('PAYSTACK_SECRET_KEY', '')

    if not paystack_secret:
        order.payment_status = 'paid'
        order.status = 'processing'
        order.payment_reference = reference
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('Payment verified (demo mode).', 'success')
        return redirect(url_for('main.order_confirmation', order_number=order.order_number))

    headers = {'Authorization': f'Bearer {paystack_secret}'}

    try:
        resp = requests.get(f'https://api.paystack.co/transaction/verify/{reference}',
                            headers=headers, timeout=30)
        result = resp.json()

        if result.get('status') and result['data']['status'] == 'success':
            order.payment_status = 'paid'
            order.status = 'processing'
            order.payment_reference = reference
            CartItem.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash('Payment successful!', 'success')
            return redirect(url_for('main.order_confirmation', order_number=order.order_number))
        else:
            flash('Payment verification failed.', 'danger')
            return redirect(url_for('main.order_detail', order_number=order.order_number))
    except Exception:
        flash('Could not verify payment. Please contact support.', 'danger')
        return redirect(url_for('main.order_detail', order_number=order.order_number))


@payment_bp.route('/webhook', methods=['POST'])
@csrf.exempt
def webhook():
    payload = request.get_data()
    signature = request.headers.get('X-Paystack-Signature', '')
    paystack_secret = current_app.config.get('PAYSTACK_SECRET_KEY', '')

    if paystack_secret:
        expected = hmac.new(
            paystack_secret.encode('utf-8'),
            payload,
            hashlib.sha512
        ).hexdigest()

        if signature != expected:
            return jsonify({'error': 'Invalid signature'}), 400

    data = json.loads(payload)
    event = data.get('event', '')

    if event == 'charge.success':
        ref = data['data']['reference']
        order = Order.query.filter_by(order_number=ref).first()
        if order:
            order.payment_status = 'paid'
            order.status = 'processing'
            order.payment_reference = ref
            CartItem.query.filter_by(user_id=order.user_id).delete()
            db.session.commit()

    return jsonify({'status': 'ok'}), 200
