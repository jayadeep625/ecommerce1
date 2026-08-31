@login_required
def payment(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():
        return redirect("cart")

    address_id = request.session.get(
        "selected_address"
    )

    if not address_id:

        messages.error(
            request,
            "Please select an address first."
        )

        return redirect("checkout")

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    total = sum(
        (
            item.product.price * item.quantity
            for item in cart_items
        ),
        Decimal("0")
    )

    # =====================================
    # POST
    # =====================================

    if request.method == "POST":

        payment_method = request.POST.get(
            "payment"
        )

        print("PAYMENT METHOD:", payment_method)


        # =================================
        # CASH ON DELIVERY
        # =================================

        if payment_method == "COD":

            request.session["payment"] = "COD"

            return redirect("place_order")


        # =================================
        # RAZORPAY
        # =================================

        if payment_method == "Razorpay":

            print("RAZORPAY SELECTED")


            amount_paise = int(
                total * 100
            )


            # Create Razorpay Order

            razorpay_order = razorpay_client.order.create({

                "amount": amount_paise,

                "currency": "INR",

                "receipt":
                    f"receipt_{request.user.id}",

                "payment_capture": 1,

            })


            print(
                "RAZORPAY ORDER:",
                razorpay_order
            )


            # Save Razorpay order ID

            request.session[
                "razorpay_order_id"
            ] = razorpay_order["id"]


            request.session[
                "selected_payment"
            ] = "Razorpay"


            # IMPORTANT:
            # Render Razorpay page

            return render(
                request,
                "orders/razorpay.html",
                {

                    "razorpay_key":
                        settings.RAZORPAY_KEY_ID,

                    "razorpay_order_id":
                        razorpay_order["id"],

                    "amount":
                        amount_paise,

                    "total":
                        total,

                    "user_name":
                        request.user.get_full_name()
                        or request.user.username,

                    "user_email":
                        request.user.email,

                    "user_phone":
                        address.phone,

                }
            )


    # =====================================
    # GET
    # =====================================

    return render(
        request,
        "orders/payment.html",
        {
            "total": total,
            "address": address,
        }
    )