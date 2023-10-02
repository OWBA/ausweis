async function decrypt(ciphertext, password) {
	const pwUtf8 = new TextEncoder().encode(password);
	const pwHash = await crypto.subtle.digest('SHA-256', pwUtf8);
	const ctUtf8 = new Uint8Array(Array.from(atob(ciphertext)).map(x => x.charCodeAt(0)));
	const alg = { name: 'AES-GCM', iv: ctUtf8.slice(0,12) };
	const key = await crypto.subtle.importKey('raw', pwHash, alg, false, ['decrypt']);
	try {
		const buf = await crypto.subtle.decrypt(alg, key, ctUtf8.slice(12));
		return new TextDecoder().decode(buf);
	} catch (e) {
		throw new Error('Decrypt failed')
	}
}
