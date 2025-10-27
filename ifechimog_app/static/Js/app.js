
document.addEventListener("DOMContentLoaded", function () {

  // --- PAYSTACK PAYMENT ---
  const payBtn = document.querySelector('button[onclick="payWithPaystack()"]');
  if (payBtn) {
    window.payWithPaystack = function () {
      const email = document.getElementById('email')?.value;
      const phone = document.getElementById('phone')?.value;
      const fullname = document.getElementById('fullname')?.value;
      if (!email || !phone || !fullname) {
        alert('Please fill out all required fields before proceeding to payment.');
        return;
      }

      var handler = PaystackPop.setup({
        key: 'YOUR_PUBLIC_KEY_HERE',
        email: email,
        amount: 35000 * 100,
        currency: 'NGN',
        ref: 'IFCHM_' + Math.floor((Math.random() * 1000000000) + 1),
        metadata: {
          custom_fields: [
            { display_name: "Full Name", variable_name: "fullname", value: fullname },
            { display_name: "Phone", variable_name: "phone", value: phone }
          ]
        },
        callback: function (response) {
          alert('Payment successful. Transaction reference: ' + response.reference);
          window.location.href = "order-success.html";
        },
        onClose: function () {
          alert('Payment window closed.');
        }
      });
      handler.openIframe();
    }
  }

  // --- LAUNDRY PRICE CALCULATOR ---
  const priceForm = document.getElementById('price-form');
  if (priceForm) {
    priceForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const service = document.getElementById('service-type').value;
      const qty = parseInt(document.getElementById('quantity').value);
      let pricePerItem = 0;

      if (service === 'Wash & Fold') pricePerItem = 300;
      else if (service === 'Dry Clean') pricePerItem = 500;
      else if (service === 'Ironing') pricePerItem = 200;

      const total = qty * pricePerItem;
      document.getElementById('price-result').textContent = `Estimated Total: ₦${total.toLocaleString()}`;
    });
  }

  // --- TRACK ORDER PAGE ---
  const trackForm = document.getElementById('track-form');
  if (trackForm) {
    trackForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const trackId = document.getElementById('tracking-id').value.trim();
      const resultBox = document.getElementById('tracking-result');
      const status = document.getElementById('tracking-status');

      if (!trackId) {
        status.textContent = 'Please enter a valid tracking ID.';
        resultBox.style.display = 'block';
        return;
      }

      status.textContent = 'Tracking ID ' + trackId + ' is currently Out for Delivery 🚚';
      resultBox.style.display = 'block';
    });
  }

  // --- SUPPORT WIDGET TOGGLE ---
  const supportBtn = document.getElementById('support-chat-btn');
  const supportWindow = document.getElementById('support-chat-window');
  if (supportBtn && supportWindow) {
    supportBtn.addEventListener('click', () => {
      supportWindow.style.display = supportWindow.style.display === 'flex' ? 'none' : 'flex';
    });
  }

  // --- SUPPORT SEND MESSAGE IN CHAT WINDOW ---
  const chatInput = document.querySelector('#support-chat-window textarea');
  const sendBtn = document.querySelector('#support-chat-window button');
  if (chatInput && sendBtn) {
    sendBtn.addEventListener('click', function () {
      const message = chatInput.value.trim();
      if (message) {
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble user';
        bubble.textContent = message;
        document.querySelector('#support-chat-window').insertBefore(bubble, sendBtn.parentNode);
        chatInput.value = '';
      }
    });
  }

});


// --- LAUNDRY BOOKING STEPPER ---
const steps = document.querySelectorAll('#laundry-steps .step');
if (steps.length) {
  let current = 0;
  const prevBtn = document.getElementById('prev-step');
  const nextBtn = document.getElementById('next-step');

  const update = () => {
    steps.forEach((s, i) => s.classList.toggle('d-none', i !== current));
    prevBtn.disabled = current === 0;
    nextBtn.textContent = current === steps.length - 1 ? 'Submit' : 'Next';
  };

  prevBtn.addEventListener('click', () => {
    if (current > 0) {
      current--;
      update();
    }
  });

  nextBtn.addEventListener('click', () => {
    if (current < steps.length - 1) {
      current++;
      update();
    } else {
      alert('Laundry booking submitted!');
      window.location.href = 'booking-success.html';
    }
  });

  update();
}
