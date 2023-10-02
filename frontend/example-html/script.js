async function decrypt(ciphertext, password) {
    const pwUtf8 = new TextEncoder().encode(password);
    const pwHash = await crypto.subtle.digest('SHA-256', pwUtf8);
    const ctUtf8 = new Uint8Array(ciphertext);
    const iv = ctUtf8.slice(0, 12);
    const alg = { name: 'AES-GCM', iv: iv, additionalData: iv };
    const key = await crypto.subtle.importKey('raw', pwHash, alg, false, ['decrypt']);
    try {
        const buf = await crypto.subtle.decrypt(alg, key, ctUtf8.slice(12));
        return new TextDecoder().decode(buf);
    } catch (e) {
        throw new Error('Decrypt failed')
    }
}

function setError(text) {
    document.getElementById('msg').innerText = text;
}

function setFields(elem, fields) {
    for (const [k, v] of Object.entries(fields)) {
        for (const el of elem.querySelectorAll('#' + k)) {
            el.innerText = v;
        }
    }
}

async function apply(data, password) {
    const json = JSON.parse(await decrypt(data, password));
    const now = new Date().getTime();
    const vA = new Date(json['valid_since'] + 'T00:00:00');
    if (vA.getTime() > now) {
        return setError('Member card not valid yet');
    }
    const vZ = new Date(json['valid_until'] + 'T23:59:59');
    if (vZ.getTime() < now) {
        return setError('Member card expired');
    }
    const pass = document.getElementById('pass');
    const imgElem = pass.querySelector('#img');
    if (imgElem) {
        if (json['img']) {
            imgElem.src = 'data:image;base64,' + json['img'];
        } else {
            imgElem.src = 'img/no-img.svg';
        }
    }
    setFields(pass, {
        name: json['name'],
        member_id: json['id'],
        org_name: json['org'],
        valid: 'on ' + new Date().toLocaleDateString('en'),
    });
    setFields(pass, json['data']); // may overwrite previous fields

    const title = 'Member card for ' + json['name'] + ' – ' + json['org'];
    document.head.querySelector('title').innerText = title;
    document.getElementById('msg').classList.add('hidden');
    pass.classList.remove('hidden');
}

async function onLoad() {
    // reset previous download
    document.getElementById('pass').classList.add('hidden');
    const msg = document.getElementById('msg');
    msg.innerText = msg.dataset.load;
    msg.classList.remove('hidden');
    // download new data
    const [org, uuid, secret] = location.hash.slice(1).split('/');
    if (!org || !uuid || !secret) {
        return setError('Invalid URL');
    }
    const res = await fetch('./data/' + org + '/' + uuid);
    if (!res.ok) {
        return setError('Error loading\n\n' + res.status + ' ' + res.statusText);
    }
    try {
        const data = await res.arrayBuffer();
        await apply(data, secret);
    } catch (e) {
        setError(e);
    }
}

// load and parse data
window.onload = onLoad;
// force reload if hash params change
window.addEventListener('hashchange', onLoad, true);

// -------------
// scale-up card
// -------------

function onResize() {
    const card = document.getElementById('card');
    const sw = window.innerWidth / card.offsetWidth;
    const sh = window.innerHeight / card.offsetHeight;
    card.style.scale = Math.min(Math.min(sw, sh) * 0.97, 2);
}

window.addEventListener('resize', onResize, true);
window.addEventListener('orientationchange', onResize, true);
screen?.orientation?.addEventListener('change', onResize, true);

// -----------------
// check for updates
// -----------------

lastUpdate = new Date().getTime();

function needsUpdate() {
    // reload page if older than 15min
    const now = new Date().getTime();
    if (now - lastUpdate > 900_000) {
        lastUpdate = now;
        onLoad();
    }
}
// setInterval(needsUpdate, 1000);
window.addEventListener('focus', needsUpdate, true);
window.addEventListener('pageshow', needsUpdate, true);
window.addEventListener('visibilitychange', function () {
    !document.hidden && document.visibilityState !== 'hidden' && needsUpdate();
}, true);
