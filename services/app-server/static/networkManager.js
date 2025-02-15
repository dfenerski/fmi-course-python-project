class NetworkManager {
    static #getCookie(name) {
        const cookieString = document.cookie;
        const cookies = cookieString.split('; ').reduce((acc, cookie) => {
            const [key, value] = cookie.split('=');
            acc[key] = value;
            return acc;
        }, {});
        return cookies[name] || null;
    }

    static #getCSRFToken() {
        return this.#getCookie('csrftoken');
    }

    static async request(method, payload, extraHeaders = {}) {
        const csrfToken = this.#getCSRFToken();

        if (!csrfToken) {
            throw new Error('CSRF token not found.');
        }

        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            ...extraHeaders,
        };

        const response = await fetch(window.location.href, {
            method,
            headers,
            credentials: 'same-origin',
            body: JSON.stringify(payload),
        });

        return response;
    }
}
