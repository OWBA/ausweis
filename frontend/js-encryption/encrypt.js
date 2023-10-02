async function encrypt(plaintext, password) {
	const pwUtf8 = new TextEncoder().encode(password);
	const pwHash = await crypto.subtle.digest('SHA-256', pwUtf8);
	const iv = crypto.getRandomValues(new Uint8Array(12));
	const alg = { name: 'AES-GCM', iv: iv };
	const key = await crypto.subtle.importKey('raw', pwHash, alg, false, ['encrypt']);
	const ptUint8 = new TextEncoder().encode(plaintext);
	const buf = await crypto.subtle.encrypt(alg, key, ptUint8);
	const ctStr = Array.from(new Uint8Array(buf)).map(b => String.fromCharCode(b)).join('');
	return btoa(String.fromCharCode(...iv) + ctStr);
}
