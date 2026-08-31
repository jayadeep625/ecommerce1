// ==========================================
// NOTIFICATION SYSTEM
// ==========================================

let notifications = [];
let notificationAudioContext = null;


// ==========================================
// SOUND SYSTEM
// ==========================================

function initializeNotificationSound() {

    if (!notificationAudioContext) {

        notificationAudioContext =
            new (window.AudioContext ||
                 window.webkitAudioContext)();

        console.log("🔊 Notification audio initialized");
    }

    if (
        notificationAudioContext.state === "suspended"
    ) {

        notificationAudioContext.resume()
            .then(() => {
                console.log("🔊 Notification audio unlocked");
            })
            .catch(error => {
                console.error(
                    "Audio unlock failed:",
                    error
                );
            });
    }
}


// Unlock audio after ANY user interaction
document.addEventListener(
    "click",
    initializeNotificationSound,
    { once: true }
);


// ==========================================
// PLAY NOTIFICATION SOUND
// ==========================================

function playNotificationSound() {

    console.log("🔊 Playing notification sound...");

    if (!notificationAudioContext) {

        console.warn(
            "Notification audio is not initialized."
        );

        return;
    }

    if (
        notificationAudioContext.state === "suspended"
    ) {

        notificationAudioContext.resume();
    }


    const now =
        notificationAudioContext.currentTime;


    // First tone
    const oscillator1 =
        notificationAudioContext.createOscillator();

    const gain1 =
        notificationAudioContext.createGain();


    oscillator1.type = "sine";

    oscillator1.frequency.setValueAtTime(
        880,
        now
    );


    gain1.gain.setValueAtTime(
        0.001,
        now
    );

    gain1.gain.exponentialRampToValueAtTime(
        0.35,
        now + 0.02
    );

    gain1.gain.exponentialRampToValueAtTime(
        0.001,
        now + 0.25
    );


    oscillator1.connect(gain1);

    gain1.connect(
        notificationAudioContext.destination
    );


    oscillator1.start(now);

    oscillator1.stop(
        now + 0.25
    );


    // Second tone
    const oscillator2 =
        notificationAudioContext.createOscillator();

    const gain2 =
        notificationAudioContext.createGain();


    oscillator2.type = "sine";

    oscillator2.frequency.setValueAtTime(
        1175,
        now + 0.20
    );


    gain2.gain.setValueAtTime(
        0.001,
        now + 0.20
    );

    gain2.gain.exponentialRampToValueAtTime(
        0.35,
        now + 0.22
    );

    gain2.gain.exponentialRampToValueAtTime(
        0.001,
        now + 0.45
    );


    oscillator2.connect(gain2);

    gain2.connect(
        notificationAudioContext.destination
    );


    oscillator2.start(
        now + 0.20
    );

    oscillator2.stop(
        now + 0.45
    );


    console.log(
        "🔊 Notification sound played!"
    );
}


