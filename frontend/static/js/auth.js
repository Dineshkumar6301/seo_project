
  // ── TAB SWITCH ──
  function showLogin(btn){
    document.getElementById("loginBox").style.display = "block";
    document.getElementById("registerBox").style.display = "none";
    document.getElementById("cardTitle").innerText = "Welcome back";
    document.getElementById("cardSub").innerText = "Sign in to your account to continue";
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }

  function showRegister(btn){
    document.getElementById("loginBox").style.display = "none";
    document.getElementById("registerBox").style.display = "block";
    document.getElementById("cardTitle").innerText = "Create account";
    document.getElementById("cardSub").innerText = "Fill in your details to get started";
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }

  // ── TOAST ──
  function showToast(msg, type=""){
    const t = document.getElementById("toast");
    t.innerText = msg;
    t.className = "toast-bar " + type + " show";
    setTimeout(() => { t.classList.remove("show"); }, 3200);
  }

  // ── REGISTER ──
  document.getElementById("registerForm").addEventListener("submit", async function(e){
    e.preventDefault();
    const password = this.password.value;
    const confirm  = this.confirm_password.value;

    if(password !== confirm){
      showToast("⚠️ Passwords do not match", "error");
      return;
    }

    const res = await fetch("/api/accounts/register/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        first_name: this.first_name.value,
        last_name:  this.last_name.value,
        mobile:     this.mobile.value,
        email:      this.email.value,
        password:   password,
        role:       this.role.value
      })
    });

    const data = await res.json();

    if(res.status === 201){
      showToast("✅ Registered successfully!", "success");
      setTimeout(() => showLogin(document.querySelectorAll('.tab-btn')[0]), 1200);
    } else {
      showToast("❌ " + JSON.stringify(data), "error");
    }
  });

  document
.getElementById("loginForm")

.addEventListener(
    "submit",

async function(e){

    e.preventDefault();

    try {

        const res = await fetch(

            "/api/accounts/login/",

            {
                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                credentials: "same-origin",

                body: JSON.stringify({

                    email:
                        this.email.value,

                    password:
                        this.password.value
                })
            }
        );

        const data = await res.json();

        // SUCCESS
        if (res.ok && data.status === "success") {

            showToast(
                "✅ Login successful",
                "success"
            );

            setTimeout(() => {

                window.location.href =
                    data.redirect;

            }, 300);

            return;
        }

        // FAILED
        showToast(

            "❌ " +

            (
                data.message ||

                "Invalid email or password"
            ),

            "error"
        );

    } catch(err){

        console.log(err);

        showToast(
            "❌ Network error",
            "error"
        );
    }
});
function openForgotModal(){
  document.getElementById("forgotModal").style.display = "flex";
}

function closeForgotModal(){
  document.getElementById("forgotModal").style.display = "none";
}
/* CSRF */
function getCSRFToken() {
  const match = document.cookie.match(/(^| )csrftoken=([^;]+)/);
  return match ? match[2] : "";
}

/* STATE */
let lastRequestTime = 0;
let isSending = false;

/* SEND RESET LINK */
async function sendResetLink(){

  console.log("SEND CLICKED"); // debug

  const now = Date.now();

  // 🚫 BLOCK FRONTEND SPAM (1 min)
  if (now - lastRequestTime < 60000) {
    showToast("⏳ Already sent. Check your email.", "success");
    return;
  }

  if(isSending){
    return; // prevent double click instantly
  }

  const email = document.getElementById("forgotEmail").value.trim();

  if(!email){
    showToast("⚠️ Enter email", "error");
    return;
  }

  isSending = true;
  lastRequestTime = now;

  try {
    showToast("⏳ Sending reset link...");

    const res = await fetch("/activities/forget_password/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      },
      body: JSON.stringify({ email })
    });

    let data = {};
    try {
      data = await res.json(); // safe parse
    } catch(e){
      console.warn("Invalid JSON response");
    }

    if(res.status === 200){
      showToast("📩 Reset link sent. Check your email.", "success");

      // delay close for UX
      setTimeout(() => {
        closeForgotModal();
      }, 1200);

    } else {
      showToast("❌ " + (data.error || "Failed to send"), "error");
      lastRequestTime = 0; 
    }

  } catch (err){
    console.error(err);
    showToast("❌ Network error", "error");
    lastRequestTime = 0; // allow retry
  }

  isSending = false;
}

/* AUTO OPEN FROM LINK */
window.addEventListener("load", function () {
  const params = new URLSearchParams(window.location.search);

  const email = params.get("email");
  const token = params.get("token");

  if (email && token) {

    localStorage.setItem("reset_email", email);
    localStorage.setItem("reset_token", token);

    openForgotModal();

    document.getElementById("forgotStep1").style.display = "none";
    document.getElementById("forgotStep2").style.display = "block";

    window.history.replaceState({}, document.title, "/");
  }
});

/* RESET PASSWORD */
async function resetPassword(){

  const password = document.getElementById("newPassword").value;
  const confirm  = document.getElementById("confirmPassword").value;

  if(!password || !confirm){
    showToast("⚠️ Fill all fields", "error");
    return;
  }

  if(password !== confirm){
    showToast("⚠️ Password mismatch", "error");
    return;
  }

  const email = localStorage.getItem("reset_email");
  const token = localStorage.getItem("reset_token");

  if(!email || !token){
    showToast("❌ Session expired. Try again.", "error");
    return;
  }

  try {
    showToast("⏳ Updating password...");

    const res = await fetch("/activities/reset_password/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      },
      body: JSON.stringify({
        email: email,
        token: token,
        password: password
      })
    });

    let data = {};
    try {
      data = await res.json();
    } catch(e){
      console.warn("Invalid JSON response");
    }

    if(res.status === 200){
      showToast("✅ Password updated", "success");

      localStorage.removeItem("reset_email");
      localStorage.removeItem("reset_token");

      setTimeout(() => {
        closeForgotModal();
        showLogin(document.querySelectorAll('.tab-btn')[0]);
      }, 1000);

    } else {
      showToast("❌ " + (data.error || "Invalid or expired link"), "error");
    }

  } catch (err){
    console.error(err);
    showToast("❌ Network error", "error");
  }
}