// ==========================================
// MAIN NOTIFICATION SYSTEM
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const bell =
            document.getElementById(
                "notificationBell"
            );

        if (!bell) {

            console.log(
                "Notification UI not found."
            );

            return;
        }


        console.log(
            "🔔 Notification system starting..."
        );


        // ==========================================
        // WEBSOCKET
        // ==========================================

        const protocol =
            window.location.protocol === "https:"
                ? "wss"
                : "ws";


        const socketUrl =
            protocol +
            "://" +
            window.location.host +
            "/ws/notifications/";


        console.log(
            "Connecting WebSocket:",
            socketUrl
        );


        const notificationSocket =
            new WebSocket(socketUrl);


        // ==========================================
        // CONNECTED
        // ==========================================

        notificationSocket.onopen =
            function () {

                console.log(
                    "🔔 Notification WebSocket connected!"
                );
            };


        // ==========================================
        // NEW NOTIFICATION
        // ==========================================

        notificationSocket.onmessage =
            function (event) {

                console.log(
                    "🔔 NEW NOTIFICATION RECEIVED:",
                    event.data
                );


                let data;

                try {

                    data =
                        JSON.parse(event.data);

                } catch (error) {

                    console.error(
                        "Invalid notification data:",
                        error
                    );

                    return;
                }


                // 🔊 INITIALIZE AND PLAY SOUND
initializeNotificationSound();
playNotificationSound();



                // ==========================================
                // ADD TO NOTIFICATION LIST
                // ==========================================

                addNotificationToUI(data);


                // ==========================================
                // UPDATE BADGE
                // ==========================================

                updateNotificationBadge();


                // ==========================================
                // SHOW TOAST
                // ==========================================

                showToast(
                    data.title,
                    data.message
                );


                // ==========================================
                // BROWSER NOTIFICATION
                // ==========================================

                if (
                    "Notification" in window &&
                    Notification.permission === "granted"
                ) {

                    new Notification(
                        data.title,
                        {
                            body: data.message
                        }
                    );
                }
            };


        // ==========================================
        // WEBSOCKET ERROR
        // ==========================================

        notificationSocket.onerror =
            function (error) {

                console.error(
                    "❌ WebSocket error:",
                    error
                );
            };


        // ==========================================
        // WEBSOCKET CLOSED
        // ==========================================

        notificationSocket.onclose =
            function () {

                console.log(
                    "❌ Notification WebSocket disconnected."
                );
            };


        // ==========================================
        // BELL
        // ==========================================

        const dropdown =
            document.getElementById(
                "notificationDropdown"
            );
        if (dropdown) {
    dropdown.style.display = "none";
}


        bell.addEventListener("click", function (event) {

    event.stopPropagation();

    // Unlock sound on bell click
    initializeNotificationSound();

    const isHidden =
        dropdown.style.display === "none";

    if (isHidden) {

        dropdown.style.display = "block";

        loadNotifications();

    } else {

        dropdown.style.display = "none";

    }

});


        // ==========================================
        // CLOSE DROPDOWN
        // ==========================================

         document.addEventListener("click", function (event) {

    if (!event.target.closest(".notification-wrapper")) {
        dropdown.classList.remove("show");
    }

});


        // ==========================================
        // MARK ALL READ
        // ==========================================

        const markAllButton =
            document.getElementById(
                "markAllReadButton"
            );


        if (markAllButton) {

            markAllButton.addEventListener(
                "click",
                function () {

                    fetch(
                        "/notifications/read-all/",
                        {
                            method: "POST",

                            headers: {
                                "X-CSRFToken":
                                    getCSRFToken()
                            }
                        }
                    )
                    .then(
                        response =>
                            response.json()
                    )
                    .then(
                        data => {

                            if (data.success) {

                                notifications =
                                    notifications.map(
                                        notification => ({
                                            ...notification,
                                            is_read: true
                                        })
                                    );


                                renderNotifications();

                                updateNotificationBadge();
                            }
                        }
                    )
                    .catch(
                        error => {

                            console.error(
                                "Mark all read error:",
                                error
                            );
                        }
                    );
                }
            );
        }


        // ==========================================
        // LOAD NOTIFICATIONS
        // ==========================================

        function loadNotifications() {

            fetch(
                "/notifications/"
            )
            .then(
                response =>
                    response.json()
            )
            .then(
                data => {

                    notifications =
                        data.notifications || [];


                    renderNotifications();

                    updateNotificationBadge();
                }
            )
            .catch(
                error => {

                    console.error(
                        "Notification loading error:",
                        error
                    );
                }
            );
        }


        // ==========================================
        // ADD NOTIFICATION
        // ==========================================

        function addNotificationToUI(
            notification
        ) {

            notifications.unshift({

                id:
                    notification.id,

                title:
                    notification.title,

                message:
                    notification.message,

                notification_type:
                    notification.notification_type,

                created_at:
                    notification.created_at,

                is_read:
                    false
            });


            notifications =
                notifications.slice(
                    0,
                    50
                );


            renderNotifications();
        }


        // ==========================================
        // RENDER
        // ==========================================

        function renderNotifications() {

            const list =
                document.getElementById(
                    "notificationList"
                );


            if (!list) {
                return;
            }


            list.innerHTML = "";


            if (
                notifications.length ===
                0
            ) {

                list.innerHTML =
                    `
                    <div class="notification-empty">
                        No notifications yet.
                    </div>
                    `;

                return;
            }


            notifications.forEach(
                notification => {

                    const item =
                        document.createElement(
                            "div"
                        );


                    item.className =
                        "notification-item" +
                        (
                            notification.is_read
                                ? ""
                                : " unread"
                        );


                    item.innerHTML =
                        `
                        <div class="notification-title">
                            ${escapeHtml(
                                notification.title
                            )}
                        </div>

                        <div class="notification-message">
                            ${escapeHtml(
                                notification.message
                            )}
                        </div>

                        <div class="notification-time">
                            ${formatTime(
                                notification.created_at
                            )}
                        </div>
                        `;


                    item.addEventListener(
                        "click",
                        function () {

                            markAsRead(
                                notification.id
                            );
                        }
                    );


                    list.appendChild(item);
                }
            );
        }


        // ==========================================
        // MARK AS READ
        // ==========================================

        function markAsRead(id) {

            fetch(
                `/notifications/${id}/read/`,
                {
                    method: "POST",

                    headers: {
                        "X-CSRFToken":
                            getCSRFToken()
                    }
                }
            )
            .then(
                response =>
                    response.json()
            )
            .then(
                data => {

                    if (data.success) {

                        const notification =
                            notifications.find(
                                n =>
                                    n.id === id
                            );


                        if (notification) {

                            notification.is_read =
                                true;
                        }


                        renderNotifications();

                        updateNotificationBadge();
                    }
                }
            )
            .catch(
                error => {

                    console.error(
                        "Mark read error:",
                        error
                    );
                }
            );
        }


        // ==========================================
        // BADGE
        // ==========================================

        function updateNotificationBadge() {

            const badge =
                document.getElementById(
                    "notificationBadge"
                );


            if (!badge) {
                return;
            }


            const unread =
                notifications.filter(
                    notification =>
                        !notification.is_read
                ).length;


            if (unread > 0) {

                badge.textContent =
                    unread > 99
                        ? "99+"
                        : unread;

                badge.style.display =
                    "block";

            } else {

                badge.style.display =
                    "none";
            }
        }


        // ==========================================
        // TOAST
        // ==========================================

        function showToast(
            title,
            message
        ) {

            const toast =
                document.createElement(
                    "div"
                );


            toast.className =
                "notification-toast";


            toast.innerHTML =
                `
                <strong>
                    ${escapeHtml(title)}
                </strong>

                <div>
                    ${escapeHtml(message)}
                </div>
                `;


            document.body.appendChild(
                toast
            );


            setTimeout(
                function () {

                    toast.remove();

                },
                5000
            );
        }


        // ==========================================
        // FORMAT TIME
        // ==========================================

        function formatTime(
            dateString
        ) {

            return new Date(
                dateString
            ).toLocaleString();
        }


        // ==========================================
        // ESCAPE HTML
        // ==========================================

        function escapeHtml(
            value
        ) {

            const div =
                document.createElement(
                    "div"
                );


            div.textContent =
                value;


            return div.innerHTML;
        }


        // ==========================================
        // CSRF
        // ==========================================

        function getCSRFToken() {

            const cookie =
                document.cookie
                    .split("; ")
                    .find(
                        row =>
                            row.startsWith(
                                "csrftoken="
                            )
                    );


            return cookie
                ? decodeURIComponent(
                    cookie.split("=")[1]
                )
                : "";
        }


        // ==========================================
        // BROWSER NOTIFICATION PERMISSION
        // ==========================================

        if (
            "Notification" in window &&
            Notification.permission ===
                "default"
        ) {

            Notification.requestPermission();
        }


        // ==========================================
        // LOAD EXISTING NOTIFICATIONS
        // ==========================================

        loadNotifications();

    }
);